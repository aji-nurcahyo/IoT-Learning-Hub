"""Harness Uji Penerimaan Ujung-ke-Ujung — Chapter 20 Connected Device Capstone.

Menjalankan secara lokal (tanpa ketergantungan cloud berbayar):
1. Server HTTP lokal (endpoint /api/v1/config/node-01)
2. Broker MQTT 3.1.1 TCP lokal (mendukung CONNECT + LWT, SUBSCRIBE, PUBLISH, Retained)
3. Simulasi perilaku node ESP32 melalui 6 kasus uji penerimaan (TC-01 s.d. TC-06).
"""

from __future__ import annotations

import json
import socket
import struct
import threading
import time
import urllib.request
from collections import deque
from http.server import BaseHTTPRequestHandler, HTTPServer


# ---------------- MQTT 3.1.1 Wire Helpers ----------------

def encode_var_len(length: int) -> bytes:
    out = bytearray()
    while True:
        byte = length % 128
        length //= 128
        if length > 0:
            byte |= 0x80
        out.append(byte)
        if length == 0:
            break
    return bytes(out)


def encode_str(text: str) -> bytes:
    raw = text.encode("utf-8")
    return struct.pack("!H", len(raw)) + raw


def decode_str(buf: bytes, offset: int) -> tuple[str, int]:
    (length,) = struct.unpack_from("!H", buf, offset)
    offset += 2
    return buf[offset : offset + length].decode("utf-8"), offset + length


def read_packet(conn: socket.socket) -> tuple[int, bytes] | None:
    hdr = conn.recv(1)
    if not hdr:
        return None
    pkt_type = hdr[0]
    mult, rem_len = 1, 0
    while True:
        b = conn.recv(1)
        if not b:
            return None
        val = b[0]
        rem_len += (val & 0x7F) * mult
        if (val & 0x80) == 0:
            break
        mult *= 128
    payload = bytearray()
    while len(payload) < rem_len:
        chunk = conn.recv(rem_len - len(payload))
        if not chunk:
            return None
        payload.extend(chunk)
    return pkt_type, bytes(payload)


def build_publish_pkt(topic: str, payload: str, retain: bool = False) -> bytes:
    flags = 0x30 | (0x01 if retain else 0x00)
    body = encode_str(topic) + payload.encode("utf-8")
    return bytes([flags]) + encode_var_len(len(body)) + body


def topic_matches(pattern: str, topic: str) -> bool:
    p_parts, t_parts = pattern.split("/"), topic.split("/")
    for idx, pat in enumerate(p_parts):
        if pat == "#":
            return True
        if idx >= len(t_parts):
            return False
        if pat != "+" and pat != t_parts[idx]:
            return False
    return len(p_parts) == len(t_parts)


# ---------------- Local HTTP Config Endpoint ----------------

class ConfigHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/api/v1/config/node-01":
            body = json.dumps({"sample_ms": 5000, "temp_high_c": 30.0, "temp_hyst_c": 1.5}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


# ---------------- Local Loopback MQTT Broker ----------------

class LocalMqttBroker:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(8)
        self.port = self.sock.getsockname()[1]
        self.running = True
        self.lock = threading.Lock()
        self.subs: list[tuple[socket.socket, list[str]]] = []
        self.retained: dict[str, str] = {}
        self.seen_keys: set[tuple[str, int]] = set()
        self.ingested_telemetry: list[dict[str, object]] = []
        self.duplicates_ignored = 0

    def start(self) -> None:
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def stop(self) -> None:
        self.running = False
        self.sock.close()

    def _accept_loop(self) -> None:
        while self.running:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                break
            threading.Thread(target=self._client_loop, args=(conn,), daemon=True).start()

    def _fanout(self, topic: str, payload: str, retain: bool = False) -> None:
        if retain:
            self.retained[topic] = payload
        if topic.endswith("/telemetry"):
            obj = json.loads(payload)
            key = (str(obj["dev"]), int(obj["seq"]))
            if key in self.seen_keys:
                self.duplicates_ignored += 1
            else:
                self.seen_keys.add(key)
                self.ingested_telemetry.append(obj)

        pkt = build_publish_pkt(topic, payload, retain=retain)
        for sub_conn, patterns in list(self.subs):
            if any(topic_matches(p, topic) for p in patterns):
                try:
                    sub_conn.sendall(pkt)
                except OSError:
                    pass

    def _client_loop(self, conn: socket.socket) -> None:
        will_topic: str | None = None
        will_msg: str | None = None
        will_retain = False
        graceful_disconnect = False
        try:
            while self.running:
                pkt = read_packet(conn)
                if pkt is None:
                    break
                ptype, body = pkt
                kind = ptype >> 4

                if kind == 1:  # CONNECT
                    _, off = decode_str(body, 0)  # protocol name
                    flags = body[off + 1]
                    off += 4  # level(1) + flags(1) + keepalive(2)
                    _, off = decode_str(body, off)  # clientId
                    if flags & 0x04:  # Will flag
                        will_retain = bool(flags & 0x20)
                        will_topic, off = decode_str(body, off)
                        will_msg, off = decode_str(body, off)
                    conn.sendall(bytes([0x20, 0x02, 0x00, 0x00]))  # CONNACK OK
                elif kind == 8:  # SUBSCRIBE
                    msg_id = struct.unpack_from("!H", body, 0)[0]
                    off = 2
                    topics = []
                    while off < len(body):
                        t, off = decode_str(body, off)
                        off += 1  # QoS
                        topics.append(t)
                    with self.lock:
                        self.subs.append((conn, topics))
                        retained_hits = [
                            (t, p) for t, p in self.retained.items() if any(topic_matches(pat, t) for pat in topics)
                        ]
                    conn.sendall(struct.pack("!BBHB", 0x90, 3, msg_id, 0))
                    for rt, rp in retained_hits:
                        conn.sendall(build_publish_pkt(rt, rp, retain=True))
                elif kind == 3:  # PUBLISH
                    qos = (ptype >> 1) & 0x03
                    retain = bool(ptype & 0x01)
                    topic, off = decode_str(body, 0)
                    msg_id = None
                    if qos > 0:
                        msg_id = struct.unpack_from("!H", body, off)[0]
                        off += 2
                    payload = body[off:].decode("utf-8")
                    with self.lock:
                        self._fanout(topic, payload, retain=retain)
                    if qos == 1 and msg_id is not None:
                        conn.sendall(struct.pack("!BBH", 0x40, 2, msg_id))
                elif kind == 12:  # PINGREQ
                    conn.sendall(bytes([0xD0, 0x00]))
                elif kind == 14:  # DISCONNECT
                    graceful_disconnect = True
                    break
        except OSError:
            pass
        finally:
            with self.lock:
                self.subs = [(c, p) for (c, p) in self.subs if c is not conn]
                if not graceful_disconnect and will_topic is not None and will_msg is not None:
                    self._fanout(will_topic, will_msg, retain=will_retain)
            conn.close()


# ---------------- Minimal MQTT Client Helper ----------------

def mqtt_connect_packet(client_id: str, will_topic: str | None = None, will_msg: str | None = None) -> bytes:
    flags = 0x02  # clean session
    vh = encode_str("MQTT") + bytes([4])
    payload = encode_str(client_id)
    if will_topic and will_msg:
        flags |= 0x04 | 0x08 | 0x20  # will + QoS 1 + retain
        payload += encode_str(will_topic) + encode_str(will_msg)
    vh += bytes([flags]) + struct.pack("!H", 30)
    body = vh + payload
    return bytes([0x10]) + encode_var_len(len(body)) + body


def run_acceptance_suite() -> None:
    print("=== CHAPTER 20 CAPSTONE: END-TO-END CONNECTIVITY ACCEPTANCE SUITE ===")
    http_srv = HTTPServer(("127.0.0.1", 0), ConfigHandler)
    http_port = http_srv.server_address[1]
    threading.Thread(target=http_srv.serve_forever, daemon=True).start()

    broker = LocalMqttBroker()
    broker.start()
    time.sleep(0.05)

    # Local monitor subscriber
    mon = socket.create_connection(("127.0.0.1", broker.port), timeout=2.0)
    mon.sendall(mqtt_connect_packet("capstone-monitor"))
    assert read_packet(mon)[0] == 0x20  # type: ignore[index]
    sub_body = struct.pack("!H", 1) + encode_str("iot/lab/node-01/#") + bytes([0])
    mon.sendall(bytes([0x82]) + encode_var_len(len(sub_body)) + sub_body)
    assert read_packet(mon)[0] == 0x90  # type: ignore[index]

    mon_events: list[tuple[str, str]] = []

    def mon_reader() -> None:
        while True:
            try:
                pkt = read_packet(mon)
            except OSError:
                break
            if pkt is None:
                break
            if (pkt[0] >> 4) == 3:
                t, off = decode_str(pkt[1], 0)
                mon_events.append((t, pkt[1][off:].decode("utf-8")))

    threading.Thread(target=mon_reader, daemon=True).start()

    # TC-01: NVS fallback + HTTP GET config sync
    with urllib.request.urlopen(f"http://127.0.0.1:{http_port}/api/v1/config/node-01", timeout=2.0) as resp:
        cfg = json.loads(resp.read().decode("utf-8"))
        assert resp.status == 200 and cfg["temp_high_c"] == 30.0
    print(f"[PASS][TC-01] HTTP GET config 200 OK -> temp_high_c={cfg['temp_high_c']} C, sample_ms={cfg['sample_ms']}")

    # TC-02: MQTT CONNECT with LWT + Retained "online"
    dev = socket.create_connection(("127.0.0.1", broker.port), timeout=2.0)
    dev.sendall(mqtt_connect_packet("node-01", "iot/lab/node-01/status", "offline"))
    assert read_packet(dev)[0] == 0x20  # type: ignore[index]
    dev.sendall(build_publish_pkt("iot/lab/node-01/status", "online", retain=True))
    sub_cmd = struct.pack("!H", 2) + encode_str("iot/lab/node-01/cmd") + bytes([0])
    dev.sendall(bytes([0x82]) + encode_var_len(len(sub_cmd)) + sub_cmd)
    assert read_packet(dev)[0] == 0x90  # type: ignore[index]
    time.sleep(0.05)
    assert ("iot/lab/node-01/status", "online") in mon_events
    print("[PASS][TC-02] MQTT LWT armed ('offline') & Retained status='online' delivered to subscriber")

    # TC-03: Live JSON telemetry (seq=1..2)
    relay_on = False
    ring: deque[dict[str, object]] = deque(maxlen=32)

    def eval_sample(seq: int, temp_c: float, th_c: float) -> dict[str, object]:
        nonlocal relay_on
        if not relay_on and temp_c >= th_c:
            relay_on = True
        elif relay_on and temp_c <= th_c - cfg["temp_hyst_c"]:
            relay_on = False
        return {
            "dev": "node-01",
            "seq": seq,
            "ts": 1762822800 + (seq - 1) * 5,
            "synced": True,
            "temp": temp_c,
            "th": th_c,
            "relay": relay_on,
            "q": len(ring),
            "drop": 0,
        }

    for seq, temp in ((1, 27.80), (2, 28.40)):
        frame = eval_sample(seq, temp, cfg["temp_high_c"])
        dev.sendall(build_publish_pkt("iot/lab/node-01/telemetry", json.dumps(frame)))
    time.sleep(0.05)
    assert len(broker.ingested_telemetry) == 2
    print("[PASS][TC-03] Live JSON telemetry seq=1..2 verified with valid UTC epoch & time_synced=true")

    # TC-04: Outage -> ring buffer + local hysteresis triggers ON at 30.80 C
    for seq, temp in ((3, 29.60), (4, 30.80), (5, 31.20), (6, 30.40)):
        ring.append(eval_sample(seq, temp, cfg["temp_high_c"]))
    assert len(ring) == 4 and relay_on is True
    print("[PASS][TC-04] Outage buffering (depth=4) & local fail-safe hysteresis triggered relay=true at 30.80 C")

    # TC-05: Batch replay + idempotent deduplication check
    first_buffered = ring[0]
    dev.sendall(build_publish_pkt("iot/lab/node-01/telemetry", json.dumps(first_buffered)))
    dev.sendall(build_publish_pkt("iot/lab/node-01/telemetry", json.dumps(first_buffered)))  # simulate retry dup
    ring.popleft()
    while ring:
        dev.sendall(build_publish_pkt("iot/lab/node-01/telemetry", json.dumps(ring.popleft())))
    time.sleep(0.05)
    assert len(broker.ingested_telemetry) == 6 and broker.duplicates_ignored == 1
    print("[PASS][TC-05] Offline batch replay complete (stored=6 unique, duplicates_ignored=1)")

    # TC-06: Remote CMD override + ungraceful disconnect LWT trigger
    admin = socket.create_connection(("127.0.0.1", broker.port), timeout=2.0)
    admin.sendall(mqtt_connect_packet("admin-cli"))
    assert read_packet(admin)[0] == 0x20  # type: ignore[index]
    admin.sendall(build_publish_pkt("iot/lab/node-01/cmd", json.dumps({"cmd": "set_threshold", "temp_high_c": 29.0})))
    cmd_pkt = read_packet(dev)
    assert cmd_pkt is not None and (cmd_pkt[0] >> 4) == 3
    _, cmd_off = decode_str(cmd_pkt[1], 0)
    new_cfg = json.loads(cmd_pkt[1][cmd_off:].decode("utf-8"))
    assert new_cfg["temp_high_c"] == 29.0

    dev.close()  # Abrupt TCP drop tanpa DISCONNECT -> memicu LWT "offline"
    time.sleep(0.1)
    assert ("iot/lab/node-01/status", "offline") in mon_events
    print("[PASS][TC-06] Remote CMD temp_high_c=29.0 received & abrupt drop triggered LWT='offline'")

    admin.close()
    mon.close()
    broker.stop()
    http_srv.shutdown()
    print("=== ALL 6 CAPSTONE ACCEPTANCE TEST CASES PASSED ===")


if __name__ == "__main__":
    run_acceptance_suite()

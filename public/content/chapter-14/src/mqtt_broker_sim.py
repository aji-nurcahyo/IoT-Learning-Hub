"""Simulasi Broker MQTT 3.1.1 Loopback & Topic Wildcard Matcher (Chapter 14).

Menjalankan mini-broker MQTT 3.1.1 di 127.0.0.1 (port TCP dinamis) dengan paket biner
asli MQTT (CONNECT, CONNACK, SUBSCRIBE, SUBACK, PUBLISH, DISCONNECT) serta
memverifikasi aturan pencocokan topic wildcard '+' dan '#'.
"""

from __future__ import annotations

import json
import socket
import struct
import threading


def topic_matches(pattern: str, topic: str) -> bool:
    """Implementasi pencocokan wildcard MQTT 3.1.1/5.0 ('+' dan '#')."""
    p_parts = pattern.split("/")
    t_parts = topic.split("/")
    for idx, p in enumerate(p_parts):
        if p == "#":
            return idx == len(p_parts) - 1
        if idx >= len(t_parts):
            return False
        if p != "+" and p != t_parts[idx]:
            return False
    return len(p_parts) == len(t_parts)


def encode_remaining_length(length: int) -> bytes:
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


def encode_str(s: str) -> bytes:
    raw = s.encode("utf-8")
    return struct.pack("!H", len(raw)) + raw


def build_connect(client_id: str) -> bytes:
    vh = encode_str("MQTT") + bytes([0x04, 0x02]) + struct.pack("!H", 60)
    pl = encode_str(client_id)
    body = vh + pl
    return bytes([0x10]) + encode_remaining_length(len(body)) + body


def build_subscribe(packet_id: int, topic_filter: str) -> bytes:
    body = struct.pack("!H", packet_id) + encode_str(topic_filter) + bytes([0x00])
    return bytes([0x82]) + encode_remaining_length(len(body)) + body


def build_publish(topic: str, payload: bytes) -> bytes:
    body = encode_str(topic) + payload
    return bytes([0x30]) + encode_remaining_length(len(body)) + body


def run_mini_broker(srv: socket.socket, stop_event: threading.Event) -> None:
    subs: list[tuple[socket.socket, str]] = []
    lock = threading.Lock()

    def handle_client(conn: socket.socket) -> None:
        try:
            while not stop_event.is_set():
                hdr = conn.recv(2)
                if len(hdr) < 2:
                    break
                pkt_type = hdr[0] >> 4
                rem_len = hdr[1]
                data = conn.recv(rem_len) if rem_len else b""

                if pkt_type == 1:  # CONNECT -> CONNACK
                    conn.sendall(bytes([0x20, 0x02, 0x00, 0x00]))
                elif pkt_type == 8:  # SUBSCRIBE -> SUBACK
                    pid = struct.unpack("!H", data[:2])[0]
                    tlen = struct.unpack("!H", data[2:4])[0]
                    tfilter = data[4 : 4 + tlen].decode("utf-8")
                    with lock:
                        subs.append((conn, tfilter))
                    conn.sendall(bytes([0x90, 0x03]) + struct.pack("!H", pid) + bytes([0x00]))
                elif pkt_type == 3:  # PUBLISH -> forward ke subscriber cocok
                    tlen = struct.unpack("!H", data[:2])[0]
                    topic = data[2 : 2 + tlen].decode("utf-8")
                    payload = data[2 + tlen :]
                    pkt = build_publish(topic, payload)
                    with lock:
                        for sc, flt in subs:
                            if topic_matches(flt, topic):
                                sc.sendall(pkt)
                elif pkt_type == 14:  # DISCONNECT
                    break
        finally:
            conn.close()

    srv.settimeout(0.2)
    while not stop_event.is_set():
        try:
            c, _ = srv.accept()
            threading.Thread(target=handle_client, args=(c,), daemon=True).start()
        except TimeoutError:
            continue
        except OSError:
            break


def main() -> None:
    print("=== UJI WILDCARD & MINI-BROKER MQTT 3.1.1 LOOPBACK (CHAPTER 14) ===")
    assert topic_matches("lab/+/temp_c", "lab/gh01/temp_c") is True
    assert topic_matches("lab/+/temp_c", "lab/gh01/z1/temp_c") is False
    assert topic_matches("lab/#", "lab/gh01/node-01/telemetry") is True
    print("[PASS] Aturan wildcard '+' dan '#' terverifikasi.")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(5)
    port = srv.getsockname()[1]
    stop = threading.Event()
    broker_thread = threading.Thread(target=run_mini_broker, args=(srv, stop), daemon=True)
    broker_thread.start()

    try:
        sub = socket.create_connection(("127.0.0.1", port), timeout=2.0)
        sub.sendall(build_connect("sub-dashboard"))
        assert sub.recv(4) == bytes([0x20, 0x02, 0x00, 0x00])
        sub.sendall(build_subscribe(1, "lab/+/node-01/#"))
        assert sub.recv(5)[:2] == bytes([0x90, 0x03])

        pub = socket.create_connection(("127.0.0.1", port), timeout=2.0)
        pub.sendall(build_connect("esp32-gh01-node01"))
        assert pub.recv(4) == bytes([0x20, 0x02, 0x00, 0x00])

        msg = json.dumps({"device_id": "esp32-gh01-node01", "seq": 1, "temp_c": 28.75, "source": "synthetic"}).encode()
        pub.sendall(build_publish("lab/gh01/node-01/telemetry", msg))

        rx_hdr = sub.recv(2)
        rx_body = sub.recv(rx_hdr[1])
        tlen = struct.unpack("!H", rx_body[:2])[0]
        rx_topic = rx_body[2 : 2 + tlen].decode("utf-8")
        rx_payload = rx_body[2 + tlen :].decode("utf-8")
        print(f"[PASS] MQTT Loopback RX topic='{rx_topic}' payload={rx_payload}")

        pub.sendall(bytes([0xE0, 0x00]))
        sub.sendall(bytes([0xE0, 0x00]))
        pub.close()
        sub.close()
    finally:
        stop.set()
        srv.close()
        broker_thread.join(timeout=1.0)


if __name__ == "__main__":
    main()

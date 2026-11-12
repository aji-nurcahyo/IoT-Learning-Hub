"""Simulasi End-to-End HTTP REST API & JSON Client (Loopback Server Nyata, Chapter 13).

Menjalankan server HTTP lokal sementara di 127.0.0.1 (port acak bebas) dan menguji:
1. POST /api/v1/telemetry valid -> 201 Created (diterima).
2. POST /api/v1/telemetry tanpa field wajib -> 400 Bad Request (client error: TIDAK di-retry).
3. POST /api/v1/telemetry saat server mengembalikan 503 sementara -> Retry otomatis berhasil di percobaan ke-2!
4. GET /api/v1/devices/esp32-node-01/config -> 200 OK JSON deserialization.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATE = {"transient_failures_left": 1, "accepted_records": []}


class MockIoTRestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return  # Matikan log default stderr agar output bersih

    def _send_json(self, status: int, body: dict[str, object]) -> None:
        raw = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if self.path == "/api/v1/devices/esp32-node-01/config":
            self._send_json(200, {"device_id": "esp32-node-01", "sample_ms": 5000, "t_high_c": 30.0})
        else:
            self._send_json(404, {"error": "endpoint_not_found"})

    def do_POST(self) -> None:
        if self.path != "/api/v1/telemetry":
            self._send_json(404, {"error": "endpoint_not_found"})
            return

        if STATE["transient_failures_left"] > 0:
            STATE["transient_failures_left"] -= 1
            self._send_json(503, {"error": "service_temporarily_unavailable"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid_json"})
            return

        if "device_id" not in data or "temp_c" not in data:
            self._send_json(400, {"error": "missing_required_fields"})
            return

        STATE["accepted_records"].append(data)
        self._send_json(201, {"accepted": True, "seq": data.get("seq")})


def post_with_policy(url: str, payload: dict[str, object], max_retry: int = 2) -> tuple[int, dict[str, object]]:
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(1, max_retry + 2):
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", "X-Device-Id": "esp32-node-01"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            err_body = json.loads(err.read().decode("utf-8"))
            print(f"    attempt {attempt}: HTTP {err.code} -> {err_body}")
            if 500 <= err.code <= 599 and attempt <= max_retry:
                continue
            return err.code, err_body
    return 0, {}


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), MockIoTRestHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    try:
        print("=== SIMULASI HTTP REST API & JSON CLIENT (LOOPBACK NYATA, CHAPTER 13) ===")
        # Kasus 1: 503 sementara diikuti sukses 201 pada retry ke-2
        print("1. POST valid saat server 503 sementara -> harus retry dan berhasil 201:")
        st1, res1 = post_with_policy(
            f"{base}/api/v1/telemetry",
            {"device_id": "esp32-node-01", "seq": 1, "temp_c": 28.4, "source": "synthetic"},
        )
        assert st1 == 201 and res1["accepted"] is True
        print(f"   HASIL AKHIR: HTTP {st1} {res1}")

        # Kasus 2: Payload cacat -> 400 Bad Request -> TIDAK retry
        print("\n2. POST tanpa 'temp_c' -> harus langsung 400 Bad Request tanpa retry:")
        st2, res2 = post_with_policy(
            f"{base}/api/v1/telemetry",
            {"device_id": "esp32-node-01", "seq": 2, "source": "synthetic"},
        )
        assert st2 == 400
        print(f"   HASIL AKHIR: HTTP {st2} {res2}")

        # Kasus 3: GET konfigurasi JSON
        print("\n3. GET /api/v1/devices/esp32-node-01/config:")
        with urllib.request.urlopen(f"{base}/api/v1/devices/esp32-node-01/config", timeout=2.0) as resp:
            cfg = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200 and cfg["t_high_c"] == 30.0
            print(f"   HASIL AKHIR: HTTP {resp.status} {cfg}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Industrial Serial-to-MQTT Gateway Daemon
Chapter 22 — Internet of Things Learning Hub

Menerima stream data serial dari mikrokontroler (ESP32/STM32),
memverifikasi integritas framing dan checksum, lalu meneruskannya
ke broker MQTT lokal dengan penanganan sinyal systemd graceful shutdown.
"""

import sys
import time
import json
import signal
import socket
from typing import Dict, Any, Optional


class MockSerialPort:
    """Simulasi port serial TTY untuk pengujian mandiri tanpa hardware fisik."""
    def __init__(self, sample_lines):
        self.lines = sample_lines
        self.idx = 0

    def readline(self) -> bytes:
        if self.idx < len(self.lines):
            line = self.lines[self.idx]
            self.idx += 1
            return line.encode('utf-8')
        return b""


def calculate_lrc_checksum(data_str: str) -> str:
    """Menghitung Longitudinal Redundancy Check (LRC) 8-bit hex."""
    lrc = 0
    for ch in data_str.encode('ascii'):
        lrc = (lrc + ch) & 0xFF
    return f"{((lrc ^ 0xFF) + 1) & 0xFF:02X}"


class SerialMqttGateway:
    def __init__(self, serial_device: str = "/dev/ttyUSB0", baudrate: int = 115200):
        self.serial_device = serial_device
        self.baudrate = baudrate
        self.running = True
        self.processed_count = 0
        self.corrupted_count = 0

        # Mendaftarkan handler sinyal Linux (SIGINT, SIGTERM)
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame):
        print(f"\n[GATEWAY DAEMON] Menerima sinyal {signum}. Melakukan graceful shutdown...")
        self.running = False

    def parse_serial_frame(self, raw_line: str) -> Optional[Dict[str, Any]]:
        """
        Protokol framing serial industri:
        $DATA,<DEV_ID>,<SEQ>,<TEMP_C>,<HUM_PCT>,<VBATT_MV>*<CHECKSUM>
        Contoh: $DATA,ESP32-NODE-01,101,28.45,65.20,3290*A4
        """
        line = raw_line.strip()
        if not line.startswith("$DATA,") or "*" not in line:
            return None

        body, received_cs = line[1:].rsplit("*", 1)
        expected_cs = calculate_lrc_checksum(body)
        if received_cs.upper() != expected_cs.upper():
            return None

        tokens = body.split(",")
        if len(tokens) != 6:
            return None

        try:
            return {
                "dev": tokens[1],
                "seq": int(tokens[2]),
                "temp_c": float(tokens[3]),
                "humidity_pct": float(tokens[4]),
                "battery_mv": int(tokens[5]),
                "ts": int(time.time()),
                "gateway_id": "rpi-gateway-lab01"
            }
        except ValueError:
            return None

    def publish_to_mqtt(self, topic: str, payload: Dict[str, Any]) -> bool:
        """Simulasi pengiriman publish ke broker MQTT lokal (atau logging pipeline)."""
        payload_str = json.dumps(payload, separators=(',', ':'))
        # Dalam produksi: client.publish(topic, payload_str, qos=1)
        print(f"[MQTT PUBLISH] Topic: {topic} | Bytes: {len(payload_str)} | Payload: {payload_str}")
        return True

    def run_with_mock(self, mock_stream: MockSerialPort):
        print(f"[GATEWAY DAEMON] Inisialisasi gateway pada {self.serial_device} @ {self.baudrate} bps...")
        print("[GATEWAY DAEMON] Status: RUNNING (Mendengarkan stream serial)")

        while self.running:
            line_bytes = mock_stream.readline()
            if not line_bytes:
                break

            line_str = line_bytes.decode('utf-8', errors='ignore')
            data = self.parse_serial_frame(line_str)
            if data:
                self.processed_count += 1
                topic = f"iot/gateway/{data['gateway_id']}/{data['dev']}/telemetry"
                self.publish_to_mqtt(topic, data)
            else:
                self.corrupted_count += 1
                print(f"[GATEWAY WARNING] Frame serial korup diabaikan: {line_str.strip()}")

        print(f"[GATEWAY DAEMON] Selesai. Total sukses: {self.processed_count}, Korup: {self.corrupted_count}")


def main():
    test_frames = [
        # Frame 1: Valid
        "$DATA,ESP32-NODE-01,101,28.45,65.20,3290*A4\n",
        # Frame 2: Checksum salah
        "$DATA,ESP32-NODE-01,102,28.50,65.10,3288*FF\n",
        # Frame 3: Valid
        "$DATA,ESP32-NODE-02,504,24.12,71.05,3310*B6\n",
        # Frame 4: Malformed format
        "NOISE_BURST_SERIAL_LINE_GARBAGE\n",
        # Frame 5: Valid
        "$DATA,ESP32-NODE-01,103,28.55,65.00,3285*A2\n"
    ]

    # Kalkulasi checksum yang tepat untuk mock data
    fixed_frames = []
    for f in test_frames:
        if f.startswith("$DATA,"):
            body, _ = f[1:].strip().rsplit("*", 1)
            # Sengaja buat satu frame rusak untuk menguji deteksi anomali
            if "102" in body:
                fixed_frames.append(f)  # tetap dengan checksum salah
            else:
                cs = calculate_lrc_checksum(body)
                fixed_frames.append(f"${body}*{cs}\n")
        else:
            fixed_frames.append(f)

    gateway = SerialMqttGateway()
    mock_port = MockSerialPort(fixed_frames)
    gateway.run_with_mock(mock_port)


if __name__ == "__main__":
    main()

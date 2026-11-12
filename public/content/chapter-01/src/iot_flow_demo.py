"""Simulasi alur data end-to-end IoT berbasis data sintetis (Chapter 01).

Menunjukkan bagaimana node sensor menghasilkan payload telemetry JSON,
gateway memvalidasi skema dan mendeteksi anomali nilai batas,
serta aplikasi menghasilkan keputusan kendali (downlink command)
untuk actuator secara deterministik.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TelemetryPacket:
    device_id: str
    seq: int
    timestamp_utc: str
    temp_c: float
    humidity_pct: float
    source: str


def validate_packet(pkt: TelemetryPacket) -> tuple[bool, str]:
    """Memeriksa kelayakan fisik dasar sebelum diteruskan ke platform."""
    if not pkt.device_id:
        return False, "device_id kosong"
    if not (-40.0 <= pkt.temp_c <= 85.0):
        return False, f"temp_c={pkt.temp_c} di luar rentang sensor (-40..85 C)"
    if not (0.0 <= pkt.humidity_pct <= 100.0):
        return False, f"humidity_pct={pkt.humidity_pct} di luar rentang (0..100 %)"
    return True, "ok"


def decide_actuator(temp_c: float, threshold_c: float = 30.0) -> str:
    """Aturan kontrol sederhana pada sisi aplikasi/edge."""
    return "FAN_ON" if temp_c >= threshold_c else "FAN_OFF"


def main() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    accepted = 0
    rejected = 0

    print("=== SIMULASI ALUR DATA END-TO-END IoT (DATA SINTETIS) ===")
    print(f"Sumber dataset: {csv_path.name} (synthetic)")
    print("-" * 68)

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            pkt = TelemetryPacket(
                device_id=row["device_id"],
                seq=int(row["seq"]),
                timestamp_utc=row["timestamp_utc"],
                temp_c=float(row["temp_c"]),
                humidity_pct=float(row["humidity_pct"]),
                source=row["source"],
            )
            ok, reason = validate_packet(pkt)
            if not ok:
                rejected += 1
                print(f"[GATEWAY DROP] seq={pkt.seq} dev={pkt.device_id} alasan={reason}")
                continue

            accepted += 1
            command = decide_actuator(pkt.temp_c, threshold_c=30.0)
            payload = {
                "device_id": pkt.device_id,
                "seq": pkt.seq,
                "temp_c": pkt.temp_c,
                "humidity_pct": pkt.humidity_pct,
                "source": pkt.source,
                "downlink_command": command,
            }
            print(f"[PLATFORM OK ] {json.dumps(payload)}")

    print("-" * 68)
    print(f"Ringkasan: diterima={accepted}, ditolak={rejected}, total={accepted + rejected}")


if __name__ == "__main__":
    main()


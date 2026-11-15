#!/usr/bin/env python3
"""
Time-Series Storage Engine, Downsampling Pipeline & Retention Policy
Chapter 25 — Internet of Things Learning Hub

Menyediakan penyimpanan deret waktu berbasis SQLite terindeks,
pipeline agregasi downsampling (rollup), pembersihan data usang (retention purge),
serta rumus estimasi kebutuhan kapasitas penyimpanan disk.
"""

import sqlite3
import time
import math
from typing import Dict, Any, List, Tuple


class TimeSeriesEngine:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_schema()

    def _init_schema(self):
        """Inisialisasi tabel deret waktu mentah dan tabel agregasi rollup."""
        # 1. Tabel Raw Telemetry (Resolusi Tinggi)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_raw (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                temp_c REAL NOT NULL,
                humidity_pct REAL NOT NULL,
                battery_mv INTEGER NOT NULL
            );
        """)
        # Indeks komposit untuk pencarian rentang waktu cepat per perangkat
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_raw_dev_ts 
            ON telemetry_raw (device_id, timestamp);
        """)

        # 2. Tabel Rollup Per Menit (Resolusi Agregat)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_rollup_1m (
                device_id TEXT NOT NULL,
                window_start INTEGER NOT NULL,
                sample_count INTEGER NOT NULL,
                avg_temp REAL NOT NULL,
                min_temp REAL NOT NULL,
                max_temp REAL NOT NULL,
                avg_humidity REAL NOT NULL,
                PRIMARY KEY (device_id, window_start)
            );
        """)
        self.conn.commit()

    def insert_raw_batch(self, records: List[Tuple[str, int, float, float, int]]):
        """Memasukkan sekumpulan rekaman telemetri dalam satu transaksi (Bulk Append)."""
        self.cursor.executemany("""
            INSERT INTO telemetry_raw (device_id, timestamp, temp_c, humidity_pct, battery_mv)
            VALUES (?, ?, ?, ?, ?);
        """, records)
        self.conn.commit()

    def execute_downsampling_1m(self) -> int:
        """
        Melakukan rollup dari data mentah ke blok 1 menit (60 detik).
        Menghitung avg, min, max, count untuk setiap jendela waktu.
        """
        # Bucket formula: (timestamp / 60) * 60
        self.cursor.execute("""
            INSERT OR REPLACE INTO telemetry_rollup_1m (device_id, window_start, sample_count, avg_temp, min_temp, max_temp, avg_humidity)
            SELECT 
                device_id,
                (timestamp / 60) * 60 AS window_start,
                COUNT(*) AS sample_count,
                ROUND(AVG(temp_c), 2) AS avg_temp,
                ROUND(MIN(temp_c), 2) AS min_temp,
                ROUND(MAX(temp_c), 2) AS max_temp,
                ROUND(AVG(humidity_pct), 2) AS avg_humidity
            FROM telemetry_raw
            GROUP BY device_id, (timestamp / 60) * 60;
        """)
        self.conn.commit()
        return self.cursor.rowcount

    def apply_retention_policy(self, max_raw_age_seconds: int, current_timestamp: int) -> int:
        """Menghapus data mentah yang lebih tua dari batas retensi (misal: > 7 hari)."""
        cutoff = current_timestamp - max_raw_age_seconds
        self.cursor.execute("DELETE FROM telemetry_raw WHERE timestamp < ?;", (cutoff,))
        purged = self.cursor.rowcount
        self.conn.commit()
        return purged

    def query_range(self, device_id: str, start_ts: int, end_ts: int) -> List[Dict[str, Any]]:
        self.cursor.execute("""
            SELECT timestamp, temp_c, humidity_pct, battery_mv 
            FROM telemetry_raw 
            WHERE device_id = ? AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC;
        """, (device_id, start_ts, end_ts))
        cols = ["ts", "temp", "humidity", "battery"]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

    def query_rollups(self, device_id: str) -> List[Dict[str, Any]]:
        self.cursor.execute("""
            SELECT window_start, sample_count, avg_temp, min_temp, max_temp, avg_humidity
            FROM telemetry_rollup_1m
            WHERE device_id = ?
            ORDER BY window_start ASC;
        """, (device_id,))
        cols = ["window_start", "count", "avg_temp", "min_temp", "max_temp", "avg_humidity"]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

    def count_raw_records(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM telemetry_raw;")
        return self.cursor.fetchone()[0]


# 4. Kalkulator Estimasi Kebutuhan Kapasitas Penyimpanan
def estimate_storage_requirements(
    num_devices: int,
    sample_interval_sec: float,
    retention_days_raw: int,
    retention_days_rollup: int,
    bytes_per_raw_row: int = 40,
    bytes_per_rollup_row: int = 48
) -> Dict[str, Any]:
    samples_per_day_per_dev = 86400 / sample_interval_sec
    total_raw_rows = num_devices * samples_per_day_per_dev * retention_days_raw
    total_raw_bytes = total_raw_rows * bytes_per_raw_row

    # Rollup 1 menit: 1440 sampel per hari per perangkat
    rollup_rows_per_day = num_devices * (86400 / 60)
    total_rollup_rows = rollup_rows_per_day * retention_days_rollup
    total_rollup_bytes = total_rollup_rows * bytes_per_rollup_row

    grand_total_bytes = total_raw_bytes + total_rollup_bytes

    return {
        "num_devices": num_devices,
        "total_raw_rows": int(total_raw_rows),
        "total_raw_mb": round(total_raw_bytes / (1024 * 1024), 2),
        "total_rollup_rows": int(total_rollup_rows),
        "total_rollup_mb": round(total_rollup_bytes / (1024 * 1024), 2),
        "grand_total_mb": round(grand_total_bytes / (1024 * 1024), 2),
        "grand_total_gb": round(grand_total_bytes / (1024 * 1024 * 1024), 3)
    }


def main():
    print("=== Time-Series Storage & Retention Verification Suite ===")
    ts_db = TimeSeriesEngine()

    # Skenario: 30 sampel telemetri melintasi 2 jendela menit
    base_time = 1762822800  # Unix Epoch
    records = []
    # Menit 1: 15 sampel (ts: 1762822800 - 1762822856)
    for i in range(15):
        t = base_time + (i * 4)
        records.append(("node-alpha", t, 26.0 + (i * 0.1), 60.0 + (i * 0.2), 3300))

    # Menit 2: 15 sampel (ts: 1762822860 - 1762822916)
    for i in range(15):
        t = base_time + 60 + (i * 4)
        records.append(("node-alpha", t, 28.0 + (i * 0.1), 65.0 - (i * 0.2), 3290))

    ts_db.insert_raw_batch(records)
    print(f"Test 1 - Bulk Ingestion: Berhasil memasukkan {ts_db.count_raw_records()} baris data mentah.")

    # Eksekusi Downsampling Rollup
    rows_affected = ts_db.execute_downsampling_1m()
    rollups = ts_db.query_rollups("node-alpha")
    print(f"\nTest 2 - Downsampling Rollup (1-Menit):")
    print(f"   Jumlah jendela agregasi terbuat: {len(rollups)}")
    for r in rollups:
        print(f"   Jendela {r['window_start']}: Count={r['count']}, AvgTemp={r['avg_temp']} C (Min={r['min_temp']}, Max={r['max_temp']})")

    assert len(rollups) == 2, "Harus menghasilkan tepat 2 jendela agregasi 1 menit!"

    # Eksekusi Kebijakan Retensi (Purge raw data older than 60 seconds from current time)
    now_simulated = base_time + 130
    purged = ts_db.apply_retention_policy(max_raw_age_seconds=60, current_timestamp=now_simulated)
    remaining_raw = ts_db.count_raw_records()
    print(f"\nTest 3 - Retention Policy Purge:")
    print(f"   Data mentah terhapus (> 60s): {purged} baris")
    print(f"   Sisa data mentah aktif       : {remaining_raw} baris")
    # Buktikan data rollup ringkas tetap utuh!
    rollups_after = ts_db.query_rollups("node-alpha")
    print(f"   Data rollup agregasi tetap utuh: {len(rollups_after)} jendela (Data historis terlindungi).")
    assert len(rollups_after) == 2, "Rollup tidak boleh terhapus oleh pembersihan raw data!"

    # Kalkulasi Estimasi Kapasitas
    print(f"\nTest 4 - Storage Capacity Estimation:")
    est = estimate_storage_requirements(
        num_devices=100,
        sample_interval_sec=5.0,
        retention_days_raw=7,
        retention_days_rollup=365
    )
    print(f"   100 Perangkat @ 5s sampling:")
    print(f"   - Raw Storage (7 hari)    : {est['total_raw_rows']} baris | {est['total_raw_mb']} MB")
    print(f"   - Rollup Storage (365 hari): {est['total_rollup_rows']} baris | {est['total_rollup_mb']} MB")
    print(f"   - Total Kebutuhan Disk    : {est['grand_total_gb']} GB")

    print("\nSemua pengujian time-series storage & retensi berhasil diselesaikan.")


if __name__ == "__main__":
    main()

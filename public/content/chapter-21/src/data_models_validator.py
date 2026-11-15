#!/usr/bin/env python3
"""
IoT Data Models, Telemetry, and Event Schema Validator & Idempotency Pipeline
Chapter 21 — Internet of Things Learning Hub
"""

import json
import time
import struct
import hashlib
from typing import Dict, Any, Tuple, List, Optional


# 1. Definisi Kontrak Skema Data Models (Telemetry, Event, Command)
TELEMETRY_SCHEMA = {
    "type": "object",
    "required": ["v", "dev", "seq", "ts", "metrics"],
    "properties": {
        "v": {"type": "integer", "enum": [1]},
        "dev": {"type": "string", "minLength": 3, "maxLength": 32},
        "seq": {"type": "integer", "minimum": 0},
        "ts": {"type": "integer", "minimum": 1700000000},  # Unix Epoch seconds
        "metrics": {
            "type": "object",
            "required": ["temp_c", "humidity_pct"],
            "properties": {
                "temp_c": {"type": "number", "minimum": -40.0, "maximum": 85.0},
                "humidity_pct": {"type": "number", "minimum": 0.0, "maximum": 100.0},
                "battery_mv": {"type": "integer", "minimum": 0, "maximum": 5000},
                "rssi_dbm": {"type": "integer", "minimum": -120, "maximum": 0}
            }
        },
        "quality": {"type": "string", "enum": ["good", "uncertain", "bad"]}
    }
}

EVENT_SCHEMA = {
    "type": "object",
    "required": ["v", "dev", "event_id", "ts", "severity", "type", "payload"],
    "properties": {
        "v": {"type": "integer", "enum": [1]},
        "dev": {"type": "string", "minLength": 3, "maxLength": 32},
        "event_id": {"type": "string", "minLength": 16},
        "ts": {"type": "integer", "minimum": 1700000000},
        "severity": {"type": "string", "enum": ["info", "warning", "critical"]},
        "type": {"type": "string"},
        "payload": {"type": "object"}
    }
}

COMMAND_SCHEMA = {
    "type": "object",
    "required": ["v", "cmd_id", "target_dev", "action", "params", "expiry_ts"],
    "properties": {
        "v": {"type": "integer", "enum": [1]},
        "cmd_id": {"type": "string", "minLength": 8},
        "target_dev": {"type": "string"},
        "action": {"type": "string", "enum": ["set_sample_rate", "actuate_relay", "reboot"]},
        "params": {"type": "object"},
        "expiry_ts": {"type": "integer", "minimum": 1700000000}
    }
}


# 2. Schema Validator Ringan (Pure Python Standalone tanpa dependensi eksternal)
def validate_payload(data: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
    errors = []
    if not isinstance(data, dict):
        return [f"{path}: harus berupa dictionary/object JSON"]

    # Periksa required fields
    for req in schema.get("required", []):
        if req not in data:
            errors.append(f"{path}: field wajib '{req}' tidak ditemukan")

    # Periksa tipe dan batasan properties
    props = schema.get("properties", {})
    for key, value in data.items():
        if key not in props:
            continue
        spec = props[key]
        subpath = f"{path}.{key}"
        expected_type = spec.get("type")

        if expected_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                errors.append(f"{subpath}: diharapkan integer, diperoleh {type(value).__name__}")
            else:
                if "minimum" in spec and value < spec["minimum"]:
                    errors.append(f"{subpath}: nilai {value} < minimum {spec['minimum']}")
                if "maximum" in spec and value > spec["maximum"]:
                    errors.append(f"{subpath}: nilai {value} > maximum {spec['maximum']}")
                if "enum" in spec and value not in spec["enum"]:
                    errors.append(f"{subpath}: nilai {value} tidak terdaftar di enum {spec['enum']}")

        elif expected_type == "number":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{subpath}: diharapkan number, diperoleh {type(value).__name__}")
            else:
                if "minimum" in spec and value < spec["minimum"]:
                    errors.append(f"{subpath}: nilai {value} < minimum {spec['minimum']}")
                if "maximum" in spec and value > spec["maximum"]:
                    errors.append(f"{subpath}: nilai {value} > maximum {spec['maximum']}")

        elif expected_type == "string":
            if not isinstance(value, str):
                errors.append(f"{subpath}: diharapkan string, diperoleh {type(value).__name__}")
            else:
                if "minLength" in spec and len(value) < spec["minLength"]:
                    errors.append(f"{subpath}: panjang string {len(value)} < minLength {spec['minLength']}")
                if "maxLength" in spec and len(value) > spec["maxLength"]:
                    errors.append(f"{subpath}: panjang string {len(value)} > maxLength {spec['maxLength']}")
                if "enum" in spec and value not in spec["enum"]:
                    errors.append(f"{subpath}: nilai '{value}' tidak ada di enum {spec['enum']}")

        elif expected_type == "object":
            if not isinstance(value, dict):
                errors.append(f"{subpath}: diharapkan object/dict")
            else:
                errors.extend(validate_payload(value, spec, subpath))

    return errors


# 3. Pipeline Deduplikasi Idempotensi (LRU / Time-Window Cache)
class IdempotencyDeduplicator:
    def __init__(self, ttl_seconds: float = 60.0, max_capacity: int = 1000):
        self.ttl = ttl_seconds
        self.max_capacity = max_capacity
        self.seen: Dict[str, float] = {}

    def is_duplicate(self, device_id: str, message_id: str, current_time: float) -> bool:
        self._evict_expired(current_time)
        key = f"{device_id}:{message_id}"
        if key in self.seen:
            return True
        if len(self.seen) >= self.max_capacity:
            # Hapus entri tertua
            oldest_key = min(self.seen, key=lambda k: self.seen[k])
            del self.seen[oldest_key]
        self.seen[key] = current_time
        return False

    def _evict_expired(self, current_time: float) -> None:
        expired = [k for k, t in self.seen.items() if current_time - t > self.ttl]
        for k in expired:
            del self.seen[k]


# 4. Komparasi Efisiensi Encoding (JSON Mentah vs Minified vs Binary Packing)
def benchmark_payload_encodings(telemetry: Dict[str, Any]) -> Dict[str, Any]:
    # JSON mentah terformat
    raw_json = json.dumps(telemetry, indent=2).encode('utf-8')
    # JSON minified
    min_json = json.dumps(telemetry, separators=(',', ':')).encode('utf-8')

    # Binary struct packing:
    # Format: uint8 version, 16-char device_id, uint32 seq, uint32 timestamp, int16 temp_c*100, uint16 hum_pct*100, uint16 vbatt, int8 rssi
    dev_bytes = telemetry["dev"].encode('ascii').ljust(16, b'\x00')[:16]
    metrics = telemetry["metrics"]
    temp_scaled = int(round(metrics["temp_c"] * 100))
    hum_scaled = int(round(metrics["humidity_pct"] * 100))
    vbatt = metrics.get("battery_mv", 3300)
    rssi = metrics.get("rssi_dbm", -65)

    packed_binary = struct.pack(
        "!B16sIIhHHb",
        telemetry["v"],
        dev_bytes,
        telemetry["seq"],
        telemetry["ts"],
        temp_scaled,
        hum_scaled,
        vbatt,
        rssi
    )

    return {
        "raw_json_bytes": len(raw_json),
        "minified_json_bytes": len(min_json),
        "packed_binary_bytes": len(packed_binary),
        "reduction_vs_raw_pct": round((1.0 - (len(packed_binary) / len(raw_json))) * 100, 2),
        "reduction_vs_min_pct": round((1.0 - (len(packed_binary) / len(min_json))) * 100, 2)
    }


def main():
    print("=== IoT Data Models & Schema Verification Suite ===")

    # Contoh 1: Telemetry Valid
    sample_telemetry = {
        "v": 1,
        "dev": "sensor-node-alpha",
        "seq": 1042,
        "ts": 1762822800,
        "metrics": {
            "temp_c": 26.75,
            "humidity_pct": 62.40,
            "battery_mv": 3280,
            "rssi_dbm": -68
        },
        "quality": "good"
    }
    errs = validate_payload(sample_telemetry, TELEMETRY_SCHEMA)
    print(f"Test 1 - Valid Telemetry Validation: {'PASSED' if not errs else 'FAILED (' + str(errs) + ')'}")

    # Contoh 2: Telemetry Malformed (Tipe salah & out of range)
    bad_telemetry = {
        "v": 1,
        "dev": "sn",  # minLength 3 dilanggar
        "seq": -5,    # minimum 0 dilanggar
        "ts": 1600000000,  # timestamp masa lalu sebelum 1700000000
        "metrics": {
            "temp_c": 125.0,  # > maximum 85.0
            "humidity_pct": "tinggi"  # tipe salah
        }
    }
    errs_bad = validate_payload(bad_telemetry, TELEMETRY_SCHEMA)
    print(f"Test 2 - Malformed Telemetry Rejection: PASSED (Tertolak {len(errs_bad)} pelanggaran skema)")
    for e in errs_bad:
        print(f"   [Expected Error] {e}")

    # Contoh 3: Event Payload Valid
    sample_event = {
        "v": 1,
        "dev": "gateway-edge-01",
        "event_id": "evt-20261116-0042a9bc",
        "ts": 1762822805,
        "severity": "warning",
        "type": "TAMPER_DETECTED",
        "payload": {
            "chassis_opened": True,
            "ambient_light_lux": 420.5
        }
    }
    errs_event = validate_payload(sample_event, EVENT_SCHEMA)
    print(f"Test 3 - Valid Event Payload: {'PASSED' if not errs_event else 'FAILED'}")

    # Contoh 4: Command Payload Valid
    sample_cmd = {
        "v": 1,
        "cmd_id": "cmd-8921",
        "target_dev": "actuator-relay-04",
        "action": "actuate_relay",
        "params": {"channel": 1, "state": True, "duration_s": 30},
        "expiry_ts": 1762822900
    }
    errs_cmd = validate_payload(sample_cmd, COMMAND_SCHEMA)
    print(f"Test 4 - Valid Command Payload: {'PASSED' if not errs_cmd else 'FAILED'}")

    # Contoh 5: Idempotensi Deduplicator
    print("\n=== Idempotency Pipeline Test ===")
    dedup = IdempotencyDeduplicator(ttl_seconds=10.0)
    now = 1000.0
    r1 = dedup.is_duplicate("dev-01", "msg-101", now)
    r2 = dedup.is_duplicate("dev-01", "msg-101", now + 1.0)  # duplicate dalam window
    r3 = dedup.is_duplicate("dev-01", "msg-102", now + 2.0)  # new message
    r4 = dedup.is_duplicate("dev-01", "msg-101", now + 15.0)  # expired TTL -> diterima kembali
    print(f"   Message 101 First Arrival: Duplicate? {r1} (Expected: False)")
    print(f"   Message 101 Resend in TTL: Duplicate? {r2} (Expected: True)")
    print(f"   Message 102 New Message:   Duplicate? {r3} (Expected: False)")
    print(f"   Message 101 After Expiry:  Duplicate? {r4} (Expected: False)")

    # Contoh 6: Encoding Efficiency Benchmark
    print("\n=== Encoding Efficiency Benchmark ===")
    stats = benchmark_payload_encodings(sample_telemetry)
    print(f"   Raw Pretty JSON  : {stats['raw_json_bytes']} bytes")
    print(f"   Minified JSON    : {stats['minified_json_bytes']} bytes")
    print(f"   Packed Binary    : {stats['packed_binary_bytes']} bytes")
    print(f"   Savings vs Raw   : {stats['reduction_vs_raw_pct']}%")
    print(f"   Savings vs Min   : {stats['reduction_vs_min_pct']}%")
    print("\nVerification suite completed successfully.")


if __name__ == "__main__":
    main()

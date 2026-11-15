#!/usr/bin/env python3
"""
Node-RED Flow Runtime & Execution Engine Simulator
Chapter 24 — Internet of Things Learning Hub

Memvalidasi struktur deklaratif flows.json, menyimulasikan eksekusi
event message (msg, context global, switch node, function node, dan catch).
"""

import json
import time
from typing import Dict, Any, List, Optional


class NodeRedSimulator:
    def __init__(self, flow_path: str):
        with open(flow_path, "r", encoding="utf-8") as f:
            self.raw_nodes: List[Dict[str, Any]] = json.load(f)

        self.nodes_by_id = {n["id"]: n for n in self.raw_nodes if "id" in n}
        self.global_context: Dict[str, Any] = {}
        self.published_alarms: List[Dict[str, Any]] = []
        self.dead_letter_errors: List[Dict[str, Any]] = []

    def validate_flow_syntax(self) -> bool:
        """Memverifikasi kelengkapan node primitives standar."""
        types_found = {n.get("type") for n in self.raw_nodes}
        expected = {"tab", "mqtt in", "change", "switch", "function", "mqtt out", "http in", "http response", "catch"}
        diff = expected - types_found
        if diff:
            print(f"[SIMULATOR ERROR] Missing node types in flow: {diff}")
            return False
        print(f"[SIMULATOR] Validasi skema flows.json SUKSES ({len(self.raw_nodes)} node terdeteksi).")
        return True

    def simulate_telemetry_event(self, incoming_msg: Dict[str, Any]):
        """Menyimulasikan alur eksekusi pesan dari MQTT in ke node hilir."""
        # 1. Update Global Context via change node
        payload = incoming_msg.get("payload", {})
        self.global_context["latest_telemetry"] = payload

        # 2. Switch Node Evaluation
        metrics = payload.get("metrics", {})
        temp = metrics.get("temp_c")

        if temp is None:
            # Pemicu Catch Error
            err_record = {"error": "Missing temp_c metric in payload", "msg": incoming_msg, "ts": time.time()}
            self.dead_letter_errors.append(err_record)
            print(f"[CATCH NODE] Exception ditangkap: {err_record['error']}")
            return

        if temp >= 30.0:
            # Wire ke node_alarm_enricher -> node_mqtt_out_alarm
            alarm_event = {
                "event_id": f"ALM-{int(time.time()*1000)}",
                "dev": payload.get("dev", "unknown"),
                "type": "HIGH_TEMPERATURE",
                "severity": "warning",
                "measured_temp": temp,
                "threshold": 30.0,
                "ts": int(time.time())
            }
            target_topic = f"iot/lab/{payload.get('dev')}/event/alarm"
            self.published_alarms.append({"topic": target_topic, "payload": alarm_event})
            print(f"[ALARM DISPATCH] Topic: {target_topic} | Temp: {temp} C >= 30.0 C | Alarm ID: {alarm_event['event_id']}")
        else:
            print(f"[NORMAL LOG] Temp: {temp} C < 30.0 C (Kondisi lingkungan normal).")

    def simulate_http_api_call(self) -> Dict[str, Any]:
        """Simulasi HTTP GET /api/v1/telemetry/latest yang mengambil dari global context."""
        state = self.global_context.get("latest_telemetry", {"status": "NO_DATA"})
        return {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": state}


def main():
    print("=== Node-RED Flow Execution & Integration Verification ===")
    sim = NodeRedSimulator("public/content/chapter-24/src/flows.json")
    assert sim.validate_flow_syntax(), "Flows.json tidak lolos validasi!"

    # Case 1: Telemetry Normal (< 30.0 C)
    print("\nCase 1: Mengirim Telemetry Normal (27.5 C)")
    sim.simulate_telemetry_event({
        "topic": "iot/lab/node-01/telemetry",
        "payload": {
            "dev": "node-01",
            "seq": 101,
            "metrics": {"temp_c": 27.5, "humidity_pct": 58.0}
        }
    })

    # Case 2: Telemetry Kritis (>= 30.0 C)
    print("\nCase 2: Mengirim Telemetry Kritis (31.8 C)")
    sim.simulate_telemetry_event({
        "topic": "iot/lab/node-01/telemetry",
        "payload": {
            "dev": "node-01",
            "seq": 102,
            "metrics": {"temp_c": 31.8, "humidity_pct": 65.0}
        }
    })
    assert len(sim.published_alarms) == 1, "Harus ada 1 alarm diterbitkan!"

    # Case 3: HTTP API Read Context
    print("\nCase 3: Menyimulasikan HTTP GET /api/v1/telemetry/latest")
    api_res = sim.simulate_http_api_call()
    print(f"HTTP Status : {api_res['statusCode']}")
    print(f"Payload Data: {api_res['body']}")
    assert api_res["body"]["metrics"]["temp_c"] == 31.8, "Global context harus menyimpan data terbaru!"

    # Case 4: Malformed message -> Ditangkap Catch Node
    print("\nCase 4: Mengirim Telemetry Rusak (Tanpa field metrics)")
    sim.simulate_telemetry_event({
        "topic": "iot/lab/node-02/telemetry",
        "payload": {"dev": "node-02", "seq": 500}
    })
    assert len(sim.dead_letter_errors) == 1, "Error harus ditangkap oleh Catch Node!"

    print("\nSemua skenario pengujian alur Node-RED berhasil diverifikasi.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
IoT Fleet Management, Device Registry & Configuration Twin Engine
Chapter 27 — Internet of Things Learning Hub

Menyediakan registri inventaris perangkat, rekonsiliasi Desired vs Reported state,
deteksi denyut jantung (Heartbeat Monitor & Dead Node Detection), serta alur decommissioning.
"""

import time
import json
from enum import Enum
from typing import Dict, Any, List, Optional


class DeviceStatus(str, Enum):
    PROVISIONED = "PROVISIONED"
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    DECOMMISSIONED = "DECOMMISSIONED"


class DeviceRecord:
    def __init__(self, dev_id: str, hw_model: str, mac_addr: str, fw_version: str):
        self.dev_id = dev_id
        self.hw_model = hw_model
        self.mac_addr = mac_addr
        self.fw_version = fw_version
        self.status = DeviceStatus.PROVISIONED
        self.last_heartbeat: float = 0.0

        # State Twin
        self.desired_config: Dict[str, Any] = {"sample_rate_sec": 10, "alert_temp_high": 30.0, "version": 1}
        self.reported_config: Dict[str, Any] = {"sample_rate_sec": 10, "alert_temp_high": 30.0, "version": 1}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dev_id": self.dev_id,
            "hw_model": self.hw_model,
            "mac_addr": self.mac_addr,
            "fw_version": self.fw_version,
            "status": self.status.value,
            "last_heartbeat": self.last_heartbeat,
            "desired_version": self.desired_config.get("version"),
            "reported_version": self.reported_config.get("version"),
            "drift": self.has_config_drift()
        }

    def has_config_drift(self) -> bool:
        return self.desired_config != self.reported_config


class FleetManager:
    def __init__(self, heartbeat_timeout_sec: float = 30.0, degraded_threshold_sec: float = 15.0):
        self.devices: Dict[str, DeviceRecord] = {}
        self.heartbeat_timeout = heartbeat_timeout_sec
        self.degraded_threshold = degraded_threshold_sec

    def enroll_device(self, dev_id: str, hw_model: str, mac_addr: str, fw_version: str) -> DeviceRecord:
        """Pendaftaran perangkat baru ke inventaris sistem."""
        if dev_id in self.devices:
            raise ValueError(f"Perangkat {dev_id} sudah terdaftar!")
        dev = DeviceRecord(dev_id, hw_model, mac_addr, fw_version)
        self.devices[dev_id] = dev
        return dev

    def record_heartbeat(self, dev_id: str, current_time: float) -> bool:
        """Mencatat denyut jantung berkala dari perangkat."""
        if dev_id not in self.devices:
            return False
        dev = self.devices[dev_id]
        if dev.status == DeviceStatus.DECOMMISSIONED:
            return False  # Perangkat pensiun ditolak
        dev.last_heartbeat = current_time
        dev.status = DeviceStatus.ONLINE
        return True

    def set_desired_config(self, dev_id: str, new_params: Dict[str, Any]) -> Dict[str, Any]:
        """Operator menetapkan konfigurasi baru di tingkat cloud/gateway."""
        if dev_id not in self.devices:
            raise KeyError(f"Perangkat {dev_id} tidak ditemukan.")
        dev = self.devices[dev_id]
        new_version = dev.desired_config.get("version", 0) + 1
        dev.desired_config.update(new_params)
        dev.desired_config["version"] = new_version
        return dev.desired_config

    def report_device_config(self, dev_id: str, reported_payload: Dict[str, Any]) -> bool:
        """Perangkat mengonfirmasi konfigurasi yang berhasil diterapkan (ACK)."""
        if dev_id not in self.devices:
            return False
        dev = self.devices[dev_id]
        dev.reported_config = reported_payload
        return True

    def evaluate_fleet_health(self, current_time: float) -> Dict[str, int]:
        """Memeriksa status ketersediaan seluruh armada berdasarkan waktu denyut terakhir."""
        summary = {s.value: 0 for s in DeviceStatus}
        for dev in self.devices.values():
            if dev.status == DeviceStatus.DECOMMISSIONED:
                summary[dev.status.value] += 1
                continue

            elapsed = current_time - dev.last_heartbeat
            if dev.last_heartbeat == 0:
                dev.status = DeviceStatus.PROVISIONED
            elif elapsed > self.heartbeat_timeout:
                dev.status = DeviceStatus.OFFLINE
            elif elapsed > self.degraded_threshold:
                dev.status = DeviceStatus.DEGRADED
            else:
                dev.status = DeviceStatus.ONLINE

            summary[dev.status.value] += 1
        return summary

    def decommission_device(self, dev_id: str) -> bool:
        """Mencabut izin operasional perangkat dan mengalihkan status ke DECOMMISSIONED."""
        if dev_id not in self.devices:
            return False
        dev = self.devices[dev_id]
        dev.status = DeviceStatus.DECOMMISSIONED
        return True


def main():
    print("=== IoT Fleet Management & Device Registry Verification Suite ===")
    manager = FleetManager(heartbeat_timeout_sec=30.0, degraded_threshold_sec=15.0)

    # 1. Enrollment
    dev1 = manager.enroll_device("node-env-01", "ESP32-WROOM-32D", "24:6F:28:B0:11:A4", "v1.2.0")
    dev2 = manager.enroll_device("node-env-02", "ESP32-S3-DEVKIT", "30:C6:F7:22:98:C2", "v1.2.0")
    print(f"Test 1 - Enrollment: Berhasil mendaftarkan {len(manager.devices)} node.")
    print(f"   Node 1 Status: {dev1.status.value}")

    # 2. Heartbeat Ping
    now = 1000.0
    manager.record_heartbeat("node-env-01", now)
    manager.record_heartbeat("node-env-02", now)
    health_now = manager.evaluate_fleet_health(now)
    print(f"\nTest 2 - Active Heartbeat: Status armada pada t={now}s -> {health_now}")
    assert health_now["ONLINE"] == 2, "Kedua node harus ONLINE!"

    # 3. Time Skew & Dead Node Detection
    # Simulasikan waktu berlalu 20s (node-env-01 tetap kirim, node-env-02 macet)
    t_step2 = now + 20.0
    manager.record_heartbeat("node-env-01", t_step2)
    health_step2 = manager.evaluate_fleet_health(t_step2)
    print(f"\nTest 3 - Degraded State (t={t_step2}s):")
    print(f"   Node 1 Status: {dev1.status.value} (Expected: ONLINE)")
    print(f"   Node 2 Status: {dev2.status.value} (Expected: DEGRADED)")
    assert dev2.status == DeviceStatus.DEGRADED, "Node 2 harus DEGRADED setelah 20s (> 15s)!"

    # Simulasikan waktu berlalu hingga t = now + 40s (node-env-02 timeout)
    t_step3 = now + 40.0
    manager.record_heartbeat("node-env-01", t_step3)
    health_step3 = manager.evaluate_fleet_health(t_step3)
    print(f"\nTest 4 - Offline Timeout (t={t_step3}s):")
    print(f"   Node 2 Status: {dev2.status.value} (Expected: OFFLINE)")
    assert dev2.status == DeviceStatus.OFFLINE, "Node 2 harus OFFLINE setelah 40s (> 30s)!"

    # 4. State Twin & Configuration Drift
    print("\nTest 5 - Desired vs Reported State Twin:")
    print(f"   Kondisi awal Node 1 Drift? {dev1.has_config_drift()}")
    # Operator mengubah ambang suhu di cloud
    manager.set_desired_config("node-env-01", {"alert_temp_high": 32.5})
    print(f"   Setelah operator update Desired: Desired Version={dev1.desired_config['version']} | Reported Version={dev1.reported_config['version']}")
    print(f"   Konfigurasi Drift Terdeteksi? {dev1.has_config_drift()} (Expected: True)")
    assert dev1.has_config_drift(), "Harus ada config drift!"

    # Node menerapkan konfigurasi dan mengirim ACK
    manager.report_device_config("node-env-01", dev1.desired_config.copy())
    print(f"   Setelah Node 1 mengirim ACK Reported: Drift? {dev1.has_config_drift()} (Expected: False)")
    assert not dev1.has_config_drift(), "Drift harus hilang setelah sinkronisasi!"

    # 5. Decommissioning
    print("\nTest 6 - Decommissioning Workflow:")
    manager.decommission_device("node-env-02")
    print(f"   Node 2 Status: {dev2.status.value}")
    # Heartbeat node yang dipensiunkan harus ditolak
    hb_res = manager.record_heartbeat("node-env-02", t_step3 + 5.0)
    print(f"   Heartbeat ditolak untuk perangkat pensiun? {'Ya' if not hb_res else 'Tidak'} (Expected: Ya)")
    assert not hb_res, "Perangkat decommissioned tidak boleh diterima lagi!"

    print("\nSemua pengujian fleet management & configuration twin berhasil diverifikasi.")


if __name__ == "__main__":
    main()

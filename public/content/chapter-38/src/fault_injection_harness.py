"""
Chapter 38: IoT Testing, Fault Injection & Reliability Engineering Simulator
Harness injeksi kegagalan (Network Packet Loss, Power Brownout Interruption) dan evaluasi metrik keandalan MTBF/MTTR.
"""

from typing import List, Dict, Any, Optional
import random


class ResilientDeviceClient:
    """Klien IoT dengan buffer retensi offline dan penanganan kegagalan jaringan."""
    def __init__(self, device_id: str, buffer_limit: int = 10):
        self.device_id = device_id
        self.buffer_limit = buffer_limit
        self.offline_buffer: List[Dict[str, Any]] = []
        self.delivered_telemetry: List[Dict[str, Any]] = []
        self.state = "OPERATIONAL"  # "OPERATIONAL", "BROWNOUT_RECOVERING"

    def send_telemetry(self, payload: Dict[str, Any], network_drop: bool = False, brownout: bool = False) -> str:
        """Mengirim telemetri dengan injeksi kegagalan jaringan atau daya listrik."""
        if brownout:
            self.state = "BROWNOUT_RECOVERING"
            # Brownout memicu reboot: volatile state hilang, namun persistent buffer aman
            return "ERR_BROWNOUT_REBOOT"

        self.state = "OPERATIONAL"
        if network_drop:
            # Jaringan terputus: simpan di offline buffer
            if len(self.offline_buffer) < self.buffer_limit:
                self.offline_buffer.append(payload)
                return "BUFFERED_OFFLINE"
            else:
                return "ERR_BUFFER_OVERFLOW"

        # Jaringan normal: kirim data saat ini + kuras buffer offline jika ada
        if self.offline_buffer:
            self.delivered_telemetry.extend(self.offline_buffer)
            self.offline_buffer.clear()

        self.delivered_telemetry.append(payload)
        return "SUCCESS"


def calculate_reliability_metrics(operational_hours: float, failure_count: int, total_repair_hours: float) -> Dict[str, float]:
    """Menghitung metrik keandalan Mean Time Between Failures (MTBF) dan Mean Time To Repair (MTTR)."""
    if failure_count == 0:
        return {
            "mtbf_hours": round(operational_hours, 2),
            "mttr_hours": 0.0,
            "availability": 1.0
        }

    mtbf = (operational_hours - total_repair_hours) / failure_count
    mttr = total_repair_hours / failure_count
    availability = mtbf / (mtbf + mttr)

    return {
        "mtbf_hours": round(mtbf, 2),
        "mttr_hours": round(mttr, 2),
        "availability": round(availability, 5)
    }


def run_fault_injection_simulation() -> None:
    print("=== CHAPTER 38: FAULT INJECTION & RELIABILITY SIMULATION ===")
    
    # 1. Uji Injeksi Kegagalan Jaringan & Retensi Buffer
    client = ResilientDeviceClient(device_id="dev-field-01", buffer_limit=5)
    
    # Transmisi normal
    status1 = client.send_telemetry({"seq": 1, "temp": 25.1})
    assert status1 == "SUCCESS"
    
    # Injeksi putus jaringan selama 3 sampel
    print("Menyuntikkan kegagalan jaringan (Network Packet Drop)...")
    for s in [2, 3, 4]:
        st = client.send_telemetry({"seq": s, "temp": 25.0 + s}, network_drop=True)
        assert st == "BUFFERED_OFFLINE"
    print(f"Status Klien: {len(client.offline_buffer)} pesan tertahan di offline buffer.")
    assert len(client.offline_buffer) == 3

    # Jaringan pulih pada sampel 5
    print("Jaringan pulih. Mengirim sampel 5 dan menguras buffer offline...")
    status5 = client.send_telemetry({"seq": 5, "temp": 25.5}, network_drop=False)
    assert status5 == "SUCCESS"
    assert len(client.offline_buffer) == 0
    assert len(client.delivered_telemetry) == 5  # Sampel 1, 2, 3, 4, 5 semua terkirim tuntas!
    print(f"Total pesan sukses terkirim ke backend: {len(client.delivered_telemetry)}")

    # 2. Injeksi Brownout Daya
    print("Menyuntikkan fluktuasi daya listrik (Power Brownout)...")
    status_bo = client.send_telemetry({"seq": 6, "temp": 26.0}, brownout=True)
    assert status_bo == "ERR_BROWNOUT_REBOOT"
    assert client.state == "BROWNOUT_RECOVERING"
    print("Perangkat mereset diri dan memulihkan status operasional...")
    
    # Pulih setelah reboot
    status_rec = client.send_telemetry({"seq": 7, "temp": 26.1}, brownout=False)
    assert status_rec == "SUCCESS"
    assert client.state == "OPERATIONAL"

    # 3. Kalkulasi Metrik Keandalan MTBF & MTTR
    rel = calculate_reliability_metrics(operational_hours=8760.0, failure_count=4, total_repair_hours=12.0)
    print(f"\nMetrik Keandalan (1 Tahun Operasi):")
    print(f"MTBF: {rel['mtbf_hours']} jam | MTTR: {rel['mttr_hours']} jam | Availability: {rel['availability'] * 100:.3f}%")
    assert rel["availability"] > 0.998
    print("STATUS: VERIFIED (Semua pengujian injeksi gangguan jaringan, brownout, dan MTBF lulus 100%)")


if __name__ == "__main__":
    run_fault_injection_simulation()

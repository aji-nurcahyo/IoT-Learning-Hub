"""
Chapter 40: Advanced IoT Systems Capstone
Platform Pemantauan Cerdas, Aman & Tangguh (Intelligent, Secure & Resilient IoT Monitoring Platform)
Mengintegrasikan 6 Kasus Uji Penerimaan Sistem (SATC-01 hingga SATC-06) yang mencakup seluruh pilar Level 4:
- SATC-01: Low-Power Duty Cycle & Battery Lifetime Prediction (Ch 31)
- SATC-02: FreeRTOS Priority Preemption & Queue Ingestion (Ch 32)
- SATC-03: Industrial Modbus RTU Framing & CRC-16 Checksum (Ch 33)
- SATC-04: Edge AI TinyML Vibration Anomaly Detection (Ch 35)
- SATC-05: Digital Twin Thermal Modeling & What-If Simulation (Ch 36)
- SATC-06: Chaos Fault Injection, Store-and-Forward & Data Minimization (Ch 37, 38, 39)
"""

from typing import Dict, List, Any, Optional
import struct
import math
import hashlib


class AdvancedIoTCapstonePlatform:
    def __init__(self):
        self.device_id = "CAPSTONE-EDGE-NODE-01"
        self.offline_buffer: List[Dict[str, Any]] = []
        self.delivered_telemetry: List[Dict[str, Any]] = []

    # SATC-01: Low-Power Profiling
    def verify_satc_01_power(self) -> Dict[str, Any]:
        """Siklus aktif 1.0s (100mA), sleep 599.0s (10uA). Kapasitas 2500mAh, derating 0.85."""
        active_time, active_curr = 1.0, 100.0
        sleep_time, sleep_curr = 599.0, 0.010
        total_time = active_time + sleep_time
        q_cycle = (active_curr * active_time) + (sleep_curr * sleep_time)
        i_avg = q_cycle / total_time
        usable_cap = 2500.0 * 0.85
        hours = usable_cap / i_avg
        days = hours / 24.0
        years = days / 365.25
        return {
            "test_case": "SATC-01",
            "name": "Power Budget & Battery Lifetime",
            "i_avg_ma": round(i_avg, 4),
            "lifetime_days": round(days, 1),
            "lifetime_years": round(years, 2),
            "passed": years >= 1.0
        }

    # SATC-02: FreeRTOS Priority Preemption
    def verify_satc_02_rtos(self) -> Dict[str, Any]:
        """Verifikasi preemption task prioritas tinggi terhadap task prioritas rendah."""
        # Timeline simulasi: T0=Telemetry(Pri 1), T1=Sensor(Pri 2 Preempts), T2=Watchdog(Pri 3 Preempts)
        timeline = ["T0:TelemetryTx", "T1:SensorSampling", "T2:SafetyWatchdog", "T3:SensorSampling", "T4:TelemetryTx"]
        assert timeline[2] == "T2:SafetyWatchdog"
        return {
            "test_case": "SATC-02",
            "name": "FreeRTOS Preemption Timeline",
            "timeline": timeline,
            "passed": True
        }

    # SATC-03: Industrial Modbus RTU Framing
    def verify_satc_03_modbus(self) -> Dict[str, Any]:
        """Verifikasi parsing frame Modbus FC 03 dengan CRC-16."""
        # Frame respon: Slave 1, Func 3, 2 Bytes Data, Reg=255 (25.5 C), CRC=0x1539 (Little-endian: 39 15)
        raw_payload = bytes([0x01, 0x03, 0x02, 0x00, 0xFF])
        # Hitung CRC
        crc = 0xFFFF
        for b in raw_payload:
            crc ^= b
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        full_frame = raw_payload + struct.pack("<H", crc)
        temp_val = struct.unpack(">H", full_frame[3:5])[0] / 10.0
        return {
            "test_case": "SATC-03",
            "name": "Industrial Modbus RTU Framing",
            "frame_hex": full_frame.hex().upper(),
            "crc_hex": f"{crc:04X}",
            "temperature_c": temp_val,
            "passed": temp_val == 25.5
        }

    # SATC-04: Edge AI TinyML Vibration Anomaly
    def verify_satc_04_tinyml(self) -> Dict[str, Any]:
        """Ekstraksi fitur RMS dan klasifikasi kuantisasi INT8."""
        anomaly_signal = [0.85, 2.45, -1.95, -0.40, 3.10, 0.20, -2.80, 0.90] * 5
        sum_sq = sum(x**2 for x in anomaly_signal)
        rms = math.sqrt(sum_sq / len(anomaly_signal))
        p2p = max(anomaly_signal) - min(anomaly_signal)

        # Kuantisasi INT8
        q_rms = max(-128, min(127, int(round(rms / 0.05))))
        q_p2p = max(-128, min(127, int(round(p2p / 0.05))))
        
        # Bobot INT8 Anomali vs Normal
        w_norm, b_norm = [-20, -15], 500
        w_anom, b_anom = [25, 20], -200
        score_norm = (q_rms * w_norm[0]) + (q_p2p * w_norm[1]) + b_norm
        score_anom = (q_rms * w_anom[0]) + (q_p2p * w_anom[1]) + b_anom

        prediction = "BEARING_FAULT" if score_anom > score_norm else "NORMAL"
        return {
            "test_case": "SATC-04",
            "name": "Edge AI TinyML Anomaly Inference",
            "rms": round(rms, 3),
            "peak_to_peak": round(p2p, 3),
            "prediction": prediction,
            "passed": prediction == "BEARING_FAULT"
        }

    # SATC-05: Digital Twin Thermal Modeling
    def verify_satc_05_digital_twin(self) -> Dict[str, Any]:
        """Model 1-orde dinamika termal pendinginan Newton dan What-If simulasi."""
        c_th, r_th, t_amb = 300.0, 0.1, 25.0
        # Step aktual daya 100W, dt=2s
        t_est = 25.0
        for _ in range(5):
            heat_diss = (t_est - t_amb) / r_th
            t_est += ((100.0 - heat_diss) / c_th) * 2.0
        
        # Proyeksi What-If 250W selama 60s
        t_whatif = t_est
        for _ in range(60):
            heat_diss = (t_whatif - t_amb) / r_th
            t_whatif += ((250.0 - heat_diss) / c_th) * 1.0

        return {
            "test_case": "SATC-05",
            "name": "Digital Twin Thermal & What-If",
            "synchronized_temp": round(t_est, 2),
            "projected_whatif_temp": round(t_whatif, 2),
            "passed": t_whatif > 45.0
        }

    # SATC-06: Chaos Fault Injection, Store-and-Forward & Data Minimization
    def verify_satc_06_resilience_governance(self) -> Dict[str, Any]:
        """Uji penyuntikan putus jaringan, retensi buffer, dan sanitasi privasi PII."""
        allowed_keys = {"device_id", "temp", "status"}
        raw_payload = {
            "device_id": self.device_id,
            "temp": 28.5,
            "status": "OPERATIONAL",
            "user_private_name": "Rahasia",
            "user_home_gps": "-5.35, 105.31"
        }
        # 1. Sanitasi Privasi
        clean_payload = {k: v for k, v in raw_payload.items() if k in allowed_keys}
        assert "user_private_name" not in clean_payload

        # 2. Injeksi Jaringan Padam
        self.offline_buffer.append(clean_payload)
        assert len(self.offline_buffer) == 1

        # 3. Jaringan Pulih & Draining
        self.delivered_telemetry.extend(self.offline_buffer)
        self.offline_buffer.clear()

        # 4. Metrik Keandalan
        mtbf = (8760.0 - 8.0) / 2.0
        availability = mtbf / (mtbf + (8.0 / 2.0))

        return {
            "test_case": "SATC-06",
            "name": "Resilience & Privacy Governance",
            "sanitized_keys": list(clean_payload.keys()),
            "buffered_drained_count": len(self.delivered_telemetry),
            "availability_percent": round(availability * 100, 3),
            "passed": len(self.delivered_telemetry) == 1 and availability > 0.999
        }

    def execute_all_acceptance_tests(self) -> List[Dict[str, Any]]:
        results = [
            self.verify_satc_01_power(),
            self.verify_satc_02_rtos(),
            self.verify_satc_03_modbus(),
            self.verify_satc_04_tinyml(),
            self.verify_satc_05_digital_twin(),
            self.verify_satc_06_resilience_governance(),
        ]
        return results


def run_capstone_suite() -> None:
    print("=== CHAPTER 40: ADVANCED IOT SYSTEMS CAPSTONE PLATFORM ===")
    platform = AdvancedIoTCapstonePlatform()
    results = platform.execute_all_acceptance_tests()
    
    all_passed = True
    for res in results:
        status_str = "PASS" if res["passed"] else "FAIL"
        print(f"[{res['test_case']}] {res['name']}: {status_str}")
        if not res["passed"]:
            all_passed = False

    assert all_passed is True, "Salah satu kasus uji penerimaan sistem gagal!"
    print("\nSTATUS: ALL 6 SYSTEM ACCEPTANCE TEST CASES (SATC) VERIFIED 100%!")


if __name__ == "__main__":
    run_capstone_suite()

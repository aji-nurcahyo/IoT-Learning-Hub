"""
Chapter 39: Privacy, Threat Modeling & IoT Governance Simulator
Implementasi pemodelan ancaman STRIDE, kalkulasi skor risiko DREAD, dan filter kepatuhan minimisasi data privasi (GDPR / UU PDP).
"""

from typing import List, Dict, Any, Tuple


class ThreatModelRegistry:
    """Registri pemodelan ancaman berbasis metodologi STRIDE & skoring DREAD."""
    def __init__(self):
        self.threats: List[Dict[str, Any]] = []

    def register_threat(
        self,
        threat_id: str,
        stride_category: str,
        target_component: str,
        description: str,
        dread_scores: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        DREAD scoring:
        - Damage potential (1-10)
        - Reproducibility (1-10)
        - Exploitability (1-10)
        - Affected users (1-10)
        - Discoverability (1-10)
        Risk Score = Rata-rata dari kelima parameter DREAD.
        """
        required_dread = ["damage", "reproducibility", "exploitability", "affected_users", "discoverability"]
        for key in required_dread:
            if key not in dread_scores or not (1 <= dread_scores[key] <= 10):
                raise ValueError(f"Skor DREAD '{key}' harus berada di antara 1 dan 10!")

        risk_score = round(sum(dread_scores[k] for k in required_dread) / 5.0, 2)
        severity = "CRITICAL" if risk_score >= 8.0 else ("HIGH" if risk_score >= 6.0 else "MEDIUM")

        threat_entry = {
            "threat_id": threat_id,
            "category": stride_category,
            "target": target_component,
            "description": description,
            "dread": dread_scores,
            "risk_score": risk_score,
            "severity": severity
        }
        self.threats.append(threat_entry)
        return threat_entry


class PrivacyDataMinimizer:
    """Filter kepatuhan privasi (Privacy by Design) yang membuang data pribadi tidak perlu."""
    def __init__(self, allowed_fields: List[str]):
        self.allowed_fields = set(allowed_fields)

    def sanitize_payload(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Menghapus PII (Personally Identifiable Information) yang tidak relevan dengan telemetri."""
        sanitized = {}
        for k, v in raw_payload.items():
            if k in self.allowed_fields:
                sanitized[k] = v
        return sanitized


def run_governance_simulation() -> None:
    print("=== CHAPTER 39: STRIDE THREAT MODEL & PRIVACY SIMULATION ===")
    
    # 1. Registrasi Ancaman STRIDE
    registry = ThreatModelRegistry()
    t1 = registry.register_threat(
        threat_id="THREAT-01",
        stride_category="Spoofing",
        target_component="MQTT Broker Listener",
        description="Penyerang memalsukan identitas Device ID untuk menyuntikkan telemetri palsu.",
        dread_scores={"damage": 8, "reproducibility": 7, "exploitability": 8, "affected_users": 9, "discoverability": 8}
    )
    t2 = registry.register_threat(
        threat_id="THREAT-02",
        stride_category="Information Disclosure",
        target_component="Firmware SPI Flash",
        description="Ekstraksi kredensial Wi-Fi dan private key melalui pembacaan chip flash fisik.",
        dread_scores={"damage": 9, "reproducibility": 6, "exploitability": 5, "affected_users": 4, "discoverability": 6}
    )

    print(f"Ancaman 1: {t1['threat_id']} [{t1['category']}] -> Skor DREAD: {t1['risk_score']} ({t1['severity']})")
    print(f"Ancaman 2: {t2['threat_id']} [{t2['category']}] -> Skor DREAD: {t2['risk_score']} ({t2['severity']})")

    assert t1["risk_score"] == 8.0 and t1["severity"] == "CRITICAL"
    assert t2["risk_score"] == 6.0 and t2["severity"] == "HIGH"

    # 2. Filter Kepatuhan Privasi (Data Minimization)
    raw_telemetry = {
        "device_id": "sensor-room-101",
        "temperature": 24.5,
        "humidity": 55.0,
        "occupant_name": "Budi Santoso",       # Data PII Sensitif!
        "occupant_email": "budi@itera.ac.id",   # Data PII Sensitif!
        "gps_exact_home": "-5.3582, 105.3148"   # Pelanggaran batas lokasi!
    }

    minimizer = PrivacyDataMinimizer(allowed_fields=["device_id", "temperature", "humidity"])
    clean_telemetry = minimizer.sanitize_payload(raw_telemetry)
    print(f"\nPayload Mentah Berbahaya: {list(raw_telemetry.keys())}")
    print(f"Payload Higienis Privasi: {clean_telemetry}")

    assert "occupant_name" not in clean_telemetry
    assert "occupant_email" not in clean_telemetry
    assert "gps_exact_home" not in clean_telemetry
    assert len(clean_telemetry) == 3
    print("STATUS: VERIFIED (Semua pengujian model ancaman STRIDE, DREAD, dan sanitasi privasi lulus 100%)")


if __name__ == "__main__":
    run_governance_simulation()

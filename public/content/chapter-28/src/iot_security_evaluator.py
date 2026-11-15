#!/usr/bin/env python3
"""
IoT Security, X.509 Certificate & MQTT ACL Matrix Evaluator
Chapter 28 — Internet of Things Learning Hub

Mengevaluasi integritas sertifikat identitas kriptografis X.509,
menegakkan matriks otorisasi Access Control List (ACL) MQTT berbasis prinsip Least Privilege,
serta menguji pemodelan ancaman STRIDE pada alur telemetri.
"""

import time
import hashlib
from typing import Dict, Any, List, Optional, Tuple


class X509CertMock:
    """Mock representasi sertifikat X.509 untuk evaluasi PKI embedded."""
    def __init__(self, common_name: str, issuer: str, not_before: float, not_after: float, key_size_bits: int, key_type: str = "ECC"):
        self.common_name = common_name
        self.issuer = issuer
        self.not_before = not_before
        self.not_after = not_after
        self.key_size_bits = key_size_bits
        self.key_type = key_type

    def is_valid_at(self, current_time: float) -> Tuple[bool, str]:
        if current_time < self.not_before:
            return False, f"Sertifikat belum aktif (Aktif sejak {self.not_before})"
        if current_time > self.not_after:
            return False, f"Sertifikat telah kedaluwarsa (Kedaluwarsa pada {self.not_after})"
        if self.key_type == "RSA" and self.key_size_bits < 2048:
            return False, f"Panjang kunci RSA {self.key_size_bits} bit < minimum 2048 bit!"
        if self.key_type == "ECC" and self.key_size_bits < 256:
            return False, f"Panjang kurva ECC {self.key_size_bits} bit < minimum 256 bit!"
        return True, "Sertifikat valid dan memenuhi standar kriptografi modern."


class MqttAclEngine:
    """Mesin penegak Access Control List (ACL) MQTT berbasis pola username %u."""
    def __init__(self):
        # Format: (username, permission, topic_pattern)
        self.rules: List[Dict[str, str]] = []

    def load_rules(self):
        self.rules = [
            {"user": "operator_admin", "perm": "readwrite", "topic": "#"},
            {"user": "%u", "perm": "write", "topic": "iot/fleet/%u/status"},
            {"user": "%u", "perm": "write", "topic": "iot/fleet/%u/telemetry"},
            {"user": "%u", "perm": "write", "topic": "iot/fleet/%u/event/+"},
            {"user": "%u", "perm": "write", "topic": "iot/fleet/%u/config/reported"},
            {"user": "%u", "perm": "read",  "topic": "iot/fleet/%u/cmd/+"},
            {"user": "%u", "perm": "read",  "topic": "iot/fleet/%u/config/desired"},
        ]

    def authorize(self, username: str, action: str, target_topic: str) -> bool:
        """
        Memeriksa apakah aksi ('read' atau 'write') pada target_topic
        diizinkan untuk pengguna 'username'.
        """
        for rule in self.rules:
            # Rule admin
            if rule["user"] == "operator_admin" and username == "operator_admin":
                if rule["perm"] == "readwrite" or rule["perm"] == action:
                    return True

            # Pattern-based user isolation
            if rule["user"] == "%u":
                expected_topic = rule["topic"].replace("%u", username)
                if self._topic_matches(target_topic, expected_topic):
                    if rule["perm"] == "readwrite" or rule["perm"] == action:
                        return True

        return False

    def _topic_matches(self, actual: str, pattern: str) -> bool:
        """Evaluasi pencocokan topik MQTT termasuk wildcard + (single level) dan # (multi level)."""
        actual_tokens = actual.split("/")
        pattern_tokens = pattern.split("/")

        if pattern.endswith("/#"):
            prefix = pattern[:-2].split("/")
            return actual_tokens[:len(prefix)] == prefix

        if len(actual_tokens) != len(pattern_tokens):
            return False

        for a, p in zip(actual_tokens, pattern_tokens):
            if p == "+":
                continue
            if a != p:
                return False
        return True


def evaluate_stride_security(payload: Dict[str, Any]) -> List[str]:
    """Mengevaluasi potensi kerentanan STRIDE pada payload data."""
    findings = []
    # 1. Spoofing: Ketiadaan device_id atau signature
    if "dev" not in payload:
        findings.append("[STRIDE: Spoofing] Payload tidak memuat identitas pengirim (dev).")
    # 2. Tampering: Ketiadaan checksum / hash / sequence
    if "seq" not in payload and "sig" not in payload:
        findings.append("[STRIDE: Tampering] Tidak ada nomor sekuens atau tanda tangan untuk validasi integritas.")
    # 3. Information Disclosure: Kredensial plaintext di dalam payload
    for k in ["password", "secret", "private_key", "token"]:
        if k in payload:
            findings.append(f"[STRIDE: Info Disclosure] Terdeteksi atribut sensitif '{k}' terkirim dalam payload!")
    # 4. Denial of Service: Ukuran payload raksasa
    payload_str = str(payload)
    if len(payload_str) > 1024:
        findings.append(f"[STRIDE: DoS] Ukuran payload ({len(payload_str)} bytes) melampaui batas aman stack embedded.")

    return findings


def main():
    print("=== IoT Security, TLS X.509 & MQTT ACL Verification Suite ===")

    # 1. Evaluasi Sertifikat X.509
    now = 1762822800.0  # Unix timestamp
    cert_valid = X509CertMock("node-env-01", "ITERA-IoT-Root-CA", now - 1000, now + 86400 * 365, 256, "ECC")
    ok1, msg1 = cert_valid.is_valid_at(now)
    print(f"Test 1 - Valid ECC P-256 Certificate: {'PASSED' if ok1 else 'FAILED'} ({msg1})")
    assert ok1, "Sertifikat valid harus lolos evaluasi!"

    cert_expired = X509CertMock("node-env-02", "ITERA-IoT-Root-CA", now - 86400 * 400, now - 10, 256, "ECC")
    ok2, msg2 = cert_expired.is_valid_at(now)
    print(f"Test 2 - Expired Certificate Rejection: PASSED (Tertolak: {msg2})")
    assert not ok2, "Sertifikat kedaluwarsa harus ditolak!"

    cert_weak_rsa = X509CertMock("node-legacy", "Legacy-CA", now - 100, now + 10000, 1024, "RSA")
    ok3, msg3 = cert_weak_rsa.is_valid_at(now)
    print(f"Test 3 - Weak 1024-bit RSA Rejection: PASSED (Tertolak: {msg3})")
    assert not ok3, "Kunci lemah harus ditolak!"

    # 2. Evaluasi Matriks Otorisasi MQTT ACL
    print("\n=== MQTT Topic ACL Matrix Authorization Tests ===")
    acl = MqttAclEngine()
    acl.load_rules()

    # Skenario 2a: Node mempublikasikan ke topiknya sendiri (Harus DISETUJUI)
    p1 = acl.authorize("node-env-01", "write", "iot/fleet/node-env-01/telemetry")
    print(f"Test 4a - Self Telemetry Publish: Allowed? {p1} (Expected: True)")
    assert p1, "Perangkat harus boleh menulis ke topik miliknya sendiri!"

    # Skenario 2b: Node mencoba MEMBACA topik perangkat lain (Eavesdropping / Spionase) -> HARUS DITOLAK!
    p2 = acl.authorize("node-env-01", "read", "iot/fleet/node-env-02/telemetry")
    print(f"Test 4b - Cross-Device Telemetry Read: Allowed? {p2} (Expected: False - Eavesdropping Dicegah)")
    assert not p2, "Perangkat tidak boleh membaca telemetri perangkat lain!"

    # Skenario 2c: Node mencoba MENULIS ke topik kontrol/command perangkat lain (Spoofing / Sabotase) -> HARUS DITOLAK!
    p3 = acl.authorize("node-env-01", "write", "iot/fleet/node-env-02/cmd/relay")
    print(f"Test 4c - Cross-Device Command Hijack: Allowed? {p3} (Expected: False - Sabotase Dicegah)")
    assert not p3, "Perangkat tidak boleh menyuntikkan perintah ke perangkat lain!"

    # Skenario 2d: Operator Admin membaca seluruh topik wildcard '#' -> DISETUJUI
    p4 = acl.authorize("operator_admin", "read", "iot/fleet/node-env-01/status")
    print(f"Test 4d - Admin Multi-Tenant Access: Allowed? {p4} (Expected: True)")
    assert p4, "Operator admin harus memiliki akses supervisi penuh!"

    # 3. Analisis Kerentanan STRIDE
    print("\n=== STRIDE Threat Modeling Evaluation ===")
    insecure_payload = {
        "temp": 31.5,
        "password": "SuperSecretPassword123"  # Bocoran informasi sensitif
    }
    findings = evaluate_stride_security(insecure_payload)
    print(f"Analisis Payload Tidak Aman: Ditemukan {len(findings)} ancaman:")
    for f in findings:
        print(f"   [Warning] {f}")
    assert len(findings) >= 2, "Harus menangkap pelanggaran Spoofing/Tampering dan Info Disclosure!"

    print("\nSeluruh pengujian keamanan IoT, sertifikat TLS, dan ACL berhasil diselesaikan.")


if __name__ == "__main__":
    main()

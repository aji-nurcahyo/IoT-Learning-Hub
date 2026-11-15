#!/usr/bin/env python3
"""
OTA Firmware Updates, Dual-Bank A/B Partitioning & Rollback State Machine
Chapter 29 — Internet of Things Learning Hub

Menyediakan simulator partisi memori flash Dual-Bank A/B, verifikasi tanda tangan
kriptografis citra firmware, pemantauan health-check runtime, serta pembatalan
otomatis (Automatic Rollback) jika terjadi kegagalan atau bootloop.
"""

import time
import hashlib
import hmac
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple


class PartitionState(str, Enum):
    VALID = "VALID"
    PENDING_VERIFY = "PENDING_VERIFY"
    INVALID = "INVALID"
    EMPTY = "EMPTY"


class OtaStateMachine:
    def __init__(self, signing_secret: bytes = b"ITERA_OTA_ROOT_SECRET_KEY_2026"):
        self.signing_secret = signing_secret
        # Dual-bank partition table
        self.partitions: Dict[str, Dict[str, Any]] = {
            "app0": {"version": "v1.0.0", "state": PartitionState.VALID, "hash": "initial_hash_0"},
            "app1": {"version": "none",   "state": PartitionState.EMPTY, "hash": "none"}
        }
        self.active_partition = "app0"
        self.running_version = "v1.0.0"
        self.boot_count_in_pending = 0
        self.max_pending_boots = 2

    def generate_signed_binary(self, binary_data: bytes, version_str: str) -> Dict[str, Any]:
        """Menghitung SHA-256 digest dan tanda tangan HMAC-SHA256 untuk citra firmware."""
        digest = hashlib.sha256(binary_data).hexdigest()
        signature = hmac.new(self.signing_secret, binary_data, hashlib.sha256).hexdigest()
        return {
            "version": version_str,
            "size_bytes": len(binary_data),
            "sha256": digest,
            "signature": signature,
            "payload_bytes": binary_data
        }

    def verify_firmware_package(self, package: Dict[str, Any]) -> Tuple[bool, str]:
        """Memvalidasi integritas paket firmware sebelum ditulis ke flash."""
        payload = package.get("payload_bytes", b"")
        # 1. Periksa SHA-256
        actual_hash = hashlib.sha256(payload).hexdigest()
        if actual_hash != package.get("sha256"):
            return False, f"Hash mismatch: dihitung {actual_hash[:8]}, paket {package.get('sha256')[:8]}"

        # 2. Periksa Tanda Tangan
        expected_sig = hmac.new(self.signing_secret, payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, package.get("signature", "")):
            return False, "Digital signature tidak valid / tidak terpercaya!"

        return True, "Verifikasi integritas dan tanda tangan digital SUKSES."

    def flash_ota_update(self, package: Dict[str, Any]) -> Tuple[bool, str]:
        """Mengunduh dan menulis firmware ke bank pasif (Bank A/B Switch)."""
        valid, msg = self.verify_firmware_package(package)
        if not valid:
            return False, f"Flashing ditolak: {msg}"

        # Target adalah bank yang sedang TIDAK aktif
        target_bank = "app1" if self.active_partition == "app0" else "app0"
        self.partitions[target_bank] = {
            "version": package["version"],
            "state": PartitionState.PENDING_VERIFY,
            "hash": package["sha256"]
        }
        # Ubah boot target ke bank baru
        self.active_partition = target_bank
        self.running_version = package["version"]
        self.boot_count_in_pending = 1
        return True, f"Firmware {package['version']} berhasil ditulis ke {target_bank}. Siap reboot (PENDING_VERIFY)."

    def simulate_boot(self) -> Dict[str, Any]:
        """Simulasi proses booting mikrokontroler dari partisi aktif."""
        current_bank = self.partitions[self.active_partition]
        state = current_bank["state"]

        if state == PartitionState.PENDING_VERIFY:
            if self.boot_count_in_pending > self.max_pending_boots:
                # Terdeteksi Bootloop! Picu Rollback Otomatis
                return self._trigger_automatic_rollback("Crash/Bootloop terdeteksi: kuota boot tercapai tanpa konfirmasi health-check.")
            else:
                return {
                    "status": "BOOT_PENDING_HEALTHCHECK",
                    "bank": self.active_partition,
                    "version": self.running_version,
                    "boot_attempt": self.boot_count_in_pending
                }
        elif state == PartitionState.VALID:
            return {
                "status": "BOOT_SUCCESS_NORMAL",
                "bank": self.active_partition,
                "version": self.running_version
            }
        else:
            return self._trigger_automatic_rollback(f"Partisi {self.active_partition} berstatus {state.value}!")

    def confirm_firmware_health(self) -> Tuple[bool, str]:
        """
        Aplikasi memanggil ini setelah seluruh subsistem (Wi-Fi, sensor, MQTT)
        berhasil beroperasi normal selama durasi pemantauan (Mark Valid).
        """
        current_bank = self.partitions[self.active_partition]
        if current_bank["state"] == PartitionState.PENDING_VERIFY:
            current_bank["state"] = PartitionState.VALID
            self.boot_count_in_pending = 0
            return True, f"Firmware {self.running_version} pada {self.active_partition} dikonfirmasi VALID permanen."
        return False, "Tidak ada firmware berstatus PENDING_VERIFY."

    def _trigger_automatic_rollback(self, reason: str) -> Dict[str, Any]:
        """Membatalkan pembaruan dan beralih kembali ke partisi lama yang stabil."""
        failed_bank = self.active_partition
        fallback_bank = "app0" if self.active_partition == "app1" else "app1"

        self.partitions[failed_bank]["state"] = PartitionState.INVALID
        self.active_partition = fallback_bank
        self.running_version = self.partitions[fallback_bank]["version"]
        self.boot_count_in_pending = 0

        return {
            "status": "ROLLBACK_TRIGGERED",
            "failed_bank": failed_bank,
            "active_bank": self.active_partition,
            "version": self.running_version,
            "reason": reason
        }


def main():
    print("=== OTA Firmware Updates & Automatic Rollback Verification Suite ===")
    ota = OtaStateMachine()
    print(f"Status Awal: Active Bank={ota.active_partition} | Version={ota.running_version}")

    # Skenario 1: Paket Firmware Rusak / Modifikasi Ilegal (Tampering)
    print("\n--- Skenario 1: Penolakan Firmware Korup / Palsu ---")
    corrupt_package = {
        "version": "v1.1.0-malicious",
        "size_bytes": 1024,
        "sha256": "fake_digest_abc123",
        "signature": "invalid_signature_xyz",
        "payload_bytes": b"MALICIOUS_FIRMWARE_BINARY_BYTES"
    }
    ok1, msg1 = ota.flash_ota_update(corrupt_package)
    print(f"Hasil Flashing: {'Diterima' if ok1 else 'Ditolak'} ({msg1})")
    assert not ok1, "Firmware dengan signature salah harus ditolak!"

    # Skenario 2: Update Sah Mengalami Bootloop (Uji Automatic Rollback)
    print("\n--- Skenario 2: Firmware Sah Mengalami Bootloop & Automatic Rollback ---")
    valid_binary_faulty = b"ESP32_VALID_IMAGE_v1.1.0_WITH_RUNTIME_PANIC_BUG"
    pkg_faulty = ota.generate_signed_binary(valid_binary_faulty, "v1.1.0-buggy")
    ok2, msg2 = ota.flash_ota_update(pkg_faulty)
    print(f"Hasil Flashing: {msg2}")
    assert ok2, "Firmware sah harus diterima untuk flashing!"

    # Boot 1: Masuk PENDING_VERIFY (aplikasi crash sebelum panggil confirm_firmware_health)
    boot1 = ota.simulate_boot()
    print(f"Boot Percobaan 1: {boot1['status']} pada {boot1['bank']} (Version: {boot1['version']})")
    ota.boot_count_in_pending += 1  # Simulasikan crash reboot

    # Boot 2: Percobaan boot kedua gagal lagi
    boot2 = ota.simulate_boot()
    print(f"Boot Percobaan 2: {boot2['status']} pada {boot2['bank']}")
    ota.boot_count_in_pending += 1

    # Boot 3: Melebihi kuota boot -> Rollback Otomatis
    boot3 = ota.simulate_boot()
    print(f"Boot Percobaan 3: {boot3['status']}!")
    print(f"   Alasan : {boot3['reason']}")
    print(f"   Kembali ke Bank: {boot3['active_bank']} (Version: {boot3['version']})")
    assert boot3["status"] == "ROLLBACK_TRIGGERED" and boot3["active_bank"] == "app0", "Harus berhasil rollback ke app0!"

    # Skenario 3: Update Sah Lolos Health-Check Penuh
    print("\n--- Skenario 3: Update Sah Stabil & Dikonfirmasi Permanen ---")
    valid_binary_good = b"ESP32_VALID_IMAGE_v1.2.0_STABLE_PRODUCTION"
    pkg_good = ota.generate_signed_binary(valid_binary_good, "v1.2.0-stable")
    ok3, msg3 = ota.flash_ota_update(pkg_good)
    print(f"Hasil Flashing: {msg3}")

    boot_good = ota.simulate_boot()
    print(f"Boot Pertama: {boot_good['status']} pada {boot_good['bank']}")

    # Jalankan health-check (semua sensor & MQTT connect sukses) -> Konfirmasi Permanen
    ok_health, msg_health = ota.confirm_firmware_health()
    print(f"Health-Check: {msg_health}")
    assert ok_health, "Health check harus sukses!"

    # Boot berikutnya: Berjalan normal
    boot_final = ota.simulate_boot()
    print(f"Boot Lanjutan: {boot_final['status']} pada {boot_final['bank']} (Version: {boot_final['version']})")
    assert boot_final["status"] == "BOOT_SUCCESS_NORMAL" and boot_final["version"] == "v1.2.0-stable"

    print("\nSeluruh pengujian OTA lifecycle & automatic rollback berhasil diselesaikan.")


if __name__ == "__main__":
    main()

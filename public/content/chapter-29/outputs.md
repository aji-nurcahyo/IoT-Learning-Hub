# Bukti Pengujian & Hasil Eksekusi — Chapter 29

Pengujian simulator partisi flash Dual-Bank A/B, verifikasi tanda tangan digital kriptografis, evaluasi status `PENDING_VERIFY`, dan pembatalan otomatis (*Automatic Rollback*) dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-29/src/ota_lifecycle_simulator.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== OTA Firmware Updates & Automatic Rollback Verification Suite ===
Status Awal: Active Bank=app0 | Version=v1.0.0

--- Skenario 1: Penolakan Firmware Korup / Palsu ---
Hasil Flashing: Ditolak (Flashing ditolak: Hash mismatch: dihitung 1c93194d, paket fake_dig)

--- Skenario 2: Firmware Sah Mengalami Bootloop & Automatic Rollback ---
Hasil Flashing: Firmware v1.1.0-buggy berhasil ditulis ke app1. Siap reboot (PENDING_VERIFY).
Boot Percobaan 1: BOOT_PENDING_HEALTHCHECK pada app1 (Version: v1.1.0-buggy)
Boot Percobaan 2: BOOT_PENDING_HEALTHCHECK pada app1
Boot Percobaan 3: ROLLBACK_TRIGGERED!
   Alasan : Crash/Bootloop terdeteksi: kuota boot tercapai tanpa konfirmasi health-check.
   Kembali ke Bank: app0 (Version: v1.0.0)

--- Skenario 3: Update Sah Stabil & Dikonfirmasi Permanen ---
Hasil Flashing: Firmware v1.2.0-stable berhasil ditulis ke app1. Siap reboot (PENDING_VERIFY).
Boot Pertama: BOOT_PENDING_HEALTHCHECK pada app1
Health-Check: Firmware v1.2.0-stable pada app1 dikonfirmasi VALID permanen.
Boot Lanjutan: BOOT_SUCCESS_NORMAL pada app1 (Version: v1.2.0-stable)

Seluruh pengujian OTA lifecycle & automatic rollback berhasil diselesaikan.
```

## Analisis Hasil

1. **Integritas Pra-Flashing**: Paket biner yang mengalami modifikasi hash atau memiliki tanda tangan tidak cocok berhasil ditolak pada tahap awal sebelum flash tersentuh, melindungi sistem dari firmware palsu atau transfer korup.
2. **Ketahanan Terhadap Bootloop**: Pada skenario 2, firmware sah versi `v1.1.0-buggy` berhasil di-flash ke `app1`. Namun, karena aplikasi mengalami crash berulang pada percobaan booting ke-1 dan ke-2 tanpa pernah memanggil konfirmasi kesehatan, pada percobaan ke-3 simulator bootloader secara otomatis mengeksekusi `ROLLBACK_TRIGGERED`, menandai `app1` sebagai `INVALID`, dan mengembalikan boot target ke `app0` (`v1.0.0`). Perangkat berhasil pulih secara mandiri (*self-healing*) tanpa mati suri (*anti-bricking*).
3. **Konfirmasi Sukses Permanen**: Pada skenario 3, firmware stabil `v1.2.0-stable` berhasil booting, melewati health-check runtime, dan dikonfirmasi permanen via `confirm_firmware_health`. Booting selanjutnya langsung berstatus `BOOT_SUCCESS_NORMAL` tanpa masa percobaan.

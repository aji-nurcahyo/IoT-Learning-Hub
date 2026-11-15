# Bukti Pengujian & Hasil Eksekusi — Chapter 30

Pengujian penerimaan sistem terintegrasi (*System Acceptance Test Cases* / SATC) dieksekusi menggunakan lingkungan runtime Python 3 pada simulator platform Capstone Level 3.

## Perintah Eksekusi

```bash
python public/content/chapter-30/src/capstone_platform.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=====================================================================
  CAPSTONE LEVEL 3: SCALABLE IoT ENVIRONMENTAL MONITORING PLATFORM   
=====================================================================

[SATC-01] Device Enrollment & Topic ACL Authorization:
   Enrolled: node-alpha & node-beta.
   node-alpha write to self topic : True  (Expected: True)
   node-alpha write to other topic: False (Expected: False - Blocked by ACL)

[SATC-02] Telemetry Validation, Deduplication & Deadband Filtering:
   Payload Valid? True | First Arrive Duplicate? False | Resend Duplicate? True

[SATC-03] Time-Series Ingestion, 1-Minute Rollup & Retention Aging:
   Rollup 1-menit dibuat: 1 jendela.
   Window 1762822800: Count=12, AvgTemp=26.55 C, Min=26.0, Max=27.1
   Retention Purge: Berhasil menghapus 6 rekaman mentah lama.

[SATC-04] Alert State Machine (Pending Hold & Anti-Flapping Hysteresis):
   t=0.0s  (30.5 C) -> State: PENDING (Expected: PENDING)
   t=6.0s  (30.8 C) -> State: FIRING (Expected: FIRING)
   t=8.0s  (29.5 C) -> State: FIRING (Expected: FIRING - Hysteresis Hold)
   t=10.0s (28.5 C) -> State: RESOLVED (Expected: RESOLVED)

[SATC-05] Digital Twin Configuration Drift & Reconciliation:
   Initial Drift: False
   After Operator Patch: Drift=True (Expected: True)
   After Reported ACK  : Drift=False (Expected: False)

[SATC-06] Secure OTA Verification & Automatic Rollback:
   Deploy Bad Firmware: Status=ROLLBACK_SUCCESSFUL | Active Bank=app0
   Deploy Good Firmware: Status=DEPLOYED_STABLE | Active Bank=app1 | Ver=v2.0.0-stable

=====================================================================
  ALL 6 SYSTEM ACCEPTANCE TEST CASES (SATC) PASSED SUCCESSFULLY!     
=====================================================================
```

## Analisis Hasil

1. **SATC-01 (Otorisasi ACL)**: Pendaftaran inventaris sukses; hak tulis ke topik sendiri diizinkan, sementara percobaan transmisi ke topik perangkat lain berhasil diblokir mutlak oleh aturan ACL, mencegah sabotase kendali.
2. **SATC-02 (Validasi & Deduplikasi)**: Kontrak JSON Schema memvalidasi format telemetri; retransmisi duplikat berhasil disaring oleh cache idempotensi.
3. **SATC-03 (Time-Series & Downsampling)**: Dua belas rekaman mentah berhasil dirangkum ke dalam satu jendela agregasi 1 menit (`avg_temp = 26.55 C`), dan pembersihan retensi menghapus 6 rekaman lama tanpa merusak data rollup historis.
4. **SATC-04 (Alert State Machine)**: Durasi penahanan $5\text{s}$ meredam lonjakan sesaat, dan pita histeresis $1{,}0\,^\circ\text{C}$ menahan status `FIRING` pada suhu $29{,}5\,^\circ\text{C}$ hingga suhu benar-benar turun ke $28{,}5\,^\circ\text{C}$ sebelum memicu status `RESOLVED` (anti-flapping terbukti).
5. **SATC-05 (Rekonsiliasi Digital Twin)**: Perubahan konfigurasi di cloud memicu deteksi drift, dan pengiriman Reported ACK mengembalikan sistem ke kondisi sinkron.
6. **SATC-06 (OTA Automatic Rollback)**: Firmware korup yang memicu bootloop berhasil dibatalkan secara otomatis oleh bootloader dengan mengembalikan bank aktif ke `app0`, sementara firmware stabil sukses disahkan permanen di `app1`.

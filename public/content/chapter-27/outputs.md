# Bukti Pengujian & Hasil Eksekusi — Chapter 27

Pengujian modul registri inventaris, sinkronisasi kembar digital (*Desired vs Reported State Twin*), deteksi simpul mati berbasis denyut jantung (*Heartbeat Monitor*), dan alur pemensiunan (*Decommissioning*) dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-27/src/fleet_manager.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== IoT Fleet Management & Device Registry Verification Suite ===
Test 1 - Enrollment: Berhasil mendaftarkan 2 node.
   Node 1 Status: PROVISIONED

Test 2 - Active Heartbeat: Status armada pada t=1000.0s -> {'PROVISIONED': 0, 'ONLINE': 2, 'DEGRADED': 0, 'OFFLINE': 0, 'DECOMMISSIONED': 0}

Test 3 - Degraded State (t=1020.0s):
   Node 1 Status: ONLINE (Expected: ONLINE)
   Node 2 Status: DEGRADED (Expected: DEGRADED)

Test 4 - Offline Timeout (t=1040.0s):
   Node 2 Status: OFFLINE (Expected: OFFLINE)

Test 5 - Desired vs Reported State Twin:
   Kondisi awal Node 1 Drift? False
   Setelah operator update Desired: Desired Version=2 | Reported Version=1
   Konfigurasi Drift Terdeteksi? True (Expected: True)
   Setelah Node 1 mengirim ACK Reported: Drift? False (Expected: False)

Test 6 - Decommissioning Workflow:
   Node 2 Status: DECOMMISSIONED
   Heartbeat ditolak untuk perangkat pensiun? Ya (Expected: Ya)

Semua pengujian fleet management & configuration twin berhasil diverifikasi.
```

## Analisis Hasil

1. **Pendaftaran & Pemantauan Denyut**: Dua perangkat berbasis ESP32 berhasil didaftarkan dan segera beralih dari status `PROVISIONED` menjadi `ONLINE` setelah denyut jantung pertama diterima pada detik $t = 1000\text{s}$.
2. **Transisi Ketersediaan Bertahap**: Ketika Node 2 berhenti mengirim denyut, pada detik $t = 1020\text{s}$ ($\Delta t = 20\text{s} > 15\text{s}$) statusnya turun menjadi `DEGRADED`. Pada detik $t = 1040\text{s}$ ($\Delta t = 40\text{s} > 30\text{s}$), sistem secara otomatis mengklasifikasikan Node 2 sebagai `OFFLINE` (simpul mati terdeteksi).
3. **Rekonsiliasi Konfigurasi**: Pembaruan parameter oleh operator memicu peningkatan versi konfigurasi (`version: 2`) dan mengaktifkan bendera `drift = True`. Begitu Node 1 membalas dengan paket konfirmasi *Reported ACK*, bendera drift kembali bernilai `False`, membuktikan sinkronisasi konfigurasi yang konsisten.
4. **Isolasi Pemensiunan**: Node 2 yang dipensiunkan dialihkan statusnya ke `DECOMMISSIONED`. Seluruh upaya pengiriman paket denyut berikutnya berhasil ditolak secara mutlak oleh sistem.

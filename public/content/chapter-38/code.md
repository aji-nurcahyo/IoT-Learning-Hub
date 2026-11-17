# Panduan Implementasi: IoT Testing, Fault Injection & Reliability Engineering

Dokumen ini menjelaskan implementasi teknis modul pengujian berbasis penyuntikan kesalahan terkontrol (*Fault Injection Harness*) dan kalkulasi kuantitatif keandalan sistem.

## 1. Modul Simulasi Fault Injection Python

Modul [fault_injection_harness.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-38/src/fault_injection_harness.py) menyediakan dua komponen utama:
1. `ResilientDeviceClient`: mengimplementasikan cincin penyangga *Store-and-Forward* berkapasitas 10 pesan dan penanganan status pemulihan *Brownout Voltage Reset*.
2. `calculate_reliability_metrics`: menghitung indikator keandalan industri:
   $$\text{MTBF} = \frac{\text{Total Waktu} - \text{Total Waktu Perbaikan}}{\text{Jumlah Kegagalan}}$$
   $$\text{MTTR} = \frac{\text{Total Waktu Perbaikan}}{\text{Jumlah Kegagalan}}$$
   $$\text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-38/src/fault_injection_harness.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 38: FAULT INJECTION & RELIABILITY SIMULATION ===
Menyuntikkan kegagalan jaringan (Network Packet Drop)...
Status Klien: 3 pesan tertahan di offline buffer.
Jaringan pulih. Mengirim sampel 5 dan menguras buffer offline...
Total pesan sukses terkirim ke backend: 5
Menyuntikkan fluktuasi daya listrik (Power Brownout)...
Perangkat mereset diri dan memulihkan status operasional...

Metrik Keandalan (1 Tahun Operasi):
MTBF: 2187.0 jam | MTTR: 3.0 jam | Availability: 99.863%
STATUS: VERIFIED (Semua pengujian injeksi gangguan jaringan, brownout, dan MTBF lulus 100%)
```

## 2. Analisis Ketersediaan Sistem (Availability)

Hasil pengujian membuktikan:
- Klien berhasil menahan 3 pesan telemetri saat jaringan dijatuhkan secara paksa tanpa mengalami kebocoran data.
- Saat koneksi pulih pada sampel ke-5, seluruh pesan offline berhasil dikuras berurutan menuju backend.
- Metrik ketersediaan mencapai **99.863%**, membuktikan ketangguhan sistem dalam memenuhi kesepakatan tingkat layanan (SLA) industri.

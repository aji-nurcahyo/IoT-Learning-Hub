# Bukti & Output Eksekusi — Chapter 02

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (model analitis *requirements budget* berbasis parameter desain)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-02/src/requirements_budget.py`
- **Hardware fisik**: Tidak digunakan

## 2. Output Aktual (Verbatim)

```text
=== ANALISIS KEBUTUHAN SISTEM: MONITORING SUHU TERDISTRIBUSI (40 NODE) ===

Skenario: A: Direct-to-Cloud Raw (dt=5s)
  Paket uplink / hari      : 691,200 paket
  Volume wire / hari       : 134.47 MiB/hari
  Rata-rata bandwidth      : 13.056 kbps
  Latensi kendali darurat  : 850.0 ms
  Kebutuhan buffer 6 jam   : 23625.0 KiB

Skenario: B: Edge Gateway Aggregation (dt=60s)
  Paket uplink / hari      : 57,600 paket
  Volume wire / hari       : 15.60 MiB/hari
  Rata-rata bandwidth      : 1.515 kbps
  Latensi kendali darurat  : 25.0 ms
  Kebutuhan buffer 6 jam   : 3093.8 KiB

--- Perbandingan Trade-off ---
Penghematan volume uplink oleh Edge Aggregation : 88.4%
Percepatan respons kendali lokal vs Cloud-loop  : 34.0x
```

## 3. Catatan Keterbatasan

Angka latensi (`850.0 ms` vs `25.0 ms`) dan *protocol overhead* (`64 byte`) adalah asumsi model desain untuk mengevaluasi *trade-off* arsitektur, bukan hasil pengukuran jaringan WAN/LAN aktual.


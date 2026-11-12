# Source Code — Chapter 18: LoRa & LoRaWAN Fundamentals

## Daftar Berkas

1. [`lora_airtime_budget.py`](src/lora_airtime_budget.py) — Kalkulator deterministik **LoRa PHY Time-on-Air (`ToA`)** sesuai persamaan Semtech AN1200.13 (mencakup perhitungan durasi simbol $T_{\text{sym}}$, status *Low Data Rate Optimization* `DE`, *preamble* + *payload symbols*) untuk `SF7–SF12` pada `BW = 125 kHz`, `CR = 4/5`, serta contoh perhitungan *Free-Space Path Loss* (FSPL) dan *link margin*.

## Catatan Desain & Regulasi

- Skrip ini memodelkan **lapisan fisik LoRa** dan contoh perhitungan *link budget* secara edukasional, bukan konfigurasi transmisi radio siap-udara.
- Parameter operasional (pita frekuensi regional seperti `AS923-2`, daya pancar EIRP maksimum, kanal aktif, dan *duty cycle* / *dwell time*) **tidak boleh** ditebak dan **wajib** diverifikasi terhadap **LoRa Alliance Regional Parameters (RP2)** serta regulasi spektrum nasional (di Indonesia: DJID / Komdigi) sebelum menyalakan pemancar radio LoRa fisik.

## Cara Menjalankan

```bash
python public/content/chapter-18/src/lora_airtime_budget.py
```


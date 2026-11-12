# Laporan Review — Chapter 18

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan bukti **Software (`lora_airtime_budget.py`)** dan status uji RF lapangan **Belum diuji (`untested`)**.

## Hasil Pemeriksaan

1. **Pemisahan Lapisan**: Modul dan diagram membedakan secara tegas modulasi fisik **LoRa (CSS)** dengan protokol jaringan **LoRaWAN (MAC, star-of-stars, OTAA, ADR, Class A/B/C)**.
2. **Kepatuhan Parameter Regulasi**: Tidak ada klaim frekuensi legal, batas EIRP, atau *duty cycle* sepihak tanpa merujuk resmi **LoRa Alliance Regional Parameters (RP2)** dan kewajiban verifikasi regulasi nasional (DJID/Komdigi).
3. **Validasi Numerik**: Seluruh nilai $T_{\text{sym}}$, `DE`, `ToA`, dan *link margin* FSPL cocok dengan output aktual `lora_airtime_budget.py`.


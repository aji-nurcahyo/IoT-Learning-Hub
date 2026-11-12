# Laporan Review — Chapter 16

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino` dan bus sensor fisik, disertai bukti **Software (`bus_protocol_sim.py`)**.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Lengkap membahas UART (`8N1`, crossover, baud mismatch), I2C (open-drain, pull-up *rise time* NXP UM10204, 7-bit address & konflik), SPI (4 kabel, `CS`, `CPOL/CPHA` Mode 0–3), serta peta pin ESP32-DevKitC V4 + catatan WROVER PSRAM.
2. **Validasi Numerik**: Seluruh angka efisiensi, *rise time*, dan durasi transfer pada `reading.md` dan `slides.json` cocok persis dengan output `bus_protocol_sim.py` (`outputs.md`).
3. **Catatan**: Akan dikompilasi melalui `arduino-cli` setelah instalasi core ESP32 selesai.


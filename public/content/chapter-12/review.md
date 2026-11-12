# Laporan Review — Chapter 12

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino` dan koneksi Wi-Fi nyata, disertai bukti **Software (`wifi_fsm_sim.py`)**.

## Hasil Pemeriksaan

1. **Keamanan & Praktik Terbaik**: `wifi_prov_fsm.ino` tidak memuat kredensial Wi-Fi *hardcoded*, menyimpan konfigurasi di NVS `Preferences`, meredaksi password di log Serial, dan menghindari *blocking reconnect loop*.
2. **Validasi Simulasi**: `wifi_fsm_sim.py` mengonfirmasi urutan *exponential backoff* ($1\text{ s} \dots 60\text{ s}$) dan reset backoff saat `CONNECTED`.
3. **Catatan**: Akan dikompilasi menggunakan `arduino-cli` setelah instalasi core `esp32:esp32` selesai.


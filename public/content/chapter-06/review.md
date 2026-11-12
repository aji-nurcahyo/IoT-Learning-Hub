# Laporan Review — Chapter 06

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-10
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi firmware `.ino`, disertai bukti **Software (`debounce_sim.py`)**.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Lengkap mencakup logika digital, `INPUT_PULLUP/PULLDOWN`, batasan `GPIO 34–39` ESP32, fisika *switch bounce*, *software* vs *hardware debounce*, *edge detection*, *polling* vs *interrupt* (`IRAM_ATTR`, `volatile`), dan FSM pengendali LED.
2. **Validasi Simulasi**: `debounce_sim.py` membuktikan secara numerik pada `telemetry.csv` bahwa *naive edge-detect* memicu 6 event palsu sedangkan *software debounce* 50 ms mendeteksi tepat 2 penekanan valid.
3. **Kejujuran Status**: Kode `.ino` dan skema Wokwi tidak diklaim *compile-verified* atau *simulator-verified* karena tool tersebut tidak terpasang di lingkungan server.


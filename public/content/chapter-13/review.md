# Laporan Review — Chapter 13

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino` ESP32, disertai bukti **Software Loopback (`http_rest_sim.py`)** yang menjalankan server & klien HTTP nyata di Python 3.12.10.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Lengkap membahas metode REST, anatomi request/response, kebijakan retry `2xx/4xx/5xx`, serialisasi JSON hemat heap, `HTTPClient` (`setTimeout`, `end()`), dan TLS/HTTPS.
2. **Validasi Loopback**: `http_rest_sim.py` menguji transaksi HTTP/1.1 nyata untuk kasus `503 -> retry -> 201`, `400 -> no retry`, dan `GET -> 200`.
3. **Catatan**: Firmware `http_rest_client.ino` akan dikompilasi setelah core `esp32:esp32` selesai terpasang.


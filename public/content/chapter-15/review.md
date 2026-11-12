# Laporan Review — Chapter 15

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino` ESP32, disertai bukti **Software (`mqtt_qos_lwt_sim.py`)**.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Lengkap membahas QoS 0/1/2, deduplikasi `seq`, *retained messages* (termasuk peringatan terhadap *command topic*), LWT, *keepalive* ($1{,}5\times$), *sessions*, dan MQTT 3.1.1 vs 5.0.
2. **Akurasi Teknis Library**: Secara eksplisit menjelaskan perbedaan kemampuan `PubSubClient` (publish QoS 0, subscribe QoS 0/1, LWT) vs `esp-mqtt` (QoS 0/1/2 penuh & MQTT 5.0).
3. **Validasi Simulasi**: `mqtt_qos_lwt_sim.py` membuktikan penyaringan duplikat `seq=11` dan transisi LWT pada $46\text{ s} > 45\text{ s}$ (`outputs.md`).


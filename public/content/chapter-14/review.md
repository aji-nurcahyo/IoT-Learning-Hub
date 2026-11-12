# Laporan Review — Chapter 14

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino` ESP32 dan Mosquitto eksternal, disertai bukti **Software Loopback (`mqtt_broker_sim.py`)**.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Lengkap membahas arsitektur Pub/Sub, topic hierarchy, wildcard `+` & `#`, payload JSON, keamanan Mosquitto, dan `PubSubClient` (`clientId` unik, `setBufferSize`, `mqtt.loop()`).
2. **Validasi Loopback**: `mqtt_broker_sim.py` mengirim paket biner MQTT 3.1.1 nyata (`CONNECT`, `SUBSCRIBE`, `PUBLISH`) di soket TCP `127.0.0.1` dan lulus tanpa error.
3. **Catatan**: Firmware `mqtt_pubsub_client.ino` memerlukan instalasi library `PubSubClient` sebelum kompilasi `arduino-cli`.


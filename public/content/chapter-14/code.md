# Source Code — Chapter 14: MQTT Publish/Subscribe Client & Loopback Broker

Folder `src/` berisi:

1. [mqtt_pubsub_client.ino](content/chapter-14/src/mqtt_pubsub_client/mqtt_pubsub_client.ino): Firmware klien MQTT ESP32 menggunakan `PubSubClient` + `Preferences.h` (tanpa password *hardcoded*), mempublikasikan *telemetry* JSON ke `lab/gh01/node-01/telemetry` dan *subscribe* ke `lab/gh01/node-01/cmd/#`.
2. [mqtt_broker_sim.py](content/chapter-14/src/mqtt_broker_sim.py): Pengujian protokol biner MQTT 3.1.1 (`CONNECT`, `CONNACK`, `SUBSCRIBE`, `SUBACK`, `PUBLISH`) dan pencocokan *wildcard* (`+`, `#`) pada *loopback* `127.0.0.1` menggunakan modul standar `socket` Python.

## Cara Menjalankan

**Simulasi Paket Biner MQTT Loopback (Python):**
```sh
python public/content/chapter-14/src/mqtt_broker_sim.py
```

**Firmware ESP32:**
- Pasang library **`PubSubClient`** (`by Nick O'Leary`) pada Arduino IDE / `arduino-cli lib install PubSubClient`.
- Jalankan **Eclipse Mosquitto** lokal pada jaringan LAN (bukan `127.0.0.1` untuk perangkat fisik) dan masukkan konfigurasi NVS terlebih dahulu.


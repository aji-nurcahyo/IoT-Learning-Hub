# Bukti & Output Eksekusi — Chapter 14

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (uji paket biner MQTT 3.1.1 & pencocokan *wildcard* `+`/`#` di socket loopback `127.0.0.1` pada Python 3.12.10)
- **Tanggal**: 2026-11-11
- **Environment**: Windows, Python 3.12.10 (`socket`, `struct`, `threading`)
- **Perintah**: `python public/content/chapter-14/src/mqtt_broker_sim.py`
- **Firmware ESP32 (`mqtt_pubsub_client.ino`) / Mosquitto Fisik**: **Belum diuji** (toolchain `esp32:esp32` masih dalam tahap instalasi; Mosquitto eksternal belum terpasang di server ini)

## 2. Output Aktual (Verbatim — Software MQTT Loopback)

```text
=== UJI WILDCARD & MINI-BROKER MQTT 3.1.1 LOOPBACK (CHAPTER 14) ===
[PASS] Aturan wildcard '+' dan '#' terverifikasi.
[PASS] MQTT Loopback RX topic='lab/gh01/node-01/telemetry' payload={"device_id": "esp32-gh01-node01", "seq": 1, "temp_c": 28.75, "source": "synthetic"}
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `mqtt_pubsub_client`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-14/src/mqtt_pubsub_client
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 899880 bytes (68%) of program storage space. Maximum is 1310720 bytes.
Global variables use 47264 bytes (14%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

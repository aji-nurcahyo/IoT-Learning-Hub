# Bukti & Output Eksekusi — Chapter 13

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (eksekusi nyata HTTP server & client *loopback* `127.0.0.1` pada Python 3.12.10)
- **Tanggal**: 2026-11-11
- **Environment**: Windows, Python 3.12.10 (`http.server` + `urllib.request`)
- **Perintah**: `python public/content/chapter-13/src/http_rest_sim.py`
- **Firmware ESP32 (`http_rest_client.ino`)**: **Belum diuji** (toolchain `esp32:esp32` masih dalam tahap instalasi; pengujian fisik WLAN belum dilakukan)

## 2. Output Aktual (Verbatim — Software Loopback HTTP Verification)

```text
=== SIMULASI HTTP REST API & JSON CLIENT (LOOPBACK NYATA, CHAPTER 13) ===
1. POST valid saat server 503 sementara -> harus retry dan berhasil 201:
    attempt 1: HTTP 503 -> {'error': 'service_temporarily_unavailable'}
   HASIL AKHIR: HTTP 201 {'accepted': True, 'seq': 1}

2. POST tanpa 'temp_c' -> harus langsung 400 Bad Request tanpa retry:
    attempt 1: HTTP 400 -> {'error': 'missing_required_fields'}
   HASIL AKHIR: HTTP 400 {'error': 'missing_required_fields'}

3. GET /api/v1/devices/esp32-node-01/config:
   HASIL AKHIR: HTTP 200 {'device_id': 'esp32-node-01', 'sample_ms': 5000, 't_high_c': 30.0}
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `http_rest_client`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-13/src/http_rest_client
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 1019952 bytes (77%) of program storage space. Maximum is 1310720 bytes.
Global variables use 49016 bytes (14%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

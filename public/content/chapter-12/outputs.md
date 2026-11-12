# Bukti & Output Eksekusi — Chapter 12

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi *state machine* *device provisioning* NVS & *exponential backoff* di Python)
- **Tanggal**: 2026-11-11
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-12/src/wifi_fsm_sim.py`
- **Firmware ESP32 (`wifi_prov_fsm.ino`)**: **Belum diuji** (toolchain `esp32:esp32` masih dalam tahap instalasi; simulator Wokwi dan router fisik tidak dijalankan di server ini)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== SIMULASI WI-FI PROVISIONING & BACKOFF FSM (CHAPTER 12) ===
[BOOT ] NVS kosong -> state=PROVISIONING
[PROV ] Disimpan ke NVS: ssid=Lab-IoT-24G, pass=REDACTED
[RETRY #1] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 1000 ms
[RETRY #2] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 2000 ms
[RETRY #3] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 4000 ms
[RETRY #4] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 8000 ms
[RETRY #5] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 16000 ms
[RETRY #6] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 32000 ms
[RETRY #7] state=CONNECTING -> timeout 10000 ms -> BACKOFF_WAIT 60000 ms
[CONN ] state=CONNECTED, IP=192.168.10.42, RSSI=-58 dBm, backoff_reset=1000 ms
```

## 3. Expected Serial Monitor Output (Teoretis untuk `wifi_prov_fsm.ino` — Belum Dieksekusi)

```text
=== CHAPTER 12: WI-FI STA + NVS PROVISIONING + BACKOFF ===
[PROV] Belum ada kredensial di NVS. Kirim: PROV:<ssid>,<password>
[PROV] Kredensial disimpan ke NVS (SSID=Wokwi-GUEST, pass=REDACTED).
[WIFI] Menghubungkan ke SSID 'Wokwi-GUEST' (timeout=10000 ms)...
[WIFI] CONNECTED | IP=10.10.0.2 | GW=10.10.0.1 | RSSI=-40 dBm
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `wifi_prov_fsm`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-12/src/wifi_prov_fsm
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 884288 bytes (67%) of program storage space. Maximum is 1310720 bytes.
Global variables use 45920 bytes (14%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

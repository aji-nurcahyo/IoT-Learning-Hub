# Source Code — Chapter 20: Connected Device Capstone

## Daftar Berkas

1. [`connected_env_capstone.ino`](src/connected_env_capstone/connected_env_capstone.ino) & [`config.h`](src/connected_env_capstone/config.h) — Firmware ESP32 lengkap (*Connected Environmental Monitoring System*) yang mengintegrasikan:
   - Penyimpanan parameter persisten di **NVS (`Preferences`)** sebagai fallback offline
   - Akuisisi analog pada **`GPIO34` (ADC1)** serta kontrol histeresis kipas lokal pada **`GPIO26`** (*fail-safe* tetap berjalan saat Wi-Fi/Broker mati)
   - *Wi-Fi STA FSM* + **Full-Jitter Exponential Backoff** (`esp_random()`)
   - Sinkronisasi konfigurasi awal melalui **HTTP `GET`** (`HTTPClient` timeout `2500 ms` + *fallback* NVS)
   - Sinkronisasi waktu UTC via **SNTP** (`configTime`) + *Static Ring Buffer* 32 slot + *Batch Drain* non-blocking (`4` item/tick)
   - Komunikasi **MQTT (`PubSubClient`)**: JSON *telemetry*, *Retained status* + **LWT `"offline"`**, serta *command subscriber* (`iot/lab/node-01/cmd`).
2. [`wokwi_diagram.json`](src/wokwi_diagram.json) — Skema rangkaian simulator Wokwi (`board-esp32-devkit-v1`, sensor analog `GPIO34`, LED status `GPIO2`, LED/aktuator kipas `GPIO26`, tombol `GPIO27`).
3. [`capstone_connectivity_test.py`](src/capstone_connectivity_test.py) — Harness uji penerimaan lokal (*simulator-first + local broker*, tanpa ketergantungan cloud berbayar) menjalankan server HTTP lokal + broker MQTT 3.1.1 TCP lokal serta 6 kasus uji penerimaan (`TC-01` s.d. `TC-06`).
4. [`telemetry.csv`](telemetry.csv) — Jejak sampel multi-fase (*live $\rightarrow$ offline buffering + histeresis lokal $\rightarrow$ replay $\rightarrow$ pembaruan ambang remote*).

## Cara Menjalankan Uji Lokal

```bash
python public/content/chapter-20/src/capstone_connectivity_test.py
```

Sketsa [`connected_env_capstone.ino`](src/connected_env_capstone/connected_env_capstone.ino) membutuhkan pustaka `PubSubClient` dan dikompilasi untuk target `esp32:esp32:esp32`.


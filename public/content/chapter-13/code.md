# Source Code — Chapter 13: HTTP REST Client, JSON & Loopback Test

Folder `src/` berisi:

1. [http_rest_client.ino](content/chapter-13/src/http_rest_client/http_rest_client.ino): Firmware klien REST HTTP pada ESP32 memakai `HTTPClient.h`, `Preferences.h`, timeout eksplisit $3000\text{ ms}$, serialisasi JSON via `snprintf()`, dan kebijakan *retry* yang hanya mengulang pada `5xx`/timeout (tidak pada `4xx`).
2. [http_rest_sim.py](content/chapter-13/src/http_rest_sim.py): Pengujian HTTP *loopback* nyata di Python (`http.server` + `urllib.request`) memvalidasi `201 Created`, `400 Bad Request` tanpa retry, `503 -> retry -> 201`, dan `GET` JSON konfigurasi.

## Cara Menjalankan

**Simulasi Loopback HTTP Nyata (Python):**
```sh
python public/content/chapter-13/src/http_rest_sim.py
```

**Firmware ESP32:**
- Gunakan target `esp32:esp32:esp32`. Pastikan endpoint server lokal menggunakan IP LAN mesin server (bukan `127.0.0.1` dari sisi ESP32).


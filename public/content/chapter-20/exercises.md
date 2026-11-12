# Exercises — Chapter 20: Connected Device Capstone

## A. Pertanyaan Desain & Arsitektur

1. Mengapa pada [`connected_env_capstone.ino`](content/chapter-20/src/connected_env_capstone/connected_env_capstone.ino), pembaruan kontrol kipas `updateLocalHysteresis(tempC)` dijalankan **sebelum** pengecekan `WiFi.status() != WL_CONNECTED`?
2. Jelaskan fungsi masing-masing tiga topik MQTT berikut dan mengapa hanya `status` yang menggunakan flag **Retained + LWT**:
   - `iot/lab/node-01/status`
   - `iot/lab/node-01/telemetry`
   - `iot/lab/node-01/cmd`
3. Jika sebuah papan ESP32 membaca sensor suhu pada **`GPIO14` (ADC2)** sementara Wi-Fi STA sedang aktif, gejala apa yang muncul dan bagaimana cara memperbaikinya?

## B. Analisis Kegagalan & Rekayasa Protokol (`capstone_connectivity_test.py`)

4. Jalankan [`capstone_connectivity_test.py`](content/chapter-20/src/capstone_connectivity_test.py) dan amati hasil `TC-01` s.d. `TC-06`. Sekarang modifikasi fungsi `run_acceptance_suite()` untuk menyimulasikan skenario tambahan:
   - a) **HTTP Server Down Saat Boot (`TC-01 Fallback`)**: Pastikan jika HTTP `GET` gagal/timeout, node tetap memakai `temp_high_c = 30.0` dari konfigurasi NVS awal tanpa menghentikan akuisisi.
   - b) **Luapan Ring Buffer**: Kecilkan kapasitas `ring` menjadi `deque(maxlen=3)` lalu masukkan `5` sampel saat *offline*; verifikasi bahwa `2` sampel paling lama tergeser dan hitung `dropped_oldest = 2`.
5. Pada [`connected_env_capstone.ino`](content/chapter-20/src/connected_env_capstone/connected_env_capstone.ino), tambahkan fitur pada tombol `PIN_REPROV_BTN` (`GPIO27`) agar ketika ditekan lebih dari `1500 ms` (memakai FSM *debounce* non-blocking!), node mereset flag `httpConfigFetched = false` sehingga langsung menarik ulang konfigurasi HTTP tanpa perlu *restart* ESP32.

## C. Evaluasi Kontrak JSON & Ukuran Paket

6. Hitung panjang byte aktual JSON telemetri di bawah ini dan jelaskan apa yang terjadi di `PubSubClient` apabila Anda lupa memanggil `mqtt.setBufferSize(512)` sementara ukuran paket melebihi `256 byte`:

```json
{"dev":"node-01","seq":1024,"ts":1762822800,"synced":true,"temp":30.80,"th":30.00,"relay":true,"q":4,"drop":0}
```

## Expected Output Acuan

Menjalankan [`capstone_connectivity_test.py`](content/chapter-20/src/capstone_connectivity_test.py) tanpa modifikasi harus mengeluarkan semua 6 baris `[PASS]` persis seperti tercatat di [`outputs.md`](content/chapter-20/outputs.md) dengan exit code `0`.


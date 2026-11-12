# Tugas & Rubrik — Chapter 13

## Skenario Tugas: Kontrak REST API Telemetry & Klien HTTP Tahan Error

Rancang dan ujilah sebuah layanan *REST endpoint* lokal (berbasis Python `http.server` atau framework lokal tanpa cloud berbayar) beserta klien `HTTPClient` ESP32 untuk menerima *telemetry* suhu/kelembaban dan menyediakan konfigurasi perangkat.

## Persyaratan Teknis

1. **Kontrak API & JSON**: Definisikan `POST /api/v1/telemetry` dan `GET /api/v1/devices/{id}/config` lengkap dengan header `Content-Type: application/json`, token otentikasi header, serta satuan eksplisit pada setiap field JSON.
2. **Kebijakan Status Code & Retry**: Implementasikan respons `201`, `400`, `401`, dan `503` pada server uji, lalu buktikan klien hanya me-retry `503`/timeout (tidak me-retry `400`/`401`).
3. **Kode ESP32**: Lengkapi [`http_rest_client.ino`](content/chapter-13/src/http_rest_client/http_rest_client.ino) dengan `setTimeout()`, `http.end()`, serialisasi statis `snprintf()`, dan tanpa password/token hardcoded.
4. **Evaluasi TLS & Bukti Uji**: Sertakan analisis singkat cara mengamankan API tersebut dengan TLS/HTTPS (`setCACert` + NTP) serta lampirkan log asli eksekusi server-klien lokal.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Desain kontrak REST API & skema JSON** | **25** | Endpoint semantik (`GET/POST`), header lengkap, validasi skema, dan satuan fisik eksplisit. |
| **Penanganan status code, timeout & retry** | **30** | Membedakan `2xx`, `4xx` (tanpa retry), dan `5xx`/timeout (retry terbatas) serta memanggil `http.end()`. |
| **Implementasi client & server uji lokal** | **25** | Server & klien lokal Python berjalan nyata; kode ESP32 rapi tanpa kredensial hardcoded. |
| **Analisis TLS/HTTPS & kejujuran bukti** | **20** | Penjelasan Root CA vs `setInsecure()` akurat serta pelaporan status verifikasi jujur. |


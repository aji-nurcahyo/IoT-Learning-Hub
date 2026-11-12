# Latihan Bertingkat — Chapter 13

## Bagian A — Pertanyaan Konseptual & Analisis Protokol

1. Jelaskan perbedaan antara metode **`GET`**, **`POST`**, **`PUT`**, dan **`DELETE`** pada REST API IoT. Mengapa `POST /api/v1/telemetry` sebaiknya tidak otomatis diulang tanpa pengaman apabila balasan `201` hilang karena putus di tengah jalan?
2. Kelompokkan kode status berikut menjadi **"Hapus dari antrean"**, **"Jangan retry (error client)"**, atau **"Retry terbatas dengan backoff"**: `201`, `400`, `401`, `404`, `429`, `503`, dan `-11 (HTTPC_ERROR_READ_TIMEOUT)`.
3. Mengapa penggunaan `WiFiClientSecure::setInsecure()` berbahaya pada perangkat IoT yang mengirim data lewat jaringan publik, dan komponen apa yang dibutuhkan ESP32 agar verifikasi sertifikat CA berhasil?

## Bagian B — Analisis Efisiensi & Debugging

4. Hitung total *wire overhead* satu kali pengiriman REST `POST` berisi payload JSON `{"temp_c":28.5}` ($15\text{ byte}$) jika *HTTP Request Header* berukuran $190\text{ byte}$ dan respons server berukuran $110\text{ byte}$ (belum termasuk header TCP/IP). Berapa persen porsi data sensor murninya?
5. Temukan **dua bug kritis** pada potongan kode klien ESP32 berikut:
   ```cpp
   void sendData(String url, String json) {
     HTTPClient http;
     http.begin(url);
     int code = http.POST(json);
     if (code != 200) {
       http.POST(json);
     }
   }
   ```

## Bagian C — Pengujian Loopback HTTP & Mini Challenge

6. **Menjalankan Simulasi Server & Client Nyata (`http_rest_sim.py`)**:
   ```sh
   python public/content/chapter-13/src/http_rest_sim.py
   ```
   **Mini Challenge**:
   - Pada salinan lokal `http_rest_sim.py`, tambahkan validasi header **`Authorization: Bearer demo-token-01`** pada endpoint `POST /api/v1/telemetry`. Jika token tidak cocok atau hilang, server wajib membalas **`401 Unauthorized`**, dan pastikan fungsi klien menghentikan *retry* secara otomatis saat menerima `401`.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **REST Methods & Idempotensi**: `GET` membaca, `POST` membuat entri baru, `PUT` mengganti/memperbarui *resource* tertentu, `DELETE` menghapus. Jika balasan `201` dari `POST` hilang di jaringan lalu klien mengulang `POST` yang sama tanpa kunci idempoten (`device_id + seq`), data tercatat ganda (*duplicate*) di database.
2. **Klasifikasi Status Code**: `201` = Hapus dari antrean; `400, 401, 404` = Jangan retry (perbaiki payload/kredensial/URL); `429, 503, -11` = Retry terbatas dengan *backoff*.
3. **`setInsecure()` & TLS**: `setInsecure()` menerima sertifikat apa pun termasuk sertifikat palsu penyerang MITM. Untuk verifikasi yang benar, ESP32 membutuhkan **Root CA Certificate** (PEM) dan waktu jam sistem yang valid (via NTP).
4. **Efisiensi Header HTTP**: Total data aplikasi bolak-balik = $15 + 190 + 110 = 315\text{ byte}$; data sensor murni hanya $15 / 315 \approx 4{,}76\%$! Ini alasan pengiriman frekuensi tinggi beralih ke batching atau MQTT.
5. **Bug Kode ESP32**: (1) Tidak ada `http.setTimeout(...)`; (2) Tidak ada `http.addHeader("Content-Type", "application/json")`; (3) Lupa memanggil `http.end()` (*memory/socket leak*); (4) Melakukan *retry* membabi-buta pada semua `code != 200` (termasuk `201 Created` dan `4xx`!).

</details>


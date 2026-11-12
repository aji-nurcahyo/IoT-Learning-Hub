# Latihan Bertingkat — Chapter 14

## Bagian A — Pertanyaan Konseptual & Topic Wildcards

1. Jelaskan tiga bentuk *decoupling* (*space*, *time*, *synchronization*) pada arsitektur **Publish/Subscribe** MQTT dibandingkan model *Request–Response* HTTP.
2. Evaluasi apakah filter subscribe berikut **VALID** dan **COCOK** dengan topic publikasi **`kampus/itera/gedung-e/ruang201/temp_c`**:
   - (a) `kampus/itera/+/ruang201/temp_c`
   - (b) `kampus/itera/+/temp_c`
   - (c) `kampus/itera/#`
   - (d) `kampus/#/temp_c`
3. Mengapa **dilarang** melakukan `mqtt.publish("lab/+/temp_c", "28.5")` dan mengapa `subscribe("#")` sebaiknya dihindari pada sistem produksi?

## Bagian B — Analisis Kode & Konfigurasi Mosquitto

4. Seorang mahasiswa menjalankan `mosquitto` di laptopnya (`IP LAN = 192.168.1.20`) dengan konfigurasi default bawaan lalu mengunggah *Firmware* ESP32 berisi `mqtt.setServer("192.168.1.20", 1883);`, tetapi selalu mendapat error `rc=-2`. Apa dua hal paling umum yang menyebabkan Mosquitto menolak koneksi dari ESP32 di LAN pada versi Mosquitto 2.x?
5. Sebuah node mengirim payload JSON sepanjang `245 byte` ke topic `kampus/itera/lab-iot/telemetry/sensor-lingkungan-01` (`54 byte`). Jika memakai `PubSubClient` tanpa mengubah `setBufferSize()`, mengapa `mqtt.publish()` gagal?

## Bagian C — Pengujian Loopback & Mini Challenge

6. **Menjalankan Uji Paket MQTT Loopback (`mqtt_broker_sim.py`)**:
   ```sh
   python public/content/chapter-14/src/mqtt_broker_sim.py
   ```
   **Mini Challenge**:
   - Pada salinan lokal `mqtt_broker_sim.py`, tambahkan **Subscriber ke-2** yang berlangganan `lab/gh01/+/cmd` dan uji pengiriman dua pesan berbeda (`lab/gh01/node-01/telemetry` dan `lab/gh01/node-01/cmd`), lalu buktikan masing-masing subscriber hanya menerima topic yang sesuai filternya!

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Decoupling**: *Space* (pengirim dan penerima tidak saling tahu IP), *Time* (tidak harus aktif bersamaan bila memakai persistent session/retained), *Synchronization* (callback asinkron tanpa memblokir).
2. **Evaluasi Wildcard** terhadap `kampus/itera/gedung-e/ruang201/temp_c` (5 level):
   - (a) Valid dan **COCOK** (`+` menggantikan `gedung-e`).
   - (b) Valid tetapi **TIDAK COCOK** (hanya 4 level).
   - (c) Valid dan **COCOK** (`#` menangkap seluruh level sisa).
   - (d) **TIDAK VALID** menurut spesifikasi MQTT karena `#` berada di tengah, bukan level terakhir!
3. **Larangan Publish Wildcard & `#` Global**: Spesifikasi MQTT melarang wildcard pada topic `PUBLISH` (karena alamat tujuan harus spesifik); `subscribe("#")` menerima seluruh trafik broker termasuk beban tak terduga dan topik sistem jika diizinkan.
4. **Mosquitto 2.x `rc=-2`**: Sejak Mosquitto 2.0, konfigurasi default hanya mendengarkan `127.0.0.1` (loopback) dan menolak klien eksternal sebelum dikonfigurasi `listener 1883` + autentikasi (`password_file`), serta firewall OS Windows/Linux sering memblokir port masuk `1883`.
5. **Buffer `PubSubClient`**: Total `54 + 245 + header` melampaui kapasitas default `256 byte` `PubSubClient`, sehingga perlu memanggil `mqtt.setBufferSize(512)`.

</details>


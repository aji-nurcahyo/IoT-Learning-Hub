# Latihan Bertingkat — Chapter 15

## Bagian A — Pertanyaan Konseptual & Jaminan QoS

1. Jelaskan mekanisme pertukaran paket pada **QoS 0**, **QoS 1**, dan **QoS 2**. Jika sebuah sensor mengirim **500 pesan** melalui koneksi yang membutuhkan 1x pengiriman ulang pada 10% pesan di QoS 1, bandingkan total paket tingkat aplikasi antara QoS 0 dan QoS 1.
2. Sebuah Publisher mengirim pesan ke topic `lab/suhu` dengan **QoS 2**, sedangkan Subscriber A berlangganan `lab/suhu` dengan **QoS 0** dan Subscriber B dengan **QoS 1**. Pada tingkat QoS berapa masing-masing Subscriber menerima pesan dari Broker?
3. Jelaskan perbedaan antara **Clean Session (`true`)** dan **Persistent Session (`false`)** pada MQTT 3.1.1, serta mengapa **MQTT 5.0** memperkenalkan **`Session Expiry Interval`**.

## Bagian B — Analisis Kasus Retained, LWT & Idempotensi

4. **Analisis Insiden Retained Command**:
   Sebuah sistem irigasi memakai topic `kebun/blok1/cmd/katup` untuk mengirim perintah `"BUKA"` selama 30 detik. Seorang developer tidak sengaja mengaktifkan `retain = true` saat mem-publish `"BUKA"`. Apa yang terjadi ketika node ESP32 di kebun mengalami reset listrik di malam hari lalu kembali menyambung ke Broker? Bagaimana cara menghapus pesan *retained* yang telanjur tersimpan di Broker?
5. **Perhitungan Waktu LWT**:
   Sebuah node dikonfigurasi dengan `keepalive = 40 detik`. Node mengalami putus daya mendadak pada $t = 120\text{ s}$ tepat $5\text{ detik}$ setelah terakhir mengirim paket `PUBLISH`. Pada detik ke berapa paling lambat Broker akan menerbitkan pesan *Last Will* node tersebut?

## Bagian C — Simulasi Software & Mini Challenge

6. **Menjalankan Simulasi (`mqtt_qos_lwt_sim.py`)**:
   ```sh
   python public/content/chapter-15/src/mqtt_qos_lwt_sim.py
   ```
   **Mini Challenge**:
   - Tambahkan mekanisme simulasi **Persistent Session (`cleanSession = false`)** pada salinan lokal `mqtt_qos_lwt_sim.py`: ketika `sub-01` terputus sementara, Broker menampung 3 pesan QoS 1 ke dalam antrean sesi `sub-01`, lalu mengirimkan ketiganya secara berurut begitu `sub-01` kembali `CONNECT` dengan `clientId` yang sama!

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Perhitungan Paket (500 pesan)**: QoS 0 = $500 \times 1 = 500$ paket. QoS 1 = $500 \times 2$ (`PUBLISH` + `PUBACK`) + $50$ retransmisi `PUBLISH` = $1.050$ paket aplikasi.
2. **QoS Efektif Subscriber**: Broker menurunkan QoS ke nilai minimum antara publikasi dan langganan: Subscriber A menerima pada **QoS 0** ($\min(2, 0)$); Subscriber B menerima pada **QoS 1** ($\min(2, 1)$).
3. **Sessions & MQTT 5.0**: Pada `cleanSession=false` di MQTT 3.1.1, Broker menyimpan antrean sesi selamanya tanpa batas waktu sehingga memori Broker bisa penuh oleh node yang sudah rusak permanen. MQTT 5.0 menambahkan `Session Expiry Interval` agar sesi otomatis dibersihkan setelah durasi tertentu.
4. **Insiden Retained & Cara Hapus**: Saat ESP32 reboot dan men-subscribe `kebun/blok1/cmd/katup`, Broker langsung mengirim pesan retained `"BUKA"` sehingga katup terbuka sendiri di malam hari! Hapus pesan retained dengan mengirim payload kosong `""` dengan `retain=true` ke topic yang sama.
5. **Waktu LWT**: Terakhir ada aktivitas pada $t = 120 - 5 = 115\text{ s}$. Menurut spesifikasi MQTT, Broker memutus klien jika senyap melebihi $1{,}5 \times \text{keepalive} = 1{,}5 \times 40 = 60\text{ detik}$, sehingga LWT terpicu sekitar $t = 115 + 60 = 175\text{ s}$.

</details>


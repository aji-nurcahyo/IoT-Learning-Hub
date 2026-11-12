# Latihan Bertingkat — Chapter 01

Latihan ini dirancang untuk menguji pemahaman konseptual, analisis aliran data, perhitungan kapasitas dasar, dan praktik simulasi *software* tanpa memerlukan *hardware* fisik.

## Bagian A — Pertanyaan Konseptual

1. Jelaskan dengan kata-kata Anda sendiri perbedaan fungsional antara **Embedded System mandiri**, **Cyber-Physical System (CPS)**, dan **sistem Internet of Things (IoT)**. Berikan masing-masing satu contoh nyata di luar modul.
2. Sebuah kulkas pintar memiliki sensor suhu internal dan layar digital di pintunya untuk mengatur kompresor, tetapi sama sekali tidak memiliki antarmuka jaringan. Apakah perangkat ini termasuk IoT? Jelaskan alasannya berdasarkan aliran data.
3. Mengapa **Gateway** tetap diperlukan pada banyak sistem IoT lapangan meskipun sebagian mikrokontroler modern (seperti ESP32) sudah memiliki radio Wi-Fi terintegrasi? Sebutkan minimal dua fungsi Gateway selain translasi protokol.

## Bagian B — Applied Engineering Problems

4. **Pemetaan Ekosistem Telekomunikasi (BTS Remote Monitoring)**:
   Sebuah menara BTS di daerah terpencil dipasangi sensor suhu kabinet baterai, sensor tegangan baterai DC, dan saklar pintu (*door contact*). Data dikirim melalui modem seluler menuju server NOC (*Network Operations Center*). Jika suhu kabinet melebihi $38\,^\circ\text{C}$, sistem menyalakan kipas cadangan dan mengirim notifikasi ke teknisi.
   - Identifikasi komponen: *Sensor*, *Embedded Node*, *Connectivity*, *Platform/Application*, dan *Actuator*.
   - Tuliskan contoh payload JSON *uplink* yang baik (memuat `device_id`, `seq`, satuan eksplisit, dan status pintu).
   - Jelaskan skenario kegagalan jika koneksi seluler ke NOC putus selama 2 jam—di mana logika penyalaan kipas sebaiknya diletakkan?

5. **Analisis Beban Data & Skala**:
   Sebuah proyek pemantauan kualitas udara kota memasang **120 node** sensor. Setiap node mengirim payload sebesar $B = 160\text{ byte}$ setiap $\Delta t = 30\text{ detik}$.
   - Hitung jumlah paket per hari dari 1 node dan dari 120 node.
   - Hitung total volume *payload* aplikasi per hari (dalam MiB) untuk seluruh jaringan.
   - Jika interval diubah menjadi $\Delta t = 5\text{ detik}$, berapa faktor kenaikan paket dan apa dua risiko teknis yang langsung muncul di sisi *Gateway* dan basis data?

## Bagian C — Simulasi Software & Mini Challenge

6. **Eksperimen Simulasi (`iot_flow_demo.py`)**:
   Jalankan skrip simulasi pada chapter ini:
   ```sh
   python public/content/chapter-01/src/iot_flow_demo.py
   ```
   - Amati mengapa paket dengan `seq=5` ditolak oleh *Gateway*.
   - **Mini Challenge**: Salin skrip ke folder kerja lokal Anda, lalu tambahkan pemeriksaan **rate-of-change** pada fungsi validasi: jika selisih suhu dengan paket valid sebelumnya ($\Delta T$) melebihi $10\,^\circ\text{C}$ dalam satu interval pembacaan, tandai paket sebagai `SUSPECT_SPIKE` alih-alih meneruskannya untuk menyalakan kipas. Uji menggunakan minimal 3 baris data sintetis baru.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

> Gunakan bagian ini **setelah** Anda mencoba menjawab seluruh soal di atas secara mandiri.

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Perbedaan konsep**: *Embedded System* mandiri fokus menjalankan fungsi khusus secara lokal tanpa keharusan terhubung ke jaringan; *CPS* menekankan interaksi kendali tertutup (*closed-loop*) yang ketat antara komputasi dan proses fisik; *IoT* menekankan konektivitas jaringan berstandar terbuka untuk mengirim *telemetry*, menyimpan/menganalisis data pada platform, dan mengintegrasikan banyak layanan.
2. **Kulkas tanpa jaringan**: Bukan sistem IoT, melainkan *Embedded System* (dan sistem kendali suhu lokal) karena tidak ada pertukaran data melalui jaringan ke platform/layanan eksternal.
3. **Fungsi Gateway**: Selain translasi protokol (misal BLE/LoRa $\rightarrow$ IP/MQTT), Gateway berfungsi untuk *local buffering* saat internet putus, agregasi/kompresi data, validasi skema awal, dan terminasi keamanan (TLS/kredensial) terpusat.
4. **BTS Remote Monitoring**:
   - *Sensor*: sensor suhu, pembagi/sensor tegangan baterai, saklar pintu. *Embedded Node*: mikrokontroler pengendali node. *Connectivity*: jaringan seluler (4G/NB-IoT) + modem/gateway. *Platform*: broker & server NOC. *Actuator*: kipas kabinet DC.
   - *Contoh payload*: `{"device_id":"bts-lampung-04","seq":102,"cabinet_temp_c":36.4,"battery_v":48.2,"door_open":false,"source":"synthetic"}`.
   - *Kegagalan koneksi*: Logika penyalaan kipas pada batas darurat ($38\,^\circ\text{C}$) **wajib dijalankan secara lokal** di *Embedded Node* (*fail-safe*), bukan menunggu perintah *downlink* dari NOC.
5. **Perhitungan 120 node ($\Delta t = 30\text{ s}, B = 160\text{ B}$)**:
   - $N_{\text{node}} = 86400 / 30 = 2880\text{ paket/hari}$.
   - $N_{\text{total}} = 120 \times 2880 = 345.600\text{ paket/hari}$.
   - $V_{\text{total}} = 345.600 \times 160 = 55.296.000\text{ byte} \approx 52{,}73\text{ MiB/hari}$.
   - Jika $\Delta t = 5\text{ s}$, jumlah paket naik $6\times$ menjadi $2.073.600\text{ paket/hari}$: risiko lonjakan tumbukan akses radio / antrean *broker* dan pembengkakan I/O serta biaya penyimpanan basis data.

</details>


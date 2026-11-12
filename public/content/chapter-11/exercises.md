# Latihan Bertingkat — Chapter 11

## Bagian A — Pertanyaan Konseptual & Analisis Protokol

1. Jelaskan fungsi masing-masing lapisan pada **TCP/IP 4-Layer Stack** dan tunjukkan di lapisan mana protokol berikut berada: `MQTT`, `IPv4`, `UDP`, `Wi-Fi 802.11`, `DNS`, dan `TCP`.
2. Mengapa sebuah payload kecil berukuran $24\text{ byte}$ lebih hemat *bandwidth* bila dikirim lewat `UDP` dibanding `TCP`? Kapan kita tetap wajib memilih `TCP` meskipun *overhead*-nya lebih besar?
3. Jelaskan mengapa alamat `127.0.0.1` pada komputer dapat dijangkau oleh `mosquitto_pub` di komputer yang sama, tetapi **selalu gagal** ketika ditulis di *Firmware* ESP32 untuk menghubungi broker di komputer tersebut.

## Bagian B — Perhitungan CIDR & Efisiensi Goodput

4. **Subnetting IPv4 CIDR**:
   Diberikan blok jaringan `172.16.20.0/25` untuk menampung node sensor gudang.
   - Tentukan *subnet mask* dalam format desimal bertitik.
   - Tentukan *network address*, *broadcast address*, rentang *usable host IP*, dan jumlah maksimal perangkat yang dapat ditampung.
   - Jika suatu node mendapat konfigurasi statis `172.16.20.140/25` dengan gateway `172.16.20.1`, mengapa node tersebut gagal berkomunikasi?

5. **Analisis Goodput Payload**:
   Hitung efisiensi *goodput* (`payload / total_wire_bytes`) untuk pengiriman via **TCP/IPv4** ($20\text{ B}$ TCP + $20\text{ B}$ IPv4 + $18\text{ B}$ link MAC = $58\text{ B}$ *overhead*) pada dua skenario:
   - (a) Mengirim 1 pembacaan mentah ($B = 25\text{ B}$).
   - (b) Menggabungkan 10 pembacaan menjadi 1 paket *batch* ($B = 250\text{ B}$).

## Bagian C — Simulasi Software & Diagnosis Jaringan

6. **Eksplorasi Skrip (`network_diagnostics_sim.py`)**:
   ```sh
   python public/content/chapter-11/src/network_diagnostics_sim.py
   ```
   **Mini Challenge**: Modifikasi salinan skrip untuk menguji subnet `/27` dan membandingkan efisiensi *goodput* TCP vs UDP untuk ukuran payload $25\text{ B}$, $100\text{ B}$, dan $500\text{ B}$.
7. **Studi Kasus Troubleshooting**:
   ESP32 terhubung ke Wi-Fi dan mendapat IP `192.168.10.23`, sukses `ping 192.168.10.50` (laptop broker), tetapi koneksi TCP ke port `1883` terus mengalami *timeout*. Sebutkan dua penyebab paling mungkin di sisi laptop/broker beserta perintah pemeriksaannya di Windows/Linux.

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Pemetaan Layer**: Application (`MQTT`, `DNS`), Transport (`TCP`, `UDP`), Internet (`IPv4`), Link/Physical (`Wi-Fi 802.11`).
2. **UDP vs TCP**: UDP hanya menambah header $8\text{ B}$ tanpa *3-way handshake*, sehingga hemat energi dan waktu bangun radio; TCP tetap wajib dipilih saat membutuhkan jaminan pengiriman terurut dan deteksi putus koneksi (seperti sesi MQTT).
3. **`127.0.0.1` (Loopback)**: Alamat loopback selalu menunjuk ke perangkat tempat kode berjalan (ESP32 itu sendiri), bukan PC di LAN.
4. **CIDR `172.16.20.0/25`**:
   - Netmask: `255.255.255.128`.
   - Network: `172.16.20.0`, Broadcast: `172.16.20.127`, Usable: `172.16.20.1 .. 172.16.20.126` (**126 host**).
   - `172.16.20.140` berada di subnet kedua (`172.16.20.128/25`), bukan subnet `0/25` tempat gateway `.1` berada!
5. **Goodput TCP ($58\text{ B}$ overhead)**:
   - (a) $25 / (25 + 58) = 25 / 83 \approx 30{,}1\%$.
   - (b) $250 / (250 + 58) = 250 / 308 \approx 81{,}2\%$ (batching menaikkan efisiensi $>2{,}6\times$).
6. **Timeout Port 1883 padahal Ping OK**: (1) *Firewall* OS memblokir koneksi masuk pada port TCP `1883`; (2) Broker Mosquitto hanya *listening* pada `127.0.0.1` alih-alih `0.0.0.0` atau IP LAN. Periksa di PowerShell dengan `Test-NetConnection 192.168.10.50 -Port 1883`.

</details>


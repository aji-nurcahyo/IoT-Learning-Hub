# Latihan Bertingkat — Chapter 16

## Bagian A — Pertanyaan Konseptual & Pemilihan Bus

1. Jelaskan mengapa **I2C** membutuhkan resistor *pull-up* pada jalur `SDA` dan `SCL`, sedangkan **SPI** tidak membutuhkannya.
2. Pilihlah bus (**UART**, **I2C**, atau **SPI**) yang paling tepat untuk masing-masing perangkat berikut dan jelaskan alasannya:
   - (a) Modul GPS yang mengeluarkan kalimat NMEA teks setiap detik.
   - (b) Penggabungan sensor suhu BME280 + sensor cahaya BH1750 + layar kecil OLED pada satu papan berpin terbatas.
   - (c) Pencatatan log data audio/getaran berkecepatan tinggi ke kartu microSD.
3. Mengapa *common ground* (`GND`) tetap wajib dihubungkan antara ESP32 dan modul sensor UART meskipun hanya ada kabel `TX` dan `RX`?

## Bagian B — Perhitungan Frame, Rise Time & Konflik Bus

4. **Efisiensi UART & Durasi Kirim**:
   Sebuah modul GPS mengirim paket NMEA sepanjang **80 byte** menggunakan **UART `9600 baud`, format `8N1`**.
   - Berapa bit total yang dikirim di kabel untuk 80 byte tersebut?
   - Berapa milidetik waktu transmisi minimum yang diperlukan?
   - Bandingkan dengan durasi transfer 80 byte yang sama melalui **SPI `4 MHz`**.
5. **Evaluasi Pull-Up I2C**:
   Jalur I2C memiliki total kapasitansi parasitik kabel & pin $C_{\text{bus}} = 120\text{ pF}$. Jika dipasang resistor *pull-up* $R_p = 4{,}7\text{ k}\Omega$, hitung perkiraan *rise time* $t_r = 0{,}8473 \cdot R_p \cdot C_{\text{bus}}$. Apakah bus tersebut memenuhi syarat **Fast Mode ($400\text{ kHz}$, maks $t_r \le 300\text{ ns}$)** atau hanya **Standard Mode ($100\text{ kHz}$, maks $t_r \le 1000\text{ ns}$)**?
6. **Alamat 7-Bit vs 8-Bit I2C**:
   Datasheet sensor menuliskan alamat *Write* `0xEC` dan *Read* `0xED` (dalam format 8-bit). Berapa alamat **7-bit** yang harus dimasukkan ke `Wire.beginTransmission(...)` di Arduino?

## Bagian C — Simulasi Software & Mini Challenge

7. **Menjalankan Analyzer (`bus_protocol_sim.py`)**:
   ```sh
   python public/content/chapter-16/src/bus_protocol_sim.py
   ```
   **Mini Challenge**:
   - Tambahkan fungsi pada salinan lokal `bus_protocol_sim.py` yang menerima daftar perangkat SPI dan menghitung sisa pin GPIO aman pada `ESP32-DevKitC V4` setelah dikurangi jalur `VSPI` (`MOSI, MISO, SCLK`), `I2C` (`SDA, SCL`), dan `UART2` (`RX2, TX2`). Berapa perangkat SPI maksimal yang masih bisa diberi pin `CS` terpisah?

---

## Kunci Jawaban & Panduan Evaluasi Mandiri

<details>
<summary>Lihat Ringkasan Pembahasan Bagian A & B</summary>

1. **Pull-Up I2C vs SPI**: I2C memakai driver *open-drain* (hanya menarik ke `LOW`, dilepas mengambang agar banyak master/slave bisa berbagi kabel tanpa *short circuit*), sehingga butuh *pull-up* untuk naik ke `HIGH`. SPI memakai *push-pull* searah per jalur (`MOSI`/`MISO`) dengan *slave* dipilih oleh `CS`.
2. **Pemilihan Bus**: (a) **UART** (modul GPS standar NMEA asinkron); (b) **I2C** (3 perangkat cukup berbagi 2 kabel SDA/SCL); (c) **SPI** (microSD butuh *throughput* tinggi).
3. **Common GND pada UART**: Level logika `TX/RX` diukur relatif terhadap `GND`; tanpa `GND` bersama, tegangan penerima tidak punya acuan $0\text{ V}$.
4. **UART `9600 8N1` vs SPI `4 MHz` (80 byte)**:
   - `8N1` = 10 bit/byte $\implies$ $80 \times 10 = 800\text{ bit}$.
   - Waktu UART = $800 / 9600 \approx 83{,}33\text{ ms}$.
   - Waktu SPI @ $4\text{ MHz}$ = $(80 \times 8) / 4{,}000{,}000 = 160\,\mu\text{s} = 0{,}16\text{ ms}$ ($\sim 520\times$ lebih cepat).
5. **Rise Time I2C ($R_p=4{,}7\text{ k}\Omega, C_{\text{bus}}=120\text{ pF}$)**:
   - $t_r = 0{,}8473 \times 4700 \times 120 \times 10^{-12} \approx 477{,}9\text{ ns}$.
   - Nilai $477{,}9\text{ ns} \le 1000\text{ ns}$ (memenuhi **Standard Mode $100\text{ kHz}$**), tetapi $> 300\text{ ns}$ (belum memenuhi Fast Mode $400\text{ kHz}$; turunkan $R_p$ ke $2{,}2\text{ k}\Omega$).
6. **Alamat 7-bit dari `0xEC` (8-bit)**: Geser kanan 1 bit (`0xEC >> 1`) $\implies$ **`0x76`**.

</details>


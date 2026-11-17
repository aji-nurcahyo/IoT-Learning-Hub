# Latihan Chapter 31: Low-Power Design & Energy Measurement

## Latihan Konseptual

1. **Perbandingan Mode Tidur**:
   Jelaskan perbedaan mendasar antara *Light Sleep* dan *Deep Sleep* pada arsitektur ESP32, khususnya ditinjau dari status memori SRAM internal, status osilator frekuensi tinggi, waktu latensi bangun (*wake-up latency*), dan konsumsi arus statis.

2. **Mekanisme Wake-up EXT0 vs EXT1**:
   Kapan Anda memilih pemicu eksternal `EXT0` dibandingkan `EXT1`? Jelaskan konfigurasi bitmask yang diperlukan jika sebuah perangkat harus bangun saat tombol darurat (GPIO 32) ditekan ATAU sensor getaran (GPIO 33) menghasilkan sinyal logika *High*.

3. **Faktor Derating Baterai**:
   Mengapa dalam perancangan teknik sistem tertanam dilarang menggunakan 100% kapasitas nominal baterai ($C_{nominal}$) dalam rumus estimasi waktu pakai? Sebutkan minimal tiga faktor fisik penyebab degradasi kapasitas efektif tersebut.

## Latihan Praktik & Perhitungan

1. **Kalkulasi Profil Energi Sensor Pertanian**:
   Sebuah node pemantau kelembapan tanah beroperasi dengan siklus berkala sebagai berikut:
   - Waktu bangun, kalibrasi ADC, dan pembacaan sensor ($T_{active1}$): 200 ms dengan arus rata-rata 35 mA.
   - Waktu koneksi Wi-Fi, handshake TLS, dan publikasi MQTT ($T_{active2}$): 1.8 detik dengan arus rata-rata 140 mA.
   - Mode Deep Sleep ($T_{sleep}$): 898 detik (total periode 15 menit). Arus bocor total rangkaian saat tidur adalah 12 $\mu$A.
   
   *Instruksi*:
   - Hitung total muatan yang dikonsumsi per siklus ($Q_{cycle}$) dalam satuan mA·s.
   - Hitung arus rata-rata sistem ($I_{avg}$) dalam mA.
   - Jika ditenagai baterai Li-SOCl2 berkapasitas 2600 mAh dengan faktor derating 0.85, perkirakan usia operasional perangkat dalam hari dan tahun.

2. **Implementasi Peripheral Power Gating**:
   Tuliskan potongan kode fungsi inisialisasi dan pemutusan daya ESP32 yang mengendalikan MOSFET switch pada GPIO 25 untuk menyalakan sensor I2C hanya saat dibutuhkan, lengkap dengan penundaan stabilisasi (*settling time*) sebesar 10 ms sebelum komunikasi bus I2C dimulai.

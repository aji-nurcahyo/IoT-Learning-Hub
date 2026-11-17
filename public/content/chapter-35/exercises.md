# Latihan Chapter 35: Edge AI, TinyML & Sensor Inference

## Latihan Konseptual

1. **Perbandingan Arsitektur AI: Cloud vs Edge**:
   Bandingkan eksekusi inferensi machine learning di server cloud terpusat dengan inferensi TinyML langsung pada node sensor mikrokontroler. Bahas berdasarkan 4 metrik rekayasa: latensi respon inferensi, konsumsi bandwidth jaringan, kerentanan kebocoran data privasi, dan ketahanan sistem saat koneksi nirkabel terputus (*offline resilience*).

2. **Dinamika Kuantisasi INT8**:
   Jelaskan bagaimana proses *Post-Training Quantization* memetakan bobot model deep learning dari domain *floating-point* 32-bit (`float32`) ke dalam format bilangan bulat *signed 8-bit* (`int8`). Mengapa operasi perkalian integer pada prosesor mikrokontroler jauh lebih efisien dibandingkan emulasi floating-point berbasis perangkat lunak?

3. **Peran Ekstraksi Fitur Domain Waktu**:
   Mengapa pada mikrokontroler dengan keterbatasan memori RAM (misalnya 64 KB SRAM), kita lebih memilih menyaring sinyal getaran sensor mentah (*raw waveform*) menggunakan fitur statistik domain waktu (RMS, Peak-to-Peak, Zero Crossing Rate) daripada memasukkan seluruh deret waktu 1000 titik sampel secara langsung ke dalam model neural network?

## Latihan Praktik & Perhitungan

1. **Kalkulasi Kuantisasi Fitur Sensor**:
   Diberikan skema kuantisasi untuk input fitur Peak-to-Peak:
   - Skala ($S$) = $0.05$
   - Titik Nol (*Zero Point* / $Z$) = $0$
   - Rentang nilai yang diizinkan: $-128 \le q \le 127$
   
   *Instruksi*:
   - Jika sinyal sensor mengukur lonjakan impak mekanis sebesar $P2P = 5.90\text{ g}$, hitung nilai integer terkuantisasi $q_{p2p}$.
   - Jika sinyal getaran normal hanya menghasilkan $P2P = 0.55\text{ g}$, hitung nilai $q_{norm}$.
   - Tunjukkan bagaimana perbedaan magnitude ini menghasilkan skor klasifikasi yang kontras saat dikalikan dengan bobot integer model.

2. **Perhitungan Penghematan Energi Inferensi vs Transmisi**:
   Sebuah mikrokontroler ESP32 memiliki dua opsi penanganan data getaran motor:
   - **Opsi A (Cloud AI)**: Menyalakan Wi-Fi selama 1.5 detik (arus rata-rata 120 mA pada tegangan 3.3V) untuk mengunggah 1000 sampel data mentah ke cloud broker.
   - **Opsi B (Edge AI)**: Mengekstrak fitur dan menjalankan model inferensi TinyML lokal selama 10 ms (arus 40 mA pada 3.3V), lalu menyalakan radio selama 50 ms (120 mA pada 3.3V) hanya untuk mengirimkan 2 byte kode status anomali.
   
   *Instruksi*:
   - Hitung total energi yang dikonsumsi (dalam miliJoule / mJ) untuk Opsi A dan Opsi B.
   - Berapa persentase penghematan energi yang dicapai oleh pendekatan Edge AI?

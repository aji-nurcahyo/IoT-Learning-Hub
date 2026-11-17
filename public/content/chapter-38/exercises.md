# Latihan Chapter 38: IoT Testing, Fault Injection & Reliability

## Latihan Konseptual

1. **Perbandingan Paradigma Pengujian Pasif vs Aktif**:
   Jelaskan mengapa metode pengujian fungsional pasif (hanya menguji jalur skenario bahagia / *happy path*) tidak mencukupi untuk memvalidasi perangkat IoT industri. Mengapa teknik *Chaos Engineering* dan *Fault Injection* (penyuntikan gangguan) wajib diterapkan sebelum produk dikirim ke lapangan?

2. **Dinamika Fenomena Brownout Tegangan**:
   Mengapa mikrokontroler yang mengalami kondisi *brownout* (misal tegangan catu daya berfluktuasi antara 2.0V–2.4V) berisiko mengalami korupsi data pada memori flash SPI internal? Jelaskan cara kerja sirkuit *Brownout Detector* (BOD) internal ESP32 dalam melindungi sistem dari kondisi membeku (*freeze*).

3. **Komparasi Strategi Penanganan Luapan Buffer**:
   Ketika koneksi internet terputus berhari-hari dan kapasitas memori buffer offline lokal (misalnya cincin memori flash LittleFS) telah penuh, bandingkan kelebihan dan kekurangan dari dua kebijakan penanganan luapan data berikut:
   - Kebijakan *Drop Oldest* (FIFO Overwrite).
   - Kebijakan *Reject Newest* (Menolak data baru dan mempertahankan rekaman lama).

## Latihan Praktik & Perhitungan

1. **Kalkulasi Metrik Keandalan MTBF & Availability**:
   Sebuah kluster gateway pemantau lingkungan beroperasi nonstop selama 2 tahun (17.520 jam). Selama periode tersebut, tercatat 5 kali insiden pemadaman sistem dengan total durasi pemulihan perbaikan selama 20 jam.
   - Hitung nilai *Mean Time Between Failures* (MTBF) dalam satuan jam.
   - Hitung nilai *Mean Time To Repair* (MTTR) dalam satuan jam.
   - Hitung persentase ketersediaan sistem (*Availability*). Apakah sistem memenuhi kualifikasi ketersediaan minimal 99.8%?

2. **Perancangan Kasus Uji Injeksi Gangguan Jaringan**:
   Rancang skenario uji laboratorium terstruktur yang menyuntikkan gangguan *packet loss* 30% dan *latency jitter* 500 ms pada jalur transmisi MQTT perangkat, serta sebutkan parameter toleransi yang membuktikan bahwa klien mampu mengirim ulang paket data tanpa terjadi duplikasi record di database backend.

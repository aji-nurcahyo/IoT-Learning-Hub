# Chapter 38: IoT Testing, Fault Injection & Reliability Engineering

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami piramida pengujian perangkat lunak dan keras IoT (*Unit Testing, Hardware-in-the-Loop Integration, dan End-to-End System Testing*).
2. Menguasai prinsip rekayasa kekacauan (*Chaos Engineering*) dan teknik penyuntikan gangguan terkontrol (**Fault Injection**): *packet drop*, latensi jitter, korupsi payload, dan fluktuasi daya (*brownout*).
3. Mengembangkan mekanisme ketahanan firmware: *Store-and-Forward Offline Buffering*, detektor *Brownout Voltage Reset* (BOD), dan pemulihan status otonom pasca-reboot.
4. Menganalisis metode evaluasi risiko keandalan industri menggunakan *Failure Mode and Effects Analysis* (FMEA) dan penentuan *Risk Priority Number* (RPN).
5. Menghitung indikator keandalan kuantitatif: *Mean Time Between Failures* (MTBF), *Mean Time To Repair* (MTTR), dan *System Availability*.

## Prasyarat

- Pemahaman arsitektur mikrokontroler, memori flash, dan sirkuit catu daya (Chapter 04 & 31).
- Konsep penanganan timeout jaringan dan protokol telemetri MQTT (Chapter 14).
- Dasar-dasar probabilitas dan statistik deskriptif.

## Konsep dan teori

### 1. Filosofi Pengujian Keandalan IoT

Sistem IoT beroperasi di lingkungan fisik yang keras dan tidak dapat diprediksi: petir memicu lonjakan voltase, cuaca ekstrem menyebabkan degradasi sinyal RF, dan baterai melemah memicu kondisi *brownout* (tegangan turun di bawah ambang operasi logika namun tidak mati total).

Pendekatan pengujian pasif ("menunggu sistem gagal di lapangan") terbukti mematikan dan mahal. Rekayasa keandalan modern menerapkan **Fault Injection Testing**: sengaja menyuntikkan kegagalan ekstrem dalam lingkungan laboratorium terkontrol untuk menguji apakah sistem gagal secara anggun (*graceful degradation*) dan pulih secara mandiri (*self-healing*).

```
+-------------------------------------------------------------+
|             Piramida Pengujian Keandalan IoT                |
+-------------------------------------------------------------+
               /      System Acceptance      \
              /       & Chaos Field Tests     \
             /---------------------------------\
            /     Hardware-in-the-Loop (HIL)    \
           /     & Fault Injection Harness       \
          /---------------------------------------\
         /    Integration Tests (MQTT/TLS/DB)      \
        /-------------------------------------------\
       /      Unit Tests (Data Models & Drivers)     \
      +-----------------------------------------------+
```

### 2. Modus Kegagalan Kritis & Mitigasi Firmware

| Modus Kegagalan | Penyebab Fisik | Bahaya bagi Sistem | Strategi Mitigasi Firmware |
|---|---|---|---|
| **Packet Loss / Drop** | Interferensi RF, kemacetan rute | Hilangnya data telemetri kritis | *Store-and-forward local ring-buffer* di flash/RAM. |
| **Power Brownout** | Baterai drop saat transmit radio | Mikrokontroler membeku (*hang/crash*) | Konfigurasi *Brownout Detector* (BOD) hardware reset. |
| **Payload Corruption** | Derau elektromagnetik industri | Salah interpretasi aktuator berbahaya | Validasi checksum CRC-16 / HMAC SHA-256. |
| **Broker Unreachable** | Server awan maintenance | Buffer lokal meledak (OOM) | Strategi *FIFO overwrite* dan backoff eksponensial. |

### 3. Formulasi Kuantitatif Keandalan: MTBF, MTTR, & Availability

Keandalan sistem dievaluasi melalui metrik waktu operasional:

1. **Mean Time Between Failures (MTBF)**: Rata-rata durasi sistem beroperasi normal di antara dua kegagalan:
   $$\text{MTBF} = \frac{\text{Total Waktu Operasi} - \text{Total Waktu Perbaikan}}{\text{Jumlah Kejadian Kegagalan}}$$
2. **Mean Time To Repair (MTTR)**: Rata-rata waktu yang dibutuhkan untuk mendiagnosis dan memulihkan sistem:
   $$\text{MTTR} = \frac{\text{Total Waktu Perbaikan}}{\text{Jumlah Kejadian Kegagalan}}$$
3. **Ketersediaan Sistem (Availability / $A$)**: Rasio waktu sistem berada dalam kondisi operasional penuh:
   $$A = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$

Sebagai contoh, jika sebuah instalasi pemantauan lingkungan beroperasi selama 1 tahun (8760 jam), mengalami 4 kali insiden kegagalan, dengan total akumulasi waktu pemulihan 12 jam:

$$\text{MTBF} = \frac{8760 - 12}{4} = \frac{8748}{4} = 2187.0\text{ jam}$$

$$\text{MTTR} = \frac{12}{4} = 3.0\text{ jam}$$

$$A = \frac{2187.0}{2187.0 + 3.0} = \frac{2187.0}{2190.0} \approx 0.99863\ (99.863\%)$$

## Latihan

1. **Analisis Fenomena Brownout**: Jelaskan mengapa penurunan tegangan operasional mikrokontroler dari 3.3V ke 2.2V (di bawah tegangan ambang minimum) lebih berbahaya daripada pemutusan daya total (0V). Bagaimana sirkuit *Brownout Detector* (BOD) internal ESP32 melindungi integritas memori flash selama kondisi tegangan kritis?
2. **Kalkulasi Metrik Ketersediaan (High Availability)**: Sebuah gerbang IoT industri beroperasi selama 3 tahun (26.280 jam) dan mengalami 6 kali insiden down dengan total durasi pemulihan 18 jam. Hitung nilai MTBF, MTTR, dan persentase Availability sistem tersebut.
3. **Penyusunan Lembar FMEA**: Buatlah matriks analisis mode kegagalan (FMEA) ringkas untuk subsistem sensor suhu lingkungan luar ruangan, yang mengevaluasi nilai *Severity* (S), *Occurrence* (O), dan *Detection* (D) dalam skala 1–10 untuk menghitung nilai *Risk Priority Number* ($\text{RPN} = S \times O \times D$).

## Tugas

Kembangkan modul simulasi *Fault Injection Harness* Python (`fault_injection_harness.py`) yang:
1. Memodelkan klien IoT tangguh (*ResilientDeviceClient*) yang memiliki kapasitas buffer offline lokal.
2. Menguji respon klien terhadap penyuntikan kegagalan jaringan (*network packet drop*) selama 3 siklus berturut-turut, membuktikan data tertahan di buffer dan terkuras habis secara berurutan saat jaringan pulih.
3. Menyuntikkan simulasi gangguan daya *brownout* dan memverifikasi transisi status pemulihan otonom pasca-reboot.
4. Menghitung dan memvalidasi metrik keandalan MTBF, MTTR, dan Availability secara terpadu.

## Ringkasan

1. Keandalan sistem IoT tidak dapat diasumsikan, melainkan harus dibuktikan melalui pengujian penyuntikan gangguan (*fault injection*).
2. Firmware yang tangguh wajib mengombinasikan penyimpanan buffer offline lokal dengan mekanisme deteksi hardware brownout.
3. Kuantifikasi keandalan berbasis MTBF dan MTTR memberikan metrik objektif untuk audit tingkat layanan (SLA) industri.

## Referensi

1. O'Connor, P., & Kleyner, A. *Practical Reliability Engineering*. 5th Edition, John Wiley & Sons, 2012.
2. Bass, L., et al. *Software Architecture in Practice: Reliability and Fault Tolerance*. Addison-Wesley, 2021.
3. IEEE Std 1413. *IEEE Standard Framework for Reliability Prediction of Hardware*. IEEE, 2020.

# Modul E03 — Cellular IoT, 5G Massive MTC & Power Saving Modes

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Membandingkan karakteristik transmisi radio 3GPP Rel 13/14 antara NB-IoT dan LTE-M (bandwidth, coverage enhancement, mobilitas, data rate).
2. Mengonfigurasi timer penghematan daya 3GPP T3324 (Active Timer) dan T3412 (Periodic TAU Timer) untuk efisiensi ekstrem.
3. Menghitung profil energi komposit per siklus transmisi (Tx, Rx, Idle Standby, PSM Deep Sleep).
4. Memvalidasi masa pakai baterai LiSOCl2 5400 mAh melampaui target 10 tahun operasional utilitas perkotaan.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 11, Chapter 14, Chapter 31.
- Modul Jalur Peminatan Prasyarat: Modul E01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Evolusi Seluler untuk IoT Skala Masif (3GPP Rel 13-17)
Jaringan seluler konvensional (2G/3G/4G Cat-4) dirancang untuk komunikasi suara dan data pita lebar dengan asumsi perangkat diisi ulang baterainya secara teratur. Dalam konteks smart city (meteran air terpendam di selokan, sensor tekanan pipa gas alam), perangkat harus beroperasi 10 hingga 15 tahun tanpa penggantian baterai.

3GPP Release 13 memperkenalkan standar seluler berlisensi berdaya rendah:
- **NB-IoT (Cat-NB1/NB2)**: Memanfaatkan alokasi pita ultra-sempit 180 kHz. Fokus utama adalah efisiensi spektral dan penetrasi struktur beton melalui pengulangan transmisi (Coverage Enhancement hingga +20 dB dibanding GPRS).
- **LTE-M (eMTC / Cat-M1)**: Beroperasi pada kanal 1.4 MHz. Mendukung data rate lebih tinggi (hingga 1 Mbps), latensi rendah, mobilitas penuh (seamless cell handover), dan Voice-over-LTE (VoLTE).

### 2. Arsitektur Penghematan Daya: PSM dan eDRX
1. **Power Saving Mode (PSM)**:
   Perangkat mematikan sirkuit radio sepenuhnya namun mempertahankan status registrasi di Core Network (MME/AMF). Tidak diperlukan pensinyalan attach ulang yang memboroskan daya saat bangun. Timer kunci:
   - **T3324 (Active Timer)**: Modem tetap bersiap menerima downlink paging sesaat setelah transmisi uplink selesai.
   - **T3412 (Periodic TAU Timer)**: Siklus pelaporan periodik status perangkat yang dapat diatur dari menit hingga 410 hari.
2. **extended Discontinuous Reception (eDRX)**:
   Memperpanjang siklus tidur receiver selama status terhubung tanpa memutus tautan RRC, menurunkan konsumsi idle listening secara drastis.

### 3. Formulasi Matematis Model Konsumsi Daya & Masa Pakai

1. **Energi Siklus Komposit ($E_{\text{cycle}}$)**:
   $$
   E_{\text{cycle}} = (P_{\text{tx}} \cdot t_{\text{tx}}) + (P_{\text{rx}} \cdot t_{\text{rx}}) + (P_{\text{idle}} \cdot t_{\text{idle}}) + (P_{\text{psm}} \cdot t_{\text{psm}})
   $$
   dengan $t_{\text{idle}} = T_{3324} - (t_{\text{tx}} + t_{\text{rx}})$ dan $t_{\text{psm}} = T_{3412} - T_{3324}$.

2. **Konsumsi Arus Rata-Rata ($I_{\text{avg}}$)**:
   $$
   P_{\text{avg}} = \frac{E_{\text{cycle}}}{T_{3412}} \implies I_{\text{avg}} = \frac{P_{\text{avg}}}{V_{\text{bat}}}
   $$

3. **Masa Pakai Baterai Kimiawi ($T_{\text{life}}$)**:
   $$
   T_{\text{life}} = \frac{C_{\text{bat}} \cdot \eta_{\text{derate}}}{I_{\text{avg}} \cdot 24 \cdot 365{,}25} \quad [\text{tahun}]
   $$
   dengan $\eta_{\text{derate}} \approx 0{,}85$ merepresentasikan faktor penuaan dan self-discharge sel LiSOCl2.

## Latihan

## Latihan Pemahaman Mandiri

1. **Pemilihan Teknologi**:
   - *Soal*: Manakah teknologi yang paling tepat untuk sistem pelacakan armada bus kota real-time: NB-IoT atau LTE-M? Jelaskan secara ilmiah.
   - *Jawaban*: LTE-M (Cat-M1). NB-IoT tidak mendukung handover mulus saat perangkat bergerak melintasi batas sel tower seluler. NB-IoT harus memutus koneksi dan melakukan registrasi ulang yang memicu latensi tinggi dan konsumsi energi besar. LTE-M mendukung seamless handover dan throughput 1 Mbps yang ideal untuk telemetri posisi kendaraan yang dinamis.

2. **Dampak Pemanjangan Timer T3324**:
   - *Soal*: Apa akibatnya jika timer T3324 diatur terlalu besar (misalnya 120 detik) pada sensor parkir nirkabel?
   - *Jawaban*: Perangkat akan tertahan pada status Active Idle mendengarkan kanal radio selama 2 menit setiap selesai transmisi dengan daya sekitar 10 mW, alih-alih lelap ke status PSM (15 uW). Hal ini akan menguras baterai dengan cepat dan menggagalkan target operasional multi-tahun.

## Tugas

## Penugasan Mandiri: Optimasi Parameter Baterai Meteran Air

1. Jalankan simulasi dengan memvariasikan interval pelaporan data (TAU) dari 1 jam hingga 24 jam dengan inkremen 1 jam.
2. Gambarkan grafik hubungan antara frekuensi pelaporan harian terhadap estimasi umur baterai.
3. Hitung kapasitas baterai minimum (mAh) yang dibutuhkan agar perangkat yang mengirim data tiap 6 jam dapat beroperasi minimal 10 tahun.
4. Buat dokumen spesifikasi teknis pemilihan sel baterai LiSOCl2 untuk kondisi suhu perkotaan tropis (30-45 derajat Celcius).

## Ringkasan
- Modul E03 memberikan pemahaman mendalam dan terapan mengenai Cellular IoT, 5G Massive MTC & Power Saving Modes pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [cellular_iot_energy_sim.py](src/cellular_iot_energy_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. 3GPP TS 23.682 - Architecture enhancements to facilitate communications with packet data networks and applications, [https://www.3gpp.org/DynaReport/23682.htm](https://www.3gpp.org/DynaReport/23682.htm) (diperiksa 2026-11-18).
2. GSMA NB-IoT Deployment Guide to Basic Security and Power Optimizations, [https://www.gsma.com/iot/resources/nb-iot-deployment-guide/](https://www.gsma.com/iot/resources/nb-iot-deployment-guide/) (diperiksa 2026-11-18).

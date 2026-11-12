# Chapter 08 — Sensors, Calibration & Measurement Uncertainty

## Overview

Sensor yang menghasilkan angka di Serial Monitor belum tentu menghasilkan angka yang **benar**. Sebagian besar sensor murah memiliki penyimpangan titik nol (*zero offset*), kesalahan kemiringan (*gain error*), *noise* acak, pergeseran seiring waktu (*drift*), serta keterlambatan respons terhadap perubahan lingkungan. Di dunia rekayasa telekomunikasi, lingkungan, dan industri, data tanpa kalibrasi dan pernyataan **ketidakpastian pengukuran (*measurement uncertainty*)** tidak dapat dijadikan dasar pengambilan keputusan yang andal.

Chapter ini membahas klasifikasi sensor, perbedaan *accuracy*, *precision*, *resolution*, dan *sensitivity*, pemisahan *systematic* vs *random error*, prosedur kalibrasi satu-titik dan dua-titik, *response time* ($\tau$), propagasi ketidakpastian (*Type A* dan *Type B*), pembacaan *datasheet* sensor, serta praktik validasi terhadap data referensi yang jelas.

## Prasyarat

- Memahami pembagi tegangan dan keselamatan DC dari [Chapter 03](#/chapter/3).
- Menguasai pembacaan `ADC1`, kuantisasi LSB, dan *moving average* dari [Chapter 07](#/chapter/7).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Mengklasifikasikan** sensor berdasarkan kebutuhan daya (*active/passive*), keluaran sinyal (*analog/digital*), dan prinsip fisikanya.
2. **Membedakan** secara tepat arti *accuracy*, *precision*, *resolution*, *sensitivity*, serta *systematic error* versus *random error*.
3. **Menyusun** dan menghitung **kalibrasi dua titik** (*slope & offset*) dari perbandingan terhadap data referensi yang terdokumentasi.
4. **Menghitung** ketidakpastian gabungan (*Type A* dari pengulangan sampel dan *Type B* dari resolusi/referensi datasheet) serta membaca parameter kritis *datasheet* sensor.

## Konsep dan teori

### 1. Klasifikasi Sensor

Sensor dapat dikelompokkan melalui tiga sumbu utama:
- **Sumber Energi**: *Passive sensor* menghasilkan sinyal tanpa eksitasi luar (misal termokopel, fotodioda mode fotovoltaik) vs *Active sensor* membutuhkan eksitasi/catu daya (termistor NTC dalam pembagi tegangan, sensor ultrasonik, sensor I2C digital).
- **Jenis Antarmuka**: *Analog* (tegangan kontinu ke `ADC1`, misal NTC, LDR, sensor pH analog) vs *Digital* (membawa ADC dan kompensasi internal melalui bus I2C, SPI, atau 1-Wire, misal BME280, SHT31, DS18B20).
- **Besaran Fisik**: Termal (NTC, RTD, IC digital), optik (LDR, fotodioda), mekanik/tekanan (strain gauge, MEMS akselerometer), kimia/gas (elektrokimia, NDIR $CO_2$).

### 2. Accuracy, Precision, Resolution, Sensitivity, dan Error

![Perbedaan akurasi vs presisi, kalibrasi dua titik, dan waktu respons orde-1](content/chapter-08/diagram.svg)

| Istilah Metrologi | Definisi Teknis | Contoh pada Sensor Suhu |
| --- | --- | --- |
| **Accuracy (Akurasi)** | Kedekatan hasil ukur terhadap nilai referensi (*true value*) | Penyimpangan maksimum $\pm 0{,}5\,^\circ\text{C}$ terhadap termometer referensi tersertifikasi |
| **Precision (Presisi)** | Konsistensi antar-pengulangan pada kondisi yang sama | Lima kali baca beruntun menghasilkan $25{,}54 \pm 0{,}05\,^\circ\text{C}$ (meski referensi $25{,}0\,^\circ\text{C}$) |
| **Resolution (Resolusi)** | Perubahan terkecil yang dapat dideteksi instrumen | $0{,}01\,^\circ\text{C}$ atau $1\text{ LSB}$ ADC |
| **Sensitivity (Sensitivitas)** | Rasio perubahan keluaran terhadap perubahan masukan ($\Delta y / \Delta x$) | $10\text{ mV}/^\circ\text{C}$ untuk sensor analog linier (LM35) |

**Resolusi tinggi $\neq$ Akurasi tinggi!** Anda bisa menampilkan 4 angka di belakang koma ($25{,}5432\,^\circ\text{C}$), tetapi jika ada *offset* $+1{,}5\,^\circ\text{C}$, angka itu tetap tidak akurat.

**Dua Jenis Kesalahan (*Error*)**:
- **Systematic Error**: Kesalahan yang berulang dengan pola konsisten (bias/offset nol, kesalahan *gain*, kesalahan nilai resistor pembagi $1\%$). **Dapat dikoreksi melalui kalibrasi.**
- **Random Error**: Fluktuasi acak tak terprediksi akibat *thermal noise* dan interferensi. **Tidak dapat dihilangkan kalibrasi**, tetapi dapat dikuantifikasi dengan simpangan baku ($s$) dan ditekan dengan *averaging* ($N$ sampel).

### 3. Metode Kalibrasi & Sensor Response Time

1. **One-Point Calibration (Offset Only)**: Mengoreksi pergeseran konstan pada satu titik acuan ($T_{\text{cal}} = T_{\text{raw}} + b$). Mudah, tetapi gagal jika kemiringan kurva (*gain*) juga melenceng.
2. **Two-Point Linear Calibration (Slope & Offset)**: Menggunakan dua titik referensi stabil ($T_{\text{ref, L}}, T_{\text{ref, H}}$) di ujung rentang kerja (misal penangas es $0\,^\circ\text{C}$ dan air hangat terukur $60\,^\circ\text{C}$):
   $$m = \frac{T_{\text{ref, H}} - T_{\text{ref, L}}}{T_{\text{raw, H}} - T_{\text{raw, L}}}, \qquad b = T_{\text{ref, L}} - m \cdot T_{\text{raw, L}}, \qquad T_{\text{cal}} = m \cdot T_{\text{raw}} + b$$
3. **Model Non-Linier (Contoh: Persamaan Beta Termistor NTC)**: Resistansi NTC turun eksponensial saat suhu naik, sehingga digunakan model:
   $$\frac{1}{T_{\text{K}}} = \frac{1}{T_0} + \frac{1}{\beta} \ln\left(\frac{R_{\text{NTC}}}{R_0}\right)$$

**Response Time ($\tau$) & Drift**:
Sensor termal memiliki inersia massa (*first-order response*). Setelah perubahan suhu mendadak (*step input*), sensor mencapai **$63{,}2\%$** perubahan akhir dalam $1\tau$ dan **$99{,}3\%$** dalam **$5\tau$**. Mengambil data kalibrasi sebelum $5\tau$ tercapai menghasilkan bias dinamis! Selain itu, komponen menua atau terpapar kelembaban tinggi mengalami **drift** sehingga kalibrasi perlu dijadwalkan ulang secara berkala.

### 4. Akuisisi Data & Propagasi Ketidakpastian Sederhana

Mengacu pada kerangka *GUM (Guide to the Expression of Uncertainty in Measurement)*, ketidakpastian gabungan ($u_c$) menggabungkan dua sumber:
- **Type A ($u_A$)**: Dievaluasi secara statistik dari $N$ pembacaan berulang:
  $$\bar{x} = \frac{1}{N}\sum_{i=1}^N x_i, \qquad s = \sqrt{\frac{1}{N-1}\sum_{i=1}^N (x_i - \bar{x})^2}, \qquad u_A = \frac{s}{\sqrt{N}}$$
- **Type B ($u_B$)**: Diperoleh dari spesifikasi *datasheet* alat referensi atau resolusi ($\pm a$ dengan distribusi persegi / *rectangular*):
  $$u_B = \frac{a}{\sqrt{3}}$$
- **Combined & Expanded Uncertainty ($k=2$ untuk $\sim 95\%$ kepercayaan)**:
  $$u_c = \sqrt{u_A^2 + u_{B,\text{ref}}^2 + u_{B,\text{res}}^2}, \qquad U = k \cdot u_c$$

Jika suatu besaran $y = f(x_1, x_2)$ dihitung dari beberapa input tak pasti yang saling bebas, propagasi ketidakpastian liniernya adalah:
$$u(y) = \sqrt{\left(\frac{\partial f}{\partial x_1} u(x_1)\right)^2 + \left(\frac{\partial f}{\partial x_2} u(x_2)\right)^2}$$

### 5. Membaca Sensor Datasheet Secara Kritis

Saat memilih sensor untuk proyek IoT, periksa minimal 6 kolom pada *datasheet*:
1. **Supply Voltage & Logic Level** ($3{,}3\text{ V}$ vs $5\text{ V}$).
2. **Operating & Calibrated Range** (rentang ukur aman vs rentang akurasi dijamin).
3. **Accuracy vs Resolution** (jangan tertipu resolusi 16-bit jika akurasi hanya $\pm 2\,^\circ\text{C}$).
4. **Response Time ($\tau_{63\%}$)** pada media udara tenang vs cairan.
5. **Self-Heating / Current Consumption** (arus eksitasi terus-menerus pada NTC memanaskan sensor sendiri!).
6. **Long-Term Drift** (misal $\pm 0{,}25\,^\circ\text{C/tahun}$).

### 6. Worked Example & Praktik Validasi (`calibration_uncertainty.py`)

Dataset sintetis [`telemetry.csv`](content/chapter-08/telemetry.csv) (`source=synthetic`) merekam perbandingan pembacaan sensor mentah terhadap termometer referensi ($0\,^\circ\text{C}$ s.d. $60\,^\circ\text{C}$) serta 5 kali pengulangan pada $25{,}00\,^\circ\text{C}$. Hasil eksekusi nyata skrip [`calibration_uncertainty.py`](content/chapter-08/src/calibration_uncertainty.py) (tercatat pada [`outputs.md`](content/chapter-08/outputs.md)):

- **Model kalibrasi 2-titik** ($0\,^\circ\text{C}$ dan $60\,^\circ\text{C}$):
  $$T_{\text{cal}} = 1{,}0381 \cdot T_{\text{raw}} - 1{,}4740$$
- **Penurunan Error (RMSE 5 titik)**: turun dari **$0{,}8544\,^\circ\text{C}$** sebelum kalibrasi menjadi **$0{,}0266\,^\circ\text{C}$** sesudah kalibrasi!
- **Ketidakpastian gabungan pada $25{,}00\,^\circ\text{C}$**:
  $u_A = 0{,}0221\,^\circ\text{C}$, $u_{B,\text{ref}} = 0{,}0577\,^\circ\text{C}$ (referensi $\pm 0{,}10\,^\circ\text{C}$), $u_{B,\text{res}} = 0{,}0144\,^\circ\text{C}$ $\implies$ $u_c = 0{,}0635\,^\circ\text{C}$.
  Nilai yang dilaporkan ($k=2$): **$25{,}05 \pm 0{,}13\,^\circ\text{C}$**.

Implementasi *Firmware* pada ESP32 tersedia di [`ex01_ntc_calibrated.ino`](content/chapter-08/src/ex01_ntc_calibrated/ex01_ntc_calibrated.ino) (disertai deteksi *open/short circuit* `NAN` dan `wokwi_diagram.json`), berstatus **Belum diuji** untuk eksekusi board/Wokwi di server ini.

### 7. Common Mistakes & Troubleshooting

| Kesalahan Metrologi | Dampak | Solusi |
| --- | --- | --- |
| Mengkalibrasi hanya 1 titik lalu mengasumsikan semua rentang akurat | *Gain error* membesar di suhu tinggi/rendah | Gunakan minimal kalibrasi 2 titik di batas rentang operasi |
| Mengambil sampel kalibrasi sebelum $5\tau$ | Kurva kalibrasi bergeser (*lag error*) | Tunggu kestabilan $\ge 5\tau$ dan pastikan suhu referensi homogen |
| Melaporkan akurasi lebih kecil dari ketidakpastian alat referensi | Klaim menyesatkan secara ilmiah | Sertakan $u_{B,\text{ref}}$ dalam $u_c$ |
| Arus eksitasi termistor terlalu besar (misal resistor seri terlalu kecil) | *Self-heating* menaikkan pembacaan $1\text{--}2\,^\circ\text{C}$ | Gunakan $R_{\text{fixed}} \ge 10\text{ k}\Omega$ atau aktifkan catu sensor hanya saat sampling |

### 8. Real-World Applications

- **Cold-Chain Farmasi & Vaksin**: Regulasi menuntut laporan suhu lengkap dengan sertifikat kalibrasi dan batas ketidakpastian $\le \pm 0{,}5\,^\circ\text{C}$ pada rentang $2\dots 8\,^\circ\text{C}$.
- **Environmental Air Quality & Smart Agriculture**: Sensor kelembaban dan konduktivitas tanah memerlukan kalibrasi spesifik media (*soil-specific calibration*) karena karakteristik tanah liat dan pasir berbeda drastis.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-08/exercises.md)):
1. Membedakan kasus akurasi vs presisi, *systematic* vs *random error*, dan membaca parameter *datasheet*.
2. Menghitung parameter kalibrasi dua titik ($m, b$) secara manual dan memperkirakan waktu tunggu $5\tau$.
3. Menghitung ketidakpastian gabungan $u_c$ dan $U$ ($k=2$) serta menjalankan [`calibration_uncertainty.py`](content/chapter-08/src/calibration_uncertainty.py).
4. Mini Challenge: Membandingkan akurasi kalibrasi *two-point* vs *ordinary least squares* (regresi linear seluruh 5 titik) di Python.

## Tugas

Susun **Prosedur Kalibrasi Sensor, Validasi Data Referensi & Laporan Ketidakpastian Pengukuran** (detail di tab **Tugas & Rubrik** — [assignment.md](content/chapter-08/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Metodologi kalibrasi & penanganan waktu respons | 25 | Kejelasan titik acuan, kondisi stabilitas $5\tau$, serta pemisahan *systematic* vs *random error* |
| Perhitungan model kalibrasi & validasi error | 30 | Ketepatan rumus *slope/offset*, perbandingan RMSE sebelum vs sesudah kalibrasi |
| Analisis ketidakpastian (Type A, Type B & k=2) | 25 | Perhitungan $u_A$, $u_B$ dari datasheet/referensi, $u_c$, dan pelaporan akhir yang benar |
| Implementasi akuisisi & kejujuran data | 20 | Sketsa/skrip validasi + pelabelan tegas sumber data (sintetis vs referensi vs fisik) |

## Ringkasan

- **Akurasi** adalah kedekatan ke nilai benar; **presisi** adalah konsistensi pengulangan; **resolusi** adalah langkah terkecil yang bisa dibaca.
- Kalibrasi dua titik ($T_{\text{cal}} = m \cdot T_{\text{raw}} + b$) menekan *systematic error* secara drastis (dalam uji data sintetis `telemetry.csv`, RMSE turun dari $0{,}8544\,^\circ\text{C}$ menjadi $0{,}0266\,^\circ\text{C}$).
- Pernyataan pengukuran profesional selalu menyertakan ketidakpastian gabungan ($u_c = \sqrt{u_A^2 + u_B^2}$), misalnya $25{,}05 \pm 0{,}13\,^\circ\text{C}$ ($k=2$).
- Analisis Python telah dieksekusi nyata (`outputs.md`); eksekusi `.ino` dan sensor NTC di Wokwi/hardware berstatus **Belum diuji** di server ini.

## Referensi

1. BIPM / JCGM 100:2008, *Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM)*, [https://www.bipm.org/en/committees/jc/jcgm/publications](https://www.bipm.org/en/committees/jc/jcgm/publications) (diperiksa 2026-11-10).
2. NIST, *Engineering Statistics Handbook — Measurement Uncertainty & Calibration*, [https://www.itl.nist.gov/div898/handbook/mpc/section5/mpc5.htm](https://www.itl.nist.gov/div898/handbook/mpc/section5/mpc5.htm) (diperiksa 2026-11-10).
3. Wokwi Documentation, *NTC Temperature Sensor Reference*, [https://docs.wokwi.com/parts/wokwi-ntc-temperature-sensor](https://docs.wokwi.com/parts/wokwi-ntc-temperature-sensor) (diperiksa 2026-11-10).


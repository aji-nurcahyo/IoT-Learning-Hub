# Chapter 40: Advanced IoT Systems Capstone

## Tujuan pembelajaran

Setelah menyelesaikan modul capstone ini, peserta didik mampu:
1. Mengintegrasikan seluruh kompetensi rekayasa Level 4 ke dalam satu platform sistem terpadu: **Intelligent, Secure & Resilient IoT Monitoring Platform**.
2. Memverifikasi pengoperasian perangkat berdaya rendah (*Low-Power Design & Deep Sleep*) dengan estimasi masa pakai multi-tahun.
3. Membuktikan determinisme waktu nyata konkurensi FreeRTOS dan pemrosesan antrean *Producer-Consumer*.
4. Menjembatani komunikasi protokol industri Modbus RTU berbasis checksum CRC-16 dengan lapisan aplikasi modern.
5. Menjalankan inferensi model kecerdasan buatan terdistribusi (*Edge AI TinyML INT8*) untuk deteksi anomali mekanis motor secara otonom.
6. Mengimplementasikan kembaran digital (*Digital Twin*) untuk sinkronisasi state termal dan simulasi prediktif *What-If*.
7. Memvalidasi ketahanan sistem melalui injeksi kegagalan (*Chaos Fault Injection*), retensi buffer offline, dan penegakan tata kelola privasi (*Data Minimization*).

## Prasyarat

- Kelulusan seluruh modul Level 1, Level 2, dan Level 3 (Chapter 01–30).
- Penguasaan mendalam materi Level 4 (Chapter 31–39).
- Pemahaman rekayasa sistem perangkat lunak, jaringan terdistribusi, dan keamanan siber industri.

## Konsep dan teori

### 1. Arsitektur Platform Capstone Level 4

Platform Capstone memadukan seluruh pilar komputasi cerdas, ketahanan fisik, dan tata kelola sistem ke dalam satu arsitektur terintegrasi:

```
+---------------------------------------------------------------------------------+
|               Intelligent, Secure & Resilient IoT Monitoring Platform           |
+---------------------------------------------------------------------------------+
| 1. Perangkat Keras & Daya: ESP32 Deep Sleep + Power Gating + Battery Life Model |
+---------------------------------------------------------------------------------+
| 2. Konkurensi Real-Time: FreeRTOS Preemptive Scheduler + Thread-Safe Queues     |
+---------------------------------------------------------------------------------+
| 3. Protokol Industri: Modbus RTU Framing + Verifikasi Polinomial CRC-16        |
+---------------------------------------------------------------------------------+
| 4. Kecerdasan Edge AI: Ekstraksi Fitur Getaran + Kuantisasi INT8 Dense Layer   |
+---------------------------------------------------------------------------------+
| 5. Kembaran Digital: Model Dinamika Termal Orde-1 + Prediksi Skenario What-If   |
+---------------------------------------------------------------------------------+
| 6. Keandalan & Tata Kelola: Store-and-Forward + BOD + Sanitasi Privasi STRIDE   |
+---------------------------------------------------------------------------------+
```

### 2. Matriks Pengujian Penerimaan Sistem (SATC)

Untuk menjamin kriteria kelulusan teknis, platform diuji terhadap 6 Kasus Uji Penerimaan Sistem (*System Acceptance Test Cases*):

| Kasus Uji | Fokus Rekayasa | Kondisi Masukan | Kriteria Penerimaan (Acceptance Criteria) |
|---|---|---|---|
| **SATC-01** | Power Budgeting | $T_{act}=1\text{s}, I_{act}=100\text{mA}, T_{slp}=599\text{s}$ | Masa pakai baterai terbukti $\ge 1.0$ tahun dengan derating. |
| **SATC-02** | RTOS Determinism | Tiga task prioritas bertingkat (Pri 1, 2, 3) | Preemption task prioritas tertinggi seketika pada tick kedatangan. |
| **SATC-03** | Modbus RTU Framing | Permintaan holding register biner | Dekoding register suhu 25.5 $^\circ\text{C}$ dengan validasi CRC-16 benar. |
| **SATC-04** | TinyML Edge Anomaly | Sinyal getaran impak transien | Klasifikasi INT8 menghasilkan prediksi `BEARING_FAULT`. |
| **SATC-05** | Digital Twin Sync | Pemanas daya 100W lalu lonjakan 250W | Galat residu stabil dan proyeksi What-If memprediksi kenaikan suhu. |
| **SATC-06** | Resilience & Privacy | Injeksi putus jaringan & payload PII | Data tertahan di buffer terkuras utuh dan data PII terbuang 100%. |

### 2.1 Landasan Matematis: Metrik Efektivitas Sistem Gabungan (OEE) & Ketersediaan Capstone (Mathematical Foundations)

Pada perancangan platform industri tingkat akhir (Level 4 Capstone), keberhasilan integrasi dievaluasi menggunakan metrik Overall Equipment Effectiveness (OEE) dan keandalan sistem kritis:

1. **Model Overall Equipment Effectiveness (OEE)**:
   Metrik OEE menggabungkan tiga dimensi utama kinerja fasilitas industri: Ketersediaan (*Availability* / $A_{\text{oee}}$), Performa (*Performance* / $P_{\text{oee}}$), dan Kualitas (*Quality* / $Q_{\text{oee}}$):
   $$
   \text{OEE} = A_{\text{oee}} \times P_{\text{oee}} \times Q_{\text{oee}}
   $$
   - $A_{\text{oee}} = \frac{\text{Operating Time}}{\text{Planned Production Time}}$
   - $P_{\text{oee}} = \frac{\text{Ideal Cycle Time} \times \text{Total Count}}{\text{Operating Time}}$
   - $Q_{\text{oee}} = \frac{\text{Good Count}}{\text{Total Count}}$

2. **Kalkulasi Kinerja Platform Smart Factory Terpadu (Worked Example)**:
   Pabrik beroperasi selama waktu terencana $T_{\text{plan}} = 480\text{ menit}$ (8 jam).
   - Waktu henti akibat setup dan perawatan adalah $30\text{ menit} \rightarrow \text{Operating Time} = 450\text{ menit}$.
     $$
     A_{\text{oee}} = \frac{450}{480} = 0{,}9375 \quad (93{,}75\%)
     $$
   - Laju ideal produksi adalah $0{,}5\text{ menit/unit}$. Total unit yang diproduksi adalah $810\text{ unit}$.
     $$
     P_{\text{oee}} = \frac{0{,}5 \times 810}{450} = \frac{405}{450} = 0{,}9000 \quad (90{,}00\%)
     $$
   - Dari 810 unit yang diproduksi, sistem inspeksi Edge AI TinyML mendeteksi 16 unit cacat sehingga produk baik berjumlah $794\text{ unit}$.
     $$
     Q_{\text{oee}} = \frac{794}{810} \approx 0{,}9802 \quad (98{,}02\%)
     $$
   Nilai OEE komprehensif pabrik yang dipantau platform IoT adalah:
   $$
   \text{OEE} = 0{,}9375 \times 0{,}9000 \times 0{,}9802 \approx 0{,}8270 \quad (82{,}70\%)
   $$
   Pencapaian $\text{OEE} > 80\%$ merefleksikan standar kelas dunia (*World Class Manufacturing*), membuktikan bahwa integrasi platform end-to-end mampu menyajikan analitik kuantitatif yang presisi untuk pengambilan keputusan operasional.

## Latihan

1. **Analisis Ketergantungan Subsistem**: Bagaimana kegagalan pada subsistem proteksi daya (Chapter 31) dapat merembet (*cascading failure*) dan memicu anomali inferensi pada model TinyML (Chapter 35)? Jelaskan perlunya detektor brownout sebagai penjaga gerbang operasional.
2. **Evaluasi Matriks SATC**: Mengapa keenam kasus uji penerimaan sistem (SATC-01 hingga SATC-06) dirancang deterministik dan dapat dieksekusi secara otomatis dalam pipeline CI/CD tanpa intervensi manual pengembang?
3. **Penyusunan Rencana Deployment Lapangan**: Jika sistem capstone ini hendak dipasang pada instalasi turbin angin lepas pantai (*offshore wind turbine*), sebutkan modifikasi fisik dan protokol tambahan yang dibutuhkan untuk menjamin operasi 5 tahun tanpa servis langsung di lokasi.

## Tugas

Eksekusi modul terpadu *Advanced IoT Systems Capstone Platform* Python (`advanced_capstone_platform.py`). Verifikasi bahwa seluruh 6 Kasus Uji Penerimaan Sistem (SATC-01 sampai SATC-06) dieksekusi tuntas dengan status `PASS` 100%. Susun laporan teknis komprehensif yang mendokumentasikan hasil pengujian, diagram arsitektur sistem, dan analisis keandalan platform.

## Ringkasan

1. Capstone Level 4 menyatukan seluruh pilar rekayasa: hemat daya, determinisme RTOS, protokol industri, inferensi TinyML, kembaran digital, dan ketahanan siber.
2. Pengujian penerimaan berbasis matriks SATC menjamin setiap persyaratan teknis terverifikasi secara matematis dan empiris.
3. Arsitektur terintegrasi ini menjadi representasi standar industri untuk sistem IoT masa depan yang cerdas, aman, dan tahan banting.

## Referensi
- SEMI E10-0304, *Specification for Definition and Measurement of Equipment Reliability, Availability, and Maintainability (RAM)*.
- IEEE Std 1012-2016, *IEEE Standard for System, Software, and Hardware Verification and Validation*, IEEE.

1. IEEE Internet of Things Journal. *Special Issue on Resilient, Secure, and Scalable IoT Systems*. 2023.
2. NIST Special Publication 800-213. *IoT Device Cybersecurity Guidance for the Federal Government*. National Institute of Standards and Technology, 2021.
3. CSA & OpenThread. *Matter Specification & Industrial IoT Reference Implementations*. 2024.

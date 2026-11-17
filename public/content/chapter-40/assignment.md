# Tugas Terbimbing: Validasi Platform Monitoring IoT Cerdas, Aman & Tangguh (Capstone Level 4)

## Deskripsi Tugas

Dalam tugas capstone ini, Anda diminta memverifikasi implementasi platform sistem pemantauan IoT cerdas, aman, dan tangguh (*Intelligent, Secure & Resilient IoT Monitoring Platform*) dengan mengeksekusi rangkaian kasus uji penerimaan sistem menyeluruh (*System Acceptance Test Cases / SATC*).

Tugas ini mewajibkan:
1. Pemodelan sistem capstone yang mengintegrasikan 6 pilar rekayasa Level 4:
   - **SATC-01**: Profil konsumsi daya rendah (*Low-Power Budgeting*) dan estimasi masa pakai multi-tahun.
   - **SATC-02**: Penjadwalan deterministik *FreeRTOS Preemption* dan antrean *thread-safe*.
   - **SATC-03**: Protokol industri *Modbus RTU Framing* dengan verifikasi *CRC-16*.
   - **SATC-04**: Inferensi kecerdasan buatan terdistribusi *Edge AI TinyML INT8* untuk deteksi anomali vibrasi bantalan motor.
   - **SATC-05**: Sinkronisasi kembaran digital (*Digital Twin*) dan simulasi prediktif *What-If*.
   - **SATC-06**: Ketahanan penyuntikan gangguan jaringan, *Store-and-Forward*, dan filter privasi *Data Minimization*.
2. Eksekusi pengujian otomatis berbasis modul Python mandiri yang membuktikan kelulusan 100% pada keenam kasus uji penerimaan sistem.
3. Penyusunan laporan teknis arsitektur sistem komprehensif yang mendokumentasikan diagram interkoneksi subsistem, evaluasi hasil pengujian empiris, serta rencana implementasi perangkat keras fisik.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-40/src/advanced_capstone_platform.py`.
2. Laporan akhir capstone yang menyajikan matriks hasil SATC-01 sampai SATC-06, diagram arsitektur sistem, dan analisis kelayakan deployment industri.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Kelengkapan Integrasi 6 Pilar Arsitektur Level 4** | 35 Poin | Platform mengintegrasikan pilar hemat daya, RTOS, Modbus, TinyML, Digital Twin, dan resiliensi secara harmonis dalam arsitektur kode modular yang bersih. |
| **Kebenaran Fungsional Matriks SATC-01 s/d SATC-06** | 35 Poin | Seluruh 6 kasus uji penerimaan sistem dieksekusi tuntas, lulus assert matematis 100%, dan terbebas dari kesalahan logika maupun kegagalan timing. |
| **Kualitas Dokumentasi Teknis & Analisis Rekayasa** | 30 Poin | Pembahasan menyajikan analisis mendalam mengenai trade-off desain, bukti log deterministik, serta kepatuhan penuh terhadap standar anti-slop akademik. |

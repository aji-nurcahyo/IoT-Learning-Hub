# Tugas Rekayasa & Rubrik: Modul B06

## Laporan Rekayasa Lengkap Proyek Capstone Predictive Maintenance

Susun laporan teknik komprehensif implementasi platform Edge PdM:
1. Dokumentasikan arsitektur sistem perangkat lunak dan diagram interaksi komponen.
2. Sajikan hasil eksekusi 4 skenario uji penerimaan sistem (SATC) lengkap dengan grafik bentuk gelombang sinyal.
3. Hitung estimasi penghematan biaya operasional (*Return on Investment* / ROI) dari pencegahan downtime katastropik pabrik.
4. Lampirkan rubrik penilaian mandiri 100 poin.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Arsitektur Sistem & Pipeline Akuisisi Getaran Frekuensi Tinggi** | 25 | Integritas sampling 10 kHz, buffer ganda DMA, dan kepatuhan model Purdue. |
| **Ekstraksi Fitur Selubung Hilbert & Deteksi Cacat Bearing** | 25 | Ketepatan implementasi Transformasi Hilbert, identifikasi BPFO, dan Kurtosis. |
| **Klasifikasi Keparahan ISO 20816 & Proteksi Trip Safe State** | 25 | Kesesuaian standar vibrasi ISO, kecepatan respon interlock darurat (< 50 ms). |
| **Integrasi OPC UA, Verifikasi SATC & Laporan Teknik** | 25 | Kelulusan 100% SATC, struktur pohon alamat OPC UA, dan profesionalisme laporan. |

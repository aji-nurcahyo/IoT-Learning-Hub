# Tugas Rekayasa & Rubrik: Modul D01

## Pemodelan Kinerja Hardware Roofline untuk Arsitektur Edge AI TinyML

Rancang studi komparasi analitis kinerja inferensi mikrokontroler target:
1. Buat model Roofline untuk keluarga prosesor ARM Cortex-M4 (tanpa SIMD) vs Cortex-M55 (dengan Helium SIMD).
2. Evaluasi estimasi latensi inferensi model CNN 1D audio klasifikasi pada kedua prosesor.
3. Lampirkan skrip Python perhitungan batas bandwidth memori dan grafik kurva Roofline.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Pemahaman Arsitektur SIMD & Akselerator NPU** | 30 | Ketepatan identifikasi perbedaan CPU, DSP, dan NPU systolic array. |
| **Formulasi & Kalkulasi Roofline Performance Model** | 35 | Akurasi perhitungan intensitas aritmatika, batas bandwidth, dan titik lutut. |
| **Analisis Profiling Memori & Kualitas Laporan** | 35 | Kedalaman evaluasi penempatan tensor Flash vs SRAM dan kejelasan penyajian data. |

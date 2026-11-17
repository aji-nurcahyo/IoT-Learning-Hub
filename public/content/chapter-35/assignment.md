# Tugas Terbimbing: Pipeline Ekstraksi Fitur & Inferensi TinyML Model INT8

## Deskripsi Tugas

Dalam tugas ini, Anda diminta merancang dan memvalidasi saluran pemrosesan data cerdas (*Edge AI pipeline*) untuk mendeteksi anomali getaran mesin industri secara lokal menggunakan teknik ekstraksi fitur domain waktu dan inferensi model terkuantisasi INT8.

Tugas ini mewajibkan:
1. Pembuatan algoritma ekstraksi fitur statistik domain waktu yang menghitung nilai *Mean*, *Root Mean Square* (RMS), *Peak-to-Peak* (P2P), dan *Zero Crossing Rate* (ZCR) dari jendela data getaran sensor.
2. Implementasi inferensi model *Dense Layer* berbasis fixed-point integer INT8 yang memetakan sinyal masukan kontinu ke dalam rentang kuantisasi $[-128, 127]$ dan menghasilkan skor klasifikasi kondisi *Normal* versus *Anomali Kerusakan Bantalan*.
3. Verifikasi otomatis skenario deteksi melalui eksekusi modul Python mandiri yang membuktikan akurasi prediksi pada sinyal uji normal dan sinyal uji anomali impak mekanis.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-35/src/tinyml_inference_sim.py`.
2. Laporan analisis teknis yang menyajikan tabel perbandingan nilai fitur statistik, analisis kuantisasi bobot dan bias, serta perhitungan estimasi penghematan energi dan memori embedded.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Ekstraksi Fitur Statistik Domain Waktu** | 35 Poin | Implementasi komputasi Mean, RMS, Peak-to-Peak, dan Zero-Crossing Rate terbukti akurat, menangani deret waktu secara efisien, dan membedakan profil energi sinyal secara jelas. |
| **Implementasi Kuantisasi & Inferensi INT8 Fixed-Point** | 35 Poin | Pemodelan fungsi kuantisasi input ($S$ dan $Z$), komputasi dot product integer terhindar dari overflow, serta pemisahan skor klasifikasi menghasilkan prediksi kondisi mesin yang tepat. |
| **Analisis Rekayasa Batasan Memori & Efisiensi Energi** | 30 Poin | Pembahasan menyajikan analisis mendalam mengenai pemanfaatan memori statis (Tensor Arena), trade-off komputasi INT8 vs FP32, dan keuntungan konsumsi daya Edge AI dibandingkan transmisi awan. |

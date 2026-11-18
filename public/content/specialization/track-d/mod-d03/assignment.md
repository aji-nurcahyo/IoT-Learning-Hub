# Tugas Rekayasa & Rubrik: Modul D03

## Pelatihan Model TinyML Klasifikasi Getaran dengan QAT & Structured Pruning

Rancang alur kerja kompresi model deep learning kompak:
1. Latih model CNN 1D baseline dalam format float32 pada dataset fitur sensor.
2. Terapkan Quantization-Aware Training (QAT) dengan simulasi kuantisasi INT8 pada layer konvolusi.
3. Lakukan pemangkasan filter terstruktur hingga mencapai sparsity minimal $25%$.
4. Bandingkan akurasi, ukuran berkas FlatBuffers TFLite, dan estimasi siklus komputasi MAC.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Konsep & Implementasi QAT vs PTQ** | 30 | Ketepatan pemodelan fake quantization forward pass dan simulasi noise pembulatan. |
| **Penerapan Straight-Through Estimator & Pruning** | 35 | Kualitas aproksimasi gradien dan pemangkasan filter terstruktur berbobot kecil. |
| **Formulasi Knowledge Distillation & Laporan Rekayasa** | 35 | Penurunan matematis soft loss Hinton, analisis trade-off kompresi vs akurasi. |

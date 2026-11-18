# Tugas Rekayasa & Rubrik: Modul D02

## Perancangan Pipeline Ekstraksi Fitur Akustik Fixed-Point pada Mikrokontroler

Rancang modul ekstraksi fitur streaming sinyal sensor:
1. Implementasikan filter digital IIR Biquad lolos-tinggi untuk menghilangkan desah offset DC.
2. Buat fungsi ekstraksi koefisien MFCC berbasis aritmatika integer fixed-point Q15.
3. Uji pipeline pada dataset rekaman suara bantalan normal dan bantalan aus, serta sajikan perbandingan akurasi representasi terhadap komputasi float32.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Desain Bank Filter Skala Mel & Konversi Frekuensi** | 30 | Ketepatan formula matematis skala Mel dan pemetaan frekuensi linier. |
| **Implementasi Aritmatika Integer Fixed-Point Q15** | 35 | Keberhasilan perkalian dan bit-shift tanpa floating-point software library. |
| **Kinerja Reduksi Dimensi & Validasi Output** | 35 | Efisiensi pemadatan ruang fitur dan ketepatan diferensiasi sinyal normal vs anomali. |

# Tugas Rekayasa & Rubrik: Modul B04

## Analisis Spektral & Diagnosis Kerusakan Bantalan Motor Induksi

Diberikan dataset getaran sintetis/rekaman akselerometer motor industri:
1. Hitung seluruh fitur domain waktu (Mean, RMS, Crest Factor, Kurtosis, Skewness).
2. Terapkan algoritma Transformasi Hilbert untuk membentuk sinyal selubung amplitudo.
3. Hitung FFT dari selubung dan bandingkan puncak spektral terhadap frekuensi teoritis BPFO dan BPFI.
4. Tulis laporan rekomendasi pemeliharaan berbasis data terhitung.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Perhitungan Fitur Domain Waktu (RMS, Peak, Kurtosis)** | 30 | Ketepatan implementasi formula matematis dan interpretasi ambang batas normal. |
| **Implementasi Demodulasi Selubung Hilbert & FFT** | 35 | Keberhasilan ekstraksi komponen modulasi dan identifikasi puncak spektrum. |
| **Kalkulasi Frekuensi Karakteristik Cacat Bantalan & Laporan** | 35 | Ketepatan formula BPFO/BPFI dan argumentasi diagnosis teknis yang kuat. |

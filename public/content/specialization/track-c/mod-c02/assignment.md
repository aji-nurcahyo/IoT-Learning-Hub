# Tugas Rekayasa & Rubrik: Modul C02

## Penugasan Mandiri: Pemulihan Kalibrasi Multi-Variabel & Estimasi GUM

Kembangkan modul Python yang menerima deret waktu pembacaan sensor tegangan mentah yang terdistorsi oleh kenaikan suhu siang hari dan degradasi penuaan selama 1 tahun. Terapkan algoritma kompensasi drift termal dan hasilkan format pelaporan metrologi resmi dengan nilai ketidakpastian $U_{95}$.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Analisis Fisika Drift & Penuaan** | 25 | Membedakan zero drift, span drift, dan penuaan reversibel vs ireversibel. |
| **Implementasi Algoritma Koreksi** | 35 | Perhitungan offset dan penskalaan tegangan terkoreksi akurat. |
| **Penerapan Metrologi GUM** | 25 | Propagasi varians dan evaluasi expanded uncertainty k=2 benar. |
| **Strategi In-Situ Re-Zeroing** | 15 | Rancangan metode ABC atau dual-probe dilaporkan secara realistis. |

# Latihan Terstruktur: Modul D06

## Latihan Pemahaman Mandiri

1. **Mengapa sistem multimodal capstone menggunakan Late Bayesian Fusion dibanding Early Fusion (menggabungkan sinyal audio mentah dan piksel kamera sebelum model)?**
   - *Jawaban*: Late Fusion memisahkan pipeline ekstraksi domain-spesifik berkecepatan berbeda, mereduksi kebutuhan sinkronisasi memori data mentah yang besar di SRAM, dan meningkatkan ketahanan sistem jika salah satu sensor mengalami gangguan.

2. **Sesuai kriteria penerimaan SATC-D02, batas latensi maksimum end-to-end dari pengambilan sampel sensor hingga evaluasi alarm adalah:**
   - *Jawaban*: 50 milidetik, guna menjamin respons proteksi mesin sebelum kerusakan mekanis katastropik terjadi.

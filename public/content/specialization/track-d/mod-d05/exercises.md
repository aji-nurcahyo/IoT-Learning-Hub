# Latihan Terstruktur: Modul D05

## Latihan Pemahaman Mandiri

1. **Jika nilai Population Stability Index (PSI) dari skor inferensi batch saat ini bernilai 0.38, tindakan apa yang direkomendasikan secara standar industri?**
   - *Jawaban*: Nilai PSI di atas 0.25 menunjukkan pergeseran populasi yang sangat signifikan dibanding data baseline, sehingga model harus di-retrain dengan data terbaru atau ambang batas anomali harus dikalibrasi ulang.

2. **Mengapa DWT (Data Watchpoint and Trace) Cycle Counter lebih dipilih untuk benchmarking latensi inferensi edge dibanding fungsi timer OS seperti millis()?**
   - *Jawaban*: Register DWT->CYCCNT mencatat setiap detak clock prosesor secara langsung di level silikon hardware, memberikan resolusi siklus instruksi nanodetik tanpa jitter interupsi sistem operasi.

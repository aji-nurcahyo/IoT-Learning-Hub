# Latihan Terstruktur: Modul D04

## Latihan Pemahaman Mandiri

1. **Mengapa matriks kovariansi error $P_k$ bernilai menurun setelah langkah Measurement Update pada EKF?**
   - *Jawaban*: Langkah Measurement Update menggunakan informasi sensor $z_k$ untuk mengoreksi state; perkalian $(I - K_k H_k) P_k^-$ secara matematis mereduksi kovariansi error karena kepastian sistem meningkat setelah observasi baru diterima.

2. **Pada Late Bayesian Fusion, apa keuntungan utama menggunakan representasi Log-Odds dibanding perkalian probabilitas langsung?**
   - *Jawaban*: Log-Odds mentransformasikan perkalian probabilitas independen menjadi operasi penjumlahan linier sederhana $\sum \log \Lambda_i$, sangat cepat dihitung pada prosesor integer fixed-point dan kebal terhadap resiko numerical underflow.

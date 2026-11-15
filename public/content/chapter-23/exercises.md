# Latihan Soal & Praktik — Chapter 23

## Bagian A — Soal Konseptual

1. **Perbandingan Latensi Keputusan**:
   Sebuah sistem pendingin tangki reaksi kimia membutuhkan waktu respon pemadaman darurat kurang dari $10\text{ ms}$ saat suhu melewati $60\,^\circ\text{C}$. Jika transmisi paket ke cloud membutuhkan waktu RTT $120\text{ ms}$ ditambah waktu komputasi server $30\text{ ms}$, jelaskan mengapa arsitektur kontrol berbasis cloud tidak memenuhi spesifikasi keselamatan operasional (*functional safety*).
2. **Karakteristik Filter IQR**:
   Diberikan sekumpulan pembacaan sensor getaran:
   `[10.1, 10.2, 10.0, 10.3, 10.2, 50.0, 10.1]`
   Jelaskan mengapa metode rata-rata aritmatika sederhana menghasilkan nilai yang terdistorsi secara signifikan, sedangkan metode IQR mampu mengeliminasi nilai `50.0` sebagai *outlier*.
3. **Mekanisme Anti-Chattering**:
   Jelaskan peran *deadband* dan *histeresis* dalam memperpanjang usia pakai komponen elektromekanik (seperti relay, motor servo, dan kompresor).

## Bagian B — Soal Praktik Komputasi

1. **Simulasi Profil Histeresis**:
   Gunakan kelas `LocalAutomationEngine` pada [`edge_engine.py`](content/chapter-23/src/edge_engine.py). Uji perilaku relay dengan profil suhu ruangan berikut:
   `[27.0, 28.5, 30.1, 30.4, 29.8, 29.2, 28.6, 28.3, 27.5]`
   Catat secara rinci status relay (`ON` atau `OFF`) serta aksi yang dihasilkan pada setiap titik pembacaan suhu.
2. **Pengujian Efisiensi Deadband**:
   Diberikan stream suhu yang bergerak lambat:
   `[25.0, 25.1, 25.1, 25.2, 25.3, 25.4, 25.5, 25.6, 25.6, 26.0]`
   Jika `threshold` deadband diatur sebesar $0{,}4\,^\circ\text{C}$, tentukan daftar nilai yang benar-benar dipublikasikan ke jaringan, dan hitung persentase data yang berhasil diredam.

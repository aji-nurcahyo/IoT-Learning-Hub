# Latihan Terstruktur: Modul C02

## Latihan Pemahaman Mandiri

1. **Apa perbedaan mendasar antara zero drift dan span drift pada kurva kalibrasi sensor?**
   - *Jawaban*: Zero drift menggeser seluruh kurva kalibrasi ke atas atau ke bawah secara paralel (offset bertambah konstan untuk semua nilai input), sedangkan span drift mengubah kemiringan kurva respons (sensitivitas sensor berubah, menghasilkan galat yang proporsional terhadap besar sinyal masukan).

2. **Mengapa nilai faktor cakupan $k = 2$ digunakan dalam menentukan ketidakpastian bentangan ($Expanded Uncertainty$ $U$)?**
   - *Jawaban*: Berdasarkan Teorema Limit Pusat, distribusi probabilitas dari kombinasi berbagai sumber ketidakpastian acak akan mendekati distribusi normal (Gauss). Faktor cakupan $k = 2$ merepresentasikan rentang interval kepercayaan sekitar $pm 2$ standar deviasi, yang mencakup probabilitas keyakinan sekitar $95{,}45\%$.

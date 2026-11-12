# Tugas & Rubrik — Chapter 03

## Skenario Tugas: Rancangan Kelistrikan, Power Budget & Audit Keselamatan Node Sensor

Anda diminta menyusun rancangan kelistrikan *low-voltage DC* untuk sebuah **Node Monitoring Ruang Server** yang terdiri dari:
- 1 unit papan MCU $3{,}3\text{ V}$ (batas aman per pin GPIO $\le 12\text{ mA}$, tegangan input pin maks $3{,}3\text{ V}$),
- 2 buah LED indikator (Merah $V_F = 2{,}0\text{ V}$ untuk status alarm, Hijau $V_F = 2{,}2\text{ V}$ untuk status normal, target masing-masing $5\text{--}8\text{ mA}$),
- 1 buah tombol tekan (*push button*) untuk reset alarm lokal,
- 1 buah modul sensor analog/digital bertenaga $5\text{ V}$ yang sinyal keluarannya mencapai $5\text{ V}$,
- Catu daya cadangan baterai $2500\text{ mAh}$ ($\eta = 0{,}80$) untuk operasi saat listrik padam.

## Instruksi & Deliverables

Buat laporan teknis singkat (format Markdown atau PDF) berisi:

1. **Perhitungan Rangkaian**:
   - Hitung nilai resistor pembatas arus standar untuk kedua LED beserta disipasi daya masing-masing.
   - Rancang rangkaian tombol dengan resistor *pull-up* atau *pull-down* $10\text{ k}\Omega$ dan nyatakan kondisi logika saat ditekan vs dilepas.
   - Rancang *voltage divider* dari sinyal $5\text{ V}$ ke pin $3{,}3\text{ V}$ dan buktikan nilainya aman ($2{,}7\text{ V} \le V_{\text{out}} \le 3{,}2\text{ V}$).
2. **Power Budget**: Hitung umur baterai jika saat mode darurat node aktif $5\text{ s}$ ($85\text{ mA}$) dan tidur $115\text{ s}$ ($0{,}20\text{ mA}$) per siklus $120\text{ s}$.
3. **Diagram Koneksi & Daftar Periksa Keselamatan (*Safety Checklist*)**: Buat diagram blok/skema koneksi lengkap dengan `GND` bersama serta minimal 5 langkah SOP aman sebelum menyalakan daya dan saat mengukur menggunakan multimeter.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Perhitungan Hukum Ohm, LED & voltage divider** | **30** | Ketepatan persamaan, pemilihan resistor standar, perhitungan arus aktual, disipasi daya, dan keamanan level tegangan. |
| **Penyusunan power budget & estimasi baterai** | **25** | Ketepatan perhitungan arus rata-rata *duty-cycle* serta analisis faktor yang memengaruhi umur baterai nyata. |
| **Audit keselamatan, batas GPIO & prosedur multimeter** | **25** | Kejelasan SOP *power-off wiring*, pencegahan *short/overcurrent/reverse polarity*, dan prosedur ukur paralel vs seri. |
| **Dokumentasi skema & kejujuran verifikasi** | **20** | Kejelasan label skema (*common GND*, nilai komponen) serta pemisahan tegas antara hitungan teoretis dan pengukuran fisik. |


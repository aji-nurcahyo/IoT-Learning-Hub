# Modul B05 — Industrial Reliability, Functional Safety & Safe State Control

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Membedakan laju kegagalan aman (safe) vs berbahaya (dangerous), serta terdeteksi (detected) vs tidak terdeteksi (undetected).
2. Menghitung Safe Failure Fraction (SFF) dan probabilitas kegagalan rata-rata saat permintaan (PFD_avg) sistem terinstrumentasi.
3. Menganalisis arsitektur voting redundansi perangkat keras (1oo1, 1oo2, 2oo3) untuk optimasi ketersediaan vs keselamatan.
4. Merancang sistem interlock keselamatan dan logika transisi ke kondisi aman (Safe State Control).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 20, Chapter 38.
- Modul Jalur Peminatan Prasyarat: Modul B01, Modul B03.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Fondasi Keselamatan Fungsional (IEC 61508 / IEC 61511)
Dalam sistem instrumentasi industri berisiko tinggi (misalnya reaktor kimia atau pemanas gas boiler), sistem keselamatan instrumen (*Safety Instrumented System* / SIS) harus dirancang terpisah dari sistem kontrol dasar (*Basic Process Control System* / BPCS). Standar IEC 61508 mengklasifikasikan kegagalan perangkat ke dalam 4 kuadran:
1. **Safe Detected ($lambda_{sd}$)**: Kegagalan aman yang terdeteksi oleh diagnostik internal (memicu trip aman).
2. **Safe Undetected ($lambda_{su}$)**: Kegagalan aman yang tidak terdeteksi.
3. **Dangerous Detected ($lambda_{dd}$)**: Kegagalan berbahaya yang dapat dideteksi diagnostik.
4. **Dangerous Undetected ($lambda_{du}$)**: Kegagalan paling kritis; komponen rusak tanpa disadari sehingga tidak merespon saat kondisi darurat datang.

### 2. Arsitektur Voting Redundansi (1oo2 vs 2oo3)
- **1oo1 (Single Channel)**: Tanpa toleransi kegagalan. Murah namun PFD tinggi.
- **1oo2 (1-out-of-2 Voting)**: Mengutamakan keselamatan (*Safety Priority*). Cukup satu dari dua sensor yang mendeteksi bahaya, sistem langsung trip. Kelemahan: rentan penghentian palsu pabrik (*spurious trip*).
- **2oo3 (2-out-of-3 Voting / TMR)**: Menyeimbangkan keselamatan dan ketersediaan operasional (*Safety & Availability*). Sistem hanya trip jika minimal dua sensor sepakat, menolak false-alarm akibat kerusakan sensor tunggal.

### 3. Landasan Matematis: Safe Failure Fraction & Probabilitas Kegagalan Rata-Rata (Mathematical Foundations)

1. **Safe Failure Fraction (SFF)**:
   $$
   	ext{SFF} = rac{sum lambda_s + sum lambda_{dd}}{sum lambda_s + sum lambda_d} 	imes 100%
   $$

2. **Probabilitas Kegagalan Rata-Rata pada Permintaan (PFD_avg)**:
   Untuk interval uji pembuktian berkala (*Proof Test Interval*) $T_I$ dan faktor kegagalan penyebab bersama $eta$:
   - Arsitektur 1oo1:
     $$
     	ext{PFD}_{	ext{avg, 1oo1}} = rac{lambda_{du} cdot T_I}{2}
     $$
   - Arsitektur 1oo2:
     $$
     	ext{PFD}_{	ext{avg, 1oo2}} = rac{lambda_{du}^2 cdot T_I^2}{3} + eta rac{lambda_{du} cdot T_I}{2}
     $$

**Worked Numerical Example**:
Sensor suhu dengan $lambda_{du} = 1{,}5 	imes 10^{-6}	ext{ jam}^{-1}$, $eta = 0{,}02$, dan interval proof-test tahunan $T_I = 8760	ext{ jam}$.
$$
	ext{PFD}_{	ext{1oo1}} = rac{1{,}5 	imes 10^{-6} 	imes 8760}{2} = 0{,}00657 quad (	ext{Target SIL 2: } 10^{-3} le 	ext{PFD} < 10^{-2})
$$
Saat dipasang konfigurasi redundant 1oo2:
$$
	ext{Suku 1} = rac{(1{,}5 	imes 10^{-6})^2 	imes (8760)^2}{3} approx 5{,}75 	imes 10^{-5}
$$
$$
	ext{Suku 2 (Common Cause)} = 0{,}02 	imes rac{1{,}5 	imes 10^{-6} 	imes 8760}{2} = 1{,}314 	imes 10^{-4}
$$
$$
	ext{PFD}_{	ext{1oo2}} = 5{,}75 	imes 10^{-5} + 1{,}314 	imes 10^{-4} approx 0{,}000189 quad (	ext{Target SIL 3: } 10^{-4} le 	ext{PFD} < 10^{-3})
$$
Arsitektur 1oo2 berhasil menaikkan tingkat integritas keselamatan sistem dari **SIL 2 ke SIL 3**.

## Latihan

### Soal 1: Penentuan Tingkat SIL (C3)
Sebuah sistem pemutus darurat katup gas memiliki nilai $	ext{PFD}_{	ext{avg}} = 2{,}4 	imes 10^{-3}$. Berdasarkan tabel standar IEC 61508, tentukan peringkat Safety Integrity Level (SIL) sistem tersebut!

### Soal 2: Evaluasi Arsitektur 2oo3 Voting (C4)
Jelaskan apa yang terjadi pada keputusan trip sistem 2oo3 jika Sensor A membaca suhu normal ($65^circ	ext{C}$), Sensor B membaca suhu kritis ($125^circ	ext{C}$), dan Sensor C membaca kabel putus (error open-loop)!

## Tugas

## Analisis Keandalan Sistem Instrumentasi Keselamatan & Perancangan Logika 2oo3

Rancang laporan analisis keandalan dan keselamatan fungsional sistem proteksi overpressure tangki bertekanan:
1. Hitung nilai Safe Failure Fraction (SFF) dari data laju kegagalan komponen instrumen.
2. Bandingkan PFD_avg arsitektur 1oo1, 1oo2, dan 2oo3 pada variasi interval uji pembuktian 6 bulan, 1 tahun, dan 2 tahun.
3. Buat skrip simulasi logika voting 2oo3 dengan penanganan kondisi sensor terdegradasi.

## Ringkasan
- Modul B05 memberikan pemahaman mendalam dan terapan mengenai Industrial Reliability, Functional Safety & Safe State Control pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [sil_voting_reliability_sim.py](src/sil_voting_reliability_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. IEC 61508: Functional safety of electrical/electronic/programmable electronic safety-related systems, [https://www.iec.ch/functional-safety](https://www.iec.ch/functional-safety) (diperiksa 2026-11-18).
2. Smith, D. J., Reliability, Maintainability and Risk: Practical Methods for Engineers, Butterworth-Heinemann, [https://www.elsevier.com/books/reliability-maintainability-and-risk/smith/978-0-12-818588-9](https://www.elsevier.com/books/reliability-maintainability-and-risk/smith/978-0-12-818588-9) (diperiksa 2026-11-18).

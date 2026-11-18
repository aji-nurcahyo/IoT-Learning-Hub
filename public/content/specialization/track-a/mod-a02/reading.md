# Modul A02 — Occupancy Sensing, Environmental Conditioning & Indoor Air Quality (IAQ)

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Membedakan prinsip deteksi kehadiran biner (PIR), jarak spasial (ToF), dan mikro-pergerakan pernapasan (radar mmWave 24 GHz).
2. Mengimplementasikan perhitungan konsentrasi gas CO2 berbasis Hukum Beer-Lambert serapan radiasi inframerah NDIR.
3. Merancang algoritma sensor fusion kehadiran tanpa false-trigger saat penghuni berada dalam kondisi duduk statis.
4. Mengembangkan kendali Demand-Controlled Ventilation (DCV) dengan histeresis deadband dinamis untuk mempertahankan CO2 < 800 ppm.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 07, Chapter 08, Chapter 23.
- Modul Jalur Peminatan Prasyarat: Modul A01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Spektroskopi Absorpsi Inframerah Tak-Terdispersi (NDIR CO2)
Pengukuran konsentrasi karbon dioksida ($	ext{CO}_2$) di dalam ruangan mengandalkan resonansi penyerapan optik inframerah pada panjang gelombang spesifik $lambda = 4{,}26,mu	ext{m}$.
- Sensor NDIR terdiri dari pemancar inframerah mikro (*IR emitter*), ruang tabung lintasan optik (*optical path chamber* berpanjang $L$), filter interferensi optik pita sempit $4{,}26,mu	ext{m}$, dan detektor termopile atau piroelektrik.
- **Hukum Beer-Lambert**: Hubungan antara intensitas cahaya yang ditransmisikan ($I$) terhadap intensitas awal tanpa gas penyerap ($I_0$):
$$
I = I_0 cdot e^{-alpha cdot C cdot L}
$$
di mana $alpha$ adalah koefisien absorpsi molekuler molar gas dan $C$ adalah konsentrasi gas dalam satuan parts-per-million ($	ext{ppm}$).
Dengan mengukur rasio transmisi $I / I_0$, konsentrasi $	ext{CO}_2$ dapat dihitung secara analitis:
$$
C = -rac{1}{alpha cdot L} lnleft( rac{I}{I_0} ight)
$$

### 2. Keterbatasan Sensor PIR & Fusi Radar Gelombang Milimeter (mmWave)
Sensor gerak inframerah pasif (*Passive Infrared* / PIR) mendeteksi perubahan diferensial radiasi panas tubuh manusia ($9 - 10,mu	ext{m}$) yang melintasi zona lensa Fresnel tersegmentasi:
- **Kelemahan Sensor PIR**: Hanya merespons gerakan makro dinamis (orang berjalan melintas). Ketika penghuni duduk diam bekerja di depan komputer atau membaca buku, fluks radiasi statis menyebabkan sensor PIR mati (*false-negative empty trigger*), mematikan lampu dan pendingin ruangan secara tidak diinginkan.
- **Radar mmWave Mikro-Gerak (24 GHz / 60 GHz FMCW)**: Memancarkan gelombang radar berfrekuensi sangat tinggi yang mampu mendeteksi pergeseran fase Doppler akibat gerakan mikroskopik dinding dada saat bernapas ($0{,}1 - 0{,}5	ext{ mm}$ displacement).
- **Fusi Multi-Modal**:
  - PIR digunakan untuk *fast-wakeup* instan saat pintu dibuka.
  - Radar mmWave mempertahankan *state presence* selama penghuni masih bernapas di dalam ruangan.

### 3. Standar ASHRAE 62.1 & Demand-Controlled Ventilation (DCV)
Standar ventilasi udara gedung komersial ASHRAE 62.1 menetapkan batasan kesehatan udara:
- Konsentrasi $	ext{CO}_2 < 800	ext{ ppm}$: Kualitas udara sangat baik, fungsi kognitif optimal.
- Konsentrasi $1000 - 1500	ext{ ppm}$: Rasa kantuk, penurunan konsentrasi kerja, ventilasi tidak memadai.
- Konsentrasi $> 2000	ext{ ppm}$: Sakit kepala, pusing, akumulasi aerosol patogen berbahaya.
Sistem DCV mengatur bukaan katup udara segar (*outdoor air damper* $0 - 100%$) secara proporsional terhadap konsentrasi $	ext{CO}_2$ aktual, menghemat energi pendinginan hingga $30%$ saat ruangan terisi sebagian.

### 4. Landasan Matematis: Penurunan Hukum Beer-Lambert & Persamaan Kesetimbangan Massa CO2

1. **Penurunan Formula Inversi Konsentrasi**:
   $$
   rac{I}{I_0} = exp(-alpha cdot C cdot L)
   $$
   $$
   lnleft( rac{I}{I_0} ight) = -alpha cdot C cdot L implies C(	ext{ppm}) = -rac{1}{alpha cdot L} lnleft( rac{I}{I_0} ight)
   $$

2. **Worked Numerical Example (Contoh Perhitungan Rinci)**:
   - **Karakteristik Sensor**:
     - Panjang lintasan optik: $L = 5{,}0	ext{ cm}$
     - Koefisien serapan NDIR: $alpha = 0{,}00045	ext{ ppm}^{-1}	ext{cm}^{-1}$
     - Intensitas referensi udara nol: $I_0 = 5000{,}0	ext{ ADC counts}$
     - Intensitas terukur saat ruangan berpenghuni: $I = 3850{,}0	ext{ ADC counts}$
   - **Langkah 1: Perhitungan Rasio Transmisi**:
     $$
     T = rac{3850}{5000} = 0{,}7700
     $$
   - **Langkah 2: Perhitungan Logaritma Natural**:
     $$
     ln(0{,}7700) = -0{,}26136
     $$
   - **Langkah 3: Perhitungan Konsentrasi CO2**:
     $$
     C = -rac{1}{0{,}00045 	imes 5{,}0} 	imes (-0{,}26136) = rac{0{,}26136}{0{,}00225} = 116{,}16	ext{ ppm di atas baseline}
     $$
     Dengan baseline atmosfer global $C_{	ext{base}} = 420	ext{ ppm}$, konsentrasi aktual ruangan adalah:
     $$
     C_{	ext{total}} = 420 + 116{,}2 = 536{,}2	ext{ ppm}
     $$
   - **Evaluasi DCV**: Karena $C_{	ext{total}} = 536{,}2	ext{ ppm} < 700	ext{ ppm}$, bukaan katup ventilasi diatur pada tingkat minimum $30%$ untuk menghemat energi pendingin udara.

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa sensor PIR tidak mampu mendeteksi orang yang sedang tertidur lelap di dalam ruangan, sementara radar mmWave mampu mendeteksinya?**
   - *Jawaban*: Sensor PIR hanya merespons perubahan fluks inframerah ketika sumber panas berpindah melintasi batas optik segmen lensa Fresnel yang berbeda. Orang yang tertidur lelap tidak menghasilkan perpindahan spasial tubuh. Sebaliknya, radar mmWave memancarkan gelombang elektromagnetik dan mendeteksi pergeseran fase mikroskopik ($< 0{,}5	ext{ mm}$) akibat gerakan naik-turun dinding dada saat bernapas.

2. **Bagaimana penerapan histeresis deadband melindungi aktuator katup ventilasi mekanikal?**
   - *Jawaban*: Histeresis mencegah osilasi buka-tutup berulang frekuensi tinggi (*actuator chattering*) di sekitar nilai ambang batas kendali, sehingga motor servo tidak terus-menerus bekerja bolak-balik saat fluktuasi derau pembacaan sensor bernilai kecil, memperpanjang usia mekanikal roda gigi aktuator.

## Tugas

## Penugasan Mandiri: Pemodelan Kontroler DCV Terintegrasi IAQ

Kembangkan simulator Python yang mengintegrasikan profil kedatangan 20 penghuni di ruang rapat selama 8 jam kerja. Simulasikan akumulasi $	ext{CO}_2$ berdasarkan laju pernapasan manusia dan buktikan algoritma DCV mempertahankan konsentrasi $< 800	ext{ ppm}$ dengan bukaan katup yang stabil.

## Ringkasan
- Modul A02 memberikan pemahaman mendalam dan terapan mengenai Occupancy Sensing, Environmental Conditioning & Indoor Air Quality (IAQ) pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [occupancy_iaq_dcv_sim.py](src/occupancy_iaq_dcv_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. ASHRAE Standard 62.1-2022, Ventilation for Acceptable Indoor Air Quality, [https://www.ashrae.org/technical-resources/standards-and-guidelines/read-only-versions-of-ashrae-standards](https://www.ashrae.org/technical-resources/standards-and-guidelines/read-only-versions-of-ashrae-standards) (diperiksa 2026-11-18).
2. Hodgkinson, J. and Tatam, R. P., Optical gas sensing: a review, Measurement Science and Technology, 2013, [https://doi.org/10.1088/0957-0233/24/1/012004](https://doi.org/10.1088/0957-0233/24/1/012004) (diperiksa 2026-11-18).

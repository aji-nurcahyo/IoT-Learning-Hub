# Modul B04 — Time & Frequency Domain Feature Engineering for Rotating Machinery

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menghitung fitur statistik domain waktu (Mean, RMS, Crest Factor, Kurtosis) untuk indikasi awal keausan mekanis.
2. Memahami keterbatasan FFT langsung terhadap benturan mikro lokal dan menerapkan Transformasi Hilbert untuk demodulasi selubung (Envelope Analysis).
3. Menurunkan rumus frekuensi karakteristik cacat mekanis bantalan (BPFO, BPFI, BSF, FTF) berdasarkan geometri fisik.
4. Membangun modul Python komparasi sinyal normal vs bantalan rusak dengan verifikasi spektral.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 05, Chapter 35.
- Modul Jalur Peminatan Prasyarat: Modul B02.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Fitur Statistik Domain Waktu
Dalam pemantauan kondisi mesin rotasi (*Condition-Based Monitoring*), fitur statistik domain waktu memberikan indikasi awal degradasi tanpa beban komputasi FFT yang berat:
- **RMS (Root Mean Square)**: Mencerminkan kandungan energi getaran total. Sangat efektif untuk memantau ketidakseimbangan massa (*unbalance*) atau misalignment poros.
- **Crest Factor**: Rasio nilai puncak (*Peak*) terhadap RMS. Sensitif terhadap lonjakan impulsif awal.
- **Kurtosis**: Momen sentral ke-4 ternormalisasi. Pada getaran acak normal (Gaussian), Kurtosis bernilai $approx 3{,}0$. Saat timbul keretakan mikro lokal pada lintasan bantalan, benturan berkala memicu lonjakan ekor distribusi sehingga Kurtosis melonjak drastis ($> 4{,}5$ hingga puluhan).

### 2. Analisis Spektrum Selubung (Envelope Analysis) & Transformasi Hilbert
Cacat lokal pada elemen bantalan menghasilkan rentetan pulsa impak mikro berdurasi sangat singkat yang membangkitkan resonansi alami struktur bearing/casing (frekuensi tinggi beberapa kHz). Jika dilakukan FFT langsung pada sinyal mentah, energi cacat ini tenggelam di bawah getaran harmonik poros dan noise mesin. **Transformasi Hilbert** mengekstraksi selubung amplitudo gelombang frekuensi tinggi termodulasi tersebut, sehingga saat selubung di-FFT, frekuensi pengulangan impak (BPFO/BPFI) tampak jelas sebagai garis spektral tajam.

### 3. Landasan Matematis: Formulasi Frekuensi Karakteristik Cacat Bantalan (Mathematical Foundations)

Berdasarkan geometri bantalan (jumlah elemen gelinding $n$, diameter bola $d$, diameter lingkaran pitch $D$, dan sudut kontak $eta$) pada kecepatan putar poros $f_r = 	ext{RPM}/60$:

1. **Frekuensi Cacat Cincin Luar (Ball Pass Frequency Outer Race / BPFO)**:
   $$
   	ext{BPFO} = rac{n}{2} cdot f_r left( 1 - rac{d}{D} cos eta ight)
   $$

2. **Frekuensi Cacat Cincin Dalam (Ball Pass Frequency Inner Race / BPFI)**:
   $$
   	ext{BPFI} = rac{n}{2} cdot f_r left( 1 + rac{d}{D} cos eta ight)
   $$

3. **Frekuensi Cacat Elemen Gelinding (Ball Spin Frequency / BSF)**:
   $$
   	ext{BSF} = rac{D}{2d} cdot f_r left( 1 - left( rac{d}{D} cos eta ight)^2 ight)
   $$

**Worked Numerical Example**:
Motor listrik berputar pada $1800	ext{ RPM}$ ($f_r = 30	ext{ Hz}$) memakai bantalan dengan $n = 9$ bola, $d = 7{,}94	ext{ mm}$, $D = 39{,}04	ext{ mm}$, dan $eta = 0^circ$.
$$
rac{d}{D} = rac{7{,}94}{39{,}04} approx 0{,}20338
$$
Kalkulasi frekuensi BPFO:
$$
	ext{BPFO} = rac{9}{2} 	imes 30 	imes (1 - 0{,}20338) = 135 	imes 0{,}79662 approx 107{,}54	ext{ Hz}
$$
Kalkulasi frekuensi BPFI:
$$
	ext{BPFI} = rac{9}{2} 	imes 30 	imes (1 + 0{,}20338) = 135 	imes 1{,}20338 approx 162{,}46	ext{ Hz}
$$
Ketika spektrum selubung sinyal getaran memperlihatkan puncak dominan pada $107{,}5	ext{ Hz}$, teknisi dapat menyimpulkan dengan kepastian tinggi bahwa kerusakan terlokalisasi pada cincin luar bantalan (*outer race flaw*).

## Latihan

### Soal 1: Analisis Kurtosis Sinyal Getaran (C3)
Diberikan rekaman getaran dengan deviasi standar $sigma = 0{,}15	ext{ g}$. Terjadi 5 lonjakan impak sebesar $2{,}5	ext{ g}$ dalam 1000 sampel. Hitung perkiraan lonjakan Kurtosis dan interpretasikan maknanya!

### Soal 2: Perhitungan BPFI Motor Pompa (C3)
Sebuah pompa sentrifugal berputar pada kecepatan 1500 RPM. Bantalan memiliki 8 bola berdiameter $10	ext{ mm}$ dan diameter pitch $50	ext{ mm}$ ($eta = 0^circ$). Hitung frekuensi BPFI dan BSF!

## Tugas

## Analisis Spektral & Diagnosis Kerusakan Bantalan Motor Induksi

Diberikan dataset getaran sintetis/rekaman akselerometer motor industri:
1. Hitung seluruh fitur domain waktu (Mean, RMS, Crest Factor, Kurtosis, Skewness).
2. Terapkan algoritma Transformasi Hilbert untuk membentuk sinyal selubung amplitudo.
3. Hitung FFT dari selubung dan bandingkan puncak spektral terhadap frekuensi teoritis BPFO dan BPFI.
4. Tulis laporan rekomendasi pemeliharaan berbasis data terhitung.

## Ringkasan
- Modul B04 memberikan pemahaman mendalam dan terapan mengenai Time & Frequency Domain Feature Engineering for Rotating Machinery pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [vibration_feature_envelope_sim.py](src/vibration_feature_envelope_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Randall, R. B., Vibration-based Condition Monitoring, Wiley, 2021, [https://www.wiley.com/en-us/Vibration+based+Condition+Monitoring-p-9781119477587](https://www.wiley.com/en-us/Vibration+based+Condition+Monitoring-p-9781119477587) (diperiksa 2026-11-18).
2. ISO 20816-3:2022 Measurement and evaluation of machine vibration — Industrial machinery, [https://www.iso.org/standard/79848.html](https://www.iso.org/standard/79848.html) (diperiksa 2026-11-18).

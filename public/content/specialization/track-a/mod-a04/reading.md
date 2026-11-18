# Modul A04 — Building Energy Optimization, Peak-Shaving & Sub-Metering

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menghitung nilai True RMS tegangan, arus, daya aktif (P), daya reaktif (Q), dan faktor daya (PF) pada beban non-linear gedung.
2. Memodelkan kurva beban harian gedung bertingkat dan mengidentifikasi penalti tarif daya semu (kVA).
3. Merancang algoritma pelepasan beban bertingkat (Load Shedding / Peak-Shaving) berbasis prioritas tier operasional.
4. Menghitung kompensasi kapasitas bank kapasitor untuk menaikkan Power Factor dari level induktif ke batas aman regulasi PLN/utility (PF >= 0.95).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 03, Chapter 21, Chapter 23.
- Modul Jalur Peminatan Prasyarat: Modul A01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Karakteristik Beban Listrik Gedung & Segitiga Daya
Dalam sistem kelistrikan gedung bertingkat komersial, beban listrik terbagi menjadi dua kategori utama:
1. **Beban Resistif Murni**: Pemanas air (*heater*), filamen lampu pijar (arus dan tegangan sefasa, $	ext{PF} = 1{,}0$).
2. **Beban Induktif & Non-Linear**: Motor induksi kompresor pendingin udara (chiller/HVAC), pompa air sirkulasi, ballast lampu fluorescent, dan catu daya switching komputer server (arus tertinggal dari tegangan / *lagging current*).

Hubungan antara daya nyata, daya reaktif, dan daya semu dirumuskan dalam **Segitiga Daya**:
- **Daya Aktif ($P$, kW)**: Energi riil yang dikonversi menjadi kerja mekanik atau panas.
- **Daya Reaktif ($Q$, kVAR)**: Energi osilasi bolak-balik yang dibutuhkan untuk membangkitkan medan magnet pada kumparan motor.
- **Daya Semu ($S$, kVA)**: Total daya resultan yang harus dialirkan oleh trafo dan jaringan kabel PLN:
$$
S = sqrt{P^2 + Q^2}
$$
- **Faktor Daya (Power Factor / $	ext{PF}$)**: Rasio efisiensi pemanfaatan daya semu:
$$
	ext{PF} = rac{P}{S} = cos(phi)
$$

### 2. Penalti Biaya KVARh & Kompensasi Bank Kapasitor
Penyedia utilitas listrik (seperti PLN) mengenakan tarif penalti biaya kelebihan pemakaian daya reaktif jika faktor daya rata-rata pelanggan industri/bisnis berada di bawah batas regulasi ($	ext{PF} < 0{,}85$ atau $0{,}90$).
- Untuk menaikkan $	ext{PF}$ dari $cos(phi_1)$ ke target $cos(phi_2) ge 0{,}95$, bank kapasitor dipasang secara paralel untuk menyuplai daya reaktif kapasitif yang meniadakan arus reaktif induktif motor:
$$
Q_{	ext{cap}}(	ext{kVAR}) = P cdot left[ 	an(phi_1) - 	an(phi_2) ight]
$$

### 3. Pemangkasan Beban Puncak (Peak-Shaving) & Demand Response
Gedung komersial memiliki kontrak daya maksimum ($P_{	ext{contract}}$). Jika lonjakan serentak kompresor AC menyebabkan beban melebihi daya kontrak bahkan selama 15 menit saja, pengelola gedung dikenakan denda penalti lonjakan daya semu (*maximum demand surcharge*) yang sangat mahal.
- **Klasifikasi Beban Bertingkat (Tiered Shedding)**:
  - **Tier 1 (Critical)**: Lampu darurat, elevator darurat, server data room (tidak boleh dipadamkan).
  - **Tier 2 (Essential)**: Pendingin ruang kerja utama, pencahayaan umum kantor.
  - **Tier 3 (Sheddable / Non-Kritis)**: Water heater toilet, chiller cadangan, pendingin koridor dan lobi.
- Sistem sub-metering IoT secara real-time memproyeksikan akumulasi beban dan secara otomatis menonaktifkan beban Tier 3 saat $P_{	ext{total}} > 0{,}90 cdot P_{	ext{contract}}$.

### 4. Landasan Matematis: Kalkulasi Segitiga Daya & Bank Kapasitor

1. **Penjumlahan Vektor Daya Multi-Beban**:
   $$
   P_{	ext{total}} = sum_{i=1}^{M} P_i, quad Q_{	ext{total}} = sum_{i=1}^{M} P_i cdot 	anleft( arccos(	ext{PF}_i) ight)
   $$
   $$
   S_{	ext{total}} = sqrt{P_{	ext{total}}^2 + Q_{	ext{total}}^2}, quad 	ext{PF}_{	ext{system}} = rac{P_{	ext{total}}}{S_{	ext{total}}}
   $$

2. **Worked Numerical Example (Kasus Gedung Perkantoran)**:
   - **Komposisi Beban Terukur**:
     - Chiller HVAC: $P_1 = 60{,}0	ext{ kW}$, $	ext{PF}_1 = 0{,}82$ ($phi_1 = 34{,}9^circ implies 	anphi_1 = 0{,}698$)
       $$
       Q_1 = 60 	imes 0{,}698 = 41{,}88	ext{ kVAR}
       $$
     - Komputer & Penerangan: $P_2 = 25{,}0	ext{ kW}$, $	ext{PF}_2 = 0{,}92$ ($phi_2 = 23{,}07^circ implies 	anphi_2 = 0{,}426$)
       $$
       Q_2 = 25 	imes 0{,}426 = 10{,}65	ext{ kVAR}
       $$
     - Chiller Sekunder: $P_3 = 20{,}0	ext{ kW}$, $	ext{PF}_3 = 0{,}75$ ($phi_3 = 41{,}4^circ implies 	anphi_3 = 0{,}882$)
       $$
       Q_3 = 20 	imes 0{,}882 = 17{,}64	ext{ kVAR}
       $$
   - **Langkah 1: Akumulasi Daya Total**:
     $$
     P_{	ext{total}} = 60 + 25 + 20 = 105{,}0	ext{ kW}
     $$
     $$
     Q_{	ext{total}} = 41{,}88 + 10{,}65 + 17{,}64 = 70{,}17	ext{ kVAR}
     $$
     $$
     S_{	ext{total}} = sqrt{105{,}0^2 + 70{,}17^2} = sqrt{11025 + 4923{,}8} = sqrt{15948{,}8} = 126{,}29	ext{ kVA}
     $$
     $$
     	ext{PF}_{	ext{system}} = rac{105{,}0}{126{,}29} = 0{,}8314 quad (	ext{Terkena denda PLN karena } < 0{,}85)
     $$
   - **Langkah 2: Perhitungan Kompensasi Kapasitor ke $	ext{PF} = 0{,}95$**:
     - Sudut target: $phi_{	ext{target}} = arccos(0{,}95) = 18{,}19^circ implies 	anphi_{	ext{target}} = 0{,}3287$
     - Sudut sistem saat ini: $phi_{	ext{sys}} = arccos(0{,}8314) = 33{,}76^circ implies 	anphi_{	ext{sys}} = 0{,}6685$
     - Kapasitas bank kapasitor:
       $$
       Q_{	ext{cap}} = 105{,}0 	imes (0{,}6685 - 0{,}3287) = 105{,}0 	imes 0{,}3398 = 33{,}68	ext{ kVAR}
       $$
   - **Langkah 3: Pemangkasan Beban Puncak (Peak Shaving)**:
     - Batas kontrak: $P_{	ext{contract}} = 100	ext{ kW}$. Beban awal $105	ext{ kW} > 100	ext{ kW}$.
     - Pelepasan beban Tier 3 sebesar $15	ext{ kW}$ menurunkan beban akhir ke $90	ext{ kW}$, mengamankan instalasi dari trip MCB dan denda beban puncak.

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa nilai Power Factor yang rendah ($	ext{PF} < 0{,}85$) merugikan baik bagi pihak pengelola gedung maupun penyedia utilitas listrik?**
   - *Jawaban*: Power Factor rendah berarti arus bolak-balik yang mengalir di kabel jauh lebih besar untuk menghasilkan daya aktif yang sama ($I = S / V$). Arus tinggi menimbulkan rugi disipasi panas kabel ($I^2 R$) yang tinggi, penurunan tegangan (*voltage drop*), pemborosan kapasitas trafo utilitas, dan memicu tagihan denda kVARh bulanan yang mahal.

2. **Apa perbedaan antara strategi konservasi energi (*Energy Efficiency*) dan pemangkasan beban puncak (*Peak-Shaving*)?**
   - *Jawaban*: Efisiensi energi berfokus pada pengurangan konsumsi energi total sepanjang waktu (kWh kumulatif), sedangkan peak-shaving berfokus pada pengendalian daya sesaat (kW/kVA puncak) pada jendela waktu tertentu untuk mencegah penalti lonjakan daya kontrak trafo, meskipun konsumsi energi total mungkin hanya digeser ke jam lain.

## Tugas

## Penugasan Mandiri: Pemodelan Profil Beban 24 Jam & Peak-Shaving

Kembangkan modul Python yang membaca profil konsumsi daya gedung 24 jam dengan interval 15 menit. Terapkan algoritma pelepasan beban bertingkat Tier 3 saat daya mendekati batas kontrak 100 kW dan hitung estimasi penghematan denda daya semu.

## Ringkasan
- Modul A04 memberikan pemahaman mendalam dan terapan mengenai Building Energy Optimization, Peak-Shaving & Sub-Metering pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [building_energy_peakshaving_sim.py](src/building_energy_peakshaving_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. IEC 62053-21:2020, Electricity metering equipment — Particular requirements, [https://webstore.iec.ch/publication/62095](https://webstore.iec.ch/publication/62095) (diperiksa 2026-11-18).
2. IEEE Std 1459-2010, IEEE Standard Definitions for the Measurement of Electric Power Quantities, [https://standards.ieee.org/ieee/1459/4405/](https://standards.ieee.org/ieee/1459/4405/) (diperiksa 2026-11-18).

# Modul C04 — Energy Harvesting, Solar Irradiance Profiling & Supercapacitor Dimensioning

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menghitung profil daya masukan sel surya monokristalin berdasarkan data insolasi harian jam-jaman (PSH).
2. Menganalisis efisiensi konverter pemanen energi mikro berbasis Maximum Power Point Tracking (MPPT).
3. Menghitung kapasitas superkapasitor (Farad) dan baterai LiFePO4 untuk memenuhi kriteria 7 hari otonomi tanpa sinar matahari.
4. Memvalidasi anggaran energi siklus tugas (duty cycle) transmisi LoRaWAN terhadap kapasitas penyimpanan.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 03, Chapter 31.
- Modul Jalur Peminatan Prasyarat: Modul C01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Dinamika Pemanenan Energi Mikro Luar Ruangan
Node sensor pertanian terpencil diwajibkan beroperasi selama bertahun-tahun tanpa penggantian baterai fisik. Pemanenan energi surya (*photovoltaic harvesting*) skala mikro memanfaatkan modul PV kompak ($10 \times 15\text{ cm}$) yang menghasilkan daya fluktuatif tergantung profil insolasi harian jam-jaman (*Peak Sun Hours* / PSH).

Tiga subsistem kritis dalam arsitektur catu daya mandiri (*energy-neutral architecture*):
1. **Modul Fotovoltaik & Pelacak Titik Daya Maksimum (MPPT)**: Karakteristik kurva $I-V$ sel surya bersifat non-linear di mana daya puncak ($P_{\text{MPP}}$) bergeser mengikuti fluktuasi intensitas radiasi dan temperatur silikon. Sirkuit konverter buck-boost terintegrasi (seperti TI BQ25570 atau SPV1040) mengeksekusi algoritma *Perturb & Observe* (P&O) atau pelacakan fraksi tegangan terbuka ($V_{\text{OC}}$) dengan efisiensi konversi $\ge 90\%$.
2. **Penyimpan Energi Buffer Sekunder**:
   - **Superkapasitor (EDLC - Electric Double-Layer Capacitor)**: Siklus hidup masif ($> 500.000$ siklus), mampu menyuplai arus lonjakan (*burst current*) transmisi radio tanpa degradasi internal, namun memiliki densitas energi volumetrik rendah dan laju kebocoran (*self-discharge*) tinggi.
   - **Sel Baterai Lithium Besi Fosfat (LiFePO4)**: Densitas energi tinggi, profil pelepasan muatan sangat datar pada tegangan $3{,}2\text{ V}$, dan stabilitas termal kimiawi yang unggul pada lingkungan perkebunan tropis ($> 45^\circ\text{C}$) dibanding Li-ion konvensional.

### 2. Metodologi Dimensi Superkapasitor untuk Transmisi Burst
Saat mikrokontroler bangkit dari mode deep sleep dan mengaktifkan penguat daya radio transmisi LoRa ($+14\text{ dBm}$ hingga $+20\text{ dBm}$), tarikan arus melonjak seketika dari $8\,\mu\text{A}$ ke $120\text{ mA}$ selama durasi time-on-air $t_{\text{burst}} \approx 2{,}5\text{ detik}$. Superkapasitor buffer harus mampu menopang lonjakan energi tersebut tanpa menyebabkan tegangan bus turun di bawah batas reset mikrokontroler ($V_{\text{BOD}} = 2{,}7\text{ V}$):
$$
E_{\text{burst}} = V_{\text{sys}} \cdot I_{\text{tx}} \cdot t_{\text{tx}}
$$
$$
C_{\text{min}} = \frac{2 \cdot E_{\text{burst}}}{\eta_{\text{conv}} \left( V_{\text{max}}^2 - V_{\text{min}}^2 \right)}
$$

### 3. Landasan Matematis: Neraca Energi Harian & 7 Hari Otonomi

1. **Persamaan Keseimbangan Energi Harian**:
   $$
   E_{\text{harvested}} = \int_{0}^{24} G(t) \cdot A_{\text{pv}} \cdot \eta_{\text{pv}} \cdot \eta_{\text{mppt}} \, dt
   $$
   Node memenuhi syarat netralitas energi (*Energy Neutrality Condition*) jika:
   $$
   E_{\text{harvested}} \ge E_{\text{consumed}} + E_{\text{leakage}}
   $$

2. **Worked Numerical Example (Contoh Perhitungan Dimensi Catu Daya)**:
   - **Profil Beban Node**:
     - Tegangan sistem: $V_{\text{sys}} = 3{,}3\text{ V}$
     - Arus aktif (baca sensor + DSP): $I_{\text{active}} = 35\text{ mA}$, durasi $10\text{ detik/jam}$
     - Arus sleep: $I_{\text{sleep}} = 8\,\mu\text{A}$ ($0{,}008\text{ mA}$)
     - Arus burst radio LoRa: $I_{\text{burst}} = 120\text{ mA}$, durasi $2{,}5\text{ detik}$
   - **Konsumsi Energi Harian**:
     - Waktu aktif total per hari: $t_{\text{act}} = 24 \times 10 = 240\text{ detik}$
     - Waktu sleep total: $t_{\text{slp}} = 86400 - 240 = 86160\text{ detik}$
     - Energi harian:
       $$
       E_{\text{active}} = 3{,}3 \times 0{,}035 \times 240 = 27{,}72\text{ Joule}
       $$
       $$
       E_{\text{sleep}} = 3{,}3 \times (8 \times 10^{-6}) \times 86160 = 2{,}27\text{ Joule}
       $$
       $$
       E_{\text{daily}} = 27{,}72 + 2{,}27 = 29{,}99\text{ Joule} = \frac{29{,}99}{3{,}6} = 8{,}33\text{ mWh}
       $$
   - **Dimensi Superkapasitor Buffer**:
     - Energi burst: $E_{\text{burst}} = 3{,}3 \times 0{,}120 \times 2{,}5 = 0{,}99\text{ Joule}$
     - Tegangan kerja superkapasitor: $V_{\text{max}} = 5{,}0\text{ V}$, $V_{\text{min}} = 3{,}0\text{ V}$, efisiensi regulator $\eta = 0{,}85$:
       $$
       C = \frac{2 \times 0{,}99}{0{,}85 \times (5{,}0^2 - 3{,}0^2)} = \frac{1{,}98}{0{,}85 \times 16{,}0} = \frac{1{,}98}{13{,}6} = 0{,}1456\text{ Farad}
       $$
       Dipilih nilai standar komersial: **Superkapasitor 0.15 F atau 0.22 F / 5.5 V**.
   - **Dimensi Baterai Otonomi 7 Hari (Kondisi Mendung Ekstrem)**:
     - Kebutuhan energi 7 hari tanpa sinar matahari dengan Depth of Discharge (DoD) $80\%$:
       $$
       E_{\text{storage}} = \frac{8{,}33\text{ mWh/hari} \times 7\text{ hari}}{0{,}80} = \frac{58{,}31}{0{,}80} = 72{,}89\text{ mWh}
       $$
     - Kapasitas mAh sel LiFePO4 ($V_{\text{cell}} = 3{,}2\text{ V}$):
       $$
       Q = \frac{72{,}89\text{ mWh}}{3{,}2\text{ V}} = 22{,}78\text{ mAh}
       $$
       Bahkan sebuah sel standar LiFePO4 18650 kapasitas $1500\text{ mAh}$ mampu menyediakan otonomi mendung teoritis lebih dari **400 hari**.

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa teknologi baterai Lithium Iron Phosphate ($	ext{LiFePO}_4$) lebih dipilih untuk stasiun IoT pertanian tropis dibandingkan Lithium-Cobalt Oxide ($	ext{LiCoO}_2$)?**
   - *Jawaban*: Sel $	ext{LiFePO}_4$ memiliki ikatan kimia kovalen $	ext{P}-	ext{O}$ yang jauh lebih stabil, tahan terhadap suhu tinggi hingga $60^circ	ext{C}$ tanpa resiko *thermal runaway* (terbakar/meledak di bawah sinar matahari langsung), memiliki siklus hidup lebih panjang ($> 2000$ siklus), dan kurva pelepasan tegangan yang sangat datar di sekitar $3{,}2	ext{ V}$.

2. **Apa yang menyebabkan osilasi brownout pada mikrokontroler saat catu daya kekurangan daya penyimpan?**
   - *Jawaban*: Saat mikrokontroler bangun dari mode sleep dan memulai transmisi, arus meningkat tajam sehingga resistansi internal sumber daya memicu penurunan tegangan di bawah ambang batas *Brownout Detector* (BOD). Mikrokontroler reset seketika, arus turun, tegangan naik kembali, mikrokontroler bangun lagi, dan siklus kegagalan ini berulang tanpa akhir hingga baterai rusak total.

## Tugas

## Penugasan Mandiri: Pemodelan Profil Pemanenan Energi & Otonomi

Kembangkan simulator Python yang memodelkan aliran energi harian simpul sensor selama 30 hari menggunakan dataset insolasi sintetis yang memuat periode mendung 7 hari berurutan. Buktikan bahwa tegangan baterai tidak pernah menyentuh level cutoff BOD.

## Ringkasan
- Modul C04 memberikan pemahaman mendalam dan terapan mengenai Energy Harvesting, Solar Irradiance Profiling & Supercapacitor Dimensioning pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [solar_energy_harvesting_sim.py](src/solar_energy_harvesting_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Roundy, S. et al., Energy Scavenging for Wireless Sensor Networks, Springer, 2004, [https://doi.org/10.1007/978-1-4615-0485-6](https://doi.org/10.1007/978-1-4615-0485-6) (diperiksa 2026-11-18).
2. Texas Instruments, BQ25570 Nano Power Boost Charger with Integrated Buck Converter, [https://www.ti.com/product/BQ25570](https://www.ti.com/product/BQ25570) (diperiksa 2026-11-18).

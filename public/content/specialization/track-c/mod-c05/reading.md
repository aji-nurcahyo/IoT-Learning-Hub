# Modul C05 — Evapotranspiration Analytics, FAO-56 Penman-Monteith & Precision Irrigation

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menghitung evapotranspirasi acuan (ET0) harian menggunakan formulasi lengkap FAO-56 Penman-Monteith.
2. Memetakan dinamika koefisien tanaman (Kc) sepanjang fase vegetatif hingga pematangan panen.
3. Mengimplementasikan model neraca air zona perakaran (Soil Water Depletion) harian.
4. Merancang algoritma aktuasi irigasi otomatis berbasis batas penipisan terkelola (Management Allowed Depletion / MAD).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 21, Chapter 23, Chapter 26.
- Modul Jalur Peminatan Prasyarat: Modul C01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Prinsip Dasar Evapotranspirasi Standar FAO-56
Evapotranspirasi merupakan kombinasi dari dua proses fisik terpisah: penguapan air dari permukaan tanah terbuka (*evaporation*) dan pelepasan uap air melalui stomata daun tanaman (*transpiration*). Untuk standarisasi kebutuhan air tanaman secara global, Organisasi Pangan dan Pertanian PBB (FAO) melalui Paper Irigasi No. 56 menetapkan konsep **Evapotranspirasi Acuan ($	ext{ET}_0$)**:
- Tanaman acuan didefinisikan sebagai hamparan rumput hijau hipotetis dengan tinggi seragam $0{,}12	ext{ m}$, resistansi permukaan tajuk kanopi $r_s = 70	ext{ s/m}$, dan albedo refleksi radiasi matahari $alpha = 0{,}23$.
- Nilai $	ext{ET}_0$ mencerminkan daya evaporatif atmosfer murni tanpa memperhitungkan jenis tanaman aktual maupun defisit air tanah.

### 2. Formulasi Penman-Monteith FAO-56
Persamaan FAO-56 Penman-Monteith mengintegrasikan hukum termodinamika kesetimbangan energi radiasi permukaan dan hukum aerodinamika transpor turbulen massa uap air:
$$
	ext{ET}_0 = rac{0{,}408 Delta (R_n - G) + gamma rac{900}{T + 273} u_2 (e_s - e_a)}{Delta + gamma (1 + 0{,}34 u_2)}
$$
Komponen fisik dalam persamaan:
- $R_n$: Radiasi netto pada permukaan tanaman ($	ext{MJ/m}^2/	ext{hari}$).
- $G$: Fluks panas konduksi tanah ($	ext{MJ/m}^2/	ext{hari}$, bernilai $approx 0$ untuk perhitungan skala harian).
- $T$: Suhu rata-rata harian udara pada ketinggian 2 meter ($^circ	ext{C}$).
- $u_2$: Kecepatan angin horizontal pada ketinggian 2 meter ($	ext{m/s}$).
- $(e_s - e_a)$: Defisit tekanan uap jenuh atmosfer (*Vapor Pressure Deficit* / VPD) ($	ext{kPa}$).
- $Delta$: Kemiringan kurva tekanan uap jenuh terhadap suhu ($	ext{kPa/}^circ	ext{C}$).
- $gamma$: Konstanta psikrometrik atmosfer ($	ext{kPa/}^circ	ext{C}$).

### 3. Koefisien Tanaman ($K_c$) & Neraca Air Tanah
Evapotranspirasi tanaman aktual ($	ext{ET}_c$) dihitung dengan mengalikan $	ext{ET}_0$ dengan koefisien tanaman $K_c$:
$$
	ext{ET}_c = K_c cdot 	ext{ET}_0
$$
Nilai $K_c$ berkembang dinamis melintasi 4 tahap pertumbuhan: tahap awal (*initial stage* $K_c approx 0{,}3 - 0{,}5$), tahap vegetatif (*crop development*), tahap pertengahan/pembungaan (*mid-season* $K_c approx 1{,}05 - 1{,}20$), dan tahap akhir pematangan (*late-season* $K_c approx 0{,}6 - 0{,}8$).

### 4. Landasan Matematis: Persamaan Psikrometrik & Keputusan Irigasi Presisi

1. **Persamaan Tekanan Uap Jenuh Tetens ($e_s$)**:
   $$
   e_s(T) = 0{,}6108 \exp\left( \frac{17{,}27 \cdot T}{T + 237{,}3} \right)
   $$
   Tekanan uap aktual: $e_a = e_s \cdot \frac{\text{RH}}{100}$.

2. **Kemiringan Kurva Tekanan Uap ($\Delta$)**:
   $$
   \Delta = \frac{4098 \cdot e_s(T)}{(T + 237{,}3)^2}
   $$

3. **Worked Numerical Example (Contoh Perhitungan Lengkap)**:
   - **Data Masukan Meteorologi**:
     - Suhu rata-rata: $T = 28{,}0^\circ\text{C}$
     - Radiasi netto: $R_n = 16{,}5\text{ MJ/m}^2/\text{hari}$ ($G = 0$)
     - Kecepatan angin: $u_2 = 1{,}8\text{ m/s}$
     - Kelembaban relatif: $\text{RH} = 70\%$
     - Konstanta psikrometrik: $\gamma = 0{,}065\text{ kPa/}^\circ\text{C}$
   - **Langkah 1: Perhitungan $e_s$, $e_a$, dan VPD**:
     $$
     e_s = 0{,}6108 \exp\left( \frac{17{,}27 \times 28}{265{,}3} \right) = 0{,}6108 \exp(1{,}8227) = 3{,}779\text{ kPa}
     $$
     $$
     e_a = 3{,}779 \times 0{,}70 = 2{,}645\text{ kPa} \implies (e_s - e_a) = 1{,}134\text{ kPa}
     $$
   - **Langkah 2: Perhitungan Kemiringan $\Delta$**:
     $$
     \Delta = \frac{4098 \times 3{,}779}{(28 + 237{,}3)^2} = \frac{15486{,}3}{70384{,}3} = 0{,}2200\text{ kPa/}^\circ\text{C}
     $$
   - **Langkah 3: Perhitungan Suku Radiasi & Aerodinamika**:
     $$
     \text{Suku Radiasi} = 0{,}408 \times 0{,}2200 \times 16{,}5 = 1{,}481\text{ mm/hari}
     $$
     $$
     \text{Suku Aerodinamika} = 0{,}065 \times \left( \frac{900}{301} \right) \times 1{,}8 \times 1{,}134 = 0{,}065 \times 2{,}990 \times 2{,}041 = 0{,}397\text{ mm/hari}
     $$
     $$
     \text{Penyebut} = 0{,}2200 + 0{,}065 \times (1 + 0{,}34 \times 1{,}8) = 0{,}2200 + 0{,}065 \times 1{,}612 = 0{,}2200 + 0{,}1048 = 0{,}3248
     $$
     $$
     \text{ET}_0 = \frac{1{,}481 + 0{,}397}{0{,}3248} = \frac{1{,}878}{0{,}3248} = 4{,}54\text{ mm/hari}
     $$
   - **Langkah 4: Keputusan Irigasi Presisi**:
     - Untuk tanaman jagung fase pembungaan ($K_c = 1{,}15$): $\text{ET}_c = 1{,}15 \times 4{,}54 = 5{,}22\text{ mm/hari}$.
     - Dengan kedalaman perakaran $Z_r = 0{,}5\text{ m}$, $\theta_{\text{FC}} = 0{,}28$, $\theta_{\text{PWP}} = 0{,}12$:
       $$
       \text{TAW} = 1000 \times (0{,}28 - 0{,}12) \times 0{,}5 = 80\text{ mm}
       $$
     - Kebutuhan air $5{,}22\text{ mm/hari}$ setara dengan debit $5{,}22\text{ Liter/m}^2$. Dengan emitter tetes $4\text{ L/jam}$, durasi bukaan katup solenoid adalah:
       $$
       t = \frac{5{,}22\text{ L}}{4{,}0\text{ L/jam}} = 1{,}305\text{ jam} = 78{,}3\text{ menit}
       $$

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa nilai fluks panas konduksi tanah ($G$) sering diasumsikan bernilai nol ($G approx 0$) pada perhitungan evapotranspirasi skala harian?**
   - *Jawaban*: Pada siklus 24 jam penuh, panas radiasi yang diserap tanah pada siang hari dilepaskan kembali secara proporsional ke atmosfer pada malam hari, sehingga perpindahan panas netto harian ke lapisan tanah dalam sangat kecil dan dapat diabaikan dibanding besarnya radiasi netto $R_n$.

2. **Apa yang dimaksud dengan batas penipisan air tanah terkelola ($Management Allowed Depletion$ / MAD)?**
   - *Jawaban*: MAD adalah fraksi dari Total Air Tersedia (TAW)—umumnya berkisar antara $40% - 50%$—yang diizinkan untuk diserap tanaman sebelum tanaman mengalami stres fisiologis atau penurunan laju fotosintesis, berfungsi sebagai ambang batas kritis pemicu aktuasi irigasi.

## Tugas

## Penugasan Mandiri: Kalkulator Neraca Air FAO-56 & Penjadwalan Irigasi

Kembangkan modul Python yang membaca data meteorologi harian selama satu musim tanam (120 hari). Terapkan algoritma FAO-56 dan koefisien tanaman dinamis untuk menghasilkan log penjadwalan irigasi tetes otomatis.

## Ringkasan
- Modul C05 memberikan pemahaman mendalam dan terapan mengenai Evapotranspiration Analytics, FAO-56 Penman-Monteith & Precision Irrigation pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [fao56_evapotranspiration_sim.py](src/fao56_evapotranspiration_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Allen, R. G. et al., Crop Evapotranspiration — Guidelines for Computing Crop Water Requirements — FAO Irrigation and Drainage Paper 56, FAO, 1998, [https://www.fao.org/land-water/databases-and-software/cropwat/en/](https://www.fao.org/land-water/databases-and-software/cropwat/en/) (diperiksa 2026-11-18).
2. ASCE-EWRI, The ASCE Standardized Reference Evapotranspiration Equation, ASCE, 2005, [https://ascelibrary.org/doi/book/10.1061/9780784408056](https://ascelibrary.org/doi/book/10.1061/9780784408056) (diperiksa 2026-11-18).

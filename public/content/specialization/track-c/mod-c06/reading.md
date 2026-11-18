# Modul C06 — Autonomous LoRaWAN Agricultural Microclimate Network (Capstone Project)

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. SATC-C01: Memvalidasi kestabilan kalibrasi sensor kelembaban tanah in-situ terhadap fluktuasi suhu (|delta theta| <= 1.5% VWC).
2. SATC-C02: Membuktikan link budget LoRaWAN menembus tajuk kanopi 50 meter pada jarak 3.5 km dengan Packet Delivery Ratio (PDR) >= 95%.
3. SATC-C03: Memverifikasi otonomi sistem catu daya surya & baterai selama 168 jam kondisi mendung total tanpa kegagalan brownout.
4. SATC-C04: Menghasilkan rekomendasi irigasi presisi FAO-56 loop tertutup tanpa deep percolation.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 30, Chapter 40.
- Modul Jalur Peminatan Prasyarat: Modul C01, Modul C02, Modul C03, Modul C04, Modul C05.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Visi Arsitektur Capstone Track C: Jaringan Mikroklimat Pertanian Cerdas
Jaringan pertanian cerdas berbasis IoT memerlukan perpaduan multi-disiplin: ilmu fisika tanah, meteorologi terapan, elektronika pemanen energi berdaya ultra-rendah, dan teknik transmisi radio sub-GHz jarak jauh.

Sistem capstone ini mengintegrasikan stasiun cuaca in-situ nirkabel yang mengukur parameter tanah bertingkat dan dinamika iklim mikro, mentransmisikan data melalui tautan radio LoRaWAN melintasi tajuk kanopi perkebunan lebat, serta mengeksekusi analitika neraca air tanah FAO-56 untuk mengatur irigasi presisi secara mandiri.

### 2. Evaluasi Skenario Uji Penerimaan Sistem (SATC)
Platform capstone divalidasi berdasarkan 4 kriteria penerimaan kuantitatif ketat:
1. **SATC-C01 (Kestabilan Termal Kalibrasi Tanah)**: Pengukuran kadar air volumetrik tanah terkompensasi suhu wajib mempertahankan akurasi dengan simpangan $|Delta 	heta| le 1{,}5%	ext{ VWC}$ melintasi rentang temperatur $20^circ	ext{C}$ hingga $42^circ	ext{C}$.
2. **SATC-C02 (Verifikasi Link Budget Kanopi)**: Transmisi paket LoRaWAN pada jarak $3{,}5	ext{ km}$ melintasi tajuk pohon sawit setebal $50	ext{ meter}$ wajib memiliki Packet Delivery Ratio (PDR) $ge 95%$.
3. **SATC-C03 (Stres Otonomi Daya 7 Hari)**: Node wajib mempertahankan operasional normal tanpa terjadi brownout reset selama $168	ext{ jam}$ kontinu di bawah kondisi mendung total ($0	ext{ W}$ solar input).
4. **SATC-C04 (Keputusan Irigasi Presisi FAO-56)**: Volume air irigasi yang disuplai mengembalikan kadar air tanah tepat ke kapasitas lapang tanpa menimbulkan perkolasi dalam (*deep percolation* $= 0$).

### 3. Landasan Matematis: Integrasi Neraca Air & Model Link Budget

1. **Model Neraca Air Zona Perakaran Tanaman**:
   $$
   D_{r,i} = D_{r,i-1} - (P_i - \text{RO}_i) - I_i + \text{ET}_{c,i} + \text{DP}_i
   $$
   di mana $D_r$ adalah penipisan air tanah, $P$ curah hujan, $I$ irigasi, $\text{ET}_c$ evapotranspirasi tanaman, dan $\text{DP}$ perkolasi dalam air gravitasi.

2. **Kondisi Batas Tanpa Pemborosan Air**:
   Irigasi presisi optimal mensyaratkan:
   $$
   I_i = D_{r,i-1} \implies D_{r,i} = 0 \quad \text{dan} \quad \text{DP}_i = 0
   $$

3. **Margin Fading Tautan Nirkabel**:
   $$
   \text{Link Margin} = P_{\text{Tx}} + G_{\text{Tx}} + G_{\text{Rx}} - L_{\text{FSPL}}(3{,}5\text{ km}) - L_{\text{veg}}(50\text{ m}) - S_{\text{SF10}} \ge +10\text{ dB}
   $$

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa kondisi perkolasi dalam bernilai nol ($Deep Percolation = 0$) dijadikan salah satu indikator keberhasilan utama irigasi presisi?**
   - *Jawaban*: Nilai perkolasi dalam nol membuktikan bahwa volume air yang disuplai oleh sistem irigasi tepat memenuhi defisit kelembaban di zona perakaran tanaman tanpa ada air berlebih yang terbuang sia-sia ke lapisan tanah yang lebih dalam di bawah jangkauan akar, menghemat air dan mencegah pencucian nutrisi pupuk (*nutrient leaching*).

2. **Bagaimana sistem membuktikan ketahanan terhadap kondisi cuaca ekstrem selama 7 hari tanpa sinar matahari?**
   - *Jawaban*: Melalui pengujian stres SATC-C03 di mana konsumsi energi harian simpul ($8{,}33	ext{ mWh/hari}$) disimulasikan selama 168 jam kontinu ($58{,}31	ext{ mWh}$ total), dan kapasitas baterai LiFePO4 terbukti masih menyisakan lebih dari $90%$ cadangan energi tanpa menyentuh ambang batas proteksi undervoltage.

## Tugas

## Penugasan Mandiri: Evaluasi Kinerja Capstone Jaringan Mikroklimat Pertanian

Tulis laporan evaluasi rekayasa formal yang merangkum hasil verifikasi SATC-C01 hingga SATC-C04. Sertakan grafik neraca energi baterai selama 7 hari mendung dan plot respons kadar air tanah sebelum dan sesudah aktuasi irigasi otomatis.

## Ringkasan
- Modul C06 memberikan pemahaman mendalam dan terapan mengenai Autonomous LoRaWAN Agricultural Microclimate Network (Capstone Project) pada tingkat kedalaman L4: Research Preparation.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [agricultural_capstone_network_sim.py](src/agricultural_capstone_network_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. WMO-No. 8, Guide to Instruments and Methods of Observation, World Meteorological Organization, 2021, [https://community.wmo.int/en/activity-areas/imop/wmo-no_8](https://community.wmo.int/en/activity-areas/imop/wmo-no_8) (diperiksa 2026-11-18).
2. FAO Irrigation and Drainage Paper 56, Guidelines for computing crop water requirements, Rome, 1998, [https://www.fao.org/land-water/databases-and-software/cropwat/en/](https://www.fao.org/land-water/databases-and-software/cropwat/en/) (diperiksa 2026-11-18).

# Modul A06 — Autonomous Micro-Climate & Demand-Response Building Controller (Capstone Project)

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. SATC-A01: Mengoperasikan kendali ventilasi closed-loop IAQ dengan respons waktu <= 5 detik saat konsentrasi CO2 meningkat tanpa chattering.
2. SATC-A02: Membuktikan ketahanan kendali lokal Thread mesh (Packet Delivery Ratio 100% dan latensi < 50 ms) saat koneksi WAN internet terputus total.
3. SATC-A03: Memverifikasi aktuasi otomatis peak-shaving yang menurunkan beban gedung ke bawah batas kontrak dalam waktu <= 3 detik tanpa trip MCB.
4. SATC-A04: Memvalidasi interlock keselamatan darurat (fail-safe door unlocked dan kipas AHU mati) dengan waktu tanggap < 80 ms saat loop EOL terputus/alarm.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 30, Chapter 40.
- Modul Jalur Peminatan Prasyarat: Modul A01, Modul A02, Modul A03, Modul A04, Modul A05.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Visi Arsitektur Capstone Track A: Pengontrol Bangunan Cerdas Otonom
Gedung modern menghadapi tantangan trilema: kenyamanan dan kesehatan penghuni (standar ASHRAE 62.1), efisiensi biaya energi listrik utilitas, dan keandalan keselamatan evakuasi darurat (NFPA 72/101).

Sistem capstone ini mengintegrasikan seluruh elemen Track A ke dalam platform pengontrol terdistribusi lokal (*Local-First Building Controller*) yang beroperasi tanpa ketergantungan pada server cloud, mengoordinasikan aktuasi iklim mikro via Matter over Thread, mengeksekusi pemotongan beban puncak secara adaptif, dan mengunci keselamatan jiwa saat insiden kebakaran terdeteksi.

### 2. Kriteria Penerimaan Khusus (SATC Matrix)
Keberhasilan sistem capstone diukur secara kuantitatif melalui 4 pengujian penerimaan:
1. **SATC-A01 (Ventilasi Loop Tertutup IAQ)**: Bukaan katup damper udara segar merespons lonjakan $	ext{CO}_2$ dalam waktu $le 5	ext{ detik}$ dan memulihkan kualitas udara ke $< 800	ext{ ppm}$ tanpa chattering.
2. **SATC-A02 (Ketahanan Jaringan Thread Lokal)**: Saat koneksi internet WAN terputus $100%$, komunikasi kontrol antar-node Thread tetap beroperasi normal dengan Packet Delivery Ratio $100%$ dan latensi rata-rata $< 50	ext{ ms}$.
3. **SATC-A03 (Pemicu Peak-Shaving Otomatis)**: Saat beban listrik gedung mendekati batas kontrak trafo ($92	ext{ kW}$ dari $100	ext{ kW}$), algoritma secara otomatis melepaskan beban Tier 3 non-kritis dan menurunkan daya ke $< 85	ext{ kW}$ dalam waktu $le 3	ext{ detik}$.
4. **SATC-A04 (Verifikasi Interlock Keselamatan Jiwa)**: Saat sinyal alarm kebakaran FAS terpicu, relay pintu magnetik beralih ke *fail-safe unlocked* dan kipas sirkulasi AC mati dalam waktu $< 80	ext{ ms}$.

### 3. Landasan Matematis: Optimasi Beban Puncak & Formulasi Penundaan Evakuasi

1. **Model Pengendalian Beban Puncak Bertingkat**:
   $$
   P_{	ext{net}}(t) = P_{	ext{total}}(t) - sum_{k in 	ext{Tier 3}} delta_k(t) cdot P_k
   $$
   di mana $delta_k in {0, 1}$ adalah status sakelar pelepasan beban non-kritis.

2. **Kondisi Batas Keamanan Kelistrikan Trafo**:
   $$
   P_{	ext{net}}(t) le 0{,}85 cdot P_{	ext{contract}} quad orall t
   $$

3. **Deterministik Waktu Tanggap Interlock Keselamatan**:
   $$
   t_{	ext{interlock}} = t_{	ext{sense}} + t_{	ext{relay_drop}} le 80	ext{ ms}
   $$

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa kemampuan beroperasi mandiri secara lokal (Local-First Resilience) menjadi kriteria penerimaan wajib pada capstone pengontrol gedung cerdas (SATC-A02)?**
   - *Jawaban*: Dalam gedung perkantoran atau fasilitas publik, kegagalan koneksi internet luar kota (WAN) tidak boleh melumpuhkan kontrol suhu ruangan, ventilasi udara segar, maupun lampu tangga darurat. Sistem kendali lokal berbasis Matter/Thread menjamin seluruh otomasi zona tetap berfungsi normal tanpa risiko mati total akibat gangguan penyedia layanan internet.

2. **Bagaimana algoritma peak-shaving membedakan beban yang boleh dimatikan dari beban yang tidak boleh disentuh?**
   - *Jawaban*: Melalui hierarki klasifikasi tier beban: Tier 1 (beban kritis seperti sistem server dan keselamatan darurat) memiliki proteksi absolut dan tidak pernah dipadamkan, sedangkan Tier 3 (beban non-kritis seperti water heater dan pendingin ruang lobi/koridor) diprogram untuk dilepas terlebih dahulu saat daya total mendekati batas kapasitas trafo gedung.

## Tugas

## Penugasan Mandiri: Laporan Evaluasi Capstone Pengontrol Gedung Cerdas

Susun laporan teknik rekayasa formal yang mendokumentasikan kelulusan pengujian SATC-A01 hingga SATC-A04. Sertakan trace log eksekusi saat sinyal alarm darurat kebakaran diinjeksikan dan buktikan waktu tanggap relay berada di bawah 80 milidetik.

## Ringkasan
- Modul A06 memberikan pemahaman mendalam dan terapan mengenai Autonomous Micro-Climate & Demand-Response Building Controller (Capstone Project) pada tingkat kedalaman L4: Research Preparation.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [building_capstone_controller_sim.py](src/building_capstone_controller_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. ANSI/ASHRAE Standard 135-2020, BACnet — A Data Communication Protocol for Building Automation, [https://www.ashrae.org/technical-resources/standards-and-guidelines](https://www.ashrae.org/technical-resources/standards-and-guidelines) (diperiksa 2026-11-18).
2. NFPA 72, National Fire Alarm and Signaling Code, 2022, [https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=72](https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=72) (diperiksa 2026-11-18).

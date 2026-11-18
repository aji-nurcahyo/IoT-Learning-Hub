# Modul A05 — Life-Safety Integration, Fail-Safe Interlocks & Emergency Evacuation Routing

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Membedakan prinsip operasi fail-safe (unlocked/open saat kehilangan daya) vs fail-secure pada sistem pintu akses darurat.
2. Menganalisis integritas sirkuit loop pengawas 2 kawat dengan resistor ujung saluran (End-of-Line / EOL).
3. Merancang interlock keselamatan perangkat keras independen yang mematikan kipas udara dan membuka pintu darurat saat alarm kebakaran aktif.
4. Mengimplementasikan algoritma penentuan jalur evakuasi darurat adaptif berbasis graf terbobot konsentrasi asap/suhu.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 28, Chapter 38.
- Modul Jalur Peminatan Prasyarat: Modul A01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Prinsip Keselamatan Jiwa (Life-Safety) & Standar NFPA 72
Integrasi sistem otomasi bangunan (*Smart Building*) dengan sistem keselamatan jiwa (*Life-Safety*) wajib tunduk pada standar keselamatan ketat (NFPA 72 - *National Fire Alarm and Signaling Code* dan NFPA 101 - *Life Safety Code*).
- **Prinsip Utama**: Sistem kenyamanan gedung (IoT pencahayaan dan pendingin udara) tidak boleh mengintervensi atau menonaktifkan fungsi independen panel alarm kebakaran terpusat (*Fire Alarm Control Panel* / FACP).
- **Interlock Satu Arah (Unidirectional Safety Interlock)**: FACP memiliki otoritas tertinggi untuk mengirimkan sinyal pemicu darurat ke sistem otomasi gedung melalui kontak kering (*dry contacts*) fisik berisolasi galvanik, namun sistem IoT gedung tidak boleh memiliki kemampuan mengirim sinyal batalkan alarm ke FACP.

### 2. Sirkuit Loop Terawasi 2 Kawat dengan Resistor End-of-Line (EOL)
Kabel komunikasi sensor alarm kebakaran di dalam gedung rentan terhadap pemotongan akibat renovasi, korsleting, atau gigitan hama. Sirkuit pengawas loop tertutup (*Supervised Circuit Class B*) membedakan tiga kondisi fisik melalui pembagian tegangan resistor ujung saluran ($R_{	ext{EOL}}$):
1. **Kondisi Normal (Supervised Normal)**: Kabel utuh, resistor $R_{	ext{EOL}}$ terhubung di ujung saluran ($V_{	ext{sense}} approx 4 - 5	ext{ V}$). Arus pengawas kecil ($approx 4	ext{ mA}$) mengalir secara konstan.
2. **Kondisi Terpicu Alarm (Alarm Active)**: Detektor asap optik menutup kontak sakelar paralel, menghubung-singkatkan saluran ($R_{	ext{loop}} approx 0 implies V_{	ext{sense}} approx 20 - 24	ext{ V}$). Panel langsung memicu alarm evakuasi.
3. **Kondisi Gangguan Terputus (Open-Circuit Fault / Trouble)**: Kabel terputus oleh kebakaran atau pekerjaan mekanis ($R_{	ext{loop}} 	o infty implies V_{	ext{sense}} approx 0	ext{ V}$). Panel memicu sinyal peringatan gangguan pemeliharaan (*trouble signal*) tanpa membunyikan sirine evakuasi palsu.

### 3. Fail-Safe vs Fail-Secure & Interlock Evakuasi Darurat
- **Fail-Safe (Aman saat Gagal)**: Perangkat beralih ke posisi terbuka/aman jika kehilangan daya listrik. Kunci pintu magnetik darurat (*magnetic lock*) wajib beroperasi secara *fail-safe*: saat listrik gedung padam atau alarm kebakaran aktif, relay memutus arus suplai koil magnet seketika, memungkinkan pintu didorong terbuka bebas tanpa kunci.
- **Fail-Secure**: Perangkat tetap terkunci saat listrik padam (digunakan pada ruang brankas bank), dilarang digunakan pada jalur tangga evakuasi utama.
- **Interlock Ventilasi Udara (AHU Shutdown)**: Kipas sirkulasi udara segar wajib dimatikan seketika saat alarm kebakaran aktif untuk mencegah penyebaran asap beracun melintasi saluran ducting AC ke lantai lain.

### 4. Landasan Matematis: Pembagian Tegangan Loop EOL & Algoritma Dijkstra Terbobot Bahaya

1. **Persamaan Pembagian Tegangan Loop Terawasi**:
   $$
   V_{	ext{sense}} = V_{	ext{loop}} cdot rac{R_{	ext{sense}}}{R_{	ext{sense}} + R_{	ext{wire}} + R_{	ext{loop}}}
   $$
   di mana $V_{	ext{loop}} = 24{,}0	ext{ V}$, $R_{	ext{sense}} = 1000,Omega$, $R_{	ext{wire}} approx 18,Omega$.
   - **Kondisi Normal ($R_{	ext{loop}} = R_{	ext{EOL}} = 4700,Omega$)**:
     $$
     V_{	ext{sense}} = 24{,}0 	imes rac{1000}{1000 + 18 + 4700} = 24{,}0 	imes rac{1000}{5718} = 4{,}20	ext{ V}
     $$
   - **Kondisi Alarm ($R_{	ext{loop}} approx 50,Omega$)**:
     $$
     V_{	ext{sense}} = 24{,}0 	imes rac{1000}{1000 + 18 + 50} = 24{,}0 	imes rac{1000}{1068} = 22{,}47	ext{ V}
     $$
   - **Kondisi Kabel Putus ($R_{	ext{loop}} 	o infty$)**:
     $$
     V_{	ext{sense}} 	o 0{,}0	ext{ V}
     $$

2. **Worked Numerical Example (Rute Evakuasi Dijkstra Bebas Asap)**:
   - **Topologi Bangunan**:
     - Ruang 302 $	o$ Koridor Tengah: $12	ext{ meter}$
     - Koridor Tengah $	o$ Tangga Timur: $25	ext{ meter}$, Tangga Timur $	o$ Pintu Keluar Timur: $40	ext{ meter}$ (Jarak total nominal $= 77	ext{ meter}$)
     - Koridor Tengah $	o$ Tangga Barat: $30	ext{ meter}$, Tangga Barat $	o$ Pintu Keluar Barat: $45	ext{ meter}$ (Jarak total nominal $= 87	ext{ meter}$)
   - **Kondisi Darurat**: Sensor asap mendeteksi gas berbahaya di Tangga Timur ($	ext{Hazard Penalty} = +1000$).
   - **Evaluasi Biaya Jalur**:
     - Biaya rute Timur: $12 + 25 + 1000 + 40 = 1077	ext{ meter}$
     - Biaya rute Barat: $12 + 30 + 45 = 87	ext{ meter}$
   - **Keputusan Sistem**: Sistem dinamis mematikan signage penunjuk arah Timur dan mengaktifkan lampu LED strobo hijau mengarahkan penghuni ke **Pintu Keluar Barat**, menjamin evakuasi bebas asap dalam jarak tempuh aman.

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa kunci pintu darurat pada tangga kebakaran gedung bertingkat wajib menerapkan mekanisme fail-safe (unlocked on power loss) dan bukan fail-secure?**
   - *Jawaban*: Pada saat kebakaran hebat, pasokan listrik gedung sering kali terputus akibat korsleting atau pemutusan darurat oleh petugas pemadam kebakaran. Jika pintu bersifat *fail-secure*, pintu akan terkunci mati dan menjebak penghuni di dalam koridor berasap tebal, mengakibatkan korban jiwa fatal. Mekanisme *fail-safe* menjamin pintu langsung membuka bebas tanpa hambatan saat listrik padam.

2. **Bagaimana sirkuit loop terawasi dengan resistor EOL dapat membedakan kabel putus dari alarm kebakaran aktif?**
   - *Jawaban*: Saat sensor mendeteksi api, kontak sakelar terhubung singkat ($R approx 0$) menghasilkan tegangan tinggi pada resistor pengukur ($V_{	ext{sense}} approx 24	ext{ V}$). Namun jika kabel putus terpotong, rangkaian menjadi terbuka ($R 	o infty$) dan tidak ada arus yang mengalir, menghasilkan tegangan mendekati nol ($V_{	ext{sense}} approx 0	ext{ V}$), sehingga panel dapat membedakan status *Trouble* dari *Alarm*.

## Tugas

## Penugasan Mandiri: Pemodelan Graf Rute Evakuasi & Interlock Keselamatan

Rancang program Python yang membaca matriks graf konektivitas 10 ruangan di lantai perkantoran. Simulasikan penyebaran asap dinamis dan buktikan algoritma Dijkstra secara adaptif memperbarui rute pintu keluar teraman bagi penghuni di setiap ruangan.

## Ringkasan
- Modul A05 memberikan pemahaman mendalam dan terapan mengenai Life-Safety Integration, Fail-Safe Interlocks & Emergency Evacuation Routing pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [lifesafety_interlock_evacuation_sim.py](src/lifesafety_interlock_evacuation_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. NFPA 72, National Fire Alarm and Signaling Code, 2022, [https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=72](https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=72) (diperiksa 2026-11-18).
2. NFPA 101, Life Safety Code, 2021, [https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=101](https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=101) (diperiksa 2026-11-18).

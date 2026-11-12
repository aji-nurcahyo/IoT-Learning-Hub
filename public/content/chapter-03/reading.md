# Chapter 03 — Electronics, Power & Hardware Safety

## Overview

Sebelum menyentuh *Microcontroller* seperti ESP32 atau merangkai sensor pada *breadboard*, seorang insinyur IoT harus menguasai hukum dasar listrik DC dan disiplin keselamatan perangkat keras (*hardware safety*). Kesalahan sekecil menukar polaritas catu daya, menghubungkan sinyal 5 V langsung ke pin GPIO 3,3 V yang tidak toleran 5 V, atau menyalakan LED tanpa resistor pembatas arus dapat merusak chip secara permanen dalam hitungan milidetik.

Chapter ini membatasi seluruh praktik pada **rangkaian DC tegangan rendah (*low-voltage DC*)** seperti 3,3 V dan 5 V. Materi tidak mencakup pekerjaan tegangan jala-jala AC PLN karena memiliki risiko sengatan listrik fatal dan berada di luar ruang lingkup fondasi awal.

## Prasyarat

- Memahami alur sistem IoT dan kebutuhan daya node dari [Chapter 01](#/chapter/1) dan [Chapter 02](#/chapter/2).
- Pemahaman dasar aljabar pecahan dan satuan metrik (mili-, kilo-, mega-).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Menghitung** tegangan ($V$), arus ($I$), resistansi ($R$), dan daya ($P$) pada rangkaian seri/paralel sederhana menggunakan Hukum Ohm dan Hukum Kirchhoff.
2. **Menentukan** nilai resistor pembatas arus LED, resistor *pull-up / pull-down*, serta *voltage divider* yang sesuai dengan batas tegangan dan arus pin GPIO.
3. **Menyusun** *power budget* sederhana untuk node IoT berbasis siklus aktif-*sleep* (*duty cycle*) dan memperkirakan umur baterai.
4. **Menerapkan** prosedur aman penggunaan *breadboard*, *DC power supply*, referensi *Ground* (`GND`), dan *multimeter* untuk mencegah *overcurrent*, *reverse polarity*, dan *short circuit*.

## Konsep dan teori

### 1. Besaran Dasar Listrik: Voltage, Current, Resistance, dan Power

| Besaran | Simbol & Satuan | Analogi Fisik | Makna Praktis pada Rangkaian IoT |
| --- | --- | --- | --- |
| **Voltage (Tegangan)** | $V$ — Volt ($\text{V}$) | Beda tekanan air antar dua titik | Beda potensial listrik relatif terhadap *Ground* (`GND`) |
| **Current (Arus)** | $I$ — Ampere ($\text{A}$, $\text{mA}$) | Laju aliran air melalui pipa | Banyaknya muatan mengalir; menentukan panas & umur baterai |
| **Resistance (Resistansi)** | $R$ — Ohm ($\Omega$, $\text{k}\Omega$) | Penyempitan pada pipa | Hambatan terhadap arus; membatasi arus dan membagi tegangan |
| **Power (Daya)** | $P$ — Watt ($\text{W}$, $\text{mW}$) | Kerja mekanis per detik | Energi per satuan waktu yang dikonsumsi atau didisipasikan sebagai panas |

### 2. Hukum Ohm, Daya Listrik, dan Hukum Kirchhoff

Hubungan linier antara tegangan, arus, dan resistansi pada beban resistif dinyatakan oleh **Hukum Ohm** dan persamaan daya:

$$
V = I \cdot R, \qquad P = V \cdot I = I^2 R = \frac{V^2}{R}
$$

Untuk menganalisis simpul (*node*) dan lintasan tertutup (*loop*) pada *breadboard*, kita menggunakan dua **Hukum Kirchhoff**:

1. **Kirchhoff's Current Law (KCL)**: Jumlah arus yang masuk ke sebuah simpul sama dengan jumlah arus yang keluar dari simpul tersebut:
   $$\sum I_{\text{masuk}} = \sum I_{\text{keluar}}$$
   *Implikasi IoT*: Jika satu pin GPIO mencatu 3 LED paralel masing-masing $6\text{ mA}$, total arus yang keluar dari pin adalah $18\text{ mA}$.
2. **Kirchhoff's Voltage Law (KVL)**: Jumlah aljabar seluruh beda potensial sepanjang lintasan tertutup sama dengan nol:
   $$\sum V = 0$$
   *Implikasi IoT*: Tegangan catu $V_{CC}$ pada loop LED terbagi antara tegangan jatuh resistor ($V_R = I \cdot R$) dan tegangan maju LED ($V_F$).

### 3. DC Power Supply, Ground Reference, dan GPIO Limits

- **DC Power Supply**: Papan pengembangan mikrokontroler modern umumnya menerima input $5\text{ V}$ melalui port USB, lalu menurunkannya melalui regulator internal (*LDO* atau *buck converter*) menjadi **$3{,}3\text{ V}$** untuk logika inti SoC.
- **Common Ground Reference (`GND`)**: Tegangan selalu bersifat relatif. Jika mikrokontroler dan modul sensor eksternal dicatu oleh dua sumber daya berbeda, pin **`GND` keduanya wajib dihubungkan bersama** agar memiliki titik acuan $0\text{ V}$ yang sama. Tanpa *common ground*, pembacaan sinyal digital maupun analog akan kacau.
- **Batas Tegangan & Arus GPIO**: Pada mayoritas keluarga ESP32 (periksa datasheet varian spesifik pada Chapter 04), level logika GPIO adalah **$3{,}3\text{ V}$** (bukan $5\text{ V}$ tolerant!) dengan batas arus kontinu per pin umumnya berada di kisaran puluhan miliampere (misal batas desain aman sering dijaga $\le 12\text{ mA}$ per pin). Menghubungkan output sensor $5\text{ V}$ langsung ke pin $3{,}3\text{ V}$ berisiko merusak dioda proteksi ESD internal chip.

### 4. Resistor Pembatas Arus LED & Pull-Up / Pull-Down

![Skema resistor pembatas arus LED, pull-up resistor, dan keselamatan multimeter](content/chapter-03/diagram.svg)

**A. Resistor Pembatas Arus LED**
LED bukan beban resistif linier: begitu tegangan melampaui tegangan maju $V_F$ (sekitar $1{,}8\text{--}2{,}2\text{ V}$ untuk merah/kuning/hijau klasik, $2{,}8\text{--}3{,}3\text{ V}$ untuk biru/putih), arus akan melonjak drastis bila tidak dibatasi. Berdasarkan KVL:

$$
R_{\text{min}} = \frac{V_{CC} - V_F}{I_{\text{target}}}
$$

**B. Pull-Up dan Pull-Down Resistor**
Pin input digital memiliki impedansi sangat tinggi. Jika tombol (*push button*) dalam keadaan terbuka dan pin tidak terhubung ke mana pun (*floating*), noise elektromagnetik di udara menyebabkan pembacaan pin melompat acak antara `HIGH` dan `LOW`.
- **Pull-Up ($10\text{ k}\Omega$ ke $+3{,}3\text{ V}$)**: Saat tombol terbuka, pin terbaca `HIGH`; saat tombol ditekan ke `GND`, pin terbaca `LOW` (*active-low*). Arus saat ditekan hanyalah $3{,}3\text{ V} / 10\text{ k}\Omega = 0{,}33\text{ mA}$.
- **Pull-Down ($10\text{ k}\Omega$ ke `GND`)**: Saat tombol terbuka, pin terbaca `LOW`; saat ditekan ke $+3{,}3\text{ V}$, pin terbaca `HIGH` (*active-high*).

**C. Pembagi Tegangan (*Voltage Divider*)**
Untuk menurunkan sinyal DC lambat dari sensor $5\text{ V}$ menjadi aman bagi input $3{,}3\text{ V}$:

$$
V_{\text{out}} = V_{\text{in}} \cdot \frac{R_2}{R_1 + R_2}
$$

*(Catatan: Voltage divider hanya cocok untuk sinyal berimpedansi tinggi seperti input GPIO/ADC, **bukan** untuk mencatu daya beban berarus besar karena tegangan keluaran akan anjlok saat arus beban ditarik).*

### 5. Power Budget Sederhana

Untuk perangkat bertenaga baterai, arus rata-rata ($I_{\text{avg}}$) dihitung berdasarkan durasi fase aktif ($t_{\text{aktif}}$ dengan arus $I_{\text{aktif}}$) dan fase tidur (*sleep* $t_{\text{sleep}}$ dengan arus $I_{\text{sleep}}$) dalam satu siklus $T_{\text{siklus}} = t_{\text{aktif}} + t_{\text{sleep}}$:

$$
I_{\text{avg}} = \frac{(I_{\text{aktif}} \cdot t_{\text{aktif}}) + (I_{\text{sleep}} \cdot t_{\text{sleep}})}{T_{\text{siklus}}}, \qquad t_{\text{hidup (jam)}} = \frac{C_{\text{baterai (mAh)}} \times \eta_{\text{usable}}}{I_{\text{avg (mA)}}}
$$

Di sini $\eta_{\text{usable}}$ (misal $0{,}75\text{--}0{,}85$) memperhitungkan bahwa baterai tidak boleh dikuras hingga $0\%$ serta kerugian efisiensi regulator.

### 6. Worked Examples (Terverifikasi dengan `electronics_calc.py`)

Berikut tiga contoh perhitungan yang dapat langsung diverifikasi menggunakan skrip [`electronics_calc.py`](content/chapter-03/src/electronics_calc.py) (hasil nyata tercatat di [`outputs.md`](content/chapter-03/outputs.md)):

1. **Resistor LED dari GPIO $3{,}3\text{ V}$**:
   Diketahui $V_{CC} = 3{,}3\text{ V}$, $V_F = 2{,}0\text{ V}$ (LED merah/kuning), dan target arus aman $I_{\text{target}} \le 6\text{ mA}$ ($0{,}006\text{ A}$).
   $$R_{\text{min}} = \frac{3{,}3 - 2{,}0}{0{,}006} = 216{,}7\,\Omega$$
   Pilih nilai resistor standar terdekat yang lebih besar: **$220\,\Omega$**.
   Arus aktual: $I = 1{,}3 / 220 = 5{,}91\text{ mA}$.
   Disipasi daya resistor: $P_R = 1{,}3\text{ V} \times 5{,}91\text{ mA} = 7{,}68\text{ mW}$ (jauh di bawah rating resistor standar $1/4\text{ W} = 250\text{ mW}$).

2. **Keamanan Voltage Divider $5\text{ V} \rightarrow 3{,}3\text{ V}$**:
   - Dengan $R_1 = 10\text{ k}\Omega$ dan $R_2 = 15\text{ k}\Omega$: $V_{\text{out}} = 5{,}0 \times \frac{15}{10+15} = 3{,}00\text{ V}$ (aman $\le 3{,}3\text{ V}$ dan masih terbaca `HIGH`).
   - Jika keliru memasang $R_1 = 4{,}7\text{ k}\Omega$ dan $R_2 = 10\text{ k}\Omega$: $V_{\text{out}} = 5{,}0 \times \frac{10}{14{,}7} = 3{,}40\text{ V}$ (melebihi $3{,}3\text{ V}$!).

3. **Estimasi Umur Baterai Node Sensor**:
   Baterai $2000\text{ mAh}$ ($\eta = 80\% \Rightarrow 1600\text{ mAh}$ efektif), siklus $300\text{ s}$: aktif $3\text{ s}$ menarik $80\text{ mA}$, tidur $297\text{ s}$ menarik $0{,}15\text{ mA}$.
   $$I_{\text{avg}} = \frac{(80 \times 3) + (0{,}15 \times 297)}{300} = 0{,}949\text{ mA}$$
   $$\text{Umur baterai} = \frac{1600}{0{,}949} \approx 1686{,}9\text{ jam} \approx 70{,}3\text{ hari}$$

### 7. Breadboard, Multimeter & Keselamatan Hardware

**Aturan Kerja Aman pada Meja Praktikum**:
1. **Putuskan daya (*power off*) sebelum mengubah kabel *jumper* atau mencabut komponen.**
2. **Periksa polaritas (`+VCC` vs `GND`) dua kali** sebelum menyalakan supply. *Reverse polarity* merusak regulator dan IC sensor secara seketika.
3. **Kenali peta koneksi *breadboard***: rel daya (`+` dan `-`) terhubung memanjang secara horizontal (periksa apakah terputus di tengah pada breadboard panjang!), sedangkan lubang komponen tengah (`a–e` dan `f–j`) terhubung per baris vertikal dan dipisahkan parit tengah (*center trench*) untuk IC.
4. **Cegah *short circuit* dan *overcurrent***:
   - Gunakan *DC power supply* dengan fitur *current limit* bila tersedia (set batas awal misal $300\text{--}500\text{ mA}$ saat menguji rangkaian baru).
   - Jangan pernah menghubungkan motor DC, relay mekanik, atau solenoid langsung ke pin GPIO tanpa rangkaian *driver* dan *flyback diode* (akan dibahas di Chapter 09).
5. **Prosedur Pengukuran Multimeter**:
   - **Voltmeter (Tegangan)**: Sambung **paralel** terhadap komponen atau antara titik uji dan `GND`.
   - **Ammeter (Arus)**: Putus rangkaian dan sambung **seri**. Pastikan probe berada di terminal `mA/A` yang sesuai. **Dilarang keras menyambungkan ammeter langsung melintasi `+VCC` dan `GND`** karena resistansi internal ammeter mendekati $0\,\Omega$ sehingga menyebabkan hubung singkat (*short circuit*)!
   - **Ohmmeter / Continuity (Resistansi)**: Hanya digunakan saat rangkaian **tidak bertegangan (*powered off*)**.

### 8. Common Mistakes & Troubleshooting

| Gejala / Kesalahan | Penyebab Umum | Pemeriksaan & Perbaikan |
| --- | --- | --- |
| LED tidak menyala sama sekali | Polaritas LED terbalik (anoda/katoda), atau resistor dipasang di baris breadboard yang salah | Uji LED dengan arah benar; pastikan kaki resistor dan LED bertemu pada node baris yang sama |
| Pembacaan tombol acak saat tidak ditekan | Pin input dibiarkan *floating* tanpa *pull-up* atau *pull-down* | Pasang resistor *pull-up/down* $10\text{ k}\Omega$ atau aktifkan *internal pull-up* |
| Regulator board sangat panas / USB komputer mati | *Short circuit* antara rel `+3.3V`/`+5V` dan `GND`, atau pin GPIO langsung ke `GND` saat output `HIGH` | Segera cabut daya! Periksa kontinuitas rel daya dan jalur *breadboard* dengan ohmmeter |
| Sekering multimeter putus pada mode arus | Probe masih di lubang `mA/A` lalu dipakai mengukur tegangan paralel | Kembalikan probe merah ke lubang `V/Ω` sebelum mengukur tegangan |

### 9. Real-World Applications

- **Telekomunikasi (BTS Battery & Rectifier Monitoring)**: Menggunakan *voltage divider* presisi dan proteksi pembatas arus untuk memantau bank baterai $48\text{ V DC}$ dengan mikrokontroler $3{,}3\text{ V}$ secara aman.
- **Smart Agriculture Node**: Desain *power budget* berbasis *deep sleep* menentukan apakah sebuah node sensor kelembaban tanah mampu bertahan 6 bulan dengan panel surya kecil dan baterai LiFePO4.
- **Industrial Control Panel**: Penggunaan *common ground* yang bersih serta resistor *pull-up/pull-down* eksternal bernilai tepat mencegah pemicu palsu akibat interferensi elektromagnetik motor pabrik.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-03/exercises.md)):
1. Soal perhitungan Hukum Ohm, KCL/KVL, resistor LED (merah vs biru), dan *voltage divider*.
2. Identifikasi bahaya *wiring* pada skenario *breadboard* dan prosedur pengukuran multimeter yang benar.
3. Simulasi *power budget* menggunakan [`electronics_calc.py`](content/chapter-03/src/electronics_calc.py) untuk membandingkan siklus kirim 1 menit vs 15 menit.
4. Praktik opsional Path B (jika memiliki multimeter, breadboard, LED, dan resistor $220\,\Omega$–$10\text{ k}\Omega$) dengan daftar periksa keselamatan wajib.

## Tugas

Susun **Rancangan Rangkaian Low-Voltage DC, Power Budget & Audit Keselamatan** untuk sebuah node sensor lapangan (detail pada tab **Tugas & Rubrik** — [assignment.md](content/chapter-03/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Perhitungan Hukum Ohm, LED & divider | 30 | Ketepatan rumus, pemilihan nilai resistor standar, dan margin daya komponen |
| Penyusunan power budget & estimasi baterai | 25 | Perhitungan arus rata-rata *duty-cycle* serta evaluasi dampak interval aktif |
| Audit keselamatan, batas GPIO & multimeter | 25 | Identifikasi risiko *overvoltage/short/reverse polarity* dan prosedur ukur yang benar |
| Dokumentasi skema & keterbatasan analisis | 20 | Kerapian tabel/diagram pin dan kejujuran membedakan hitungan vs pengukuran |

## Ringkasan

- Hukum Ohm ($V = IR$), daya ($P = VI$), dan Hukum Kirchhoff (KCL/KVL) menjadi dasar untuk memastikan setiap pin mikrokontroler dan komponen bekerja dalam batas aman datasheet.
- Pin input digital tidak boleh dibiarkan *floating*; gunakan *pull-up* atau *pull-down* untuk mendefinisikan status logika awal.
- Keselamatan *low-voltage DC* dimulai dari disiplin: *power off* saat merangkai, cek polaritas, hormati batas tegangan $3{,}3\text{ V}$ GPIO, gunakan *common ground*, dan ukur tegangan secara paralel serta arus secara seri.
- Verifikasi pada chapter ini bersifat analitis/*software* melalui `electronics_calc.py`; pengukuran rangkaian fisik pada *breadboard* berstatus **Belum diuji** di lingkungan ini.

## Referensi

1. Espressif Systems, *ESP32 Series Datasheet — Electrical Characteristics & Recommended Operating Conditions*, [https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) (diperiksa 2026-11-10).
2. Arduino Official Documentation, *Digital Pins & Pull-Up Resistors Guide*, [https://docs.arduino.cc/learn/microcontrollers/digital-pins/](https://docs.arduino.cc/learn/microcontrollers/digital-pins/) (diperiksa 2026-11-10).
3. SparkFun / Electronics Reference (Open Educational Tutorial), *How to Use a Multimeter & Breadboard Basics*, [https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) (diperiksa 2026-11-10).


# Chapter 09 — Actuators, Drivers & Control Fundamentals

## Overview

Sensor membaca kondisi dunia fisik, tetapi **Actuator** lah yang memberi dampak balik ke lingkungan—menyalakan indikator, membunyikan peringatan, menggerakkan katup servo, atau memutar kipas pendingin. Namun, menghubungkan *Actuator* berarus besar atau berbeban induktif langsung ke pin GPIO *Microcontroller* adalah penyebab kerusakan papan pengembangan yang paling sering terjadi di laboratorium.

Chapter ini membahas jenis-jenis *Actuator* *low-voltage DC* (LED, *buzzer*, relay DC, servo, motor DC), alasan diperlukannya **rangkaian driver**, proteksi **flyback diode**, aktuasi berbasis PWM, perbedaan kontrol *open-loop* vs *closed-loop*, kontrol ambang batas (*threshold*) dengan **histeresis**, serta prinsip **safety interlock** dan **fail-safe**. Seluruh praktik dibatasi pada **tegangan rendah DC ($3{,}3\text{--}12\text{ V}$)** dan tidak mencakup pensaklaran listrik AC jala-jala.

## Prasyarat

- Memahami Hukum Ohm, batas arus pin GPIO, dan *common ground* dari [Chapter 03](#/chapter/3).
- Menguasai `GPIO` input/output dari [Chapter 06](#/chapter/6) dan PWM `LEDC` dari [Chapter 07](#/chapter/7).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Memilih** rangkaian *driver* (*NPN transistor* atau *logic-level N-MOSFET*) dan **flyback diode** berdasarkan kebutuhan tegangan, arus, dan sifat induktif *Actuator* *low-voltage DC*.
2. **Menjelaskan** aktuasi berbasis PWM untuk motor DC (*speed control*) dan motor servo (*pulse width* $1\dots 2\text{ ms}$ @ $50\text{ Hz}$).
3. **Membandingkan** kontrol *open-loop*, *closed-loop single-threshold*, dan kontrol **histeresis** untuk mencegah *chattering*.
4. **Merancang** *safety interlock* dan kondisi *fail-safe* ketika sensor gagal (`NaN`), catu daya reset, atau pelindung terbuka.

## Konsep dan teori

### 1. Ragam Actuator Low-Voltage DC & Batas Arus GPIO

| Actuator | Tegangan & Arus Khas | Sifat Beban | Kebutuhan Driver dari GPIO $3{,}3\text{ V}$ |
| --- | --- | --- | --- |
| **LED Indikator** | $1{,}8\text{--}3{,}3\text{ V}$, $5\text{--}15\text{ mA}$ | Semikonduktor | Cukup resistor pembatas seri (mis. $220\,\Omega$) |
| **Active/Passive Buzzer** | $3{,}3\text{--}5\text{ V}$, $15\text{--}40\text{ mA}$ | Kapasitif/Induktif | Buzzer kecil bisa langsung jika $<10\text{ mA}$; modul/5 V pakai transistor |
| **Relay Modul DC 5 V** | Koil $5\text{ V}$, $60\text{--}90\text{ mA}$ | **Induktif** | Wajib transistor/optocoupler driver + *flyback diode* + suplai 5 V |
| **Hobby Servo (SG90/MG90)** | Suplai $5\text{ V}$ ($100\text{--}700\text{ mA}$), Sinyal $3{,}3\text{ V}$ | Motor + gearbox | Suplai daya dari rel 5 V eksternal; sinyal PWM $50\text{ Hz}$ dari GPIO |
| **Motor DC / Kipas 5–12 V** | $5\text{--}12\text{ V}$, $150\text{ mA}\dots 2\text{ A}$ | **Induktif & *stall current* tinggi** | **Wajib** N-MOSFET / H-Bridge driver + *flyback diode* + suplai terpisah |

### 2. Rangkaian Driver Low-Side & Flyback Diode

Pin GPIO ESP32 hanya sanggup menyuplai sekitar $\le 12\text{ mA}$ secara aman pada $3{,}3\text{ V}$. Untuk menyalakan kipas DC $5\text{ V}$ $200\text{ mA}$, kita memakai **N-MOSFET *logic-level*** (atau transistor NPN seperti 2N2222 / TIP122 untuk arus menengah) sebagai saklar elektronik di sisi bawah (*low-side switch*).

![Skema low-side MOSFET driver dengan flyback diode dan kurva kontrol histeresis](content/chapter-09/diagram.svg)

**Mengapa Tiga Komponen Proteksi Ini Wajib Ada?**
1. **Resistor Gate/Basis ($220\,\Omega$)**: Membatasi lonjakan arus pengisian kapasitansi *gate* MOSFET (atau mengatur arus basis $I_B$ pada BJT) agar pin GPIO tetap aman.
2. **Resistor Pull-Down Gate ($10\text{ k}\Omega$ ke `GND`)**: Saat MCU baru menyala atau *reset*, pin GPIO berada pada mode impedansi tinggi (*floating*). Tanpa *pull-down* $10\text{ k}\Omega$, muatan liar dapat membuat MOSFET menyala sesaat (*fail-unsafe*)!
3. **Flyback Diode (1N5819 / 1N4007 antiparalel terhadap beban induktif)**: Kumparan motor dan relay menyimpan energi magnetik. Ketika MOSFET tiba-tiba memutus arus ($dI/dt$ negatif besar), induktor membangkitkan lonjakan tegangan balik (*inductive kickback*) sangat tinggi sesuai hukum induksi:
   $$V_L = -L \frac{dI}{dt}$$
   Tanpa *flyback diode* (yang dipasang terbalik terhadap suplai normal: katoda ke `+VCC`, anoda ke drain/kolektor), tegangan balik puluhan hingga ratusan volt ini langsung merusak MOSFET dan dapat merambat kembali ke MCU!

### 3. PWM-Based Actuation (Motor DC & Servo)

- **Motor DC (Kecepatan)**: Mengirim sinyal PWM $5\text{--}20\text{ kHz}$ ke *gate* MOSFET mengatur daya rata-rata yang diterima motor secara halus tanpa boros panas seperti resistor seri.
- **Hobby Servo (Posisi Sudut $0^\circ \dots 180^\circ$)**: Memakai PWM berfrekuensi tetap **$50\text{ Hz}$** (periode $T = 20\text{ ms}$). Sudut ditentukan oleh lebar pulsa `HIGH` antara **$1{,}0\text{ ms}$** ($0^\circ$), **$1{,}5\text{ ms}$** ($90^\circ$), hingga **$2{,}0\text{ ms}$** ($180^\circ$).

### 4. Open-Loop vs Closed-Loop Control

- **Open-Loop Control**: Aktuator diperintah berdasarkan jadwal atau nilai tetap tanpa mengukur hasil aktual di lingkungan (contoh: kipas menyala 10 menit setiap jam terlepas dari suhu ruangan). Tidak bisa mengoreksi gangguan luar.
- **Closed-Loop Control (Feedback Control)**: Sistem mengukur keluaran lingkungan menggunakan *Sensor*, membandingkannya dengan *setpoint* target, lalu menyesuaikan *Actuator* secara otomatis (contoh: kipas menyala hanya saat suhu $\ge 30\,^\circ\text{C}$).

### 5. Threshold Control vs Hysteresis (Anti-Chattering)

Kontrol ambang tunggal (*bang-bang*) `if (temp >= 30.0) fan = ON; else fan = OFF;` bermasalah ketika suhu berada di sekitar $30{,}0\,^\circ\text{C}$ disertai *noise* sensor $\pm 0{,}3\,^\circ\text{C}$. Kipas atau relay akan menyala-mati puluhan kali per menit (**chattering**), mempercepat keausan kontak dan memicu lonjakan arus *inrush*.

Solusinya adalah **Hysteresis** (*deadband*) dengan dua ambang: $T_{\text{high}}$ (untuk menyalakan) dan $T_{\text{low}}$ (untuk mematikan):

$$
u[n] = \begin{cases} \text{ON}, & \text{jika } T[n] \ge T_{\text{high}} \\ \text{OFF}, & \text{jika } T[n] \le T_{\text{low}} \\ u[n-1], & \text{jika } T_{\text{low}} < T[n] < T_{\text{high}} \end{cases}
$$

Lebar pita mati (*deadband*) adalah $\Delta T_{\text{hyst}} = T_{\text{high}} - T_{\text{low}}$ (misal $30{,}0 - 28{,}0 = 2{,}0\,^\circ\text{C}$).

**Bukti Simulasi (`hysteresis_control_sim.py` pada `telemetry.csv`)**:
Pada trace 16 langkah dengan *noise* sekitar $30\,^\circ\text{C}$ (hasil nyata di [`outputs.md`](content/chapter-09/outputs.md)):
- **Single-Threshold ($30{,}0\,^\circ\text{C}$)**: mengalami **8 kali transisi** ON/OFF (*chattering*).
- **Hysteresis ($28{,}0\dots 30{,}0\,^\circ\text{C}$)**: hanya **2 kali transisi** bersih (1x ON saat $\ge 30{,}1\,^\circ\text{C}$, 1x OFF saat $\le 27{,}8\,^\circ\text{C}$)!

### 6. Safety Interlock & Fail-Safe Principles

1. **Fail-Safe Default State**: Tetapkan status aman awal saat *boot* (`ledcWrite(FAN_PIN, 0);`) dan gunakan *pull-down* $10\text{ k}\Omega$ pada *gate* MOSFET agar beban mati jika MCU *hang* atau *reset*.
2. **Sensor-Fault Shutdown**: Jika kabel sensor putus atau korsleting (`isnan(tempC)`), jangan biarkan pemanas terus menyala atau kipas berjalan tak terkendali—masuk ke mode `FAIL_SAFE_OFF` dan nyalakan alarm peringatan.
3. **Safety Interlock**: Saklar fisik (misalnya sensor penutup pelindung kipas atau tombol *E-Stop*) yang diperiksa paling awal di setiap siklus kontrol dan langsung memutus aktuator bila terbuka.

### 7. Implementasi Praktis: Firmware Histeresis + Interlock (`ex01_hysteresis_driver.ino`)

- **Target Board**: `ESP32-DevKitC V4` (`GPIO 34` sensor analog, `GPIO 27` interlock `INPUT_PULLUP`, `GPIO 25` PWM driver kipas/LED beban, `GPIO 26` alarm buzzer).
- **Firmware & Simulasi**: [`ex01_hysteresis_driver.ino`](content/chapter-09/src/ex01_hysteresis_driver/ex01_hysteresis_driver.ino) + Wokwi [`wokwi_diagram.json`](content/chapter-09/src/wokwi_diagram.json).
- **Status Verifikasi**: Skrip [`hysteresis_control_sim.py`](content/chapter-09/src/hysteresis_control_sim.py) dieksekusi nyata di Python 3.12.10 (`outputs.md`); firmware `.ino` berstatus **Belum diuji** di server ini.

### 8. Common Mistakes & Troubleshooting

| Kesalahan | Akibat Fisik / Logis | Perbaikan |
| --- | --- | --- |
| Menghubungkan motor/relay 5 V langsung ke pin GPIO | Arus tarik $>100\text{ mA}$ merusak pin ESP32 & menyebabkan *brownout* | Gunakan driver transistor/MOSFET + suplai 5 V terpisah + *common GND* |
| Lupa memasang *flyback diode* pada motor/relay | Lonjakan $L \frac{dI}{dt}$ membakar MOSFET atau me-reset ESP32 | Pasang dioda 1N5819/1N4007 antiparalel di kaki beban induktif |
| Tidak ada *pull-down* di *gate* MOSFET | Beban menyala sendiri selama proses *booting* chip | Tambahkan resistor $10\text{ k}\Omega$ antara *gate* dan `GND` |
| Memakai *single threshold* tanpa histeresis | Relay berbunyi berisik (*chattering*) dan cepat rusak | Tambahkan *deadband* histeresis sesuai tingkat *noise* sensor |

### 9. Real-World Applications

- **Pendinginan Kabinet Telekomunikasi (BTS Shelter)**: Kipas DC $12\text{ V}/48\text{ V}$ dikendalikan driver MOSFET dengan histeresis $2\dots 3\,^\circ\text{C}$ serta *interlock* pintu untuk keselamatan teknisi saat inspeksi.
- **Irigasi Katup Solenoid Smart Agriculture**: Menggunakan katup solenoid DC $12\text{ V}$ ber-*flyback diode* dengan *fail-safe max-open timer* agar pompa/katup menutup otomatis saat sistem kehilangan sinyal sensor kelembaban.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-09/exercises.md)):
1. Identifikasi kesalahan rangkaian driver (hilangnya *flyback diode*, salah orientasi dioda, kurang *common GND*, atau lupa *pull-down*).
2. Perhitungan arus basis transistor NPN / pemilihan *logic-level MOSFET* untuk beban kipas $12\text{ V}$ $300\text{ mA}$ dan konversi pulsa servo $50\text{ Hz}$.
3. Analisis perbandingan transisi pada [`hysteresis_control_sim.py`](content/chapter-09/src/hysteresis_control_sim.py) beserta Mini Challenge penambahan *minimum-on-time* $5\text{ detik}$.

## Tugas

Rancang **Sistem Driver & Kontrol Histeresis Low-Voltage DC dengan Safety Interlock** (detail di tab **Tugas & Rubrik** — [assignment.md](content/chapter-09/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Desain rangkaian driver & proteksi induktif | 30 | Driver MOSFET/BJT tepat, *flyback diode*, resistor gate/base, *pull-down* fail-safe, *common GND* |
| Implementasi kontrol histeresis & PWM | 25 | *Deadband* jelas bebas *chattering*, aktuasi PWM benar dan non-blocking |
| Safety interlock & prinsip fail-safe | 25 | Penanganan sensor `NaN`, *interlock* darurat prioritas tertinggi, state boot aman |
| Dokumentasi, simulasi & kejujuran bukti | 20 | BOM & wiring low-voltage DC lengkap, log simulasi/expected output terdokumentasi jujur |

## Ringkasan

- Beban berarus tinggi atau induktif (motor, relay, buzzer besar) wajib dikendalikan melalui **driver** (N-MOSFET/BJT), suplai eksternal ber-*common ground*, dan **flyback diode** untuk meredam lonjakan $L \frac{dI}{dt}$.
- **Kontrol histeresis** ($T_{\text{high}}$ dan $T_{\text{low}}$) menghilangkan *chattering* akibat *noise* sensor di sekitar ambang batas (dalam simulasi `hysteresis_control_sim.py`, transisi turun dari 8x menjadi 2x).
- **Safety interlock** dan **fail-safe shutdown** saat sensor bermasalah (`NaN`) adalah bagian wajib dari kontrol aktuator yang bertanggung jawab.
- Simulasi kontrol telah dieksekusi di Python (`outputs.md`); eksekusi `.ino` dan uji Wokwi/hardware berstatus **Belum diuji** di server ini.

## Referensi

1. Espressif Systems, *ESP-IDF LEDC & MCPWM Peripherals Documentation*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/ledc.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/ledc.html) (diperiksa 2026-11-10).
2. Arduino Official Documentation, *Servo & Motor Control Fundamentals (Low-Voltage DC)*, [https://docs.arduino.cc/learn/electronics/servo-motors/](https://docs.arduino.cc/learn/electronics/servo-motors/) (diperiksa 2026-11-10).
3. Wokwi Documentation, *Buzzer & Slide Switch Simulation Reference*, [https://docs.wokwi.com/parts/wokwi-buzzer](https://docs.wokwi.com/parts/wokwi-buzzer) (diperiksa 2026-11-10).


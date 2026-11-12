# Chapter 07 — Analog Signals, ADC, PWM & Sampling

## Overview

Dunia fisik sebagian besar bersifat **kontinu** (analog): suhu berubah mulus, intensitas cahaya matahari naik perlahan, dan tegangan potensiometer atau mikrofon berubah secara kontinu terhadap waktu. Sebaliknya, *Microcontroller* hanya bekerja menggunakan angka biner **diskrit** baik dalam waktu (*sampling*) maupun amplitudo (*quantization*).

Chapter ini membahas mekanisme **Analog-to-Digital Converter (ADC)** untuk membaca sinyal analog, **Pulse Width Modulation (PWM)** untuk menghasilkan keluaran daya bervariasi pada LED atau penggerak motor, keterbatasan spesifik ADC pada ESP32, kriteria **Nyquist**, fenomena ***aliasing***, penyaringan *noise* sederhana (*moving average*), serta praktik mengatur kecerahan LED melalui pembacaan potensiometer.

## Prasyarat

- Memahami pembagi tegangan dan batas $3{,}3\text{ V}$ pada pin GPIO dari [Chapter 03](#/chapter/3).
- Memahami peta pin `ESP32-DevKitC V4` (`GPIO 34–39` *input-only*) dari [Chapter 04](#/chapter/4).
- Menguasai struktur non-blocking `millis()` dari [Chapter 05](#/chapter/5).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Menghitung** resolusi langkah kuantisasi ($1\text{ LSB}$), tegangan analog dari kode biner ADC, dan ketidakpastian kuantisasi teoretis ($\pm 0{,}5\text{ LSB}$).
2. **Menjelaskan** pengaturan atenuasi ADC ESP32 (`ADC_11db`), fungsi `analogReadMilliVolts()`, serta keterbatasan non-linearitas dan konflik `ADC2` dengan Wi-Fi.
3. **Menghitung** *duty cycle*, tegangan rata-rata PWM, dan batas kombinasi frekuensi-resolusi pada periferal `LEDC`.
4. **Menganalisis** kriteria *sampling* Nyquist ($f_s > 2 f_{\max}$), memprediksi frekuensi *aliasing*, dan meredam *noise* menggunakan *moving average*.

## Konsep dan teori

### 1. Analog vs Digital, Sampling, dan Kuantisasi

Mengubah sinyal analog $x(t)$ menjadi data digital membutuhkan dua langkah utama:
1. **Sampling (Diskritisasi Waktu)**: Mengambil cuplikan nilai tegangan setiap selang waktu $T_s = 1 / f_s$, dengan $f_s$ adalah laju *sampling* (Hz).
2. **Quantization (Diskritisasi Amplitudo)**: Membulatkan setiap nilai tegangan kontinu ke salah satu dari $2^N$ tingkat diskrit pada ADC beresolusi $N$-bit.

Pada ADC $N$-bit dengan rentang skala penuh $V_{FS}$ (misalnya $12\text{-bit} \Rightarrow 0\dots 4095$):

$$
\Delta V_{\text{LSB}} = \frac{V_{FS}}{2^N - 1}, \qquad V_{\text{ukur}} = D_{\text{ADC}} \times \frac{V_{FS}}{2^N - 1}
$$

Kesalahan pembulatan akibat proses kuantisasi ideal berada dalam batas $\pm \frac{1}{2}\text{ LSB}$. Untuk $N = 12$ dan $V_{FS} = 3{,}30\text{ V}$, $1\text{ LSB} \approx 0{,}806\text{ mV}$, sehingga ketidakpastian kuantisasi ideal adalah $\pm 0{,}403\text{ mV}$.

![Diagram sampling ADC, kuantisasi, Nyquist aliasing, dan duty cycle PWM](content/chapter-07/diagram.svg)

### 2. Referensi, Atenuasi, dan Keterbatasan ADC pada ESP32

Berbeda dengan sebagian MCU sederhana, **ADC ESP32 klasik memiliki beberapa keterbatasan penting yang wajib dipahami**:
- **Tegangan Referensi & Atenuasi**: Tegangan referensi internal ADC ESP32 bernilai nominal $\sim 1{,}1\text{ V}$ (bervariasi tiap chip!). Untuk mengukur hingga $\sim 3{,}1\text{ V}$, aktifkan atenuasi **`ADC_11db`** (`analogSetPinAttenuation(pin, ADC_11db)`).
- **Non-Linearitas & Dead-Zone**: Pada ujung bawah ($< 150\text{ mV}$) dan ujung atas ($> 3100\text{ mV}$ pada `11 dB`), kurva ADC ESP32 klasik menjadi tidak linier dan jenuh di `0` atau `4095`. Karena itu, gunakan **`analogReadMilliVolts(pin)`** yang memanfaatkan kurva kalibrasi eFuse pabrik dibanding mengkalikan `analogRead()` dengan `3.3 / 4095` secara naif.
- **Konflik `ADC2` dengan Wi-Fi**: ESP32 klasik memiliki dua unit ADC: `ADC1` (`GPIO 32–39`) dan `ADC2` (`GPIO 0, 2, 4, 12–15, 25–27`). **`ADC2` dipakai oleh driver Wi-Fi sehingga gagal atau error saat Wi-Fi aktif!** Selalu prioritaskan pin **`ADC1` (`GPIO 32, 33, 34, 35, 36, 39`)** untuk sensor analog.

### 3. Pulse Width Modulation (PWM) & LEDC ESP32

*Microcontroller* digital umumnya tidak memakai DAC murni untuk mengatur kecepatan motor atau kecerahan LED; sebagai gantinya digunakan **PWM**, yaitu sinyal kotak berfrekuensi tetap $f_{\text{PWM}}$ dengan lebar pulsa `HIGH` yang divariasikan (*duty cycle* $D$):

$$
D = \frac{t_{\text{ON}}}{T_{\text{periode}}} \times 100\%, \qquad V_{\text{avg}} = \frac{t_{\text{ON}}}{T_{\text{periode}}} \cdot V_{\text{HIGH}}
$$

Pada ESP32, periferal **LEDC** menghasilkan PWM secara perangkat keras (*hardware timer*). Pada *Arduino-ESP32 v3.x*, konfigurasinya menggunakan `ledcAttach(pin, freq, resBits)` dan `ledcWrite(pin, duty)`.
Perhatikan **trade-off frekuensi vs resolusi**:

$$
f_{\text{PWM, max}} \approx \frac{f_{\text{clock}}}{2^{N_{\text{res}}}}
$$

Dengan *clock* $80\text{ MHz}$, resolusi 10-bit ($1024$ langkah) mendukung frekuensi hingga puluhan kHz (misal $5\text{ kHz}$ sangat mulus untuk LED tanpa kedipan kamera), sedangkan resolusi 16-bit membatasi frekuensi maksimum jauh lebih rendah.

### 4. Kriteria Sampling Nyquist & Aliasing

Menurut **Teorema Sampling Nyquist-Shannon**, untuk merekonstruksi sinyal berfrekuensi maksimum $f_{\max}$ tanpa kehilangan informasi, laju *sampling* $f_s$ harus memenuhi:

$$
f_s > 2 f_{\max}
$$

Jika $f_s < 2 f_{\max}$ (*undersampling*), komponen frekuensi tinggi akan **melipat turun menjadi frekuensi palsu (*aliasing*)**:

$$
f_{\text{alias}} = \left| f_{\text{sig}} - k \cdot f_s \right| \quad (\text{untuk bilangan bulat } k \text{ sehingga } f_{\text{alias}} \le f_s / 2)
$$

**Contoh Nyata pada `adc_nyquist_sim.py`**: Jika sinyal getaran $60\text{ Hz}$ disampling terlalu lambat pada $f_s = 80\text{ Hz}$ (padahal syarat Nyquist $> 120\text{ Hz}$), sampel diskrit yang terekam identik dengan gelombang palsu berfrekuensi $|60 - 80| = 20\text{ Hz}$ (deviasi numerik hanya $1{,}41 \times 10^{-14}$)! Dalam praktik *engineering*, pilih $f_s \ge 5\times \dots 10\times f_{\max}$ serta tambahkan *low-pass filter* RC analog sebelum pin ADC bila terdapat sinyal frekuensi tinggi.

### 5. Noise & Filtering Sederhana (*Moving Average*)

Pembacaan ADC ESP32 sangat rentan terhadap *noise* dari catu daya USB dan radio Wi-Fi. Teknik paling ringan untuk sinyal lambat (suhu, cahaya, potensiometer) adalah **Moving Average** atas $M$ sampel terakhir:

$$
\bar{x}[n] = \frac{1}{M} \sum_{k=0}^{M-1} x[n-k]
$$

Untuk *white noise* acak yang tidak berkorelasi, rata-rata $M$ sampel menurunkan simpangan baku *noise* dengan faktor $\frac{1}{\sqrt{M}}$. Pada skrip simulasi [`adc_nyquist_sim.py`](content/chapter-07/src/adc_nyquist_sim.py) terhadap dataset sintetis [`telemetry.csv`](content/chapter-07/telemetry.csv), *moving average* $N=4$ menurunkan simpangan baku dari **$21{,}32\text{ mV}$ menjadi $2{,}30\text{ mV}$**.

### 6. Implementasi Praktis: ADC Potensiometer Mengatur PWM LED

**Spesifikasi Target (`ESP32-DevKitC V4`)**:
- **BOM**: 1x `ESP32-DevKitC V4`, 1x Potensiometer $10\text{ k}\Omega$, 1x LED, 1x Resistor $220\,\Omega$.
- **Pin Mapping**:
  - Potensiometer: ujung ke `3V3` dan `GND`, pin tengah (*wiper*) ke `GPIO 34` (`ADC1_CH6`)
  - LED: `GPIO 25` $\rightarrow$ Resistor $220\,\Omega$ $\rightarrow$ Anoda LED $\rightarrow$ Katoda $\rightarrow$ `GND`
- **Firmware & Simulasi**: [`ex01_adc_pwm_dimmer.ino`](content/chapter-07/src/ex01_adc_pwm_dimmer/ex01_adc_pwm_dimmer.ino) + Wokwi [`wokwi_diagram.json`](content/chapter-07/src/wokwi_diagram.json). Firmware membaca `analogReadMilliVolts(34)` tiap $50\text{ ms}$, menghitung *moving average* 8-sampel memakai *circular buffer* tanpa *loop* penjumlahan ulang, lalu memetakannya ke PWM 10-bit (`0..1023`) pada $5\text{ kHz}$.
- **Status Verifikasi**: Skrip [`adc_nyquist_sim.py`](content/chapter-07/src/adc_nyquist_sim.py) telah dijalankan di Python 3.12.10 (`outputs.md`); firmware `.ino` berstatus **Belum diuji** di server ini.

### 7. Common Mistakes & Troubleshooting

| Gejala Masalah | Penyebab Umum | Solusi |
| --- | --- | --- |
| Pembacaan ADC gagal / selalu 0 saat Wi-Fi menyala | Memakai pin `ADC2` (misal `GPIO 4` atau `26`) | Pindahkan sensor analog ke kanal `ADC1` (`GPIO 32–39`) |
| Nilai tegangan melenceng ratusan mV | Memakai `raw * 3.3 / 4095` tanpa koreksi referensi/non-linearitas | Gunakan `analogReadMilliVolts()` + jaga sinyal di area linier ($0{,}2\dots 3{,}0\text{ V}$) |
| Error kompilasi `ledcSetup was not declared` | Memakai API v2.x pada board package Arduino-ESP32 v3.x | Gunakan `ledcAttach(pin, freq, res)` dan `ledcWrite(pin, duty)` untuk v3.x |
| LED berkedip kasar saat redup | Frekuensi PWM terlalu rendah (misal $20\text{ Hz}$) | Naikkan frekuensi PWM ke $1\text{--}5\text{ kHz}$ |

### 8. Real-World Applications

- **Telecommunications RF Power & RSSI Envelope Sampling**: Menentukan laju *sampling* ADC yang tepat agar variasi cepat sinyal tidak mengalami *aliasing*.
- **Smart Greenhouse Lighting**: Mengatur intensitas *grow-light* LED secara proporsional melalui PWM berdasarkan pembacaan sensor cahaya analog yang sudah difilter.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-07/exercises.md)):
1. Perhitungan resolusi LSB ADC (10-bit vs 12-bit vs 16-bit), *duty cycle* PWM, dan *trade-off* frekuensi LEDC.
2. Identifikasi masalah `ADC2` + Wi-Fi dan batas non-linearitas ESP32.
3. Perhitungan frekuensi *aliasing* Nyquist pada beberapa skenario *undersampling*.
4. Simulasi Python dengan [`adc_nyquist_sim.py`](content/chapter-07/src/adc_nyquist_sim.py) serta Mini Challenge pemetaan non-linier (*gamma correction*) pada kecerahan LED PWM.

## Tugas

Bangun **Sistem Akuisisi Sinyal Analog Terfilter & Pengendali PWM Dual-Channel** (detail di tab **Tugas & Rubrik** — [assignment.md](content/chapter-07/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Pemilihan pin ADC1 & perhitungan kuantisasi | 25 | Wajib memakai ADC1, atenuasi tepat, perhitungan LSB dan ketidakpastian kuantisasi akurat |
| Desain filter noise & analisis sampling | 25 | Implementasi *moving average* non-blocking dan justifikasi laju sampling vs kriteria Nyquist |
| Konfigurasi LEDC PWM & pemetaan duty cycle | 30 | Resolusi/frekuensi PWM tepat, pemetaan aman (*clamping*), tanpa `delay()` |
| Dokumentasi, simulasi & kejujuran bukti | 20 | Skema wiring lengkap, log aktual/expected output terpisah jelas |

## Ringkasan

- ADC melakukan **sampling** (waktu) dan **kuantisasi** (amplitudo); ADC 12-bit pada $3{,}3\text{ V}$ memiliki $1\text{ LSB} \approx 0{,}806\text{ mV}$.
- Pada ESP32 klasik, selalu gunakan **`ADC1` (`GPIO 32–39`)** agar tidak bentrok dengan Wi-Fi, dan manfaatkan `analogReadMilliVolts()` untuk akurasi yang lebih baik.
- Penuhi kriteria Nyquist ($f_s > 2 f_{\max}$) untuk mencegah *aliasing*, dan gunakan *moving average* untuk meredam *noise* acak.
- Analisis kuantisasi, *moving average*, dan pembuktian *aliasing* telah diverifikasi secara *software* di Python (`outputs.md`); eksekusi `.ino` di Wokwi/hardware belum dijalankan di server ini.

## Referensi

1. Espressif Systems, *ESP-IDF Analog to Digital Converter (ADC) Calibration & Driver*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/adc_oneshot.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/adc_oneshot.html) (diperiksa 2026-11-10).
2. Espressif Systems, *Arduino-ESP32 LEDC (PWM) API Documentation*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html) (diperiksa 2026-11-10).
3. Wokwi Documentation, *Potentiometer Simulation Reference*, [https://docs.wokwi.com/parts/wokwi-potentiometer](https://docs.wokwi.com/parts/wokwi-potentiometer) (diperiksa 2026-11-10).


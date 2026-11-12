# Chapter 10 — Embedded Foundations Capstone

## Overview

**Capstone Level 1** mengintegrasikan seluruh kompetensi Chapter 01 sampai Chapter 09 menjadi satu sistem nyata yang utuh: **Smart Environmental Monitoring & Local Control System** (*low-voltage DC*). Proyek ini membaca kondisi lingkungan menggunakan sensor analog terkalibrasi pada ESP32, memfilter *noise* secara *non-blocking*, menerima konfigurasi mode dari tombol ter-*debounce*, menjaga keselamatan lewat *safety interlock*, menggerakkan *Actuator* lokal dengan *hysteresis*, dan mengeluarkan *Serial telemetry* terstruktur—**tanpa mensyaratkan Wi-Fi, MQTT, atau cloud** (yang akan menjadi fokus Level 2).

## Prasyarat

- Menyelesaikan fondasi Level 1 ([Chapter 01](#/chapter/1) hingga [Chapter 09](#/chapter/9)), terutama keselamatan low-voltage DC, batas pin `ESP32-DevKitC V4`, `millis()` non-blocking, *debouncing*, `ADC1` + `LEDC PWM`, kalibrasi dua titik, serta kontrol histeresis dan *fail-safe*.

## Tujuan pembelajaran

Setelah menyelesaikan proyek capstone ini, mahasiswa mampu:

1. **Mengintegrasikan** akuisisi sensor analog (`ADC1`), input digital ter-*debounce*, *safety interlock*, dan aktuasi PWM dalam satu arsitektur *Firmware* modular *non-blocking*.
2. **Menerapkan** kalibrasi dua titik, deteksi kerusakan sensor (`NaN`), dan kontrol histeresis multi-mode (`AUTO_NORMAL`, `AUTO_STRICT`, `MANUAL_ON`, `FAULT_SAFE`).
3. **Merancang** skema *low-voltage DC* lengkap beserta *Bill of Materials* (BOM), *pin mapping*, serta daftar periksa keselamatan (*safety checklist*).
4. **Melaksanakan** pengujian berbasis *test cases* (*Simulator-First* atau *Hardware* opsional) dan menyusun laporan teknis yang jujur terhadap bukti uji.

## Konsep dan teori

### 1. Project Requirements (Fungsional & Non-Fungsional)

| ID | Kebutuhan | Spesifikasi Terukur |
| --- | --- | --- |
| `REQ-F1` | Akuisisi & Kalibrasi | Membaca tegangan sensor tiap `100 ms`, filter *moving average* `N=8`, terkalibrasi ke $^\circ\text{C}$ |
| `REQ-F2` | Pemilihan Mode Lokal | Tombol mode ter-*debounce* (`50 ms`) menggeser mode: `AUTO_NORMAL` ($28\dots 30\,^\circ\text{C}$), `AUTO_STRICT` ($25\dots 27\,^\circ\text{C}$), `MANUAL_ON` |
| `REQ-F3` | Kontrol Histeresis & PWM | Mengendalikan kipas/LED beban via `LEDC` (`5 kHz`, 8-bit) tanpa *chattering* |
| `REQ-F4` | Interlock & Fail-Safe | Saklar *interlock* terbuka atau sensor `NaN` memaksa kipas `OFF` dan menyalakan buzzer alarm |
| `REQ-F5` | Serial Telemetry | Mencetak payload JSON ke `UART0` (`115200 baud`) setiap `1000 ms` menggunakan `snprintf()` |
| `REQ-NF1` | Non-Blocking & Aman | Nol `delay()` di `loop()`; seluruh rangkaian hanya memakai *low-voltage DC* ($3{,}3\text{ V}/5\text{ V}$) |

### 2. System Architecture & Wiring (ESP32-DevKitC V4)

![Arsitektur dan pemetaan pin Capstone Smart Environmental Monitoring pada ESP32-DevKitC V4](content/chapter-10/diagram.svg)

**Bill of Materials (BOM — Path B Hardware Opsional / Path A Wokwi Virtual)**:

| Komponen | Jumlah | Spesifikasi / Catatan Keselamatan |
| --- | --- | --- |
| Board MCU | 1 | `ESP32-DevKitC V4 (WROOM-32)` (3,3 V logic) |
| Sensor Suhu | 1 | Modul NTC 10k ($\beta=3950\text{ K}$) + resistor seri $10\text{ k}\Omega$ ($1\%$) |
| Push Button & Slide Switch | 2 | 1x tombol mode, 1x saklar *interlock* |
| LED Indikator + Resistor | 2 set | 2x LED + 2x resistor $220\,\Omega$ |
| Buzzer Alarm | 1 | Active buzzer $3{,}3\text{ V}$ (atau via NPN driver jika $>12\text{ mA}$) |
| Driver Aktuator (untuk Kipas DC fisik) | 1 set | Logic-level N-MOSFET + $R_{\text{gate}} = 220\,\Omega$ + $R_{\text{pd}} = 10\text{ k}\Omega$ + 1N5819 *flyback* + suplai $5\text{ V}$ |

**Pin Mapping Table**:

| Sinyal | Pin ESP32 | Mode / Periferal | Keterangan |
| --- | --- | --- | --- |
| `PIN_NTC_ADC` | `GPIO 34` | `ADC1_CH6` (`ADC_11db`) | Input-only, aman Wi-Fi, rentang valid $100\dots 3200\text{ mV}$ |
| `PIN_MODE_BUTTON` | `GPIO 27` | `INPUT_PULLUP` | *Active-low* ke `GND`, *debounce* $50\text{ ms}$ |
| `PIN_INTERLOCK` | `GPIO 14` | `INPUT_PULLUP` | `LOW` = aman tertutup, `HIGH` = terbuka (*fault*) |
| `PIN_FAN_PWM` | `GPIO 25` | `LEDC PWM` (`5 kHz`, 8-bit) | Ke *gate* MOSFET driver (atau LED beban di Wokwi) |
| `PIN_STATUS_LED` | `GPIO 26` | `OUTPUT` | Kedip $1\text{ s}$ (Normal), $250\text{ ms}$ (Strict), Solid (Manual), Mati (Fault) |
| `PIN_ALARM_BUZZER` | `GPIO 18` | `OUTPUT` | `HIGH` saat `FAULT_SAFE` atau suhu $\ge 45\,^\circ\text{C}$ |

### 3. Implementasi Firmware Modular

Kode dibagi menjadi dua berkas bersih agar mudah dirawat:
1. [`env_config.h`](content/chapter-10/src/capstone_env_monitor/env_config.h): Konstanta pin, parameter Beta + kalibrasi 2-titik (`CAL_SLOPE = 1.0381`, `CAL_OFFSET = -1.4740`), batas histeresis, dan `enum class ControlMode`.
2. [`capstone_env_monitor.ino`](content/chapter-10/src/capstone_env_monitor/capstone_env_monitor.ino): Alur utama non-blocking:
   - `handleModeButton(now)`: *debounce* 50 ms + rotasi mode (dinonaktifkan saat `FAULT_SAFE`).
   - `convertMvToCalibratedC(mv)`: deteksi *open/short* + rumus Beta + kalibrasi dua titik.
   - `evaluateControl(interlockOpen)`: prioritas keselamatan (*Interlock* $\rightarrow$ *Sensor Fault* $\rightarrow$ Mode Kontrol Histeresis).
   - `updateStatusLed(now)` & blok telemetry JSON tiap $1000\text{ ms}$ via `snprintf()`.

### 4. Alternatif Simulasi & Acceptance Test Cases

- **Simulasi Wokwi (Path A)**: Gunakan [`wokwi_diagram.json`](content/chapter-10/src/wokwi_diagram.json) bersama `capstone_env_monitor.ino` dan `env_config.h`.
- **Acceptance Test Harness Python (`capstone_logic_test.py`)**: Menguji 13 langkah transisi pada [`telemetry.csv`](content/chapter-10/telemetry.csv) (`source=synthetic`) yang mencakup 7 skenario uji utama:
  1. `TC-01`: Inisialisasi awal `AUTO_NORMAL` pada $24{,}48\,^\circ\text{C}$ $\rightarrow$ kipas `OFF`.
  2. `TC-02`: Suhu naik ke $30{,}58\,^\circ\text{C}$ ($\ge 30{,}0$) $\rightarrow$ kipas `ON`.
  3. `TC-03`: Suhu turun ke $28{,}80\,^\circ\text{C}$ (di dalam *deadband* $28\dots 30\,^\circ\text{C}$) $\rightarrow$ kipas **tetap `ON`**.
  4. `TC-04`: Suhu turun ke $27{,}05\,^\circ\text{C}$ ($\le 28{,}0$) $\rightarrow$ kipas `OFF`.
  5. `TC-05`: Tombol mode ditekan $\rightarrow$ `AUTO_STRICT` ($25\dots 27\,^\circ\text{C}$); pada $27{,}92\,^\circ\text{C}$ kipas `ON`, bertahan di $26{,}19\,^\circ\text{C}$, mati di $24{,}48\,^\circ\text{C}$.
  6. `TC-06`: Tombol mode ditekan $\rightarrow$ `MANUAL_ON` (kipas `ON`), lalu *interlock* dibuka $\rightarrow$ `FAULT_SAFE` seketika (`fan=OFF, alarm=true`).
  7. `TC-07`: Sensor keluar rentang ($3280\text{ mV}$) $\rightarrow$ `FAULT_SAFE` (`temp_c: null`, `fault: "SENSOR_FAULT_NAN"`), dan pulih saat nilai kembali normal.

Seluruh 13/13 langkah lulus pada eksekusi [`capstone_logic_test.py`](content/chapter-10/src/capstone_logic_test.py) (lihat [`outputs.md`](content/chapter-10/outputs.md)). Kompilasi `.ino` dan uji Wokwi/hardware tetap berstatus **Belum diuji** di server ini.

### 5. Verification Checklist & Technical Report Template

Sebelum menyatakan sistem Anda siap dinilai, periksa:
- [ ] Seluruh nilai pin cocok dengan `ESP32-DevKitC V4` (tidak memakai `GPIO 6–11` atau `ADC2`).
- [ ] Tidak ada `delay()` di `loop()` dan tidak ada konkatenasi `String` di *heap*.
- [ ] Jalur Path B fisik memakai suplai eksternal + MOSFET driver + *flyback diode* + *common `GND`*.
- [ ] Laporan memuat: (1) Ringkasan Sistem & Requirements, (2) BOM & Wiring Table, (3) Penjelasan Kalibrasi & Histeresis, (4) Tabel Hasil Test Case (Expected vs Actual), (5) Status Verifikasi & Keterbatasan.

### 6. Common Mistakes & Troubleshooting Capstone

- **Lupa menyalin `env_config.h` ke folder/tab proyek**: Menyebabkan error `env_config.h: No such file or directory`.
- **Mode terkunci di `FAULT_SAFE` di Wokwi**: Pastikan *slide switch* interlock (`GPIO 14`) terhubung ke `GND` (`LOW`) untuk kondisi normal tertutup.
- **Kipas fisik tidak mati saat sensor dicabut**: Pastikan kabel analog tidak *floating* dekat rel tengah; tambahkan *pull-up* atau cek batas `ADC_MIN_MV` / `ADC_MAX_MV`.

### 7. Real-World Applications

Sistem ini merupakan prototipe fungsional utuh (*standalone local smart controller*) untuk **kabinet baterai BTS**, **ruang server mini**, maupun **rumah kaca pertanian** sebelum dihubungkan ke jaringan Wi-Fi dan MQTT pada **Level 2**.

## Latihan

Latihan kesiapan capstone tersedia pada tab **Exercises** ([exercises.md](content/chapter-10/exercises.md)):
1. Verifikasi kesesuaian syarat integrasi antar-chapter (03–09) pada arsitektur `capstone_env_monitor.ino`.
2. Skenario *fault injection* (putus kabel NTC, *interlock* terbuka saat `MANUAL_ON`, *switch bounce* tombol mode).
3. Menjalankan [`capstone_logic_test.py`](content/chapter-10/src/capstone_logic_test.py) dan memodifikasi batas suhu preset `AUTO_STRICT`.

## Tugas

Selesaikan **Proyek Capstone Level 1: Smart Environmental Monitoring & Local Control System** beserta Laporan Teknis (template & kriteria lengkap di tab **Tugas & Rubrik** — [assignment.md](content/chapter-10/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Arsitektur, BOM & keselamatan wiring DC | 20 | Diagram blok, BOM lengkap, pin mapping valid, driver & *common GND* aman |
| Akuisisi terkalibrasi & kontrol histeresis | 25 | Pembacaan ADC1 terfilter, kalibrasi 2-titik, histeresis bebas *chattering* |
| Firmware non-blocking, FSM & fail-safe | 25 | Modular `.h`, bebas `delay()`, *debounce* tombol, *interlock* & fault `NaN` aman |
| Pengujian test-case, dokumentasi & kejujuran | 30 | Hasil uji seluruh *test cases* terdokumentasi rapi dengan bukti dan status verifikasi jujur |

## Ringkasan

- Capstone Level 1 menyatukan seluruh fondasi: *requirements*, keselamatan *low-voltage DC*, pin `ESP32-DevKitC V4`, C++ modular non-blocking, *debouncing*, `ADC1` + `LEDC PWM`, kalibrasi dua titik, serta kontrol histeresis + *fail-safe*.
- *Acceptance test harness* Python (`capstone_logic_test.py`) memverifikasi 13/13 langkah logika kendali dan pemulihan *fault* secara deterministik (`outputs.md`).
- Kode `.ino` dan skema Wokwi siap diuji pada komputer/simulator pembelajar (berstatus **Belum diuji** di server ini). Selanjutnya di **Level 2**, sistem lokal ini akan dihubungkan ke jaringan IP, Wi-Fi, dan protokol MQTT.

## Referensi

1. Espressif Systems, *ESP32 Series Datasheet & ESP-IDF Documentation*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html) (diperiksa 2026-11-10).
2. Espressif Systems, *Arduino-ESP32 API Reference (v3.x)*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/](https://docs.espressif.com/projects/arduino-esp32/en/latest/) (diperiksa 2026-11-10).
3. Wokwi Documentation, *ESP32 Simulation & Parts Reference*, [https://docs.wokwi.com/guides/esp32](https://docs.wokwi.com/guides/esp32) (diperiksa 2026-11-10).
4. National Institute of Standards and Technology (NIST), *NIST Cybersecurity for IoT Program*, [https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program](https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program) (diperiksa 2026-11-10).


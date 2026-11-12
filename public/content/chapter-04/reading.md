# Chapter 04 — Microcontrollers, ESP32 & Development Boards

## Overview

Di balik hampir setiap node sensor IoT modern terdapat sebuah **Microcontroller Unit (MCU)**. Namun, pemula sering menyamakan MCU dengan komputer papan tunggal (*Single-Board Computer / SBC*) seperti Raspberry Pi, atau menganggap semua papan berlabel "ESP32" identik sehingga sembarang menyalin nomor pin dari tutorial internet. Akibatnya beragam: board gagal *boot*, *flash* korup, atau kode gagal dikompilasi karena perbedaan varian chip.

Chapter ini membedah arsitektur internal *Microcontroller*, membandingkan keluarga chip **ESP32** (`ESP32`, `ESP32-S3`, `ESP32-C3`), menjelaskan pembatasan pin pada papan pengembangan acuan (**ESP32-DevKitC V4 / WROOM-32**), membandingkan *Arduino Framework* dan *ESP-IDF*, serta membahas alur *flashing*, *boot mode*, dan *Serial Monitor*.

## Prasyarat

- Memahami batas tegangan ($3{,}3\text{ V}$), batas arus GPIO, dan resistor pembatas arus dari [Chapter 03](#/chapter/3).
- Disarankan meninjau panduan instalasi editor/simulator pada [Getting Started](#/getting-started).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Membedakan** arsitektur *Microcontroller* (MCU) dengan *Microprocessor* / SBC berdasarkan integrasi memori, konsumsi daya, dan peran sistem operasi.
2. **Menjelaskan** fungsi CPU, *Flash*, *SRAM*, dan *peripherals* (GPIO, ADC, PWM, UART, I2C, SPI) di dalam SoC ESP32.
3. **Mengidentifikasi** perbedaan varian keluarga ESP32 (`ESP32`, `ESP32-S3`, `ESP32-C3`) serta batasan pin (*SPI Flash pins*, *input-only*, *strapping pins*) dari datasheet resmi.
4. **Memilih** *framework* (*Arduino* vs *ESP-IDF*), menyusun *development environment*, serta mendiagnosis masalah *flashing*, *boot mode*, dan *Serial Monitor*.

## Konsep dan teori

### 1. Microcontroller (MCU) vs Microprocessor (MPU / SBC)

Perbedaan paling mendasar bukan pada "kecepatan", melainkan **tingkat integrasi dan tujuan desain**:

- **Microcontroller (MCU)**: Mengintegrasikan inti CPU, memori program non-volatil (*Flash*), memori kerja volatil (*SRAM*), osilator, dan *peripherals* I/O ke dalam satu keping silikon (*System-on-Chip / SoC*). Dirancang untuk mengendalikan perangkat keras secara langsung, *boot* dalam milidetik, dan berdaya sangat rendah.
- **Microprocessor (MPU) / Single-Board Computer (SBC)**: CPU berkinerja tinggi yang membutuhkan RAM eksternal (DDR) dan penyimpanan eksternal (eMMC/microSD) di luar chip. Umumnya menjalankan sistem operasi penuh seperti Linux, cocok untuk *Edge Gateway*, basis data lokal, atau pemrosesan citra/video, tetapi membutuhkan daya jauh lebih besar (watt vs miliwatt).

### 2. Arsitektur Internal MCU: CPU, Memori, dan Peripherals

Di dalam satu MCU terdapat tiga subsistem utama yang terhubung melalui *internal bus*:

1. **CPU Core**: Mengeksekusi instruksi mesin dari *Firmware* (misalnya arsitektur Xtensa LX6 dual-core pada ESP32 klasik, atau RISC-V 32-bit pada ESP32-C3).
2. **Subsistem Memori**:
   - **Flash Memory (Non-Volatil, misal 4 MiB)**: Menyimpan kode program (*Firmware*), konstanta (`const`), dan partisi data persisten (NVS/SPIFFS/LittleFS). Data tetap tersimpan saat daya dimatikan.
   - **SRAM (Volatil, misal 520 KiB pada ESP32 klasik)**: Menyimpan variabel runtime, *stack* pemanggilan fungsi, dan *heap* alokasi dinamis. Isinya hilang saat reset atau daya putus.
   - **ROM Bootloader**: Memori baca-saja permanen dari pabrik yang menangani proses *boot* awal dan pemrograman ulang (*UART/USB download mode*).
3. **Peripherals**: Blok perangkat keras khusus untuk berkomunikasi dengan dunia luar tanpa membebani CPU penuh, antara lain **GPIO** (digital I/O), **ADC** (analog ke digital), **LEDC/PWM**, **Timers**, **UART**, **I2C**, **SPI**, serta subsistem radio **Wi-Fi / Bluetooth LE**.

### 3. Keluarga ESP32 & Perbedaan Varian

**Peringatan Penting**: Nama "ESP32" sekarang merujuk pada **keluarga besar SoC**, bukan satu pinout tunggal! Menganggap kode atau nomor pin `ESP32` klasik otomatis berlaku di `ESP32-C3` atau `ESP32-S3` adalah sumber kesalahan fatal.

| Fitur | ESP32 (WROOM-32) | ESP32-S3 | ESP32-C3 |
| --- | --- | --- | --- |
| **Arsitektur CPU** | Xtensa LX6 Dual-Core (hingga 240 MHz) | Xtensa LX7 Dual-Core + ekstensi vektor AI (240 MHz) | RISC-V RV32IMC Single-Core (hingga 160 MHz) |
| **SRAM Internal** | 520 KiB | 512 KiB | 400 KiB |
| **USB Native** | Tidak (butuh chip bridge CP2102 / CH340) | Ya (USB OTG + Serial/JTAG built-in) | Ya (USB Serial/JTAG built-in) |
| **Wi-Fi & BLE** | Wi-Fi 4 + Bluetooth Classic + BLE 4.2 | Wi-Fi 4 + BLE 5.0 | Wi-Fi 4 + BLE 5.0 |
| **Pin SPI Flash Internal** | GPIO 6–11 | GPIO 26–32 | GPIO 12–17 |
| **Pin Input-Only** | GPIO 34, 35, 36, 39 | Tidak ada | Tidak ada |
| **Strapping Pins** | GPIO 0, 2, 5, 12, 15 | GPIO 0, 3, 45, 46 | GPIO 2, 8, 9 |

Perhatikan contoh pada tabel: **`GPIO 12`** adalah pin *SPI Flash* pada **ESP32-C3** (haram dipakai!), *strapping pin* pengatur tegangan flash pada **ESP32 klasik**, namun merupakan GPIO biasa yang aman pada **ESP32-S3**! Hasil eksekusi skrip audit [`board_matrix.py`](content/chapter-04/src/board_matrix.py) memperlihatkan validasi aturan ini secara otomatis.

![Perbandingan arsitektur MCU vs SBC dan klasifikasi pin ESP32-DevKitC V4](content/chapter-04/diagram.svg)

### 4. Board Acuan Level 1: ESP32-DevKitC V4 (WROOM-32) & Batasan Pin

Untuk konsistensi seluruh praktik Level 1 (Path A Wokwi maupun Path B Hardware opsional), board acuan yang digunakan adalah **ESP32-DevKitC V4 dengan modul ESP32-WROOM-32** (38 pin, 3,3 V logic, USB-to-UART bridge). Pembaca yang memakai board lain **wajib** mencocokkan *pinout* dari datasheet produsen board tersebut.

Aturan pembagian pin pada **ESP32-DevKitC V4 (WROOM-32)**:
- **Pin Terlarang (GPIO 6–11)**: Terhubung langsung ke chip *SPI Flash* internal. Menggunakan pin ini sebagai GPIO menyebabkan *crash* / *Guru Meditation Error* / *boot loop*.
- **Pin Input-Only (GPIO 34, 35, 36/VP, 39/VN)**: Hanya memiliki sirkuit input (sangat baik untuk pembacaan sensor analog ADC1 atau input digital dengan resistor eksternal). Tidak dapat dikonfigurasi sebagai `OUTPUT` dan **tidak memiliki resistor *internal pull-up / pull-down***.
- **Strapping Pins (GPIO 0, 2, 5, 12, 15)**: Dibaca oleh *ROM bootloader* saat reset untuk menentukan mode *boot* dan tegangan *flash*. Menarik `GPIO 12` ke `HIGH` saat boot pada modul 3,3 V dapat membuat flash gagal dibaca; menarik `GPIO 0` ke `LOW` saat reset memaksa chip masuk ke *Download Mode*.
- **Jalur Serial Utama (GPIO 1 TX0, GPIO 3 RX0)**: Dipakai oleh *USB-to-UART bridge* untuk *flashing* dan `Serial.print()`. Hindari menyambungkan beban eksternal ke pin ini jika masih membutuhkan *Serial Monitor*.
- **GPIO Aman Umum**: `GPIO 4, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33` (catatan: pada varian *WROVER* dengan PSRAM, GPIO 16 dan 17 terpakai oleh PSRAM).

### 5. Arduino Framework vs ESP-IDF

| Aspek | Arduino-ESP32 Framework | Espressif ESP-IDF (Native SDK) |
| --- | --- | --- |
| **Abstraksi** | API sederhana (`setup()`, `loop()`, `pinMode()`, `digitalWrite()`) | Akses penuh FreeRTOS, driver HAL, menuconfig, dan partisi flash |
| **Kurva belajar** | Cepat untuk prototipe & pembelajaran dasar | Lebih curam; membutuhkan pemahaman C/RTOS lebih dalam |
| **Fondasi di balik layar** | Berjalan di atas ESP-IDF dan FreeRTOS | SDK resmi langsung dari Espressif |
| **Kapan dipilih?** | Level 1–2, prototipe cepat, ekosistem library Arduino luas | Produk komersial, optimasi daya/memori ekstrem, keamanan lanjut |

Pada Level 1 kita menggunakan **Arduino-ESP32** (melalui Arduino IDE 2.x, PlatformIO, atau Wokwi) agar fokus tertuju pada konsep *embedded*, kelistrikan, dan logika *Firmware* tanpa tenggelam dalam kompleksitas konfigurasi *build system* sejak hari pertama.

### 6. Development Environment, Flashing, Boot Modes & Serial Monitor

Alur kerja pengembangan *Firmware* mengikuti siklus: **Edit Kode $\rightarrow$ Compile (menghasilkan biner `.bin`) $\rightarrow$ Flash via UART/USB $\rightarrow$ Monitor Output via Serial**.

**Boot Modes ESP32 Klasik**:
1. **Normal Execution (SPI Flash Boot)**: `GPIO 0 = HIGH` (ditarik *pull-up* internal/eksternal) saat `EN` (*Reset*) dilepas $\rightarrow$ menjalankan *Firmware* pengguna.
2. **Download / Flashing Mode**: `GPIO 0 = LOW` saat `EN` dilepas $\rightarrow$ menunggu unggahan biner baru melalui UART0. Pada *DevKit* modern, rangkaian transistor otomatis (*auto-reset DTR/RTS*) menekan kondisi ini, tetapi pada sebagian papan Anda mungkin perlu **menahan tombol `BOOT` (GPIO 0), menekan `EN/RST` sebentar, lalu melepas `BOOT`**.

### 7. Implementasi Praktis: Path A (Simulasi) & Path B (Hardware Opsional)

**Spesifikasi Target & BOM**:
- **Board Target**: `ESP32-DevKitC V4` (`ESP32-WROOM-32`, FQBN: `esp32:esp32:esp32`)
- **BOM Tambahan**: 1x Resistor $220\,\Omega$, 1x LED Hijau, kabel *jumper*, kabel USB data (untuk Path B)
- **Pin Mapping**: `GPIO 25` $\rightarrow$ Resistor $220\,\Omega$ $\rightarrow$ Anoda LED $\rightarrow$ Katoda LED $\rightarrow$ `GND`
- **Toolchain Target**: Arduino IDE 2.x + `esp32 by Espressif Systems` (v3.x) atau simulator Wokwi (`board-esp32-devkit-c-v4`)

Source code lengkap tersedia pada [`ch04_board_probe.ino`](content/chapter-04/src/ch04_board_probe/ch04_board_probe.ino) dan konfigurasi simulasi Wokwi pada [`wokwi_diagram.json`](content/chapter-04/src/wokwi_diagram.json).

**Catatan Status Verifikasi**: Skrip audit pin [`board_matrix.py`](content/chapter-04/src/board_matrix.py) telah dieksekusi nyata (lihat [`outputs.md`](content/chapter-04/outputs.md)). Kode `.ino` dan skema Wokwi berstatus **Belum diuji** di server ini karena *compiler* `arduino-cli` dan `wokwi-cli` tidak terpasang.

### 8. Common Mistakes & Troubleshooting

| Gejala Error | Kemungkinan Penyebab | Langkah Diagnosis |
| --- | --- | --- |
| Port COM / `/dev/ttyUSB*` tidak muncul | Kabel USB hanya kabel *charging* (tanpa jalur data), atau driver CP210x/CH34x belum terpasang | Ganti kabel data; periksa *Device Manager* / `lsusb` |
| `Failed to connect to ESP32: Timed out waiting for packet header` | Board tidak masuk *Download Mode* atau port serial dipakai aplikasi lain | Tutup Serial Monitor lain; tahan tombol `BOOT` saat muncul `Connecting...` |
| Serial Monitor menampilkan karakter acak (`⸮⸮⸮`) | Ketidakcocokan *baud rate* antara `Serial.begin(115200)` dan monitor | Samakan *baud rate* Serial Monitor ke `115200` (catatan: pesan ROM awal ESP32 selalu di `74880`/`115200` baud) |
| Board terus reset (*Brownout detector was triggered*) | Suplai USB lemah, kabel terlalu tipis, atau beban arus tinggi terhubung ke pin `3V3` | Lepas beban berat, ganti kabel/port USB berarus cukup |

### 9. Real-World Applications

- **Pemilihan Board Industri & Agrikultur**: Memilih `ESP32-C3` berbiaya rendah untuk node sensor sederhana berdaya hemat, versus `ESP32-S3` ketika sistem membutuhkan pemrosesan sinyal audio/kamera ringan di *Edge* (*TinyML*).
- **Desain PCB Custom Telekomunikasi**: Memahami *strapping pins* dan *SPI Flash pins* mencegah kesalahan tata letak PCB yang menyebabkan ribuan unit modul gagal menyala setelah dirakit di pabrik.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-04/exercises.md)):
1. Perbandingan arsitektur MCU vs SBC untuk *node sensor* vs *Edge Gateway*.
2. Audit alokasi pin lintas varian (`ESP32`, `ESP32-S3`, `ESP32-C3`) untuk menghindari *SPI Flash* dan *strapping pins*.
3. Diagnosis skenario *troubleshooting* *flashing*, *brownout*, dan *baud rate mismatch*.
4. Menjalankan dan memperluas skrip [`board_matrix.py`](content/chapter-04/src/board_matrix.py) serta menguji sketsa di Wokwi (Path A) atau board fisik (Path B).

## Tugas

Susun **Dokumen Pemilihan Board, Peta Pin Aman (*Pinout Allocation Table*), dan Rencana Verifikasi Bring-Up** untuk sebuah node ESP32 (detail lengkap di tab **Tugas & Rubrik** — [assignment.md](content/chapter-04/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Justifikasi pemilihan varian chip & framework | 25 | Ketepatan memilih antara ESP32/S3/C3 dan Arduino/ESP-IDF sesuai kebutuhan |
| Alokasi pin aman & analisis batasan | 30 | Tidak melanggar pin Flash/strapping/input-only; disertai rujukan datasheet spesifik |
| Kelengkapan BOM, wiring & prosedur bring-up | 25 | Pin mapping lengkap, resistor pengaman LED, langkah build/flash/monitor jelas |
| Troubleshooting & kejujuran status uji | 20 | Rencana diagnosis kesalahan boot/serial dan pemisahan jelas bukti uji vs teoretis |

## Ringkasan

- MCU menyatukan CPU, *Flash*, *SRAM*, dan *peripherals* dalam satu chip hemat daya untuk kontrol langsung; SBC/MPU cocok untuk beban setingkat OS Linux.
- Keluarga ESP32 (`ESP32`, `ESP32-S3`, `ESP32-C3`) memiliki arsitektur CPU, dukungan USB, pin *SPI Flash*, dan *strapping pins* yang berbeda—**wajib rujuk datasheet varian spesifik**.
- Pada `ESP32-DevKitC V4`, hindari `GPIO 6–11` (*SPI Flash*), perhatikan sifat *input-only* `GPIO 34–39`, dan waspadai *strapping pins* (`0, 2, 5, 12, 15`).
- Audit aturan pin melalui `board_matrix.py` telah dieksekusi di Python; kompilasi firmware `.ino` dan uji board fisik tetap berstatus **Belum diuji** di lingkungan server ini.

## Referensi

1. Espressif Systems, *ESP32 Series Datasheet & Pin List*, [https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) (diperiksa 2026-11-10).
2. Espressif Systems, *ESP-IDF Programming Guide — ESP32-S3 & ESP32-C3 Targets*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html) (diperiksa 2026-11-10).
3. Espressif Systems, *Arduino-ESP32 Official Documentation*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/](https://docs.espressif.com/projects/arduino-esp32/en/latest/) (diperiksa 2026-11-10).
4. Wokwi Documentation, *ESP32 Simulation Guide*, [https://docs.wokwi.com/guides/esp32](https://docs.wokwi.com/guides/esp32) (diperiksa 2026-11-10).


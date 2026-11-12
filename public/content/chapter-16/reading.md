# Chapter 16 — UART, I2C & SPI

## Overview

Sensor cerdas (seperti BME280, MPU6050, modul GPS, kartu microSD, layar OLED/TFT, serta transceiver radio LoRa SX1278) tidak berkomunikasi menggunakan tegangan analog sederhana, melainkan bertukar data biner langsung antar-IC melalui bus komunikasi serial papan (*on-board / short-range wired buses*). Tiga antarmuka yang mendominasi *Embedded Systems* adalah **UART**, **I2C**, dan **SPI**.

Chapter ini membedah prinsip kerja sinkron vs asinkron, format *frame*, pengalamatan bus, kebutuhan resistor *pull-up*, mode *clock* SPI, pemetaan pin pada `ESP32-DevKitC V4`, perbandingan pemilihan bus, serta teknik *troubleshooting* ketika sensor tidak merespons.

## Prasyarat

- Memahami *pull-up resistor*, logika $3{,}3\text{ V}$, dan *common ground* dari [Chapter 03](#/chapter/3).
- Memahami peta pin aman `ESP32-DevKitC V4` dari [Chapter 04](#/chapter/4).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Membedakan** komunikasi **asinkron (UART)** dan **sinkron (I2C, SPI)** beserta format *frame*, peran sinyal *clock*, serta metode pengendalian aliran data.
2. **Menghitung** efisiensi *frame* UART (`8N1` vs `8E1`), *rise time* bus I2C berdasarkan resistor *pull-up* dan kapasitansi jalur, serta durasi transfer SPI.
3. **Memetakan** *wiring* dan konfigurasi pin `UART`, `I2C`, dan `SPI` yang benar pada `ESP32-DevKitC V4` tanpa melanggar pin terlarang/PSRAM.
4. **Mendiagnosis** kesalahan umum bus serial (TX/RX terbalik, *baud rate mismatch*, hilangnya *pull-up* I2C, konflik alamat 7-bit, dan salah mode `CPOL/CPHA` SPI).

## Konsep dan teori

### 1. Perbandingan Ringkas UART vs I2C vs SPI

| Aspek | UART (*Universal Async Rx/Tx*) | I2C (*Inter-Integrated Circuit*) | SPI (*Serial Peripheral Interface*) |
| --- | --- | --- | --- |
| **Sinkronisasi** | **Asinkron** (tanpa kabel *clock*) | **Sinkron** (`SCL` dari Master) | **Sinkron** (`SCLK` dari Master) |
| **Jumlah kabel data** | 2 (`TX`, `RX`) + `GND` | 2 (`SDA`, `SCL`) + `GND` | 4 (`MOSI`, `MISO`, `SCLK`, `CS`) + `GND` |
| **Topologi** | *Point-to-point* (1-ke-1) | Multi-slave via **alamat 7-bit** | Multi-slave via pin **`CS` terpisah** |
| **Tipe driver listrik** | Push-pull | **Open-drain** (**wajib pull-up!**) | Push-pull (kecepatan tinggi) |
| **Duplex** | *Full-duplex* | *Half-duplex* | *Full-duplex* |
| **Kecepatan umum** | $9600\dots 921600\text{ bps}$ | $100\text{ kHz}$ (Std), $400\text{ kHz}$ (Fast) | $1\text{ MHz}\dots 40\text{ MHz}+$ |
| **Contoh perangkat** | GPS NEO-6M, RS-485, Modem GSM | BME280, SHT31, OLED SSD1306, RTC | Kartu microSD, SX127x LoRa, Layar TFT |

![Perbandingan antarmuka UART, I2C open-drain dengan pull-up, dan SPI 4-kawat](content/chapter-16/diagram.svg)

### 2. UART: Format Frame & Crossover Wiring

Karena UART tidak memiliki kabel *clock*, pengirim dan penerima wajib menyepakati **baud rate** yang sama (misal `9600` atau `115200 bps`; selisih *clock* $> 2\text{--}3\%$ menyebabkan karakter korup).
- **Wiring Crossover**: Pin `TX` pengirim disambung ke `RX` penerima, dan `RX` pengirim ke `TX` penerima (ditambah `Common GND`).
- **Format Frame `8N1`**: 1 *Start bit* (`0`) + 8 *Data bits* (LSB dulu) + 0 *Parity bit* + 1 *Stop bit* (`1`) = **10 bit per 1 byte data** (efisiensi $8/10 = 80\%$). Jika memakai `8E1` (1 bit paritas genap), butuh 11 bit/byte ($72{,}7\%$).
- **Tiga UART ESP32**: `UART0` (`GPIO 1 TX0, 3 RX0`) dipakai USB Serial Monitor; `UART1` dan `UART2` dapat di-remapping ke hampir semua GPIO aman lewat matriks pin ESP32 (`Serial2.begin(9600, SERIAL_8N1, rxPin, txPin)`). *Peringatan*: pin default `UART2` (`GPIO 16/17`) bentrok dengan PSRAM jika Anda memakai modul **ESP32-WROVER**!

### 3. I2C: Open-Drain, Pull-Up Resistor & Bus Addressing

Bus I2C hanya memakai 2 jalur dua-arah: **`SDA`** (data) dan **`SCL`** (clock), yang pada `ESP32-DevKitC V4` secara default dipetakan ke **`GPIO 21` (SDA)** dan **`GPIO 22` (SCL)**.
- **Open-Drain & Wajib Pull-Up**: Perangkat I2C hanya bisa menarik jalur ke `LOW` (`GND`); ia tidak mendorong ke `HIGH`. Jalur kembali ke `HIGH` ($3{,}3\text{ V}$) melalui **resistor pull-up** eksternal! Jika lupa memasang pull-up (banyak *breakout board* sensor sudah menyertakannya, tetapi sensor chip telanjang belum), komunikasi macet.
- **Rise Time Pull-Up (Spesifikasi NXP UM10204)**:
  $$t_r \approx 0{,}8473 \times R_p \times C_{\text{bus}}$$
  Untuk bus berkapasitansi $C_{\text{bus}} = 100\text{ pF}$: resistor $10\text{ k}\Omega$ menghasilkan $t_r = 847{,}3\text{ ns}$ (lulus Standard Mode $100\text{ kHz}$ $\le 1000\text{ ns}$, tetapi **gagal** di Fast Mode $400\text{ kHz}$ $\le 300\text{ ns}$!), sedangkan $2{,}2\text{ k}\Omega$ menghasilkan $186{,}4\text{ ns}$ (lulus hingga $400\text{ kHz}$).
- **7-Bit Addressing & Konflik Alamat**: Setiap perangkat memiliki alamat 7-bit (`0x08..0x77`), diakhiri bit `R/W` dan bit **`ACK`/`NACK`** pada bit ke-9. Jika dua sensor identik memiliki alamat default sama (`0x76`), ubah pin selektor `SDO`/`ADDR` pada salah satunya ke `0x77` atau gunakan *I2C multiplexer* (misal TCA9548A).

### 4. SPI: Full-Duplex, Chip Select & SPI Modes

SPI memakai driver *push-pull* berkecepatan tinggi dengan 4 jalur (*VSPI* default ESP32: `MOSI=23`, `MISO=19`, `SCLK=18`, `CS=5`):
- **Chip Select (`CS` / `SS`, *active-low*)**: Master menarik `CS` perangkat target ke `LOW` sebelum memulai transfer dan mengembalikannya ke `HIGH` setelah selesai. Satu pin GPIO `CS` terpisah diperlukan untuk setiap tambahan perangkat *slave*.
- **4 Mode SPI (`CPOL` & `CPHA`)**:
  - `CPOL` (*Clock Polarity*): status *clock* saat idle (`0` = `LOW`, `1` = `HIGH`).
  - `CPHA` (*Clock Phase*): tepi *clock* saat data dicuplik (`0` = tepi pertama, `1` = tepi kedua).
  - Cocokkan **`SPI_MODE0..3`** dengan *timing diagram* di *datasheet* sensor/radio!

### 5. Implementasi & Verifikasi (`i2c_uart_spi_probe.ino` & `bus_protocol_sim.py`)

- **Firmware ESP32**: [`i2c_uart_spi_probe.ino`](content/chapter-16/src/i2c_uart_spi_probe/i2c_uart_spi_probe.ino) menggabungkan *I2C Scanner* (`0x08..0x77`), `Serial2` `8N1`, dan transaksi uji `SPI_MODE0`. Berstatus **Belum diuji** di server ini sementara core ESP32 dipasang.
- **Verifikasi Software**: [`bus_protocol_sim.py`](content/chapter-16/src/bus_protocol_sim.py) menguji kalkulasi efisiensi `8N1`/`8E1`, validasi *rise time* I2C $10\text{ k}\Omega / 4{,}7\text{ k}\Omega / 2{,}2\text{ k}\Omega$, deteksi konflik alamat `0x76`, serta waktu transfer $64\text{ B}$ SPI ($128{,}0\,\mu\text{s}$ @ $4\text{ MHz}$ vs $\sim 5{,}56\text{ ms}$ pada UART $115200$) — seluruhnya dieksekusi nyata di Python (`outputs.md`).

### 6. Common Mistakes & Troubleshooting Bus Serial

| Gejala | Penyebab Umum | Pemeriksaan & Solusi |
| --- | --- | --- |
| UART2 tidak menerima apa-apa | `TX` disambung ke `TX` (lupa crossover), beda *baud rate*, atau `GND` belum terhubung | Tukar `TX–RX`, samakan *baud rate*, cek *common GND* |
| I2C Scanner menemukan `0` perangkat atau hang | `SDA`/`SCL` tertukar, tidak ada resistor *pull-up*, atau alamat 7-bit vs 8-bit tertukar | Cek pin `21/22`, ukur tegangan idle $3{,}3\text{ V}$, pasang pull-up $4{,}7\text{ k}\Omega$ |
| Pembacaan SPI selalu `0x00` atau `0xFF` | Pin `CS` lupa ditarik `LOW`, `MISO`/`MOSI` tertukar, atau `SPI_MODE` salah | Periksa `digitalWrite(CS, LOW)` dan cocokkan `CPOL/CPHA` dengan *datasheet* |

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-16/exercises.md)):
1. Memilih bus yang tepat untuk 4 skenario sensor/modul beserta alasannya.
2. Menghitung waktu kirim 250 byte data melalui UART `9600 8N1` vs SPI `2 MHz`, serta mengecek *rise time* I2C.
3. Diagnosis kasus dua sensor BME280 beralamat `0x76` dan kesalahan alamat 8-bit vs 7-bit.
4. Menjalankan [`bus_protocol_sim.py`](content/chapter-16/src/bus_protocol_sim.py) dan Mini Challenge kalkulator jumlah slave maksimum SPI terhadap jumlah GPIO tersedia.

## Tugas

Susun **Rancangan Integrasi Multi-Bus (UART + I2C + SPI) & Panduan Troubleshooting Bus pada ESP32-DevKitC V4** (detail & rubrik 100 poin di tab **Tugas & Rubrik** — [assignment.md](content/chapter-16/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Pemilihan bus & pemetaan pin ESP32 | 25 | Kesesuaian UART/I2C/SPI terhadap kecepatan & jarak serta bebas konflik pin Flash/PSRAM |
| Perhitungan parameter protokol & elektrikal | 25 | Ketepatan efisiensi frame UART, *rise time* pull-up I2C, dan alamat 7-bit tanpa tabrakan |
| Implementasi kode / skema komunikasi | 30 | Inisialisasi `Wire`/`Serial2`/`SPI` yang benar, `beginTransaction`/`CS` tepat, non-blocking |
| Panduan troubleshooting & kejujuran bukti | 20 | Prosedur diagnosis `TX/RX`, pull-up, I2C scanner, `CPOL/CPHA`, serta status uji jujur |

## Ringkasan

- **UART** bersifat asinkron *point-to-point* (crossover `TX-RX`, frame `8N1` ber-efisiensi $80\%$, butuh kesamaan *baud rate*).
- **I2C** bersifat sinkron *open-drain* 2-kabel (`SDA/SCL`) dengan **pull-up wajib** dan pengalamatan **7-bit**, cocok untuk banyak sensor berkecepatan rendah–menengah jarak dekat.
- **SPI** bersifat sinkron *push-pull* *full-duplex* berkecepatan tinggi dengan 4 kabel (`MOSI, MISO, SCLK, CS` per *slave*) dan 4 mode (`CPOL/CPHA`).
- Perhitungan teknis bus telah diverifikasi melalui `bus_protocol_sim.py` (`outputs.md`); kompilasi `i2c_uart_spi_probe.ino` menunggu selesainya instalasi core ESP32.

## Referensi

1. NXP Semiconductors, *UM10204: I2C-bus Specification and User Manual*, [https://www.nxp.com/docs/en/user-guide/UM10204.pdf](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) (diperiksa 2026-11-11).
2. Espressif Systems, *ESP-IDF UART, I2C, and SPI Master Driver Documentation*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/index.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/index.html) (diperiksa 2026-11-11).
3. Arduino Official Documentation, *Wire (I2C) & SPI Library Reference*, [https://docs.arduino.cc/language-reference/en/functions/communication/wire/](https://docs.arduino.cc/language-reference/en/functions/communication/wire/) (diperiksa 2026-11-11).


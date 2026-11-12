# Tugas & Rubrik — Chapter 16

## Skenario Tugas: Integrasi Multi-Bus (UART + I2C + SPI) pada Node Sensor

Anda diminta merancang integrasi perangkat keras & *Firmware* untuk **Stasiun Cuaca & Logger Lokal** berbasis `ESP32-DevKitC V4` yang menggabungkan:
- 1x Modul GPS (antarmuka **UART** `9600 8N1`),
- 1x Sensor BME280 (`0x76`) + 1x Layar OLED SSD1306 (`0x3C`) (antarmuka **I2C** $100\text{ kHz}$),
- 1x Modul microSD Card (antarmuka **SPI** `Mode 0`).

## Instruksi Pengerjaan

1. **Peta Pin & Skema Kelistrikan**: Susun tabel *pin mapping* lengkap tanpa konflik *SPI Flash* (`GPIO 6–11`), *strapping pins*, atau konflik `ADC2` bila Wi-Fi akan diaktifkan. Cantumkan nilai resistor *pull-up* I2C dan bukti hitungan *rise time* ($C_{\text{bus}} = 100\text{ pF}$).
2. **Analisis Timing & Efisiensi**: Hitung waktu transfer 128 byte ke microSD via SPI ($4\text{ MHz}$) vs membaca 128 byte kalimat GPS via UART (`9600 8N1`), dan jelaskan mengapa pembacaan UART harus non-blocking.
3. **Kode Probe & Checklist Troubleshooting**: Sesuaikan [`i2c_uart_spi_probe.ino`](content/chapter-16/src/i2c_uart_spi_probe/i2c_uart_spi_probe.ino) untuk skenario di atas dan susun 5 langkah diagnosis apabila I2C Scanner gagal atau microSD mengembalikan `0xFF`.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Pemilihan bus & pemetaan pin ESP32** | **25** | Alokasi pin UART/I2C/SPI valid pada ESP32-DevKitC V4, bebas konflik Flash/strapping. |
| **Perhitungan parameter protokol & elektrikal** | **25** | Efisiensi `8N1`, durasi SPI vs UART, *rise time* pull-up I2C, dan cek alamat 7-bit tepat. |
| **Implementasi kode / skema komunikasi** | **30** | Konfigurasi `Wire`, `Serial2`, dan `SPI.beginTransaction()` + `CS` rapi dan non-blocking. |
| **Panduan troubleshooting & kejujuran bukti** | **20** | SOP diagnosis TX/RX, pull-up, CPOL/CPHA jelas; laporan status uji sesuai bukti aktual. |


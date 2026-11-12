# Source Code — Chapter 16: UART, I2C & SPI Probe

Folder `src/` berisi:

1. [i2c_uart_spi_probe.ino](content/chapter-16/src/i2c_uart_spi_probe/i2c_uart_spi_probe.ino): Firmware ESP32 untuk memindai bus I2C (`GPIO 21/22`), menginisialisasi `UART2` (`GPIO 16/17`, `8N1`), dan menguji transaksi *full-duplex* `VSPI` (`Mode 0`, `GPIO 5` CS).
2. [bus_protocol_sim.py](content/chapter-16/src/bus_protocol_sim.py): Kalkulator Python yang menguji efisiensi frame UART, menghitung *rise time* resistor *pull-up* I2C terhadap spesifikasi NXP UM10204, mendeteksi tabrakan alamat 7-bit, dan membandingkan kecepatan SPI Mode 0–3.

## Cara Menjalankan

**Simulasi & Kalkulator Python:**
```sh
python public/content/chapter-16/src/bus_protocol_sim.py
```

**Firmware ESP32:**
- Target: `ESP32-DevKitC V4 (WROOM-32)`. (Peringatan: jika memakai modul `WROVER` dengan PSRAM eksternal, pindahkan pin `UART2` dari `GPIO 16/17` ke pin bebas lain via `Serial2.begin(9600, SERIAL_8N1, rxPin, txPin)`).


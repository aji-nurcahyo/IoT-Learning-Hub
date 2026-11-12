# Bukti & Output Eksekusi — Chapter 16

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (analisis efisiensi frame UART, *rise time* pull-up I2C NXP UM10204, konflik alamat 7-bit, dan mode SPI pada Python 3.12.10)
- **Tanggal**: 2026-11-11
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-16/src/bus_protocol_sim.py`
- **Firmware ESP32 (`i2c_uart_spi_probe.ino`)**: **Belum diuji** (toolchain `esp32:esp32` masih dalam tahap instalasi; sensor I2C/SPI fisik belum dihubungkan)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== ANALISIS TEKNIS UART, I2C & SPI (CHAPTER 16) ===
UART 9600 baud (8N1): 10 bit/frame -> efisiensi=80.0%, maks=960 B/s
UART 115200 baud (8N1): 10 bit/frame -> efisiensi=80.0%, maks=11,520 B/s
UART 115200 baud (8E1): 11 bit/frame -> efisiensi=72.7%, maks=10,473 B/s

--- Evaluasi Pull-Up I2C (Batas NXP UM10204) ---
I2C R_p=10000 ohm, C_bus=100 pF -> t_r=847.3 ns | 100kHz(<=1000ns)=True | 400kHz(<=300ns)=False
I2C R_p=4700 ohm, C_bus=100 pF -> t_r=398.2 ns | 100kHz(<=1000ns)=True | 400kHz(<=300ns)=False
I2C R_p=2200 ohm, C_bus=100 pF -> t_r=186.4 ns | 100kHz(<=1000ns)=True | 400kHz(<=300ns)=True

--- Cek Konflik Alamat I2C 7-bit ---
  [KONFLIK] BMP280_alt (0x76) bentrok dengan BME280! Ubah pin SDO/ADDR atau pakai I2C mux.

--- Matriks Mode SPI & Waktu Transfer 64 Byte @ 4 MHz ---
  SPI_MODE0: CPOL=0, CPHA=0 -> sample data pada Rising edge
  SPI_MODE1: CPOL=0, CPHA=1 -> sample data pada Falling edge
  SPI_MODE2: CPOL=1, CPHA=0 -> sample data pada Falling edge
  SPI_MODE3: CPOL=1, CPHA=1 -> sample data pada Rising edge
  Durasi transfer 64 byte SPI @ 4 MHz = 128.0 us (vs ~5.56 ms pada UART 115200)
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `i2c_uart_spi_probe`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-16/src/i2c_uart_spi_probe
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 298660 bytes (22%) of program storage space. Maximum is 1310720 bytes.
Global variables use 23596 bytes (7%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

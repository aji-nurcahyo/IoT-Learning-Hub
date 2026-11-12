# Source Code — Chapter 04: ESP32 Board Probe & Variant Pin Audit

Folder `src/` berisi kode untuk dua jalur belajar:

1. **Firmware ESP32 (Arduino Framework)**: [ch04_board_probe.ino](content/chapter-04/src/ch04_board_probe/ch04_board_probe.ino)
   - Target board: `ESP32-DevKitC V4 (ESP32-WROOM-32)`
   - Membaca identitas chip (`ESP.getChipModel()`, revisi, core, flash, free heap) dan mengedipkan LED pada `GPIO 25`.
2. **Konfigurasi Simulasi Wokwi (Path A)**: [wokwi_diagram.json](content/chapter-04/src/wokwi_diagram.json)
   - Memetakan `board-esp32-devkit-c-v4` dengan resistor $220\,\Omega$ dan LED hijau pada `GPIO 25`.
3. **Skrip Audit Pin Lintas Varian (Python)**: [board_matrix.py](content/chapter-04/src/board_matrix.py)
   - Membandingkan arsitektur `ESP32`, `ESP32-S3`, dan `ESP32-C3` serta mendeteksi konflik pin SPI Flash, *input-only*, dan *strapping pins*.

## Cara Menjalankan

**Skrip Python (Software Verification):**
```sh
python public/content/chapter-04/src/board_matrix.py
```

**Firmware ESP32 (Path A Wokwi atau Path B Hardware):**
1. Buka proyek Wokwi ESP32 baru atau Arduino IDE 2.x dengan board package `esp32 by Espressif Systems` (v3.x) dan pilih board `ESP32 Dev Module`.
2. Salin isi `ch04_board_probe.ino` (dan `wokwi_diagram.json` pada tab `diagram.json` Wokwi).
3. Hubungkan Serial Monitor pada baud rate `115200`.

## Status Verifikasi

- `board_matrix.py`: **Dieksekusi nyata** di Python 3.12.10 (lihat `outputs.md`).
- `ch04_board_probe.ino` & `wokwi_diagram.json`: **Belum diuji** (kompilasi `arduino-cli` dan simulator Wokwi tidak tersedia di environment server ini).


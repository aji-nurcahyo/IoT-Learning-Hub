# Laporan Verifikasi — Level 1 & Level 2 Toolchain, Kompilasi & Simulasi

Laporan ini disusun secara objektif berdasarkan audit kondisi aktual lingkungan pengembangan pada Windows 11, instalasi resmi native toolchain Arduino ESP32, kompilasi setiap sketsa firmware, eksekusi harness uji simulasi software/jaringan, serta keterbatasan akses simulator dan perangkat keras fisik.

## 1. Audit Toolchain & Lingkungan

- **Sistem Operasi**: Windows 11 Enterprise (x64)
- **Python**: 3.12.10
- **Node.js**: v24.15.0
- **Arduino CLI**: v1.5.1 (`Commit: 01f3d4f2b Date: 2026-06-05T10:22:12Z`) terpasang di `%LOCALAPPDATA%\Programs\ArduinoCLI\arduino-cli.exe`
- **Core Board ESP32**: Espressif Arduino-ESP32 **v3.3.12** via official package URL `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Eksternal**: `PubSubClient v2.8.0` terpasang di pustaka user Arduino
- **Wokwi CLI**: **Tidak tersedia** (`wokwi-cli` tidak terpasang di PATH/winget; variabel lingkungan `WOKWI_CLI_TOKEN` tidak disetel). Sesuai aturan kejujuran verifikasi, status simulasi Wokwi dicatat **Not Tested**.
- **Hardware Fisik**: **Tidak tersedia** (pengujian fisik papan ESP32 / transceiver RF tidak dapat diakses dari lingkungan ini). Dicatat **Not Tested**.

---

## 2. Tabel Status Verifikasi Contoh Program (Chapters 01–20)

| Chapter | Contoh / Sketsa | Compile (`esp32:esp32:esp32`) | Simulator (Wokwi CLI) | Hardware Fisik | Bukti & Log Aktual |
|---|---|---|---|---|---|
| **01** | `iot_layer_matrix.py` | N/A (Python Model) | Not Tested | Not Tested | `public/content/chapter-01/outputs.md` |
| **02** | `iot_arch_evaluator.py` | N/A (Python Model) | Not Tested | Not Tested | `public/content/chapter-02/outputs.md` |
| **03** | `power_safety_calculator.py` | N/A (Python Model) | Not Tested | Not Tested | `public/content/chapter-03/outputs.md` |
| **04** | `ch04_board_probe.ino` | **Verified (EXIT=0)**<br>Flash: 273.748 B (20%)<br>RAM: 22.116 B (6%) | Not Tested | Not Tested | `public/content/chapter-04/outputs.md` |
| **05** | `ex01_types_serial.ino` | **Verified (EXIT=0)**<br>Flash: 269.032 B (20%)<br>RAM: 22.116 B (6%) | Not Tested | Not Tested | `public/content/chapter-05/outputs.md` |
| **05** | `ex02_nonblocking_fsm.ino` | **Verified (EXIT=0)**<br>Flash: 272.284 B (20%)<br>RAM: 22.156 B (6%) | Not Tested | Not Tested | `public/content/chapter-05/outputs.md` |
| **06** | `ex01_button_debounce_fsm.ino` | **Verified (EXIT=0)**<br>Flash: 272.400 B (20%)<br>RAM: 22.132 B (6%) | Not Tested | Not Tested | `public/content/chapter-06/outputs.md` |
| **06** | `ex02_interrupt_flag.ino` | **Verified (EXIT=0)**<br>Flash: 274.336 B (20%)<br>RAM: 22.612 B (6%) | Not Tested | Not Tested | `public/content/chapter-06/outputs.md` |
| **07** | `ex01_adc_pwm_dimmer.ino` | **Verified (EXIT=0)**<br>Flash: 286.723 B (21%)<br>RAM: 22.440 B (6%) | Not Tested | Not Tested | `public/content/chapter-07/outputs.md` |
| **08** | `ex01_ntc_calibrated.ino` | **Verified (EXIT=0)**<br>Flash: 279.396 B (21%)<br>RAM: 22.196 B (6%) | Not Tested | Not Tested | `public/content/chapter-08/outputs.md` |
| **09** | `ex01_hysteresis_driver.ino` | **Verified (EXIT=0)**<br>Flash: 289.171 B (22%)<br>RAM: 22.392 B (6%) | Not Tested | Not Tested | `public/content/chapter-09/outputs.md` |
| **10** | `capstone_env_monitor.ino` | **Verified (EXIT=0)**<br>Flash: 290.515 B (22%)<br>RAM: 22.472 B (6%) | Not Tested | Not Tested | `public/content/chapter-10/outputs.md` |
| **11** | `network_diagnostics_sim.py` | N/A (Python Network Sim) | Not Tested | Not Tested | `public/content/chapter-11/outputs.md` |
| **12** | `wifi_prov_fsm.ino` | **Verified (EXIT=0)**<br>Flash: 884.288 B (67%)<br>RAM: 45.920 B (14%) | Not Tested | Not Tested | `public/content/chapter-12/outputs.md` |
| **13** | `http_rest_client.ino` | **Verified (EXIT=0)**<br>Flash: 1.019.952 B (77%)<br>RAM: 49.016 B (14%) | Not Tested | Not Tested | `public/content/chapter-13/outputs.md` |
| **14** | `mqtt_pubsub_client.ino` | **Verified (EXIT=0)**<br>Flash: 899.880 B (68%)<br>RAM: 47.264 B (14%) | Not Tested | Not Tested | `public/content/chapter-14/outputs.md` |
| **15** | `mqtt_lwt_retained.ino` | **Verified (EXIT=0)**<br>Flash: 914.608 B (69%)<br>RAM: 47.280 B (14%) | Not Tested | Not Tested | `public/content/chapter-15/outputs.md` |
| **16** | `i2c_uart_spi_probe.ino` | **Verified (EXIT=0)**<br>Flash: 298.660 B (22%)<br>RAM: 23.596 B (7%) | Not Tested | Not Tested | `public/content/chapter-16/outputs.md` |
| **17** | `ble_gatt_sensor.ino` | **Verified (EXIT=0)**<br>Flash: 1.096.915 B (83%)<br>RAM: 41.332 B (12%) | Not Tested | Not Tested | `public/content/chapter-17/outputs.md` |
| **18** | `lora_airtime_budget.py` | N/A (Python ToA & Link Budget) | Not Tested | Not Tested | `public/content/chapter-18/outputs.md` |
| **19** | `offline_queue_ntp.ino` | **Verified (EXIT=0)**<br>Flash: 901.794 B (68%)<br>RAM: 48.060 B (14%) | Not Tested | Not Tested | `public/content/chapter-19/outputs.md` |
| **20** | `connected_env_capstone.ino` | **Verified (EXIT=0)**<br>Flash: 1.045.668 B (79%)<br>RAM: 50.600 B (15%) | Not Tested | Not Tested | `public/content/chapter-20/outputs.md` |

---

## 3. Ringkasan Kuantitatif

- **Total Sketsa Firmware Native ESP32**: 17 sketsa
- **Tingkat Keberhasilan Kompilasi Native**: **17 / 17 (100% EXIT=0)**
- **Total Chapter Terbit (Level 1 & Level 2)**: 20 Chapter (01–20)
- **Status Chapter Mendatang (Level 3 & Level 4)**: 20 Chapter (21–40) tetap berstatus `coming-soon`
- **Simulasi Software & Uji Jaringan**: Terverifikasi lokal (loopback HTTP/REST, loopback binary MQTT 3.1.1, evaluasi ToA Semtech AN1200.13, Ring Buffer offline replay & idempotensi).
- **Integritas Bukti**: Tidak ada klaim palsu atas simulasi Wokwi berlisensi atau pengujian perangkat fisik yang tidak dieksekusi.


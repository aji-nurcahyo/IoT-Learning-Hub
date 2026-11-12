# Source Code — Chapter 17: Bluetooth Low Energy (BLE GATT)

## Daftar Berkas

1. [`ble_gatt_sim.py`](src/ble_gatt_sim.py) — Simulasi Python untuk pengodean karakteristik suhu GATT (`0x2A6E` little-endian `int16` skala `0,01 C`), fragmentasi ATT MTU (`23` vs `65` vs `247` byte), serta perhitungan arus rata-rata dan estimasi umur baterai koin `CR2032` pada berbagai *Advertising Interval*.
2. [`ble_gatt_sensor.ino`](src/ble_gatt_sensor/ble_gatt_sensor.ino) — Firmware ESP32 berbasis pustaka resmi Arduino ESP32 BLE (`BLEDevice`, `BLEServer`, `BLE2902`) dengan:
   - Service `0x181A` (*Environmental Sensing*)
   - Characteristic `0x2A6E` (`READ | NOTIFY` + Descriptor CCCD `0x2902`)
   - Characteristic kontrol interval (`READ | WRITE`)
   - Penanganan `onDisconnect` yang memanggil ulang `startAdvertising()` agar node dapat ditemukan lagi oleh Central.

## Cara Menjalankan

```bash
python public/content/chapter-17/src/ble_gatt_sim.py
```

Firmware ESP32 dikompilasi melalui Arduino CLI / Arduino IDE dengan target board `esp32:esp32:esp32`.


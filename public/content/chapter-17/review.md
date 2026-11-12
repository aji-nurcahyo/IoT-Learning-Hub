# Laporan Review — Chapter 17

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-11
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk kompilasi `.ino` dan uji radio BLE nyata, disertai bukti **Software (`ble_gatt_sim.py`)**.

## Hasil Pemeriksaan

1. **Kelengkapan Konsep**: Memetakan peran GAP (*Peripheral*/*Central*), hierarki GATT (*Service* `0x181A`, *Characteristic* `0x2A6E`, Descriptor CCCD `0x2902`), negosiasi ATT MTU (`23` vs `247`), serta perbedaan `Notify` vs `Indicate`.
2. **Validasi Numerik**: Output `ble_gatt_sim.py` konsisten dengan seluruh contoh di `reading.md` dan `slides.json` (`27,85 C` -> `e1 0a`; MTU `23`/`65`/`247`; estimasi `CR2032`).
3. **Catatan Lanjutan**: Sketsa `ble_gatt_sensor.ino` akan dikompilasi dengan `arduino-cli` setelah core ESP32 selesai dipasang.


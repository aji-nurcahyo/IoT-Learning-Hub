# Bukti & Output — Chapter 17: Bluetooth Low Energy

- **Status Verifikasi Saat Ini**: Software Simulation **Terverifikasi (`software`)**; kompilasi `.ino` (`compile`), simulator Wokwi (`simulator`), dan pengujian radio BLE pada papan ESP32 fisik (`hardware`) belum dijalankan (*Not Tested*) pada tahap penulisan modul ini.
- **Catatan Lingkungan**: Pengujian Python dijalankan pada Windows 11 (`python 3.12.10`). Pengujian BLE radio nyata membutuhkan papan ESP32 serta aplikasi BLE Central (misal nRF Connect / Python `bleak`).

## Output Aktual `ble_gatt_sim.py`

Command:

```text
python public/content/chapter-17/src/ble_gatt_sim.py
```

Exit code: `0`

```text
=== CHAPTER 17: BLE GATT, ATT MTU & POWER BUDGET SIMULATION ===
[GATT] Service=0x181A Char=0x2A6E temp=27.85 C -> bytes=e1 0a -> decoded=27.85 C
[MTU] payload=64 B, ATT_MTU=23 -> max_att_payload=20 B -> packets_needed=4
[MTU] payload=64 B, ATT_MTU=65 -> max_att_payload=62 B -> packets_needed=2
[MTU] payload=64 B, ATT_MTU=247 -> max_att_payload=244 B -> packets_needed=1
[POWER] adv_interval= 100.0 ms -> I_avg=0.3373 mA -> CR2032_life=  27.2 days
[POWER] adv_interval= 500.0 ms -> I_avg=0.0715 mA -> CR2032_life= 128.3 days
[POWER] adv_interval=1000.0 ms -> I_avg=0.0382 mA -> CR2032_life= 239.8 days
[POWER] adv_interval=2000.0 ms -> I_avg=0.0216 mA -> CR2032_life= 424.1 days
[MODE] NOTIFY: throughput max = 1+ PDU per 100 ms (tanpa tunggu ATT Confirmation).
[MODE] INDICATE: 1 PDU butuh 1 RTT konfirmasi (~200 ms per transaksi).
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ble_gatt_sensor`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-17/src/ble_gatt_sensor
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 1096915 bytes (83%) of program storage space. Maximum is 1310720 bytes.
Global variables use 41332 bytes (12%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

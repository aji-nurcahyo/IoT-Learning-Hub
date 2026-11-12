# Source Code — Chapter 12: Wi-Fi Provisioning & Reconnect Backoff

Folder `src/` berisi:

1. [wifi_prov_fsm.ino](content/chapter-12/src/wifi_prov_fsm/wifi_prov_fsm.ino): Firmware ESP32 menggunakan `WiFi.h` (`WIFI_STA`) + `Preferences.h` (NVS Flash) dengan *Serial provisioning* (`PROV:<ssid>,<password>` dan `WIPE`), *timeout* koneksi 10 detik, *exponential backoff* ($1\text{ s} \dots 60\text{ s}$), dan diagnostik `RSSI`. Tidak ada kredensial *hardcoded*.
2. [wokwi_diagram.json](content/chapter-12/src/wokwi_diagram.json): Konfigurasi Wokwi (`board-esp32-devkit-c-v4` + tombol reset NVS pada `GPIO 27` + LED status biru pada `GPIO 25`). (Catatan: di Wokwi, jaringan virtual menggunakan SSID `Wokwi-GUEST` tanpa password).
3. [wifi_fsm_sim.py](content/chapter-12/src/wifi_fsm_sim.py): Skrip Python memverifikasi transisi state provisioning dan urutan *exponential backoff*.

## Cara Menjalankan

**Simulasi Python:**
```sh
python public/content/chapter-12/src/wifi_fsm_sim.py
```

**Firmware ESP32 (Wokwi / Hardware):**
- Di Serial Monitor (`115200 baud`), kirim perintah `PROV:Wokwi-GUEST,` (atau SSID/password lab lokal Anda — **jangan** commit log yang memuat password asli!).


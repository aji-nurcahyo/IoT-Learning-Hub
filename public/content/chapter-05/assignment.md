# Tugas & Rubrik — Chapter 05

## Skenario Tugas: Firmware Non-Blocking & Modular State Machine

Rancang *Firmware* modular untuk **ESP32-DevKitC V4** yang menjalankan tiga tugas bersamaan secara **non-blocking** tanpa `delay()` di `loop()`:
1. **Task Heartbeat LED (`GPIO 25`)**: Berkedip stabil tiap $1000\text{ ms}$ untuk menandakan MCU tidak *hang*.
2. **Task State Machine Pemantau (`IDLE`, `MONITOR`, `WARNING`, `FAULT`)**: Mengevaluasi data simulasi internal tiap $500\text{ ms}$ dan mengendalikan LED peringatan (`GPIO 26`, mati saat `IDLE/MONITOR`, kedip $250\text{ ms}$ saat `WARNING`, menyala terus saat `FAULT`).
3. **Task Serial Telemetry**: Mencetak status state dan *uptime* dalam format terstruktur setiap $2000\text{ ms}$ menggunakan `snprintf()` dan buffer statis (tanpa `String`).

## Deliverables

- Kode sumber modular (`.ino` + minimal 1 file `.h` dengan *include guard*).
- Diagram atau tabel transisi *Finite State Machine*.
- Daftar uji logika / simulasi Python atau log Wokwi/hardware (nyatakan jujur status verifikasi).

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Struktur C/C++, tipe data & modularitas header** | **25** | Memakai `uint*_t`, `constexpr`, minimal 1 file `.h` ber-*include guard*, dan bebas alokasi *heap* `String` di `loop()`. |
| **Implementasi non-blocking `millis()`** | **30** | Nol `delay()` di `loop()`, pengurangan *unsigned* aman *rollover*, dan ketiga interval berjalan independen. |
| **Desain Finite State Machine (FSM)** | **25** | Menggunakan `enum class` dan `switch-case` bersih dengan kondisi transisi terdefinisi dan status awal aman. |
| **Dokumentasi, bukti uji & kejujuran status** | **20** | Kode rapi, ada tabel/diagram transisi, serta pemisahan tegas antara simulasi/expected output dan eksekusi nyata. |


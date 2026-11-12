# Tugas & Rubrik — Chapter 06

## Skenario Tugas: Pengendali Tombol Dual-Action (Short & Long Press) + Debounce

Rancang *Firmware* untuk `ESP32-DevKitC V4` yang membaca **1 push button** (`GPIO 27`, `INPUT_PULLUP`) dan mengendalikan **2 LED indikator** (`LED_STATUS` pada `GPIO 25`, `LED_ALERT` pada `GPIO 26`, masing-masing seri resistor $220\,\Omega$).

## Persyaratan Fungsional & Teknis

1. **Software Debouncing**: Gunakan jendela stabilitas $40\text{--}50\text{ ms}$ berbasis `millis()` tanpa `delay()` di `loop()`.
2. **Deteksi Short Press vs Long Press**:
   - **Short Press** (dilepas sebelum $1200\text{ ms}$): Menggeser mode `LED_STATUS`: `OFF -> ON -> BLINK (300 ms) -> OFF`.
   - **Long Press** (ditahan $\ge 1200\text{ ms}$): Mengaktifkan/mematikan status *System Lock* (`LED_ALERT` menyala, `LED_STATUS` dipaksa mati dan mengabaikan *short press* sampai *long press* berikutnya membuka kunci).
3. **Serial Telemetry**: Cetak setiap transisi valid beserta *timestamp* `millis()` menggunakan `snprintf()`.
4. **Simulasi / Dokumentasi**: Sertakan skema `wokwi_diagram.json` atau tabel *wiring* lengkap, serta laporkan hasil uji dengan jujur (*Belum diuji*, *Simulator-verified*, atau *Hardware-verified* sesuai pengujian yang benar-benar Anda jalankan).

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Konfigurasi GPIO & keamanan rangkaian** | **20** | Pin valid sesuai ESP32-DevKitC V4, resistor LED $220\,\Omega$ tercantum, `INPUT_PULLUP` benar. |
| **Implementasi debouncing & edge detection** | **30** | Debounce non-blocking bebas pantulan, tidak memicu berulang saat tombol ditahan. |
| **Desain FSM & logika short/long press** | **30** | Transisi state (`OFF`, `ON`, `BLINK`, `LOCKED`) bersih, akurat, dan bebas `delay()`. |
| **Dokumentasi, wiring & kejujuran status uji** | **20** | Pin mapping jelas, skenario uji terperinci, dan bukti/status sesuai pengujian aktual. |


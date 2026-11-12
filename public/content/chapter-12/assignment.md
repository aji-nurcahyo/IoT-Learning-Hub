# Tugas & Rubrik — Chapter 12

## Skenario Tugas: Wi-Fi Provisioning & Non-Blocking Connection Manager

Bangun modul manajemen koneksi Wi-Fi untuk `ESP32-DevKitC V4` yang memisahkan konfigurasi jaringan dari *source code* dan tetap responsif ketika router mati.

## Persyaratan Teknis

1. **Zero Hardcoded Secrets**: Kredensial Wi-Fi disimpan pada partisi **NVS (`Preferences`)** melalui perintah Serial (`PROV:<ssid>,<pass>`) atau SoftAP lokal. Sediakan perintah/tombol *factory wipe* (`WIPE` / `GPIO 27`).
2. **Non-Blocking Connection FSM**: Implementasikan state `PROVISIONING`, `CONNECTING` (timeout $\le 10\text{ s}$), `CONNECTED`, dan `BACKOFF_WAIT` ($1\text{ s} \rightarrow 2\text{ s} \rightarrow \dots \rightarrow 60\text{ s}$) tanpa `while` atau `delay()` yang memblokir tugas kedip LED / pembacaan sensor.
3. **Diagnostik & Opsi Static IP**: Cetak status koneksi, IP, Gateway, dan `RSSI` (dengan klasifikasi kualitas sinyal), serta dokumentasikan cara beralih dari DHCP ke Static IP (`WiFi.config()`).
4. **Keamanan & Kejujuran Log**: Pastikan seluruh log Serial maupun laporan tugas **tidak** menampilkan password asli (gunakan `REDACTED`), dan nyatakan status verifikasi sesuai pengujian aktual.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Device provisioning & penyimpanan NVS aman** | **30** | Nol kredensial *hardcoded*, persistensi `Preferences` benar, fitur *wipe* tersedia, dan password ter-redaksi di log. |
| **Connection state machine & exponential backoff** | **30** | FSM non-blocking `millis()`, batas timeout jelas, urutan *backoff* sampai cap maksimum, dan reset saat `CONNECTED`. |
| **Diagnostik Wi-Fi, Static/DHCP & keamanan** | **20** | Pemantauan `RSSI`, analisis DHCP vs Static IP, dan praktik keamanan WPA2/WPA3 terdokumentasi baik. |
| **Dokumentasi, simulasi & kejujuran bukti** | **20** | Diagram FSM rapi, skrip uji/Wokwi terdokumentasi, serta status uji dilaporkan sesuai bukti nyata. |


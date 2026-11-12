# Chapter 12 — Wi-Fi Connectivity & Device Provisioning

## Overview

Sebagian besar tutorial pemula menghubungkan ESP32 ke Wi-Fi dengan menuliskan `const char* ssid = "WifiRumah"; const char* pass = "Rahasia123";` langsung di *source code* lalu memanggil `while (WiFi.status() != WL_CONNECTED) { delay(500); }`. Dalam rekayasa IoT profesional, pola tersebut memiliki **dua cacat serius**: (1) kredensial bocor ke repositori Git dan perangkat tidak dapat dipindah ke jaringan lain tanpa *flash* ulang; (2) perulangan `while` yang memblokir membuat sistem kendali lokal membeku ketika *Access Point* (AP) sedang mati!

Chapter ini membahas pengoperasian Wi-Fi ESP32 (*Station mode*), **Device Provisioning** tanpa *hardcoded credentials* menggunakan *Non-Volatile Storage* (**NVS / `Preferences`**), perancangan *connection state machine* dengan *timeout* dan *exponential backoff*, konfigurasi DHCP vs *Static IP*, diagnostik Wi-Fi (`RSSI`, *reason codes*, kanal 2,4 GHz), serta keamanan koneksi nirkabel.

## Prasyarat

- Memahami IPv4, *subnet mask*, *default gateway*, DHCP, dan DNS dari [Chapter 11](#/chapter/11).
- Menguasai *non-blocking* `millis()` dan *Finite State Machine* dari [Chapter 05](#/chapter/5).
- Ingat batasan hardware [Chapter 07](#/chapter/7): mengaktifkan Wi-Fi pada ESP32 klasik menonaktifkan unit **`ADC2`** (`GPIO 0, 2, 4, 12–15, 25–27`), sehingga sensor analog wajib berada di **`ADC1` (`GPIO 32–39`)**.

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Mengonfigurasi** ESP32 pada mode **Wi-Fi Station (`WIFI_STA`)** dengan pilihan **DHCP** maupun **Static IP** (`WiFi.config()`).
2. **Merancang** alur **Device Provisioning** berbasis penyimpanan persisten **NVS (`Preferences`)** tanpa menanam kredensial di *source code*.
3. **Mengimplementasikan** *connection state machine* *non-blocking* dengan batas *timeout* dan **exponential backoff** agar node tetap responsif saat AP terputus.
4. **Mendiagnosis** masalah konektivitas Wi-Fi menggunakan `RSSI`, kanal 2,4 GHz, event koneksi (`WiFi.onEvent`), serta menerapkan praktik keamanan koneksi dasar.

## Konsep dan teori

### 1. Mode Wi-Fi ESP32 & Station Mode (`WIFI_STA`)

Chip `ESP32` mendukung tiga mode Wi-Fi pada pita **$2{,}4\text{ GHz}$ (IEEE 802.11 b/g/n)**:
- **`WIFI_STA` (Station)**: ESP32 bertindak sebagai klien yang terhubung ke *Access Point* / router yang sudah ada. Ini mode standar untuk node sensor operasional.
- **`WIFI_AP` (Soft Access Point)**: ESP32 memancarkan SSID sendiri agar ponsel/laptop dapat terhubung langsung untuk konfigurasi awal (*captive portal*).
- **`WIFI_AP_STA`**: Gabungan keduanya (sering dipakai saat proses *provisioning* agar ESP32 bisa menerima kredensial lewat AP sambil menguji koneksi STA ke router).

### 2. Device Provisioning Tanpa Hardcoded Credentials

**Device Provisioning** adalah proses memasukkan identitas dan konfigurasi jaringan (SSID, *password*, alamat broker) ke perangkat secara aman di lapangan tanpa mengubah kode program.

| Metode Provisioning | Mekanisme Kerja | Kelebihan | Keterbatasan |
| --- | --- | --- | --- |
| **Serial CLI Provisioning** | Operator mengirim `PROV:<ssid>,<pass>` lewat USB-UART lalu disimpan ke **NVS** | Sangat sederhana, tanpa server web di MCU, aman fisik via kabel | Memerlukan akses kabel USB saat setup awal |
| **SoftAP Captive Portal** | Node membuka AP sementara + halaman web lokal untuk memilih SSID | Mudah dipakai pengguna awam via browser HP | Mengonsumsi RAM/Flash lebih besar; portal harus dimatikan setelah selesai |
| **BLE Provisioning (ESP-IDF/Improv)** | Mengirim kredensial melalui layanan GATT BLE terenkripsi | Tidak memutus koneksi Wi-Fi internet di HP pengguna | Membutuhkan aplikasi pendamping atau Web Bluetooth |

Pada ESP32, kredensial disimpan di partisi **NVS (*Non-Volatile Storage*)** melalui pustaka `Preferences.h` sehingga tetap bertahan saat daya dimatikan, dan dapat dihapus lewat tombol *factory reset* (`WIPE`). **Jangan pernah mencetak *password* secara terang-terangan di log Serial maupun menyimpan kredensial asli di repositori Git.**

### 3. Connection State Machine & Reconnect Strategy

![State machine konektivitas Wi-Fi ESP32, NVS provisioning, dan backoff](content/chapter-12/diagram.svg)

Memanggil `WiFi.begin()` di dalam *while-loop* yang memblokir adalah kesalahan arsitektur. Sebaliknya, gunakan 4 state non-blocking:
1. **`PROVISIONING`**: Terjadi saat NVS kosong atau tombol *wipe* ditekan; LED berkedip cepat ($150\text{ ms}$) menunggu perintah `PROV:<ssid>,<pass>`.
2. **`CONNECTING`**: Memanggil `WiFi.begin(ssid, pass)` dengan *timeout* $10.000\text{ ms}$. Selama menunggu asosiasi dan DHCP, loop kendali sensor & aktuator **tetap berjalan normal**.
3. **`CONNECTED`**: Masuk saat `WiFi.status() == WL_CONNECTED`; menyalakan LED solid dan me-reset `backoffMs` ke nilai awal ($1000\text{ ms}$).
4. **`BACKOFF_WAIT`**: Jika koneksi *timeout* atau tiba-tiba terputus (`DISCONNECTED`), tunggu jeda **exponential backoff**:
   $$t_{\text{backoff}}(k) = \min\left(t_{\min} \cdot 2^{k}, \; t_{\max}\right)$$
   Dengan $t_{\min} = 1\text{ s}$ dan $t_{\max} = 60\text{ s}$, urutan jeda adalah $1\text{ s} \rightarrow 2\text{ s} \rightarrow 4\text{ s} \rightarrow 8\text{ s} \rightarrow 16\text{ s} \rightarrow 32\text{ s} \rightarrow 60\text{ s}$. Strategi ini mencegah ratusan node membombardir *Access Point* dengan permintaan otentikasi setiap detik saat listrik router baru menyala kembali (*thundering herd*).

### 4. DHCP vs Static IP pada ESP32

- **DHCP (Default)**: Otomatis dan mudah dikelola untuk jaringan kampus/rumah. Gunakan *DHCP Reservation* berbasis alamat MAC di router jika node membutuhkan IP tetap tanpa mengubah *Firmware*.
- **Static IP (`WiFi.config(local_ip, gateway, subnet, dns1)`)**: Mempercepat waktu *reconnect* (menghemat fase DHCP Discover/Offer $\sim 1\text{--}2\text{ s}$, sangat berguna bagi node *deep sleep* bertenaga baterai). Namun berisiko konflik IP jika tidak dicatat rapi.

### 5. Wi-Fi Diagnostics & Connection Security

- **RSSI (*Received Signal Strength Indicator*)**: Diukur dalam $\text{dBm}$ (negatif). Nilai $> -65\text{ dBm}$ tergolong kuat; $-75 \dots -85\text{ dBm}$ rawan *packet loss* tinggi; $< -88\text{ dBm}$ sering menyebabkan *disconnect*.
- **Interferensi Kanal 2,4 GHz**: ESP32 klasik hanya mendukung pita $2{,}4\text{ GHz}$ (bukan $5\text{ GHz}$!). Hanya terdapat **3 kanal non-overlapping** yaitu **Kanal 1, 6, dan 11**. Memasang AP di kanal 3 atau 8 menyebabkan interferensi tumpang-tindih.
- **Keamanan Koneksi**:
  - Gunakan minimal **WPA2-PSK** (atau **WPA3-SAE** bila router mendukung) dan hindari jaringan terbuka (*Open Wi-Fi*) untuk node operasional karena lalu lintas lokal mudah disadap.
  - Pada penerapan produksi dengan risiko akses fisik, aktifkan **Flash Encryption** dan **Secure Boot** di ESP-IDF agar kredensial di partisi NVS tidak dapat dibaca lewat pembacaan flash mentah.

### 6. Implementasi Praktis (`wifi_prov_fsm.ino` & `wifi_fsm_sim.py`)

- **Firmware ESP32**: [`wifi_prov_fsm.ino`](content/chapter-12/src/wifi_prov_fsm/wifi_prov_fsm.ino) (menggunakan `WiFi.h` + `Preferences.h`, tombol *wipe* di `GPIO 27`, LED status di `GPIO 25`).
- **Simulasi Wokwi**: [`wokwi_diagram.json`](content/chapter-12/src/wokwi_diagram.json).
- **Verifikasi Software**: [`wifi_fsm_sim.py`](content/chapter-12/src/wifi_fsm_sim.py) menguji alur NVS kosong $\rightarrow$ *provisioning* (dengan *password* ter-redaksi) $\rightarrow$ urutan *exponential backoff* $1\text{ s} \dots 60\text{ s}$ $\rightarrow$ reset backoff saat `CONNECTED` (`outputs.md`). Firmware `.ino` masih berstatus **Belum diuji** terhadap compiler/simulator/router fisik.

### 7. Common Mistakes & Troubleshooting

| Masalah Umum | Penyebab | Solusi |
| --- | --- | --- |
| ESP32 tidak pernah menemukan SSID router kampus/rumah | Router hanya memancarkan pita **5 GHz** (`802.11ac/ax 5G`) | Aktifkan SSID **2,4 GHz** (`802.11b/g/n`) pada *Access Point* |
| Pin sensor `ADC2` (`GPIO 4 / 25 / 26`) gagal dibaca setelah `WiFi.begin()` | Konflik perangkat keras `ADC2` dan radio Wi-Fi pada ESP32 klasik | Pindahkan seluruh sensor analog ke **`ADC1` (`GPIO 32–39`)** |
| Kredensial langsung hilang / salah pasca-upload | Lupa menyimpan ke NVS atau karakter `\r\n` dari Serial Monitor ikut terbaca | Bersihkan `\r` sebelum parsing `\n` saat menyimpan string ke `Preferences` |
| Router hang saat 30 node reboot bersamaan | Reconnect instan tanpa jeda (*tight loop*) | Terapkan *exponential backoff* (plus *random jitter* di Chapter 19) |

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-12/exercises.md)):
1. Perbandingan metode *provisioning* (Serial, SoftAP, BLE) dan manajemen risiko kebocoran kredensial.
2. Analisis kode *blocking* `while (WiFi.status() != WL_CONNECTED)` dan perbaikan ke FSM non-blocking.
3. Perhitungan total waktu tunggu akumulatif untuk 6 kali kegagalan *exponential backoff* ($1\text{ s} \dots 32\text{ s}$).
4. Simulasi Python dengan [`wifi_fsm_sim.py`](content/chapter-12/src/wifi_fsm_sim.py) dan Mini Challenge penambahan *max-attempt alert* serta perintah status diagnostik.

## Tugas

Rancang dan implementasikan **Modul Wi-Fi Provisioning & Non-Blocking Reconnect Manager** untuk `ESP32-DevKitC V4` (spesifikasi & rubrik di tab **Tugas & Rubrik** — [assignment.md](content/chapter-12/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Device provisioning & penyimpanan NVS aman | 30 | Nol kredensial *hardcoded*, penyimpanan persisten `Preferences`, fitur *wipe/reset*, tanpa mencetak password di log |
| Connection state machine & exponential backoff | 30 | Non-blocking `millis()`, batas *timeout*, urutan *backoff* hingga batas maksimum tercapai, reset saat terhubung |
| Diagnostik Wi-Fi, Static/DHCP & keamanan | 20 | Pemantauan `RSSI`, dukungan konfigurasi IP/DHCP yang tepat, serta catatan keamanan WPA2/WPA3 |
| Dokumentasi, simulasi & kejujuran bukti | 20 | Diagram FSM jelas, log teredaksi, dan pelaporan status uji sesuai bukti aktual |

## Ringkasan

- Kredensial Wi-Fi tidak boleh ditanam di *source code*; simpan di partisi **NVS (`Preferences`)** melalui alur **Device Provisioning** dan sediakan tombol/perintah *factory wipe*.
- Kelola koneksi melalui *State Machine* non-blocking (`PROVISIONING`, `CONNECTING`, `CONNECTED`, `BACKOFF_WAIT`) dengan *timeout* dan **exponential backoff** agar node lokal tetap berjalan saat jaringan padam.
- ESP32 klasik hanya beroperasi pada $2{,}4\text{ GHz}$ dan menonaktifkan `ADC2` ketika Wi-Fi aktif.
- Simulasi logika provisioning dan backoff telah dieksekusi di Python (`outputs.md`); uji kompilasi `.ino` dan koneksi router fisik masih berstatus **Belum diuji** saat dokumen ini ditulis.

## Referensi

1. Espressif Systems, *ESP-IDF Wi-Fi Driver & Provisioning Guide*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi.html) (diperiksa 2026-11-11).
2. Espressif Systems, *Arduino-ESP32 WiFi & Preferences API*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/api/preferences.html](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/preferences.html) (diperiksa 2026-11-11).
3. NIST, *NISTIR 8259A: IoT Device Cybersecurity Capability Core Baseline*, [https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program](https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program) (diperiksa 2026-11-11).


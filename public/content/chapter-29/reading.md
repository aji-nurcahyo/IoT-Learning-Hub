# Chapter 29 — OTA Updates, Observability & Device Lifecycle

Memperbarui firmware pada ribuan perangkat lapangan yang telah terpasang di atap gedung, tiang lampu jalan, atau mesin pabrik terpencil menghadirkan risiko operasional paling tinggi dalam rekayasa sistem IoT. Kesalahan kecil pada baris kode baru dapat memicu kondisi mati suri permanen (*device bricking*) yang mengharuskan penggantian fisik perangkat secara manual dengan biaya yang sangat mahal.

Mekanisme **Over-The-Air (OTA) Updates** kelas industri wajib menerapkan arsitektur memori **Dual-Bank (Partisi A/B)**, verifikasi integritas citra biner menggunakan tanda tangan digital kriptografis (*cryptographic code signing*), peluncuran bertahap (*canary deployment*), serta pengujian kesehatan runtime otomatis yang mampu melakukan pemulihan mandiri (*Automatic Rollback*) seketika jika firmware baru mengalami kegagalan booting atau *bootloop*.

![Arsitektur Partisi Dual-Bank A/B, Verifikasi Kriptografis, dan Automatic Rollback Engine](content/chapter-29/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Memahami Arsitektur Partisi Dual-Bank A/B**: Menjelaskan struktur tabel partisi flash memori ESP32 (`app0`, `app1`, dan `otadata`) serta mekanisme pergantian pointer bootloader saat pembaruan firmware.
2. **Menerapkan Verifikasi Tanda Tangan Kriptografis**: Mengonfigurasi validasi hash SHA-256 dan tanda tangan digital asimetris (RSA-3072 / ECDSA) pada citra biner sebelum proses penulisan ke flash diizinkan.
3. **Menerapkan Siklus Deployment Bertahap (Canary Release)**: Merancang strategi peluncuran firmware bertahap (Canary $5\% \rightarrow 25\% \rightarrow 100\%$) untuk membatasi dampak ledakan (*blast radius*) jika terjadi bug tersembunyi.
4. **Membangun Mekanisme Pemulihan Mandiri (Automatic Rollback)**: Mengimplementasikan siklus status `PENDING_VERIFY`, penghitung kegagalan boot (*boot counter monitor*), dan panggilan fungsi pembatalan otomatis jika perangkat mengalami *kernel panic* atau gagal tersambung ke jaringan.
5. **Mengelola Siklus Hidup Penuh Perangkat (Device Lifecycle Observability)**: Melacak status evolusi perangkat dari tahap pabrikasi (*Factory/Provisioned*), operasional aktif (*Active*), pembaruan sistem (*Updating*), hingga pemensiunan (*Decommissioned*).

## Prasyarat

- Memahami arsitektur partisi flash, bootloader, dan NVS dari [Chapter 08](chapter-08).
- Memahami protokol komunikasi HTTP Client dan MQTT dari [Chapter 13](chapter-13) dan [Chapter 14](chapter-14).
- Memahami konsep kriptografi asimetris dan integritas hash dari [Chapter 28](chapter-28).

## Konsep dan teori

### 1. Struktur Partisi Flash Dual-Bank (A/B)

Pada arsitektur memori ESP32 standar (misal flash $4\text{ MB}$), ruang penyimpanan dibagi menjadi beberapa partisi khusus:

| Nama Partisi | Tipe | Sub-tipe | Ukuran Tipikal | Fungsi Operasional |
| :--- | :---: | :---: | :---: | :--- |
| **`nvs`** | Data | NVS | $16\text{ KB}\text{–}64\text{ KB}$ | Menyimpan Wi-Fi SSID, konfigurasi twin, sertifikat |
| **`otadata`** | Data | OTA | $8\text{ KB}$ | Menyimpan pointer bank mana yang aktif di-booting |
| **`app0` (Bank A)** | App | OTA_0 | $1{,}25\text{ MB}\text{–}1{,}5\text{ MB}$ | Partisi firmware utama (slot aktif awal) |
| **`app1` (Bank B)** | App | OTA_1 | $1{,}25\text{ MB}\text{–}1{,}5\text{ MB}$ | Partisi firmware cadangan / target pengunduhan baru |

Keuntungan arsitektur Dual-Bank:
- Mikrokontroler tetap menjalankan firmware lama di `app0` secara normal selama proses pengunduhan firmware baru berlangsung ke partisi `app1` (*zero downtime*).
- Jika listrik padam di tengah proses pengunduhan, sistem tidak rusak (*non-bricking*); bootloader tetap menjalankan firmware stabil di `app0`.

### 2. Tanda Tangan Kriptografis Firmware (Code Signing)

Firmware biner mentah tidak boleh langsung dieksekusi tanpa validasi keaslian. Penyerang yang berhasil memalsukan respons DNS server dapat mengarahkan perangkat untuk mengunduh firmware peretas (*malicious firmware*).

Alur penandatanganan kode:
1. Server build menghasilkan citra biner `firmware.bin`.
2. Server menghitung hash SHA-256 dari biner tersebut dan mengenkripsinya menggunakan kunci privat pengembang (*Developer Private Key*):
   $$\text{Signature} = \text{Sign}_{\text{PrivKey}}(\text{SHA256}(\text{Firmware Bytes}))$$
3. Mikrokontroler mengunduh paket lengkap (biner + tanda tangan), lalu memverifikasi tanda tangan menggunakan kunci publik terpercaya (*Root Public Key*) yang telah terkunci di dalam memori bootloader perangkat keras (*Secure Boot*):
   $$\text{Verify}_{\text{PubKey}}(\text{Digest}, \text{Signature}) \stackrel{?}{=} \text{True}$$
4. Jika tanda tangan tidak cocok atau biner mengalami perubahan 1 bit saja, seluruh paket langsung dibuang.

### 3. Mesin Status Health-Check & Automatic Rollback

ESP-IDF menyediakan pustaka resmi `esp_ota_ops.h` yang mengimplementasikan mesin status pemulihan mandiri:

1. **Unduh & Tulis**: Firmware baru ditulis ke partisi pasif (misal `app1`).
2. **Switch Boot Pointer**: Bootloader memperbarui sektor `otadata` dengan status partisi `ESP_OTA_IMG_PENDING_VERIFY`.
3. **Reboot**: Perangkat me-reboot dirinya sendiri ke partisi `app1`.
4. **Fase Evaluasi (Health-Check)**:
   - Aplikasi baru harus membuktikan dirinya sehat: inisialisasi pin I/O sukses, sensor merespons, koneksi Wi-Fi tersambung, dan handshake MQTT dengan broker berhasil.
   - Jika seluruh pengujian berhasil, aplikasi memanggil:
     `esp_ota_mark_app_valid_cancel_rollback();`
     Status di `otadata` berubah menjadi `ESP_OTA_IMG_VALID` (firmware resmi permanen).
5. **Kondisi Kegagalan (Automatic Rollback)**:
   - Jika firmware baru mengalami crash (*kernel panic / exception*), memori bocor, atau gagal terhubung ke broker dalam durasi waktu tertentu, *Hardware Watchdog Timer* me-reset mikrokontroler.
   - Bootloader mendeteksi bahwa partisi masih berstatus `PENDING_VERIFY`. Begitu jumlah reboot melebihi batas kuota (misal $2\text{ kali}$), bootloader secara otomatis menandai `app1` sebagai `INVALID` dan beralih kembali menjalankan firmware lama yang terbukti stabil di `app0` (*automatic self-healing*).

### 4. Strategi Peluncuran Bertahap (Canary Deployment)

Memperbarui $10.000$ unit perangkat secara serentak dalam satu detik (*big bang release*) adalah praktik berbahaya. Jika terdapat bug tersembunyi yang baru muncul pada suhu tinggi atau jam tertentu, seluruh armada akan lumpuh total secara bersamaan.

Praktik terbaik industri:
1. **Fase 1 (Internal Test)**: Update disalurkan ke $5\text{ unit}$ perangkat laboratorium.
2. **Fase 2 (Canary Group)**: Update disalurkan ke $5\%$ armada produksi acak. Sistem memantau metrik crash rate, PDR, dan stabilitas baterai selama $24\text{–}48\text{ jam}$.
3. **Fase 3 (Staged Wave)**: Jika kelompok canary stabil, rilis diperluas ke $25\%$, lalu $50\%$, dan akhirnya $100\%$ armada penuh.

## Latihan

1. **Analisis Dual-Bank Partitioning**:
   Jelaskan mengapa mikrokontroler berkapasitas flash kecil ($1\text{ MB}$) sering kali tidak dapat menerapkan skema partisi Dual-Bank A/B untuk binary aplikasi berukuran $600\text{ KB}$, dan apa risiko fatal yang dihadapi jika pembaruan OTA dilakukan dengan menimpa partisi tunggal secara langsung (*Single Partition In-Place Flashing*).
2. **Mekanisme Otomatis Anti-Bricking**:
   Sebuah firmware baru versi `v2.0.0` berhasil diunduh dan ditulis ke partisi `app1`. Namun, programmer lupa menyertakan kredensial Wi-Fi yang benar sehingga mikrokontroler tidak pernah bisa terhubung ke internet. Uraikan bagaimana siklus `PENDING_VERIFY` dan batas toleransi reboot (*boot count threshold*) menyelamatkan perangkat tersebut dari kematian permanen.
3. **Mitigasi Serangan Downgrade**:
   Dalam keamanan OTA, serangan *Downgrade Attack* terjadi saat penyerang memaksa perangkat mengunduh firmware resmi versi lama yang sah namun memiliki celah keamanan kritis yang telah diketahui umum (*known vulnerability*). Bagaimana fitur *Anti-Rollback Version Counter* pada bootloader mencegah serangan ini?

## Tugas

Bangun dan uji sistem simulator partisi Dual-Bank A/B dan pemulihan otomatis OTA menggunakan Python:

1. **Model Partisi Dual-Bank A/B**:
   Susun kelas `OtaStateMachine` yang memodelkan dua bank aplikasi (`app0` dan `app1`) serta melacak status partisi (`VALID`, `PENDING_VERIFY`, `INVALID`, `EMPTY`).
2. **Pembangkitan & Verifikasi Tanda Tangan Kriptografis**:
   Implementasikan fungsi `generate_signed_binary` dan `verify_firmware_package` yang memverifikasi integritas digest SHA-256 dan keabsahan tanda tangan digital HMAC/asimetris sebelum data diizinkan ditulis ke flash.
3. **Simulasi Kegagalan Bootloop & Automatic Rollback**:
   Uji skenario di mana firmware baru yang sah mengalami crash berturut-turut pada saat reboot. Buktikan bahwa bootloader simulator mendeteksi kegagalan kuota boot dan secara otomatis memulihkan bank aktif kembali ke partisi lama yang stabil.
4. **Simulasi Pembaruan Sukses & Konfirmasi Permanen**:
   Uji skenario kedua di mana firmware stabil berhasil booting dan memanggil fungsi `confirm_firmware_health`, membuktikan konfirmasi status permanen tanpa pemicuan rollback.

### Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Model Partisi Dual-Bank & Verifikasi Tanda Tangan** | 35% | Struktur partisi A/B dimodelkan akurat; paket biner korup atau dengan signature salah ditolak sebelum tahap flashing. |
| **Logika Automatic Rollback & Anti-Bootloop** | 35% | Siklus status PENDING_VERIFY dan kuota bootloop bekerja presisi; kegagalan booting memicu pemulihan otomatis ke partisi lama yang valid. |
| **Konfirmasi Kesehatan & Dokumentasi Hasil Uji** | 30% | Alur konfirmasi sukses memvalidasi firmware secara permanen; seluruh 3 skenario pengujian diverifikasi secara deterministik pada laporan. |

## Ringkasan

1. **Ketahanan Partisi Ganda**: Skema partisi Dual-Bank A/B menjamin perangkat tidak akan mengalami bricking meskipun terjadi pemadaman listrik di tengah proses transfer firmware.
2. **Keabsahan Kriptografis**: Pemeriksaan tanda tangan digital memastikan hanya citra biner resmi dari pengembang sah yang diizinkan dieksekusi di memori flash.
3. **Penyembuhan Mandiri**: Mekanisme `PENDING_VERIFY` dan automatic rollback memulihkan perangkat secara mandiri saat firmware baru mengalami kegagalan fatal di lapangan.
4. **Penyebaran Bertahap**: Strategi rilis canary meminimalkan risiko operasional dengan membatasi dampak kesalahan kode hanya pada sebagian kecil armada uji.

## Referensi

1. Espressif Systems. *ESP-IDF Programming Guide: Over The Air Updates (OTA) & Anti-rollback*. https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html
2. ARM Mbed. *Mbed OS Bootloader and Dual-Bank Firmware Update Architecture*.
3. Internet Engineering Task Force (IETF). *RFC 9019: A Firmware Update Architecture for Internet of Things Devices (SUIT)*.

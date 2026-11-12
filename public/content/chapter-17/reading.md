# Chapter 17 — Bluetooth Low Energy (BLE)

Pada IoT jarak dekat, banyak perangkat sensor tidak terus-menerus membutuhkan jalur internet langsung ke *router* Wi-Fi, melainkan berkomunikasi hemat daya dengan *smartphone* teknisi atau *gateway* lokal pada jarak beberapa meter. **Bluetooth Low Energy (BLE)** dirancang dari awal untuk skenario *burst* singkat berdaya rendah—berbeda mendasar dengan *Bluetooth Classic* (BR/EDR) yang berorientasi *streaming* audio kontinu. Bab ini membedah peran perangkat di lapis **GAP**, struktur data **GATT**, penghematan energi melalui interval iklan dan koneksi, serta implementasi *GATT Server* pada ESP32.

![Arsitektur BLE GAP dan Hierarki GATT Profile](content/chapter-17/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, Anda diharapkan mampu:

1. Membedakan *Bluetooth Classic* (BR/EDR) dan **Bluetooth Low Energy (BLE)** pada pita $2{,}4\text{ GHz}$ dari sisi topologi, *duty cycle*, *throughput*, dan konsumsi daya.
2. Menjelaskan peran perangkat pada lapis **GAP** (*Broadcaster*, *Observer*, *Peripheral*, *Central*) serta fungsi 3 kanal *advertising* (`37, 38, 39`) dan 37 kanal data.
3. Merancang struktur **GATT Profile** lengkap (*Service UUID*, *Characteristic UUID*, *Properties* `READ`/`WRITE`/`NOTIFY`/`INDICATE`, serta *Descriptor CCCD* `0x2902`).
4. Menghitung jumlah paket fragmentasi akibat batas **ATT MTU** (`23` vs `247` byte) serta mengestimasi arus rata-rata dan umur baterai berdasarkan *Advertising Interval*.
5. Mengimplementasikan dan mendiagnosis *GATT Server* ESP32 (`BLEDevice`, `BLEServer`, `BLE2902`), termasuk memulihkan *advertising* otomatis saat *Central* terputus.

## Prasyarat

- Pemahaman representasi data biner (*little-endian*, `int16`, *bitmask*) dan serialisasi JSON dasar ([Chapter 05](chapter-05) dan [Chapter 13](chapter-13)).
- Pemahaman arsitektur Wi-Fi pada ESP32 dan konsep berbagi antena radio $2{,}4\text{ GHz}$ (*coexistence*) ([Chapter 12](chapter-12)).

## Konsep dan teori

### 1. Bluetooth Classic vs BLE & Pita Frekuensi

Meski sama-sama beroperasi di pita ISM $2{,}400\text{–}2{,}4835\text{ GHz}$, *Bluetooth Classic* (BR/EDR) membagi spektrum menjadi 79 kanal berlebar $1\text{ MHz}$ untuk tautan *point-to-point* kontinu (seperti audio A2DP atau port serial SPP), sedangkan **BLE** membagi pita tersebut menjadi **40 kanal berlebar $2\text{ MHz}$**:

- **3 kanal *Advertising* primer** (kanal `37` pada $2402\text{ MHz}$, `38` pada $2426\text{ MHz}$, dan `39` pada $2480\text{ MHz}$) yang ditempatkan sengaja di sela-sela antara kanal Wi-Fi non-overlapping (`1, 6, 11`) agar penemuan perangkat tetap andal meski di lingkungan Wi-Fi padat.
- **37 kanal Data** yang memakai *Adaptive Frequency Hopping* (AFH) untuk menghindari kanal yang sedang mengalami interferensi.

### 2. Lapisan GAP: Penemuan Perangkat dan Peran Koneksi

**Generic Access Profile (GAP)** mengatur bagaimana perangkat mengumumkan keberadaannya (*advertising*) dan menjalin koneksi:

1. **Broadcaster** (hanya menyiarkan *beacon* satu arah, misalnya *iBeacon* / *Eddystone*) dan **Observer** (hanya memindai tanpa meminta koneksi).
2. **Peripheral** (umumnya sensor ESP32 atau *wearable*): menyiarkan paket `ADV_IND` (maksimal `31` byte *Advertising Data* + `31` byte *Scan Response* opsional pada BLE 4.x *Legacy Advertising*) dan menerima permintaan koneksi dari *Central*.
3. **Central** (biasanya *smartphone* atau *Raspberry Pi gateway*): memindai kanal `37/38/39` lalu mengirim `CONNECT_IND` yang menentukan parameter koneksi awal, termasuk **Connection Interval** ($7{,}5\text{ ms}\text{ s.d. }4{,}0\text{ s}$ dalam kelipatan $1{,}25\text{ ms}$).

> **Jebakan klasik ESP32 BLE**: saat *Central* terhubung, radio *Peripheral* otomatis berhenti melakukan *advertising* *connectable*. Ketika *Central* memutus koneksi, ESP32 **tidak otomatis** kembali terlihat sampai *callback* `onDisconnect()` (atau *loop state machine*) memanggil kembali `startAdvertising()`.

### 3. Hierarki GATT (Generic Attribute Profile)

Setelah koneksi GAP terbentuk, pertukaran data terstruktur berlangsung melalui **GATT** di atas protokol **ATT** (*Attribute Protocol*). Umumnya *Peripheral* bertindak sebagai **GATT Server** (penyimpan tabel atribut) dan *Central* sebagai **GATT Client**:

- **Profile & Service**: Pengelompokan logis fungsi perangkat. Standar Bluetooth SIG memakai UUID pendek `16-bit` (seperti `0x181A` untuk *Environmental Sensing* atau `0x180F` untuk *Battery Service*), sementara aplikasi kustom wajib memakai UUID `128-bit` acak agar tidak berbenturan.
- **Characteristic**: Elemen data konkret di dalam *Service*, memiliki *UUID* (misal `0x2A6E` untuk *Temperature* berskala $0{,}01\,^\circ\text{C}$ dalam format `int16` *little-endian*), **Value**, dan bitmask **Properties**:
  - `READ`: Client membaca nilai terbaru atas permintaan (*pull*).
  - `WRITE` / `WRITE_NR`: Client menulis perintah/konfigurasi ke Server (dengan atau tanpa balasan ATT ACK).
  - `NOTIFY`: Server mendorong pembaruan asinkron ke Client **tanpa** menunggu konfirmasi lapis ATT (cepat, *overhead* rendah).
  - `INDICATE`: Server mendorong pembaruan ke Client dan **menunggu** ATT *Handle Value Confirmation* (lebih andal, tetapi maksimal hanya 1 transaksi per *Connection Interval* atau $\sim 2\times$ latensi konfirmasi).
- **Descriptor — khususnya CCCD (`0x2902`)**: Agar Server diizinkan mengirim `NOTIFY` atau `INDICATE`, *GATT Client* wajib menulis bit `0x0001` (*Notify*) atau `0x0002` (*Indicate*) ke *Client Characteristic Configuration Descriptor* (`0x2902`, pada pustaka ESP32 diwakili oleh `new BLE2902()`). Tanpa descriptor ini, langganan notifikasi dari aplikasi *smartphone* gagal.

### 4. ATT MTU, Fragmentasi, dan Anggaran Daya

Secara baku (BLE 4.0), ukuran **ATT MTU** (*Maximum Transmission Unit*) adalah **$23\text{ byte}$**. Karena header ATT untuk operasi *Read/Write/Notify* memakai `3 byte` (`1 B` opcode + `2 B` attribute handle), ruang payload bersih per PDU hanya:

$$L_{\text{payload, max}} = \text{ATT\_MTU} - 3\text{ byte}$$

Dengan demikian, payload JSON atau biner sepanjang $64\text{ byte}$ pada MTU standar `23 B` hanya muat $20\text{ B}$ per paket dan harus dipecah menjadi $\lceil 64 / 20 \rceil = 4$ notifikasi terpisah. Setelah *Central* dan *Peripheral* menegosiasikan **MTU Exchange** (misalnya `247 B`), seluruh $64\text{ byte}$ terkirim utuh dalam **1 paket tunggal** (memangkas *overhead* radio sekaligus mencegah pesan JSON terpotong di tengah).

Di sisi daya, node yang hanya beriklan periodik setiap $T_{\text{adv}}$ dengan durasi bangun aktif $t_{\text{act}}$ pada arus $I_{\text{act}}$ dan arus tidur $I_{\text{sleep}}$ memiliki arus rata-rata:

$$I_{\text{avg}} = \frac{t_{\text{act}} \cdot I_{\text{act}} + (T_{\text{adv}} - t_{\text{act}}) \cdot I_{\text{sleep}}}{T_{\text{adv}}}$$

### 5. Worked Example — Simulasi `ble_gatt_sim.py`

Pada skrip [`ble_gatt_sim.py`](content/chapter-17/src/ble_gatt_sim.py), kita menguji tiga aspek kuantitatif:

1. **Pengodean GATT `0x2A6E`**: Suhu $27{,}85\,^\circ\text{C}$ dikalikan $100$ menjadi bilangan bulat `2785` (`0x0AE1`). Dalam urutan *little-endian* 2 byte, nilainya dikirim sebagai `e1 0a` dan didekode kembali persis `27.85 C`.
2. **Dampak Negosiasi MTU untuk 64-byte payload**:
   - `ATT_MTU = 23` $\rightarrow$ kapasitas bersih `20 B` $\rightarrow$ butuh **`4` paket**.
   - `ATT_MTU = 65` $\rightarrow$ kapasitas bersih `62 B` $\rightarrow$ butuh **`2` paket**.
   - `ATT_MTU = 247` $\rightarrow$ kapasitas bersih `244 B` $\rightarrow$ butuh **`1` paket**.
3. **Umur Baterai Koin `CR2032` ($220\text{ mAh}$)** dengan model bangun $t_{\text{act}} = 3{,}5\text{ ms}$, $I_{\text{act}} = 9{,}5\text{ mA}$, $I_{\text{sleep}} = 5\,\mu\text{A}$:
   - $T_{\text{adv}} = 100\text{ ms}$ $\rightarrow$ $I_{\text{avg}} = 0{,}3373\text{ mA}$ $\rightarrow$ **`27.2` hari** (responsif, tetapi boros).
   - $T_{\text{adv}} = 1000\text{ ms}$ $\rightarrow$ $I_{\text{avg}} = 0{,}0382\text{ mA}$ $\rightarrow$ **`239.8` hari** (~8 bulan).
   - $T_{\text{adv}} = 2000\text{ ms}$ $\rightarrow$ $I_{\text{avg}} = 0{,}0216\text{ mA}$ $\rightarrow$ **`424.1` hari** (> 1 tahun).

> **Catatan keamanan & arsitektur ESP32**: Untuk data sensitif, BLE tidak boleh hanya mengandalkan mode *Just Works* tanpa autentikasi; gunakan *LE Secure Connections* (ECDH) dengan *Passkey/Numeric Comparison* bila diperlukan, dan perhatikan bahwa BLE serta Wi-Fi di ESP32 berbagi satu modul radio $2{,}4\text{ GHz}$ secara bergiliran (*coexistence*), sehingga penggunaan keduanya serentak menuntut alokasi RAM dan manajemen interval yang hati-hati.

### 6. Implementasi Firmware & Troubleshooting Umum

Sketsa [`ble_gatt_sensor.ino`](content/chapter-17/src/ble_gatt_sensor/ble_gatt_sensor.ino) memperlihatkan pola minimal namun tangguh untuk *GATT Server* ESP32: menggunakan `BLEDevice::setMTU(128)`, mendaftarkan descriptor `new BLE2902()` pada karakteristik `NOTIFY`, memvalidasi rentang input pada `onWrite()`, dan memanggil ulang `pServer->startAdvertising()` setelah *Central* putus.

**Kesalahan umum & diagnosa**:
- **Karakteristik tidak bisa di-*subscribe* di aplikasi nRF Connect**: Lupa menambahkan descriptor `BLE2902` (`0x2902`) atau lupa flag `BLECharacteristic::PROPERTY_NOTIFY`.
- **Perangkat hilang selamanya setelah klien pertama keluar**: Callback `onDisconnect` tidak memicu `startAdvertising()`.
- **Sketsa kehabisan flash/RAM (`IRAM/DRAM overflow`)**: Pustaka Bluedroid bawaan ESP32 cukup besar; jika memakai Wi-Fi + BLE sekaligus, pilih skema partisi *Minimal SPIFFS* / *Huge APP* atau pertimbangkan pustaka lebih ringan seperti *NimBLE-Arduino*.

## Latihan

Latihan konseptual, analisis ATT/GATT, perhitungan daya, dan tugas pemrograman tersedia pada tab **[Exercises](chapter-17#exercises)**.

## Tugas

Rancang *GATT Profile* untuk stasiun iklim mikro bertenaga baterai dan selesaikan implementasinya pada tab **[Tugas & Rubrik](chapter-17#assignment)** (total bobot 100 poin).

## Ringkasan

- BLE menggunakan **40 kanal $2\text{ MHz}$** pada pita $2{,}4\text{ GHz}$: kanal `37, 38, 39` untuk *advertising* dan 37 kanal untuk pertukaran data berbasis *frequency hopping*.
- **GAP** mengatur penemuan dan status koneksi (*Peripheral* vs *Central*), sedangkan **GATT** menstrukturkan data dalam hierarki *Service $\rightarrow$ Characteristic $\rightarrow$ Descriptor (CCCD `0x2902`)*.
- Negosiasi **ATT MTU** dari baku `23 B` menjadi `247 B` memangkas fragmentasi paket dan *overhead* transmisi radio secara signifikan.
- Menjaga **Advertising Interval** tetap realistis ($500\text{–}2000\text{ ms}$) dan memulihkan *advertising* pada `onDisconnect()` adalah kunci keandalan node BLE lapangan.

## Referensi

1. Bluetooth SIG, *Bluetooth Core Specification & Technical Overview*, [https://www.bluetooth.com/learn-about-bluetooth/tech-overview/](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/).
2. Bluetooth SIG, *GATT Specification Supplement (Assigned Numbers: 0x181A, 0x2A6E, 0x2902)*, [https://www.bluetooth.com/specifications/assigned-numbers/](https://www.bluetooth.com/specifications/assigned-numbers/).
3. Espressif Systems, *Arduino-ESP32 BLE Library Reference & Coexistence Notes*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/](https://docs.espressif.com/projects/arduino-esp32/en/latest/).


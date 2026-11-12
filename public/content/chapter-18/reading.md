# Chapter 18 — LoRa & LoRaWAN Fundamentals

Ketika aplikasi *smart agriculture*, pemantauan sungai, atau kehutanan membutuhkan jangkauan kilometer dengan baterai yang harus bertahan berbulan-bulan hingga tahunan, Wi-Fi dan BLE tidak lagi memadai dan seluler sering kali terlalu boros daya. **LPWAN** (*Low-Power Wide-Area Network*) mengisi celah ini dengan mengorbankan *bandwidth* demi jangkauan dan efisiensi energi. Bab ini membedah pemisahan tegas antara **LoRa** sebagai modulasi lapisan fisik (PHY) dan **LoRaWAN** sebagai protokol lapisan MAC/jaringan, perhitungan matematis **Time-on-Air (ToA)** serta *link budget*, arsitektur *Star-of-Stars*, keamanan OTAA/ABP, serta keharusan memverifikasi parameter regional resmi sebelum menyalakan pemancar radio.

![Arsitektur LoRa PHY vs LoRaWAN Star-of-Stars](content/chapter-18/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, Anda diharapkan mampu:

1. Membedakan **LoRa** (modulasi fisik *Chirp Spread Spectrum*) dengan **LoRaWAN** (protokol MAC/jaringan standar LoRa Alliance) secara arsitektural.
2. Menjelaskan pengaruh **Spreading Factor (SF7–SF12)**, **Bandwidth (BW)**, dan **Coding Rate (CR)** terhadap sensitivitas penerima, jarak, dan *Time-on-Air*.
3. Menghitung *symbol duration* ($T_{\text{sym}}$), *Time-on-Air* ($T_{\text{packet}}$), serta *Free-Space Path Loss* (FSPL) dan *link margin* dari sebuah skenario transmisi LoRa.
4. Menguraikan arsitektur **Star-of-Stars LoRaWAN** (*End-Device $\rightarrow$ Gateway $\rightarrow$ Network Server $\rightarrow$ Application Server*), perbedaan **Class A/B/C**, mekanisme **OTAA vs ABP**, dan **ADR**.
5. Menjelaskan mengapa parameter pita frekuensi sub-GHz, daya pancar (EIRP), dan batas *duty cycle* / *dwell time* **wajib diverifikasi** terhadap **LoRa Alliance Regional Parameters (RP2)** dan regulator spektrum nasional sebelum implementasi lapangan.

## Prasyarat

- Pemahaman dasar rasio sinyal terhadap derau (SNR), *decibel* (dB/dBm), dan *link budget* komunikasi nirkabel ([Chapter 11](chapter-11) dan [Chapter 12](chapter-12)).
- Pemahaman antarmuka **SPI** karena modul radio transceiver LoRa (`SX1276`, `SX1278`, `SX1262`, `RFM95`) umumnya berkomunikasi dengan ESP32 melalui bus SPI ([Chapter 16](chapter-16)).

## Konsep dan teori

### 1. Membedakan LoRa (PHY) dan LoRaWAN (MAC/Network)

Banyak kesalahan perancangan awal muncul karena menganggap LoRa dan LoRaWAN adalah hal yang sama:

- **LoRa (*Long Range*) adalah Lapisan Fisik (PHY)** hak cipta Semtech berbasis **Chirp Spread Spectrum (CSS)**. Sinyal informasi dimodulasi ke dalam pulsa frekuensi yang menyapu naik atau turun (*up-chirp* / *down-chirp*) di sepanjang lebar pita tertentu (`BW`). Berkat sifat penyebaran spektrum ini, penerima LoRa mampu mendeteksi paket bahkan ketika daya sinyal berada **di bawah lantai derau** (*noise floor*), yakni pada rasio SNR negatif hingga sekitar $-20\text{ dB}$ pada `SF12`. Dua ESP32 dengan modul SX127x bisa berkomunikasi *peer-to-peer* hanya dengan LoRa PHY, tetapi secara baku tidak memiliki mekanisme *addressing* jaringan, pencegahan tabrakan antar-ribuan node, maupun enkripsi ujung-ke-ujung terstandar.
- **LoRaWAN adalah Lapisan MAC & Arsitektur Jaringan** terbuka yang distandardisasi oleh **LoRa Alliance** dan bekerja *di atas* modulasi LoRa PHY (serta FSK di wilayah tertentu). LoRaWAN mendefinisikan format frame MAC, aktivasi perangkat (**OTAA/ABP**), enkripsi dua lapis AES-128 (`NwkSKey` & `AppSKey`), *Adaptive Data Rate* (ADR), dan arsitektur perutean *End-Device $\rightarrow$ Gateway $\rightarrow$ Network Server $\rightarrow$ Application Server*.

### 2. Parameter Modulasi LoRa PHY: SF, BW, dan CR

Tiga tuas utama pada transceiver LoRa mengendalikan pertukaran (*trade-off*) antara jarak tempuh, kekebalan interferensi, dan waktu mengudara:

1. **Spreading Factor ($\text{SF} \in \{7, 8, 9, 10, 11, 12\}$)**: Setiap simbol membawa $\text{SF}$ bit mentah dan terdiri atas $2^{\text{SF}}$ *chip*. Durasi satu simbol adalah:

$$T_{\text{sym}} = \frac{2^{\text{SF}}}{\text{BW}}$$

   Kenaikan 1 tingkat `SF` (misalnya `SF7` $\rightarrow$ `SF8`) menggandakan durasi simbol (~2× lebih lama di udara dan ~2× lebih boros energi baterai), tetapi meningkatkan *processing gain* serta memperbaiki sensitivitas penerima sekitar $2{,}5\text{ dB}$. Selain itu, paket dengan `SF` berbeda pada kanal yang sama bersifat nyaris ortogonal sehingga *gateway* dapat menerima keduanya hampir bersamaan.
2. **Bandwidth ($\text{BW}$)**: Lebar spektrum sapuan *chirp*, lazimnya $125\text{ kHz}$, $250\text{ kHz}$, atau $500\text{ kHz}$. Menggandakan `BW` memangkas `ToA` menjadi setengahnya, namun mengurangi sensitivitas karena lebih banyak derau termal ikut masuk ke *receiver*.
3. **Coding Rate ($\text{CR} \in \{4/5, 4/6, 4/7, 4/8\}$)**: Redundansi *Forward Error Correction* (FEC) untuk memulihkan bit rusak akibat interferensi singkat tanpa meminta kirim ulang.

### 3. Persamaan Time-on-Air (ToA) & Link Budget

Mengacu catatan aplikasi **Semtech AN1200.13**, jumlah simbol payload ($n_{\text{payload}}$) dan total *Time-on-Air* ($T_{\text{packet}}$) dihitung dari:

$$T_{\text{preamble}} = (n_{\text{preamble}} + 4{,}25) \cdot T_{\text{sym}}$$

$$n_{\text{payload}} = 8 + \max\left(\left\lceil \frac{8\,\text{PL} - 4\,\text{SF} + 28 + 16\,\text{CRC} - 20\,\text{IH}}{4(\text{SF} - 2\,\text{DE})} \right\rceil (\text{CR}_p + 4), \; 0\right)$$

$$T_{\text{packet}} = T_{\text{preamble}} + n_{\text{payload}} \cdot T_{\text{sym}}$$

Di sini $\text{PL}$ adalah panjang payload (byte), $\text{CRC} \in \{0,1\}$, $\text{IH}=0$ untuk *explicit header*, $\text{CR}_p \in \{1..4\}$ untuk `4/5`..`4/8`, dan **DE** (*Low Data Rate Optimization*) bernilai `1` otomatis ketika $T_{\text{sym}} \ge 16\text{ ms}$ (umumnya `SF11` dan `SF12` pada `BW = 125 kHz`).

Di lapis propagasi, daya terima estimasi ($P_{\text{rx}}$) dan *link margin* ditentukan oleh:

$$P_{\text{rx}}\text{ (dBm)} = P_{\text{tx}} + G_{\text{tx}} + G_{\text{rx}} - L_{\text{kabel}} - L_{\text{path}} - M_{\text{fading}}$$

$$\text{Margin (dB)} = P_{\text{rx}} - S_{\text{rx}}(\text{SF}, \text{BW})$$

### 4. Arsitektur LoRaWAN Star-of-Stars, Class A/B/C & Keamanan

Berbeda dari jaringan *mesh* di mana node saling meneruskan paket orang lain (sehingga node perantara cepat kehabisan baterai), **LoRaWAN** memakai topologi **Star-of-Stars**:

1. **End-Device**: Memancarkan uplink RF ke segala arah (*broadcast RF*); tidak terikat ke satu *gateway* tertentu.
2. **Gateway**: Berperan seperti jembatan transparan (*Packet Forwarder* multi-kanal) yang menerima beberapa `SF` sekaligus dan meneruskannya lewat IP (*Ethernet/Wi-Fi/4G*) ke *Network Server*. Jika dua gateway menerima uplink yang sama, keduanya meneruskan ke *server*.
3. **Network Server (LNS)**: Otak jaringan yang melakukan **deduplikasi** paket dari multi-gateway, memverifikasi integritas **MIC** (*Message Integrity Code*) memakai **`NwkSKey`**, menjalankan **ADR** (*Adaptive Data Rate*) untuk menurunkan `SF` node yang sinyalnya kuat agar menghemat spektrum, serta menjadwalkan *downlink* lewat gateway dengan RSSI/SNR terbaik.
4. **Application Server**: Mendekripsi muatan aplikasi (`FRMPayload`) dengan **`AppSKey`** (AES-128) dan meneruskannya ke dashboard via MQTT atau HTTP Webhook.

**Kelas Perangkat LoRaWAN**:
- **Class A** (*wajib di semua perangkat*): Paling hemat baterai; hanya membuka dua jendela terima singkat **RX1** dan **RX2** tepat setelah mengirim *uplink*.
- **Class B**: Menambah jendela terima terjadwal berbasis *beacon* GPS dari *gateway*.
- **Class C**: Penerima terus aktif kecuali saat memancarkan *uplink* (butuh catu daya eksternal, cocok untuk aktuator listrik PLN).

Untuk aktivasi jaringan, **OTAA** (*Over-The-Air Activation* memakai `DevEUI`, `AppEUI/JoinEUI`, dan `AppKey`) jauh lebih aman dan dianjurkan untuk produksi dibanding **ABP** (*Activation By Personalization* dengan kunci sesi statis), karena OTAA menegosiasikan kunci sesi baru dan *frame counter* bersih setiap *Join*.

### 5. Kepatuhan Parameter Regional (Regulatory Guard)

Frekuensi operasi sub-GHz ISM, lebar kanal aktif, daya pancar maksimum (*EIRP*), dan pembatasan waktu udara (*duty cycle* atau *dwell time*) **berbeda antarnegara dan wilayah** (misalnya `EU868`, `US915`, `AS923-1/2/3/4`). Oleh karena itu, modul pembelajaran ini **tidak mengasumsikan atau menetapkan** angka frekuensi legal, daya pancar, maupun batas *duty cycle* untuk lokasi Anda secara sepihak; insinyur IoT **wajib merujuk dokumen resmi *LoRa Alliance Regional Parameters (RP2)*** dan peraturan otoritas spektrum nasional setempat (seperti DJID/Komdigi di Indonesia) sebelum menyusun konfigurasi kanal atau mengudara di lapangan.

### 6. Worked Example — Hasil `lora_airtime_budget.py`

Skrip [`lora_airtime_budget.py`](content/chapter-18/src/lora_airtime_budget.py) menghitung dampak kenaikan `SF7` ke `SF12` untuk payload `24 byte` (`11 B` data sensor + `13 B` header LoRaWAN minimum) pada `BW = 125 kHz`, `CR = 4/5`:

| SF | $T_{\text{sym}}$ (ms) | DE | ToA (ms) | Contoh jeda 1% (*ilustratif*) | Sensitivitas Ref. SX1276 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `SF7` | `1.024` | `0` | **`61.70` ms** | `6.11` s | `-123.0 dBm` |
| `SF8` | `2.048` | `0` | **`113.15` ms** | `11.20` s | `-126.0 dBm` |
| `SF9` | `4.096` | `0` | **`205.82` ms** | `20.38` s | `-129.0 dBm` |
| `SF10` | `8.192` | `0` | **`370.69` ms** | `36.70` s | `-132.0 dBm` |
| `SF11` | `16.384` | `1` | **`823.30` ms** | `81.51` s | `-134.5 dBm` |
| `SF12` | `32.768` | `1` | **`1482.75` ms** | `146.79` s | `-137.0 dBm` |

Terlihat bahwa satu paket `24 byte` pada `SF12` menghabiskan **`1,48 detik`** di udara—hampir **24 kali lebih lama** dibanding `SF7` (`61,7 ms`)! Pada simulasi *link budget* ruang bebas jarak $3{,}0\text{ km}$ ($923\text{ MHz}$ sebagai titik uji model FSPL, $\text{FSPL} = 101{,}29\text{ dB}$, *shadow margin* $15\text{ dB}$, $P_{\text{tx}}=14\text{ dBm}$, $G_{\text{tx}}+G_{\text{rx}}-L_{\text{kabel}}=3{,}5\text{ dB}$), daya terima terhitung $P_{\text{rx}} = -98{,}79\text{ dBm}$, memberi *margin* positif $+24{,}21\text{ dB}$ bahkan di `SF7` (sehingga ADR akan menurunkan `SF` agar hemat baterai dan tidak menyumbat spektrum).

## Latihan

Latihan konseptual, kalkulasi `ToA`, studi *link budget*, dan analisis arsitektur tersedia pada tab **[Exercises](chapter-18#exercises)**.

## Tugas

Rancang arsitektur jaringan LoRaWAN untuk sistem pemantauan iklim mikro kampus/lahan pertanian lengkap dengan analisis `ToA`, pemilihan `SF`, OTAA/ADR, dan daftar periksa verifikasi regulasi regional pada tab **[Tugas & Rubrik](chapter-18#assignment)** (total 100 poin).

## Ringkasan

- **LoRa** adalah modulasi fisik **CSS** (*Chirp Spread Spectrum*) dengan parameter `SF`, `BW`, dan `CR`; **LoRaWAN** adalah protokol MAC/jaringan (*Star-of-Stars*, *OTAA*, *ADR*, *Class A/B/C*, enkripsi `NwkSKey`/`AppSKey`).
- Menaikkan `SF` memperluas jangkauan dan sensitivitas penerima, tetapi memanjangkan *Time-on-Air* secara eksponensial (`61,7 ms` di `SF7` vs `1482,75 ms` di `SF12` untuk payload `24 B`), sehingga menguras baterai dan kapasitas kanal.
- Mengirim JSON teks mentah di atas LoRa sangat tidak efisien; gunakan **payload biner padat** ($10\text{–}25\text{ byte}$) dan aktifkan **ADR** pada node stasioner.
- Parameter spektrum (pita frekuensi, batas EIRP, *duty cycle*/*dwell time*) **wajib diverifikasi** langsung terhadap **LoRa Alliance RP2** dan regulator nasional sebelum deployment fisik.

## Referensi

1. LoRa Alliance, *LoRaWAN Specification & Regional Parameters (RP2)*, [https://lora-alliance.org/about-lorawan/](https://lora-alliance.org/about-lorawan/).
2. Semtech Corporation, *AN1200.13: LoRa Modem Designer's Guide & SX1276/77/78/79 Datasheet*, [https://www.semtech.com/products/wireless-rf/lora-connect](https://www.semtech.com/products/wireless-rf/lora-connect).
3. The Things Network / The Things Industries, *LoRaWAN Architecture, Security (OTAA/ABP) & ADR Fundamentals*, [https://www.thethingsnetwork.org/docs/lorawan/](https://www.thethingsnetwork.org/docs/lorawan/).


# Chapter 31: Low-Power Design, Sleep Modes & Energy Measurement

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami arsitektur power domain pada mikrokontroler modern (active, idle, light sleep, dan deep sleep).
2. Mengonfigurasi berbagai sumber pembangkit (*wake-up sources*) pada ESP32 seperti timer RTC dan GPIO external interrupt.
3. Menghitung profil konsumsi arus rata-rata ($I_{avg}$), *charge budget*, dan estimasi masa pakai baterai riil dengan faktor *derating* serta *self-discharge*.
4. Mengimplementasikan teknik *duty cycling* sensor dan *peripheral power gating* menggunakan MOSFET switch.
5. Menganalisis *trade-off* kritis antara latensi respon telemetri terhadap penghematan energi sistem tertanam.

## Prasyarat

- Pemahaman arsitektur mikrokontroler dan GPIO (Chapter 04–06).
- Penguasaan hukum dasar kelistrikan (Ohm, Kirchhoff) serta konsep muatan listrik Coulomb ($Q = I \times t$).
- Kemampuan dasar pemrograman Python dan C/C++ pada ESP32 Arduino Core.

## Konsep dan teori

### 1. Taksonomi Mode Daya Mikrokontroler

Perangkat IoT bertenaga baterai (seperti node pemantau lingkungan atau pertanian presisi) menghabiskan lebih dari 95% masa pakainya dalam keadaan diam (*idle*). Pada mikrokontroler ESP32, terdapat empat domain daya utama:

1. **Active Mode**: CPU aktif penuh (80–240 MHz), Wi-Fi/Bluetooth beroperasi penuh, periferal menyala. Arus rata-rata berada pada rentang 80–240 mA.
2. **Modem-sleep Mode**: CPU tetap bekerja, namun radio Wi-Fi dan Bluetooth dimatikan. Arus berkisar antara 20–30 mA.
3. **Light-sleep Mode**: Clock CPU dihentikan sementara (*gated*), memori internal dan periferal digital dipertahankan. Waktu bangun (*wake-up latency*) sangat cepat (< 1 ms), dengan konsumsi arus sekitar 0.8–2 mA.
4. **Deep-sleep Mode**: Seluruh domain CPU utama, memori SRAM standar, dan sebagian besar periferal dimatikan total. Hanya RTC domain (RTC Slow Memory, RTC Fast Memory, ULP co-processor, dan RTC timer) yang tetap dialiri daya. Konsumsi arus turun drastis hingga rentang 5–15 $\mu$A.

```
+----------------------------------------------------------------+
|                        ESP32 Power Domains                     |
|                                                                |
|  [Main Domain - Power Gated in Deep Sleep]                     |
|   +-----------------------+    +----------------------------+  |
|   | Dual-Core Tensilica   |    | Radio (Wi-Fi / BLE)        |  |
|   | 240 MHz CPU           |    | Baseband & RF Synth        |  |
|   +-----------------------+    +----------------------------+  |
|   +-----------------------+    +----------------------------+  |
|   | Standard SRAM         |    | High-Speed Peripherals     |  |
|   | (520 KB)              |    | (SPI, I2C, UART)           |  |
|   +-----------------------+    +----------------------------+  |
|                                                                |
|  [RTC Domain - Always Powered in Deep Sleep]                   |
|   +-----------------------+    +----------------------------+  |
|   | RTC Fast/Slow SRAM    |    | ULP Co-processor           |  |
|   | (8 KB + 8 KB)         |    | (Ultra Low Power FSM/RISC) |  |
|   +-----------------------+    +----------------------------+  |
|   +-----------------------+    +----------------------------+  |
|   | RTC Controller        |    | RTC Timers & EXT IO        |  |
|   | & Regulators          |    | (Wake-up pin triggers)     |  |
|   +-----------------------+    +----------------------------+  |
+----------------------------------------------------------------+
```

### 2. Formulasi Matematis Arus Rata-Rata dan Energi

Siklus operasi berkala didefinisikan oleh waktu aktif ($T_{active}$) dan waktu tidur ($T_{sleep}$). Periode total siklus adalah:

$$T_{cycle} = T_{active} + T_{sleep}$$

Muatan listrik yang dikonsumsi per siklus ($Q_{cycle}$) dalam satuan miliampere-detik (mA·s) adalah:

$$Q_{cycle} = (I_{active} \times T_{active}) + (I_{sleep} \times T_{sleep})$$

Arus rata-rata sistem ($I_{avg}$) dihitung sebagai:

$$I_{avg} = \frac{Q_{cycle}}{T_{cycle}} = \frac{I_{active} \cdot T_{active} + I_{sleep} \cdot T_{sleep}}{T_{active} + T_{sleep}}$$

Sebagai contoh, jika $I_{active} = 120\text{ mA}$, $T_{active} = 1.5\text{ s}$, $I_{sleep} = 0.010\text{ mA}$ ($10\ \mu\text{A}$), dan $T_{sleep} = 598.5\text{ s}$ ($T_{cycle} = 600\text{ s}$ atau 10 menit):

$$Q_{cycle} = (120 \times 1.5) + (0.010 \times 598.5) = 180 + 5.985 = 185.985\text{ mA}\cdot\text{s}$$

$$I_{avg} = \frac{185.985}{600} \approx 0.310\text{ mA}$$

### 3. Estimasi Masa Pakai Baterai Riil

Kapasitas nominal baterai ($C_{nominal}$ dalam mAh) tidak dapat dikuras 100% karena adanya *cutoff voltage* rangkaian regulator (LDO) dan degradasi temperatur. Faktor *derating* ($\eta$) yang realistis berkisar antara 0.80–0.85. Selain itu, baterai kimia (seperti Li-SOCl2 atau Li-Ion) mengalami arus bocor internal (*self-discharge rate* $S_d \approx 1\text{--}3\%$ per tahun).

Masa pakai nominal (dalam jam):

$$L_{hours} = \frac{C_{nominal} \times \eta}{I_{avg}}$$

Dengan baterai 2500 mAh dan $\eta = 0.85$ ($C_{usable} = 2125\text{ mAh}$):

$$L_{hours} = \frac{2125}{0.310} \approx 6854.8\text{ jam} \approx 285.6\text{ hari}$$

Jika interval diperpanjang menjadi 30 menit ($T_{cycle} = 1800\text{ s}$) dan daya sensor diputus menggunakan MOSFET gating sehingga $I_{sleep} = 5\ \mu\text{A}$ dan $T_{active} = 0.5\text{ s}$ ($I_{active} = 80\text{ mA}$):

$$I_{avg} = \frac{(80 \times 0.5) + (0.005 \times 1799.5)}{1800} = \frac{40 + 8.9975}{1800} \approx 0.0272\text{ mA}$$

$$L_{hours} = \frac{2125}{0.0272} \approx 78125\text{ jam} \approx 3255\text{ hari} \approx 8.9\text{ tahun}$$

### 4. Teknik Peripheral Power Gating

Sensor analog atau digital (seperti sensor gas, akselerometer, atau probe tanah) sering kali tetap mengonsumsi arus statis 100 $\mu$A hingga beberapa mA meskipun mikrokontroler sudah tertidur lelap jika jalur $V_{DD}$ sensor terhubung langsung ke rel suplai daya.

Solusi standar industri adalah menggunakan **High-Side Switch** berbasis P-Channel MOSFET atau chip *load switch* terintegrasi. Pin GPIO mikrokontroler mengendalikan gerbang (*gate*) MOSFET. Saat mikrokontroler tidur, GPIO berada pada status *high-impedance* atau ditarik tinggi sehingga saklar memutus suplai tegangan ke sensor sepenuhnya.

## Latihan

1. **Analisis Matematis**: Hitung masa pakai baterai nominal 1200 mAh (derating 0.80) jika perangkat aktif selama 2 detik dengan arus 150 mA setiap 5 menit (300 detik), dan arus sleep sebesar 15 $\mu$A.
2. **Konfigurasi Wake-up**: Modifikasi sketsa ESP32 agar dapat bangun baik karena alarm timer (setiap 60 detik) maupun pemicu tombol darurat pada pin GPIO 33 menggunakan `esp_sleep_enable_ext0_wakeup()`.
3. **Optimasi Boot**: Mengapa penyimpanan variabel state pada `RTC_DATA_ATTR` lebih hemat energi dibandingkan menyimpannya pada flash SPI (EEPROM/NVS) saat perangkat bangun berulang kali?

## Tugas

Implementasikan skrip simulasi profil konsumsi daya komprehensif pada Python (`power_model_sim.py`) dan kode firmware ESP32 Arduino (`esp32_low_power_firmware.ino`). Lakukan pengujian terhadap tiga variasi beban kerja operasional serta simulasikan dampak *self-discharge* baterai terhadap masa pakai tahunan. Laporkan hasil perhitungan dalam dokumen teknis terstruktur.

## Ringkasan

1. Mode daya pada mikrokontroler modern memisahkan domain daya berkecepatan tinggi dengan subsistem *Real-Time Clock* (RTC) berdaya mikroampere.
2. Formulasi muatan listrik $Q = \int I(t)\,dt$ adalah dasar utama perhitungan profil energi perangkat IoT.
3. *Duty cycling* agresif dan *peripheral power gating* menggunakan MOSFET terbukti mampu meningkatkan masa pakai baterai dari hitungan minggu menjadi beberapa tahun.

## Referensi

1. Espressif Systems. *ESP32 Technical Reference Manual: Low-Power Management and RTC Controller*. Espressif Inc., 2024.
2. Texas Instruments. *Calculating Battery Life for IoT Devices*. Application Report SLVA877, 2023.
3. IEEE Communications Surveys & Tutorials. *Energy Harvesting and Low-Power Techniques for IoT Sensor Nodes*. Vol. 24, No. 3, 2022.

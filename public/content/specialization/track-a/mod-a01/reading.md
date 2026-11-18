# Modul A01 — Smart Building Architecture, Zoning & Multi-Protocol Coexistence

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menyusun pemodelan hierarki zonasi fisik dan logis sistem otomasi bangunan bertingkat.
2. Menganalisis interferensi kanal silang nirkabel antara kanal Wi-Fi (1, 6, 11) dan kanal 802.15.4 (11 hingga 26).
3. Menghitung rasio Carrier-to-Interference (CIR) untuk memastikan batas margin penerimaan paket nirkabel aman.
4. Merancang segmentasi jaringan VLAN 802.1Q untuk mengisolasi lalu lintas kendali lokal dari jaringan publik.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 01, Chapter 02, Chapter 11.
- Modul Jalur Peminatan Prasyarat: Tidak ada (modul awal jalur peminatan).
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Arsitektur Otomasi Gedung Cerdas (BACnet & Purdue Enterprise)
Sistem otomasi gedung komersial (*Building Management System* / BMS) dirancang mengikuti hierarki kontrol ruang fisik dan logis yang teratur:
- **Level 1 (Field Device & Sensing)**: Sensor okupansi, transduser kualitas udara IAQ, aktuator katup pendingin VAV, dan sakelar cerdas di setiap ruangan (*Room Level*).
- **Level 2 (Zone / Floor Controller)**: Pengontrol tepi lokal berbasis mikrokontroler (Direct Digital Control / DDC) yang mengelola logika kenyamanan termal per zona tanpa ketergantungan pada server utama.
- **Level 3 (Facility Management & SCADA BMS)**: Server pengawas terpusat yang menjalankan protokol standar industri BACnet over IP (ANSI/ASHRAE Standard 135) untuk penjadwalan terpadu, pemantauan konsumsi daya listrik, dan alarm gedung.

### 2. Koeksistensi Spektrum Nirkabel 2.4 GHz
Pita frekuensi Industrial, Scientific, and Medical (ISM) $2{,}4\text{ GHz}$ menampung berbagai teknologi nirkabel yang beroperasi secara simultan di dalam gedung:
1. **Wi-Fi (IEEE 802.11ax/ac)**: Lebar pita kanal $20\text{ MHz}$ atau $40\text{ MHz}$, daya pancar tinggi ($+20\text{ dBm}$), transmisi data burst berkecepatan ratusan Mbps.
2. **Thread / Zigbee (IEEE 802.15.4)**: Lebar pita kanal sempit $2\text{ MHz}$ ($5\text{ MHz}$ spacing), daya pancar rendah ($0 - +10\text{ dBm}$), transmisi data kontrol telemetri singkat berlatensi deterministik.
3. **Bluetooth Low Energy (BLE 5.x)**: 40 kanal dengan jarak $2\text{ MHz}$, termasuk 3 kanal iklan utama (37, 38, 39) yang sering digunakan untuk suar lokasi (*beacons*).

Ketika pemancar Wi-Fi mentransmisikan paket berdaya tinggi di Kanal 1, 6, atau 11, emisi spektral luar-pita (*spectral regrowth*) dapat menenggelamkan sinyal IEEE 802.15.4 di kanal-kanal yang berdekatan.

### 3. Rasio Carrier-to-Interference (CIR) & Pemilihan Kanal Bersih
Untuk menjamin komunikasi kontrol Thread/Zigbee bebas gangguan (Packet Error Rate $\le 1\%$), rasio sinyal pembawa yang diinginkan terhadap interferensi akumulatif wajib memenuhi ambang batas aman:
$$
\text{CIR}_{\text{dB}} = P_{\text{desired}} - 10 \log_{10} \left( \sum_{k=1}^{M} 10^{P_{\text{int},k}/10} \right) \ge +3\text{ dB}
$$
Strategi alokasi kanal industri merekomendasikan penempatan kanal Thread pada Kanal 15, 20, 25, atau 26 (di mana Kanal 25 dan 26 berada di luar batas spektrum Wi-Fi Kanal 11 di sebagian besar regulasi regional).

### 4. Landasan Matematis: Masking Spektral Wi-Fi & Kalkulasi CIR

1. **Model Masking Spektrum Emisi Wi-Fi**:
   Daya interferensi efektif ($P_{\text{int}}$) yang diterima pada kanal 802.15.4 berjarak $\Delta f$ dari frekuensi tengah Wi-Fi:
   $$
   P_{\text{int}}(\text{dBm}) = P_{\text{Tx,WiFi}} - L_{\text{path}}(\text{dB}) + A_{\text{mask}}(\Delta f)
   $$
   di mana $A_{\text{mask}}$ adalah atenuasi kurva spektral filter emisi Wi-Fi (dB).

2. **Worked Numerical Example (Contoh Perhitungan Rinci)**:
   - **Kondisi Pengujian**:
     - Daya terima sinyal Thread yang diinginkan: $P_{\text{desired}} = -72{,}0\text{ dBm}$
     - Daya pancar Access Point Wi-Fi Kanal 6 ($2437\text{ MHz}$): $P_{\text{Tx,WiFi}} = +20{,}0\text{ dBm}$
     - Redaman lintasan jarak fisik pemisah $5\text{ meter}$: $L_{\text{path}} = 35{,}0\text{ dB}$
   - **Kasus A: Kanal 802.15.4 Kanal 15 ($2425\text{ MHz}$)**:
     - Jarak frekuensi: $|2425 - 2437| = 12\text{ MHz}$ (berada di lereng spektral Wi-Fi, $A_{\text{mask}} = -24{,}0\text{ dB}$)
     - Daya interferensi efektif:
       $$
       P_{\text{int}} = 20{,}0 - 35{,}0 + (-24{,}0) = -39{,}0\text{ dBm}
       $$
     - Perhitungan Rasio CIR:
       $$
       \text{CIR} = -72{,}0 - (-39{,}0) = -33{,}0\text{ dB} \ll +3{,}0\text{ dB}
       $$
       *Kesimpulan*: Terjadi interferensi destruktif masif; paket Thread Kanal 15 akan mengalami tabrakan data (*collision*) konstan saat ada transfer video Wi-Fi.
   - **Kasus B: Kanal 802.15.4 Kanal 26 ($2480\text{ MHz}$)**:
     - Jarak frekuensi: $|2480 - 2437| = 43\text{ MHz}$ (berada jauh di luar pita Wi-Fi Ch 6, $A_{\text{mask}} = -48{,}0\text{ dB}$)
     - Daya interferensi efektif:
       $$
       P_{\text{int}} = 20{,}0 - 35{,}0 + (-48{,}0) = -63{,}0\text{ dBm}
       $$
     - Perhitungan Rasio CIR:
       $$
       \text{CIR} = -72{,}0 - (-63{,}0) = -9{,}0\text{ dB}
       $$
       Meskipun membaik $24\text{ dB}$, jika jarak fisik didekatkan ke $10\text{ meter}$ ($L_{\text{path}} = 45\text{ dB}$), $\text{CIR} = +1{,}0\text{ dB}$, dan pada Kanal 25 dengan Wi-Fi Kanal 1 yang aktif, Kanal 25/26 menjadi sangat aman ($> +15\text{ dB}$).

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa kanal IEEE 802.15.4 Kanal 26 sering disebut sebagai kanal nirkabel paling aman dari interferensi Wi-Fi di gedung komersial?**
   - *Jawaban*: Frekuensi tengah Kanal 26 berada pada $2480	ext{ MHz}$, berada di luar batas spektrum emisi tertinggi Wi-Fi pita $2{,}4	ext{ GHz}$ Kanal 11 ($2473	ext{ MHz}$) maupun Kanal 13, sehingga atenuasi masking spektral luar-pita bernilai maksimum ($> 45	ext{ dB}$ redaman tambahan).

2. **Apa risiko operasional utama jika sistem otomasi kontrol zona ruangan bergantung sepenuhnya pada server cloud publik?**
   - *Jawaban*: Jika koneksi kabel serat optik atau penyedia layanan internet (ISP) gedung mengalami gangguan sesaat (*WAN outage*), kontroler lokal kehilangan perintah setpoint suhu, sensor kehadiran gagal menyalakan lampu darurat, dan katup pendingin dapat mengalami kegagalan kendali yang menimbulkan lonjakan tagihan energi atau ketidaknyamanan termal parah.

## Tugas

## Penugasan Mandiri: Pemetaan Spektrum Koeksistensi & Rancangan VLAN Gedung

Susun dokumen teknis yang memetakan kanal nirkabel Wi-Fi (Kanal 1, 6, 11) dan Thread (Kanal 15, 20, 25) pada denah gedung 3 lantai. Sertakan konfigurasi tabel VLAN 802.1Q pada switch managed untuk mengisolasi subnet kontrol BACnet.

## Ringkasan
- Modul A01 memberikan pemahaman mendalam dan terapan mengenai Smart Building Architecture, Zoning & Multi-Protocol Coexistence pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [building_coexistence_cir_sim.py](src/building_coexistence_cir_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. ANSI/ASHRAE Standard 135-2020, BACnet — A Data Communication Protocol for Building Automation and Control Networks, [https://www.ashrae.org/technical-resources/standards-and-guidelines/read-only-versions-of-ashrae-standards](https://www.ashrae.org/technical-resources/standards-and-guidelines/read-only-versions-of-ashrae-standards) (diperiksa 2026-11-18).
2. IEEE Std 802.15.4-2020, IEEE Standard for Low-Rate Wireless Networks, [https://standards.ieee.org/ieee/802.15.4/7029/](https://standards.ieee.org/ieee/802.15.4/7029/) (diperiksa 2026-11-18).

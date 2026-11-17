# Chapter 34: Interoperability, Matter & Thread Fundamentals

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami masalah fragmentasi ekosistem IoT (*walled gardens*) dan pentingnya standar interoperabilitas terpadu.
2. Menganalisis arsitektur protokol jaringan nirkabel **Thread**: lapisan fisik IEEE 802.15.4, adaptasi IPv6 melalui 6LoWPAN, dan routing mesh *self-healing*.
3. Mengidentifikasi peran elemen jaringan Thread: *Thread Leader*, *Thread Router*, *End Devices*, dan *Thread Border Router*.
4. Memahami lapisan aplikasi **Matter (Project CHIP)**, model data (*Clusters, Endpoints, Attributes*), dan konsep *Multi-Admin/Multi-Fabric*.
5. Menjelaskan siklus hidup commissioning Matter: *Password-Authenticated Session Establishment* (PASE menggunakan SPAKE2+) dan *Certificate-Authenticated Session Establishment* (CASE).

## Prasyarat

- Pemahaman model referensi OSI dan arsitektur pengalamatan IPv6 (Chapter 11 & 12).
- Konsep dasar kriptografi asimetris, sertifikat X.509, dan pertukaran kunci Diffie-Hellman (Chapter 28).
- Dasar-dasar komunikasi radio mesh nirkabel (Chapter 17).

## Konsep dan teori

### 1. Masalah Fragmentasi Ekosistem IoT

Selama lebih dari satu dekade, industri rumah pintar (*smart home*) terfragmentasi ke dalam pulau-pulau protokol tertutup: Zigbee, Z-Wave, Bluetooth Mesh, serta ekosistem proprietary (Apple HomeKit, Google Home, Amazon Alexa, Tuya). Konsumen terpaksa menggunakan beberapa aplikasi pengendali dan *bridge* perangkat keras terpisah.

**Matter** (dikembangkan oleh Connectivity Standards Alliance / CSA) hadir sebagai lapisan aplikasi terbuka (*application layer*) yang terpadu di atas protokol transport berbasis IP standar (Wi-Fi, Ethernet, dan Thread).

```
+-------------------------------------------------------------+
|                Matter Application Layer                     |
|       (Data Model, Device Types, Clusters, Security)        |
+-------------------------------------------------------------+
|                         IPv6                                |
+-------------------------------+-----------------------------+
|         Wi-Fi / Ethernet      |      Thread (802.15.4)      |
|    (Bandwidth Tinggi, Listrik)|    (Mesh, Baterai, 6LoWPAN) |
+-------------------------------+-----------------------------+
```

### 2. Arsitektur Jaringan Thread

Thread adalah protokol jaringan mesh nirkabel berdaya rendah berbasis standar terbuka:
- **Lapisan Fisik & MAC**: IEEE 802.15.4 beroperasi pada pita frekuensi 2.4 GHz global dengan kecepatan data 250 kbps.
- **Lapisan Jaringan**: Native IPv6 murni tanpa perlu translasi NAT di dalam jaringan lokal.
- **Lapisan Adaptasi**: **6LoWPAN** (*IPv6 over Low-Power Wireless Personal Area Networks*) mengompresi header IPv6 standar (40 byte) menjadi beberapa byte saja agar muat dalam MTU 802.15.4 (127 byte).
- **Self-Healing Mesh**: Tidak ada *Single Point of Failure*. Jika node *Leader* mati, para *Router* secara otonom menyelenggarakan pemungutan suara (*election*) untuk memilih Leader baru dalam hitungan detik.

#### Hirarki Peran Node Thread:
1. **Thread Leader**: Mengelola alokasi alamat RLOC16 (*Routing Locator*) dan mengkoordinasikan tabel konfigurasi jaringan.
2. **Thread Router**: Node bertenaga listrik konstan yang meneruskan paket data antar-node (*packet forwarding*).
3. **End Device / Sleepy End Device (SED)**: Node bertenaga baterai yang tidur secara periodik dan hanya berkomunikasi melalui satu router induk (*parent*).
4. **Thread Border Router (OTBR)**: Jembatan transparan yang menghubungkan jaringan mesh Thread (802.15.4) dengan jaringan Wi-Fi/Ethernet rumah Anda.

### 3. Model Data Matter

Matter mengorganisasi perangkat pintar menggunakan hierarki berorientasi objek:
- **Node**: Perangkat fisik yang memiliki alamat IP tunggal di dalam jaringan.
- **Endpoint**: Titik fungsi mandiri di dalam node (misalnya Stopkontak Ganda memiliki Endpoint 1 dan Endpoint 2).
- **Cluster**: Kumpulan atribut (*Attributes*), perintah (*Commands*), dan peristiwa (*Events*) standar (contoh: *On/Off Cluster*, *Level Control Cluster*).

### 4. Protokol Keamanan & Commissioning Matter

Setiap perangkat Matter dilengkapi dengan kode QR atau PIN penyiapan (*Setup PIN Code*) unik dari pabrikan:
1. **PASE (Password-Authenticated Session Establishment)**: Menggunakan algoritma kriptografi pertukaran kunci berbasis password **SPAKE2+**. Pengguna memasukkan PIN penyiapan untuk membentuk saluran terenkripsi pertama kali tanpa pernah mengirimkan password mentah melintasi udara.
2. **Penerbitan Kredensial Fabric**: Komisioner menerbitkan *Node Operational Certificate* (NOC) yang ditandatangani oleh *Root of Trust* ekosistem (*Fabric CA*).
3. **CASE (Certificate-Authenticated Session Establishment)**: Setelah perangkat bergabung ke dalam Fabric, komunikasi operasional antar-perangkat Matter diautentikasi timbal-balik (*mutual TLS-like*) menggunakan sertifikat digital NOC tersebut.
4. **Multi-Admin Support**: Satu bola lampu pintar Matter dapat dikendalikan secara bersamaan oleh Apple Home, Google Home, dan Home Assistant melalui Fabric terpisah tanpa konflik perintah.

## Latihan

1. **Analisis Kompresi 6LoWPAN**: Mengapa header IPv6 standar (40 byte) dan header UDP (8 byte) tidak efisien jika ditransmisikan langsung pada frame IEEE 802.15.4? Jelaskan bagaimana mekanisme *stateless header compression* pada 6LoWPAN mengatasi batasan panjang paket (MTU 127 byte) tersebut.
2. **Mekanisme Failover Thread Leader**: Jelaskan apa yang terjadi pada topologi Thread mesh apabila node *Thread Leader* mendadak kehilangan daya listrik. Bagaimana cara router tetangga mendeteksi ketiadaan sinyal *keep-alive* dan memilih pemimpin baru?
3. **Diferensiasi PASE vs CASE**: Dalam arsitektur keamanan Matter, kapan fase PASE berakhir dan fase CASE dimulai? Mengapa PIN setup pabrikan tidak lagi digunakan setelah proses *commissioning* selesai?

## Tugas

Kembangkan modul simulasi Python (`matter_thread_sim.py`) yang memverifikasi:
1. Routing multihop pada topologi mesh Thread dari node *Sleepy End Device* melintasi *Router* dan *Leader* menuju *Border Router*.
2. Alur *Matter Commissioning* yang mengautentikasi *Setup PIN Code* via mekanisme PASE dan menerbitkan parameter *Node Operational Certificate (NOC)* ke dalam *Fabric*.

## Ringkasan

1. Matter dan Thread memecahkan perang protokol rumah pintar dengan menyatukan lapisan aplikasi terbuka di atas pondasi native IPv6.
2. Thread menghadirkan jaringan mesh nirkabel yang tangguh, hemat daya, dan bebas titik kegagalan tunggal berkat peran *Thread Border Router*.
3. Arsitektur keamanan Matter menjamin privasi lokal total melalui algoritma SPAKE2+ (PASE), sertifikat operasional digital (CASE), dan dukungan *Multi-Fabric*.

## Referensi

1. Connectivity Standards Alliance (CSA). *Matter Core Specification Version 1.3*. 2024.
2. Thread Group. *Thread 1.3.0 Specification: Enhancing Matter Connectivity and IP Interoperability*. 2023.
3. Shelby, Z., & Bormann, C. *6LoWPAN: The Wireless Embedded Internet*. John Wiley & Sons, 2021.

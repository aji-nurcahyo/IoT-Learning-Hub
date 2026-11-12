# Chapter 11 — Networking Fundamentals for IoT

## Overview

Pada Level 1, seluruh pemrosesan dan kontrol terjadi secara lokal di atas meja praktikum. Memasuki **Level 2 — Connectivity & Communication Protocols**, perangkat terhubung (*connected devices*) mulai bertukar *telemetry* dan perintah melewati jaringan lokal maupun internet. Agar mampu mendiagnosis kegagalan koneksi ESP32 ke *MQTT Broker* atau API server, seorang insinyur IoT wajib menguasai arsitektur **TCP/IP stack**, pengalamatan IP dan *subnetting*, peran **DHCP** dan **DNS**, perbedaan mendasar **TCP vs UDP**, konsep **ports** dan **sockets**, serta metrik performa jaringan (*latency*, *bandwidth*, *throughput*, *goodput*, dan *packet loss*).

## Prasyarat

- Menyelesaikan [Chapter 01](#/chapter/1) (komponen ekosistem IoT) dan [Chapter 10](#/chapter/10) (Capstone Level 1).
- Pemahaman dasar aritmatika biner ($2^n$) dan pengoperasian terminal/command prompt.

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Menjelaskan** fungsi setiap lapisan pada **TCP/IP 4-layer stack** beserta alur enkapsulasi paket *telemetry* IoT.
2. **Menghitung** *network address*, *broadcast address*, *subnet mask*, dan rentang *host usable* dari notasi IPv4 CIDR serta membedakan fungsi **DHCP** dan **DNS**.
3. **Membandingkan** karakteristik **TCP vs UDP**, peran *port* & *socket*, serta menghitung dampak *header overhead* terhadap *goodput*.
4. **Mendiagnosis** kegagalan konektivitas lokal menggunakan metrik *latency* (RTT), *jitter*, *throughput*, *packet loss*, dan utilitas jaringan dasar (`ping`, `nslookup`, `tracert`).

## Konsep dan teori

### 1. TCP/IP Stack & Enkapsulasi Paket IoT

Model praktis jaringan internet menggunakan **TCP/IP 4-Layer Stack** (sering dipetakan ke 7 lapis model referensi OSI):

| Lapisan TCP/IP | Peran Utama | Contoh Protokol / Elemen IoT |
| --- | --- | --- |
| **4. Application** | Format pesan & semantik pertukaran data | `MQTT`, `HTTP/REST`, `CoAP`, `DNS`, `NTP` |
| **3. Transport** | Multiplexing proses (*port*) & keandalan ujung-ke-ujung | `TCP` (andal, berurut), `UDP` (ringan, tanpa koneksi) |
| **2. Internet** | Pengalamatan logis lintas jaringan & *routing* | `IPv4` (32-bit), `IPv6` (128-bit), `ICMP` (`ping`) |
| **1. Link / Physical** | Transmisi *frame* di media fisik / radio lokal | `Wi-Fi (802.11)`, `Ethernet (802.3)`, `PPP` |

Ketika ESP32 mengirim payload JSON $48\text{ byte}$, setiap lapisan membungkusnya dengan *header* (*encapsulation*): `TCP (20 B)` $\rightarrow$ `IPv4 (20 B)` $\rightarrow$ `Link/MAC (~18 B)`. Akibatnya, ukuran paket di kabel/udara membengkak menjadi $106\text{ byte}$ sebelum sinyal dikirim!

![Model TCP/IP 4 lapis, perbandingan TCP vs UDP, dan alur DHCP/DNS/Socket](content/chapter-11/diagram.svg)

### 2. IPv4 Addressing, Subnetting (CIDR), DHCP, dan DNS

- **Alamat IPv4 & Ruang Privat (RFC 1918)**: Alamat IPv4 sepanjang 32 bit (4 oktet desimal, misal `192.168.50.37`). Jaringan IoT lokal umumnya memakai blok privat **RFC 1918**: `10.0.0.0/8`, `172.16.0.0/12`, atau `192.168.0.0/16` (tidak langsung dirutekan di internet publik tanpa NAT).
- **Subnetting & Notasi CIDR**: Notasi `/n` menyatakan jumlah bit *network prefix* dari 32 bit. Sisa bit host $h = 32 - n$ menentukan jumlah alamat usable:
  $$N_{\text{usable}} = 2^{(32 - n)} - 2$$
  (dikurangi 2 untuk alamat *network* paling awal dan alamat *broadcast* paling akhir).
  Jika dua perangkat berada pada *subnet* yang berbeda, paket wajib melewati **Default Gateway** (*router*). Salah mengisi *subnet mask* menyebabkan node gagal menemukan *Gateway* atau *Broker* lokal meski sinyal Wi-Fi penuh!
- **DHCP (*Dynamic Host Configuration Protocol*, UDP 67/68)**: Memberikan konfigurasi otomatis (*IP address*, *subnet mask*, *default gateway*, dan *DNS server*) kepada node IoT dengan masa sewa (*lease time*).
- **DNS (*Domain Name System*, UDP/TCP 53)**: Menerjemahkan nama host manusiawi (misal `broker.kampus.local`) menjadi alamat IP numerik. Jika DNS gagal, ESP32 tetap bisa terhubung ke IP mentah, tetapi gagal menyambung ke domain!

### 3. TCP vs UDP, Ports, dan Sockets

- **Port (16-bit: `0..65535`)**: Mengidentifikasi layanan tujuan di satu host (misal `1883` MQTT, `8883` MQTTS, `80` HTTP, `443` HTTPS, `53` DNS, `123` NTP).
- **Socket**: Pasangan alamat IP dan nomor port (`192.168.10.50:1883`) yang menjadi titik akhir komunikasi dua arah.

| Parameter | TCP (*Transmission Control Protocol*) | UDP (*User Datagram Protocol*) |
| --- | --- | --- |
| **Pendirian koneksi** | Wajib **3-way handshake** (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`) | Tanpa handshake (*connectionless*) |
| **Header minimum** | **20 byte** | **8 byte** |
| **Jaminan pengiriman** | Retransmisi otomatis, urutan paket terjaga, *flow control* | *Best-effort*; paket bisa hilang atau tertukar urutan |
| **Penggunaan di IoT** | `MQTT`, `HTTP/HTTPS` (butuh integritas) | `DHCP`, `DNS`, `NTP`, `CoAP` (payload kecil, hemat daya) |

### 4. Latency, Bandwidth, Throughput, Goodput, dan Packet Loss

Insinyur jaringan membedakan lima metrik ini secara ketat:
1. **Bandwidth**: Kapasitas teoretis maksimum kanal (bps, Mbps).
2. **Throughput**: Laju transfer data aktual yang melewati jalur (termasuk *header* dan *retransmission*).
3. **Goodput**: Laju data **berguna** (*application payload*) yang benar-benar sampai ke aplikasi tujuan:
   $$\text{Efisiensi Goodput} = \frac{B_{\text{payload}}}{B_{\text{payload}} + B_{\text{headers}}} \times 100\%$$
4. **Latency (RTT)**: Waktu tempuh paket bolak-balik (*Round-Trip Time*), tersusun dari *propagation delay*, *transmission/serialization delay*, *queuing delay*, dan *processing delay*. Variasi antar-RTT disebut **jitter**.
5. **Packet Loss**: Persentase paket yang gagal mencapai tujuan akibat kemacetan antrean, interferensi RF, atau *timeout*.

### 5. Worked Example (`network_diagnostics_sim.py`)

Hasil eksekusi nyata skrip [`network_diagnostics_sim.py`](content/chapter-11/src/network_diagnostics_sim.py) (`outputs.md`):

1. **Subnetting `192.168.50.37/26`**:
   - Karena `/26` menyisakan $32 - 26 = 6$ bit host, ukuran blok = $2^6 = 64$.
   - *Network Address*: `192.168.50.0`, *Broadcast*: `192.168.50.63`, *Netmask*: `255.255.255.192`.
   - *Host Usable*: `192.168.50.1 .. 192.168.50.62` ($64 - 2 = 62$ host).
2. **Perbandingan Goodput untuk Payload $48\text{ B}$** (dengan MAC/link overhead $18\text{ B}$):
   - **TCP/IPv4** ($48 + 20 + 20 + 18 = 106\text{ B}$): *goodput* hanya **$45{,}3\%$**!
   - **UDP/IPv4** ($48 + 8 + 20 + 18 = 94\text{ B}$): *goodput* naik ke **$51{,}1\%$**, dan tanpa *overhead* handshake 3-arah.
3. **Analisis Probe Sintetis ([`telemetry.csv`](content/chapter-11/telemetry.csv))**:
   - Dari 10 probe (`ICMP` ke gateway & `TCP_1883` ke broker), 1 paket hilang (**10,0% packet loss**), RTT min/avg/max = $2{,}4 / 6{,}57 / 18{,}6\text{ ms}$, dan *jitter* (simpangan baku) = $5{,}16\text{ ms}$.

### 6. Alur Troubleshooting Konektivitas IoT Berlapis (Bottom-Up)

Saat ESP32 gagal mengirim data ke server, periksa secara berurutan dari lapisan terbawah:
1. **Link/Wi-Fi**: Apakah SSID terhubung dan mendapat kekuatan sinyal memadai?
2. **IP / DHCP**: Apakah node mendapat IP valid di *subnet* yang benar (bukan `0.0.0.0` atau `169.254.x.x`), serta *subnet mask* & *default gateway* tepat?
3. **Reachability (`ping`)**: Dapatkah *Gateway* dan host tujuan dicapai lewat ICMP (catatan: sebagian *cloud server* memblokir ICMP)?
4. **DNS (`nslookup`)**: Apakah nama domain broker berhasil di-resolve menjadi IP yang benar?
5. **Port / Firewall (`Test-NetConnection` / `nc -vz`)**: Apakah port tujuan (misal `1883` atau `8080`) benar-benar terbuka dan tidak diblokir *firewall* lokal OS server?

### 7. Real-World Applications

- **Segmentasi VLAN / Subnet Smart Campus & Pabrik**: Memisahkan 60 node sensor ke subnet `/26` tersendiri mencegah *broadcast storm* mengganggu jaringan kantor dan membatasi permukaan serangan (*attack surface*).
- **Pemilihan UDP vs TCP pada Sensor Baterai**: Protokol berbasis UDP (seperti CoAP atau DNS) memangkas waktu bangun radio ESP32 karena tidak memerlukan *TCP 3-way handshake* pada setiap pengiriman singkat.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-11/exercises.md)):
1. Perhitungan CIDR subnetting (`/25`, `/27`, `/28`) dan pengecekan apakah dua IP berada pada subnet yang sama.
2. Analisis paket & perhitungan efisiensi *goodput* untuk payload $20\text{ B}$ vs $512\text{ B}$.
3. Skenario diagnosis kegagalan konektivitas bertahap (DHCP gagal vs DNS gagal vs Firewall port `1883` diblokir).
4. Simulasi Python dengan [`network_diagnostics_sim.py`](content/chapter-11/src/network_diagnostics_sim.py).

## Tugas

Susun **Rencana Pengalamatan Subnet IoT, Analisis Goodput & Panduan Diagnosis Jaringan** untuk satu proyek lapangan (detail di tab **Tugas & Rubrik** — [assignment.md](content/chapter-11/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Perhitungan pengalamatan IPv4 & CIDR subnetting | 25 | Pembagian subnet tepat, tidak tumpang tindih, menyertakan Gateway & batas usable host |
| Analisis protokol Transport (TCP vs UDP) & goodput | 25 | Ketepatan perbandingan handshake/header dan perhitungan persentase *goodput* |
| Prosedur troubleshooting jaringan berlapis | 30 | Diagnosis terstruktur dari Link $\rightarrow$ IP/DHCP $\rightarrow$ Gateway $\rightarrow$ DNS $\rightarrow$ Port/Firewall |
| Dokumentasi, simulasi & kejujuran bukti | 20 | Output skrip/uji terdokumentasi jelas tanpa klaim pengukuran jaringan fiktif |

## Ringkasan

- TCP/IP 4-layer stack memisahkan tanggung jawab **Link**, **Internet (IP/Routing)**, **Transport (TCP/UDP + Port)**, dan **Application (MQTT/HTTP)**.
- **TCP** menjamin urutan dan keandalan lewat *3-way handshake* dan retransmisi dengan *header* $20\text{ B}$, sedangkan **UDP** hemat *overhead* ($8\text{ B}$, tanpa handshake) untuk pesan ringan yang toleran kehilangan.
- **Bandwidth** bukanlah **goodput**; pada payload IoT kecil ($48\text{ B}$), lebih dari separuh *byte* di kabel adalah *header* protokol ($45{,}3\%$ *goodput* pada TCP/IPv4).
- Skrip Python `network_diagnostics_sim.py` telah dieksekusi nyata untuk memvalidasi kalkulasi CIDR dan probe sintetis (`outputs.md`).

## Referensi

1. IETF RFC 1918, *Address Allocation for Private Internets*, [https://datatracker.ietf.org/doc/html/rfc1918](https://datatracker.ietf.org/doc/html/rfc1918) (diperiksa 2026-11-11).
2. IETF RFC 9293, *Transmission Control Protocol (TCP)*, [https://datatracker.ietf.org/doc/html/rfc9293](https://datatracker.ietf.org/doc/html/rfc9293) (diperiksa 2026-11-11).
3. Espressif Systems, *ESP-IDF lwIP TCP/IP Stack Documentation*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/lwip.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/lwip.html) (diperiksa 2026-11-11).


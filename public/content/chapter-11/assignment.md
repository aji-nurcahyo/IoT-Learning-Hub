# Tugas & Rubrik — Chapter 11

## Skenario Tugas: Rencana Pengalamatan Subnet & Panduan Diagnosis Jaringan IoT

Sebuah gedung kampus memiliki 3 zona pemasangan perangkat IoT:
- **Zona A (Ruang Lab & Server)**: 22 node sensor + 1 *Edge Gateway* + 1 *Broker*.
- **Zona B (Taman & Greenhouses)**: 50 node sensor + 2 *Gateway*.
- **Zona C (Area Parkir & Gerbang)**: 10 node sensor + 1 *Gateway*.

## Instruksi Pengerjaan

1. **Rancangan Subnet CIDR**: Gunakan blok induk `192.168.40.0/24` dan bagi menjadi 3 subnet terpisah (*VLSM* atau blok berukuran sesuai kebutuhan tiap zona dengan margin pertumbuhan minimal $25\%$). Cantumkan *Network*, *Netmask*, *Default Gateway*, rentang *Usable Host*, dan *Broadcast* setiap zona tanpa tumpang tindih.
2. **Analisis Transport & Goodput**: Bandingkan pengiriman via TCP vs UDP untuk skenario payload $64\text{ B}$ setiap $10\text{ detik}$ vs *batch* $320\text{ B}$ setiap $50\text{ detik}$.
3. **SOP Troubleshooting 5-Langkah**: Susun alur diagnosis dari *Link* hingga *Socket/Firewall* untuk memecahkan kasus: (a) IP `0.0.0.0`, (b) DNS gagal, dan (c) port broker diblokir.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Perhitungan pengalamatan IPv4 & CIDR subnetting** | **25** | Pembagian subnet dari `/24` bebas tumpang tindih, kapasitas mencukupi margin, serta *netmask/gateway/broadcast* akurat. |
| **Analisis protokol Transport (TCP vs UDP) & goodput** | **25** | Perbandingan *handshake/header* tepat dan perhitungan persentase *goodput* benar. |
| **Prosedur troubleshooting jaringan berlapis** | **30** | SOP diagnosis berurutan (Link $\rightarrow$ IP/DHCP $\rightarrow$ Gateway $\rightarrow$ DNS $\rightarrow$ Port/Firewall) dilengkapi perintah uji nyata. |
| **Dokumentasi, simulasi & kejujuran bukti** | **20** | Penyajian tabel rapi, hasil uji skrip/perhitungan terdokumentasi jujur tanpa klaim jaringan fiktif. |


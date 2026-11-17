# Latihan Chapter 34: Interoperability, Matter & Thread Fundamentals

## Latihan Konseptual

1. **Komparasi Matter vs Zigbee/Z-Wave**:
   Mengapa pengenalan Matter dianggap sebagai titik balik industri smart home dibandingkan protokol pendahulunya seperti Zigbee atau Z-Wave? Jelaskan dampak penerapan native IPv6 dan ketiadaan kebutuhan jembatan (*proprietary bridges*) terhadap pengalaman pengguna dan skalabilitas aplikasi.

2. **Dinamika Topologi Thread Mesh**:
   Jelaskan perbedaan mendasar antara node bertipe *Thread Router* dengan *Sleepy End Device (SED)* dalam hal sumber daya energi, tanggung jawab penerusan paket (*packet forwarding*), dan pemeliharaan tabel routing RLOC16.

3. **Mekanisme Multi-Fabric Matter**:
   Jelaskan bagaimana sebuah perangkat cerdas (misalnya bohlam pintar) dapat dikendalikan secara simultan oleh ekosistem Apple Home dan Google Home tanpa membocorkan kredensial atau riwayat telemetri di antara kedua ekosistem tersebut.

## Latihan Praktik & Perhitungan

1. **Analisis Rute Multihop Thread Mesh**:
   Diberikan topologi jaringan Thread dengan node-node berikut:
   - DoorLock (End Device) terhubung ke Router1.
   - Router1 terhubung ke Thread Leader.
   - Thread Leader terhubung ke Border Router (OTBR).
   - LightSensor (End Device) terhubung ke Border Router.
   
   *Instruksi*:
   - Tuliskan urutan rute paket data dari node `DoorLock` menuju `LightSensor`.
   - Berapa jumlah hop transmisi radio yang dilalui paket tersebut?
   - Jika satu hop IEEE 802.15.4 rata-rata memerlukan waktu transmisi dan pemrosesan 15 ms, estimasikan total latensi transfer paket antar kedua perangkat tersebut.

2. **Simulasi Alur Commissioning PASE**:
   Uraikan langkah-langkah pertukaran data kriptografi yang terjadi ketika pengguna memindai kode QR perangkat Matter hingga terbentuknya saluran terenkripsi pertama kali berbasis algoritma SPAKE2+.

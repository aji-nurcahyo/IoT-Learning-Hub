# Chapter 37: Scalable IoT Architecture & Deployment

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami prinsip skalabilitas sistem IoT berskala besar (*millions of concurrent connections*).
2. Membedakan strategi skalabilitas vertikal (*scaling up*) versus skalabilitas horizontal (*scaling out*).
3. Menganalisis arsitektur pengelompokan broker MQTT (*Broker Clustering*) menggunakan EMQX/Mosquitto Bridge dan load balancer HAProxy.
4. Mengimplementasikan teknik partisi data telemetri (*Sharding / Consistent Hashing*) untuk mendistribusikan beban kerja secara merata ke kluster worker.
5. Memahami penanganan tekanan balik antrean (*Backpressure Mitigation*) dan orkestrasi berbasis kontainer (Docker & Kubernetes).

## Prasyarat

- Pemahaman arsitektur protokol MQTT dan pola publish/subscribe (Chapter 14).
- Konsep dasar jaringan komputer, proxy TCP/IP, dan load balancer layer-4/7 (Chapter 12).
- Dasar-dasar struktur data antrean dan fungsi hash kriptografi (Chapter 24 & 32).

## Konsep dan teori

### 1. Tantangan Skalabilitas IoT

Ketika ekosistem IoT bertumbuh dari 100 node menjadi 1.000.000 node, arsitektur monolitik tunggal akan runtuh akibat empat faktor:
1. **Kapasitas Soket TCP**: Batas file descriptor sistem operasi Linux (`ulimit -n`) membatasi jumlah koneksi persisten bersamaan.
2. **Ledakan Throughput**: Jutaan pesan per detik meluapkan buffer RAM antrean database.
3. **Penyebaran Topik (Fan-out)**: Broker tunggal kehabisan memori untuk melacak jutaan subscription tree dan filter wildcard (`#`, `+`).
4. **Ketersediaan Tinggi (High Availability)**: Kerusakan pada satu server fisik tidak boleh memutus kendali operasional seluruh armada.

```
                  [1.000.000 Device Connections]
                                |
                                v
               [Layer-4 Load Balancer (HAProxy)]
                (TCP Round-Robin / IP-Hash)
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
 [MQTT Node A]           [MQTT Node B]           [MQTT Node C]
  (Cluster EMQX) <=====>  (Cluster EMQX) <=====>  (Cluster EMQX)
        |                       |                       |
        +-----------------------+-----------------------+
                                |
                                v
             [Distributed Sharding Queue / Kafka]
             Partition 0 | Partition 1 | Partition 2
                                |
                                v
               [Auto-scaling Worker Consumers]
```

### 2. Partisi Data & Consistent Hashing

Untuk memproses telemetri secara paralel tanpa terjadi benturan data, pesan dikelompokkan ke dalam partisi (*Partitions*) menggunakan kunci identitas perangkat (*Device ID*):

$$\text{Partition ID} = \text{Hash}(\text{Device ID}) \pmod N$$

Di mana $N$ adalah jumlah partisi aktif.

Dengan algoritma hash yang seragam (seperti MD5 atau MurmurHash3):
- Beban komputasi terdistribusi secara seimbang ke seluruh partisi (misalnya 25% per partisi pada kluster 4-node).
- Pesan dari satu perangkat yang sama selalu mendarat pada partisi yang identik, menjamin integritas urutan kejadian (*strict in-order delivery*).

### 3. Penanganan Tekanan Balik (Backpressure)

Ketika laju kedatangan pesan ($R_{in}$) melebihi laju pemrosesan database ($R_{out}$), antrean akan membengkak hingga menghabiskan alokasi memori heap (OOM Crash).

Strategi mitigasi backpressure industri:
1. **Drop Newest / Drop Oldest**: Mengorbankan pesan telemetri frekuensi tinggi yang sudah usang demi mempertahankan stabilitas sistem.
2. **Pushback / Throttling**: Memberikan sinyal *slow-down* kepada perangkat pengirim melalui penurunan interval pelaporan.
3. **Queue Buffering**: Mengalirkan lonjakan beban ke dalam distributed persistent log seperti Apache Kafka atau RabbitMQ.

## Latihan

1. **Analisis Hash Sharding**: Mengapa penggunaan nomor urut acak (*random round-robin*) dilarang saat mendistribusikan telemetri sensor ke beberapa antrean worker yang terpisah? Apa dampaknya terhadap pemeliharaan state sensor dan deteksi anomali deret waktu?
2. **Batas File Descriptor Linux**: Pada sistem operasi Linux yang menjalankan broker MQTT, jika nilai default `ulimit -n` adalah 1024, berapa maksimal koneksi perangkat yang dapat dilayani sebelum sistem menghasilkan error `Too many open files`? Bagaimana cara mengonfigurasinya untuk menangani 100.000 koneksi?
3. **Mekanisme Shared Subscriptions**: Dalam spesifikasi MQTT v5.0, jelaskan bagaimana fitur *Shared Subscriptions* (`$share/group_name/topic`) secara otomatis membagi beban pesan ke beberapa klien pelanggan tanpa membutuhkan proxy tambahan.

## Tugas

Kembangkan modul simulasi arsitektur terdistribusi Python (`scalability_cluster_sim.py`) yang:
1. Menerapkan pembagian 4 partisi deterministik berbasis hash MD5 dari 100 perangkat IoT unik.
2. Memverifikasi keseimbangan distribusi beban lintas partisi tanpa ada partisi yang kelaparan (*starvation*).
3. Menguji batas proteksi tekanan balik (*backpressure*) saat antrean partisi penuh dan memvalidasi pengurasan batch data oleh worker pemroses secara paralel.

## Ringkasan

1. Skalabilitas IoT skala masif menuntut transisi dari broker tunggal menuju kluster horizontal dengan load balancing terdistribusi.
2. Consistent hashing menjamin distribusi beban telemetri yang merata sekaligus menjaga integritas urutan pesan per perangkat.
3. Penerapan kontrol backpressure yang disiplin melindungi ketersediaan platform dari ancaman lonjakan trafik tak terduga.

## Referensi

1. Kleppmann, M. *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*. O'Reilly Media, 2017.
2. OASIS. *MQTT Version 5.0 Standard Specification: Shared Subscriptions*. 2019.
3. Burns, B. *Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services*. O'Reilly Media, 2018.

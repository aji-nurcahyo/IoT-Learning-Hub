# Tugas Terbimbing: Perancangan Partisi Antrean Terdistribusi & Mitigasi Backpressure

## Deskripsi Tugas

Dalam tugas ini, Anda diminta merancang dan memverifikasi arsitektur kluster pemrosesan telemetri IoT terdistribusi yang mampu mempartisi beban kerja dari ratusan perangkat serta memproteksi kestabilan sistem dari ancaman kelebihan beban (*backpressure*).

Tugas ini mewajibkan:
1. Pembuatan modul *Partitioned Broker Cluster* Python yang membagi aliran telemetri ke dalam beberapa partisi antrean deterministik menggunakan fungsi hash berbasis *Device ID*.
2. Pengujian distribusi beban lintas partisi menggunakan data uji 100 perangkat IoT unik untuk membuktikan keseimbangan beban tanpa ada partisi yang kelaparan (*starvation*).
3. Penerapan dan pengujian mekanisme proteksi *Backpressure Queue Limit* yang menolak atau membuang lonjakan pesan saat batas antrean tercapai, serta verifikasi pengurasan batch data oleh worker secara paralel.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-37/src/scalability_cluster_sim.py`.
2. Laporan analisis teknis yang mencakup tabel distribusi pesan per partisi, analisis grafik lonjakan antrean, dan rekomendasi tuning kernel Linux untuk platform berskala 100.000+ perangkat.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Pemodelan Sharding & Distribusi Hash** | 35 Poin | Implementasi pembagian partisi berbasis hash MD5 terbukti deterministik, mendistribusikan 100 pesan ke 4 partisi secara seimbang, dan menjamin *in-order routing* per perangkat. |
| **Penerapan Proteksi Batas Antrean & Backpressure** | 35 Poin | Batas kapasitas antrean partisi (50 pesan) ditegakkan secara disiplin, penghitungan pesan terbuang terbukti akurat, dan sistem terhindar dari *crash* kehabisan memori. |
| **Kualitas Konsumsi Batch & Analisis Skalabilitas** | 30 Poin | Pengurasan batch data worker berjalan efisien, pembahasan menyajikan analisis mendalam mengenai kluster MQTT horizontal, Shared Subscriptions, dan tuning soket Linux. |

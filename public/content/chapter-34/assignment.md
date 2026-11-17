# Tugas Terbimbing: Pemodelan Topologi Thread Mesh & Alur Commissioning Matter

## Deskripsi Tugas

Dalam tugas ini, Anda diminta membangun modul simulasi yang memodelkan interkoneksi jaringan mesh Thread berbasis IEEE 802.15.4/IPv6 serta alur proses *commissioning* standar Matter (Project CHIP).

Tugas ini mewajibkan:
1. Pemodelan topologi jaringan *Thread Mesh* yang mencakup peran *Leader*, *Router*, *End Device*, dan *Border Router*, lengkap dengan algoritma penentuan rute multihop terpendek.
2. Implementasi mekanisme otentikasi awal *Password-Authenticated Session Establishment* (PASE) menggunakan kode PIN verifikasi serta penerbitan kredensial operasional *Node Operational Certificate* (NOC) ke dalam *Fabric*.
3. Verifikasi otomatis skenario penemuan rute dan penyelesaian *commissioning* melalui eksekusi skrip Python terpadu.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-34/src/matter_thread_sim.py`.
2. Laporan teknis yang menyajikan visualisasi diagram topologi mesh, evaluasi latensi transmisi multihop, serta analisis keunggulan model data Matter Multi-Admin.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Pemodelan Jaringan Thread & Routing Multihop** | 35 Poin | Topologi Thread mesh membedakan peran node secara benar, rute paket terpendek (BFS) teridentifikasi secara tepat, dan konsep bebas titik kegagalan tunggal (*self-healing*) terjelaskan secara tuntas. |
| **Implementasi Alur Commissioning Matter (PASE & NOC)** | 35 Poin | Alur commissioning memvalidasi kode PIN penyiapan, membedakan tahap PASE dan CASE secara konseptual, serta menerbitkan Fabric ID dan status operasional perangkat secara akurat. |
| **Analisis Interoperabilitas & Arsitektur Multi-Fabric** | 30 Poin | Pembahasan menyajikan pemahaman mendalam mengenai kompresi header 6LoWPAN, manfaat native IPv6, dan isolasi keamanan kriptografi pada arsitektur multi-ekosistem. |

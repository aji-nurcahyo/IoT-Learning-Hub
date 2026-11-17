# Panduan Implementasi: Scalable IoT Architecture & Deployment

Dokumen ini menjelaskan implementasi teknis pemartisian antrean data telemetri berbasis *consistent hashing* dan proteksi *backpressure* pada sistem terdistribusi.

## 1. Modul Simulasi Kluster Partisi Python

Modul [scalability_cluster_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-37/src/scalability_cluster_sim.py) mengimplementasikan:
1. `PartitionedBrokerCluster`: menghitung indeks partisi deterministik menggunakan hash MD5 dari `device_id` modulo jumlah partisi aktif ($N=4$):
   $$\text{Partition ID} = \text{int}(\text{MD5}(\text{device\_id}), 16) \pmod 4$$
2. Proteksi *Backpressure*: membatasi antrean partisi maksimal 50 pesan. Bila batas terlampaui, pesan berlebih akan ditolak/dibuang secara aman untuk mencegah kehabisan alokasi memori heap (*OOM crash*).
3. Konsumsi Batch Worker: fungsi `consume_batch` yang memungkinkan worker membaca sekumpulan pesan secara paralel.

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-37/src/scalability_cluster_sim.py
```

### Hasil Verifikasi Eksekusi:
```text
=== CHAPTER 37: SCALABLE IOT ARCHITECTURE SIMULATION ===
Mendistribusikan telemetri dari 100 perangkat IoT...
Distribusi Pesan pada Partisi [0, 1, 2, 3]: [25, 24, 23, 28]
Menguji batas antrean partisi (Backpressure test)...
Partisi 0 Size: 50 | Total Dropped (Backpressure): 5
Worker menguras 20 pesan dari Partisi 0. Sisa antrean: 30
STATUS: VERIFIED (Semua pengujian sharding partisi, hash deterministik, dan backpressure lulus 100%)
```

## 2. Jaminan Urutan Pesan (In-Order Delivery)

Dengan menggunakan identitas perangkat (*Device ID*) sebagai kunci partisi:
- Seluruh pesan dari `dev-edge-001` akan selalu dipetakan ke partisi yang sama setiap saat.
- Worker yang didedikasikan untuk partisi tersebut memproses telemetri secara berurutan sesuai kedatangan, mengeliminasi risiko pembacaan state yang saling mendahului (*out-of-order state corruption*).

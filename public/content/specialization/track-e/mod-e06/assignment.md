# Tugas Rekayasa & Rubrik: Modul E06

## Penugasan Mandiri: Audit Kesiapan Produksi Platform Smart City

1. Kembangkan rencana deployment Docker Compose untuk platform kota cerdas yang mengintegrasikan Orion-LD Context Broker, MongoDB backend, Mosquitto MQTT broker, dan dashboard GIS.
2. Buat skenario pengujian penetrasi keamanan (penetration testing) untuk memverifikasi isolasi token multi-tenant antar-dinas.
3. Rancang rencana mitigasi bencana (*Disaster Recovery Plan*) untuk command center kota dengan target RPO (Recovery Point Objective) < 1 menit dan RTO (Recovery Time Objective) < 15 menit.
4. Susun laporan rekayasa komprehensif yang siap dipresentasikan kepada pimpinan dinas kominfo kota.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Kinerja Ingestion SATC-E01** | 25 | Ketahanan penyerapan 12.000 pkt/s tanpa packet loss |
| **Garansi SLA Latensi SATC-E02** | 25 | Waktu tinggal paket darurat M/G/1 di bawah 80 ms pada utilisasi tinggi |
| **Isolasi Multi-Tenant SATC-E03** | 25 | Penolakan 403 Forbidden terbukti pada upaya akses cross-tenant |
| **Geofencing & Privasi SATC-E04** | 25 | Deteksi pelanggaran rute < 100 ms dan kuantisasi spasial heksagonal H3 |

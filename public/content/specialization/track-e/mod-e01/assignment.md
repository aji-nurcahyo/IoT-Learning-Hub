# Tugas Rekayasa & Rubrik: Modul E01

## Penugasan Mandiri: Pemodelan Entitas NGSI-LD & Audit Multi-Tenant

Rancang skema entitas NGSI-LD lengkap untuk sistem pemantauan kualitas udara kota (tipe *AirQualityObserved*). Kembangkan modul Python yang memvalidasi integritas data dan menguji bahwa pengguna tenant eksternal tanpa hak akses ditolak dengan status HTTP 403 Forbidden.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Pemodelan Arsitektur IoT Perkotaan** | 25 | Menjelaskan topologi bertingkat dan integrasi sensor perkotaan terdistribusi. |
| **Implementasi Entitas FIWARE NGSI-LD** | 35 | Menyusun struktur entitas JSON-LD dengan properti dan observedAt yang tepat. |
| **Penegakan Keamanan Multi-Tenant** | 25 | Membuktikan pemblokiran akses lintas dinas dengan status HTTP 403 Forbidden. |
| **Kalkulasi Keandalan Four-Nines** | 15 | Menghitung ketersediaan paralel gateway multi-link secara matematis. |

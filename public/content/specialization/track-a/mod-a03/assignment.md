# Tugas Rekayasa & Rubrik: Modul A03

## Penugasan Mandiri: Pemodelan Siklus Commissioning Matter & Topologi Thread

Kembangkan simulator Python yang memodelkan transisi status perangkat Matter (dari UNCOMMISSIONED -> PASE -> ATTESTATION -> OPERATIONAL). Simulasikan injeksi perintah kluster On/Off dan verifikasi bahwa penolakan terjadi jika Fabric Index tidak valid.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Prinsip Arsitektur Matter & Thread** | 30 | Menjelaskan peran node Thread dan kedaulatan komunikasi lokal. |
| **Kriptografi SPAKE2+ & DAC** | 30 | Menganalisis alur pertukaran kunci PASE dan verifikasi sertifikat X.509. |
| **Konfigurasi Jaringan & Dataset Thread** | 25 | Menjelaskan parameter PAN ID, channel, dan routing IPv6. |
| **Pemodelan Multi-Admin & ZCL Cluster** | 15 | Mendokumentasikan eksekusi perintah cluster pada multiple fabrics. |

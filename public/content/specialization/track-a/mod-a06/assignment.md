# Tugas Rekayasa & Rubrik: Modul A06

## Penugasan Mandiri: Laporan Evaluasi Capstone Pengontrol Gedung Cerdas

Susun laporan teknik rekayasa formal yang mendokumentasikan kelulusan pengujian SATC-A01 hingga SATC-A04. Sertakan trace log eksekusi saat sinyal alarm darurat kebakaran diinjeksikan dan buktikan waktu tanggap relay berada di bawah 80 milidetik.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **SATC-A01: Ventilasi IAQ Closed-Loop** | 25 | Respon cepat <= 5s dan pemulihan CO2 < 800 ppm tanpa chattering. |
| **SATC-A02: Ketahanan Jaringan Thread Lokal** | 25 | Operasi normal PDR 100% dan latensi < 50ms saat WAN terputus. |
| **SATC-A03: Pemicu Peak-Shaving Beban** | 25 | Daya gedung turun di bawah batas kontrak dalam waktu <= 3s. |
| **SATC-A04: Interlock Keselamatan Jiwa** | 25 | Pintu terbuka fail-safe dan kipas mati dalam waktu < 80ms saat alarm. |

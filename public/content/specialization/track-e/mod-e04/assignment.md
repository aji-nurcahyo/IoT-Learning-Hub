# Tugas Rekayasa & Rubrik: Modul E04

## Penugasan Mandiri: Pemodelan Antrean Multi-Prioritas Gateway Kota

1. Perluas fungsi simulasi M/G/1 untuk mendukung 3 kelas prioritas (Emergency, Control Command, Telemetry).
2. Lakukan uji stres dengan meningkatkan utilisasi total $\rho$ dari 0.50 hingga 0.98.
3. Analisis pada utilisasi berapa latensi Kelas 3 mulai mengalami ketidakstabilan eksponensial (*queue explosion*).
4. Buat algoritma pembatasan laju (*rate-limiting*) pada simpul telemetri rutin untuk mencegah kolapsnya antrean gateway saat terjadi bencana kota.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Analisis Kapasitas ALOHA** | 30 | Ketepatan pemodelan kurva Pure vs Slotted ALOHA |
| **Formulasi Antrean M/G/1** | 40 | Kebenaran penurunan matematis waktu tunggu residu dan prioritas |
| **Validasi SLA Latensi** | 30 | Bukti komputasi latensi Kelas 1 di bawah 80 ms pada beban tinggi |

# Tugas Rekayasa & Rubrik: Modul E03

## Penugasan Mandiri: Optimasi Parameter Baterai Meteran Air

1. Jalankan simulasi dengan memvariasikan interval pelaporan data (TAU) dari 1 jam hingga 24 jam dengan inkremen 1 jam.
2. Gambarkan grafik hubungan antara frekuensi pelaporan harian terhadap estimasi umur baterai.
3. Hitung kapasitas baterai minimum (mAh) yang dibutuhkan agar perangkat yang mengirim data tiap 6 jam dapat beroperasi minimal 10 tahun.
4. Buat dokumen spesifikasi teknis pemilihan sel baterai LiSOCl2 untuk kondisi suhu perkotaan tropis (30-45 derajat Celcius).

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Konfigurasi 3GPP Timers** | 30 | Ketepatan perhitungan durasi aktif T3324 dan interval pelaporan T3412 |
| **Model Konsumsi Energi** | 40 | Akurasi pemodelan matematis multi-state (Active, Idle, PSM) |
| **Validasi SLA 10 Tahun** | 30 | Bukti komputasi ketahanan baterai LiSOCl2 melampaui 10 tahun operasional |

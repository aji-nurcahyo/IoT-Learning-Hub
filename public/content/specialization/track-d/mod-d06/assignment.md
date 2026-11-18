# Tugas Rekayasa & Rubrik: Modul D06

## Penugasan Mandiri

Rancang arsitektur sistem deteksi anomali multimodal audio-vision pada mikrokontroler target. Tunjukkan bukti bahwa pemakaian memori statis SRAM berada di bawah 192 KB dan total waktu inferensi end-to-end di bawah 50 milidetik.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **SATC-D01: Dual Modal Pipeline** | 25 | Pipeline audio dan vision beroperasi secara komplementer. |
| **SATC-D02: SLA Latensi < 50 ms** | 25 | Profiling end-to-end terbukti di bawah 50 ms. |
| **SATC-D03: On-Device Bayesian Fusion** | 25 | Evaluasi log-odds berjalan lokal dan mandiri. |
| **SATC-D04: Budget Memori & Daya** | 25 | Verifikasi pemakaian memori di bawah ambang batas RTOS. |

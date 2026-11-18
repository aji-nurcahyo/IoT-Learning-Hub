# Tugas Rekayasa & Rubrik: Modul D04

## Penugasan Mandiri

Kembangkan skrip Python/C yang menerapkan EKF 4-state pada mikrokontroler untuk mengestimasi keausan bantalan. Fusi harus mampu memitigasi anomali derau transien pada pembacaan sensor getaran tanpa mengalami divergensi kovariansi P.

---

## Rubrik Penilaian (Total 100 Poin)

| Kriteria Penilaian | Bobot | Deskripsi Capaian Kinerja |
|---|:---:|---|
| **Perumusan State Space & Jacobian** | 30 | Matriks Jacobian F dan H diturunkan secara analitis dan akurat. |
| **Implementasi Algoritma EKF** | 40 | Siklus predict dan update berjalan tanpa lonjakan instabilitas numerik. |
| **Integrasi Late Bayesian Fusion** | 30 | Log-odds berhasil menyatukan sensor dengan interval sampling heterogen. |

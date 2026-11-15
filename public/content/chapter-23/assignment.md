# Tugas Mandiri: Implementasi Pipeline Edge Analytics & Local Automation

## Deskripsi Tugas

Tugas ini melatih mahasiswa merancang dan memvalidasi pipeline komputasi tepi (*edge computing*) pada gateway IoT lokal. Anda diminta untuk membangun sistem pengondisian sinyal terintegrasi yang mampu menyaring derau dan lonjakan anomali, meredam transmisi data statis berlebih, menghitung ringkasan statistik deret waktu, serta mengendalikan aktuator lokal secara mandiri menggunakan logika histeresis anti-chattering.

## Petunjuk Pengerjaan

1. **Pengondisian Sinyal (Signal Conditioning)**:
   - Implementasikan fungsi filter statistik berbasis Rentang Interkuartil (*Interquartile Range* / IQR) dengan pengali $k = 1{,}5$.
   - Bangun kelas `DeadbandFilter` yang membatasi pengiriman data hanya jika perubahan absolut terhadap nilai terkirim sebelumnya melampaui batas toleransi yang ditetapkan.
2. **Agregator Jendela Waktu (Windowing)**:
   - Susun kelas `SlidingWindowAggregator` berkapasitas $N = 5$ sampel yang secara otomatis membersihkan outlier dan menghitung rata-rata, nilai ekstrem (min/max), dan deviasi standar.
3. **Mesin Aturan Histeresis Lokal**:
   - Bangun kelas `LocalAutomationEngine` dengan ambang batas atas ($30{,}0\,^\circ\text{C}$) dan pita histeresis ($1{,}5\,^\circ\text{C}$).
   - Uji sistem dengan profil suhu yang berosilasi di sekitar ambang batas dan buktikan ketiadaan fenomena *chattering* pada sakelar relay.
4. **Buffer Sinkronisasi Cloud (Store-and-Forward)**:
   - Implementasikan antrean sirkular `EdgeSpoolBuffer` berkapasitas terbatas dengan kebijakan *drop-oldest* saat offline dan *batch draining* saat online.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Filter Outlier IQR & Deadband Compression** | 35 | Algoritma IQR dan deadband berhasil menyaring anomali ekstrim dan menekan volume transmisi data statis sesuai spesifikasi teknis. |
| 2 | **Agregasi Window & Mesin Aturan Histeresis** | 35 | Kalkulasi statistik moving average akurat; mesin aturan lokal mampu mempertahankan stabilitas relay tanpa chattering osilatif. |
| 3 | **Buffer Spooling & Arsitektur Kode** | 30 | Mekanisme store-and-forward menangani kondisi offline secara elegan dengan drop-oldest dan batch drain; kode modular, rapi, dan reproducible. |

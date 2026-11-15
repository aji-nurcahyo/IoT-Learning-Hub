# Tugas Mandiri: Perancangan Data Pipeline & Validasi Skema IoT

## Deskripsi Tugas

Tugas ini bertujuan melatih mahasiswa merancang arsitektur kontrak data IoT yang tangguh, efisien, dan idempoten pada sistem monitoring lingkungan multi-sensor. Anda diminta untuk mengimplementasikan modul validator Python mandiri yang mampu menyaring data korup sebelum diteruskan ke basis data deret waktu, serta membangun mekanisme deduplikasi pesan untuk mengatasi retransmisi jaringan.

## Petunjuk Pengerjaan

1. **Rancang Kontrak Data**:
   - Definisikan skema JSON untuk tiga tipe pesan: *telemetry* (suhu, kelembapan, tekanan udara, baterai), *event* (alarm kebocoran atau getaran tinggi), dan *command* (pengubahan interval sampling).
   - Tentukan batasan numerik fisik rasional dan tipe data primitif pada setiap atribut.
2. **Implementasikan Modul Validator**:
   - Terapkan fungsi validasi skema yang memverifikasi kehadiran *required fields*, kesesuaian tipe data, batas rentang nilai, dan kepatuhan terhadap format stempel waktu Unix Epoch UTC.
   - Sediakan mekanisme pelaporan kesalahan terstruktur yang merinci lokasi field dan jenis pelanggarannya.
3. **Bangun Pipeline Deduplikasi**:
   - Bangun struktur cache berbasis Time-To-Live (TTL $60\text{ detik}$) yang menyimpan kunci gabungan `(device_id, sequence_number)` atau `event_id`.
   - Pastikan entri usang dibersihkan secara otomatis (*eviction*) tanpa memicu kebocoran memori.
4. **Analisis Efisiensi Kompresi**:
   - Lakukan perbandingan byte antara format JSON terformat, JSON terkompresi (*minified*), dan struktur biner (*binary struct*).
   - Sajikan laporan ringkas hasil benchmark dan implikasi penghematan biaya bandwidth jaringan.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Ketepatan Skema & Validasi Data** | 35 | Kontrak skema mencakup seluruh batas fisik sensor; validator mampu mendeteksi payload malformed, out-of-range, dan format waktu invalid dengan pesan diagnostik yang jelas. |
| 2 | **Keandalan Mekanisme Idempotensi** | 35 | Logika deduplikasi berhasil mendeteksi dan mengeliminasi paket retransmisi duplikat dalam batas jendela TTL, serta menerapkan mekanisme pembersihan entri kadaluwarsa secara berkala. |
| 3 | **Efisiensi Serialisasi & Dokumentasi Teknis** | 30 | Skrip menyajikan perbandingan empiris efisiensi encoding biner vs tekstual; kode ditulis modular, bebas redundansi, dan menyertakan panduan eksekusi yang reproducible. |

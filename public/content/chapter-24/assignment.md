# Tugas Mandiri: Rancang Bangun Event-Driven Pipeline dengan Node-RED

## Deskripsi Tugas

Tugas ini melatih mahasiswa merancang, menyusun, dan menguji arsitektur alur kerja integrasi berbasis event (*event-driven integration flow*) menggunakan Node-RED. Anda diminta untuk menyusun alur deklaratif JSON yang menerima telemetri lingkungan dari broker MQTT, memperbarui cache status global, menyaring kondisi bahaya dengan simpul Switch dan Function, menyediakan antarmuka REST API mikro, serta mengisolasi galat tak terduga dengan simpul Catch.

## Petunjuk Pengerjaan

1. **Penyusunan Alur Deklaratif (`flows.json`)**:
   - Susun simpul `mqtt in` dengan konfigurasi subskripsi topik `iot/lab/+/telemetry`.
   - Hubungkan ke simpul `change` untuk merekam status telemetri terbaru ke variabel konteks `global`.
   - Tambahkan simpul `switch` dengan aturan evaluasi `>= 30.0 C` (jalur kritis) dan `< 30.0 C` (jalur normal).
2. **Penyusunan Simpul Pengayaan & Penerbitan**:
   - Pada jalur kritis, hubungkan simpul `function` yang menyusun objek pesan event alarm baru (menyertakan atribut `event_id`, `type`, `severity`, dan stempel waktu UTC).
   - Terbitkan pesan alarm tersebut ke broker MQTT lokal menggunakan simpul `mqtt out`.
3. **Penyediaan Endpoint REST API Mikro**:
   - Susun simpul `http in` untuk melayani panggilan metode `GET /api/v1/telemetry/latest`.
   - Baca status dari variabel konteks `global` dan kembalikan ke klien menggunakan simpul `http response` berstatus `200 OK`.
4. **Isolasi Galat Runtime**:
   - Pasang simpul `catch` yang mengawasi seluruh canvas dan mengalirkan pengecualian ke simpul log antrean surat mati (*Dead-Letter Log*).
5. **Verifikasi Simulasi Otomatis**:
   - Jalankan uji validasi menggunakan skrip [`nodered_flow_runner.py`](content/chapter-24/src/nodered_flow_runner.py) dan dokumentasikan hasil eksekusi terminal pada laporan.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Struktur Alur Deklaratif & Logika Percabangan** | 35 | Berkas flows.json valid secara skema; simpul switch dan function memilah dan memperkaya payload alarm secara akurat. |
| 2 | **Manajemen Konteks Global & Integrasi REST API** | 35 | Variabel konteks global terbarukan dengan benar; endpoint HTTP melayani pembacaan data telemetri terkini tanpa galat. |
| 3 | **Penanganan Galat Catch & Kelengkapan Verifikasi** | 30 | Simpul catch menangani pesan malformed secara terisolasi tanpa memicu crash; seluruh kasus uji lolos verifikasi simulasi. |

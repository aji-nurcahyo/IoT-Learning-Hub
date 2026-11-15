# Tugas Mandiri: Rancang Bangun Device Registry & Fleet Manager

## Deskripsi Tugas

Tugas ini melatih mahasiswa membangun modul sistem manajemen armada perangkat terhubung (*IoT Fleet Management*) yang mencakup registri inventaris perangkat keras, pemantauan kesehatan armada melalui detak jantung (*heartbeat monitoring*), rekonsiliasi konfigurasi menggunakan pola kembar digital (*Digital Twin Desired vs Reported State*), dan prosedur pemensiunan perangkat (*decommissioning*).

## Petunjuk Pengerjaan

1. **Struktur Data Registri Inventaris**:
   - Susun kelas `DeviceRecord` yang menyimpan identitas unik perangkat keras (`dev_id`, `hw_model`, `mac_addr`, `fw_version`), status siklus hidup, dan stempel waktu denyut terakhir.
   - Sediakan metode serialisasi `to_dict()` yang merangkum kondisi status dan status *configuration drift*.
2. **Pola Kembar Digital (Digital Twin)**:
   - Bangun pasangan atribut kamus `desired_config` dan `reported_config` yang dilengkapi penomoran versi inkremental (`version`).
   - Implementasikan fungsi `set_desired_config` untuk memperbarui konfigurasi di sisi server/operator.
   - Implementasikan fungsi `report_device_config` yang menyimulasikan konfirmasi penerimaan (*Reported ACK*) dari mikrokontroler fisik hingga bendera drift kembali bernilai `False`.
3. **Heartbeat Monitor & Deteksi Node Mati**:
   - Bangun metode `evaluate_fleet_health` yang menghitung selisih waktu terhadap detak terakhir ($\Delta t$).
   - Klasifikasikan status node secara dinamis:
     - `ONLINE`: Jika $\Delta t \le 15\text{s}$.
     - `DEGRADED`: Jika $15\text{s} < \Delta t \le 30\text{s}$.
     - `OFFLINE`: Jika $\Delta t > 30\text{s}$.
4. **Prosedur Pemensiunan Aman (Decommissioning)**:
   - Implementasikan fungsi `decommission_device` yang mengubah status node menjadi `DECOMMISSIONED`.
   - Buktikan melalui pengujian unit bahwa seluruh transmisi atau denyut jantung berikutnya dari node yang telah dipensiunkan ditolak secara tegas oleh sistem.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Desain Registri & Manajemen Identitas** | 30 | Struktur data registri inventaris lengkap; validasi pendaftaran node baru mencegah duplikasi identitas perangkat. |
| 2 | **Sinkronisasi Digital Twin & Deteksi Drift** | 35 | Rekonsiliasi Desired vs Reported state twin bekerja presisi; penomoran versi konfigurasi dan eliminasi drift terbukti akurat. |
| 3 | **Deteksi Ketersediaan & Alur Decommissioning** | 35 | Klasifikasi status bertingkat (Online/Degraded/Offline) berbasis waktu tepat; pengujian penolakan node pensiun berhasil dibuktikan. |

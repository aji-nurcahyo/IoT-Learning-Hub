# Tugas Mandiri: Rancang Bangun Simulator OTA Dual-Bank & Automatic Rollback

## Deskripsi Tugas

Tugas ini melatih mahasiswa merancang dan memvalidasi alur kerja pembaruan firmware jarak jauh (*Over-The-Air / OTA Updates*) tingkat industri. Anda diminta untuk mengimplementasikan simulator arsitektur partisi flash Dual-Bank A/B, memvalidasi tanda tangan digital kriptografis citra firmware, menguji pemantauan kesehatan runtime (*health-check*), serta memverifikasi mekanisme pembatalan otomatis (*Automatic Rollback*) saat terjadi kegagalan bootloop.

## Petunjuk Pengerjaan

1. **Model Partisi Memori Flash Dual-Bank A/B**:
   - Susun kelas `OtaStateMachine` yang mengelola dua bank aplikasi (`app0` dan `app1`) dan penanda status partisi (`VALID`, `PENDING_VERIFY`, `INVALID`, `EMPTY`).
   - Terapkan logika pemilihan bank target pengunduhan (memilih bank pasif yang sedang tidak aktif).
2. **Pembangkitan & Verifikasi Tanda Tangan Kriptografis**:
   - Bangun fungsi penandatanganan `generate_signed_binary` yang menghitung hash digest SHA-256 dan tanda tangan digital HMAC.
   - Bangun fungsi `verify_firmware_package` yang menolak biner yang mengalami perubahan hash (*tampering*) atau tanda tangan tidak valid sebelum penulisan flash.
3. **Simulasi Bootloop & Automatic Rollback**:
   - Bangun metode `simulate_boot` yang melacak jumlah percobaan booting saat partisi berstatus `PENDING_VERIFY`.
   - Jika jumlah reboot melebihi batas kuota toleransi (misal 2 kali) tanpa adanya konfirmasi kesehatan, picu fungsi `_trigger_automatic_rollback` untuk mengembalikan target booting ke partisi lama yang stabil.
4. **Alur Konfirmasi Kesehatan Permanen**:
   - Implementasikan fungsi `confirm_firmware_health` yang mengubah status partisi dari `PENDING_VERIFY` menjadi `VALID` permanen saat seluruh pengujian sistem dinyatakan sehat.
5. **Validasi Tiga Skenario Pengujian**:
   - Eksekusi skrip pengujian mandiri [`ota_lifecycle_simulator.py`](content/chapter-29/src/ota_lifecycle_simulator.py) yang memvalidasi ketiga skenario: penolakan biner korup, rollback saat bootloop, dan konfirmasi permanen firmware stabil.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Model Partisi Dual-Bank & Kriptografi Tanda Tangan** | 35% | Struktur partisi A/B dimodelkan akurat; integritas SHA-256 dan verifikasi tanda tangan digital menolak biner korup dengan tepat. |
| **Logika Automatic Rollback & Anti-Bootloop** | 35% | Pelacakan status PENDING_VERIFY dan kuota bootloop bekerja presisi; kegagalan booting memicu pemulihan mandiri ke bank stabil. |
| **Konfirmasi Kesehatan Permanen & Dokumentasi Uji** | 30% | Alur konfirmasi kesehatan mengesahkan biner permanen; seluruh 3 skenario pengujian diverifikasi secara deterministik pada laporan. |

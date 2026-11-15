# Latihan Soal & Praktik — Chapter 29

## Bagian A — Soal Konseptual

1. **Prinsip Dual-Bank Partitioning**:
   Jelaskan mengapa arsitektur pembaruan firmware menggunakan skema partisi Dual-Bank A/B jauh lebih aman daripada metode penulisan partisi tunggal (*Single-Bank in-place flashing*), khususnya ketika terjadi pemadaman listrik di tengah proses transmisi data biner melalui Wi-Fi.
2. **Kriteria Kelulusan Health-Check**:
   Sebutkan minimal tiga kondisi operasional fisik yang wajib dipenuhi oleh firmware baru di fase `PENDING_VERIFY` sebelum program diizinkan memanggil fungsi pengesahan permanen `esp_ota_mark_app_valid_cancel_rollback()`.
3. **Strategi Canary Deployment**:
   Mengapa perusahaan teknologi terkemuka melarang keras metode pembaruan firmware massal serentak (*Big-Bang Release*) ke seluruh $100\%$ perangkat dalam satu waktu? Jelaskan konsep *Blast Radius* dalam konteks pembaruan firmware armada IoT.

## Bagian B — Soal Praktik Komputasi

1. **Simulasi Bootloop & Kuota Boot**:
   Menggunakan kelas `OtaStateMachine` pada skrip [`ota_lifecycle_simulator.py`](content/chapter-29/src/ota_lifecycle_simulator.py), ubah parameter `max_pending_boots` menjadi $3$.
   - Jika sebuah firmware baru diunggah ke `app1` dan mengalami crash setiap kali me-reboot dirinya sendiri, pada percobaan reboot ke berapa fungsi `_trigger_automatic_rollback` dipanggil?
   - Apa status partisi `app1` setelah rollback selesai dieksekusi?
2. **Uji Integritas Tanda Tangan**:
   Gunakan metode `generate_signed_binary` untuk menandatangani sebuah biner contoh `b"FIRMWARE_V3"`. Ubah satu byte di dalam payload biner (misal menjadi `b"FIRMWARE_V4"`), lalu panggil `verify_firmware_package`. Amati pesan kesalahan penolakan yang dihasilkan.

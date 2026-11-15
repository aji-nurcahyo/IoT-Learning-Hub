# Panduan Implementasi Kode — Chapter 29

Dokumentasi ini menjelaskan arsitektur simulator OTA pada [`ota_lifecycle_simulator.py`](content/chapter-29/src/ota_lifecycle_simulator.py).

## Struktur Modul

1. **Enumerasi `PartitionState`**:
   Mendefinisikan empat status partisi firmware:
   - `EMPTY`: Partisi belum terisi citra biner.
   - `PENDING_VERIFY`: Firmware baru baru saja ditulis dan sedang menjalani pengujian runtime.
   - `VALID`: Firmware telah membuktikan kestabilannya dan disahkan permanen.
   - `INVALID`: Firmware gagal pengujian booting atau mengalami bootloop dan dilarang di-boot kembali.
2. **Kelas `OtaStateMachine`**:
   - `generate_signed_binary`: Menghitung digest SHA-256 dan membubuhkan tanda tangan HMAC-SHA256 menggunakan kunci rahasia root pengembang.
   - `verify_firmware_package`: Memvalidasi integritas digest SHA-256 dan keabsahan tanda tangan kriptografis sebelum biner diizinkan ditulis ke flash.
   - `flash_ota_update`: Menulis biner ke bank pasif (`app1` jika sedang aktif di `app0`, atau sebaliknya) dan mengalihkan status ke `PENDING_VERIFY`.
   - `simulate_boot`: Menyimulasikan siklus booting bootloader. Melacak jumlah reboot berturut-turut pada status `PENDING_VERIFY`.
   - `confirm_firmware_health`: Mengesahkan status partisi menjadi `VALID` permanen dan mereset penghitung bootloop.
   - `_trigger_automatic_rollback`: Menandai bank gagal sebagai `INVALID` dan secara otomatis mengembalikan penunjuk bootloader ke bank stabil sebelumnya.

## Eksekusi Pengujian

Jalankan pengujian simulator OTA dan automatic rollback langsung dari terminal:

```bash
python public/content/chapter-29/src/ota_lifecycle_simulator.py
```

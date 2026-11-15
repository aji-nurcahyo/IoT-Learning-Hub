# Panduan Implementasi Kode — Chapter 21

Dokumentasi ini menjelaskan arsitektur dan cara kerja modul [`data_models_validator.py`](content/chapter-21/src/data_models_validator.py).

## Struktur Program

Skrip disusun dalam empat bagian utama tanpa dependensi pustaka luar:

1. **Definisi Kontrak Skema**:
   - `TELEMETRY_SCHEMA`: Menetapkan struktur payload telemetri dengan field wajib `v` (skema versi 1), `dev`, `seq`, `ts`, dan sub-objek `metrics` (`temp_c`, `humidity_pct`, `battery_mv`, `rssi_dbm`).
   - `EVENT_SCHEMA`: Menetapkan struktur notifikasi diskrit asinkron lengkap dengan tingkat keparahan (*severity* `info`, `warning`, `critical`).
   - `COMMAND_SCHEMA`: Menetapkan kontrak instruksi kontrol jarak jauh dengan parameter kedaluwarsa `expiry_ts`.
2. **Mesin Validasi Skema (`validate_payload`)**:
   - Menelusuri pohon data JSON secara rekursif.
   - Memeriksa kelengkapan atribut wajib (*required*).
   - Menegakkan batasan tipe data primitif (`integer`, `number`, `string`, `object`).
   - Memvalidasi batas rentang numerik (`minimum`, `maximum`) dan panjang teks (`minLength`, `maxLength`).
3. **Pipeline De-duplikasi Idempotensi (`IdempotencyDeduplicator`)**:
   - Memelihara tabel hash `seen` yang memetakan `device_id:message_id` terhadap stempel waktu kedatangan.
   - Mengimplementasikan penghapusan entri kadaluwarsa (*TTL eviction*) untuk mencegah kebocoran memori.
4. **Analisis Efisiensi Serialisasi (`benchmark_payload_encodings`)**:
   - Mengomparasi ukuran representasi data dalam bentuk Pretty JSON, Minified JSON, dan Packed Binary menggunakan modul Python `struct` (`!B16sIIhHHb`).

## Cara Menjalankan

Eksekusi skrip pengujian langsung dari terminal proyek:

```bash
python public/content/chapter-21/src/data_models_validator.py
```

# Bukti Pengujian & Hasil Eksekusi — Chapter 21

Pengujian modul validasi skema data, pipeline deduplikasi idempotensi, dan efisiensi serialisasi dieksekusi menggunakan lingkungan runtime Python 3 pada platform simulasi/verifikasi lokal.

## Perintah Eksekusi

```bash
python public/content/chapter-21/src/data_models_validator.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== IoT Data Models & Schema Verification Suite ===
Test 1 - Valid Telemetry Validation: PASSED
Test 2 - Malformed Telemetry Rejection: PASSED (Tertolak 5 pelanggaran skema)
   [Expected Error] root.dev: panjang string 2 < minLength 3
   [Expected Error] root.seq: nilai -5 < minimum 0
   [Expected Error] root.ts: nilai 1600000000 < minimum 1700000000
   [Expected Error] root.metrics.temp_c: nilai 125.0 > maximum 85.0
   [Expected Error] root.metrics.humidity_pct: diharapkan number, diperoleh str
Test 3 - Valid Event Payload: PASSED
Test 4 - Valid Command Payload: PASSED

=== Idempotency Pipeline Test ===
   Message 101 First Arrival: Duplicate? False (Expected: False)
   Message 101 Resend in TTL: Duplicate? True (Expected: True)
   Message 102 New Message:   Duplicate? False (Expected: False)
   Message 101 After Expiry:  Duplicate? False (Expected: False)

=== Encoding Efficiency Benchmark ===
   Raw Pretty JSON  : 209 bytes
   Minified JSON    : 157 bytes
   Packed Binary    : 32 bytes
   Savings vs Raw   : 84.69%
   Savings vs Min   : 79.62%

Verification suite completed successfully.
```

## Analisis Hasil

1. **Integritas Skema**: Validator berhasil meloloskan paket telemetri valid dan menolak paket malformed dengan menangkap secara akurat 5 pelanggaran aturan (panjang string, batas bawah sekuens, batas minimal waktu epoch, pelanggaran batas maksimal sensor suhu, dan ketidaksesuaian tipe data).
2. **Keandalan De-duplikasi**: Paket dengan identitas yang sama dalam jendela TTL $10\text{ detik}$ berhasil dideteksi sebagai duplikat, sedangkan pesan baru dan pesan setelah batas waktu kedaluwarsa diproses secara normal.
3. **Efisiensi Payload**: Teknik binary struct packing terbukti mampu memangkas volume payload dari $209\text{ byte}$ menjadi $32\text{ byte}$ (penghematan $84{,}69\%$).

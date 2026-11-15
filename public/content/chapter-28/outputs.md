# Bukti Pengujian & Hasil Eksekusi — Chapter 28

Pengujian validasi sertifikat identitas X.509, penegakan matriks otorisasi Access Control List (ACL) MQTT, dan pemindaian ancaman STRIDE dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-28/src/iot_security_evaluator.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== IoT Security, TLS X.509 & MQTT ACL Verification Suite ===
Test 1 - Valid ECC P-256 Certificate: PASSED (Sertifikat valid dan memenuhi standar kriptografi modern.)
Test 2 - Expired Certificate Rejection: PASSED (Tertolak: Sertifikat telah kedaluwarsa (Kedaluwarsa pada 1762822790.0))
Test 3 - Weak 1024-bit RSA Rejection: PASSED (Tertolak: Panjang kunci RSA 1024 bit < minimum 2048 bit!)

=== MQTT Topic ACL Matrix Authorization Tests ===
Test 4a - Self Telemetry Publish: Allowed? True (Expected: True)
Test 4b - Cross-Device Telemetry Read: Allowed? False (Expected: False - Eavesdropping Dicegah)
Test 4c - Cross-Device Command Hijack: Allowed? False (Expected: False - Sabotase Dicegah)
Test 4d - Admin Multi-Tenant Access: Allowed? True (Expected: True)

=== STRIDE Threat Modeling Evaluation ===
Analisis Payload Tidak Aman: Ditemukan 3 ancaman:
   [Warning] [STRIDE: Spoofing] Payload tidak memuat identitas pengirim (dev).
   [Warning] [STRIDE: Tampering] Tidak ada nomor sekuens atau tanda tangan untuk validasi integritas.
   [Warning] [STRIDE: Info Disclosure] Terdeteksi atribut sensitif 'password' terkirim dalam payload!

Seluruh pengujian keamanan IoT, sertifikat TLS, dan ACL berhasil diselesaikan.
```

## Analisis Hasil

1. **Integritas Sertifikat Digital**: Sertifikat dengan algoritma kurva eliptik modern ECC P-256 berhasil lolos validasi. Sebaliknya, sertifikat yang melampaui masa aktif dan sertifikat dengan panjang kunci RSA lemah (1024-bit) berhasil ditolak secara deterministik.
2. **Penegakan Matriks ACL**: Percobaan penerbitan telemetri ke topik sendiri (`iot/fleet/node-env-01/telemetry`) disetujui. Namun, upaya penyadapan telemetri perangkat lain (`node-env-02`) dan upaya pembajakan perintah aktuator lintas perangkat ditolak secara mutlak oleh mesin ACL.
3. **Deteksi Kerentanan STRIDE**: Pemindai otomatis berhasil mengidentifikasi 3 celah keamanan kritis pada payload uji: ketiadaan identitas node (potensi pemalsuan/spoofing), ketiadaan pelindung urutan (potensi manipulasi/tampering), dan kebocoran kredensial plaintext (pelanggaran kerahasiaan informasi).

# Panduan Implementasi Kode — Chapter 28

Dokumentasi ini menjelaskan konfigurasi ACL pada [`mosquitto_acl.conf`](content/chapter-28/src/mosquitto_acl.conf) dan modul evaluasi keamanan siber pada [`iot_security_evaluator.py`](content/chapter-28/src/iot_security_evaluator.py).

## Konfigurasi Mosquitto ACL

Berkas `mosquitto_acl.conf` menetapkan aturan keamanan tingkat broker:
1. `allow_anonymous false`: Menonaktifkan koneksi tanpa otentikasi.
2. `pattern write iot/fleet/%u/telemetry`: Hanya mengizinkan perangkat mempublikasikan data ke topik yang mencocokkan identitas pengguna (`%u`) miliknya sendiri.
3. `pattern read iot/fleet/%u/cmd/+`: Hanya mengizinkan perangkat mendengarkan perintah kontrol yang ditargetkan langsung kepadanya.
4. `user operator_admin`: Memberikan hak baca/tulis penuh (`topic readwrite #`) khusus untuk akun pengawas sistem.

## Modul Evaluasi Kriptografis (`iot_security_evaluator.py`)

1. **Kelas `X509CertMock`**:
   - Memeriksa batas waktu `current_time >= not_before` dan `current_time <= not_after`.
   - Memastikan kunci kurva eliptik ECC memiliki panjang minimal 256 bit atau kunci RSA memiliki panjang minimal 2048 bit.
2. **Kelas `MqttAclEngine`**:
   - Menerapkan fungsi `authorize(username, action, target_topic)` yang mencocokkan topik aktual dengan pola aturan menggunakan penggantian variabel `%u` dan evaluasi wildcard `+` serta `#`.
3. **Fungsi `evaluate_stride_security`**:
   - Memindai keberadaan atribut `dev` (Spoofing).
   - Memindai kehadiran penanda integritas `seq` atau `sig` (Tampering).
   - Mendeteksi kata kunci sensitif plaintext seperti `password`, `secret`, `token` (Information Disclosure).
   - Memeriksa batas ukuran payload memori stack embedded (Denial of Service).

## Eksekusi Pengujian

Jalankan pengujian keamanan dan verifikasi ACL langsung dari terminal:

```bash
python public/content/chapter-28/src/iot_security_evaluator.py
```

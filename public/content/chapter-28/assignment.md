# Tugas Mandiri: Audit Keamanan IoT, Evaluasi X.509 PKI & Matriks MQTT ACL

## Deskripsi Tugas

Tugas ini melatih mahasiswa mengevaluasi dan menegakkan standar keamanan siber enterprise pada infrastruktur perangkat terhubung (*IoT Cybersecurity*). Anda diminta untuk mengimplementasikan modul validator sertifikat digital X.509, membangun mesin penegak Access Control List (ACL) pada broker MQTT berbasis pola isolasi pengguna, serta melakukan pemindaian kerentanan payload menggunakan kerangka kerja pemodelan ancaman STRIDE.

## Petunjuk Pengerjaan

1. **Evaluasi Sertifikat Kriptografis X.509**:
   - Susun kelas `X509CertMock` yang memverifikasi rentang masa aktif sertifikat (`not_before` dan `not_after`) serta memastikan kepatuhan panjang kunci kriptografi modern (ECC NIST P-256 atau RSA $\ge 2048\text{ bit}$).
   - Uji penolakan otomatis terhadap sertifikat yang telah kedaluwarsa atau menggunakan kunci lemah.
2. **Mesin Penegak Matriks Otorisasi MQTT ACL**:
   - Bangun kelas `MqttAclEngine` yang memuat aturan hak akses berbasis pola `%u` dari spesifikasi [`mosquitto_acl.conf`](content/chapter-28/src/mosquitto_acl.conf).
   - Validasi empat skenario otorisasi kritis:
     - Izin tulis telemetri ke topik perangkat sendiri (*Self Publish*).
     - Pemblokiran izin baca terhadap telemetri perangkat lain (*Anti-Eavesdropping*).
     - Pemblokiran izin suntik perintah ke perangkat lain (*Anti-Spoofing / Anti-Sabotage*).
     - Izin supervisi penuh bagi akun administrator (`operator_admin`).
3. **Pemodelan Ancaman STRIDE Otomatis**:
   - Implementasikan fungsi `evaluate_stride_security` yang memindai struktur payload telemetri untuk mendeteksi potensi pemalsuan identitas (*Spoofing*), ketiadaan integritas urutan (*Tampering*), dan kebocoran rahasia plaintext (*Information Disclosure*).
4. **Verifikasi dan Dokumentasi**:
   - Jalankan skrip pengujian mandiri [`iot_security_evaluator.py`](content/chapter-28/src/iot_security_evaluator.py) dan dokumentasikan log hasil eksekusi terminal secara lengkap.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Validasi Sertifikat PKI & Kriptografi** | 35% | Logika evaluasi masa berlaku dan kekuatan kunci akurat; sertifikat usang dan kunci RSA lemah berhasil ditolak secara konsisten. |
| **Penegakan Matriks Otorisasi MQTT ACL** | 35% | Logika pencocokan pola topik `%u` dan wildcard berfungsi tepat; akses lintas perangkat tidak sah berhasil diblokir secara tegas. |
| **Pemodelan Ancaman STRIDE & Dokumentasi** | 30% | Pemindai mendeteksi kerentanan payload tidak aman; berkas konfigurasi ACL terstruktur rapi dan mematuhi kaidah NIST IR 8259. |

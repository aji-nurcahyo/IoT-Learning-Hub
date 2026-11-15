# Latihan Soal & Praktik — Chapter 28

## Bagian A — Soal Konseptual

1. **Pemodelan STRIDE**:
   Pada sebuah sistem pemantauan tangki bahan bakar pintar, seorang penyerang berhasil memasang perangkat pemancar radio tiruan di pagar fasilitas dan memancarkan data level bensin konstan $90\%$ ke broker MQTT yang tidak terproteksi.
   - Identifikasi kategori ancaman STRIDE yang dilancarkan penyerang.
   - Jelaskan dua mekanisme pertahanan kriptografis yang mampu menggagalkan serangan tersebut secara tuntas.
2. **Karakteristik Mutual TLS (mTLS)**:
   Jelaskan perbedaan mendasar antara *Server Authentication TLS* (seperti saat Anda mengunjungi situs perbankan di peramban web) dengan *Mutual TLS (mTLS)* yang diterapkan pada sistem perangkat IoT industri. Mengapa otentikasi satu arah belum memadai untuk komunikasi mikrokontroler-ke-broker?
3. **Prinsip Least Privilege pada Topik MQTT**:
   Jika sebuah aturan ACL mengizinkan seluruh sensor menulis ke topik `iot/fleet/+/telemetry`, jelaskan bahaya peretasan yang timbul jika satu sensor berhasil dibongkar dan penyerang mengekstrak kredensialnya. Bagaimana aturan berbasis pola `iot/fleet/%u/telemetry` mengatasi celah tersebut?

## Bagian B — Soal Praktik Komputasi

1. **Uji Matriks ACL Kustom**:
   Menggunakan kelas `MqttAclEngine` pada skrip [`iot_security_evaluator.py`](content/chapter-28/src/iot_security_evaluator.py), tambahkan satu aturan hak akses baru:
   - Pengguna dengan peran `maintenance_tech` diizinkan membaca (`read`) seluruh topik telemetri `iot/fleet/+/telemetry`, namun dilarang menulis (`write`) ke topik perintah `iot/fleet/+/cmd/+`.
   - Uji aturan tersebut dan pastikan pengujian otorisasi mengembalikan nilai `True` untuk baca telemetri dan `False` untuk eksekusi perintah.
2. **Analisis Kerentanan Payload**:
   Jalankan fungsi `evaluate_stride_security` dengan payload berikut:
   `{"dev": "sensor-99", "temp": 28.5, "api_token": "bearer-xyz-12345"}`
   Amati pesan peringatan yang dihasilkan dan jelaskan perbaikan struktur data yang harus dilakukan.

# Latihan Terstruktur: Modul A03

## Latihan Pemahaman Mandiri

1. **Apa perbedaan mendasar antara pembentukan sesi aman PASE dan CASE pada standar Matter?**
   - *Jawaban*: PASE (*Passcode-Authenticated Session Establishment*) menggunakan passcode setup 8-digit dengan algoritma SPAKE2+ untuk onboarding perangkat baru yang belum terdaftar di jaringan, sedangkan CASE (*Certificate-Authenticated Session Establishment*) menggunakan sertifikat operasional PKI X.509 (*Node Operational Certificate* / NOC) untuk komunikasi terenkripsi antar-node yang sudah tergabung di dalam Fabric jaringan.

2. **Mengapa protokol Thread tidak memerlukan koordinator pusat tunggal yang menjadi single point of failure (seperti pada Zigbee konvensional)?**
   - *Jawaban*: Thread menerapkan arsitektur *self-healing* terdesentralisasi. Jika simpul yang bertindak sebagai *Leader* mengalami kegagalan daya, salah satu simpul *Router* yang aktif akan secara otomatis dipromosikan menjadi Leader baru melalui konsensus internal tanpa merusak topologi jaringan mesh.

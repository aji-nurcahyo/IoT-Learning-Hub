# Tugas Terbimbing: Rancang Bangun Harness Injeksi Gangguan & Pengukuran Keandalan IoT

## Deskripsi Tugas

Dalam tugas ini, Anda diminta membangun modul pengujian berbasis penyuntikan kesalahan terkontrol (*Fault Injection Test Harness*) untuk memverifikasi ketahanan klien telemetri IoT terhadap kegagalan jaringan berkala dan fluktuasi catu daya listrik (*brownout*), serta mengukur metrik keandalan sistem industri.

Tugas ini mewajibkan:
1. Pemodelan klien telemetri IoT yang memiliki mekanisme penyimpanan lokal *Store-and-Forward Ring-Buffer* untuk mempertahankan paket data saat jaringan internet padam.
2. Pengujian otomatis yang menyuntikkan kegagalan paket data jaringan selama beberapa siklus dan membuktikan bahwa seluruh paket yang tertahan berhasil dikuras tanpa ada data yang hilang saat koneksi pulih.
3. Penyuntikan gangguan tegangan *brownout* untuk memverifikasi transisi status pemulihan otonom mikrokontroler pasca-reboot.
4. Perhitungan kuantitatif metrik keandalan operasional: *Mean Time Between Failures* (MTBF), *Mean Time To Repair* (MTTR), dan persentase ketersediaan (*Availability*).

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-38/src/fault_injection_harness.py`.
2. Laporan analisis teknis yang mencakup tabel trace eksekusi pengujian, analisis status transisi siklus kegagalan, dan formulasi matematis metrik keandalan sistem.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Model Injeksi Gangguan & Retensi Buffer** | 35 Poin | Mekanisme *store-and-forward* terbukti menahan data saat jaringan padam, pengurasan data berurutan berhasil saat jaringan pulih, dan nol kehilangan rekaman data. |
| **Penanganan Brownout & Transisi Status Pemulihan** | 35 Poin | Klien merespon kondisi *brownout* secara tepat, membedakan memori persisten vs memori volatil, dan memulihkan status operasional pasca-reboot secara otonom. |
| **Kuantifikasi Metrik Keandalan MTBF, MTTR & Availability** | 30 Poin | Perhitungan metrik keandalan matematis terbukti akurat, analisis mencakup pemenuhan target ketersediaan industri, dan evaluasi matriks risiko FMEA dibahas tuntas. |

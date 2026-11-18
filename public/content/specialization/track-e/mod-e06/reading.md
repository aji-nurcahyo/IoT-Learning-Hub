# Modul E06 — City-Scale Multi-Tenant IoT Platform & Telecommunications Integration Capstone

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Merancang dan memvalidasi platform IoT kota cerdas terdistribusi yang mampu menelan beban stres 12.000 paket/detik tanpa kehilangan paket (SATC-E01).
2. Mengimplementasikan antrean prioritas non-preemptive M/G/1 untuk menjamin latensi peringatan bencana darurat < 80 ms (SATC-E02).
3. Menegakkan kedaulatan data multi-tenant dengan isolasi kriptografis lintas dinas (PUPR, Kebersihan, BPBD) dan respon 403 Forbidden terbukti (SATC-E03).
4. Mengintegrasikan pipeline geofencing spasial dengan formula Haversine WGS84, ray-casting alert < 100 ms, dan agregasi heksagonal H3 untuk perlindungan privasi publik (SATC-E04).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 11, Chapter 21, Chapter 23, Chapter 25, Chapter 30, Chapter 40.
- Modul Jalur Peminatan Prasyarat: Modul E01, Modul E02, Modul E03, Modul E04, Modul E05.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Visi Integrasi Platform IoT Skala Metropolitan
Platform IoT perkotaan modern bukan sekadar dashboard visualisasi, melainkan sistem operasi terdistribusi (*Urban Operating System*) yang menghubungkan puluhan juta interaksi harian masyarakat, utilitas, dan layanan darurat.

Proyek Capstone Track E menggabungkan seluruh disiplin telekomunikasi dan komputasi perkotaan ke dalam arsitektur terpadu:
1. **Standar Ontologi Semantik FIWARE NGSI-LD (ETSI GS CIM 009)**:
   Menyatukan format data sensor banjir (PUPR), sensor armada sampah (DLH), dan alarm darurat (BPBD) dengan skema entitas terstandarisasi.
2. **Kedaulatan & Keamanan Data Multi-Tenant**:
   Mencegah kebocoran data rahasia utilitas atau peretasan lintas dinas dengan penegakan otorisasi token kriptografis ketat (*Zero-Trust Municipal Architecture*).
3. **Rekayasa Kualitas Layanan (QoS) & Kontensi Kanal**:
   Menjamin paket darurat keselamatan publik tidak tertelan antrean telemetri rutin jutaan meteran air perkotaan.
4. **Analitik Geospasial & Perlindungan Privasi Warga**:
   Memungkinkan pusat kendali mendeteksi pelanggaran zona bahaya secara real-time sekaligus melindungi privasi pengemudi publik dengan masking spasial heksagonal H3.

### 2. Validasi Kriteria Keberimaan Sistem (Acceptance Criteria)

- **SATC-E01 (Throughput Ingestion)**:
  Kapasitas penyerapan beban minimum 12.000 paket/detik dengan probabilitas paket hilang nol ($P_{\text{drop}} = 0$).
- **SATC-E02 (Latency SLA Antrean Prioritas M/G/1)**:
  $$
  W_1 = \frac{R}{1 - \rho_1} + E[X] < 80\text{ ms}
  $$
  dengan utilisasi total sistem $\rho \ge 0{,}80$.
- **SATC-E03 (Isolasi Multi-Tenant)**:
  Akses cross-tenant tanpa otorisasi wajib menghasilkan respon `403 Forbidden` tanpa kebocoran payload.
- **SATC-E04 (Deteksi Geofence & Kepatuhan Privasi)**:
  Algoritma Ray-Casting mendeteksi pelanggaran poligon dengan waktu komputasi $< 100\text{ ms}$ dan masking koordinat GPS ke dalam sel heksagonal Uber H3 Resolution 8.

## Latihan

## Latihan Pemahaman Mandiri

1. **Strategi Pemulihan Gateway Down**:
   - *Soal*: Jika satu tower seluler kota mati total akibat putusnya pasokan listrik, bagaimana arsitektur redundansi multi-gateway dan LPWAN perkotaan menjamin data sensor kritis tetap sampai ke markas komando?
   - *Jawaban*: Simpul IoT perkotaan berada dalam jangkauan sel tumpang tindih (*overlapping coverage*). Ketika base station primer mati, simpul secara otomatis melakukan retransmisi ke frekuensi alternatif atau gateway sekunder yang mendengarkan kanal bersama. Dengan model ketersediaan paralel komposit $A = 1 - \prod(1 - A_i)$, ketersediaan tautan tetap terjaga di atas 99.9%.

2. **Dampak Masking Privasi H3**:
   - *Soal*: Apakah masking spasial H3 mengurangi efektivitas deteksi dini banjir kota? Jelaskan trade-off teknologinya.
   - *Jawaban*: Tidak. Sensor debit air dan pintu air adalah aset fisik statis milik dinas (bukan individu personal), sehingga koordinat presisi tetap tersimpan di database internal tertutup (akses PUPR). Masking H3 hanya diterapkan pada portal Open Data publik yang diakses masyarakat luas untuk memantau tren genangan tingkat distrik tanpa membuka detail instalasi infrastruktur vital kepada pihak yang tidak berkepentingan.

## Tugas

## Penugasan Mandiri: Audit Kesiapan Produksi Platform Smart City

1. Kembangkan rencana deployment Docker Compose untuk platform kota cerdas yang mengintegrasikan Orion-LD Context Broker, MongoDB backend, Mosquitto MQTT broker, dan dashboard GIS.
2. Buat skenario pengujian penetrasi keamanan (penetration testing) untuk memverifikasi isolasi token multi-tenant antar-dinas.
3. Rancang rencana mitigasi bencana (*Disaster Recovery Plan*) untuk command center kota dengan target RPO (Recovery Point Objective) < 1 menit dan RTO (Recovery Time Objective) < 15 menit.
4. Susun laporan rekayasa komprehensif yang siap dipresentasikan kepada pimpinan dinas kominfo kota.

## Ringkasan
- Modul E06 memberikan pemahaman mendalam dan terapan mengenai City-Scale Multi-Tenant IoT Platform & Telecommunications Integration Capstone pada tingkat kedalaman L3: Advanced / Capstone Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [city_scale_capstone_platform.py](src/city_scale_capstone_platform.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. FIWARE Foundation - NGSI-LD Specification & Architecture Guide, [https://www.fiware.org/developers/catalogue/](https://www.fiware.org/developers/catalogue/) (diperiksa 2026-11-18).
2. ETSI GS CIM 009 - Context Information Management (CIM); NGSI-LD API, [https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.06.01_60/gs_cim009v010601p.pdf](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.06.01_60/gs_cim009v010601p.pdf) (diperiksa 2026-11-18).
3. Smart Data Models Initiative - Cross-domain Smart City Entities, [https://smartdatamodels.org/](https://smartdatamodels.org/) (diperiksa 2026-11-18).

# Modul E01 — Smart City IoT Systems Engineering, Urban Topologies & Municipal Architecture

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Merancang topologi komunikasi data perkotaan bertingkat (Field Node -> Edge Aggregator -> Municipal Cloud Command Center).
2. Mengimplementasikan representasi entitas data terstandar FIWARE NGSI-LD (Smart Data Models) dengan validasi skema JSON-LD.
3. Menerapkan isolasi multi-tenant berbasis token kriptografis dan Access Control List (ACL) lintas dinas kota.
4. Menghitung probabilitas ketersediaan sistem jaringan perkotaan dengan model redundansi gateway paralel.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 01, Chapter 02, Chapter 11.
- Modul Jalur Peminatan Prasyarat: Tidak ada (modul awal jalur peminatan).
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Visi Arsitektur Sistem IoT Skala Metropolitan
Kota cerdas modern mengintegrasikan jutaan instrumen fisik yang tersebar di wilayah geografis ratusan kilometer persegi: sistem penerangan jalan umum cerdas (PJU), sensor kualitas udara distrik, meteran air dan listrik utilitas publik, sistem deteksi dini banjir di kanal perkotaan, hingga pelacakan armada transportasi publik.

Membangun infrastruktur silang independen untuk masing-masing dinas pemerintah daerah (Dinas PUPR, Dinas Perhubungan, Dinas Kebersihan, dan BPBD) menimbulkan duplikasi biaya modal dan operasional yang masif. Diperlukan arsitektur sistem bersama (*shared municipal platform*) yang mampu mengagregasi data heterogen secara efisien dengan kedaulatan tata kelola multi-tenant yang ketat.

### 2. Standar Ontologi Konteks FIWARE NGSI-LD (ETSI GS CIM 009)
Untuk mencegah silo data antar-aplikasi kota, European Telecommunications Standards Institute (ETSI) bersama konsorsium FIWARE menetapkan standar pertukaran data konteks **NGSI-LD** (*Next Generation Service Interfaces with Linked Data*):
- **Struktur Entitas Universal**: Setiap objek fisik dimodelkan sebagai *Entity* dengan identitas unik berformat URN ("urn:ngsi-ld:<Type>:<ID>").
- **Property & Relationship**: Nilai pembacaan sensor dimodelkan sebagai "Property" dengan metadata stempel waktu pengamatan "observedAt", sedangkan keterkaitan spasial antar-aset dimodelkan sebagai "Relationship".
- **Linked Data Context ("@context")**: Memetakan atribut lokal ke ontologi semantik global standar W3C JSON-LD, memastikan nama variabel memiliki definisi semantik yang seragam dan dapat dipahami secara mesin oleh seluruh dinas kota.

### 3. Ketersediaan Jaringan Redundansi Multi-Gateway
Pada area perkebunan atau pedesaan, kegagalan satu gateway LoRaWAN dapat memutus komunikasi area lokal. Namun di lingkungan metropolitan, topologi seluler dan LPWAN dirancang dengan prinsip tumpang tindih redundan (*overlapping cell coverage*):
- Jika sebuah simpul meteran air kota berada dalam jangkauan $N$ gateway independen yang masing-masing memiliki probabilitas ketersediaan tautan $A_{	ext{gw}}$, probabilitas ketersediaan sistem komposit kota ($A_{	ext{city}}$) dirumuskan:
$$
A_{	ext{city}} = 1 - prod_{i=1}^{N} (1 - A_{	ext{gw}, i})
$$
Dengan menempatkan 4 gateway paralel bertingkat reliabilitas $90%$, ketersediaan sistem melonjak drastis mencapai standar *Four-Nines* ($99{,}99%$).

### 4. Landasan Matematis: Model Keandalan Paralel & Multi-Tenant Access Matrix

1. **Persamaan Ketersediaan Sistem Paralel Redundan**:
   $$
   U_{	ext{total}} = prod_{i=1}^{N} (1 - A_i) implies A_{	ext{composite}} = 1 - U_{	ext{total}}
   $$
   di mana $U_{	ext{total}}$ adalah probabilitas kegagalan simultan seluruh gateway.

2. **Worked Numerical Example (Kasus Redundansi Gateway Distrik Kota)**:
   - **Kondisi Lapangan**: Distrik kota dipayungi oleh $N = 4$ unit gateway LoRaWAN/seluler paralel. Masing-masing gateway memiliki ketersediaan tautan operasional individual $A_i = 0{,}90$ ($90%$).
   - **Langkah 1: Perhitungan Unavailability Tiap Gateway**:
     $$
     U_i = 1 - A_i = 1 - 0{,}90 = 0{,}10 quad (10%)
     $$
   - **Langkah 2: Probabilitas Kegagalan Simultan Seluruh 4 Gateway**:
     $$
     U_{	ext{total}} = U_1 	imes U_2 	imes U_3 	imes U_4 = (0{,}10)^4 = 0{,}0001 quad (0{,}01%)
     $$
   - **Langkah 3: Ketersediaan Efektif Komposit ($A_{	ext{city}}$)**:
     $$
     A_{	ext{city}} = 1 - 0{,}0001 = 0{,}9999 quad (99{,}99%)
     $$
   *Interpretasi Rekayasa*: Meskipun masing-masing gateway hanya memiliki ketersediaan individual $90%$ (downtime kumulatif 36,5 hari per tahun), arsitektur paralel 4 gateway menghasilkan ketersediaan Four-Nines ($99{,}99%$) dengan total downtime hanya **52,6 menit per tahun**, memenuhi syarat SLA layanan publik kritis.

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa standar ontologi data terhubung (Linked Data / JSON-LD) seperti FIWARE NGSI-LD sangat penting dalam integrasi sistem IoT perkotaan?**
   - *Jawaban*: Dalam lingkungan kota yang kompleks, dinas-dinas yang berbeda menggunakan vendor perangkat keras yang heterogen dengan format JSON acak yang berbeda nama field-nya. JSON-LD menyematkan konteks semantik global ("@context") yang secara presisi mendefinisikan arti setiap properti, memungkinkan sistem analitik lintas dinas memproses dan menghubungkan data tanpa perlu menulis ulang adaptor konversi untuk setiap vendor baru.

2. **Bagaimana arsitektur 4 gateway paralel dengan reliabilitas individual 90% mampu menghasilkan ketersediaan komposit Four-Nines (99.99%)?**
   - *Jawaban*: Melalui prinsip redundansi independen: paket data yang dipancarkan oleh simpul sensor akan diterima jika minimal salah satu dari 4 gateway beroperasi. Peluang sistem gagal total adalah probabilitas keempat gateway mati secara serentak, yaitu $(1 - 0{,}9)^4 = 0{,}1^4 = 0{,}0001$. Ketersediaan sistem adalah komplemennya: $1 - 0{,}0001 = 0{,}9999$ ($99{,}99%$).

## Tugas

## Penugasan Mandiri: Pemodelan Entitas NGSI-LD & Audit Multi-Tenant

Rancang skema entitas NGSI-LD lengkap untuk sistem pemantauan kualitas udara kota (tipe *AirQualityObserved*). Kembangkan modul Python yang memvalidasi integritas data dan menguji bahwa pengguna tenant eksternal tanpa hak akses ditolak dengan status HTTP 403 Forbidden.

## Ringkasan
- Modul E01 memberikan pemahaman mendalam dan terapan mengenai Smart City IoT Systems Engineering, Urban Topologies & Municipal Architecture pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [smart_city_ngsild_multitenant_sim.py](src/smart_city_ngsild_multitenant_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. ETSI GS CIM 009 V1.6.1, Context Information Management (CIM); NGSI-LD API, 2022, [https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.06.01_60/gs_cim009v010601p.pdf](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.06.01_60/gs_cim009v010601p.pdf) (diperiksa 2026-11-18).
2. ITU-T Recommendation Y.4200, Requirements for IoT smart city platforms, 2018, [https://www.itu.int/rec/T-REC-Y.4200-201802-I/en](https://www.itu.int/rec/T-REC-Y.4200-201802-I/en) (diperiksa 2026-11-18).

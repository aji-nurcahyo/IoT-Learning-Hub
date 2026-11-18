import fs from 'node:fs';
import path from 'node:path';

interface ChapterTarget {
  slug: string;
  targetBefore: string;
  mathContent: string;
  extraReferences?: string[];
}

const targets: ChapterTarget[] = [
  {
    slug: 'chapter-22',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Buffer Dimensioning & Latensi Pemrosesan Gateway (Mathematical Foundations)

Sebagai jembatan antara bus sensor fisik dan infrastruktur IP, gateway bertindak sebagai sistem antrean $M/M/1$:

1. **Pemodelan Antrean Gateway (Queueing Model)**:
   Jika kedatangan paket dari simpul sensor memiliki laju rata-rata $\\lambda$ (paket/detik) berdistribusi Poisson, dan laju layanan transmisi gateway ke broker cloud adalah $\\mu$ (paket/detik) dengan syarat kestabilan $\\rho = \\frac{\\lambda}{\\mu} < 1$:
   - Jumlah rata-rata paket dalam antrean buffer gateway $L_q$ adalah:
     $$
     L_q = \\frac{\\rho^2}{1 - \\rho} = \\frac{\\lambda^2}{\\mu(\\mu - \\lambda)}
     $$
   - Waktu tunggu rata-rata paket di gateway sebelum terkirim $W$ dirumuskan menurut Teorema Little:
     $$
     W = \\frac{1}{\\mu - \\lambda}
     $$

2. **Perhitungan Waktu Tunggu Gateway Terhadap Utilitas (Worked Example)**:
   Sebuah gateway mengumpulkan data dari 50 sensor dengan total laju kedatangan $\\lambda = 80\\text{ paket/detik}$. Kapasitas pemrosesan dan enkapsulasi JSON gateway mencapai $\\mu = 100\\text{ paket/detik}$.
   Faktor utilitas gateway $\\rho$ adalah:
   $$
   \\rho = \\frac{80}{100} = 0{,}80 \\quad (80\\%)
   $$
   Waktu tinggal rata-rata paket di gateway:
   $$
   W = \\frac{1}{100 - 80} = \\frac{1}{20} = 0{,}05\\text{ detik } (50\\text{ ms})
   $$
   Jika koneksi internet mengalami degradasi sehingga laju pengiriman turun menjadi $\\mu' = 85\\text{ paket/detik}$ (utilitas melonjak ke $\\rho = 0{,}941$), maka waktu tunggu rata-rata melonjak drastis menjadi $W' = \\frac{1}{85 - 80} = 0{,}20\\text{ detik}$ ($200\\text{ ms}$). Pemodelan ini membuktikan perlunya alokasi thread pool asinkron agar gateway tidak mengalami penumpukan antrean (*queue explosion*).
`,
    extraReferences: [
      '- Kleinrock, L., *Queueing Systems, Volume 1: Theory*, John Wiley & Sons, 1975.',
      '- POSIX.1-2017 / IEEE Std 1003.1-2017, *Standard for Information Technology—Portable Operating System Interface (POSIX)*.'
    ]
  },
  {
    slug: 'chapter-24',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Throughput Aliran Peristiwa & Latensi Pipeline Node-RED (Mathematical Foundations)

Pemrosesan berbasis aliran (*Flow-Based Programming*) pada Node-RED memproses pesan sebagai aliran peristiwa diskrit di atas event-loop single-threaded Node.js:

1. **Model Penjadwalan Event Loop & Waktu Eksekusi Fungsi**:
   Total latensi transit suatu pesan $T_{\\text{pipeline}}$ yang melewati rantai $K$ node fungsi dihitung sebagai:
   $$
   T_{\\text{pipeline}} = \\sum_{i=1}^{K} t_{\\text{exec},i} + \\sum_{i=1}^{K-1} t_{\\text{queue},i}
   $$
   di mana $t_{\\text{exec},i}$ adalah waktu eksekusi komputasi node ke-$i$ dan $t_{\\text{queue},i}$ adalah waktu tunggu di antrean mikro-task V8.

2. **Kapasitas Throughput Maksimum Pipeline (Worked Example)**:
   Sebuah flow Node-RED menerima pesan MQTT, memvalidasi skema JSON ($t_{\\text{exec},1} = 0{,}8\\text{ ms}$), mengevaluasi ambang batas alarm ($t_{\\text{exec},2} = 0{,}2\\text{ ms}$), dan memformat data untuk database ($t_{\\text{exec},3} = 0{,}5\\text{ ms}$). Total waktu eksekusi sinkron per pesan adalah:
   $$
   T_{\\text{sync}} = 0{,}8 + 0{,}2 + 0{,}5 = 1{,}5\\text{ ms}
   $$
   Throughput komputasi teoritis maksimum pipeline pada satu inti CPU adalah:
   $$
   \\text{Throughput}_{\\text{max}} = \\frac{1}{T_{\\text{sync}}} = \\frac{1}{1{,}5 \\times 10^{-3}\\text{ s}} \\approx 666{,}7\\text{ pesan/detik}
   $$
   Jika beban kedatangan telemetri melampaui 667 pesan/detik, latensi antrean $t_{\\text{queue}}$ akan meningkat tanpa batas (*starvation*), sehingga diperlukan partisi beban dengan kluster Node-RED atau pendelegasian pemrosesan berat ke worker thread.
`,
    extraReferences: [
      '- Morrison, J. P., *Flow-Based Programming: A New Approach to Application Development*, 2nd Edition, CreateSpace, 2010.',
      '- OpenJS Foundation, *Node-RED Programming Guide & Node Architecture*, Official Documentation.'
    ]
  },
  {
    slug: 'chapter-27',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Skalabilitas Registri & Interval Heartbeat Adaptif (Mathematical Foundations)

Pengelolaan armada perangkat IoT berskala besar (*fleet management*) membutuhkan optimasi interval detak jantung (*heartbeat*) untuk menyeimbangkan deteksi kegagalan simpul dan beban jaringan:

1. **Hubungan Waktu Deteksi Kegagalan vs Beban Jaringan**:
   Jika armada terdiri atas $N$ perangkat dengan interval heartbeat seragam $T_{\\text{hb}}$ detik dan ambang batas kegagalan dideklarasikan setelah $K$ heartbeat hilang berturut-turut:
   - Waktu deteksi node mati $T_{\\text{detect}}$ adalah:
     $$
     T_{\\text{detect}} = K \\cdot T_{\\text{hb}}
     $$
   - Total volume paket heartbeat yang masuk ke platform server per detik $\\Lambda_{\\text{hb}}$:
     $$
     \\Lambda_{\\text{hb}} = \\frac{N}{T_{\\text{hb}}}
     $$

2. **Optimasi Interval Heartbeat Armada 10.000 Node (Worked Example)**:
   Sebuah perusahaan mengelola armada $N = 10.000$ meteran pintar air.
   - Skenario A ($T_{\\text{hb}} = 10\\text{ s}$, $K=3$):
     $$
     T_{\\text{detect}} = 3 \\times 10 = 30\\text{ detik}, \\quad \\Lambda_{\\text{hb}} = \\frac{10.000}{10} = 1000\\text{ request/detik}
     $$
     Beban 1.000 req/s membutuhkan kluster server basis data berkapasitas tinggi.
   - Skenario B (Heartbeat Adaptif: $T_{\\text{hb}} = 300\\text{ s}$, $K=2$):
     $$
     T_{\\text{detect}} = 2 \\times 300 = 600\\text{ detik } (10\\text{ menit}), \\quad \\Lambda_{\\text{hb}} = \\frac{10.000}{300} \\approx 33{,}33\\text{ request/detik}
     $$
     Beban server berkurang hingga $96{,}7\\%$. Untuk aset non-kritis, pemilihan $T_{\\text{hb}} = 300\\text{ s}$ memberikan penghematan infrastruktur komputasi yang masif dengan tetap menjamin pelacakan inventaris yang akurat.
`,
    extraReferences: [
      '- NIST Special Publication 800-146, *Cloud Computing Synopsis and Recommendations*, National Institute of Standards and Technology.',
      '- ISO/IEC 30141:2018, *Internet of Things (IoT) — Reference Architecture*, International Organization for Standardization.'
    ]
  },
  {
    slug: 'chapter-28',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Kompleksitas Komputasi Kriptografi Elliptic Curve (ECDSA) (Mathematical Foundations)

Keamanan IoT modern mengandalkan kriptografi kurva eliptis (*Elliptic Curve Cryptography* / ECC) seperti kurva NIST P-256 (secp256r1) karena efisiensi panjang kunci yang jauh lebih ringkas dibanding RSA:

1. **Perbandingan Kekuatan Keamanan & Ukuran Kunci**:
   Tingkat keamanan $k$ bit simetris yang setara dirumuskan menurut rekomendasi NIST SP 800-57:
   - RSA-2048 memberikan kekuatan keamanan $\\approx 112\\text{ bit}$ simetris (panjang kunci publik: 256 byte).
   - RSA-3072 memberikan kekuatan keamanan $\\approx 128\\text{ bit}$ simetris (panjang kunci publik: 384 byte).
   - ECC P-256 memberikan kekuatan keamanan $\\approx 128\\text{ bit}$ simetris dengan panjang kunci publik hanya **64 byte** (atau 33 byte terkompresi).

2. **Beban Transmisi Handshake TLS (Worked Example)**:
   Sertifikat digital X.509 berbasis RSA-2048 memiliki ukuran tipikal $L_{\\text{cert,RSA}} \\approx 1800\\text{ byte}$, sedangkan sertifikat ECDSA P-256 hanya $L_{\\text{cert,ECC}} \\approx 650\\text{ byte}$.
   Pada mutual TLS (mTLS v1.3), kedua belah pihak mempertukarkan sertifikat (perangkat $\\leftrightarrow$ server). Penghematan byte selama negosiasi handshake adalah:
   $$
   \\Delta L_{\\text{handshake}} = 2 \\times (L_{\\text{cert,RSA}} - L_{\\text{cert,ECC}}) = 2 \\times (1800 - 650) = 2300\\text{ byte}
   $$
   Pengurangan lebih dari 2 KiB data transmisi pada setiap proses pembentukan sesi TLS memangkas konsumsi energi radio mikrokontroler hingga $\\approx 60\\%$, membuktikan keunggulan mutlak cipher-suite ECDSA (seperti \`TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\`) untuk sistem tertanam.
`,
    extraReferences: [
      '- NIST Special Publication 800-57 Part 1 Rev. 5, *Recommendation for Key Management*, NIST, 2020.',
      '- IETF RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*, Internet Engineering Task Force.'
    ]
  },
  {
    slug: 'chapter-29',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Probabilitas Kegagalan Flash & Model Pemulihan Rollback (Mathematical Foundations)

Mekanisme pembaruan firmware over-the-air (OTA) dirancang untuk memastikan perangkat tidak mengalami *bricking* meskipun terjadi gangguan transmisi atau galat firmware:

1. **Model Keandalan Transmisi OTA Multi-Blok**:
   Jika firmware berukuran $M$ byte dipecah menjadi $N_{\\text{block}} = \\lceil M / S_{\\text{block}} \\rceil$ blok independen, dan probabilitas integritas hash SHA-256 per blok berhasil adalah $q = (1 - p)$ di mana $p$ adalah packet error rate:
   $$
   P_{\\text{success}} = q^{N_{\\text{block}}} = (1 - p)^{N_{\\text{block}}}
   $$
   Untuk firmware sebesar 1 MiB ($M = 1.048.576\\text{ byte}$) dengan ukuran blok $S_{\\text{block}} = 4096\\text{ byte}$, terdapat $N_{\\text{block}} = 256$ blok. Jika $p = 0{,}001$ ($0{,}1\\%$ galat per blok):
   $$
   P_{\\text{success}} = (1 - 0{,}001)^{256} \\approx 0{,}774 \\quad (77{,}4\\%)
   $$
   Tanpa mekanisme pengulangan blok individual (*per-block retry*), lebih dari $22\\%$ proses unduh firmware akan gagal total.

2. **Analisis Waktu Timeout Watchdog & Rollback State Machine (Worked Example)**:
   Setelah partisi boot baru diaktifkan, firmware baru diberi waktu jendela evaluasi keselamatan $T_{\\text{window}} = 30\\text{ detik}$ untuk menghubungi server validasi dan mencatat status \`ESP_OTA_IMG_VALID\`. Jika dalam waktu $T_{\\text{window}}$ terjadi crash CPU (*panik/kernel fault*) atau koneksi server gagal:
   $$
   T_{\\text{rollback}} = T_{\\text{watchdog}} + T_{\\text{reboot}} \\approx 5{,}0\\text{ s} + 1{,}2\\text{ s} = 6{,}2\\text{ detik}
   $$
   Hardware RTC bootloader otomatis mengembalikan pointer boot ke partisi sebelumnya (Slot A), menjamin ketersediaan sistem tetap $100\\%$ pulih tanpa intervensi fisik teknisi ke lapangan.
`,
    extraReferences: [
      '- Espressif Systems, *Over-The-Air Updates (OTA) Architecture Guidelines*, ESP-IDF Programming Guide.',
      '- IEC 62443-4-2, *Security for industrial automation and control systems - Technical security requirements for IACS components*.'
    ]
  },
  {
    slug: 'chapter-30',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Ketersediaan Layanan Pipeline End-to-End & Analisis Latensi P99 (Mathematical Foundations)

Pada integrasi sistem tingkat platform (Level 3 Capstone), parameter kualitas layanan (*Quality of Service*) dievaluasi melalui latensi persentil ke-99 ($P_{99}$) dan ketersediaan komposit:

1. **Distribusi Latensi Persentil ke-99 ($P_{99}$)**:
   Dalam sistem telemetri terdistribusi, rata-rata latensi ($\mu$) sering kali menyamarkan lonjakan waktu respons ekstrem (*tail latency*). Nilai persentil ke-99 menyatakan batas atas latensi di mana $99\\%$ transaksi berhasil diselesaikan:
   $$
   P_{99} = \\inf \\{ t \\in \\mathbb{R} : F(t) \\ge 0{,}99 \\}
   $$
   di mana $F(t)$ adalah fungsi distribusi kumulatif waktu respons end-to-end (Sensor $\\rightarrow$ Broker $\\rightarrow$ Database $\\rightarrow$ UI).

2. **Kalkulasi Ketersediaan Layanan Komposit (Worked Example)**:
   Arsitektur capstone terdiri atas empat tier independen yang terhubung seri:
   - Ingest Broker (MQTT Cluster): $A_1 = 99{,}95\\%$
   - Gateway/Worker Stream Processor: $A_2 = 99{,}90\\%$
   - Time-Series Database Cluster: $A_3 = 99{,}99\\%$
   - Web Dashboard & Alerting Service: $A_4 = 99{,}90\\%$
   Ketersediaan sistem end-to-end $A_{\\text{E2E}}$ adalah:
   $$
   A_{\\text{E2E}} = A_1 \\times A_2 \\times A_3 \\times A_4 = 0{,}9995 \\times 0{,}9990 \\times 0{,}9999 \\times 0{,}9990 \\approx 0{,}9974 \\quad (99{,}74\\%)
   $$
   Waktu henti (*downtime*) kumulatif per tahun dari platform sistem adalah:
   $$
   T_{\\text{down}} = 8760 \\times (1 - 0{,}9974) = 8760 \\times 0{,}0026 \\approx 22{,}78\\text{ jam/tahun}
   $$
   Untuk meningkatkan ketersediaan menjadi $99{,}99\\%$ (*Four Nines*), tier worker stream processor dan ingest broker wajib mengimplementasikan redundansi aktif paralel (*Active-Active Clustered Nodes*).
`,
    extraReferences: [
      '- Dean, J., & Barroso, L. A., *The Tail at Scale*, Communications of the ACM, Vol. 56 No. 2, 2013.',
      '- IEEE Std 1451.4, *Standard for A Smart Transducer Interface for Sensors and Actuators*, IEEE.'
    ]
  },
  {
    slug: 'chapter-32',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Penjadwalan Rate-Monotonic (RMA) & Schedulability Bounds (Mathematical Foundations)

Sistem operasi waktu-nyata (*Real-Time Operating System* / RTOS) seperti FreeRTOS menjamin batas waktu deterministik melalui algoritma penjadwalan prioritas preemptive:

1. **Batas Keterjadwalan Liu & Layland (Rate-Monotonic Analysis / RMA)**:
   Untuk satu set $n$ task periodik independen dengan waktu komputasi terburuk (*Worst-Case Execution Time* / WCET) $C_i$ dan periode pengulangan $T_i$, di mana task dengan periode lebih pendek diberi prioritas lebih tinggi, task dijamin memenuhi deadline jika total utilisasi CPU $U$ memenuhi:
   $$
   U = \\sum_{i=1}^{n} \\frac{C_i}{T_i} \\le n \\left(2^{1/n} - 1\\right)
   $$
   Untuk jumlah task mendekati tak terhingga ($n \\to \\infty$), batas keterjadwalan asimtotik adalah:
   $$
   \\lim_{n \\to \\infty} n \\left(2^{1/n} - 1\\right) = \\ln(2) \\approx 0{,}693 \\quad (69{,}3\\%)
   $$

2. **Uji Keterjadwalan Sistem Multi-Task FreeRTOS ESP32 (Worked Example)**:
   Sebuah sistem akuisisi data memiliki 3 task konkuren:
   - Task 1 (Sampling Sensor Cepat): $C_1 = 2\\text{ ms}$, $T_1 = 10\\text{ ms} \\rightarrow U_1 = \\frac{2}{10} = 0{,}20$
   - Task 2 (Kalkulasi Filter & FSM): $C_2 = 10\\text{ ms}$, $T_2 = 50\\text{ ms} \\rightarrow U_2 = \\frac{10}{50} = 0{,}20$
   - Task 3 (Enkapsulasi & Kirim Jaringan): $C_3 = 25\\text{ ms}$, $T_3 = 100\\text{ ms} \\rightarrow U_3 = \\frac{25}{100} = 0{,}25$
   Total utilisasi CPU gabungan adalah:
   $$
   U = 0{,}20 + 0{,}20 + 0{,}25 = 0{,}65 \\quad (65\\%)
   $$
   Batas teoritis Liu & Layland untuk $n = 3$ task adalah:
   $$
   U_{\\text{bound}} = 3 \\left(2^{1/3} - 1\\right) = 3 \\left(1{,}2599 - 1\\right) = 3 \\times 0{,}2599 \\approx 0{,}7798 \\quad (77{,}98\\%)
   $$
   Karena $U = 0{,}65 \\le 0{,}7798$, seluruh task terbukti secara matematis **dijamin 100% memenuhi deadline** tanpa risiko *deadline miss*.
`,
    extraReferences: [
      '- Liu, C. L., & Layland, J. W., *Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment*, Journal of the ACM, 1973.',
      '- Barry, R., *Mastering the FreeRTOS Real Time Kernel: A Hands-On Tutorial Guide*, Real Time Engineers Ltd.'
    ]
  },
  {
    slug: 'chapter-33',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Polinomial CRC-16 Modbus & Verifikasi Integritas Frame (Mathematical Foundations)

Komunikasi industri (IIoT) mengandalkan Cyclic Redundancy Check (CRC-16) standar Modbus untuk mendeteksi galat transmisi di lingkungan pabrik yang penuh gangguan elektromagnetik:

1. **Polinomial Pembagi CRC-16 (Modbus Standard)**:
   Algoritma CRC-16 Modbus menggunakan representasi polinomial biner:
   $$
   G(x) = x^{16} + x^{15} + x^2 + 1 \\quad (\\text{heksadesimal: } \\texttt{0x8005}, \\text{ reversed: } \\texttt{0xA001})
   $$
   Register CRC diinisialisasi dengan nilai \`0xFFFF\`. Setiap byte data di-XOR dengan 8 bit terendah register, kemudian digeser ke kanan sebanyak 8 kali dengan conditional XOR terhadap polinomial \`0xA001\`.

2. **Kemampuan Deteksi Galat & Analisis Probabilitas Residual Error (Worked Example)**:
   Secara teoritis, CRC-16 menjamin deteksi $100\\%$ terhadap seluruh galat bit tunggal (*single-bit error*), galat bit ganda (*double-bit error*), dan pola rentetan galat (*burst error*) dengan panjang $\\le 16\\text{ bit}$.
   Probabilitas galat acak yang lolos dari deteksi CRC-16 pada frame data sembarang adalah:
   $$
   P_{\\text{undetected}} = \\frac{1}{2^{16}} = \\frac{1}{65536} \\approx 1{,}526 \\times 10^{-5} \\quad (0{,}0015\\%)
   $$
   Untuk frame Modbus RTU standar dengan panjang $L = 8\\text{ byte}$ pada baud rate $9600\\text{ bps}$ ($T_{\\text{char}} = 1{,}04\\text{ ms}$), waktu transmisi frame total adalah:
   $$
   T_{\\text{frame}} = 8 \\times 10 \\times \\frac{1}{9600} \\approx 8{,}33\\text{ ms}
   $$
   Waktu hening antar-frame minimum (*silent interval*) yang disyaratkan standar Modbus adalah $t_{3{,}5} = 3{,}5 \\times T_{\\text{char}} \\approx 3{,}65\\text{ ms}$, memastikan demarkasi frame tanpa memerlukan karakter khusus pembungkus paket.
`,
    extraReferences: [
      '- Modbus Organization, *Modbus Application Protocol Specification V1.1b3*, Modbus.org, 2012.',
      '- IEC 62541-1:2020, *OPC Unified Architecture - Part 1: Overview and Concepts*, International Electrotechnical Commission.'
    ]
  },
  {
    slug: 'chapter-34',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Topologi Jaringan Mesh Thread & Routing Distance-Vector (Mathematical Foundations)

Jaringan Thread (IEEE 802.15.4 pada $2{,}4\\text{ GHz}$) menggunakan varian protokol perutean jarak jauh (*Distance Vector Routing*) untuk mengoordinasikan topologi multi-hop mesh mandiri (*self-healing mesh*):

1. **Metrik Biaya Jalur (Path Cost Metric)**:
   Biaya per tautan nirkabel $C_{ij}$ antara router $i$ dan router $j$ diturunkan dari kualitas tautan sinyal (*Link Quality Indicator* / LQI):
   $$
   C_{ij} = \\text{Cost}(\\text{LQI}_{ij}) \\in \\{1, 2, 4, \\infty\\}
   $$
   Total biaya perutean rute multi-hop $P = (v_1, v_2, \\dots, v_k)$ adalah akumulasi biaya setiap hop:
   $$
   \\text{Cost}(P) = \\sum_{m=1}^{k-1} C_{v_m, v_{m+1}}
   $$
   Algoritma perutean Thread memilih jalur dengan $\\min \\text{Cost}(P)$ untuk meminimalkan transmisi ulang radio.

2. **Perhitungan Latensi Multi-Hop Mesh (Worked Example)**:
   Sebuah node Thread End Device (ED) mengirimkan perintah Matter ke Border Router melalui 3 hop router intermediate ($k=4$ simpul).
   Jika latensi per hop radio rata-rata (termasuk CSMA-CA backoff dan ACK lapisan MAC) adalah $t_{\\text{hop}} = 12\\text{ ms}$, total latensi propagasi transmisi perintah adalah:
   $$
   T_{\\text{mesh}} = (k - 1) \\times t_{\\text{hop}} = 3 \\times 12\\text{ ms} = 36\\text{ ms}
   $$
   Nilai $36\\text{ ms}$ berada jauh di bawah ambang batas persepsi interaksi manusia ($100\\text{ ms}$), membuktikan bahwa arsitektur Thread mampu memberikan responsivitas setara koneksi langsung kabel untuk otomasi bangunan pintar.
`,
    extraReferences: [
      '- Thread Group, *Thread 1.3.0 Specification: Mesh Networking for Smart Devices*, Thread Group Inc, 2022.',
      '- Connectivity Standards Alliance (CSA), *Matter Core Specification Version 1.3*, CSA, 2024.'
    ]
  },
  {
    slug: 'chapter-37',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Distribusi Consistent Hashing & Penyeimbangan Beban Sharding (Mathematical Foundations)

Dalam arsitektur IoT terdistribusi berskala jutaan perangkat, skema partisi kunci menggunakan algoritma Consistent Hashing meminimalkan redistribusi data saat penambahan atau pengurangan node server:

1. **Rasio Migrasi Kunci pada Pertambahan Node Server**:
   Pada skema modulo tradisional ($h(k) \\pmod N$), perubahan jumlah node dari $N$ menjadi $N+1$ menyebabkan hampir seluruh kunci berpindah partisi dengan rasio migrasi:
   $$
   R_{\\text{modulo}} = \\frac{N}{N + 1} \\approx 100\\% \\quad (\\text{untuk } N \\gg 1)
   $$
   Sebaliknya, pada cincin Consistent Hashing dengan $V$ virtual node per server fisik, penambahan satu server hanya memindahkan rata-rata kunci sebesar:
   $$
   R_{\\text{consistent}} = \\frac{1}{N + 1}
   $$

2. **Analisis Beban Kluster 10 Server Terdistribusi (Worked Example)**:
   Sebuah platform IoT menangani $M = 1.000.000$ koneksi perangkat MQTT pada kluster $N = 10$ broker.
   Saat server ke-11 ditambahkan untuk mengantisipasi lonjakan beban (*scale-out*):
   - Jumlah koneksi yang perlu dimigrasikan pada Consistent Hashing:
     $$
     K_{\\text{migrasi}} = \\frac{1}{11} \\times 1.000.000 \\approx 90.909\\text{ koneksi } (9{,}09\\%)
     $$
   - Jika memakai modulo hashing tradisional:
     $$
     K_{\\text{migrasi,trad}} = \\frac{10}{11} \\times 1.000.000 \\approx 909.091\\text{ koneksi } (90{,}91\\%)
     $$
   Pengurangan migrasi dari $90{,}9\\%$ menjadi hanya $9{,}09\\%$ mencegah fenomena badai koneksi ulang (*thundering herd reconnection*) yang dapat melumpuhkan seluruh kluster broker IoT.
`,
    extraReferences: [
      '- Karger, D., et al., *Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web*, ACM STOC, 1997.',
      '- Kleppmann, M., *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*, O\'Reilly Media.'
    ]
  },
  {
    slug: 'chapter-39',
    targetBefore: '## Latihan',
    mathContent: `### 3.1 Landasan Matematis: Kuantifikasi Skor Risiko DREAD & Entropi Diferensial Privasi (Mathematical Foundations)

Kuantifikasi risiko keamanan siber IoT dan kepatuhan privasi (*Privacy by Design*) diukur menggunakan skor numerik terstruktur DREAD dan jaminan diferensial:

1. **Formulasi Indeks Risiko DREAD**:
   Tingkat risiko kuantitatif $R_{\\text{DREAD}}$ dihitung sebagai nilai rerata aritmatika dari 5 parameter bernilai 1 hingga 10: Damage potential ($D$), Reproducibility ($R$), Exploitability ($E$), Affected users ($A$), dan Discoverability ($D_v$):
   $$
   R_{\\text{DREAD}} = \\frac{D + R + E + A + D_v}{5}
   $$
   Tingkat keparahan risiko diklasifikasikan menjadi: Rendah ($1{,}0 - 3{,}9$), Menengah ($4{,}0 - 6{,}9$), dan Kritis/Tinggi ($7{,}0 - 10{,}0$).

2. **Model Privasi Diferensial pada Agregasi Telemetri (Worked Example)**:
   Sebuah sistem smart meter mengumpulkan data konsumsi energi rumah tangga. Untuk melindungi privasi tanpa merusak akurasi analitik agregat, mekanisme Laplace menambahkan derau acak $Y \\sim \\text{Laplace}(0, b)$ dengan parameter skala:
   $$
   b = \\frac{\\Delta f}{\\epsilon}
   $$
   di mana $\\Delta f$ adalah sensitivitas global kueri dan $\\epsilon$ adalah anggaran privasi (*privacy budget*).
   Jika sensitivitas pembacaan konsumsi daya per rumah adalah $\\Delta f = 2{,}5\\text{ kWh}$ dan dipilih parameter privasi ketat $\\epsilon = 0{,}5$:
   $$
   b = \\frac{2{,}5}{0{,}5} = 5{,}0\\text{ kWh}
   $$
   Varians desah privasi yang ditambahkan adalah $\\sigma^2 = 2 b^2 = 2 \\times (5{,}0)^2 = 50\\text{ kWh}^2$. Saat diagregasikan pada tingkat gardu trafo $1000$ rumah tangga, deviasi baku rata-rata per rumah tangga terdistribusi turun sebanding dengan $\\frac{1}{\\sqrt{1000}} \\approx 0{,}0316$, sehingga analitik grid tetap sangat akurat sementara identitas individu terlindungi secara matematis.
`,
    extraReferences: [
      '- Dwork, C., & Roth, A., *The Algorithmic Foundations of Differential Privacy*, Foundations and Trends in Theoretical Computer Science, 2014.',
      '- ISO/IEC 27400:2022, *Cybersecurity — IoT security and privacy — Guidelines*, International Organization for Standardization.'
    ]
  },
  {
    slug: 'chapter-40',
    targetBefore: '## Latihan',
    mathContent: `### 2.1 Landasan Matematis: Metrik Efektivitas Sistem Gabungan (OEE) & Ketersediaan Capstone (Mathematical Foundations)

Pada perancangan platform industri tingkat akhir (Level 4 Capstone), keberhasilan integrasi dievaluasi menggunakan metrik Overall Equipment Effectiveness (OEE) dan keandalan sistem kritis:

1. **Model Overall Equipment Effectiveness (OEE)**:
   Metrik OEE menggabungkan tiga dimensi utama kinerja fasilitas industri: Ketersediaan (*Availability* / $A_{\\text{oee}}$), Performa (*Performance* / $P_{\\text{oee}}$), dan Kualitas (*Quality* / $Q_{\\text{oee}}$):
   $$
   \\text{OEE} = A_{\\text{oee}} \\times P_{\\text{oee}} \\times Q_{\\text{oee}}
   $$
   - $A_{\\text{oee}} = \\frac{\\text{Operating Time}}{\\text{Planned Production Time}}$
   - $P_{\\text{oee}} = \\frac{\\text{Ideal Cycle Time} \\times \\text{Total Count}}{\\text{Operating Time}}$
   - $Q_{\\text{oee}} = \\frac{\\text{Good Count}}{\\text{Total Count}}$

2. **Kalkulasi Kinerja Platform Smart Factory Terpadu (Worked Example)**:
   Pabrik beroperasi selama waktu terencana $T_{\\text{plan}} = 480\\text{ menit}$ (8 jam).
   - Waktu henti akibat setup dan perawatan adalah $30\\text{ menit} \\rightarrow \\text{Operating Time} = 450\\text{ menit}$.
     $$
     A_{\\text{oee}} = \\frac{450}{480} = 0{,}9375 \\quad (93{,}75\\%)
     $$
   - Laju ideal produksi adalah $0{,}5\\text{ menit/unit}$. Total unit yang diproduksi adalah $810\\text{ unit}$.
     $$
     P_{\\text{oee}} = \\frac{0{,}5 \\times 810}{450} = \\frac{405}{450} = 0{,}9000 \\quad (90{,}00\\%)
     $$
   - Dari 810 unit yang diproduksi, sistem inspeksi Edge AI TinyML mendeteksi 16 unit cacat sehingga produk baik berjumlah $794\\text{ unit}$.
     $$
     Q_{\\text{oee}} = \\frac{794}{810} \\approx 0{,}9802 \\quad (98{,}02\\%)
     $$
   Nilai OEE komprehensif pabrik yang dipantau platform IoT adalah:
   $$
   \\text{OEE} = 0{,}9375 \\times 0{,}9000 \\times 0{,}9802 \\approx 0{,}8270 \\quad (82{,}70\\%)
   $$
   Pencapaian $\\text{OEE} > 80\\%$ merefleksikan standar kelas dunia (*World Class Manufacturing*), membuktikan bahwa integrasi platform end-to-end mampu menyajikan analitik kuantitatif yang presisi untuk pengambilan keputusan operasional.
`,
    extraReferences: [
      '- SEMI E10-0304, *Specification for Definition and Measurement of Equipment Reliability, Availability, and Maintainability (RAM)*.',
      '- IEEE Std 1012-2016, *IEEE Standard for System, Software, and Hardware Verification and Validation*, IEEE.'
    ]
  }
];

for (const t of targets) {
  const filePath = path.join('public', 'content', t.slug, 'reading.md');
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    continue;
  }
  let content = fs.readFileSync(filePath, 'utf8');

  if (content.includes('Mathematical Foundations')) {
    console.log(`Skipping ${t.slug}, already has Mathematical Foundations.`);
    continue;
  }

  if (!content.includes(t.targetBefore)) {
    console.warn(`Target not found in ${t.slug}: "${t.targetBefore}"`);
    continue;
  }

  content = content.replace(t.targetBefore, t.mathContent + '\n' + t.targetBefore);

  if (t.extraReferences && t.extraReferences.length > 0) {
    const refHeader = '## Referensi';
    if (content.includes(refHeader)) {
      const extraRefText = '\n' + t.extraReferences.join('\n');
      content = content.replace(refHeader, refHeader + extraRefText);
    }
  }

  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Successfully enhanced ${t.slug}!`);
}


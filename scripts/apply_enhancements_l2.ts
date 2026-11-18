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
    slug: 'chapter-11',
    targetBefore: '### 6. Alur Troubleshooting Konektivitas IoT Berlapis (Bottom-Up)',
    mathContent: `### 5.1 Model Matematis Transmisi Sinyal & Perhitungan Throughput Efektif (Mathematical Foundations)

Karakteristik jaringan IoT dibatasi oleh kapasitas kanal fisik dan rasio overhead enkapsulasi protokol:

1. **Teorema Kapasitas Kanal Shannon-Hartley**:
   Kapasitas informasi maksimum teoritis $C$ (dalam bit per detik/bps) pada kanal dengan lebar pita (bandwidth) $B$ (dalam Hz) dan rasio sinyal terhadap desah (*Signal-to-Noise Ratio* / SNR) dinyatakan oleh:
   $$
   C = B \\log_2 \\left(1 + \\text{SNR}\\right) = B \\log_2 \\left(1 + 10^{\\frac{\\text{SNR}_{\\text{dB}}}{10}}\\right)
   $$
   Untuk kanal nirkabel sempit dengan $B = 125\\text{ kHz}$ dan $\\text{SNR}_{\\text{dB}} = 10\\text{ dB}$ (sehingga rasio linier $\\text{SNR} = 10$):
   $$
   C = 125 \\times 10^3 \\times \\log_2(1 + 10) = 125 \\times 10^3 \\times 3{,}459 \\approx 432{,}4\\text{ kbps}
   $$

2. **Efisiensi Protokol & Overhead Enkapsulasi (Worked Example)**:
   Sebuah sensor IoT mengirimkan payload data telemetri suhu dan tekanan berukuran $L_{\\text{payload}} = 24\\text{ byte}$. Ketika ditransmisikan melalui stack IPv4 dan UDP standar, header tambahan yang ditambahkan mencakup:
   - Header IEEE 802.11 (Wi-Fi MAC): $L_{\\text{MAC}} = 36\\text{ byte}$
   - Header IPv4: $L_{\\text{IP}} = 20\\text{ byte}$
   - Header UDP: $L_{\\text{UDP}} = 8\\text{ byte}$
   Total ukuran frame fisik yang dikirimkan pada lapisan tautan adalah:
   $$
   L_{\\text{total}} = L_{\\text{payload}} + L_{\\text{UDP}} + L_{\\text{IP}} + L_{\\text{MAC}} = 24 + 8 + 20 + 36 = 88\\text{ byte}
   $$
   Efisiensi transmisi data aplikasi $\\eta_{\\text{proto}}$ dirumuskan sebagai:
   $$
   \\eta_{\\text{proto}} = \\frac{L_{\\text{payload}}}{L_{\\text{total}}} \\times 100\\% = \\frac{24}{88} \\times 100\\% \\approx 27{,}27\\%
   $$
   Jika menggunakan protokol TCP ($L_{\\text{TCP}} = 20\\text{ byte}$), ukuran frame membengkak menjadi $100\\text{ byte}$ sehingga efisiensi merosot ke $24\\%$. Fakta matematis ini mendasari perlunya protokol kompresi header seperti 6LoWPAN pada jaringan berdaya rendah (*Constrained Networks*).
`,
    extraReferences: [
      '- Shannon, C. E., *A Mathematical Theory of Communication*, Bell System Technical Journal, Vol. 27, 1948.',
      '- IETF RFC 791, *Internet Protocol (IPv4) Specification*, DARPA Internet Program Protocol Specification.'
    ]
  },
  {
    slug: 'chapter-12',
    targetBefore: '### 7. Common Mistakes & Troubleshooting',
    mathContent: `### 6.1 Model Matematis Propagasi Radio Wi-Fi & Link Budget (Mathematical Foundations)

Konektivitas Wi-Fi (IEEE 802.11 b/g/n) pada frekuensi $2{,}4\\text{ GHz}$ mengalami redaman daya propagasi di ruang bebas (*Free-Space Path Loss* / FSPL) yang dirumuskan oleh persamaan Friis:

1. **Redaman Ruang Bebas (Free-Space Path Loss)**:
   $$
   \\text{FSPL}_{\\text{dB}} = 20 \\log_{10}(d) + 20 \\log_{10}(f) - 147{,}55
   $$
   di mana jarak $d$ dinyatakan dalam meter (m) dan frekuensi transmisi $f$ dalam Hertz (Hz). Untuk frekuensi tengah Wi-Fi kanal 6 ($f = 2{,}437\\text{ GHz} = 2{,}437 \\times 10^9\\text{ Hz}$):
   $$
   \\text{FSPL}_{\\text{dB}}(d) = 20 \\log_{10}(d) + 20 \\log_{10}(2{,}437 \\times 10^9) - 147{,}55 = 20 \\log_{10}(d) + 40{,}19\\text{ dB}
   $$

2. **Perhitungan Daya Terima (RSSI) & Link Margin (Worked Example)**:
   Daya sinyal yang diterima oleh perangkat ESP32 ($P_{\\text{RX}}$ dalam dBm) ditentukan oleh daya pancar Access Point ($P_{\\text{TX}}$), penguatan antena pemancar ($G_{\\text{TX}}$), penguatan antena penerima ($G_{\\text{RX}}$), dan redaman dinding/penghalang ($L_{\\text{obs}}$):
   $$
   P_{\\text{RX}} = P_{\\text{TX}} + G_{\\text{TX}} + G_{\\text{RX}} - \\text{FSPL} - L_{\\text{obs}}
   $$
   **Kasus**: Pemancar Wi-Fi memancarkan daya $P_{\\text{TX}} = +18\\text{ dBm}$, $G_{\\text{TX}} = 2\\text{ dBi}$, antena PCB ESP32 memiliki $G_{\\text{RX}} = 1\\text{ dBi}$, jarak perangkat $d = 20\\text{ meter}$, dan sinyal menembus 1 dinding bata ringan ($L_{\\text{obs}} = 6\\text{ dB}$):
   $$
   \\text{FSPL}_{\\text{dB}}(20) = 20 \\log_{10}(20) + 40{,}19 = 26{,}02 + 40{,}19 = 66{,}21\\text{ dB}
   $$
   $$
   P_{\\text{RX}} = 18 + 2 + 1 - 66{,}21 - 6 = -51{,}21\\text{ dBm}
   $$
   Jika sensitivitas minimum penerima ESP32 untuk modulasi MCS7 (72 Mbps) adalah $S_{\\text{min}} = -71\\text{ dBm}$, maka *Link Margin* ($M$) sistem adalah:
   $$
   M = P_{\\text{RX}} - S_{\\text{min}} = -51{,}21\\text{ dBm} - (-71\\text{ dBm}) = +19{,}79\\text{ dB}
   $$
   Link margin $> 15\\text{ dB}$ menjamin tautan nirkabel stabil terhadap *fading* dan fluktuasi interferensi lingkungan sekitar.
`,
    extraReferences: [
      '- IEEE Std 802.11-2020, *IEEE Standard for Information Technology—Telecommunications and Information Exchange between Systems - Local and Metropolitan Area Networks—Specific Requirements - Part 11: Wireless LAN MAC and PHY Specifications*.',
      '- Friis, H. T., *A Note on a Simple Transmission Formula*, Proceedings of the IRE, 1946.'
    ]
  },
  {
    slug: 'chapter-13',
    targetBefore: '### 7. Common Mistakes & Troubleshooting',
    mathContent: `### 6.1 Landasan Matematis: Overhead Protokol HTTP & Analisis Latensi REST (Mathematical Foundations)

Meskipun protokol HTTP/REST berbasis JSON sangat mudah diintegrasikan dengan sistem cloud web, karakteristik stateless berbasis koneksi TCP memunculkan overhead latensi dan bandwidth yang signifikan:

1. **Pemodelan Waktu Respons Transaksi HTTP (RTT Modeling)**:
   Setiap transaksi HTTP non-persistent memerlukan tahapan *3-Way Handshake* TCP sebelum data dapat dikirim. Waktu penyelesaian transaksi total $T_{\\text{HTTP}}$ dengan waktu bolak-balik jaringan *Round-Trip Time* ($\\text{RTT}$) dan latensi pemrosesan server $T_{\\text{proc}}$ adalah:
   $$
   T_{\\text{HTTP}} = 1{,}5 \\cdot \\text{RTT} + T_{\\text{tx,req}} + T_{\\text{proc}} + T_{\\text{tx,res}} + 0{,}5 \\cdot \\text{RTT} = 2 \\cdot \\text{RTT} + T_{\\text{proc}} + \\frac{L_{\\text{req}} + L_{\\text{res}}}{R_{\\text{link}}}
   $$
   Jika enkripsi TLS (HTTPS) diaktifkan, diperlukan tambahan $2 \\cdot \\text{RTT}$ untuk negosiasi kunci kriptografi (TLS 1.2), sehingga total latensi melonjak menjadi $4 \\cdot \\text{RTT} + T_{\\text{proc}}$.

2. **Perhitungan Rasio Overhead Payload JSON (Worked Numerical Example)**:
   Sebuah node sensor mengirimkan nilai suhu $28{,}5\\,^\\circ\\text{C}$ dan kelembaban $62\\%$.
   - Payload JSON ringkas: \`{"t":28.5,"h":62}\` $\\rightarrow L_{\\text{payload}} = 17\\text{ byte}$.
   - Header HTTP Request (\`POST /api/v1/telemetry HTTP/1.1\\r\\nHost: iot.itera.ac.id\\r\\nContent-Type: application/json\\r\\nContent-Length: 17\\r\\nUser-Agent: ESP32HTTPClient\\r\\nConnection: close\\r\\n\\r\\n\`): $L_{\\text{header}} = 168\\text{ byte}$.
   Total data pada lapisan aplikasi adalah:
   $$
   L_{\\text{app}} = L_{\\text{header}} + L_{\\text{payload}} = 168 + 17 = 185\\text{ byte}
   $$
   Rasio pemborosan data akibat header HTTP dinyatakan dengan:
   $$
   \\Omega_{\\text{overhead}} = \\frac{L_{\\text{header}}}{L_{\\text{app}}} \\times 100\\% = \\frac{168}{185} \\times 100\\% \\approx 90{,}81\\%
   $$
   Lebih dari $90\\%$ bandwidth terbuang hanya untuk metadata protokol HTTP. Analisis ini membuktikan secara matematis mengapa protokol berorientasi pesan seperti MQTT atau CoAP jauh lebih unggul untuk simpul telemetri periodik.
`,
    extraReferences: [
      '- IETF RFC 9110, *HTTP Semantics*, Internet Engineering Task Force (IETF), 2022.',
      '- Fielding, R. T., *Architectural Styles and the Design of Network-based Software Architectures*, Doctoral Dissertation, University of California, Irvine, 2000.'
    ]
  },
  {
    slug: 'chapter-15',
    targetBefore: '### 7. Common Mistakes & Troubleshooting',
    mathContent: `### 6.1 Model Matematis Keandalan QoS & Analisis Probabilitas Pengiriman Pesan (Mathematical Foundations)

Mekanisme Quality of Service (QoS) pada MQTT menjamin tingkat keterikatan pengiriman pesan di atas jaringan transmisi nirkabel yang memiliki probabilitas kehilangan paket (*Packet Loss Rate* / $p$):

1. **Probabilitas Sukses Pengiriman Berdasarkan Tingkat QoS**:
   Jika probabilitas kegagalan transmisi paket tunggal di kanal nirkabel adalah $p$ ($0 \\le p < 1$):
   - **QoS 0 (*At Most Once*)**: Pesan hanya dikirim satu kali tanpa konfirmasi. Probabilitas pesan berhasil diterima subscriber $P_{\\text{succ,0}}$ adalah:
     $$
     P_{\\text{succ,0}} = 1 - p
     $$
   - **QoS 1 (*At Least Once*)**: Pengirim mengulang transmisi hingga menerima PUBACK sampai batas pengulangan maksimum $K$ kali. Probabilitas kegagalan pesan hilang sepenuhnya merosot menjadi $p^K$:
     $$
     P_{\\text{succ,1}} = 1 - p^K
     $$
     Untuk $p = 0{,}10$ ($10\\%$ packet loss) dan batas pengulangan $K = 3$, $P_{\\text{succ,1}} = 1 - (0{,}1)^3 = 0{,}999$ ($99{,}9\\%$ sukses).

2. **Analisis Beban Pesan & Waktu Tunda Transaksi 4-Way Handshake QoS 2 (Worked Example)**:
   Pada QoS 2 (*Exactly Once*), proses transmisi melibatkan pertukaran 4 paket kontrol: PUBLISH $\\rightarrow$ PUBREC $\\rightarrow$ PUBREL $\\rightarrow$ PUBCOMP.
   Total waktu transmisi end-to-end tanpa kehilangan paket $T_{\\text{QoS2}}$ adalah:
   $$
   T_{\\text{QoS2}} = 4 \\cdot \\left( \\frac{\\text{RTT}}{2} \\right) = 2 \\cdot \\text{RTT}
   $$
   Total byte kontrol yang dikonsumsi untuk satu pesan QoS 2 (di luar payload) dengan ukuran rata-rata paket kontrol MQTT 4 byte dan header TCP/IP 40 byte adalah:
   $$
   B_{\\text{overhead}} = 4 \\times (4\\text{ B} + 40\\text{ B}) = 176\\text{ byte}
   $$
   Beban kontrol ini 4 kali lebih besar dibanding QoS 0. Oleh karena itu, aturan rekayasa industri menetapkan: QoS 0 digunakan untuk data telemetri frekuensi tinggi yang toleran terhadap kehilangan sampel terisolasi (misal sensor suhu lingkungan), QoS 1 untuk log kejadian berkala, dan QoS 2 dicadangkan khusus untuk transaksi kritis (seperti perintah transfer finansial atau pemutakhiran firmware).
`,
    extraReferences: [
      '- OASIS Standard, *MQTT Version 5.0 Section 4.3: Quality of Service levels and protocol flows*, OASIS Open.',
      '- RFC 8938, *Deterministic Networking (DetNet) Data Plane - Security Considerations*, IETF.'
    ]
  },
  {
    slug: 'chapter-17',
    targetBefore: '### 6. Implementasi Firmware & Troubleshooting Umum',
    mathContent: `### 5.1 Landasan Matematis: BLE Advertising Interval & Perhitungan Konsumsi Energi (Mathematical Foundations)

Protokol Bluetooth Low Energy (BLE Core Specification v5.x) mengoptimalkan konsumsi daya melalui siklus duty cycle siaran periodik pada tiga kanal iklan bebas interferensi Wi-Fi (Kanal 37, 38, dan 39):

1. **Interval Siaran (Advertising Interval) & Pertambahan Jitter Acak**:
   Untuk menghindari tabrakan berulang (*packet collision*) antar-beacons independen, waktu antar-paket siaran $T_{\\text{adv}}$ dirumuskan dengan menambahkan penundaan acak (*pseudo-random delay*):
   $$
   T_{\\text{adv}} = \\text{advInterval} + \\text{advDelay}
   $$
   di mana $\\text{advInterval}$ merupakan kelipatan bulat dari $0{,}625\\text{ ms}$ (rentang $20\\text{ ms}$ hingga $10{,}24\\text{ s}$), dan $\\text{advDelay}$ adalah bilangan bulat acak seragam antara $0\\text{ ms}$ hingga $10\\text{ ms}$.

2. **Perhitungan Arus Rata-Rata Beacon & Daya Tahan Baterai Coin-Cell (Worked Example)**:
   Sebuah BLE beacon mengirimkan paket non-connectable advertising sepanjang $t_{\\text{tx}} = 3\\text{ ms}$ dengan arus puncak $I_{\\text{peak}} = 15\\text{ mA}$. Di antara interval pengiriman, modul berada dalam kondisi deep sleep dengan arus statis $I_{\\text{sleep}} = 4\\,\\mu\\text{A}$. Interval siaran diatur sebesar $T_{\\text{adv}} = 1000\\text{ ms}$ (1 detik).
   Muatan listrik per siklus transmisi siaran $Q_{\\text{adv}}$ adalah:
   $$
   Q_{\\text{adv}} = I_{\\text{peak}} \\cdot t_{\\text{tx}} + I_{\\text{sleep}} \\cdot (T_{\\text{adv}} - t_{\\text{tx}})
   $$
   $$
   Q_{\\text{adv}} = (15\\text{ mA} \\times 0{,}003\\text{ s}) + (0{,}004\\text{ mA} \\times 0{,}997\\text{ s}) = 0{,}045\\text{ mAs} + 0{,}003988\\text{ mAs} \\approx 0{,}04899\\text{ mAs}
   $$
   Arus rata-rata kontinu $I_{\\text{avg}}$ sistem adalah:
   $$
   I_{\\text{avg}} = \\frac{Q_{\\text{adv}}}{T_{\\text{adv}}} = \\frac{0{,}04899\\text{ mAs}}{1\\text{ s}} \\approx 0{,}049\\text{ mA} = 49\\,\\mu\\text{A}
   $$
   Dengan menggunakan baterai koin lithium CR2032 berkapasitas nominal $C = 220\\text{ mAh}$ dan faktor penurunan kapasitas akibat arus pulsa $\\eta = 0{,}85$:
   $$
   t_{\\text{life}} = \\frac{220 \\times 0{,}85\\text{ mAh}}{0{,}049\\text{ mA}} \\approx 3816\\text{ jam } (\\sim 159\\text{ hari} \\text{ atau } 5{,}3\\text{ bulan})
   $$
   Jika interval siaran diperpanjang menjadi $5\\text{ detik}$, arus rata-rata merosot ke $\\approx 13\\,\\mu\\text{A}$ sehingga usia baterai melonjak hingga 1,6 tahun.
`,
    extraReferences: [
      '- Bluetooth SIG, *Bluetooth Core Specification v5.4*, Vol 6: Low Energy Controller, 2023.',
      '- Gomez, C., Oller, J., & Paradells, J., *Overview and Evaluation of Bluetooth Low Energy: An Emerging Technology for the Internet of Things*, Sensors, 2012.'
    ]
  },
  {
    slug: 'chapter-19',
    targetBefore: '## Latihan',
    mathContent: `### 5.1 Landasan Matematis: Sinkronisasi Waktu SNTP & Kapasitas Buffer Deret Waktu (Mathematical Foundations)

Keandalan simpul IoT saat jaringan terputus bergantung pada presisi pelacakan waktu lokal dan ukuran buffer penampungan:

1. **Model Drift Clock Osilator Lokal & Galat Waktu Akumulatif**:
   Osilator kristal kuarsa internal mikrokontroler memiliki toleransi kestabilan frekuensi yang dinyatakan dalam bagian per sejuta (*parts per million* / ppm), umumnya $\\delta = \\pm 20\\text{ ppm}$ hingga $\\pm 50\\text{ ppm}$. Waktu drift akumulatif $\\Delta t_{\\text{drift}}$ setelah durasi offline $T_{\\text{offline}}$ dirumuskan dengan:
   $$
   \\Delta t_{\\text{drift}} = \\delta \\times 10^{-6} \\times T_{\\text{offline}}
   $$
   Jika sistem terputus dari server waktu SNTP selama $T_{\\text{offline}} = 7\\text{ hari}$ ($604.800\\text{ detik}$) dengan osilator $\\delta = 30\\text{ ppm}$:
   $$
   \\Delta t_{\\text{drift}} = 30 \\times 10^{-6} \\times 604.800 = 18{,}144\\text{ detik}
   $$
   Penyimpangan lebih dari 18 detik dapat mengacaukan pengurutan data deret waktu dan membatalkan validitas sertifikat keamanan TLS.

2. **Perhitungan Kapasitas Ring Buffer Offline (Worked Engineering Example)**:
   Sebuah node telemetri merekam paket data berukuran $S_{\\text{packet}} = 64\\text{ byte}$ setiap interval $T_{\\text{sample}} = 15\\text{ detik}$. Sistem dirancang harus mampu mempertahankan integritas data selama gangguan jaringan maksimum $T_{\\text{outage}} = 48\\text{ jam}$.
   Total paket yang dihasilkan selama durasi pemadaman jaringan $N_{\\text{packets}}$ adalah:
   $$
   N_{\\text{packets}} = \\frac{T_{\\text{outage}} \\times 3600}{T_{\\text{sample}}} = \\frac{48 \\times 3600}{15} = \\frac{172.800}{15} = 11.520\\text{ paket}
   $$
   Kapasitas memori penyimpanan minimum yang wajib dialokasikan $M_{\\text{buffer}}$:
   $$
   M_{\\text{buffer}} = N_{\\text{packets}} \\times S_{\\text{packet}} = 11.520 \\times 64\\text{ byte} = 737.280\\text{ byte} \\approx 720\\text{ KiB}
   $$
   Karena SRAM internal mikrokontroler terbatas (misal ESP32 hanya memiliki 520 KiB di mana hanya $\\approx 150\\text{ KiB}$ tersedia untuk heap aplikasi), buffer sebesar $720\\text{ KiB}$ **tidak boleh disimpan di RAM**, melainkan wajib disimpan di partisi memori Non-Volatile (SPI Flash via LittleFS/NVS atau SD Card eksternal).
`,
    extraReferences: [
      '- IETF RFC 5905, *Network Time Protocol Version 4: Protocol and Algorithms Specification*, 2010.',
      '- Mills, D. L., *Computer Network Time Synchronization: The Network Time Protocol on Earth and in Space*, CRC Press.'
    ]
  },
  {
    slug: 'chapter-20',
    targetBefore: '### 5. Panduan Troubleshooting Capstone',
    mathContent: `### 4.1 Landasan Matematis: Ketersediaan Sistem (Availability) & MTBF Capstone (Mathematical Foundations)

Pada perancangan sistem capstone terhubung Level 2, keandalan keseluruhan perangkat telemetri nirkabel dimodelkan dengan teori probabilitas keandalan sistem (*Reliability Engineering*):

1. **Ketersediaan Sistem Jamak Seri (Series System Availability)**:
   Sistem telemetri IoT terdiri atas rantai subsistem yang saling bergantung: Sensor node ($A_{\\text{node}}$), Jaringan Wi-Fi/AP ($A_{\\text{net}}$), dan Server/MQTT Broker ($A_{\\text{srv}}$). Ketersediaan sistem total $A_{\\text{system}}$ dirumuskan sebagai:
   $$
   A_{\\text{system}} = A_{\\text{node}} \\times A_{\\text{net}} \\times A_{\\text{srv}}
   $$
   Jika ketersediaan perangkat keras node adalah $99{,}5\\%$, jaringan nirkabel lokal $98\\%$, dan broker cloud $99{,}9\\%$:
   $$
   A_{\\text{system}} = 0{,}995 \\times 0{,}980 \\times 0{,}999 \\approx 0{,}9741 \\text{ (atau } 97{,}41\\%\\text{)}
   $$
   Meskipun server memiliki SLA tinggi, ketersediaan akhir dibatasi oleh mata rantai terlemah (jaringan Wi-Fi).

2. **Perhitungan MTBF dan Waktu Henti Tahunan (Worked Example)**:
   Waktu henti (*downtime*) tahunan $T_{\\text{down}}$ dari sistem beroperasi kontinu ($8760\\text{ jam/tahun}$) dengan $A_{\\text{system}} = 97{,}41\\%$ adalah:
   $$
   T_{\\text{down}} = 8760 \\times (1 - 0{,}9741) = 8760 \\times 0{,}0259 \\approx 226{,}9\\text{ jam/tahun } (\\sim 9{,}45\\text{ hari})
   $$
   Dengan mengimplementasikan **arsitektur offline ring-buffer** di sisi node (sebagaimana diajarkan pada Chapter 19 & 20), data tidak hilang selama 226 jam putusnya koneksi jaringan. Begitu koneksi pulih, seluruh data terkirim kembali (*flushed*) sehingga ketersediaan data logis (*data retention availability*) meningkat menjadi:
   $$
   A_{\\text{data}} = \\frac{N_{\\text{transmitted}} + N_{\\text{buffered}}}{N_{\\text{total}}} \\approx 99{,}99\\%
   $$
`,
    extraReferences: [
      '- IEEE Std 1451.0-2007, *IEEE Standard for a Smart Transducer Interface for Sensors and Actuators*, IEEE.',
      '- IEC 61508, *Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems*, International Electrotechnical Commission.'
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


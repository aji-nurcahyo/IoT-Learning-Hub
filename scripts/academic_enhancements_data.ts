// Content definitions for academic mathematical deepening

export interface ChapterAcademicDeepening {
  slug: string;
  targetBeforeHeading: string;
  mathMarkdown: string;
  extraReferences: string[];
}

export const ACADEMIC_ENHANCEMENTS: ChapterAcademicDeepening[] = [
  {
    slug: 'chapter-04',
    targetBeforeHeading: '### 6. Development Environment, Flashing, Boot Modes & Serial Monitor',
    mathMarkdown: `### 5.1 Landasan Matematis: Frekuensi Clock, Disipasi Daya CMOS & Perhitungan Beban Pin (Mathematical Foundations)

Pemilihan mikrokontroler dan perancangan periferal perangkat keras memerlukan pemodelan kuantitatif waktu eksekusi clock dan konsumsi energi:

1. **Frekuensi Clock dan Periode Siklus Instruksi**:
   Jika prosesor beroperasi pada frekuensi inti $f_{\\text{cpu}}$, periode siklus instruksi dasar $T_{\\text{clk}}$ dinyatakan dengan:
   $$
   T_{\\text{clk}} = \\frac{1}{f_{\\text{cpu}}}
   $$
   Untuk ESP32 pada frekuensi clock maksimum $f_{\\text{cpu}} = 240\\text{ MHz}$, $T_{\\text{clk}} = \\frac{1}{240 \\times 10^6} \\approx 4{,}167\\text{ ns}$.

2. **Daya Dinamis CMOS (Dynamic Switching Power)**:
   Konsumsi daya mikrokontroler didominasi oleh pengisian dan pengosongan kapasitansi gerbang internal $C_{\\text{eff}}$ pada tegangan operasi $V_{\\text{dd}}$:
   $$
   P_{\\text{dynamic}} = \\alpha \\cdot C_{\\text{eff}} \\cdot V_{\\text{dd}}^2 \\cdot f_{\\text{cpu}}
   $$
   di mana $\\alpha$ adalah rasio peralihan gerbang (*activity factor*). Hubungan kuadratik terhadap $V_{\\text{dd}}^2$ dan linier terhadap frekuensi $f_{\\text{cpu}}$ menjelaskan mengapa menurunkan frekuensi clock (misalnya dari 240 MHz ke 80 MHz) memangkas arus dari $\\sim 50\\text{ mA}$ menjadi $\\sim 20\\text{ mA}$ saat aktif tanpa radio.

3. **Perhitungan Arus LED & Disipasi Daya Resistor Pembatas (Worked Numerical Example)**:
   Saat mengendalikan periferal indikator (seperti LED hijau pada GPIO 25) dari pin mikrokontroler dengan tegangan logika $V_{\\text{OH}} = 3{,}3\\text{ V}$ dan tegangan maju LED $V_{\\text{F}} = 2{,}1\\text{ V}$:
   $$
   I_{\\text{LED}} = \\frac{V_{\\text{OH}} - V_{\\text{F}}}{R_{\\text{lim}}}
   $$
   Dengan memilih resistor pembatas arus standar $R_{\\text{lim}} = 220\\,\\Omega$:
   $$
   I_{\\text{LED}} = \\frac{3{,}3\\text{ V} - 2{,}1\\text{ V}}{220\\,\\Omega} = \\frac{1{,}2\\text{ V}}{220\\,\\Omega} \\approx 5{,}45\\text{ mA}
   $$
   Nilai $5{,}45\\text{ mA}$ berada jauh di bawah batas arus rekomendasi maksimum pin ESP32 ($I_{\\text{max}} = 12\\text{ mA}$ per pin, batas absolut $40\\text{ mA}$). Daya yang didisipasikan oleh resistor adalah:
   $$
   P_{\\text{R}} = I_{\\text{LED}}^2 \\cdot R_{\\text{lim}} = (0{,}00545\\text{ A})^2 \\times 220\\,\\Omega \\approx 6{,}53\\text{ mW}
   $$
   Nilai ini sangat aman untuk resistor SMD atau *through-hole* standar dengan batas rating $0{,}125\\text{ W}$ ($125\\text{ mW}$).
`,
    extraReferences: [
      '- JEDEC Standard JESD8C.01, *Interface Standard for Nominal 3 V/3.3 V Supply Digital Integrated Circuits*, JEDEC Solid State Technology Association.',
      '- Espressif Systems, *ESP32 Datasheet (Rev 4.x)*, Espressif Systems.'
    ]
  },
  {
    slug: 'chapter-05',
    targetBeforeHeading: '### 6. Finite State Machine (FSM) Dasar',
    mathMarkdown: `### 5.1 Landasan Matematis: Analisis Kompleksitas & Pemodelan Fragmentasi Heap (Mathematical Foundations)

Dalam rekayasa sistem tertanam (*embedded systems*), efisiensi algoritma dan pemodelan alokasi memori berbanding lurus dengan keandalan perangkat:

1. **Kompleksitas Waktu dan Pemakaian Siklus Instruksi**:
   Operasi sampling atau manipulasi buffer ring berukuran $N$ sampel memiliki kompleksitas waktu $O(1)$ untuk penyisipan (*enqueue*) dan $O(N)$ untuk kalkulasi rata-rata bergerak (*moving average*):
   $$
   \\mu_k = \\frac{1}{N} \\sum_{i=0}^{N-1} x_{k-i}
   $$
   Jika setiap iterasi akumulasi membutuhkan $C_{\\text{loop}} = 4$ siklus instruksi pada frekuensi clock $f_{\\text{cpu}} = 160\\text{ MHz}$, total waktu eksekusi $t_{\\text{exec}}$ adalah:
   $$
   t_{\\text{exec}} = \\frac{N \\cdot C_{\\text{loop}}}{f_{\\text{cpu}}}
   $$
   Untuk buffer berukuran $N = 256$, waktu eksekusi komputasi hanya $t_{\\text{exec}} = \\frac{256 \\times 4}{160 \\times 10^6} = 6{,}4\\,\\mu\\text{s}$, yang sepenuhnya memenuhi batas waktu *real-time*.

2. **Model Fragmentasi Heap & Kapasitas Memori (Worked Example)**:
   Alokasi dinamis berulang (\`malloc\` / \`new\`) pada heap mikrokontroler memicu fragmentasi memori eksternal. Jika blok bebas terbesar $B_{\\text{max}}$ lebih kecil dari ukuran alokasi yang diminta $S_{\\text{req}}$, alokasi akan gagal meskipun total memori bebas $M_{\\text{free}} > S_{\\text{req}}$. Indeks fragmentasi memori $F_{\\text{heap}}$ dirumuskan sebagai:
   $$
   F_{\\text{heap}} = 1 - \\frac{B_{\\text{max}}}{M_{\\text{free}}}
   $$
   **Kasus**: Sistem memiliki total sisa memori bebas $M_{\\text{free}} = 40\\text{ KiB}$, namun terpecah-pecah sehingga blok bebas contiguous terbesar hanya $B_{\\text{max}} = 4\\text{ KiB}$.
   $$
   F_{\\text{heap}} = 1 - \\frac{4}{40} = 0{,}90 \\text{ (atau } 90\\%\\text{ terfragmentasi)}
   $$
   Kondisi $F_{\\text{heap}} = 90\\%$ menyebabkan sistem menolak alokasi buffer jaringan 8 KiB (\`ESP_ERR_NO_MEM\`). Oleh karena itu, prinsip rekayasa *embedded* mengharuskan alokasi array statis (\`static\` buffer) di masa kompilasi untuk menjamin ketiadaan fragmentasi heap runtime.
`,
    extraReferences: [
      '- MISRA C:2012, *Guidelines for the Use of the C Language in Critical Systems*, MISRA Consortium Ltd, 2013.',
      '- ISO/IEC 9899:2018, *Information technology — Programming languages — C*, International Organization for Standardization.'
    ]
  },
  {
    slug: 'chapter-06',
    targetBeforeHeading: '### 6. Implementasi Praktis: Button-Controlled LED FSM',
    mathMarkdown: `### 5.1 Model Matematis Kontak Bouncing & Perhitungan Filter Debounce (Mathematical Foundations)

Sakelar mekanis (push-button) mengalami fenomena transien *bouncing* saat kontak logam saling berbenturan sebelum mencapai kondisi tunak (*steady-state*):

1. **Karakteristik Transien Sakelar Mekanis**:
   Lama waktu osilasi bouncing $t_{\\text{bounce}}$ umumnya berlangsung antara $2\\text{ ms}$ hingga $20\\text{ ms}$. Jika frekuensi sampling $f_s$ terlalu tinggi tanpa filter, satu kali penekanan tombol dapat memicu puluhan interrupt palsu. Syarat kestabilan periode filter debouncing $T_{\\text{debounce}}$ adalah:
   $$
   T_{\\text{debounce}} > \\max(t_{\\text{bounce}})
   $$
   Dalam praktik rekayasa perangkat lunak, nilai standar yang direkomendasikan adalah $T_{\\text{debounce}} = 30\\text{ ms}$ hingga $50\\text{ ms}$.

2. **Perhitungan Filter RC Debounce Perangkat Keras (Worked Example)**:
   Pada sirkuit debouncing berbasis perangkat keras (hardware filter), kontak sakelar dihubungkan dengan filter lolos-rendah (Low-Pass Filter) resistor-kapasitor (RC). Waktu pengisian kapasitor hingga mencapai tegangan ambang input logika $V_{\\text{IH}} = 0{,}7 \\cdot V_{\\text{DD}}$ dinyatakan dengan:
   $$
   V_C(t) = V_{\\text{DD}} \\left(1 - e^{-t / (R C)}\\right)
   $$
   Menyelesaikan persamaan untuk waktu tunda $t_{\\text{delay}}$:
   $$
   t_{\\text{delay}} = -R C \\cdot \\ln\\left(1 - \\frac{V_{\\text{IH}}}{V_{\\text{DD}}}\\right) = -R C \\cdot \\ln(1 - 0{,}7) \\approx 1{,}204 \\cdot R C
   $$
   Jika dipilih kapasitor keramik $C = 100\\text{ nF}$ dan diinginkan tunda debounce $t_{\\text{delay}} = 10\\text{ ms}$:
   $$
   R = \\frac{t_{\\text{delay}}}{1{,}204 \\cdot C} = \\frac{10 \\times 10^{-3}\\text{ s}}{1{,}204 \\times 100 \\times 10^{-9}\\text{ F}} \\approx 83\\text{ k}\\Omega \\quad (\\text{digunakan resistor standar } 82\\text{ k}\\Omega)
   $$
   Resistor *pull-up* $82\\text{ k}\\Omega$ dan kapasitor $100\\text{ nF}$ menjamin osilasi transien teredam sepenuhnya sebelum sinyal diteruskan ke pin GPIO mikrokontroler.
`,
    extraReferences: [
      '- JEDEC Standard JESD8C.01, *Interface Standard for Nominal 3 V/3.3 V Supply Digital Integrated Circuits*, JEDEC Solid State Technology Association.',
      '- Ganssle, J., *A Guide to Debouncing*, The Ganssle Group, Whitepaper Technical Report.'
    ]
  },
  {
    slug: 'chapter-10',
    targetBeforeHeading: '### 6. Common Mistakes & Troubleshooting Capstone',
    mathMarkdown: `### 5.1 Model Matematis Estimasi Daya Sistem & Akurasi Sensor Lingkungan (Mathematical Foundations)

Pada tahap integrasi sistem capstone embedded (Chapter 10), integrasi multi-sensor dan aktuator memerlukan pemodelan konsumsi energi serta propagasi galat pengukuran:

1. **Kombinasi Ketidakpastian Pengukuran Multi-Sensor (Measurement Uncertainty Propagation)**:
   Jika parameter indeks kenyamanan termal $H$ bergantung pada suhu $T$ dan kelembaban relatif $RH$ melalui fungsi analitik $H = f(T, RH)$, maka varians ketidakpastian baku gabungan $u_c(H)$ sesuai pedoman ISO/IEC Guide 98-3 (GUM) dihitung melalui:
   $$
   u_c^2(H) = \\left( \\frac{\\partial f}{\\partial T} \\right)^2 u^2(T) + \\left( \\frac{\\partial f}{\\partial RH} \\right)^2 u^2(RH) + 2 \\left( \\frac{\\partial f}{\\partial T} \\right) \\left( \\frac{\\partial f}{\\partial RH} \\right) u(T, RH)
   $$
   Untuk sensor suhu independen dengan deviasi baku $u(T) = 0{,}2\\,^\\circ\\text{C}$ dan sensor kelembaban dengan $u(RH) = 1{,}5\\%$, tanpa kovarians ($u(T, RH) = 0$), kontribusi galat terisolasi secara kuadratik.

2. **Model Energi Rata-Rata Multi-Kondisi (Worked Engineering Example)**:
   Sistem beroperasi dalam siklus periodik dengan durasi sampling $t_{\\text{sample}} = 0{,}5\\text{ s}$ pada arus aktif $I_{\\text{active}} = 65\\text{ mA}$ (CPU 160 MHz + pembacaan I2C/ADC), durasi penyalaan aktuator buzzer/LED $t_{\\text{act}} = 0{,}1\\text{ s}$ pada arus $I_{\\text{act}} = 25\\text{ mA}$, dan waktu siaga tanpa radio $t_{\\text{idle}} = 4{,}4\\text{ s}$ pada arus $I_{\\text{idle}} = 12\\text{ mA}$ dalam periode total $T_{\\text{period}} = 5{,}0\\text{ s}$:
   $$
   I_{\\text{avg}} = \\frac{I_{\\text{active}} \\cdot t_{\\text{sample}} + I_{\\text{act}} \\cdot t_{\\text{act}} + I_{\\text{idle}} \\cdot t_{\\text{idle}}}{T_{\\text{period}}}
   $$
   Substitusi nilai:
   $$
   I_{\\text{avg}} = \\frac{(65 \\times 0{,}5) + (25 \\times 0{,}1) + (12 \\times 4{,}4)}{5{,}0} = \\frac{32{,}5 + 2{,}5 + 52{,}8}{5{,}0} = \\frac{87{,}8}{5{,}0} = 17{,}56\\text{ mA}
   $$
   Untuk baterai Li-Ion dengan kapasitas nominal $C_{\\text{bat}} = 2000\\text{ mAh}$ dan faktor degradasi praktis $\\eta = 0{,}85$, perkiraan masa pakai operasional kontinu $t_{\\text{life}}$ adalah:
   $$
   t_{\\text{life}} = \\frac{C_{\\text{bat}} \\cdot \\eta}{I_{\\text{avg}}} = \\frac{2000 \\times 0{,}85}{17{,}56} \\approx 96{,}8\\text{ jam } (\\sim 4{,}03\\text{ hari})
   $$
   Perhitungan ini membuktikan bahwa tanpa penerapan mode sleep mendalam (*deep sleep*), perangkat tidak dapat beroperasi berbulan-bulan dengan daya baterai portabel.
`,
    extraReferences: [
      '- JCGM 100:2008 (GUM), *Evaluation of measurement data — Guide to the expression of uncertainty in measurement*, BIPM/ISO/IEC.',
      '- Espressif Systems, *ESP32 Hardware Design Guidelines*, Technical Documentation.'
    ]
  },
  {
    slug: 'chapter-11',
    targetBeforeHeading: '### 6. Alur Troubleshooting Konektivitas IoT Berlapis (Bottom-Up)',
    mathMarkdown: `### 5.1 Model Matematis Transmisi Sinyal & Perhitungan Throughput Efektif (Mathematical Foundations)

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
    targetBeforeHeading: '### 7. Common Mistakes & Troubleshooting',
    mathMarkdown: `### 6.1 Model Matematis Propagasi Radio Wi-Fi & Link Budget (Mathematical Foundations)

Konektivitas Wi-Fi (IEEE 802.11 b/g/n) pada frekuensi $2{,}4\\text{ GHz}$ mengalami redaman daya propagasi di ruang bebas (*Free-Space Path Loss* / FSPL) yang dirumuskan oleh persamaan Friis:

1. **Redaman Ruang Bebas (Free-Space Path Loss)**:
   $$
   \\text{FSPL}_{\\text{dB}} = 20 \\log_{10}(d) + 20 \\log_{10}(f) - 147{,}55
   $$
   di mana jarak $d$ dinyatakan dalam meter (m) dan frekuensi transmisi $f$ dalam Hertz (Hz). Untuk frekuensi tengah Wi-Fi kanal 6 ($f = 2{,}437\\text{ GHz} = 2{,}437 \\times 10^9\\text{ Hz}$):
   $$
   \\text{FSPL}_{\\text{dB}}(d) = 20 \\log_{10}(d) + 20 \\log_{10}(2{,}437 \\times 10^9) - 147{,}55 = 20 \\log_{10}(d) + 187{,}74 - 147{,}55 = 20 \\log_{10}(d) + 40{,}19\\text{ dB}
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
    targetBeforeHeading: '### 7. Common Mistakes & Troubleshooting',
    mathMarkdown: `### 6.1 Landasan Matematis: Overhead Protokol HTTP & Analisis Latensi REST (Mathematical Foundations)

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
    slug: 'chapter-14',
    targetBeforeHeading: '### 6. Common Mistakes & Troubleshooting',
    mathMarkdown: `### 5.1 Landasan Matematis: Efisiensi Protokol MQTT & Beban Jaringan Brokering (Mathematical Foundations)

Protokol MQTT (OASIS Standard) dirancang untuk meminimalkan beban komputasi dan bandwidth pada jaringan berdaya terbatas:

1. **Struktur Header Paket MQTT Fixed Header**:
   Header tetap paket MQTT hanya membutuhkan ukuran minimum 2 byte ($B_{\\text{fixed}} = 2\\text{ byte}$), terdiri atas:
   - Byte 1: Tipe paket kontrol (4 bit) + Flag kontrol (4 bit, misal QoS, DUP, RETAIN).
   - Byte 2: *Remaining Length* terenkode variabel (1 hingga 4 byte).
   Beban transmisi paket PUBLISH tanpa variabel header identifikasi (QoS 0) dengan panjang topik $L_{\\text{topic}}$ dan payload $L_{\\text{data}}$ adalah:
   $$
   L_{\\text{MQTT}} = 2 + 2 + L_{\\text{topic}} + L_{\\text{data}} = 4 + L_{\\text{topic}} + L_{\\text{data}}
   $$

2. **Perbandingan Efisiensi Bandwidth MQTT vs HTTP (Worked Example)**:
   Sebuah stasiun pemantau cuaca mengirimkan payload JSON 30 byte setiap 10 detik ke server.
   - Pada HTTP: Request memerlukan $\\approx 185\\text{ byte}$ dan Response server memerlukan $\\approx 120\\text{ byte}$, total $305\\text{ byte}$ per transaksi. Ditambah handshake TCP ($3 \\times 54 = 162\\text{ byte}$), total per transaksi mencapai $467\\text{ byte}$.
   - Pada MQTT (koneksi persist tetap terbuka): Satu paket PUBLISH dengan topik \`itera/farm/t1\` (13 karakter) memerlukan:
   $$
   L_{\\text{MQTT}} = 4 + 13 + 30 = 47\\text{ byte}
   $$
   Ditambah header TCP/IP (40 byte), total paket hanya $87\\text{ byte}$ tanpa perlunya response balik pada QoS 0.
   Penghematan data per jam untuk pengiriman setiap 10 detik ($N = 360\\text{ sampel/jam}$):
   $$
   \\Delta V = 360 \\times (467\\text{ B} - 87\\text{ B}) = 360 \\times 380\\text{ B} = 136.800\\text{ byte} \\approx 133{,}6\\text{ KiB/jam}
   $$
   Dalam 1 bulan (720 jam), penghematan kuota data mencapai $\\approx 96{,}2\\text{ MiB}$ per perangkat. Pengurangan volume sebesar $81{,}3\\%$ ini sangat krusial pada penerapan kartu SIM IoT seluler komersial.
`,
    extraReferences: [
      '- OASIS Standard, *MQTT Version 5.0 Specification*, OASIS Open, 2019.',
      '- OASIS Standard, *MQTT Version 3.1.1 Specification*, OASIS Open, 2014.'
    ]
  },
  {
    slug: 'chapter-15',
    targetBeforeHeading: '### 7. Common Mistakes & Troubleshooting',
    mathMarkdown: `### 6.1 Model Matematis Keandalan QoS & Analisis Probabilitas Pengiriman Pesan (Mathematical Foundations)

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
    slug: 'chapter-16',
    targetBeforeHeading: '### 6. Common Mistakes & Troubleshooting',
    mathMarkdown: `### 5.1 Landasan Matematis: Kapasitas Saluran Serial, Batas Jarak I2C & Baud Rate Error (Mathematical Foundations)

Antarmuka komunikasi serial perangkat keras (UART, I2C, SPI) diatur oleh batas fisik waktu propagasi dan kapasitansi saluran:

1. **Toleransi Galat Baud Rate UART**:
   Komunikasi UART asinkron mengandalkan clock lokal di kedua simpul tanpa jalur clock bersama. Pembacaan bit data dilakukan pada pertengahan periode bit ($t_{\\text{sample}} = 0{,}5 \\cdot T_{\\text{bit}}$). Akumulasi pergeseran fase waktu sepanjang 1 frame (1 Start bit + 8 Data bit + 1 Stop bit = 10 bit) tidak boleh melebihi $\\pm 0{,}5 \\cdot T_{\\text{bit}}$. Syarat batas deviasi frekuensi baud rate maksimum $\\Delta f_{\\text{baud}}$ secara analitis adalah:
   $$
   |\\Delta f_{\\text{baud}}| < \\frac{0{,}5}{10} \\times 100\\% = 5\\%
   $$
   Dalam standar rekayasa industri, deviasi baud rate kumulatif antara pemancar dan penerima wajib dijaga di bawah $|\\text{Error}| \\le 2{,}0\\%$ untuk mencegah salah baca data (*framing error*).

2. **Perhitungan Batas Jarak & Kapasitansi Bus I2C (Worked Example)**:
   Standar NXP I2C Bus Specification menetapkan waktu naik sinyal maksimum (*rise time*) untuk mode Standard ($100\\text{ kHz}$) adalah $t_r \\le 1000\\text{ ns}$, dan untuk Fast Mode ($400\\text{ kHz}$) adalah $t_r \\le 300\\text{ ns}$. Rise time ditentukan oleh konstanta waktu sirkuit resistor pull-up $R_p$ dan kapasitansi total bus $C_{\\text{bus}}$:
   $$
   t_r = R_p \\cdot C_{\\text{bus}} \\cdot \\ln\\left( \\frac{V_{\\text{DD}} - 0{,}1 \\cdot V_{\\text{DD}}}{V_{\\text{DD}} - 0{,}7 \\cdot V_{\\text{DD}}} \\right) = R_p \\cdot C_{\\text{bus}} \\cdot \\ln\\left( \\frac{0{,}9}{0{,}3} \\right) \\approx 1{,}0986 \\cdot R_p \\cdot C_{\\text{bus}}
   $$
   Maka batas kapasitansi bus maksimum untuk resistor pull-up $R_p = 4{,}7\\text{ k}\\Omega$ pada Fast Mode ($t_r = 300\\text{ ns}$) adalah:
   $$
   C_{\\text{bus,max}} = \\frac{t_r}{1{,}0986 \\cdot R_p} = \\frac{300 \\times 10^{-9}}{1{,}0986 \\times 4700} \\approx 58\\text{ pF}
   $$
   Jika kabel jumper memiliki kapasitansi parasitik $\\approx 50\\text{ pF/meter}$, panjang fisik kabel I2C maksimum pada frekuensi 400 kHz tidak boleh melebihi $1{,}1\\text{ meter}$. Fakta matematis ini membuktikan bahwa I2C murni ditujukan untuk komunikasi antar-chip di dalam satu PCB (*intra-board bus*).
`,
    extraReferences: [
      '- UM10204, *I2C-bus specification and user manual*, Rev. 7.0, NXP Semiconductors, 2021.',
      '- Texas Instruments, *Understanding the I2C Bus*, Application Report SLVA704.'
    ]
  },
  {
    slug: 'chapter-17',
    targetBeforeHeading: '### 6. Implementasi Firmware & Troubleshooting Umum',
    mathMarkdown: `### 5.1 Landasan Matematis: BLE Advertising Interval & Perhitungan Konsumsi Energi (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 5.1 Landasan Matematis: Sinkronisasi Waktu SNTP & Kapasitas Buffer Deret Waktu (Mathematical Foundations)

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
    targetBeforeHeading: '### 5. Panduan Troubleshooting Capstone',
    mathMarkdown: `### 4.1 Landasan Matematis: Ketersediaan Sistem (Availability) & MTBF Capstone (Mathematical Foundations)

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
  },
  {
    slug: 'chapter-22',
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Buffer Dimensioning & Latensi Pemrosesan Gateway (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Throughput Aliran Peristiwa & Latensi Pipeline Node-RED (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Skalabilitas Registri & Interval Heartbeat Adaptif (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Kompleksitas Komputasi Kriptografi Elliptic Curve (ECDSA) (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Probabilitas Kegagalan Flash & Model Pemulihan Rollback (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Ketersediaan Layanan Pipeline End-to-End & Analisis Latensi P99 (Mathematical Foundations)

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
   T_{\\text{down}} = 8760 \\times (1 - 0{,}9974) = 8760 \\times 0{,}0259 \\approx 22{,}78\\text{ jam/tahun}
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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Penjadwalan Rate-Monotonic (RMA) & Schedulability Bounds (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Polinomial CRC-16 Modbus & Verifikasi Integritas Frame (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Topologi Jaringan Mesh Thread & Routing Distance-Vector (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Distribusi Consistent Hashing & Penyeimbangan Beban Sharding (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 3.1 Landasan Matematis: Kuantifikasi Skor Risiko DREAD & Entropi Diferensial Privasi (Mathematical Foundations)

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
    targetBeforeHeading: '## Latihan',
    mathMarkdown: `### 2.1 Landasan Matematis: Metrik Efektivitas Sistem Gabungan (OEE) & Ketersediaan Capstone (Mathematical Foundations)

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

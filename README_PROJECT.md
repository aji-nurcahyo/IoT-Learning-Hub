# README_PROJECT — IoT Learning Hub Project Memory & Continuation Guide

> **MANDATORY NOTICE FOR AI AGENTS:**  
> At the beginning of every new AI Agent session, read this document (`README_PROJECT.md`) first to restore the complete project context, development history, architectural decisions, permanent rules, and current project status.  
> **DO NOT RESTART OR REBUILD THE PROJECT FROM SCRATCH.**  
> The core curriculum (Chapters 01–40) and all five specialization tracks (Tracks A–E, 30 modules) are fully implemented, verified, tested, and published.

---

## 1. Identitas, Tujuan, dan Batasan Proyek

- **Nama Proyek:** Internet of Things Learning Hub (*From Connected Devices to Intelligent Systems*)
- **Pencipta & Pengembang:** **Aji Pamungkas Tri Nurcahyo**, Institut Teknologi Sumatera (ITERA).
- **Repositori Resmi:** [https://github.com/aji-nurcahyo/IoT-Learning-Hub.git](https://github.com/aji-nurcahyo/IoT-Learning-Hub.git)
- **Alamat Publikasi:** [https://aji-nurcahyo.github.io/IoT-Learning-Hub/](https://aji-nurcahyo.github.io/IoT-Learning-Hub/)
- **Karakter & Tujuan Proyek:**  
  Perpustakaan sumber daya pembelajaran terbuka (*web-based educational resource library*) yang memuat kurikulum berjenjang dari fondasi elektronika, pemrograman embedded, protokol komunikasi nirkabel/kabel, arsitektur edge gateway, hingga sistem cerdas berbasis Edge AI dan spesialisasi domain industri.
- **Batasan Proyek (Non-Goals):**
  - **BUKAN Learning Management System (LMS):** Tidak menyediakan sistem login user, absensi, pelacakan progress berbasis database user, gradebook, forum diskusi, atau manajemen kuis dinamis.
  - **BUKAN Live IoT Platform / Cloud Broker:** Tidak berfungsi sebagai broker MQTT publik atau server telemetri live untuk ribuan simpul nyata; semua visualisasi dan pipeline menggunakan simulasi komputasi mandiri dan demonstrasi lokal.
  - **Zero Paid Cloud / Hardware Requirements:** Materi dirancang agar dapat dipelajari secara mandiri tanpa kewajiban membeli perangkat keras khusus atau berlangganan layanan cloud berbayar (tersedia alternatif Path A software simulation untuk seluruh modul).

---

## 2. Arsitektur Website, Technology Stack & Struktur Folder

### 2.1 Technology Stack
- **Runtime & Toolchain:** Node.js 24 LTS, npm.
- **Frontend Core:** React 19, TypeScript 5.9 (Strict mode), Vite 7.
- **Presentasi & Rendering:** Reveal.js 5 (slide deck viewer), `react-markdown`, `remark-math`, `rehype-katex` (KaTeX LaTeX rendering), `rehype-highlight` (sintaks kode).
- **Tipografi & Ikonografi:** `@fontsource-variable/dm-sans`, `@fontsource-variable/manrope`, `lucide-react`.
- **Validasi Skema:** Zod 4.
- **Pengujian & CI:** Node.js native test runner (`tsx --test`), ESLint 9, Playwright E2E browser tests, Python 3.12 (simulasi komputasi deterministik).

### 2.2 Struktur Folder Repository
```text
Internet Of Things/
├── .agents/skills/              # Antislop skills bundle (core, ui, copy, code, layout, human)
├── .github/workflows/           # CI/CD deployment GitHub Actions (pages.yml)
├── content/
│   ├── catalog.json             # Authoritative catalog: 40 core chapters, 5 specialization tracks
│   └── schemas/                 # JSON Schemas untuk bab dan slide deck
├── docs/                        # Laporan verifikasi teknis, review akademik, dan audit Phase 1-7
├── public/
│   ├── .nojekyll                # Bypass Jekyll processing di GitHub Pages
│   ├── content/                 # Konten Chapter 01-40 & Specialization Track A-E
│   │   ├── chapter-01 .. 40/    # 8 canonical files + src/ firmware/sim
│   │   └── specialization/      # 5 Tracks (track-a .. track-e) masing-masing 6 modul
│   ├── guides/                  # Getting Started guide
│   └── templates/               # Markdown, slide, and evidence templates
├── scripts/
│   ├── base.ts                  # Base path sanitization & normalization
│   ├── http-test.ts             # Static multi-base server HTTP test
│   ├── validate.ts              # Publication guard & SHA-256 evidence checker
│   └── spec_module_generator.ts # Canonical bundle generator for specialization
├── src/
│   ├── Deck.tsx                 # Reveal.js presentation viewer
│   ├── Reading.tsx              # Markdown reading mode component with TOC
│   ├── catalog.ts               # Runtime catalog loader & search filters
│   ├── config.ts                # Application configuration & base path
│   ├── main.tsx                 # Root router & layout component
│   └── schema.ts                # TypeScript interfaces & Zod validation
├── tests/                       # Unit tests, browser tests, & integrity suites
├── AGENTS.md                    # Permanent rules for AI Agents
├── README.md                    # Public user-facing README
└── README_PROJECT.md            # Master memory & continuation instructions (Dokumen ini)
```

### 2.3 Metadata, Routing & Base Path
- **Routing:** Hash-based routing (`#/chapter/:id`, `#/track/:trackId/module/:modId`, `#/slides/...`, `#/guides/getting-started`) memastikan kompatibilitas penuh dengan hosting statis GitHub Pages tanpa ketergantungan pada server-side rewrite.
- **Base Path:** Default `/iot-learning-hub/` (lokal) dan `/IoT-Learning-Hub/` (GitHub Pages). Semua aset internal mengacu pada `import.meta.env.BASE_URL`.

---

## 3. Status 40 Core Chapters dan 30 Specialization Modules

Seluruh **70 modul pembelajaran** telah selesai ditulis, divalidasi, dan berstatus aktif:

### 3.1 Core Curriculum (40 Chapters — Status: `published`)
- **Level 1 (Chapter 01–10): Fundamentals & Prototyping**
  - Ch 01: IoT Ecosystem & Trade-offs
  - Ch 02: Architecture & Requirements
  - Ch 03: Electronics & Power Rails
  - Ch 04: Microcontrollers & Memory
  - Ch 05: Embedded C++ & Build Systems
  - Ch 06: GPIO & Debouncing
  - Ch 07: Analog Sensors & ADC
  - Ch 08: PWM, Actuators & Relays
  - Ch 09: Hardware Timers, Watchdog & FSM
  - Ch 10: Embedded Capstone Prototype
- **Level 2 (Chapter 11–20): Systems & Connectivity**
  - Ch 11: Wireless Networking Fundamentals
  - Ch 12: Wi-Fi Provisioning & Station Mode
  - Ch 13: HTTP, REST & WebSockets
  - Ch 14: MQTT Protocol, QoS & LWT
  - Ch 15: CoAP & CBOR Optimization
  - Ch 16: Serial Buses (I2C, SPI, UART)
  - Ch 17: Bluetooth Low Energy (BLE) GATT
  - Ch 18: LoRa & LoRaWAN Communications
  - Ch 19: Security, TLS & Crypto Keystore
  - Ch 20: Connected Node Capstone System
- **Level 3 (Chapter 21–30): Data, Gateways & IoT Applications**
  - Ch 21: Data Models & Telemetry Schema
  - Ch 22: Edge Gateways & Multiplexing
  - Ch 23: Edge Processing & Filtering Rules
  - Ch 24: Node-RED & Low-Code Automation
  - Ch 25: Time-Series Databases (TSDB)
  - Ch 26: Dashboards, Metrics & Alerts
  - Ch 27: Device Management & Digital Twins
  - Ch 28: Mutual TLS & Token Security
  - Ch 29: Dual-Bank A/B OTA Updates
  - Ch 30: Edge Gateway Capstone Platform
- **Level 4 (Chapter 31–40): Advanced & Intelligent IoT Systems**
  - Ch 31: Low-Power Design & Sleep Modes
  - Ch 32: Real-Time OS (FreeRTOS)
  - Ch 33: Modbus RTU & OPC UA Fieldbuses
  - Ch 34: Thread Mesh & Matter Standard
  - Ch 35: Edge AI & TinyML Quantization
  - Ch 36: Thermal Digital Twins & Simulation
  - Ch 37: Broker Clustering & Backpressure
  - Ch 38: Chaos Testing & MTBF Resilience
  - Ch 39: Threat Modeling (STRIDE/DREAD)
  - Ch 40: Advanced Intelligent IoT Capstone

### 3.2 Specialization Tracks (5 Tracks, 30 Modules — Status: `available`)
- **Track A: Smart Home & Building Automation (Modul A01–A06)**
  - A01: Coexistence & Co-channel CIR
  - A02: IAQ & Demand-Controlled Ventilation
  - A03: Matter & Thread Commissioning
  - A04: Building Microgrid Peak-Shaving
  - A05: Life-Safety Interlocks & Evacuation
  - A06: Building Capstone Controller
- **Track B: Industrial IoT & Predictive Maintenance (Modul B01–B06)**
  - B01: Purdue Model & IEC 62443 Security
  - B02: High-Frequency Vibration ADC
  - B03: FFT & Envelope Signal Processing
  - B04: Modbus RTU Industrial Gateways
  - B05: Asset Reliability & Weibull Modeling
  - B06: Predictive Maintenance Capstone
- **Track C: Smart Agriculture & Environmental Monitoring (Modul C01–C06)**
  - C01: Soil Moisture Physics & Topp Model
  - C02: Sensor Calibration, GUM & Drift
  - C03: LoRaWAN Canopy Path Loss
  - C04: Solar Harvesting & Supercapacitors
  - C05: FAO-56 Penman-Monteith Irrigation
  - C06: Agricultural Capstone Network
- **Track D: AIoT & Edge Intelligence (Modul D01–D06)**
  - D01: Microcontroller Neural Constraints
  - D02: Audio Feature Extraction (MFCC)
  - D03: Quantization & INT8 Inference
  - D04: Extended Kalman Filter (EKF) Fusion
  - D05: Concept Drift & Continuous Learning
  - D06: Multimodal AIoT Capstone
- **Track E: IoT for Telecommunications & Smart Cities (Modul E01–E06)**
  - E01: FIWARE NGSI-LD Multi-Tenant Platform
  - E02: Urban RF Propagation (COST 231 Hata)
  - E03: Cellular IoT (NB-IoT/LTE-M) & PSM/eDRX
  - E04: Municipal Contention ALOHA & M/G/1
  - E05: Geospatial Telemetry, Geofence & H3
  - E06: City-Scale Multi-Tenant Capstone

---

## 4. Struktur Resource Pembelajaran & Publication Guard

### 4.1 Bundel Kanonikal per Modul
Setiap bab dan modul spesialisasi wajib memiliki bundel file lengkap:
1. `reading.md`: Teks akademik komprehensif, tujuan pembelajaran, landasan matematika, panduan implementasi, latihan, penugasan, dan referensi primer.
2. `slides.json`: Slide presentasi interaktif Reveal.js (format `{ title, body, notes }`).
3. `code.md`: Walkthrough arsitektur kode dan instruksi eksekusi.
4. `diagram.svg`: Diagram arsitektur teknis mandiri berbasis SVG (responsif, skema warna gelap #0f172a).
5. `exercises.md`: Latihan terstruktur dan pembahasan soal rekayasa.
6. `assignment.md`: Penugasan mandiri disertai tabel rubrik penilaian objektif 100 poin.
7. `review.md`: Laporan telaah sejawat (*peer-review evaluation*).
8. `outputs.md`: Rekaman output eksekusi simulator atau log build perangkat keras.
9. `src/<script>.py`: Skrip simulasi komputasi deterministik berbasis Python 3 standar tanpa library pihak ketiga yang berat.

### 4.2 Publication Guard (`scripts/validate.ts`)
Publication Guard adalah mekanisme otomatis yang memverifikasi integritas katalog:
- Menolak resource yang hilang atau memiliki path traversal.
- Menolak penerbitan bab jika evidence hash tidak cocok.
- Memastikan setiap bab memiliki rubrik total tepat 100 poin.
- Memastikan tidak ada placeholder atau link rusak.

---

## 5. Riwayat Pengembangan Phase 1–7

- **Phase 1 & 2:** Perancangan arsitektur fondasi web, layout responsif, Markdown/KaTeX/Reveal.js viewer, dan implementasi materi Chapter 01–20 beserta verifikasi perangkat keras ESP32.
- **Phase 3:** Pengembangan materi Level 3 (Chapter 21–30) mencakup edge gateway, Node-RED, time-series database, dan pembaruan OTA dual-bank A/B.
- **Fix GitHub Actions LF Hashing:** Standardisasi hashing SHA-256 menggunakan normalisasi byte LF lintas Windows dan Ubuntu (`.gitattributes`).
- **Phase 4:** Pengembangan materi Level 4 (Chapter 31–40) mencakup FreeRTOS, Modbus/OPC UA, Thread/Matter, TinyML INT8 quantization, Digital Twins, dan threat modeling.
- **Phase 5:** Academic Deepening — Penguatan matematika formal (persamaan KaTeX eksplisit, penurunan rumus, worked numerical examples, dan audit 100-poin).
- **Phase 6A:** Perancangan kurikulum dan arsitektur 5 Specialization Tracks (A–E, 30 modul) beserta capstone design dan prerequisite map.
- **Phase 6B, 6C, 6D:** Implementasi penuh Wave 1 (Tracks B & D), Wave 2 (Tracks C & A), dan Wave 3 (Track E) lengkap dengan 11 berkas kanonikal per modul dan simulasi komputasi Python terverifikasi.
- **Phase 7:** Audit independen menyeluruh terhadap 70 modul (inventarisasi konten, validasi matematis independen, reproduksibilitas ilmiah, evaluasi defensif keamanan/privasi, UI/UX, dan publikasi final ke GitHub Pages).

---

## 6. Kebijakan Permanen Anti-Slop (`DURING` Mode)

Berdasarkan aturan pada `AGENTS.md`:
- **Mode Aktif:** **`DURING`** (Terkunci permanen, tidak boleh menanyakan pemilihan mode lagi).
- **Cakupan:** Teks akademik, kode sumber, komentar kode, tata letak mobile, aksesibilitas, diagram SVG, dan slide deck.
- **Prinsip Utama:**
  - Kedalaman teknis dan ketepatan matematika lebih diutamakan daripada estetika permukaan.
  - Hilangkan seluruh kata pengisi klise AI (*slop*) seperti: *"In today's fast-paced digital world"*, *"Delve into"*, *"Needless to say"*, atau kalimat meta-komentari yang tidak informatif.
  - Pertahankan komponen desain yang sudah ada (tidak mendesain ulang UI secara acak).
  - Lakukan audit anti-slop setelah setiap tahap penyelesaian rilis.

---

## 7. Standar Bahasa dan Terminologi

- **Bahasa Pengantar:** Bahasa Indonesia akademik formal yang lugas, presisi, dan terstruktur.
- **Terminologi Teknis:** Wajib mempertahankan istilah teknis bahasa Inggris standar industri yang sudah mapan untuk mencegah kerancuan makna (misalnya: *Power Saving Mode*, *Coverage Enhancement*, *Resource Block*, *Ray-Casting*, *Point-in-Polygon*, *Deadband*, *Hysteresis*, *Double Buffering*, *FreeRTOS*, *TinyML*, *Envelope Analysis*).
- **Matematika & KaTeX:** Rumus ditulis menggunakan KaTeX standard. Hindari tanda dolar literal yang tidak di-escape dalam teks naratif.

---

## 8. Sistem Pengujian & Integritas Bukti SHA-256

Repositori dilengkapi rangkaian pengujian otomatis yang harus selalu lulus $100\%$:

```powershell
# Jalankan seluruh rangkaian regresi
npm run check

# Rincian perintah individual:
npm run lint           # ESLint pada src, scripts, vite.config.ts
npm test               # 37 unit test mencakup chapter, hashing, & 5 track
npm run check:content  # Publication Guard (scripts/validate.ts)
npm run typecheck      # TypeScript compilation check (tsc --noEmit)
npm run test:http      # Static multi-base server test (754 files across 3 paths)
npm run test:browser   # Playwright E2E browser tests (Desktop & Mobile)
```

### Integritas SHA-256
- Hashing teks dinormalisasi ke format **LF** (`\n`) sebelum di-hash via SHA-256 untuk memastikan hasil identik di lingkungan Windows (CRLF) dan Linux/GitHub Actions runner (LF).
- File biner di-hash secara raw byte.

---

## 9. Konfigurasi GitHub Pages & CI/CD Deployment

- **Remote:** `https://github.com/aji-nurcahyo/IoT-Learning-Hub.git`
- **Branch Produksi:** `main`
- **GitHub Actions Workflow:** [`.github/workflows/pages.yml`](.github/workflows/pages.yml)
  - Otomatis terpicu pada setiap push ke branch `main`.
  - Menjalankan `npm ci` dan `npm run check` pada container Ubuntu Latest Node.js 24.
  - Membangun artefak statis `dist/` dengan base path `/IoT-Learning-Hub/` dan menyalin `index.html` ke `404.html` untuk fallback SPA.
  - Mengunggah dan mempublikasikan halaman ke GitHub Pages.
- **Push Policy:** Wajib menggunakan Fast-Forward normal push (`git push origin main`). **DILARANG MENGGUNAKAN `git push --force`**.

---

## 10. Status Terakhir & Maintenance yang Relevan

- **Status Saat Ini:** **PRODUCTION RELEASED & LIVE** (Commit `87b5b8c` di-deploy secara sukses).
- **Tugas Maintenance / Enhancement Masa Depan (Bila Diminta Pengguna):**
  - Pemeliharaan dependensi berkala via `npm audit` dan update versi library.
  - Penyempurnaan tipografi atau perbaikan kecil (*errata*) pada teks bacaan jika ada feedback kurikulum.
  - Pemantauan masa aktif tautan eksternal (*broken link checker*) pada daftar referensi.

---

## 11. Larangan Mutlak bagi AI Agent (Strict Guardrails)

1. **JANGAN MEMBANGUN ULANG (REBUILD) PROYEK:** Dilarang membuat repositori baru, menginisialisasi ulang Vite/React dari nol, atau merusak struktur komponen yang ada.
2. **JANGAN MENAMBAH FITUR LMS:** Dilarang membuat database user, backend login, sistem otentikasi siswa, sistem nilai dinamis, atau fitur kuis interaktif yang mengubah sifat proyek dari perpustakaan statis terbuka menjadi aplikasi LMS.
3. **JANGAN MENGUBAH KURIKULUM TANPA INSTRUKSI:** 40 Core Chapters dan 30 Modul Spesialisasi telah disetujui secara akademik. Jangan mengubah urutan, menghapus bab, atau mengganti silabus.
4. **JANGAN MENGABAIKAN ANTI-SLOP:** Mode `DURING` wajib selalu aktif.
5. **JANGAN MELAKUKAN UNAPPROVED PUSH:** Jangan pernah melakukan `git push` atau deployment tanpa persetujuan eksplisit dari pengguna.

---

## 12. Panduan Melanjutkan Pengembangan pada Sesi AI Agent Baru

Saat memulai sesi percakapan baru atau menerima instruksi lanjutan:

1. **Langkah 1 — Muat Konteks:**  
   Baca `README_PROJECT.md` dan `AGENTS.md`. Sadari bahwa proyek ini sudah berada pada status selesai dan terverifikasi penuh (Phase 1–7 complete).
2. **Langkah 2 — Periksa Status Repositori:**  
   Jalankan `git status` untuk memastikan working tree bersih dan branch berada di `main`.
3. **Langkah 3 — Verifikasi Kesehatan Sistem:**  
   Jalankan `npm run check:content` dan `npm test` untuk memastikan seluruh 70 modul dan 37 pengujian tetap dalam kondisi lulus.
4. **Langkah 4 — Tangani Permintaan Spesifik:**  
   Lakukan modifikasi hanya pada file yang ditargetkan oleh permintaan pengguna. Jangan melakukan refactoring liar pada file lain.
5. **Langkah 5 — Validasi & Lindungi Kualitas:**  
   Setelah melakukan perubahan, jalankan `npm run check` untuk memverifikasi bahwa perubahan tidak merusak linting, typecheck, test suites, atau publication guard.

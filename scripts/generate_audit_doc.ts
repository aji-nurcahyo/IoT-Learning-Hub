import fs from 'node:fs';
import path from 'node:path';
import { ChapterAudit } from './generate_audit_data';

const auditList: ChapterAudit[] = JSON.parse(fs.readFileSync('scripts/audit_output.json', 'utf8'));

let md = `# Audit Kualitas Akademik & Rekayasa — IoT Learning Hub (Phase 5)

Dokumen ini memuat audit komprehensif 40 bab kurikulum **Internet of Things Learning Hub** pada 4 level pembelajaran berdasarkan 7 dimensi mutu akademik dan keteknikan.

- **Proyek**: Internet of Things Learning Hub (*From Connected Devices to Intelligent Systems*)
- **Pengembang & Kurator**: Aji Pamungkas Tri Nurcahyo (Institut Teknologi Sumatera - ITERA)
- **Repositori**: \`https://github.com/aji-nurcahyo/IoT-Learning-Hub.git\`
- **Kebijakan Anti-Slop**: Permanent Active (Mode: **DURING**)
- **Tanggal Baseline Audit**: 18 November 2026

---

## 1. Rubrik Penilaian 7 Dimensi (Total 100 Poin)

| No | Dimensi Penilaian | Bobot Maksimal | Kriteria Penilaian Akademik & Rekayasa |
|---|---|---|---|
| 1 | **Kejelasan Konseptual & Penyelarasan Prasyarat** (D1) | 15 poin | Batasan ruang lingkup materi tajam, taksonomi konsep konsisten, prasyarat realistis, ketiadaan jargon kosong/meta-commentary. |
| 2 | **Kedalaman Teori & Ketepatan Teknis** (D2) | 20 poin | Menjelaskan *mekanisme internal* dan *underlying physical/protocol phenomena* secara presisi (bukan sekadar tutorial permukaan). |
| 3 | **Landasan Matematis & Contoh Numerik** (D3) | 15 poin | Penurunan rumus formal KaTeX (Hukum Ohm, Nyquist, Path Loss, ToA, Welford, Peukert, RMA, INT8 quantization) disertai step-by-step worked engineering calculation. |
| 4 | **Implementasi Praktis & Reproduksibilitas** (D4) | 20 poin | Source code mandiri/simulasi dapat dieksekusi 100%, pinout akurat, error handling eksplisit, verifikasi outputs teruji. |
| 5 | **Kualitas Asesmen & Penyelarasan Taksonomi Bloom** (D5) | 10 poin | Latihan kognitif bertingkat (C1–C6), tugas berbasis masalah nyata (PBL), rubrik penilaian analitik 100 poin. |
| 6 | **Rujukan Primer & Standar Industri** (D6) | 10 poin | Mengacu pada spesifikasi standar primer (IEEE, IETF RFC, ISO/IEC, 3GPP, ITU-T, vendor whitepapers/datasheets). |
| 7 | **Slide, Diagram, Aksesibilitas & Anti-Slop** (D7) | 10 poin | Diagram SVG teknis informatif, slide deck ringkas dan bermakna dengan presenter notes bernas, kontras WCAG AAA, zero slop. |

---

## 2. Ringkasan Evaluasi Baseline

- **Total Bab**: 40 bab (Level 1: 10 bab, Level 2: 10 bab, Level 3: 10 bab, Level 4: 10 bab).
- **Rata-rata Skor Baseline**: **84.0 / 100**.
- **Bab Prioritas Peningkatan (Skor < 85)**: 22 bab.
  - *Level 1 (Foundations)*: Membutuhkan formalisasi matematis (ADC step, resistor divider thermal drift, Nyquist sampling frequency, error propagation).
  - *Level 2 (Protocols & Networks)*: Membutuhkan derivasi eksak link budget (Friis FSPL), LoRa Time-on-Air (ToA) payload formula, CSMA/CA slot timing, dan packet overhead byte budget.
  - *Level 3 (Data & Gateways)*: Membutuhkan formulasi agregasi data stream (Welford recurrence), kompresi time-series (Gorilla XOR), dan model kriptografi TLS timing.
  - *Level 4 (Advanced Systems)*: Membutuhkan kalkulasi analitik RMA schedulability bounds, INT8 quantization scaling factor, dan pemodelan State-Space / Digital Twin thermal decay.

---

## 3. Matriks Audit 40 Bab (Detailed Evaluation Matrix)

| Bab | Judul Kurikulum | Level | D1 (15) | D2 (20) | D3 (15) | D4 (20) | D5 (10) | D6 (10) | D7 (10) | Total (100) | Status | Gap Utama & Rencana Pengayaan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
`;

for (const ch of auditList) {
  md += `| **${ch.slug.toUpperCase()}** | ${ch.title} | L${ch.levelId} | ${ch.d1} | ${ch.d2} | ${ch.d3} | ${ch.d4} | ${ch.d5} | ${ch.d6} | ${ch.d7} | **${ch.total}** | \`${ch.statusRating}\` | ${ch.gapSummary} |\n`;
}

md += `
---

## 4. Matriks Rujukan Standar & Spesifikasi Primer (Standards Mapping)

Setiap materi yang diperdalam wajib memuat rujukan otoritatif primer sesuai bidangnya:

1. **Embedded & Perangkat Fisik (Level 1)**:
   - IEEE 1451 (*Standard for a Smart Transducer Interface for Sensors and Actuators*).
   - ISO/IEC/IEEE 21451 (*Information technology — Smart transducer interface for sensors and actuators*).
   - Espressif Systems *ESP32 Technical Reference Manual & Datasheet* (Rev 4.x).
   - JEDEC Standard JESD8C.01 (*Interface Standard for Nominal 3 V/3.3 V Supply Digital Integrated Circuits*).
2. **Jaringan & Protokol Nirkabel (Level 2)**:
   - OASIS *MQTT Version 3.1.1 & MQTT Version 5.0 Specification*.
   - IETF RFC 7252 (*The Constrained Application Protocol - CoAP*).
   - LoRa Alliance *LoRaWAN Link Layer Specification v1.0.4 / v1.1*.
   - IEEE 802.11-2020 (*Wireless LAN Medium Access Control and Physical Layer Specifications*).
   - Bluetooth SIG *Bluetooth Core Specification v5.4*.
3. **Arsitektur Gateway & Data (Level 3)**:
   - IETF RFC 8446 (*The Transport Layer Security (TLS) Protocol Version 1.3*).
   - IETF RFC 5280 (*Internet X.509 Public Key Infrastructure Certificate and CRL Profile*).
   - NIST SP 800-146 (*Cloud Computing Synopsis and Recommendations*).
   - IEC 62443-4-2 (*Security for industrial automation and control systems — Technical security requirements for IACS components*).
4. **Sistem Lanjut, Edge AI & Industri (Level 4)**:
   - IEC 61158 / IEC 61784 (*Industrial communication networks — Fieldbus specifications*).
   - OPC Unified Architecture (OPC UA) IEC 62541-1 through IEC 62541-7.
   - CSA (Connectivity Standards Alliance) *Matter Core Specification Version 1.3*.
   - Thread Group *Thread 1.3.0 Specification*.
   - IEEE 1012 (*Standard for System, Software, and Hardware Verification and Validation*).

---

## 5. Rencana Aksi Bertahap (Roadmap Peningkatan Mutu)

1. **Level 1 (Chapter 01–10)**:
   - Tambahkan blok KaTeX penurunan rumus, model galat sensor ($u_c = \\sqrt{\\sum c_i^2 u_i^2}$), kuantisasi ADC ($Q = \\frac{V_{ref}}{2^N}$), dan worked numerical example terstruktur di setiap reading.md.
   - Perkaya rujukan standar IEEE/ISO/Espressif.
2. **Level 2 (Chapter 11–20)**:
   - Turunkan persamaan propagasi radio Friis ($FSPL = 20\\log_{10}(d) + 20\\log_{10}(f) - 147.55$), formula eksak Time-on-Air (ToA) LoRaWAN, dan analisis overhead protokol per paket data.
   - Sediakan tabel komparasi parameter terukur secara empiris.
3. **Level 3 (Chapter 21–30)**:
   - Tambahkan model rekursif Welford untuk varians online tanpa overflow, formula kompresi Delta-of-Delta Gorilla, dan verifikasi kriptografi TLS/ECDSA.
4. **Level 4 (Chapter 31–40)**:
   - Perluas kalkulasi penjadwalan real-time FreeRTOS (RMA bound $\\sum \\frac{C_i}{T_i} \\le n(2^{1/n}-1)$), kuantisasi bobot INT8 TinyML ($q = \\text{round}(r/S) + Z$), serta model State-Space Digital Twin.

Setiap bab setelah diperdalam akan diverifikasi kembali terhadap suite pengujian: \`npm run check:content\`, \`npm test\`, \`npm run check\`, dan browser UI regression testing.
`;

fs.writeFileSync('docs/ACADEMIC_DEEPENING_AUDIT.md', md, 'utf8');
console.log('Successfully written docs/ACADEMIC_DEEPENING_AUDIT.md');

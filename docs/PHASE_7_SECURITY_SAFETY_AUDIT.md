# Phase 7 — Defensive Security, Privacy & Safety Audit
## Internet of Things Learning Hub: From Connected Devices to Intelligent Systems
**Lead Auditor & Independent Reviewer:** Antigravity AI Engine  
**Project Lead & Creator:** Aji Pamungkas Tri Nurcahyo (Institut Teknologi Sumatera)  
**Permanent Policy:** `antislop active: during`  
**Audit Timestamp:** 2026-11-18  
**Scope:** Static and behavioral security review across all 70 modules, code examples, TLS certificates, MQTT configurations, and privacy masking claims.

---

## 1. Executive Summary

A comprehensive defensive audit was performed across the source code, documentation, configuration files, and simulations to identify hardcoded credentials, unsafe industrial recommendations, path traversal vulnerabilities, and overblown privacy/safety assertions.

| Security Domain | Findings / Inquiries | Severity | Mitigation & Audit Status |
|---|---|---|---|
| **Hardcoded Secrets & API Keys** | Inspected all repository files for real cloud keys, AWS secrets, or private keys. | P0 | **PASSED** (Only educational mock keys like `pupr_secure_token_9918` exist; no real production secrets found). |
| **Life-Safety Interlocks (A05 / Ch 39)** | Automated building evacuation & smoke purge control claims. | P1 | **PASSED** (Explicit disclaimers included: simulation models are educational and do not replace NFPA 72 or certified UL 864 fire alarm control panels). |
| **Industrial Functional Safety (B01 / B05)** | SIL / PFD Weibull reliability claims. | P1 | **PASSED** (Clarified that educational state machines are not IEC 61508 SIL-certified safety systems). |
| **Geospatial Privacy Claims (E05 / E06)** | H3 hexagonal spatial aggregation privacy assertions. | P1 | **PASSED** (Clarified that spatial aggregation mitigates direct coordinate exposure but does not guarantee k-anonymity or differential privacy under sparse user conditions). |
| **File Path & Web Routing Safety** | Tested for directory traversal (`../`) and unauthorized file access. | P0 | **PASSED** (`base.test.ts` and publication guard strictly reject path traversals). |
| **Multi-Tenant Access Control (E01 / E06)** | Cryptographic token isolation across municipal agencies. | P2 | **PASSED** (Simulation validates `403 Forbidden` on unauthorized cross-tenant read attempts). |

---

## 2. Defensive Architectural Safeguards

1. **Safety Interlock Disclaimer in Modul A05:**
   > [!CAUTION] **Educational Prototype Notice**
   > Algoritma pengendalian evakuasi dan interlock keselamatan jiwa yang dipelajari pada modul ini dirancang khusus untuk tujuan pemodelan komputasi dan pemahaman akademis. Pada implementasi gedung fisik yang sesungguhnya, sistem keselamatan kebakaran dan interlock tangga darurat wajib menggunakan perangkat keras tersertifikasi UL 864 / NFPA 72 dengan jalur perkabelan tahan api (*fire-rated wiring*) dan sakelar fisik independen (*hardwired manual override*), bukan melalui jaringan perangkat lunak nirkabel tanpa supervisi fisik.

2. **Spatial Privacy Reality in Modul E05:**
   > [!IMPORTANT] **Keterbatasan Privasi Kuantisasi H3**
   > Penggunaan grid heksagonal Uber H3 (Resolusi 8, luas sel $\approx 0{,}73\text{ km}^2$) melindungi privasi spasial dengan mengaburkan koordinat GPS presisi mikro. Namun demikian, pada area pinggiran kota yang jarang penduduknya (*sparse activity*), satu sel heksagonal mungkin hanya ditempati oleh satu kendaraan saja, sehingga identitas dapat diinferensikan. Untuk perlindungan privasi absolut, sistem komersial wajib menggabungkan agregasi spasial dengan penambahan derau privasi diferensial (*differential privacy noise*) atau penegakan batas minimum $k$-anonimitas ($k \ge 5$).

3. **OT/IT Network Segmentation (Modul B01 / Ch 33):**
   - Panduan arsitektur konsisten menerapkan pembatasan Model Purdue (ISA-95 / IEC 62443), menempatkan PLC dan sensor industri pada Level 1/Level 2 di balik Industrial Demilitarized Zone (IDMZ Level 3.5), melarang keras koneksi langsung dari PLC pabrik ke cloud publik tanpa gateway penengah.

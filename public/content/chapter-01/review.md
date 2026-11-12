# Laporan Review — Chapter 01

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-10
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk eksperimen hardware, serta bukti **Software (`iot_flow_demo.py`)** yang telah dieksekusi nyata.

## Hasil Pemeriksaan

1. **Keselarasan Kurikulum**: Seluruh topik Chapter 01 (definisi, evolusi, IoT vs Embedded vs CPS, 6 komponen ekosistem, aliran data uplink/downlink, tantangan keamanan/skala/keandalan, contoh telekomunikasi & agrikultur) tercakup lengkap.
2. **Struktur & Bahasa**: Menggunakan Bahasa Indonesia akademik yang konsisten dengan terminologi teknis Inggris sesuai `docs/TECHNICAL_LANGUAGE_GUIDE.md`.
3. **Kesesuaian Resource**:
   - `reading.md`: Memuat seluruh bagian wajib (`Tujuan pembelajaran`, `Prasyarat`, `Konsep dan teori`, `Latihan`, `Tugas`, `Ringkasan`, `Referensi`), KaTeX math, tabel GFM, dan SVG diagram.
   - `slides.json`: 16 slide ringkas dengan *notes* presenter dan tanpa branding Reveal.js pada tampilan pembelajar.
   - `exercises.md` & `assignment.md`: Lengkap dengan kunci pembahasan terpisah dan rubrik total 100 poin.
   - `code.md`, `src/iot_flow_demo.py`, `telemetry.csv`, `outputs.md`: Skrip dijalankan nyata di Python 3.12.10 dengan dataset sintetis.
4. **Keterbatasan**: Belum menggunakan *hardware* fisik maupun simulator mikrokontroler karena fokus chapter ini adalah fondasi konseptual dan alur data *end-to-end*.


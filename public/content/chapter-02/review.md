# Laporan Review — Chapter 02

- **Reviewer**: Aji Pamungkas Tri Nurcahyo (Self-Review Kurikulum & Teknis)
- **Tanggal**: 2026-11-10
- **Status Publikasi**: Layak dipublikasi dengan label verifikasi **Belum diuji (`untested`)** untuk pengujian hardware/jaringan nyata, disertai verifikasi **Software (`requirements_budget.py`)**.

## Hasil Pemeriksaan

1. **Cakupan Materi**: Mencakup model 3-lapis vs 5-lapis, *functional* & *non-functional requirements*, *system boundaries*, *trade-off* Edge vs Cloud, *use-case* & *block diagram*, dan studi kasus sistem monitoring suhu terdistribusi.
2. **Validasi Teknis**: Rumus *wire volume* dan *offline buffer* konsisten dengan implementasi `requirements_budget.py`. Angka perbandingan (88,4% penghematan dan $34\times$ percepatan latensi lokal) berasal langsung dari output eksekusi model tersebut dengan asumsi desain yang dinyatakan eksplisit.
3. **Kesesuaian Resource & Rubrik**: Seluruh 7 bagian wajib `reading.md` terpenuhi, `slides.json` berisi 16 slide ringkas tanpa label Reveal.js, serta `assignment.md` dan `catalog.json` berbagi rubrik identik total 100 poin.
4. **Keterbatasan**: Belum menguji latensi WAN aktual maupun perangkat *Gateway* fisik.


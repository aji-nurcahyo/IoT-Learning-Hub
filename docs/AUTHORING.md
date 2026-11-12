# Menulis chapter

1. Pilih entri di `content/catalog.json`; pertahankan id, slug, level, dan judul master curriculum. Perbaiki tujuan serta prasyarat sesuai lingkup.
2. Buat folder `public/content/chapter-NN/`. Salin template modul dan deck dari `public/templates/` di dalam proyek ini. Jangan menyalin materi proyek referensi.
3. Isi teori, contoh, latihan bertingkat, tugas, ringkasan, dan referensi. Lengkapi resource yang relevan. Tulis `not-applicable` beserta alasan substantif untuk yang tidak perlu, bukan untuk melewati syarat publikasi.
4. Set resource menjadi `available` hanya ketika file nyata tersedia. Path relatif terhadap `public`, misalnya `content/chapter-01/reading.md`. Tidak ada prefix base URL pada metadata. Renderer menerima Markdown dengan GFM table, semantic lists, links, fenced code, dan math `$...$` / `$$...$$`. HTML mentah tidak dieksekusi.
5. Deck JSON berisi array `{title, body, notes, fragment?}`. `body` mendukung Markdown yang sama. Pecah slide padat; uji desktop/mobile. Hash Reveal dimatikan agar tidak merusak routing.
6. Isi rubrik di metadata: `criterion`, `points`, `description`, total tepat 100. Bacaan/tugas harus konsisten dengan rubrik tersebut.
7. Untuk praktik hardware, set `hardware.required=true`, lengkapkan semua dokumen serta datasheet. Jangan menebak electrical ratings dari nama keluarga chip.
8. Simpan bukti asli dalam file public yang sudah disunting untuk menghapus secret. Catat `kind`, `environment`, `command`, `date`, `path`, `sha256`. Di PowerShell, `Get-FileHash -Algorithm SHA256 <file>`; simpan hash lowercase. Verifikasi software dapat memiliki `kind=software` tanpa mengklaim hardware teruji.
9. Reviewer menulis laporan, nama, tanggal, dan keterbatasan. Isi `review.report` dengan path file nyata. Jangan menggunakan boolean `reviewed` saja.
10. Ubah status menjadi `published` hanya setelah semua pemeriksaan lulus dan review manusia selesai. Jalankan `npm run check`, `npm run test:http`, dan `npm run test:browser`.

Schema runtime ada di `src/schema.ts`; ekspor JSON Schema dengan `npx tsx scripts/export-schema.ts` setelah perubahan. File JSON Schema membantu editor, sedangkan validasi filesystem/publication tetap dilakukan `scripts/validate.ts`.

## Label pengujian

| Label | Syarat | Tidak membuktikan |
| --- | --- | --- |
| Belum diuji | Batasan dijelaskan | Build atau perilaku perangkat |
| Compile-verified | Log compile, command, toolchain, hash | Perilaku fisik |
| Simulator-verified | Versi simulator, skenario, log, hash | Electrical/radio aktual |
| Hardware-verified | Board/revisi, setup, kondisi, output asli, hash | Semua konfigurasi di luar uji |

Simpan output aktual terpisah dari output yang diharapkan. Tidak ada kewajiban notebook, PDF, pembelian board, cloud berbayar, atau Docker untuk seluruh pembelajar.

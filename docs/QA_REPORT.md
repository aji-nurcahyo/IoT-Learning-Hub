# Hasil audit dan QA fondasi IoT — 5 November 2026

Target: D:\Workstation\Repo My Corses\Internet Of Things

## Kondisi aktual

Folder sudah berisi implementasi React, TypeScript, Vite dan dependencies saat pertama kali diperiksa dalam chat ini. Asal implementasi sebelumnya, termasuk apakah dibuat di Antigravity, belum dikonfirmasi. Setelah interupsi tersedia pula Getting Started, template, dokumentasi, schema JSON, workflow manual, dan tes. Komponen yang tersedia dipertahankan dan diaudit.

Fondasi memiliki metadata 40 chapter pada empat level, lima tracks, pencarian/filter, navigasi chapter, tema light/dark/system, renderer Markdown GFM/KaTeX/highlighting, mode baca, Reveal.js, serta unduhan panduan dan template. Semua chapter tetap Coming Soon dan Belum diuji; template bukan materi chapter selesai.

## Perbaikan audit ini

- Publication guard memeriksa heading bacaan melalui AST Markdown. Heading di code fence tidak memenuhi bagian wajib publikasi; regression assertion ditambahkan.
- Tes filter menggunakan combobox dengan accessible name yang tepat.
- Catatan kondisi awal folder pada AUDIT.md dikoreksi berdasarkan pengamatan langsung.
- Register lisensi dependency runtime dihasilkan dari package yang benar-benar terpasang.

## Bukti pengujian

| Pemeriksaan | Hasil |
| --- | --- |
| npm run check | Lulus: lint, 8 unit tests, validasi katalog/resource, TypeScript, production build |
| npm run test:http | Lulus: /iot-learning-hub/, /, /kelas/iot/; masing-masing 77 berkas, prefix asset, byte unduhan, .nojekyll, 404.html, dan resource hilang |
| npm run test:browser | Lulus 8/8, Chrome desktop 1440×1000 dan mobile emulation 390×844; 13,6 detik pada run final |
| Pemeriksaan visual | Screenshot homepage mobile diperiksa; bukti screenshot home light/dark, reading, slides tersedia di test-results/ |

Tes browser mencakup tema tersimpan/system, pencarian/filter, chapter prev/next, browser back/reload, Getting Started, TOC tanpa perubahan route, mode baca, unduhan nyata, menu mobile, Markdown tables/math/code, Reveal fragments/notes/cleanup, tracks, serta 404. Mobile emulation bukan pengujian perangkat fisik.

Run browser awal mengalami dua kegagalan pencarian label tes yang kemudian diperbaiki. Run berikutnya mengalami satu kegagalan HTTP saat build dan browser dijalankan bersamaan. Setelah build dan tes HTTP selesai, seluruh browser suite dijalankan ulang secara berurutan dan lulus 8/8. Build final memakai /iot-learning-hub/.

## Batas dan tindak lanjut

Build memberi warning ukuran bundle utama sekitar 1,07 MB (gzip sekitar 307 KB) dan anotasi komentar Zod. Ini bukan kegagalan build; pemecahan renderer dapat menjadi peningkatan berikutnya.

Tidak menjalankan firmware compile, simulator, broker MQTT, Node-RED, atau hardware. Petunjuk Getting Started belum menjadi bukti praktik. Referensi eksternal tidak diverifikasi ulang melalui web pada audit lanjutan ini. Publication guard memeriksa struktur, file dan integritas bukti; mutu pedagogis serta keaslian bukti tetap memerlukan review manusia.

Tidak mengubah proyek referensi, tidak melakukan push/deployment. Workflow GitHub Pages tetap manual. Langkah selanjutnya: menulis dan mereview chapter 01–03 secara bertahap tanpa menerbitkan placeholder.

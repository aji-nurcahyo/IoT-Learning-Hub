# Audit fondasi — 4 November 2026

## Kondisi awal

Saat audit langsung dalam chat ini, folder `D:\Workstation\Repo My Corses\Internet Of Things` sudah berisi aplikasi awal React/TypeScript/Vite, metadata, dan dependencies. Implementasi dipertahankan dan diperiksa; asal pekerjaan sebelumnya (termasuk apakah melalui Antigravity) belum dikonfirmasi. Setelah interupsi, panduan, template, dokumentasi, dan tes juga ditemukan tersedia. Catatan kondisi kosong dari handoff bukan kondisi aktual audit ini. Pencarian AGENTS.md pada area proyek tidak menemukan instruksi tambahan.

Proyek Alpro-python memiliki React/TypeScript/Vite, katalog level/chapter, resource map, theme, Reveal.js, UI kode/math, GitHub Pages, dan materi Python. Proyek Kecerdasan Buatan menggunakan pola serupa dengan katalog 40 chapter, renderer bacaan, validasi konten, tracks, dan resource publik. Keduanya hanya dibaca; tidak ada perubahan, instalasi dependency, build, atau pengujian yang dijalankan di folder referensi.

## Temuan dan keputusan

| Area referensi | Temuan | Fondasi IoT |
| --- | --- | --- |
| UI/UX | Katalog level, chapter, track; theme dan navigation | Pola dipertahankan dengan UI IoT baru dan warna hijau mineral |
| Renderer AI | Split baris; heading code fence dapat masuk TOC, daftar bukan list semantik | AST Markdown, GFM, KaTeX, highlight, semantic lists, TOC dari heading AST |
| Resource Python | Map terpisah dengan nama file spesifik Python | Metadata tunggal dan pemeriksaan file nyata |
| Publication AI | Boolean review/execution; notebook wajib | Bukti ber-hash, reviewer/report/date, rubrik 100, alasan opsional |
| Reveal | Hash dimatikan agar route SPA tidak tertimpa | Dipertahankan melalui konfigurasi baru, lifecycle cleanup |
| Preferences/branding | Namespace dan label spesifik proyek asal | Konfigurasi identitas IoT terpusat |
| GitHub Pages Python | Workflow push otomatis | Workflow manual saja; base default sesuai repo IoT |
| Konten lama | Materi Python dan AI tersedia | Tidak disalin |

Kode implementasi ditulis baru. Tidak menyalin `.git`, `node_modules`, `dist`, log, atau materi lama. Copyright Reveal.js dipertahankan sebagai notice upstream; daftar dependency dan atribusi dicatat terpisah. Belum dilakukan push/deploy.

## Batas audit

Audit berfokus pada file arsitektur, renderer, schema/resource, theme, navigasi, konfigurasi build, workflow, serta notice; tidak menilai seluruh materi pembelajaran pada proyek referensi. Keberhasilan website tidak menjadi bukti eksperimen IoT.

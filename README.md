# Internet of Things Learning Hub

**From Connected Devices to Intelligent Systems**

Created & Developed by **Aji Pamungkas Tri Nurcahyo** · Institut Teknologi Sumatera.

Perpustakaan modul pembelajaran terbuka, bukan LMS. Foundation menyediakan empat level, 40 chapter Coming Soon, lima specialization tracks, Getting Started, serta laboratorium template bacaan dan presentasi. Template bukan chapter yang selesai.

## Menjalankan

Gunakan Node.js 24 LTS dan npm. Dari folder ini:

```powershell
npm ci
npm run dev
```

Buka URL yang dicetak Vite dengan path `/iot-learning-hub/`. Port mengikuti Vite atau parameter `--port`; tidak memakai port proyek referensi.

```powershell
npm run check
npm run test:http
npm run test:browser
npm run preview
```

`check` menjalankan lint, unit tests, validasi konten, TypeScript, dan production build. `test:http` membangun dan menguji default base, root, serta `/kelas/iot/` pada server statis tanpa SPA fallback; setelah selesai build default dipulihkan. Browser tests memakai Chrome terpasang, desktop dan mobile emulation, serta production preview. Ganti channel di `playwright.config.ts` jika menggunakan Chromium; jalankan `npx playwright install chromium` bila diperlukan. Hasil lokal berada di `test-results/` dan tidak masuk Git.

## Base path dan GitHub Pages

Situs ini dipublikasikan pada GitHub Pages di [https://aji-nurcahyo.github.io/IoT-Learning-Hub/](https://aji-nurcahyo.github.io/IoT-Learning-Hub/) dari repositori [https://github.com/aji-nurcahyo/IoT-Learning-Hub](https://github.com/aji-nurcahyo/IoT-Learning-Hub).

Routing aplikasi menggunakan hash routing (misalnya `#/chapter/14`) sehingga kompatibel secara penuh dengan hosting statis GitHub Pages. Seluruh link resource internal menggunakan `import.meta.env.BASE_URL`.

Untuk deployment ke GitHub Pages, alur GitHub Actions otomatis terkonfigurasi pada [`.github/workflows/pages.yml`](.github/workflows/pages.yml) dengan base path `/IoT-Learning-Hub/`. Workflow ini berjalan otomatis pada setiap push ke cabang `main` atau dapat dipicu manual via `workflow_dispatch`.

Untuk pengujian lokal di root atau path lain:

```powershell
$env:VITE_BASE_PATH = '/'
npm run build
npm run preview
```

Untuk path lain seperti `/kelas/iot/`:

```powershell
$env:VITE_BASE_PATH = '/kelas/iot/'
npm run build
npm run preview
```

Bersihkan override dengan `Remove-Item Env:VITE_BASE_PATH` sebelum membangun kembali untuk default. File `public/.nojekyll` disalin otomatis oleh Vite, dan proses build menyalin `index.html` menjadi `dist/404.html` untuk fallback halaman statis.

## Struktur

- `content/catalog.json`: sumber metadata level, chapter, track, referensi, dan resource fondasi.
- `src/schema.ts` dan `content/schemas/`: schema chapter/resource, praktik hardware, bukti uji, dan slide.
- `src/main.tsx`, `src/Reading.tsx`, `src/Deck.tsx`: UI, Markdown AST, dan Reveal.js.
- `public/guides/`: Getting Started yang terpisah dari chapter.
- `public/templates/`: template bacaan, slide, dan laporan bukti.
- `public/content/`: lokasi resource chapter saat materi mulai ditulis.
- `scripts/validate.ts`: guard publikasi dan pemeriksaan file nyata.
- `docs/`: standar, audit, referensi, lisensi, roadmap, dan laporan pengujian.

Mulai penulisan dari [panduan kontribusi chapter](docs/AUTHORING.md). Baca [aturan bahasa](docs/TECHNICAL_LANGUAGE_GUIDE.md), [standar kurikulum](docs/CURRICULUM_STANDARD.md), dan [hasil QA](docs/QA_REPORT.md).

## Kejujuran verifikasi

Semua chapter masih Belum diuji. Tidak ada klaim Hardware-verified, hasil Sensor, latency, packet loss, power consumption, atau inference accuracy. Getting Started adalah petunjuk persiapan, bukan rekaman eksperimen yang sudah dijalankan. Hardware, Docker, dan layanan berbayar tidak diwajibkan.

# Desain Arsitektur Konten & Integrasi Platform Jalur Peminatan
## IoT Learning Hub — Phase 6A: Specialization Content System & Publication Guard Integration

Dokumen ini mendefinisikan arsitektur konten, skema metadata, sistem berkas sumber daya (*resource bundle*), routing platform, dan strategi integrasi pengawal publikasi (*Publication Guard*) untuk 5 Jalur Peminatan (Track A–E, total 30 modul).

- **Proyek**: Internet of Things Learning Hub (*From Connected Devices to Intelligent Systems*)
- **Pengembang & Kurator**: Aji Pamungkas Tri Nurcahyo (Institut Teknologi Sumatera - ITERA)
- **Kebijakan Anti-Slop**: Permanent Active (Mode: **DURING**)
- **Fase**: Phase 6A — Specialization Architecture & Curriculum Design
- **Tanggal Rilis**: 18 November 2026

---

## 1. Arsitektur Berkas & Struktur Sumber Daya Modul

Mengikuti prinsip konsistensi ketat dengan 40 bab kurikulum inti (*Core Curriculum*), setiap modul spesialisasi dirancang untuk memiliki direktori mandiri di bawah jalur:

`public/content/specialization/{trackId}/{moduleId}/`

Contoh: `public/content/specialization/track-b/mod-b01/`

### 1.1 Struktur Standar Bundel Berkas Modul Spesialisasi (11 Berkas Standar)

Setiap modul peminatan lengkap akan memuat 11 berkas sumber daya kanonikal yang mematuhi kontrak integritas data hub:

```
public/content/specialization/track-{a..e}/mod-{id}/
├── reading.md        # Modul bacaan akademik terstruktur (Tujuan, Prasyarat, Teori, Math, Latihan, Tugas, Ringkasan, Referensi)
├── slides.json       # Slide presentasi Reveal.js (Array JSON dengan title, body, dan presenter notes >= 10 karakter)
├── code.md           # Snippet dan walkthrough instruksi implementasi software / simulasi
├── diagram.svg       # Diagram arsitektur vektor SVG mandiri (kontras WCAG AAA, informatif, non-dekoratif)
├── exercises.md      # Bank latihan kognitif bertingkat (C1 hingga C6 Taksonomi Bloom)
├── assignment.md     # Tugas rekayasa terstruktur berbasis masalah (Problem-Based Learning)
├── review.md         # Laporan telaah rekan sejawat / peer-review independen
├── outputs.md        # Catatan bukti verifikasi pengujian eksekusi nyata (dilengkapi SHA-256 canonical LF hash)
├── telemetry.csv     # (Opsional/Sesuai kebutuhan) Dataset deret waktu sintetis/empiris untuk analisis
├── notebook.ipynb    # (Opsional/Sesuai kebutuhan) Jupyter notebook interaktif untuk komputasi analitik
└── src/              # Direktori source code mandiri yang dapat dieksekusi 100%
    ├── __init__.py
    └── {module}_sim.py
```

---

## 2. Skema Metadata & Rencana Ekstensi Katalog (Catalog Schema Extension)

Katalog platform (`content/catalog.json`) yang saat ini memuat array `tracks` dengan ringkasan tingkat tinggi akan diperluas secara bertahap tanpa merusak validasi yang ada.

### 2.1 Definisi Tipe TypeScript (`src/schema.ts` Extension Plan)

```typescript
// Rencana ekstensi schema.ts untuk mendukung detail modul peminatan
export type SpecializationStatus = 'planned' | 'coming-soon' | 'in-development' | 'published';

export interface SpecializationModuleMeta {
  id: string;               // e.g. "a01", "b04"
  slug: string;             // e.g. "mod-a01", "mod-b04"
  trackId: 'a' | 'b' | 'c' | 'd' | 'e';
  number: number;           // 1 to 6
  title: string;
  description: string;
  academicDepth: 'L2: Undergraduate Complete' | 'L3: Advanced Engineering' | 'L4: Research Preparation';
  objectives: string[];
  prerequisites: {
    coreChapters: number[]; // e.g. [1, 2, 11]
    trackModules: string[]; // e.g. ["a01"]
  };
  tags: string[];
  status: SpecializationStatus;
  resources: ChapterResources; // Konsisten dengan tipe resource Chapter existing
  verification: VerificationMeta;
  review: ReviewMeta;
  rubric: RubricCriterion[];
  hardware: {
    required: boolean;
    reason: string;
  };
}

export interface TrackExtendedMeta {
  id: 'a' | 'b' | 'c' | 'd' | 'e';
  title: string;
  overview: string;
  competencyTarget: string;
  topics: string[];
  chapters: number[];        // Core prerequisite chapters
  modules: SpecializationModuleMeta[];
  status: SpecializationStatus;
}
```

### 2.2 Penjelasan Status Modul & Siklus Hidup (Lifecycle State Transitions)

| Status | Makna & Kondisi Akses Pengguna | Syarat Pengawal Publikasi (Publication Guard) |
|---|---|---|
| `planned` | Modul berada pada tahap silabus & spesifikasi kurikulum; belum ada kode/bacaan di disk. Ditampilkan sebagai roadmap terencana. | Hanya memvalidasi metadata silabus dan ketergantungan prasyarat. |
| `coming-soon` | Kerangka direktori modul telah dibuat; silabus dapat dibaca, berkas sumber daya sedang dalam persiapan. | Memeriksa ketersediaan `reading.md` dasar dan `assignment.md`. |
| `in-development` | Berkas bacaan, slide, dan kode sumber sedang diintegrasikan dan diverifikasi oleh tim pengembang. | Memvalidasi seluruh heading wajib `reading.md` dan struktur `slides.json`. |
| `published` | Modul telah tuntas $100\%$, seluruh berkas tersedia, bukti eksekusi diverifikasi nyata, dan lulus audit anti-slop. | **Strict Guard**: Memvalidasi integritas hash SHA-256 `outputs.md`, rubrik $= 100$ poin, zero missing resource. |

---

## 3. Strategi Integrasi Routing & Navigasi Pengguna

Untuk menjaga keramahan navigasi tanpa membebani menu utama kurikulum 40 bab, integrasi UI dirancang sebagai berikut:

### 3.1 Struktur Routing Hash-Based (React Routing)
- `#/tracks`: Menampilkan ikhtisar 5 Jalur Peminatan dengan kartu deskriptif, indikator kompetensi, dan status kemajuan.
- `#/track/:id`: Menampilkan halaman beranda peminatan spesifik (misal `#/track/b`), memuat:
  1. Target kompetensi profesional dan profil karir terkait.
  2. Daftar 6 modul terstruktur (A01–A06 hingga E01–E06) dengan badge kedalaman akademik (L2/L3/L4) dan status modul.
  3. Diagram alir prasyarat interaktif (*Interactive Prerequisite Graph*).
  4. Sorotan proyek Capstone di modul ke-6.
- `#/track/:id/:moduleId`: Menampilkan viewer modul lengkap (pembacaan Markdown dengan KaTeX math, Reveal.js slides viewer, tab latihan, tugas, rubrik, dan tombol download kode sumber mandiri).

---

## 4. Rencana Validasi Pengawal Publikasi (Publication Guard Adaptation Plan)

Skrip validasi utama (`scripts/validate.ts`) akan diperluas pada fase implementasi modul dengan menambahkan fungsi pengawas khusus:

```typescript
// Logika adaptasi validate.ts untuk modul spesialisasi (Phase 6B onwards)
export function validateSpecializationTracks(data: ExtendedCatalog, root: string): string[] {
  const errors: string[] = [];
  if (!data.tracks || data.tracks.length !== 5) {
    errors.push('Harus terdapat tepat 5 specialization tracks');
    return errors;
  }
  for (const track of data.tracks) {
    if (track.modules && track.modules.length > 0) {
      if (track.modules.length !== 6) {
        errors.push(`Track ${track.id} harus memiliki tepat 6 modul (ditemukan: ${track.modules.length})`);
      }
      for (const mod of track.modules) {
        if (mod.status === 'published') {
          // Menjalankan validasi ketat identik dengan bab kurikulum inti
          validatePublishedModule(mod, root, errors);
        }
      }
    }
  }
  return errors;
}
```

Adaptasi ini menjamin bahwa penambahan modul spesialisasi tidak akan pernah menurunkan standar integritas pembuktian pengujian (*proof-of-verification*) yang sudah kokoh pada bab-bab inti.


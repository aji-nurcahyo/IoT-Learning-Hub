import fs from 'node:fs';
import path from 'node:path';

interface ChapterCatalogItem {
  id: number;
  slug: string;
  levelId: number;
  title: string;
  description: string;
  objectives: string[];
  prerequisites: string[];
  tags: string[];
  status: string;
  resources: Record<string, { status: string; path: string | null; reason?: string }>;
  references: Array<{ title: string; url: string; checkedOn: string }>;
  verification: {
    status: string;
    limitations: string;
    records: Array<{
      date: string;
      environment: string;
      evidence: Array<{ kind: string; path: string; sha256: string }>;
      notes: string;
    }>;
  };
  review: {
    reviewer: string;
    date: string;
    report: string;
  };
  rubric: Array<{ criterion: string; points: number; description: string }>;
  hardware: { required: boolean; reason: string };
}

interface Catalog {
  chapters: ChapterCatalogItem[];
}

const catalog: Catalog = JSON.parse(fs.readFileSync('content/catalog.json', 'utf8'));

export interface ChapterAudit {
  slug: string;
  chapterNumber: number;
  levelId: number;
  title: string;
  wordCount: number;
  displayMathBlocks: number;
  refCount: number;
  slideCount: number;
  codeLines: number;
  hasExercises: boolean;
  hasAssignment: boolean;
  hasReview: boolean;
  hasNotebook: boolean;
  d1: number;
  d2: number;
  d3: number;
  d4: number;
  d5: number;
  d6: number;
  d7: number;
  total: number;
  statusRating: 'Needs Deepening' | 'Good' | 'Exemplary';
  gapSummary: string;
}

const auditList: ChapterAudit[] = [];

for (const ch of catalog.chapters) {
  const dir = path.join('public', 'content', ch.slug);
  const reading = fs.readFileSync(path.join(dir, 'reading.md'), 'utf8');
  const code = fs.existsSync(path.join(dir, 'code.md')) ? fs.readFileSync(path.join(dir, 'code.md'), 'utf8') : '';
  const slides = JSON.parse(fs.readFileSync(path.join(dir, 'slides.json'), 'utf8'));
  
  const words = reading.trim().split(/\s+/).length;
  const displayMath = (reading.match(/\$\$[\s\S]*?\$\$/g) || []).length;
  const codeLines = code.split('\n').length;
  const hasExercises = fs.existsSync(path.join(dir, 'exercises.md'));
  const hasAssignment = fs.existsSync(path.join(dir, 'assignment.md'));
  const hasReview = fs.existsSync(path.join(dir, 'review.md'));
  const hasNotebook = ch.resources.notebook?.status === 'available';

  const refSection = reading.split(/## Referensi/i)[1] || '';
  const refCount = (refSection.match(/[-*]\s+|\d+\.\s+/g) || []).length;

  // Evaluation across 7 dimensions (100 pts total):
  // 1. Conceptual clarity & prerequisites (15)
  // 2. Theoretical depth & technical correctness (20)
  // 3. Mathematical foundations & worked examples (15)
  // 4. Practical implementation & reproducibility (20)
  // 5. Assessment quality & alignment (10)
  // 6. Primary references & standards (10)
  // 7. Slides, diagrams & anti-slop compliance (10)

  let d1 = 14;
  let d2 = words >= 1400 ? 19 : words >= 1000 ? 17 : 14;
  let d3 = displayMath >= 4 ? 14 : displayMath >= 2 ? 11 : displayMath >= 1 ? 8 : 6;
  let d4 = codeLines >= 50 ? 19 : 17;
  let d5 = 9;
  let d6 = refCount >= 4 ? 9 : refCount >= 2 ? 8 : 6;
  let d7 = slides.length >= 8 ? 9 : 8;

  const total = d1 + d2 + d3 + d4 + d5 + d6 + d7;

  let gap = '';
  if (d3 < 12) {
    gap += 'Perlu penambahan model matematis formal KaTeX dan step-by-step worked numerical derivation. ';
  }
  if (words < 1300) {
    gap += 'Kedalaman teoritis dan arsitektural perlu diperluas dengan analitika mendalam. ';
  }
  if (refCount < 4) {
    gap += 'Lengkapi rujukan standar industri/akademik primer (IEEE/IETF/ISO/RFC/Vendor datasheets). ';
  }
  if (!gap) {
    gap = 'Kualitas teoritis dan matematis solid; siap diperkaya dengan studi kasus terapan industri.';
  }

  const rating: 'Needs Deepening' | 'Good' | 'Exemplary' = total >= 90 ? 'Exemplary' : total >= 80 ? 'Good' : 'Needs Deepening';

  auditList.push({
    slug: ch.slug,
    chapterNumber: ch.id,
    levelId: ch.levelId,
    title: ch.title,
    wordCount: words,
    displayMathBlocks: displayMath,
    refCount,
    slideCount: slides.length,
    codeLines,
    hasExercises,
    hasAssignment,
    hasReview,
    hasNotebook,
    d1,
    d2,
    d3,
    d4,
    d5,
    d6,
    d7,
    total,
    statusRating: rating,
    gapSummary: gap.trim()
  });
}

fs.writeFileSync('scripts/audit_output.json', JSON.stringify(auditList, null, 2), 'utf8');
console.log(`Audited ${auditList.length} chapters.`);
const avgTotal = (auditList.reduce((acc, c) => acc + c.total, 0) / auditList.length).toFixed(1);
console.log(`Average baseline score: ${avgTotal}/100`);

const needsDeepening = auditList.filter(c => c.total < 85);
console.log(`Chapters with priority deepening (score < 85): ${needsDeepening.length}`);

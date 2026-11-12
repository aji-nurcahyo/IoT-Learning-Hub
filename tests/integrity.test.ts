import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { hashEvidence, validateChapter } from '../scripts/validate';
import { chapters } from '../src/catalog';

test('hashEvidence: canonicalization teks menghasilkan hash identik untuk CRLF dan LF', () => {
  const contentLf = 'baris satu\nbaris dua\nbaris tiga\n';
  const contentCrlf = 'baris satu\r\nbaris dua\r\nbaris tiga\r\n';

  const extensions = ['outputs.md', 'compile.log', 'script.py', 'sketch.ino', 'header.h', 'data.json'];
  for (const filename of extensions) {
    const hashLf = hashEvidence(Buffer.from(contentLf, 'utf8'), filename);
    const hashCrlf = hashEvidence(Buffer.from(contentCrlf, 'utf8'), filename);

    const expectedHash = createHash('sha256').update(contentLf).digest('hex');
    assert.equal(hashLf, expectedHash, `Hash LF harus cocok dengan expected canonical hash untuk ${filename}`);
    assert.equal(hashCrlf, expectedHash, `Hash CRLF harus dinormalisasi dan cocok dengan hash LF untuk ${filename}`);
    assert.equal(hashLf, hashCrlf, `Hash LF dan CRLF harus identik untuk ${filename}`);
  }
});

test('hashEvidence: binary files di-hash raw tanpa normalisasi byte', () => {
  const binaryWithCrlfBytes = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0xFF]);
  const expectedRawHash = createHash('sha256').update(binaryWithCrlfBytes).digest('hex');

  const binaryExtensions = ['image.png', 'firmware.bin', 'archive.zip', 'photo.jpg'];
  for (const filename of binaryExtensions) {
    const resultHash = hashEvidence(binaryWithCrlfBytes, filename);
    assert.equal(resultHash, expectedRawHash, `Binary file ${filename} tidak boleh mengalami normalisasi CRLF`);
  }
});

test('integritas bukti: tampering konten sekecil 1 karakter menggagalkan validasi', () => {
  const dir = mkdtempSync(join(tmpdir(), 'iot-tamper-'));
  try {
    mkdirSync(join(dir, 'content'));
    const c = structuredClone(chapters[20]);
    c.status = 'published';

    for (const key of Object.keys(c.resources) as (keyof typeof c.resources)[]) {
      c.resources[key] = { status: 'not-applicable', path: null, reason: 'Tidak diperlukan pada unit test fixture.' };
    }

    const reading = ['Tujuan pembelajaran', 'Prasyarat', 'Konsep dan teori', 'Latihan', 'Tugas', 'Ringkasan', 'Referensi']
      .map(s => `## ${s}\nMateri pengujian integritas bukti.`).join('\n');
    writeFileSync(join(dir, 'content/reading.md'), reading);
    writeFileSync(join(dir, 'content/slides.json'), JSON.stringify([{
      title: 'Judul Slide Uji',
      body: 'Materi slide pengujian integritas bukti.',
      notes: 'Catatan pengujian unit test integritas bukti yang memadai.'
    }]));
    writeFileSync(join(dir, 'content/exercises.md'), 'Latihan');
    writeFileSync(join(dir, 'content/assignment.md'), 'Tugas');
    writeFileSync(join(dir, 'content/review.md'), 'Review');

    for (const key of ['reading', 'slides', 'exercises', 'assignment'] as const) {
      c.resources[key] = { status: 'available', path: `content/${key}.${key === 'slides' ? 'json' : 'md'}` };
    }

    c.review = { reviewer: 'Reviewer fixture', date: '2026-11-13', report: 'content/review.md' };
    c.rubric = [
      { criterion: 'Kebutuhan', points: 30, description: 'Kriteria rinci kebutuhan' },
      { criterion: 'Analisis', points: 40, description: 'Kriteria rinci analisis' },
      { criterion: 'Dokumentasi', points: 30, description: 'Kriteria rinci dokumentasi' }
    ];

    const logOriginal = 'Compilation finished with 0 errors.\nMemory usage: 12%\n';
    writeFileSync(join(dir, 'content/outputs.md'), logOriginal);

    const validHash = hashEvidence(Buffer.from(logOriginal, 'utf8'), 'content/outputs.md');
    c.verification = {
      status: 'compile-verified',
      limitations: 'Simulasi tanpa hardware fisik.',
      records: [{
        kind: 'compile',
        path: 'content/outputs.md',
        date: '2026-11-13',
        command: 'arduino-cli compile',
        environment: 'ESP32 Core 3.0.7',
        sha256: validHash
      }]
    };

    assert.deepEqual(validateChapter(c, dir), [], 'Chapter valid harus lolos validasi guard');

    // Modifikasi 1 karakter (tampering)
    const logTampered = 'Compilation finished with 1 errors.\nMemory usage: 12%\n';
    writeFileSync(join(dir, 'content/outputs.md'), logTampered);
    const errors = validateChapter(c, dir);
    assert.ok(errors.length > 0, 'Tampering file evidence wajib menghasilkan error validasi');
    assert.match(errors.join(), /hash bukti uji tidak cocok/, 'Pesan error harus eksplisit menyebut hash tidak cocok');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('integritas bukti: file evidence yang hilang menggagalkan validasi', () => {
  const dir = mkdtempSync(join(tmpdir(), 'iot-missing-'));
  try {
    mkdirSync(join(dir, 'content'));
    const c = structuredClone(chapters[20]);
    c.status = 'published';

    for (const key of Object.keys(c.resources) as (keyof typeof c.resources)[]) {
      c.resources[key] = { status: 'not-applicable', path: null, reason: 'Tidak diperlukan pada unit test fixture.' };
    }

    const reading = ['Tujuan pembelajaran', 'Prasyarat', 'Konsep dan teori', 'Latihan', 'Tugas', 'Ringkasan', 'Referensi']
      .map(s => `## ${s}\nMateri pengujian file hilang.`).join('\n');
    writeFileSync(join(dir, 'content/reading.md'), reading);
    writeFileSync(join(dir, 'content/slides.json'), JSON.stringify([{
      title: 'Judul Slide Uji',
      body: 'Materi slide pengujian file evidence hilang.',
      notes: 'Catatan pengujian unit test file hilang yang memadai.'
    }]));
    writeFileSync(join(dir, 'content/exercises.md'), 'Latihan');
    writeFileSync(join(dir, 'content/assignment.md'), 'Tugas');
    writeFileSync(join(dir, 'content/review.md'), 'Review');

    for (const key of ['reading', 'slides', 'exercises', 'assignment'] as const) {
      c.resources[key] = { status: 'available', path: `content/${key}.${key === 'slides' ? 'json' : 'md'}` };
    }

    c.review = { reviewer: 'Reviewer fixture', date: '2026-11-13', report: 'content/review.md' };
    c.rubric = [
      { criterion: 'Kebutuhan', points: 30, description: 'Kriteria rinci kebutuhan' },
      { criterion: 'Analisis', points: 40, description: 'Kriteria rinci analisis' },
      { criterion: 'Dokumentasi', points: 30, description: 'Kriteria rinci dokumentasi' }
    ];

    c.verification = {
      status: 'compile-verified',
      limitations: 'Simulasi tanpa hardware fisik.',
      records: [{
        kind: 'compile',
        path: 'content/outputs-missing.md',
        date: '2026-11-13',
        command: 'arduino-cli compile',
        environment: 'ESP32 Core 3.0.7',
        sha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
      }]
    };

    const errors = validateChapter(c, dir);
    assert.ok(errors.length > 0, 'Missing evidence wajib menghasilkan error');
    assert.match(errors.join(), /bukti uji tidak ada/, 'Pesan error harus eksplisit menyebut bukti uji tidak ada');
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

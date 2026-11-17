import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { headings } from '../src/markdown';
import { chapters, filterChapters } from '../src/catalog';
import { validateAll, validateChapter } from '../scripts/validate';
import { normalizeBase } from '../scripts/base';
test('katalog memiliki Level 1-4 Tersedia (01-40) tanpa download semu',()=>{
 assert.equal(chapters.length,40);
 assert.ok(chapters.every(c=>c.status==='published'&&c.rubric.reduce((s,r)=>s+r.points,0)===100));
 assert.deepEqual(validateAll(),[]);
});
test('TOC mengabaikan code fence, mengenali heading setext dan heading duplikat',()=>{const h=headings('# Judul\n\n```md\n# Bukan heading\n```\n\n## Judul\n\nBagian\n------');assert.deepEqual(h.map(x=>x.text),['Judul','Judul','Bagian']);assert.equal(new Set(h.map(x=>x.id)).size,3);});
test('search menggabungkan kata, nomor, level, dan ketersediaan',()=>{assert.equal(filterChapters(chapters,'mqtt qos','2','all')[0].id,15);assert.equal(filterChapters(chapters,'01','all','all')[0].id,1);assert.equal(filterChapters(chapters,'mqtt','1','all').length,0);assert.equal(filterChapters(chapters,'','all','available').length,40);assert.equal(filterChapters(chapters,'','all','published').length,40);});
test('base menerima root dan subpath, menolak URL atau traversal',()=>{assert.equal(normalizeBase(),'/iot-learning-hub/');assert.equal(normalizeBase('/'),'/');assert.equal(normalizeBase('/kelas/iot'),'/kelas/iot/');for(const value of ['../x','https://host/','/../x/','//host/'])assert.throws(()=>normalizeBase(value));});
test('guard menolak resource hilang, traversal, dan tanpa alasan',()=>{const c=structuredClone(chapters[0]);c.resources.reading={status:'available',path:'content/missing.md'};assert.match(validateChapter(c).join(),/tidak ada/);c.resources.reading={status:'available',path:'../secret.md'};assert.ok(validateChapter(c).length);c.resources.reading={status:'not-applicable',path:null,reason:''};assert.ok(validateChapter(c).length);});
test('boolean reviewed tidak dapat menerbitkan chapter',()=>{const c={...structuredClone(chapters[0]),status:'published',reviewed:true,rubric:[],review:{reviewer:'',date:null,report:null},resources:{...chapters[0].resources,reading:{status:'planned',path:null,reason:'Materi sedang dalam proses penulisan terstruktur.'}}};const e=validateChapter(c).join();assert.match(e,/rubrik/);assert.match(e,/review/);assert.match(e,/wajib tersedia/);});
test('label hardware tidak boleh didukung oleh log compile saja',()=>{const c=structuredClone(chapters[0]);c.verification.status='hardware-verified';assert.match(validateChapter(c).join(),/bukti uji/);});
test('publikasi lengkap, notebook opsional, rubrik 100 dan integritas bukti',()=>{
 const dir=mkdtempSync(join(tmpdir(),'iot-guard-'));
 try{
  mkdirSync(join(dir,'content'));
  const c=structuredClone(chapters[0]);c.status='published';
  c.verification={status:'untested',limitations:'Tidak ada verifikasi hardware.',records:[]};
  for(const key of Object.keys(c.resources) as (keyof typeof c.resources)[]) c.resources[key]={status:'not-applicable',path:null,reason:'Tidak diperlukan pada contoh konseptual ini.'};
  const reading=['Tujuan pembelajaran','Prasyarat','Konsep dan teori','Latihan','Tugas','Ringkasan','Referensi'].map(s=>`## ${s}\nMateri contoh untuk pengujian guard, bukan chapter publik.`).join('\n');
  const files:Record<string,string>={'reading.md':reading,'slides.json':JSON.stringify([{title:'Konsep pengujian',body:'Materi contoh yang hanya dipakai pada unit test.',notes:'Jelaskan bahwa ini fixture pengujian internal.'}]),'exercises.md':'Latihan dasar, menengah, dan lanjut.','assignment.md':'Tugas dengan rubrik metadata.','review.md':'Reviewer memeriksa materi dan sumber primer.'};
  for(const [name,body] of Object.entries(files))writeFileSync(join(dir,'content',name),body);
  for(const key of ['reading','slides','exercises','assignment'] as const)c.resources[key]={status:'available',path:`content/${key}.${key==='slides'?'json':'md'}`};
  c.review={reviewer:'Reviewer fixture',date:'2026-11-04',report:'content/review.md'};
  c.rubric=[{criterion:'Kebutuhan',points:30,description:'Kriteria rinci kebutuhan'},{criterion:'Analisis',points:40,description:'Kriteria rinci analisis'},{criterion:'Dokumentasi',points:30,description:'Kriteria rinci dokumentasi'}];
  assert.deepEqual(validateChapter(c,dir),[]);
  writeFileSync(join(dir,'content/reading.md'),'```md\n'+reading+'\n```');
  assert.match(validateChapter(c,dir).join(),/bacaan tidak memuat/);
  writeFileSync(join(dir,'content/reading.md'),reading);
  c.rubric[0].points=29;assert.match(validateChapter(c,dir).join(),/100/);c.rubric[0].points=30;
  writeFileSync(join(dir,'content/log.txt'),'hasil fixture');
  c.verification={status:'compile-verified',limitations:'Tidak ada hardware fisik yang diuji.',records:[{kind:'compile',path:'content/log.txt',date:'2026-11-04',command:'fixture build',environment:'Unit test fixture',sha256:createHash('sha256').update('hasil fixture').digest('hex')}]};
  assert.deepEqual(validateChapter(c,dir),[]);
  writeFileSync(join(dir,'content/log.txt'),'log berubah');assert.match(validateChapter(c,dir).join(),/hash/);
 }finally{rmSync(dir,{recursive:true,force:true});}
});

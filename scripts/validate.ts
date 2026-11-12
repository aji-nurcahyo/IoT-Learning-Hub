import { readFileSync, existsSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { chapterSchema, deckSchema, type Chapter } from '../src/schema';
import { headings } from '../src/markdown';
const root=resolve(import.meta.dirname,'..');
export function hashEvidence(buffer: Buffer, filePath: string): string {
 const isText = /\.(md|txt|csv|json|py|ino|h|svg|log|ya?ml)$/i.test(filePath);
 if (isText) {
  const canonical = buffer.toString('utf8').replace(/\r\n/g, '\n');
  return createHash('sha256').update(canonical, 'utf8').digest('hex');
 }
 return createHash('sha256').update(buffer).digest('hex');
}
export function validateChapter(input:unknown, publicRoot=resolve(root,'public')):string[] {
 const result=chapterSchema.safeParse(input);
 if(!result.success) return result.error.issues.map(i=>`${i.path.join('.')}: ${i.message}`);
 const c:Chapter=result.data, errors:string[]=[];
 const check=(ok:unknown,msg:string)=>{if(!ok)errors.push(`${c.id}: ${msg}`);};
 const file=(p:string)=>{const f=resolve(publicRoot,p);return existsSync(f)&&statSync(f).isFile()&&statSync(f).size>0;};
 check(c.slug===`chapter-${String(c.id).padStart(2,'0')}`,'slug tidak cocok');
 check(c.levelId===Math.ceil(c.id/10),'level tidak cocok');
 check(c.prerequisites.every(id=>id<c.id),'prasyarat harus mendahului chapter');
 for(const [key,r] of Object.entries(c.resources)) if(r.status==='available'){
   check(file(r.path),`file ${key} tidak ada / kosong`);
   if(file(r.path)&&key==='slides'){try{deckSchema.parse(JSON.parse(readFileSync(resolve(publicRoot,r.path),'utf8')));}catch{check(false,'deck tidak valid');}}
 }
 for(const e of c.verification.records){
   check(file(e.path),'bukti uji tidak ada');
   if(file(e.path)){
     const buf = readFileSync(resolve(publicRoot,e.path));
     check(hashEvidence(buf, e.path)===e.sha256,'hash bukti uji tidak cocok');
   }
 }
 const kinds={'compile-verified':'compile','simulator-verified':'simulator','hardware-verified':'hardware'} as const;
 if(c.verification.status!=='untested')check(c.verification.records.some(e=>e.kind===kinds[c.verification.status as keyof typeof kinds]),'status tidak didukung bukti uji');
 if(c.hardware.required){for(const p of [c.hardware.bom,c.hardware.pinMapping,c.hardware.wiring,c.hardware.instructions])check(file(p),'dokumen hardware tidak ada');}
 if(c.status==='published'){
  check(c.review.reviewer.trim()&&c.review.date&&c.review.report&&file(c.review.report),'review bertanggal dan laporan wajib');
  check(c.rubric.length>=3&&c.rubric.reduce((sum,r)=>sum+r.points,0)===100,'rubrik wajib total 100 poin');
  for(const k of ['reading','slides','exercises','assignment'] as const)check(c.resources[k].status==='available',`${k} wajib tersedia`);
  for(const [k,r] of Object.entries(c.resources))check(r.status!=='planned',`${k} masih direncanakan`);
  check(c.references.length>=2,'minimal dua referensi primer');
  if(c.resources.code.status==='available')check(c.verification.records.length>0&&c.resources.outputs.status==='available','kode memerlukan bukti eksekusi dan output');
  if(c.hardware.required)check(c.verification.status!=='untested','praktik hardware memerlukan verifikasi minimal compile dengan batasan eksplisit');
  if(c.resources.reading.status==='available'&&file(c.resources.reading.path)){
   const text=readFileSync(resolve(publicRoot,c.resources.reading.path),'utf8');
   const sections=headings(text).filter(h=>h.depth===2).map(h=>h.text);
   for(const heading of ['Tujuan pembelajaran','Prasyarat','Konsep dan teori','Latihan','Tugas','Ringkasan','Referensi'])check(sections.includes(heading),`bacaan tidak memuat ${heading}`);
   check(!/\bTODO\b|\[ISI\]/.test(text),'placeholder tidak boleh dipublikasi');
  }
 }
 return errors;
}
export function validateAll(){
 const data=JSON.parse(readFileSync(resolve(root,'content/catalog.json'),'utf8'));
 const errors:string[]=data.chapters.flatMap((c:unknown)=>validateChapter(c));
 if(data.chapters.length!==40||new Set(data.chapters.map((c:Chapter)=>c.id)).size!==40)errors.push('Harus 40 chapter unik');
 if(data.levels.length!==4||new Set(data.levels.map((l:{id:number})=>l.id)).size!==4)errors.push('Harus empat level unik');
 if(data.tracks.length!==5||new Set(data.tracks.map((t:{id:string})=>t.id)).size!==5)errors.push('Harus lima track unik');
 for(const t of data.tracks)if(!t.topics.length||!t.chapters.every((id:number)=>data.chapters.some((c:Chapter)=>c.id===id)))errors.push(`Track ${t.id} tidak valid`);
 for(const r of data.foundationResources)if(r.status==='available'&&(!existsSync(resolve(root,'public',r.path))||statSync(resolve(root,'public',r.path)).size===0))errors.push(`Resource fondasi hilang: ${r.path}`);
 deckSchema.parse(JSON.parse(readFileSync(resolve(root,'public/templates/slides.json'),'utf8')));
 return errors;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){const e=validateAll();if(e.length){console.error(e.join('\n'));process.exitCode=1;}else console.log('PASS: metadata, 40 chapter, 4 level, 5 track, resource, publication guard, template.');}

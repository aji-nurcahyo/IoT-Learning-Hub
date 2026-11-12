import { z } from 'zod';
export const resourceKinds = ['reading','slides','code','notebook','telemetry','outputs','exercises','assignment','diagram','pdf'] as const;
export const resourceLabels:Record<typeof resourceKinds[number],string> = {reading:'Modul bacaan',slides:'Slides',code:'Source code',notebook:'Notebook',telemetry:'Sample telemetry / dataset',outputs:'Bukti & output eksekusi',exercises:'Latihan bertingkat',assignment:'Tugas & rubrik',diagram:'Diagram / wiring',pdf:'PDF'};
export const publicationLabels = {'coming-soon':'Coming Soon',published:'Tersedia'};
export const verificationLabels = {untested:'Belum diuji','compile-verified':'Compile-verified','simulator-verified':'Simulator-verified','hardware-verified':'Hardware-verified'};
const localPath = z.string().regex(/^[a-zA-Z0-9_/-]+\.[a-zA-Z0-9]+$/).refine(s=>!s.startsWith('/')&&!s.split('/').includes('..'));
const resource = z.discriminatedUnion('status',[
  z.object({status:z.literal('available'),path:localPath,reason:z.string().optional()}),
  z.object({status:z.enum(['planned','not-applicable']),path:z.null(),reason:z.string().min(12)}),
]);
const evidence = z.object({status:z.enum(['untested','compile-verified','simulator-verified','hardware-verified']),limitations:z.string().min(12),records:z.array(z.object({kind:z.enum(['compile','simulator','hardware','software']),path:localPath,environment:z.string().min(5),command:z.string().min(3),date:z.iso.date(),sha256:z.string().regex(/^[a-f0-9]{64}$/)}))});
export const chapterSchema = z.object({
 id:z.number().int().min(1).max(40),slug:z.string().regex(/^chapter-\d{2}$/),levelId:z.number().int().min(1).max(4),title:z.string().min(8),description:z.string().min(20),
 status:z.enum(['coming-soon','published']),objectives:z.array(z.string().min(20)).min(2),prerequisites:z.array(z.number().int().min(1).max(40)),tags:z.array(z.string()).min(1),
 resources:z.record(z.enum(resourceKinds),resource),
 references:z.array(z.object({title:z.string().min(3),url:z.url().startsWith('https://'),checkedOn:z.iso.date()})).min(1),
 verification:evidence,
 review:z.object({reviewer:z.string(),date:z.union([z.iso.date(),z.null()]),report:z.union([localPath,z.null()])}),
 rubric:z.array(z.object({criterion:z.string().min(5),points:z.number().int().positive(),description:z.string().min(10)})),
 hardware:z.discriminatedUnion('required',[z.object({required:z.literal(false),reason:z.string().min(12)}),z.object({required:z.literal(true),board:z.string().min(3),revision:z.string().min(1),bom:localPath,pinMapping:localPath,wiring:localPath,electrical:z.array(z.object({component:z.string(),datasheet:z.url().startsWith('https://'),voltage:z.string().min(3),current:z.string().min(3),protection:z.string().min(5)})).min(1),toolchain:z.string().min(5),instructions:localPath})]),
});
export type Chapter = z.infer<typeof chapterSchema>;
export const deckSchema = z.array(z.object({title:z.string().min(3),body:z.string().min(5),notes:z.string().min(10),fragment:z.string().optional()})).min(1);

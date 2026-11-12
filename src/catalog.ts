import data from '../content/catalog.json';
import { chapterSchema, type Chapter } from './schema';
export const chapters = data.chapters.map(c=>chapterSchema.parse(c));
export const levels = data.levels;
export const tracks = data.tracks;
export const references = data.references;
export const foundationResources = data.foundationResources;
export function filterChapters(items:Chapter[], query:string, level:string, availability:string) {
 const words=query.trim().toLocaleLowerCase('id').split(/\s+/).filter(Boolean);
 return items.filter(c => (level==='all'||c.levelId===Number(level)) && (availability==='all'||(availability==='available'?Object.values(c.resources).some(r=>r.status==='available'):c.status===availability)) && words.every(w=>`${String(c.id).padStart(2,'0')} ${c.title} ${c.description} ${c.tags.join(' ')}`.toLocaleLowerCase('id').includes(w)));
}

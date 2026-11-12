import { z } from 'zod';
import { writeFileSync, mkdirSync } from 'node:fs';
import { chapterSchema, deckSchema } from '../src/schema';
mkdirSync('content/schemas',{recursive:true});
writeFileSync('content/schemas/chapter.schema.json',JSON.stringify(z.toJSONSchema(chapterSchema),null,2)+'\n');
writeFileSync('content/schemas/slides.schema.json',JSON.stringify(z.toJSONSchema(deckSchema),null,2)+'\n');
console.log('Schema JSON diekspor dari schema Zod.');

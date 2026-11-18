import fs from 'node:fs';
import path from 'node:path';
import { ACADEMIC_ENHANCEMENTS } from './academic_enhancements_data';

for (const item of ACADEMIC_ENHANCEMENTS) {
  const filePath = path.join('public', 'content', item.slug, 'reading.md');
  if (!fs.existsSync(filePath)) {
    console.error(`Not found: ${filePath}`);
    continue;
  }
  let content = fs.readFileSync(filePath, 'utf8');
  if (content.includes('Mathematical Foundations')) {
    console.log(`Already enhanced: ${item.slug}`);
    continue;
  }
  if (!content.includes(item.targetBeforeHeading)) {
    console.warn(`Target heading not found in ${item.slug}: "${item.targetBeforeHeading}"`);
    continue;
  }

  // Use a replacer function to avoid String.prototype.replace $ substitution
  content = content.replace(item.targetBeforeHeading, () => item.mathMarkdown + '\n' + item.targetBeforeHeading);

  if (item.extraReferences && item.extraReferences.length > 0) {
    const refHeader = '## Referensi';
    if (content.includes(refHeader)) {
      const extraText = '\n' + item.extraReferences.join('\n');
      content = content.replace(refHeader, refHeader + extraText);
    }
  }

  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Successfully applied academic deepening to ${item.slug}`);
}

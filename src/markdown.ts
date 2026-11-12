import { unified } from 'unified';
import remarkParse from 'remark-parse';
import { visit } from 'unist-util-visit';
import { toString } from 'mdast-util-to-string';
export function headings(text:string){
 const result:{id:string;text:string;depth:number}[]=[];
 visit(unified().use(remarkParse).parse(text),'heading',node=>{result.push({id:`section-${node.position?.start.offset}`,text:toString(node),depth:node.depth});});
 return result;
}

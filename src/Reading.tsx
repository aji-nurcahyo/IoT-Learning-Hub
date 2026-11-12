import { useState } from 'react';
import Markdown from 'react-markdown';
import gfm from 'remark-gfm';
import math from 'remark-math';
import katex from 'rehype-katex';
import highlight from 'rehype-highlight';
import { headings } from './markdown';
import { assetUrl } from './config';
import 'katex/dist/katex.min.css';
import 'highlight.js/styles/github-dark.css';
const resolveAsset=(uri?:string)=>uri&&!uri.startsWith('https://')&&!uri.startsWith('http://')&&!uri.startsWith('#')&&!uri.startsWith('data:')?assetUrl(uri):uri;
export function RichText({text}:{text:string}) {
 return <Markdown remarkPlugins={[gfm,math]} rehypePlugins={[katex,highlight]} components={{
  h1:({node,...props})=><h1 id={`section-${node?.position?.start.offset}`} {...props}/>,h2:({node,...props})=><h2 id={`section-${node?.position?.start.offset}`} {...props}/>,h3:({node,...props})=><h3 id={`section-${node?.position?.start.offset}`} {...props}/>,
  table:({children})=><div className="table-scroll"><table>{children}</table></div>,
  img:({src,alt,title})=><figure className="prose-figure"><img src={resolveAsset(src)} alt={alt||''}/>{(alt||title)&&<figcaption>{title||alt}</figcaption>}</figure>,
  a:({href,children})=>{const resolved=resolveAsset(href);const isDownload=Boolean(href&&href.startsWith('content/')&&!/\.(md|html)$/.test(href));return <a href={resolved} {...(href?.startsWith('https://')?{target:'_blank',rel:'noreferrer'}:isDownload?{download:true}:{})}>{children}</a>;},
 }}>{text}</Markdown>;
}
export function Reading({text,label='MODUL BACAAN'}:{text:string;label?:string}){
 const [focused,setFocused]=useState(false);
 return <div className={`reader ${focused?'focused':''}`}><div className="reader-toolbar"><span>{label}</span><button aria-pressed={focused} onClick={()=>setFocused(!focused)}>{focused?'Keluar mode fokus':'Mode baca fokus'}</button></div><div className="reading-grid"><aside aria-label="Daftar isi"><h2>Di halaman ini</h2>{headings(text).filter(h=>h.depth<=3).map(h=><a key={h.id} href={`#${h.id}`} onClick={e=>{e.preventDefault();document.getElementById(h.id)?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}}>{h.text}</a>)}</aside><article className="prose"><RichText text={text}/></article></div></div>;
}

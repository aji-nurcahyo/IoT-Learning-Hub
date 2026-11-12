import { useEffect, useRef, useState } from 'react';
import Reveal from 'reveal.js';
import 'reveal.js/dist/reveal.css';
import { RichText } from './Reading';
import { deckSchema } from './schema';
import { site } from './config';
export default function Deck({data}:{data:unknown}){
 const slides=deckSchema.parse(data), host=useRef<HTMLDivElement>(null), api=useRef<Reveal.Api|null>(null);
 const [index,setIndex]=useState(0),[error,setError]=useState(''),[notes,setNotes]=useState(false);
 useEffect(()=>{
  if(!host.current)return;
  const deck=new Reveal(host.current,{embedded:true,hash:false,history:false,respondToHashChanges:false,controls:true,progress:true,slideNumber:'c/t',width:1100,height:680,margin:0.08,transition:matchMedia('(prefers-reduced-motion: reduce)').matches?'none':'fade',keyboardCondition:'focused'});
  let disposed=false; api.current=deck;
  deck.on('slidechanged',()=>setIndex(deck.getIndices().h));
  void deck.initialize().then(()=>{if(disposed)void deck.destroy();}).catch(()=>{if(!disposed)setError('Presentasi gagal dimuat. Coba muat ulang.');});
  return()=>{disposed=true;api.current=null;void deck.destroy();};
 },[]);
 return <div className="deck-area"><div className="deck-toolbar"><span>Slide {index+1} / {slides.length}</span><button onClick={()=>setNotes(!notes)} aria-pressed={notes}>Catatan presenter</button><button onClick={()=>{void host.current?.requestFullscreen().catch(()=>setError('Layar penuh tidak tersedia pada browser ini.'));}}>Layar penuh</button></div>{error&&<p role="alert">{error}</p>}<div className="reveal" ref={host} tabIndex={0} aria-label="Presentasi interaktif"><div className="slides">{slides.map((s,i)=><section key={i}><small>{site.shortName} · PRESENTASI</small><h2>{s.title}</h2><div className="slide-body"><RichText text={s.body}/>{s.fragment&&<p className="fragment">{s.fragment}</p>}</div></section>)}</div></div><div className="deck-toolbar"><button onClick={()=>api.current?.prev()} disabled={index===0}>← Sebelumnya</button><span>Klik slide, lalu gunakan tombol panah. Esc: overview.</span><button onClick={()=>api.current?.next()} disabled={index===slides.length-1}>Berikutnya →</button></div>{notes&&<aside className="notice"><strong>Catatan presenter</strong><p>{slides[index].notes}</p></aside>}</div>;
}

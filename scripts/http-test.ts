import { build } from 'vite';
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { resolve, extname } from 'node:path';
import assert from 'node:assert/strict';
import { normalizeBase } from './base';
const data=JSON.parse(readFileSync('content/catalog.json','utf8'));
const walk=(dir:string):string[]=>readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(resolve(dir,e.name)):[resolve(dir,e.name)]);
const mime:Record<string,string>={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.md':'text/plain','.woff2':'font/woff2','.svg':'image/svg+xml','.csv':'text/csv','.txt':'text/plain','.py':'text/plain','.ino':'text/plain','.h':'text/plain'};
try{
for(const base of ['/iot-learning-hub/','/','/kelas/iot/']){
 process.env.VITE_BASE_PATH=base;await build({logLevel:'error'});
 const root=resolve('dist');
 const server=createServer((req,res)=>{const pathname=new URL(req.url!,'http://localhost').pathname;if(!pathname.startsWith(base)){res.writeHead(404).end();return;}const rel=decodeURIComponent(pathname.slice(base.length))||'index.html';const file=resolve(root,rel);if(!file.startsWith(root)||!existsSync(file)||!statSync(file).isFile()){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[extname(file)]||'application/octet-stream');res.end(readFileSync(file));});
 await new Promise<void>(r=>server.listen(0,'127.0.0.1',r));
 const address=server.address();if(!address||typeof address==='string')throw Error('No address');
 const origin=`http://127.0.0.1:${address.port}`;
 try{
  const home=await fetch(origin+base);assert.equal(home.status,200);const html=await home.text();
  assert.ok(html.includes('Internet of Things Learning Hub'));const urls=[...html.matchAll(/(?:src|href)="([^"]+)"/g)].map(x=>x[1]);
  assert.ok(urls.length>=2);for(const url of urls){assert.ok(url.startsWith(base),`${url} harus memakai ${base}`);const r=await fetch(origin+url);assert.equal(r.status,200);assert.ok(!(await r.text()).startsWith('<!doctype'));}
  for(const r of data.foundationResources){const response=await fetch(origin+base+r.path);assert.equal(response.status,200);assert.deepEqual(Buffer.from(await response.arrayBuffer()),readFileSync(resolve('public',r.path)));}
  let count=0;for(const f of walk(root)){const rel=f.slice(root.length+1).replaceAll('\\','/');const r=await fetch(origin+base+rel);assert.equal(r.status,200,rel);count++;}
  assert.equal((await fetch(origin+base+'.nojekyll')).status,200);assert.equal((await fetch(origin+base+'404.html')).status,200);assert.equal((await fetch(origin+base+'missing-resource.json')).status,404);
  assert.equal(normalizeBase(base),base);console.log(`PASS HTTP ${base}: ${count} file, asset prefix, download bytes, .nojekyll, 404, missing resource.`);
 }finally{await new Promise<void>((r,j)=>server.close(e=>e?j(e):r()));}
}
}finally{delete process.env.VITE_BASE_PATH;await build({logLevel:'error'});console.log('Build final dikembalikan ke /iot-learning-hub/.');}

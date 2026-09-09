import http from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=fileURLToPath(new URL('.',import.meta.url));
const allowed=new Set(['sources.html','sources.mjs','provenance.mjs','sources/joint-census-api.json','sources/orientation-2024.xlsx','calculator.html','dating.mjs','dating-model.mjs','dating.css','data/filters.json','sources/qualifications-2021.xlsx','sources/hse-2024.xlsx','sources/hmrc-2023-24.ods','index.html','app.mjs','model.mjs','style.css','data/evidence.json','sources/mye24tablesuk.xlsx','sources/living-arrangements.xlsx']);
const types={'.html':'text/html; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','.ods':'application/vnd.oasis.opendocument.spreadsheet'};
const server=http.createServer(async(req,res)=>{
 try {
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
  const url=new URL(req.url,'http://localhost');
  if(url.pathname==='/health'){res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({status:'ok',version:'3.3.0',pid:process.pid}));return;}
  const name=decodeURIComponent(url.pathname).replace(/^\//,'')||'calculator.html';
  if(!allowed.has(name)){res.writeHead(404);res.end('Not found');return;}
  const file=await readFile(path.join(root,name));
  res.writeHead(200,{'Content-Type':types[path.extname(name)],'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer'});
  res.end(req.method==='HEAD'?undefined:file);
 } catch {res.writeHead(500);res.end('Unable to load resource');}
});
// Port zero asks the OS to allocate a genuinely free, random port to this process.
server.listen(Number(process.env.PORT||0),'127.0.0.1',()=>console.log(`UK Dating V3: http://127.0.0.1:${server.address().port} (PID ${process.pid})`));

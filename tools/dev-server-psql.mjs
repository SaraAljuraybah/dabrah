// خادم تجربة محلي بدون مكتبات: يخدم site/ ويمرر /api/* للراوتر على PostgreSQL محلي عبر psql.
// التشغيل: PGURI="host=localhost user=postgres dbname=dabrah" node tools/dev-server-psql.mjs ثم افتح http://localhost:8899
// خادم تجربة محلي: يخدم site/ ويمرر /api/* للراوتر على PostgreSQL المحلي عبر psql
import http from 'node:http';import fs from 'node:fs';import path from 'node:path';import { execFileSync } from 'node:child_process';
import { handle } from '../netlify/functions/lib/routes.mjs';
const uri=process.env.PGURI||'host=/tmp port=5544 user=postgres dbname=dabrah';
const lit=v=>v===null||v===undefined?'NULL':typeof v==='number'||typeof v==='boolean'?String(v):"'"+String(v).replace(/'/g,"''")+"'";
const db={async query(t,p=[]){const sql=t.replace(/\$(\d+)/g,(_,i)=>lit(p[i-1]));const rd=/^\s*SELECT/i.test(sql)||/RETURNING/i.test(sql);const o=execFileSync('psql',[uri,'-v','ON_ERROR_STOP=1','-Atq','-c',rd?`WITH t AS (${sql}) SELECT COALESCE(json_agg(t),'[]') FROM t`:sql],{encoding:'utf8'}).trim();return {rows:rd?JSON.parse(o||'[]'):[]}}};
const root=new URL('../site/',import.meta.url).pathname;
http.createServer(async(req,res)=>{const u=new URL(req.url,'http://x');
 if(u.pathname.startsWith('/api/')){let b='';for await(const c of req)b+=c;let body={};try{body=JSON.parse(b||'{}')}catch{}body.role=body.role||req.headers['x-dabrah-role'];
  try{const o=await handle(db,req.method,u.pathname.slice(4),body);res.writeHead(o.status,{'content-type':'application/json'});res.end(JSON.stringify(o.body))}catch(e){console.error(e);res.writeHead(500);res.end('{}')}return}
 if(u.pathname==='/env.js'){res.writeHead(200,{'content-type':'text/javascript'});res.end('window.__ENV={API_BASE:"/api"};');return}
 const f=path.join(root,u.pathname==='/'?'index.html':u.pathname);if(fs.existsSync(f)){res.writeHead(200,{'content-type':f.endsWith('.html')?'text/html; charset=utf-8':'application/octet-stream'});fs.createReadStream(f).pipe(res)}else{res.writeHead(404);res.end()}
}).listen(8899,()=>console.log('dev on 8899'));

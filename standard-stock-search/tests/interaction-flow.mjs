// Offline workflow fixture. These records are not sourcing results.
import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
import {headers,processTask} from '../scripts/core.mjs';
import assert from 'node:assert/strict';
const [mode,dir]=process.argv.slice(2);
await fs.mkdir(dir,{recursive:true});
if(mode==='input'){
 const w=Workbook.create(),s=w.worksheets.add('采购需求');
 s.getRange('A4:L4').values=[headers];
 s.getRange('A5:L12').values=Array.from({length:8},(_,i)=>[`P${String(i+1).padStart(3,'0')}`,'离线模拟商品','模拟品牌',`SIM-${i+1}`,10,'个','中国',i<2?'武汉市':null,null,null,'否',null]);
 w.recalculate();await(await SpreadsheetFile.exportXlsx(w)).save(dir+'/input.xlsx');
}else{
 const task=JSON.parse(await fs.readFile(dir+'/import.json','utf8'));
 assert.equal(task.requests.length,8);
 assert.equal(task.requests.filter(r=>r.status==='待补充').length,6);
 assert.equal(task.questions.length,6);
 assert.equal(task.requests[2].id,'P003');
 const c={complete:true,queries:['离线模拟，无网络'],scope:'模拟测试',stop_reason:'测试结束'};
 for(const r of task.requests.filter(r=>!r.status))task.coverage[r.id]={mainland:c,global:c};
 const initial=processTask(task);
 assert.equal(initial.summary.filter(r=>r.status==='待补充').length,6);
 await fs.writeFile(dir+'/initial.json',JSON.stringify(task));
 // Apply one explicit input correction. Do not propagate it to other rows.
 const r=task.requests.find(r=>r.id==='P003');r.city='武汉市';delete r.status;delete r.pending_reason;
 task.coverage[r.id]={mainland:c,global:c};
 const after=processTask(task);
 assert.equal(after.summary.length,8);
 assert.equal(after.summary.filter(r=>r.status==='待补充').length,5);
 assert.equal(task.requests.find(r=>r.id==='P004').city,null);
 await fs.writeFile(dir+'/after.json',JSON.stringify(task));
 console.log('8项需求：2项可搜索/6项待补充；单项补充后3项可处理/5项仍待补充；编号保持不变');
}

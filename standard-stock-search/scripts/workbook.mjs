import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
import {headers} from './core.mjs';
import {buildSheets} from './report_data.mjs';
import {alignReportSheet} from './quote_format.mjs';

function safe(v){return typeof v==='string'&&/^[=+@-]/.test(v)?"'"+v:v??null;}
const [mode,input,output]=process.argv.slice(2);
const dest=mode==='template'?input:output;
if(!dest||!['template','report','questions'].includes(mode)) throw Error('用法: template 输出.xlsx | report 任务.json 输出.xlsx | questions 问题.json 输出.xlsx');
try{await fs.access(dest);throw Error('输出已存在，请使用新路径');}catch(e){if(e.code!=='ENOENT')throw e;}
const wb=Workbook.create();
function sheet(name,title,labels,rows,width=22){
 const s=wb.worksheets.add(name);s.showGridLines=false;
 s.getRange('A2').values=[[title]];
 s.getRange('A2').format.font={name:'Arial',size:14,bold:true};
 const all=[labels,...rows].map(r=>r.map(safe));
 s.getRangeByIndexes(3,0,all.length,labels.length).values=all;
 const area=s.getRangeByIndexes(3,0,all.length,labels.length);
 area.format.font={name:'Arial',size:10};area.format.columnWidth=width;area.format.rowHeight=36;area.format.wrapText=true;area.format.verticalAlignment='center';
 for(let i=0;i<labels.length;i++){if(/编号|型号/.test(labels[i]))s.getRangeByIndexes(4,i,Math.max(1,rows.length),1).setNumberFormat('@');}
 const h=s.getRangeByIndexes(3,0,1,labels.length);h.format.fill='#254761';h.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};h.format.rowHeight=32;h.format.horizontalAlignment='center';
 s.freezePanes.freezeRows(4);s.tables.add(s.getRangeByIndexes(3,0,Math.max(2,all.length),labels.length),true,'StockTable'+wb.worksheets.items.length);
 alignReportSheet(s,4+rows.length);
 area.format.autofitRows();
 return s;
}
if(mode==='template'){
 const s=sheet('采购需求','采购需求填写表',headers,Array.from({length:100},()=>Array(12).fill(null)));
 s.getRange('A3').values=[['前8列必填；一行一个产品；黄色区域可填写；填写后上传给 Agent。']];s.getRange('A3:H3').merge();
 s.getRange('A5:L104').format.fill='#FFF8DF';
 for(const col of ['A','B','C','D','F','G','H'])s.getRange(`${col}5:${col}104`).setNumberFormat('@');
 s.getRange('E5:E104').setNumberFormat('0.####');
 s.getRange('K5:K104').dataValidation={rule:{type:'list',values:['是','否']}};
 s.getRange('A5:H104').conditionalFormats.addCustom('AND(COUNTA($A5:$L5)>0,A5="")',{fill:'#FCE4D6'});
 sheet('填写说明','填写说明',['项目','要求'],[
 ['必填项','需求编号、产品名称、品牌、完整型号、需求数量、单位、收货国家/地区、收货城市'],
 ['编号和型号','使用文本，保留前导零及完整后缀；需求编号不能重复。'],
 ['无品牌/型号','明确填无品牌或无型号，并补充足以唯一匹配的规格。'],
 ['数量与单位','数量填正数，单位明确到个、盒、卷、套等。'],
 ['采购要求','仅全新原装；替代品默认不接受。交期可填YYYY-MM-DD。'],
 ['填写区域','预留100行，可继续添加；不要修改第4行表头。缺失项以导入校验为准。'],
 ['示例（勿填入需求表）','001 / 断路器 / 示例品牌 / 001-ABC / 10 / 个 / 中国大陆 / 上海']
 ],65);
}else{
 const task=JSON.parse(await fs.readFile(input,'utf8'));
 for(const d of buildSheets(mode,task)){
  const s=sheet(d.name,d.title,d.labels,d.rows,d.width);
  if(mode==='questions'){
   s.getRange(`A4:G${4+d.rows.length}`).format.horizontalAlignment='center';
   s.getRange(`F5:F${4+d.rows.length}`).format.fill='#FFF8DF';
   s.getRange(`D5:F${4+d.rows.length}`).format.columnWidth=45;
   s.getRange(`A5:G${4+d.rows.length}`).format.rowHeight=65;
  }
 }
}
wb.recalculate();
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1200})).ndjson);
await fs.mkdir(path.dirname(dest),{recursive:true});
await (await SpreadsheetFile.exportXlsx(wb)).save(dest);
if(process.env.STOCK_PREVIEW_DIR){
 await fs.mkdir(process.env.STOCK_PREVIEW_DIR,{recursive:true});
 for(const s of wb.worksheets.items){
  const cols=s.name==='渠道报价明细'?34:s.name==='需求汇总'?11:s.name==='采购需求'?12:2;
  for(let start=0;start<cols;start+=6){
   const letter=n=>{let x='';for(n++;n;n=Math.floor((n-1)/26))x=String.fromCharCode(65+(n-1)%26)+x;return x;};
   const range=`${letter(start)}1:${letter(Math.min(cols-1,start+5))}11`;
   const blob=await wb.render({sheetName:s.name,range,scale:1.2,format:'png'});await fs.writeFile(path.join(process.env.STOCK_PREVIEW_DIR,s.name+'-'+start+'.png'),new Uint8Array(await blob.arrayBuffer()));
  }
 }
}
console.log(dest);

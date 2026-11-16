import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
import {headers} from '../scripts/core.mjs';
const dir=process.argv[2];await fs.mkdir(dir,{recursive:true});
const valid=['001','模拟商品','模拟品牌','001-A',20,'个','中国大陆','上海',null,null,'否',null];
const cases={valid:[valid],missing_city:[[...valid.slice(0,7),'',...valid.slice(8)]],duplicate:[valid,valid],negative:[[...valid.slice(0,4),-1,...valid.slice(5)]],numeric_model:[[...valid.slice(0,3),123,...valid.slice(4)]],no_model:[[...valid.slice(0,3),'无型号',...valid.slice(4)]],formula:[valid]};
cases.mixed=[valid,['002',...valid.slice(1,7),'',...valid.slice(8)]];
for(const [name,rows] of Object.entries(cases)){
 const w=Workbook.create(),s=w.worksheets.add('采购需求');s.getRange('A4:L4').values=[headers];s.getRangeByIndexes(4,0,rows.length,12).values=rows;
 if(name==='formula')s.getRange('D5').formulas=[['="001-A"']];
 w.recalculate();await (await SpreadsheetFile.exportXlsx(w)).save(dir+'/'+name+'.xlsx');
}

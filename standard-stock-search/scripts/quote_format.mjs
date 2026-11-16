// Headers and body share centered alignment, including unknown values.
export function alignQuoteColumns(sheet,lastRow){
 const end=Math.max(5,lastRow);
 sheet.getRange(`A4:AH${end}`).format.verticalAlignment='center';
 sheet.getRange('A4:AH4').format.horizontalAlignment='center';
 sheet.getRange(`A5:AH${end}`).format.horizontalAlignment='center';
}

export function alignReportSheet(sheet,lastRow){
 if(sheet.name==='渠道报价明细')return alignQuoteColumns(sheet,lastRow);
 const lastCol=sheet.name==='需求汇总'?'K':sheet.name==='查询说明'?'B':null;
 if(!lastCol)return;
 const end=Math.max(5,lastRow);
 sheet.getRange(`A4:${lastCol}${end}`).format.verticalAlignment='center';
 sheet.getRange(`A4:${lastCol}4`).format.horizontalAlignment='center';
 sheet.getRange(`A5:${lastCol}${end}`).format.horizontalAlignment='center';
}

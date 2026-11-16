"""Fallback for hosts without artifact-tool. Python/openpyxl + Node core, offline."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import unicodedata
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

BASE=Path(__file__).resolve().parents[1]

def generate(mode,input_path,output):
    output=Path(output)
    if output.exists():
        raise ValueError('输出已存在，请使用新路径')
    if mode=='template':
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('xb') as f,(BASE/'assets/采购需求模板.xlsx').open('rb') as source:
            shutil.copyfileobj(source,f)
        return
    node=shutil.which('node')
    if not node:raise ValueError('报告/清单需Node.js运行共享校验逻辑；本工具无需artifact-tool')
    p=subprocess.run([node,str(BASE/'scripts/export_data.mjs'),mode,str(Path(input_path).resolve())],capture_output=True,text=True,timeout=120)
    if p.returncode:raise ValueError(p.stderr.strip() or '共享数据校验失败')
    sheets=json.loads(p.stdout)
    wb=Workbook();wb.remove(wb.active)
    for idx,data in enumerate(sheets,1):
        ws=wb.create_sheet(data['name']);ws.sheet_view.showGridLines=False;ws.freeze_panes='A5'
        ws.cell(2,1,data['title']).font=Font(name='Arial',size=14,bold=True)
        ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=min(6,len(data['labels'])))
        ws.row_dimensions[2].height=28
        for col,label in enumerate(data['labels'],1):
            ws.column_dimensions[get_column_letter(col)].width=data['width']
            c=ws.cell(4,col,label);c.font=Font(name='Arial',size=10,bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='254761');c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
        if ws.title=='查询说明':ws.column_dimensions['A'].width=28;ws.column_dimensions['B'].width=110
        if ws.title=='需求汇总':
            for col in ['H','K']:ws.column_dimensions[col].width=50
        if ws.title=='渠道报价明细':
            for col in ['X','Y','Z','AD','AF','AH']:ws.column_dimensions[col].width=55
            ws.column_dimensions['AA'].width=40
        if mode=='questions':
            for col in ['D','E','F']:ws.column_dimensions[col].width=45
        ws.row_dimensions[4].height=32
        rows=data['rows'] or [[None]*len(data['labels'])]
        for row_index,values in enumerate(rows,5):
            max_lines=1
            for col,value in enumerate(values,1):
                c=ws.cell(row_index,col,value)
                if isinstance(value,str):c.data_type='s' # retain leading zeroes; never execute source text
                c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True);c.font=Font(name='Arial',size=10)
                if isinstance(value,(int,float)) and not isinstance(value,bool):c.number_format='#,##0' if float(value).is_integer() else '0.000000' if data['labels'][col-1]=='汇率' else '0.0000'
                if '编号' in data['labels'][col-1] or '型号' in data['labels'][col-1]:c.number_format='@'
                text='' if value is None else str(value)
                width=ws.column_dimensions[get_column_letter(col)].width
                lines=sum(max(1,math.ceil(sum(2 if unicodedata.east_asian_width(ch) in ('W','F') else 1 for ch in line)/max(1,width-2))) for line in text.split('\n'))
                max_lines=max(max_lines,lines)
                if mode=='questions' and col==6:c.fill=PatternFill('solid',fgColor='FFF8DF')
            ws.row_dimensions[row_index].height=min(409,max(20,max_lines*15+5))
        table=Table(displayName=f'StockTable{idx}',ref=f'A4:{get_column_letter(len(data["labels"]))}{4+len(rows)}')
        table.tableStyleInfo=TableStyleInfo(name='TableStyleMedium2',showRowStripes=True)
        ws.add_table(table)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('xb') as f:wb.save(f)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['template','report','questions'])
    p.add_argument('paths',nargs='+')
    a=p.parse_args()
    expected=1 if a.mode=='template' else 2
    if len(a.paths)!=expected:p.error('template需输出路径；report/questions需输入JSON与输出路径')
    try:
        generate(a.mode,None if a.mode=='template' else a.paths[0],a.paths[-1]);print(a.paths[-1])
    except (ValueError,OSError,subprocess.TimeoutExpired) as exc:sys.exit(str(exc))

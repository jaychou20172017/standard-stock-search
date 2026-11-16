"""Build a whitelist-only portable package; exclude runtime and business data."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import json

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('output')
args = parser.parse_args()
base = root / 'standard-stock-search'
files = json.loads((base / 'manifest.json').read_text(encoding='utf-8'))
if (root / 'LICENSE').read_bytes() != (base / 'LICENSE').read_bytes():
    raise SystemExit('拒绝打包：项目与技能目录的许可条款不一致')
from openpyxl import load_workbook
ws = load_workbook(base / 'assets/采购需求模板.xlsx', data_only=False)['采购需求']
if any(c.value is not None for row in ws.iter_rows(min_row=5) for c in row):
    raise SystemExit('拒绝打包：模板含有填写数据')
with ZipFile(args.output, 'x', compression=ZIP_DEFLATED) as z:
    for name in files:
        z.write(base / name, 'standard-stock-search/' + name)
print(f'已打包 {len(files)} 个文件')

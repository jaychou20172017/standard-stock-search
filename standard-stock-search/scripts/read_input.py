"""Read and validate the procurement workbook; never evaluates Excel formulas."""
import json, sys, math
from pathlib import Path
from openpyxl import load_workbook

HEADERS = ['需求编号','产品名称','品牌','完整型号','需求数量','计量单位','收货国家/地区','收货城市','期望到货日期','规格补充','接受替代品','其他采购要求']
KEYS = ['id','name','brand','model','quantity','unit','country','city','due','spec','alternatives','requirements']

def read(path, batch=False):
    wb = load_workbook(path, data_only=False, read_only=True)
    ws = wb['采购需求']
    if [c.value for c in next(ws.iter_rows(min_row=4,max_row=4,max_col=12))] != HEADERS:
        raise ValueError('请使用模板，不要修改第4行列名')
    result, seen, issues = [], set(), []
    raw_rows = []
    for source_row, row in enumerate(ws.iter_rows(min_row=5, max_col=12),5):
        if all(c.value is None for c in row):
            continue
        raw = {k: (c.value.strip() if isinstance(c.value, str) else c.value) for k, c in zip(KEYS, row)}
        raw["source_row"] = source_row
        raw_rows.append(raw)
        try:
            values = []
            for c in row:
                if c.data_type == 'f':
                    raise ValueError(f'{c.coordinate}: 不接受公式，请填写原始值')
                values.append(c.value.strip() if isinstance(c.value, str) else c.value)
            r = dict(zip(KEYS, values))
            for k in KEYS[:8]:
                if r[k] is None or r[k] == '':
                    raise ValueError(f'第{source_row}行缺少 {HEADERS[KEYS.index(k)]}')
            for k in ['id','brand','model']:
                if not isinstance(r[k], str):
                    raise ValueError(f'第{source_row}行 {k}须为文本，以保留前导零')
            n = r['quantity']
            if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or n <= 0:
                raise ValueError('需求数量必须为正数')
            if r['id'] in seen:
                raise ValueError('需求编号重复')
            seen.add(r['id'])
            if r['alternatives'] not in (None, '', '是', '否'):
                raise ValueError('接受替代品仅填是或否')
            r['alternatives'] = r['alternatives'] or '否'
            for k in ['brand','model']:
                if r[k] in ('无品牌','无型号') and not r['spec']:
                    raise ValueError('无品牌/无型号时规格补充必填')
            r["source_row"] = source_row
            result.append(r)
        except ValueError as exc:
            if not batch:
                raise
            issues.append({"source_row": source_row, "question": str(exc)})
    if not raw_rows:
        raise ValueError('模板尚未填写')
    if not batch:
        return result
    counts = {}
    for r in raw_rows:
        key = str(r.get('id'))
        counts[key] = counts.get(key, 0) + 1
    invalid = {i['source_row'] for i in issues}
    for r in raw_rows:
        if counts[str(r.get('id'))] > 1:
            invalid.add(r['source_row'])
            issues.append({'source_row':r['source_row'],'question':'需求编号重复，请按源行确认唯一编号'})
    ready = {r['source_row']:r for r in result}
    requests = []
    occupied = {r['id'] for r in result if r['source_row'] not in invalid}
    for raw in raw_rows:
        line=raw['source_row']
        if line not in invalid:
            requests.append(ready[line])
            continue
        original=raw.get('id')
        usable=isinstance(original,str) and bool(original.strip()) and counts[str(original)]==1
        temp=original if usable else f"待确认-源行{line}"
        while temp in occupied: temp+='-临时'
        occupied.add(temp)
        requests.append({**raw,'original_id':raw.get('id'),'id':temp,'status':'待补充','pending_reason':'；'.join(dict.fromkeys(i['question'] for i in issues if i['source_row']==line))})
    return {'requests':requests,'questions':[{**i,'issue_id':f"Q{n:03d}",'request_id':next(r['id'] for r in requests if r['source_row']==i['source_row'])} for n,i in enumerate(issues,1)],'quotes':[],'coverage':{}}

if __name__ == '__main__':
    try:
        data = read(sys.argv[1], batch=True) if '--batch' in sys.argv[3:] else {'requests': read(sys.argv[1]), 'quotes': [], 'coverage': {}}
        with Path(sys.argv[2]).open('x', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        pending=sum(r.get('status')=='待补充' for r in data['requests'])
        print(f'共 {len(data["requests"])} 项需求；可搜索 {len(data["requests"])-pending} 项，待补充 {pending} 项')
    except (ValueError, KeyError, FileExistsError) as exc:
        sys.exit(str(exc))

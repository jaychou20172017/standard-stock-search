"""Offline readiness check. Does not install dependencies or change settings."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

base = Path(__file__).resolve().parents[1]
checks = {
    'python': {'ready': sys.version_info >= (3, 9), 'version': sys.version.split()[0]},
    'input_reader': {'ready': importlib.util.find_spec('openpyxl') is not None},
    'template': {'ready': (base / 'assets' / '采购需求模板.xlsx').is_file()},
}
node = shutil.which('node')
checks['excel_generator'] = {'ready': False}
if node:
    try:
        p = subprocess.run([node, '--input-type=module', '-e',
                            "await import('@oai/artifact-tool'); console.log('ready')"],
                           cwd=base, capture_output=True, text=True, timeout=20)
        checks['excel_generator'] = {
            'ready': p.returncode == 0,
            'detail': '可导入Excel组件' if p.returncode == 0 else '无法导入@oai/artifact-tool；需配置依赖或等价Excel工具'
        }
    except (OSError, subprocess.TimeoutExpired):
        checks['excel_generator']['detail'] = 'Node执行失败或超时'
else:
    checks['excel_generator']['detail'] = '未找到Node.js'
if checks['excel_generator']['ready']:
    checks['excel_generator']['backend']='artifact-tool'
elif node and checks['input_reader']['ready'] and (base/'scripts/workbook_portable.py').is_file():
    try:
        probe=subprocess.run([node,'--input-type=module','-e',"await import('./scripts/report_data.mjs')"],cwd=base,capture_output=True,text=True,timeout=20)
        if probe.returncode==0:
            checks['excel_generator']={'ready':True,'backend':'portable-python','detail':'Python/openpyxl写Excel，Node运行共享校验；无需artifact-tool'}
        else:
            checks['excel_generator']['detail']='备用后端共享数据模块无法导入，请核对Node版本和包内资源'
    except (OSError,subprocess.TimeoutExpired):
        checks['excel_generator']['detail']='备用后端共享数据模块检查失败'
ready = all(c['ready'] for c in checks.values())
print(json.dumps({'local_tools_ready': ready, 'checks': checks,
                  'not_checked': ['Agent联网检索', '附件读写权限', '客户端技能发现', '跨电脑实机运行']},
                 ensure_ascii=False, indent=2))
sys.exit(0 if ready else 1)

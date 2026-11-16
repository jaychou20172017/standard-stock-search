"""Install a portable skill into an explicit project. Standard library only."""
import argparse
import json
from pathlib import Path, PurePosixPath
import shutil
import sys

PROFILES = {'claude-code': '.claude', 'comate': '.comate', 'qwen-code': '.qwen'}

def install(agent, project, apply=False, source=None):
    source = Path(source or Path(__file__).resolve().parents[1]).resolve()
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError('项目目录不存在，请提供已有的工作目录')
    if agent not in PROFILES:
        raise ValueError('不支持此安装目标；千问桌面和豆包使用手动附件方案')
    target = project / PROFILES[agent] / 'skills' / 'standard-stock-search'
    for p in [project / PROFILES[agent], target.parent, target]:
        if p.is_symlink():
            raise ValueError(f'目标路径包含符号链接，未写入：{p}')
    if target.exists():
        raise ValueError(f'目标已存在，拒绝覆盖：{target}')
    files = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
    if not isinstance(files, list) or len(files) != len(set(files)):
        raise ValueError('安装清单无效')
    for name in files:
        rel = PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or '\\' in name:
            raise ValueError('安装清单含无效路径')
        p = source / name
        if not p.is_file() or p.is_symlink() or source not in p.resolve().parents:
            raise ValueError(f'缺少必要资源或资源不可迁移：{name}')
    result = {'agent': agent, 'target': str(target), 'file_count': len(files),
              'applied': apply, 'dependencies_installed': False,
              'client_verified': False}
    if apply:
        target.mkdir(parents=True, exist_ok=False)
        for name in files:
            dest = target / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, dest)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', required=True, choices=PROFILES)
    parser.add_argument('--project', required=True)
    parser.add_argument('--apply', action='store_true', help='执行复制；省略时仅显示安装计划')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.agent, args.project, args.apply), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))

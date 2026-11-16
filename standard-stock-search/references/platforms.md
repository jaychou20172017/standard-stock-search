# 使用与跨电脑迁移

## 核心运行条件

先在解压后的技能目录运行 `python3 scripts/check_runtime.py`。此命令离线、只读，不会安装依赖；返回 local_tools_ready 仅代表本地脚本依赖具备，不代表Agent可以联网或已经识别技能。

Agent需要联网搜索、读取附件及交付文件能力。本包支持现有Node/artifact-tool后端，以及缺少该组件时的Python/openpyxl备用后端。备用后端仍需Node.js（支持ES modules）运行共享筛选、排序和数据校验，避免维护两套业务算法。Python需3.9或以上及openpyxl。运行环境检查会显示backend，不自动安装任何依赖。

没有artifact-tool、但Python/openpyxl及Node可用的迁移目录可运行：

```text
python3 scripts/workbook_portable.py template 新空白模板.xlsx
python3 scripts/workbook_portable.py questions 问题.json 待确认清单.xlsx
python3 scripts/workbook_portable.py report 任务.json 搜索结果.xlsx
```

模板命令复制随包空白模板；report/questions写真正的xlsx，使用相同字段和业务结果，三页表头正文居中，清单决定留空。缺少Python/openpyxl/Node时须配置依赖或等价工具，不能宣称无依赖运行；依赖安装按所在环境权限执行。

```text
node --input-type=module -e "import('@oai/artifact-tool').then(()=>console.log('Excel ready'))"
python3 -c "import openpyxl; print('Input ready')"
```

Windows 可将 python3 替换为实际可用的 python。所有业务路径通过命令参数传入；包含空格的路径需引号。生成工具拒绝覆盖既有文件。

## Codex

可先在当前对话指定解压目录中的 SKILL.md，要求按其执行。需要工作区发现时，把整个 standard-stock-search 文件夹放在工作区的 `.agents/skills/` 中；Codex官方支持此目录及符号链接。技能名为 `$standard-stock-search`。官方说明：https://learn.chatgpt.com/docs/build-skills 。如未显示，重新打开会话或重启Codex；不能将目录安装成功视为客户端已调用成功。

## WorkBuddy

官方文档确认技能机制及 SKILL.md 资源结构：
https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market
https://open.workbuddy.cn/docs/skill

使用客户端当前提供的本地技能导入入口选择技能包；具体入口以安装版本为准。导入后先要求返回空白模板，再用测试需求验证联网和报告生成。官方机制存在不代表本包已实机通过；本轮尚未实测。

## 豆包桌面客户端

本轮未找到足以确认原生 SKILL.md 导入和本地脚本执行能力的官方依据，不提供未经验证的安装路径。可尝试将 SKILL.md、interaction.md、workflow.md、data-contract.md 和空白模板作为任务附件，并输入：

“按所附标准品现货搜索流程执行，先检查联网、Excel读取和生成能力。无需求且数量不明先问产品数量：1个聊天填写，多个提供模板；已有需求直接校验。多产品问题集中处理，逐项先大陆、条件不满足再全球，保留全部报价和来源，按合同输出三页Excel。缺失能力先明确说明。”

这属于手动任务适配，尚非原生技能安装。附件和 Excel 生成能力需在用户客户端实测；若不能完成关键步骤，该客户端暂不满足完整功能要求。

## Claude Code

官方说明：https://code.claude.com/docs/en/skills （核对日期2026-11-15）。

将整个 standard-stock-search 文件夹复制到项目的 `.claude/skills/standard-stock-search/`，或个人目录 `~/.claude/skills/standard-stock-search/`。在该项目的Claude Code会话中输入 `/standard-stock-search`，也可直接提出标准品寻源需求让Agent匹配技能。此处针对Claude Code本地会话；不能将Claude普通聊天、Cowork或云端会话等同为同一加载机制。

先运行本包环境检查，再验证单产品聊天、多产品Excel、联网及报告交付。能加载SKILL.md不代表已具备Excel组件；本包不附带Node/Python依赖。尚未进行Claude Code客户端完整实测。

## Comate

Comate团队官方说明：https://developer.baidu.com/article/detail.html?id=6272460 （作者文心快码BaiduComate，核对日期2026-11-15）。

将整个文件夹放到项目的 `.comate/skills/standard-stock-search/`；个人使用可放 `~/.comate/skills/standard-stock-search/`。官方亦列出项目`.agents/skills/`，但同一项目选择一个入口，避免重复发现。在Agent对话输入 `/` 搜索 standard-stock-search，或用自然语言请求调用。具体客户端版本需具备Skills功能。

与编码Agent共同运行的脚本和联网工具依赖用户环境及权限；先检查运行条件再验证业务流程。尚未进行Comate客户端实测，不能宣称安装路径核对就是全流程通过。

## 千问桌面客户端

按用户的桌面客户端需求提供手动任务适配，不默认将“千问”解释成Qwen Code。当前未确认用户具体客户端名称/版本，也没有足以核实该客户端原生技能加载路径的依据；不写入猜测的隐藏目录，不把第三方文档或平台控制台技能市场当作桌面能力证明。

先将本包以下材料作为可读取附件：SKILL.md、references/interaction.md、references/workflow.md、references/data-contract.md、assets/采购需求模板.xlsx；如支持访问本地文件夹，直接指定整个文件夹。使用references/client-adapters.md中的统一启动提示词。

让客户端首先说明联网、读取Excel、生成真正.xlsx及执行本地脚本的可用能力。无法执行本包脚本时，可以用客户端的等价Excel工具，但须遵守相同数据合同、筛选规则和居中格式。缺少任何关键能力要报告具体缺项，不声称完整适配。当前属于手动适配方案，未实机验收。

### 可选：Qwen Code（与千问桌面聊天分开）

仅用户明确使用Qwen Code时采用。官方QwenLM文档：https://github.com/QwenLM/qwen-code-docs/blob/main/website/content/en/users/features/skills.md （核对日期2026-11-15）。项目目录 `.qwen/skills/standard-stock-search/`；个人目录 `~/.qwen/skills/standard-stock-search/`。用自然语言要求使用技能并确认已发现，实际手动调用入口以当前版本为准。不将该目录套用到普通千问桌面客户端。未实测。

## 迁移

复制整个 standard-stock-search 文件夹；迁移 ZIP 不含 node_modules、本机绝对路径或运行数据。每台电脑先做依赖检查。模板与规则可直接迁移，联网和脚本能力取决于 Agent。不得将用户填写的模板、任务 JSON、报价报告或凭据放入公共包。

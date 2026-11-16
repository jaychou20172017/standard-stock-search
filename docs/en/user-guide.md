# User guide

[中文](../../使用说明.md) | [Home](../../README.en.md)

## Runtime and installation

Use the entire `standard-stock-search` directory. The host Agent needs web search, attachment reading, actual .xlsx generation and file delivery. Run from that directory:

```sh
python3 scripts/check_runtime.py
```

This is an offline dependency check, not a client or network acceptance test. The Node backend uses `@oai/artifact-tool`; the portable fallback needs Python 3.9+, openpyxl and Node.js with ES modules. Dependencies are not included or installed automatically. On Windows, use the available `python` command and quote paths containing spaces.

```sh
python3 scripts/workbook_portable.py template request.xlsx
python3 scripts/read_input.py filled.xlsx task.json --batch
python3 scripts/workbook_portable.py report completed-task.json result.xlsx
python3 scripts/workbook_portable.py questions questions.json decisions.xlsx
```

`task.json` from import contains requests; the Agent must search and populate evidence, quotes and coverage before report generation. The scripts do not perform web search. Outputs refuse to overwrite existing files. With the Node backend, replace `python3 scripts/workbook_portable.py` with `node scripts/workbook.mjs`.

## Interaction

When no request is provided, the Agent asks how many items are needed. One item uses a copyable chat form: product name, brand, complete model, quantity, unit, destination country/region and city; optional due date, specifications and procurement conditions. More than one item uses Excel. Existing complete input is validated directly.

Save a separate copy of the blank template before filling it. Preserve row 4 headers. Enter one item per row; the first eight fields are required. Destination is mandatory for every task. Preserve identifiers and complete models as text. Default conditions are new/genuine, exact match, no substitutions and no combining suppliers' stock.

All requests remain in the task. Missing information is grouped by item ID or source row; valid items continue. Up to five questions are handled in chat; more use a decision workbook with blank decision cells. A response affects only explicitly identified items and decisions. Silence or “continue” is not consent to substitutions or combined sourcing.

## Excel fields

Keep the template's Chinese labels unchanged; English labels below are a reading aid.

| Chinese input field | English meaning |
|---|---|
| 需求编号 | Request ID |
| 产品名称 | Product name |
| 品牌 | Brand |
| 完整型号 | Complete model/manufacturer part number |
| 需求数量 | Required quantity |
| 单位 | Unit |
| 收货国家/地区 | Destination country/region |
| 收货城市 | Destination city |
| 期望到货日期 | Requested arrival date |
| 规格补充 | Additional specifications |
| 是否接受替代 | Accept alternatives (是 = yes; 否 = no) |
| 其他采购要求 | Other procurement requirements |

The actual labels in the supplied workbook are authoritative. Reports contain `需求汇总` (request summary), `渠道报价明细` (channel quote details), and `查询说明` (search notes). Headers and body are horizontally and vertically centered. Rows fit wrapped text without shrinking fonts; the Python fallback estimates height. Unknown prices/stock are not zero.

Qualified quotes rank by comparable CNY unit price within each request and tax group. All other quotes retain reasons for exclusion. Converted prices are references, not landed costs; public inventory is not a supply commitment.

## Clients

Codex: workspace `.agents/skills/standard-stock-search/`, invoke `$standard-stock-search`. Claude Code: `.claude/skills/standard-stock-search/`, invoke `/standard-stock-search`. Comate: `.comate/skills/standard-stock-search/`, find the skill in the client. WorkBuddy: use the installed version's local skill import facility.

The project installer previews by default and copies only with `--apply`:

```sh
python3 scripts/install_agent.py --agent claude-code --project "/path/to/project"
python3 scripts/install_agent.py --agent claude-code --project "/path/to/project" --apply
```

Other installer profiles: `comate` and `qwen-code`. Qwen Code is distinct from the Qianwen desktop chat client. Doubao desktop and Qianwen desktop currently use manual attachments/folder instructions; native import and local execution are not confirmed. See [client instructions](../../standard-stock-search/references/en/platforms.md). Other-client and other-computer acceptance tests are deferred, not passed.

## License

Noncommercial and internal business use are free under the custom license. External commercialization needs Zhou Jie's written authorization: 3504264104@qq.com. See [license translation](../../LICENSE.en.md).

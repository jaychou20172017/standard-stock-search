# Platforms and client acceptance

[中文平台说明](../platforms.md) | [中文接入流程](../client-adapters.md)

Run `python3 scripts/check_runtime.py` first; it is offline/read-only and does not install dependencies. Local readiness does not prove networking or client discovery. Node/artifact-tool is the preferred backend; Python 3.9+/openpyxl plus Node ES modules is the fallback. Both use shared business logic. Copy the entire skill directory without node_modules, private tasks or credentials. Use quoted paths; Windows may use `python` instead of `python3`. Output files are not overwritten.

| Client | Entry | Verification limit |
|---|---|---|
| Codex | `.agents/skills/standard-stock-search/`, `$standard-stock-search` | Current workspace discovered; local real sourcing completed |
| WorkBuddy | Installed client's skill import UI | Mechanism documented; this package not client-tested |
| Doubao desktop | Attach files or point to folder | Manual adaptation; native import/local execution unconfirmed |
| Claude Code | `.claude/skills/standard-stock-search/`, `/standard-stock-search` | Directory documented; full client test deferred |
| Comate | `.comate/skills/standard-stock-search/`, skill picker | Directory documented; full client test deferred |
| Qianwen desktop chat | Attach files or folder | Version/native import unconfirmed; not Qwen Code |
| Qwen Code (optional) | `.qwen/skills/standard-stock-search/` | Separate client; full test deferred |

These directory/documentation findings were checked in the Chinese references on 2026-11-15; they are not guarantees for every client version. Official sources are retained there. Do not invent installation paths for desktop chat apps.

The standard-library installer supports `claude-code`, `comate`, `qwen-code` project profiles. Run `python3 scripts/install_agent.py --agent claude-code --project "/existing/project"` to preview, then add `--apply` to copy. It does not install runtime dependencies or change global settings, refuses existing targets and copies manifest files only. Use a deliberately chosen new location for upgrades. Do not use Qwen Code paths for Qianwen desktop chat.

## Copyable manual start prompt

```text
Read the attached standard-stock-search SKILL.md and its references; English instructions are in SKILL.en.md and references/en/.
Check web search, Excel reading, actual .xlsx generation and file-delivery capabilities. Report missing capabilities honestly.
Run scripts/check_runtime.py if local commands are available; otherwise identify equivalent Excel tools.
If no request exists, ask the item count: one uses a chat form, multiple use the blank template. Validate supplied input directly.
Group questions by ID: up to five in chat, more in a decision workbook with blank responses. Continue valid items and retain pending ones.
Consent stays within the expressly identified items/decisions; “continue” does not approve substitutions or combining stock.
Search mainland China first, then globally under the per-item rules. Require new/genuine goods and keep all quotes, evidence and timestamps.
Export the three-sheet report, with centered headers/body and fitted row heights. Current Excel labels/enums remain Chinese.
Do not log in, contact suppliers or place orders.
```

## Acceptance checklist

Record exact client/version, OS/date, loading method and tools. In a fresh conversation test count-based entry and direct existing input; mixed complete/incomplete batches; more than five questions with blank decisions; one partial response leaving others pending; real sourcing with honest no-result handling; and an actual three-sheet .xlsx with readable sources/time and centered fitted rows. CSV-only or instructions-only delivery is not a pass. Same-machine tests do not establish another client's compatibility.

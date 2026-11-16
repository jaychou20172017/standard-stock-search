# Implementation and release status

[中文计划](../../implementation-plan.md) | [中文历史](../../development-status.md)

## Current implementation

One shared core implements eligibility, packaging conversion, tier selection, tax-group ranking, deduplication/conflict handling and coverage checks. `read_input.py` validates Excel in strict or batch mode, preserving incomplete requests. The Node and portable Python workbook backends share `report_data.mjs`/`export_data.mjs` and business calculations. `check_runtime.py` checks local dependencies; `install_agent.py` previews/copies whitelisted project files without changing global configuration.

Interaction rules cover count-based input, grouped questions, partial decisions, stable identifiers and stop conditions. Three report sheets retain all requests and quotes. Centered alignment and fitted row heights are implemented. The blank template is protected from packaging filled data. A manifest-based archive excludes dependencies and business records.

## Release history summary

- v0.1.0–v0.1.2: initial rules, template, core, input/report helpers, runtime check and workspace discovery.
- v0.1.3–v0.1.4: alignment changes; the latest centered header/body rule supersedes earlier left/right alignment.
- v0.1.5–v0.1.6: batch interactions, pending requests and offline end-to-end decision scenarios.
- v0.1.7–v0.1.8: additional client instructions and project installer.
- v0.1.9: portable Python backend sharing the same business logic.
- v0.1.10: two-item real search, read-only bounded input parsing and fitted row heights. Input regression and official skill-format checks passed after correcting fixture invocation and supplying temporary PyYAML.
- v0.1.11: custom licensing; noncommercial and internal business use free, external commercialization requires written authorization.
- v0.1.12: Chinese/English documentation, English license translation and public-repository preparation. Runtime Excel/CLI labels remain Chinese. Publication status is recorded separately after an actual successful push.

## Remaining scope

Other clients and another computer remain untested; the user agreed to defer them. Real missing-input and substitution/combined-sourcing decisions have not all occurred naturally; offline scenarios do not prove those client interactions. No blanket compatibility or exhaustive Internet coverage is claimed.

The English pages consolidate the current state rather than reproduce every historical Chinese log entry. Historical failures remain in the Chinese log; later successful checks supersede the corresponding obsolete status.

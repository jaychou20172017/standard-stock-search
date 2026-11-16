# Task JSON contract

[中文](../data-contract.md)

Shared scripts and JSON keys are unchanged. Use `requests`, `quotes`, `coverage` and optional `questions`. Business data belongs outside the skill package. Unknown numeric values are JSON `null`, never the string “unknown” or zero.

Requests: `id`, `name`, `brand`, `model`, positive `quantity`, `unit`, `country`, `city`, plus `due`, `spec`, `alternatives`, `requirements`. Batch pending requests may add `status`, `pending_reason`, `source_row`, `original_id`. Keep the Chinese status values `待补充` (incomplete) and `待用户确认` (awaiting user decision); these remain in reports without fabricated search coverage or qualified ranks. Clear pending status only after corresponding resolution.

Each quote requires `request_id`, `channel`, `channel_type`, `region` (`CN` or `GLOBAL`), `brand`, `model`, actual product `url`, timezone-qualified `checked_at`, and concrete `evidence`.

Boolean flags must be true only with evidence: `exact`, `original_verified`, `conditions_met`. The latter includes destination delivery, deadline and other requirements. Originality requires a manufacturer/verified authorized source; unverified seller assertions use false with notes. Compare actual models/specifications, not just string similarity.

Numeric fields: `pack_units`, `stock_packs`, `moq_packs`, `multiple_packs`, `price_pack`, `tier_min_packs`, `tier_max_packs` (null for no upper limit), `fx_cny`. A purchasable individual unit still needs evidence for pack/MOQ/multiple = 1. Currency uses ISO codes. `tax` keeps `含税` (included), `未税` (excluded) or `未知` (unknown). Foreign conversion requires `fx_source` and `fx_date`.

Additional fields: `shipping`, `origin`, `lead_time`, `stock_status`, `authorization_url`, `notes`. Stock states retain Chinese values such as `网页显示` (web listing), `供应商确认` (supplier confirmed), `未知` (unknown). Save authorization source and evidence.

`coverage` is indexed by request ID with `mainland` and, where required, `global`. Each stage contains boolean `complete`, actual `queries` array, `scope`, `stop_reason`, `checked_at`, `obstacles`. Complete means this round's scoped queries were done, not the entire Internet. Incomplete required coverage blocks a final report. Completed coverage with no quotes is allowed.

Questions contain `issue_id`, `request_id`, `source_row`, `question` and optional `options`; exported user-decision cells are blank. The Agent validates consent rather than automatically approving it.

Report sheets are `需求汇总` (summary), `渠道报价明细` (quotes), `查询说明` (notes). Headers and body are horizontally/vertically centered. Fit row height to wrapped text at current widths/font; do not shrink fonts. The Node backend uses autofit; Python estimates display width. Inspect long text after export. `evaluate` checks provided facts; it neither searches nor proves those facts true.

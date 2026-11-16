# 任务 JSON 合同

互动任务可给需求加 status（待补充或待用户确认）及必填 pending_reason、source_row、original_id。这两种状态的需求在总报告保留，不要求伪造检索覆盖，不进入合格报价排名。其余需求仍必须完成原有覆盖检查。--batch返回questions，包含issue_id、request_id、source_row、question；用户决定不由脚本自动接受，按interaction.md核对后才更新需求/规则。修复输入后清除待补充状态；已完成原条件搜索但等待拼单/替代决定时可保留原结果，以待用户确认状态交付，不声称全任务完成。

报告三个sheet的列标题及正文全部统一水平居中、垂直居中，包括文字、数字、链接及未知占位内容，不再按数据类型区分对齐。规则由 scripts/quote_format.mjs 维护，不改变原始数据。

各行行高按该行文字在当前列宽、字号下的实际换行自动适配，避免整表固定大行高；保留少量上下留白，不缩小字号。Node后端使用autofitRows；便携Python后端按文字显示宽度估算行高。输出后检查长文本没有截断。

先用 read_input.py 导出 requests，保留全部字段；quotes 与 coverage 由 Agent 检索后填写。运行数据存用户指定目录，不存入 skill 包。

每项需求：id、name、brand、model、quantity（正数）、unit、country、city，以及 due、spec、alternatives、requirements。

每条 quotes 必须有：request_id、channel、channel_type、region（CN 或 GLOBAL）、brand、model、url（实际商品网页）、checked_at（带时区的查询时间）、evidence（型号、库存、原装及采购条件的具体判定依据）。

判定字段 exact、original_verified、conditions_met 均为布尔值；只有明确证据支持才能设 true。conditions_met 包含收货地可配送、要求的交期和其他采购条件。original_verified 为原厂/已核验授权渠道的全新原装，其他商家声明但不能核验填 false，并在 notes 记录声明。必须将需求和展示型号逐项核对；不能仅让脚本判断字符串。

数值字段未知填 null，不填“未知”或0：

- pack_units：每包装包含的需求单位数量，必须有换算依据。
- stock_packs：现货包装数量。
- moq_packs：起订包装数。
- multiple_packs：购买倍数（包装）。单个可买也须有依据才能填1。
- price_pack：适用阶梯的每包装价格。
- tier_min_packs、tier_max_packs：阶梯有效数量范围（包装），无上限填 null。
- currency：ISO 币种代码；tax：含税、未税或未知。
- fx_cny：一单位原币兑换人民币；外币换算还需 fx_source 和 fx_date。

其他信息：shipping、origin、lead_time、stock_status（网页显示/供应商确认/未知）、authorization_url、notes。授权核验依据在 evidence 中写明，并保留授权来源链接。

coverage 按需求 id 索引，每项含 mainland，必要时含 global。各阶段含 complete（布尔值）、queries（实际查询词数组）、scope（实际覆盖渠道/范围）、stop_reason（停止原因）、checked_at（时间）、obstacles（访问阻碍）。complete 表示本轮约定范围查询完成，不表示互联网穷尽；无法完成填 false，不生成正式完成报告。

最小结构示意（不是报价数据）：

```json
{"requests":[],"quotes":[],"coverage":{}}
```

evaluate(request, quote) 仅评估已采集事实是否满足条件，不执行网页搜索，也不能证明事实真假。processTask 会拒绝未完成必要阶段的报告。覆盖已完成但无报价时可以输出零结果报告。

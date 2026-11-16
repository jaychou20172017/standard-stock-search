# User interaction

[中文](../interaction.md)

Ask the product count only when no request exists and it is unknown. For one item provide a copyable form with product name, brand, complete model, quantity, unit, country/region and city; due date, additional specifications and other requirements are optional. State defaults: new/genuine, exact model, no alternatives and no combined sourcing. Echo complete key requirements briefly and search without an extra start confirmation.

For multiple items give the blank Excel template. Use `--batch`, report totals, keep all rows and continue complete items. Reject the entire file only for structural failure. Missing/duplicate/invalid IDs use temporary source-row identifiers; preserve valid unique IDs. Do not associate decisions with ambiguous identifiers before clarification.

Group missing information, model ambiguities, stock-combining and alternative decisions by ID. Up to five questions use chat; more use `questions` Excel with columns for issue ID, request ID, source row, question, options, blank user decision and status. Never prefill consent.

Replies apply only to explicitly addressed items and decision types. Keep the original response and effective value with issue/request scope. Silence, elapsed time and “continue” grant no permission. “All items” applies only to the expressly identified current-task decision. Validate returned decision IDs/source rows against the original list; clarify duplicates, unknown IDs or contradictions. Blank decisions stay pending.

Continue original-condition searches while combined sourcing/alternative decisions are pending; pause an item's search if identity is unclear. Reports retain all requests and distinguish completed, stock insufficient/quote needed, incomplete, pending decision and no result. Pending items must not be described as completed.

Use aggregated progress counts and avoid repeated interruptions. When further public searching adds no useful evidence, explain scope and bottlenecks. Offer further checks, inquiry drafts or reply verification without automatically contacting suppliers.

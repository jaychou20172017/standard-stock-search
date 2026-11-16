# Standard Stock Search Skill

[中文](README.md) | English

Search for new, genuine, in-stock standard products across categories. Start with mainland China and expand globally for each item when no mainland channel satisfies the complete requirements. Keep all relevant quotes and evidence, and export a three-sheet Excel report.

## Start here

- [User guide](docs/en/user-guide.md)
- [Requirements](docs/en/requirements.md)
- [Implementation and release status](docs/en/project-status.md)
- [Acceptance record](docs/en/acceptance.md)
- [English skill instructions](standard-stock-search/SKILL.en.md)
- [Chinese development history](development-status.md) (historical log; the English status document summarizes the current release)

The portable skill is in `standard-stock-search/`. Read its instructions and run `python3 scripts/check_runtime.py`. Copy the entire directory when installing; do not copy development dependencies or procurement data. See the user guide for commands and client limitations.

Chinese and English instructions use the same scripts and data contract. The current Excel template, report headings, CLI messages and JSON enum values remain Chinese. [Field translations](docs/en/user-guide.md#excel-fields) help English-speaking users; this release does not claim a fully English Excel/CLI interface.

## License

Copyright (c) 2026 Zhou Jie. Noncommercial use and internal business use are free under the [custom license](LICENSE). External commercial distribution, paid services and commercial product integration require prior written authorization. Contact [3504264104@qq.com](mailto:3504264104@qq.com); see [commercial licensing](standard-stock-search/COMMERCIAL-LICENSE.en.md).

The [English license translation](LICENSE.en.md) is provided for convenience; the Chinese LICENSE governs. This is source-available software under a restricted-use license, not an OSI open-source license.

## Publication and privacy

Publish source, documentation and the blank template only. Exclude `exports/`, outputs, credentials, dependencies and historical ZIP files. Build portable releases with `package_skill.py`; inspect staged files before uploading. A gitignore does not remove already tracked files.

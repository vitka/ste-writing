# STE Writing

An agent skill for writing, rewriting, and reviewing technical prose with selected ASD-STE100 rules and local style preferences. Includes strict and flavored modes and a Python linter.
This is an editing aid, not an STE compliance checker. Neither mode includes the full STE dictionary.

Predecessor: [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill). This project adapts its approach for technical prose and repository editing.

Install this folder as `ste-writing` in your project's skills directory:

| Harness | Directory |
| --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/` |
| [Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) | `.github/skills/` |
| [Cursor](https://cursor.com/help/customization/skills) | `.cursor/skills/` |

Ask: “Use ste-writing to review this document.” See [SKILL.md](SKILL.md) for modes and output formats.

To run the linter directly with Python 3.9 or later:

```sh
python3 scripts/ste-lint.py --strict /path/to/document.md
```

Score version 3 counts only mechanical findings. Context-dependent review and house-style findings do not affect the score or `--fail-over`.

Quotations are checked by default. Use `--exclude-quotes` for protected text inside paired quotation marks. This option does not exclude Markdown blockquotes.
Link destinations and code are excluded. Link labels and individual table cells are checked.

Scores are not comparable with earlier versions. There is no calibrated pass threshold, and a clean result does not establish STE compliance.
This skill is unofficial and is not affiliated with [ASD](https://asd-ste100.org).

Original code and documentation: [MIT](LICENSE). The ASD-STE100 standard is not covered by this license.

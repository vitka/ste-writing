# STE Writing

An agent skill for writing, rewriting, and reviewing technical prose with ASD-STE100 rules. Includes strict and flavored modes and a Python linter.

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

Lint scores are advisory. This skill is unofficial and is not affiliated with [ASD](https://asd-ste100.org).

Original code and documentation: [MIT](LICENSE). The ASD-STE100 standard is not covered by this license.

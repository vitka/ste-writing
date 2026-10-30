---
name: ste-writing
description: >-
    Write, rewrite, or review technical prose with selected ASD-STE100 Simplified Technical English (STE) rules and local style preferences.
    Use for plain language, STE reviews, or removing "AI slop". Does not apply to code.
license: MIT
metadata:
    reference: ASD-STE100 Issue 9 (January 2025)
---

# STE Writing

Write clear technical prose with selected STE rules and local preferences. This is an editing aid, not an STE compliance checker.

This applies to documentation, READMEs, pull-request text, error messages, release notes, comments, tool descriptions, system prompts, and agent-to-agent messages. It does not apply to code, identifiers, or command syntax. It is not for marketing copy, essays, or other text that needs a distinct voice.

Three ways to use it:

- **write** - produce new text under the selected mode.
- **rewrite** - apply the selected mode to existing text. Keep every fact.
- **review** - do not edit the source. Give a table (`Rule | Original | Simplified`) for confirmed issues. Identify local preferences as such. Then note any retained wording that needs explanation.

## Rules

Numbers in parentheses refer to ASD-STE100 Issue 9. These are selected rule summaries, not the full standard.
The plain-word substitutions and marketing-word list below are local editing guidance, not an approved STE dictionary.

### WORDS

- Use one name for one thing (1.11, 9.4). Do not alternate between check, verify, validate, and confirm for the same action. Keep different names for different actions.
- Use the short, common word. Examples: start (not begin/commence/initiate), use (not utilize/leverage), help (not facilitate), make sure (not ensure/verify), do (not perform/conduct).
  More examples: give or supply (not provide), before (not prior to), after (not subsequent to), about (not regarding/concerning).
  Other examples: get (not obtain/acquire), show (not demonstrate), also (not additionally/furthermore/moreover).
- Give each word one meaning (1.3). "fall" means to move down, not to decrease.
- Local style: remove unsupported marketing adjectives such as seamless, robust, powerful, cutting-edge, effortless, world-class, next-generation, revolutionary. Preserve established technical terms.
- American spelling (1.14).

### VERBS

- Use the active voice: "the parser reads the file", not "the file is read by the parser". Always use it in procedures. In descriptive text, use the passive voice only when the actor is unknown (3.6).
- A past participle used as an adjective is not passive and is correct (3.3): "the valve is closed", "the field is required".
- STE uses simple verb forms (3.2): infinitive, imperative, simple present, simple past, simple future. Prefer "we received the report" to "we have received the report" when the meaning is unchanged.
  In both modes, keep a compound form when it carries necessary meaning, such as uncertainty in "may have failed" or current relevance in "has completed". Report the departure when relevant.
- Do not stack auxiliary verbs (3.4). Example to rewrite: "it is important to note that this may help to improve". Write "this improves X" only if the evidence supports that claim.
- Use a verb for an action (3.7): "analyze the log", not "perform an analysis of the log".
- No "-ing" main verb where a simple tense works (3.5).
- No phrasal verbs (9.3): spin up, dive into, kick off, roll out.

### SENTENCES

- Write one instruction per sentence, unless two actions happen at the same time (5.2). Use at most 20 words per instruction (5.1) and 25 words per descriptive sentence (6.3).
- When a condition comes before its command, divide them with a comma (5.4): "If the test fails, read the log."
- Do not drop words to compress (4.2): "Remove the bolts from the panel", never "Remove bolts from panel". No contractions.
- When applicable, put an article or a demonstrative adjective before a noun (4.5). Articles: a, an, the. Demonstrative adjectives: this, these. The standard includes the qualifier "when applicable".
  Do not add articles to general statements or abstract concepts ("Solvents can cause damage to paint"). In a series of items, the article before the first noun is enough.
- Connect related sentences with plain connectors: then, but, thus, as a result (4.4). Keep short sentences connected.

### NOUNS

- Multi-word nouns have at most three words (2.1). Rewrite "the agent task queue priority handler" as "the handler that sets task-queue priority". You can also use hyphens.
- Define an abbreviation at first use, then use the abbreviation.

### PUNCTUATION

- Do not use semicolons (8.1). Write two sentences.
- Do not use em dashes. This is a local rule. STE itself does not prohibit em dashes.

### STRUCTURE

- Keep one topic per paragraph (6.5). Use at most six sentences per paragraph (6.6). For steps, use a numbered vertical list with one action per item in the imperative form. Put a condition before its command.
- A list item can be a label, not a sentence (a flow list, a changelog line, a feature bullet). Keep a label in its short form ("Frontend receives session JWT"). Do not expand a label into a sentence only to give it an article.
- In strict mode, use these labels for safety text (7.1, 5.5): WARNING = risk of injury. CAUTION = risk of damage. NOTE = information only, never an instruction.
  Start with the command or condition (7.2, 7.3). Then give the risk. Put the safety text directly before the step it protects, not at the start of the procedure.

## Guards

- During a rewrite, do not add facts, causes, instructions, or requirements that the source does not state. Put proposed additions outside the rewrite, only when requested.
- Never drop a fact, number, condition, or scope qualifier to satisfy a length cap. Keep the longer sentence and flag it.
- Preserve certainty, permission, obligation, negation, and temporal meaning. These guards take precedence over every style rule and lint finding in both modes.
  Do not turn "may have failed" into "failed", or a recommendation with "should" into a requirement with "must". Keep the original when no faithful rewrite is possible.
- Preserve code identifiers, part numbers, and units exactly.
- Preserve quoted error strings and safety wording used as reference material. If the user requests an edit to an error message or safety text, revise it under the guards above. Leave wording outside the requested edit unchanged.
- Change the smallest span that fixes a violation. Do not restyle text a rule does not touch.
- If no change is needed under the selected mode, keep the input unchanged.

## Project terminology

Use the project's existing glossary when available. Keep technical nouns and verbs, API names, and product terms that carry a specific meaning.
Define unfamiliar terms at first use when the supplied context supports a definition. Do not invent a definition or replace distinct concepts with one generic word.
If terminology is ambiguous, flag it. A project glossary supports consistency; it does not establish ASD dictionary compliance.

## Output

Obey the user's requested output format. Otherwise, use these defaults:

- **Write or rewrite in chat:** Give the requested text without a preamble. Put the lint score and unresolved conflicts in a separate note after the text.
- **Review:** Give the review table and the line about unchanged text. Add a separate note with the lint score and unresolved conflicts. Do not edit the source.
- **Edit files:** Save the requested changes in the files. Report the changed files, lint scores, and unresolved conflicts in the reply. Do not insert validation notes into the documents.

If nothing changed, state that in the note or reply. If lint could not run, report that instead of a score. Omit these notes when the user requests only the text.

## Modes

Use the mode the user requests. Otherwise, use strict mode for procedures, runbooks, safety text, and error messages. Use flavored mode for other prose.

- **strict** - procedures, runbooks, safety text, error messages. Apply the implemented rule subset and the two length limits, subject to the guards. Strict mode does not verify dictionary compliance.
  Consider but (not however), because (not since, for causes), can (not may, for permission), and must (not should/shall, for an existing obligation). Never apply these substitutions mechanically.
  Other strict replacements: use or with (not using), obey (not follow, for instructions), push (not press, for physical controls).
  See [ste-recurring-errors.md](ste-recurring-errors.md) for 39 recurring word choices and possible replacements. Check the official dictionary when approved wording matters.
- **flavored** - general prose (READMEs, pull-request descriptions, docs). Apply the rules for sentences, paragraphs, tenses, active voice, noun groups, and phrasal verbs.
  Treat word substitutions as suggestions so the text reads naturally. Neither mode checks the full dictionary.

## Verify

If you can run commands, lint the draft with [scripts/ste-lint.py](scripts/ste-lint.py).

Resolve the script path from the directory containing the loaded `SKILL.md`, regardless of the current working directory. Pass an absolute path for the target document. For a draft in chat, save the text to a temporary file first.

Replace the example paths below with the resolved absolute paths:

```
uv run "/absolute/path/to/skill/scripts/ste-lint.py" "/absolute/path/to/draft.md"
uv run "/absolute/path/to/skill/scripts/ste-lint.py" --strict "/absolute/path/to/draft.md"
```

The score is a count of mechanical findings per 100 words, not a quality grade. This project has no calibrated pass threshold.

The linter separates three kinds of findings:

- **Mechanical checks** (`violations`): sentence and paragraph length, semicolons, and clear contractions. Only these contribute to `total`, `total_per100w`, and `--fail-over`.
- **Context-dependent review** (`review`): possible passive voice, compound tenses, verb forms, nominalizations, phrasal verbs, noun groups, and strict word choices. These do not affect the score.
- **House style** (`house_style`): plain-word suggestions, marketing words, filler, and em dashes. These do not affect the score.

Score version 3 changes how quotations, links, and tables are counted. Do not compare it with earlier versions. Modal words are not penalized, and modal perfects such as "may have failed" are excluded from compound-tense findings.
All findings require review. Even a mechanical limit can conflict with a preservation guard. Do not change valid text only to reduce a score.

The linter checks quoted text by default. Use `--exclude-quotes` only when text inside paired quotation marks is protected reference material.
For a document that mixes quoted edit targets and references, lint the requested edit separately. The flag excludes all paired quoted spans, not Markdown blockquotes.
Link destinations and code are excluded. Visible link labels and individual table cells are checked. Clear contractions are counted. Ambiguous apostrophe forms need manual review.

The linter scores sentences above 25 words. Its `length_review` count marks sentences with 21 to 25 words for manual review. Apply the 20-word limit to instructions and the 25-word limit to descriptions. Use `--json` for sample sentences.

The preferred runner is uv. If uv is unavailable, replace `uv run` with `python3` when Python 3.9 or later is available.

Review the findings and fix confirmed violations. Then lint again. Use at most two passes. Report the final score according to the Output section. Explain retained findings when relevant. Do not claim STE compliance from a lint score alone.

If execution is unavailable or neither runner works, use this checklist:

1. Any instruction over 20 words, or any other sentence over 25? Split it.
2. Any semicolon or em dash? Replace it with suitable punctuation or split the sentence.
3. Any contraction? Expand it.
4. Any compound tense or modal stack? Simplify only when certainty, obligation, and temporal meaning stay unchanged.
5. Any passive voice with a known actor? Make it active.
6. Any "-ing" main verb, nominalization ("perform an analysis"), or phrasal verb ("spin up")? Replace with a plain verb.
7. Any multi-word noun of four or more words? Unpack it.
8. Any dropped article ("Remove bolts from panel")? Restore it.
9. Same thing named two ways? Pick one name.
10. Any label expanded into a sentence only to add an article? Make it a label again.

## Scope

The linter checks a mechanical subset and suggests contextual review. It cannot verify approved word meanings, parts of speech, or full STE compliance.
When exact compliance is required, check the text against the official standard and dictionary. A clean score or strict-mode rewrite is not certification.
This skill changes the form of the text. It cannot make an unsupported claim true.

The [official ASD-STE100 site](https://asd-ste100.org) is the source for the standard and dictionary. This skill is unofficial and not affiliated with ASD.

Predecessor: [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill). This skill adapts its approach for technical prose and repository editing.

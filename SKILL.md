---
name: ste-writing
description: >-
    Write, rewrite, or review technical prose with ASD-STE100 Simplified Technical English (STE) rules.
    Use for plain language, STE reviews, or removing "AI slop". Does not apply to code.
license: MIT
metadata:
    spec: ASD-STE100 Issue 9 (January 2025)
---

# STE Writing

Write prose in ASD-STE100 Simplified Technical English (STE). Issue 9 has 53 rules in 9 sections and 875 approved words.

This applies to documentation, READMEs, pull-request text, error messages, release notes, comments, tool descriptions, system prompts, and agent-to-agent messages. It does not apply to code, identifiers, or command syntax. It is not for marketing copy, essays, or other text that needs a distinct voice.

Three ways to use it:

- **write** - produce new text in STE.
- **rewrite** - convert existing text to STE. Keep every fact.
- **review** - do not rewrite. Give a table (`Rule | Original | Simplified`) with one row per violation. Then add one line about text you did not change and why.

## Rules

Numbers in parentheses are rule numbers in ASD-STE100 Issue 9.

### WORDS

- Use one name for one thing (1.11, 9.4). Do not alternate between check, verify, validate, and confirm for the same action. Choose one word. Certified STE uses "make sure" or "examine".
- Use the short, common word. Examples: start (not begin/commence/initiate), use (not utilize/leverage), help (not facilitate), make sure (not ensure/verify), do (not perform/conduct).
  More examples: give or supply (not provide), before (not prior to), after (not subsequent to), about (not regarding/concerning).
  Other examples: get (not obtain/acquire), show (not demonstrate), also (not additionally/furthermore/moreover).
- Give each word one meaning (1.3). "fall" means to move down, not to decrease.
- No marketing adjectives: seamless, robust, powerful, cutting-edge, effortless, world-class, next-generation, revolutionary.
- American spelling (1.14).

### VERBS

- Use the active voice: "the parser reads the file", not "the file is read by the parser". Always use it in procedures. In descriptive text, use the passive voice only when the actor is unknown (3.6).
- A past participle used as an adjective is not passive and is correct (3.3): "the valve is closed", "the field is required".
- Only simple tenses (3.2): infinitive, imperative, simple present, simple past, simple future. No present perfect: "we received the report", never "we have received the report".
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

- Never drop a fact, number, condition, or scope qualifier to satisfy a length cap. Keep the longer sentence and flag it.
- Preserve certainty, permission, obligation, and negation. If a substitution changes meaning, rewrite the sentence or flag the conflict. This guard takes precedence over word replacements in every mode.
- Preserve code identifiers, part numbers, and units exactly.
- Preserve quoted error strings and safety wording used as reference material. If the user requests an edit to an error message or safety text, revise it under the guards above. Leave wording outside the requested edit unchanged.
- Change the smallest span that fixes a violation. Do not restyle text a rule does not touch.
- If the input already complies, keep it unchanged.

## Output

Obey the user's requested output format. Otherwise, use these defaults:

- **Write or rewrite in chat:** Give the requested text without a preamble. Put the lint score and unresolved conflicts in a separate note after the text.
- **Review:** Give the review table and the line about unchanged text. Add a separate note with the lint score and unresolved conflicts. Do not edit the source.
- **Edit files:** Save the requested changes in the files. Report the changed files, lint scores, and unresolved conflicts in the reply. Do not insert validation notes into the documents.

If nothing changed, state that in the note or reply. If lint could not run, report that instead of a score. Omit these notes when the user requests only the text.

## Modes

Use the mode the user requests. Otherwise, use strict mode for procedures, runbooks, safety text, and error messages. Use flavored mode for other prose.

- **strict** - procedures, runbooks, safety text, error messages. Apply every rule and the two length limits. Use the strict word set: but (not however), because (not since, for causes), can (not may), must (not should/shall).
  Other strict replacements: use or with (not using), obey (not follow, for instructions), push (not press, for physical controls).
  The standard lists the 39 most frequent writer errors in [ste-recurring-errors.md](ste-recurring-errors.md).
- **flavored** - general prose (READMEs, pull-request descriptions, docs). Apply the rules for sentences, paragraphs, tenses, active voice, noun groups, and phrasal verbs.
  Permit exceptions to the 875-word dictionary and the strict word set so the text reads naturally.

## Verify

If you can run commands, lint the draft with [scripts/ste-lint.py](scripts/ste-lint.py).

Resolve the script path from the directory containing the loaded `SKILL.md`, regardless of the current working directory. Pass an absolute path for the target document. For a draft in chat, save the text to a temporary file first.

Replace the example paths below with the resolved absolute paths:

```
uv run "/absolute/path/to/skill/scripts/ste-lint.py" "/absolute/path/to/draft.md"
uv run "/absolute/path/to/skill/scripts/ste-lint.py" --strict "/absolute/path/to/draft.md"
```

The flavored target is below 2.5 per 100 words. The strict target is below 1.5 per 100 words.

Treat lint findings as candidates for review. The scores are advisory, not proof of STE compliance. Do not change valid text only to reduce a score.

The linter excludes quoted text from language checks. Review quotations manually when they are part of the requested edit. It counts clear contractions but leaves ambiguous apostrophe forms for manual review.

The linter scores sentences above 25 words. Its `length_review` count marks sentences with 21 to 25 words for manual review. Apply the 20-word limit to instructions and the 25-word limit to descriptions. Use `--json` for sample sentences.

The preferred runner is uv. If uv is unavailable, replace `uv run` with `python3` when Python 3.9 or later is available.

Review the findings and fix confirmed violations. Then lint again. Use at most two passes. Report the final score according to the Output section. Explain retained findings when relevant. Do not claim STE compliance from a lint score alone.

If execution is unavailable or neither runner works, use this checklist:

1. Any instruction over 20 words, or any other sentence over 25? Split it.
2. Any semicolon or em dash? Replace it with suitable punctuation or split the sentence.
3. Any contraction? Expand it.
4. Any present perfect ("has/have received") or modal stack? Use a simple tense.
5. Any passive voice with a known actor? Make it active.
6. Any "-ing" main verb, nominalization ("perform an analysis"), or phrasal verb ("spin up")? Replace with a plain verb.
7. Any multi-word noun of four or more words? Unpack it.
8. Any dropped article ("Remove bolts from panel")? Restore it.
9. Same thing named two ways? Pick one name.
10. Any label expanded into a sentence only to add an article? Make it a label again.

## Scope

The linter can check the mechanical rules above. Full STE also needs human judgment about the correct technical noun and whether a sentence makes sense. This skill changes the form of the text. It cannot make an unsupported claim true.

The full standard is free at https://asd-ste100.org. This skill is unofficial and not affiliated with ASD. ASD-STE100 is a registered EU trademark (No. 017966390).

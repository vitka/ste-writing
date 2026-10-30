# 39 recurring word choices

This reference collects word choices and possible replacements based on the recurring-errors list in ASD-STE100 Issue 9.
It is not a complete dictionary or a list of automatic substitutions. Check the official standard for approved meanings, parts of speech, and conditions of use.
The [official ASD-STE100 site](https://asd-ste100.org) is the source for the standard.

Uppercase marks replacement candidates in this table. It does not certify their use in a particular sentence.
Some replacements change the part of speech. For example, check as a verb becomes CHECK as a noun: "do a check".
For these replacements, change the sentence structure.

| # | Word to review | Replacement to consider |
|---|---|---|
| 1 | acceptable (adj) | PERMITTED |
| 2 | alternate (adj) | ALTERNATIVE |
| 3 | any (adj) | none, or a different sentence construction |
| 4 | avoid (v) | PREVENT |
| 5 | both (adj) | THE TWO |
| 6 | check (v) | CHECK (n): "do a check" |
| 7 | cover (v) | COVER (n) |
| 8 | complete (adj) | COMPLETED |
| 9 | damage (v) | DAMAGE (n) |
| 10 | ensure (v) | MAKE SURE |
| 11 | fit (v) | INSTALL |
| 12 | follow (v) | OBEY |
| 13 | further (adj) | MORE |
| 14 | further (adv) | MORE |
| 15 | have to (v) | an action verb in the imperative form |
| 16 | however (adv) | BUT |
| 17 | insert (v) | PUT |
| 18 | main (adj) | PRIMARY |
| 19 | may (v) | CAN |
| 20 | need (v) | NECESSARY (adj) |
| 21 | now (adv) | AT THIS TIME |
| 22 | old (adj) | REMAINING, USED, EXPIRED |
| 23 | over (prep) | ABOVE, ON, ALONG |
| 24 | people (n) | PERSON, PERSONNEL |
| 25 | perform (v) | DO |
| 26 | portion (n) | PART |
| 27 | press (v) | PUSH |
| 28 | reach (v) | GET |
| 29 | repeat (v) | DO … AGAIN |
| 30 | required (v) | NECESSARY (adj) |
| 31 | rotate (v) | TURN |
| 32 | secure (v) | ATTACH, SAFETY |
| 33 | shall (v) | MUST |
| 34 | should (v) | MUST |
| 35 | since (conj) | BECAUSE |
| 36 | test (v) | TEST (n) |
| 37 | therefore (adv) | THUS, AS A RESULT |
| 38 | under (prep) | BELOW, IN, LESS THAN |
| 39 | using (v) | USE, WITH |

## Replacements for software docs

Many entries concern aerospace procedures. The examples below show how to apply them to engineering prose.
In strict mode, apply the replacements when they preserve meaning.
In flavored mode, follow the rules in [SKILL.md](SKILL.md). These examples add no requirements to that mode.

- **ensure → make sure**: Use this replacement in READMEs.
- **however → but** and **therefore → thus / as a result**: These shorter connectors keep the same logic.
- **since → because**: Use this replacement only for a cause. Keep temporal meaning when "since" refers to time.
  For example, "since the server restarted" can have either meaning.
- **may → can** and **should / shall → must**: Their meaning depends on context, including uncertainty, permission, recommendations, and obligations.
  Use "can" for permission and "must" for an obligation only when these words preserve the original meaning.
  Preserve recommendations and uncertainty. If a replacement changes meaning, rewrite the sentence or flag the conflict.
- **perform → do**: "perform an analysis" uses a noun for an action. Write "analyze".
- **using → use / with**: CLI means command-line interface.
  Rewrite "Using the CLI, run…" as "Run … with the CLI."
- **check / test as verbs**: STE uses them as nouns ("do a check", "do a test") to keep action verbs unambiguous.
  In flavored software prose, you can keep "check" as a verb. Use one word for the action.

The `--strict` flag of [scripts/ste-lint.py](scripts/ste-lint.py) requests contextual review of however, since, using, and forms of follow.
These findings do not affect the score. The linter does not flag may, should, or shall as word-choice errors: their meaning needs human review.
This list is a reference for selected substitutions, not a complete dictionary check. The preservation guards in [SKILL.md](SKILL.md) apply to every entry.

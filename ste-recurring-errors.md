# The 39 recurring errors

ASD-STE100 Issue 9 ends its dictionary introduction with a list of frequent writer errors.
The list gives an approved replacement for each word. This file contains that list as data.
It is a short factual excerpt. The full standard is free at https://asd-ste100.org.

The dictionary prints approved replacements in UPPERCASE. This file uses the same format.
Some replacements change the part of speech. For example, check as a verb becomes CHECK as a noun: "do a check".
For these replacements, change the sentence structure.

| # | Do not write | Write |
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
- **since → because**: STE prohibits "since" because it can mean time or cause.
  For example, "since the server restarted" can have either meaning.
- **may → can** and **should / shall → must**: These words express permission and obligation.
  Use "can" for permission and "must" for an obligation only when these words preserve the original meaning.
  Preserve recommendations and uncertainty. If a replacement changes meaning, rewrite the sentence or flag the conflict.
- **perform → do**: "perform an analysis" uses a noun for an action. Write "analyze".
- **using → use / with**: CLI means command-line interface.
  Rewrite "Using the CLI, run…" as "Run … with the CLI."
- **check / test as verbs**: STE uses them as nouns ("do a check", "do a test") to keep action verbs unambiguous.
  In flavored software prose, you can keep "check" as a verb. Use one word for the action.

The `--strict` flag of [scripts/ste-lint.py](scripts/ste-lint.py) enforces the strict subset: however, since, may, should, shall, using, follow.
Flavored mode permits these words.

# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///

import glob
import io
import json
import os
import re
import sys
from typing import TypedDict

# Increment when scoring rules or output change.
SCORE_VERSION = 1

LintResult = TypedDict(
    "LintResult",
    {
        "score_version": int,
        "mode": str,
        "words": int,
        "sentences": int,
        "violations": dict[str, int],
        "total": int,
        "total_per100w": float,
        "em_dash(slop-marker)": int,
        "noun_train(>=4w,marker)": int,
        "sentence_21_to25w(marker)": int,
        "sample_sentence_length_review": list[str],
        "longest_sentence_words": int,
        "sample_marketing": list[str],
        "sample_banned": list[str],
        "sample_noun_train": list[str],
    },
)

MARKETING: list[str] = [
    "seamless",
    "seamlessly",
    "robust",
    "powerful",
    "cutting-edge",
    "effortless",
    "effortlessly",
    "world-class",
    "next-generation",
    "revolutionary",
    "blazing",
    "lightning-fast",
    "elegant",
    "delightful",
    "turnkey",
    "best-in-class",
    "state-of-the-art",
    "game-changing",
    "first-class",
    "battle-tested",
    "enterprise-grade",
    "supercharge",
    "unlock",
    "unleash",
    "empower",
    "empowers",
]
BANNED: list[str] = [
    "begin",
    "begins",
    "commence",
    "commences",
    "initiate",
    "initiates",
    "originate",
    "utilize",
    "utilizes",
    "utilizing",
    "leverage",
    "leverages",
    "leveraging",
    "facilitate",
    "facilitates",
    "ensure",
    "ensures",
    "ensuring",
    "prior to",
    "subsequent to",
    "obtain",
    "obtains",
    "acquire",
    "acquires",
    "demonstrate",
    "demonstrates",
    "additionally",
    "furthermore",
    "moreover",
    "comprehensive",
    "comprehensively",
    "utilization",
    "aforementioned",
    "henceforth",
    "therein",
    "whilst",
    "amongst",
    "numerous",
    "myriad",
    "plethora",
    "provide",
    "provides",
    "provided",
    "in order to",
    "a variety of",
    "in the event that",
    "due to the fact that",
    "it is important to note",
]
# Strict mode checks terms that can appear in ordinary documentation.
STRICT_BANNED: list[str] = [
    "however",
    "since",
    "should",
    "shall",
    "using",
    "follow",
    "follows",
    "followed",
]
PHRASAL: list[str] = [
    "spin up",
    "spin down",
    "reach out",
    "dive into",
    "dives into",
    "diving into",
    "kick off",
    "kicks off",
    "roll out",
    "rolls out",
    "tear down",
    "ramp up",
    "circle back",
    "drill down",
    "spun up",
    "reaching out",
]
MODAL_HEDGE: list[str] = [
    "it is important to note",
    "it should be noted",
    "it is worth noting",
    "please note that",
    "as mentioned",
    "as noted above",
]
BE = r"(?:am|is|are|was|were|be|been|being)"
PP_IRREG = r"(?:done|made|sent|read|built|kept|held|set|put|run|written|shown|given|taken|found|got|gotten|seen|known|thrown|drawn)"
# Rule 3.3: Adjectival participles count as passive only with a by-agent.
STATIVE = r"(?:closed|opened?|damaged|completed?|installed|connected|required|expected|configured|enabled|disabled|deprecated|supported)"
FUNC_WORDS: set[str] = {
    "a",
    "an",
    "the",
    "this",
    "that",
    "these",
    "those",
    "of",
    "for",
    "to",
    "in",
    "on",
    "at",
    "by",
    "with",
    "from",
    "as",
    "and",
    "or",
    "but",
    "if",
    "when",
    "then",
    "than",
    "not",
    "no",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "am",
    "do",
    "does",
    "did",
    "has",
    "have",
    "had",
    "will",
    "would",
    "can",
    "could",
    "may",
    "might",
    "must",
    "should",
    "shall",
    "it",
    "its",
    "their",
    "your",
    "our",
    "his",
    "her",
    "they",
    "we",
    "you",
    "i",
}


def strip_code(t: str) -> str:
    lines = []
    fence = None
    list_indents = []
    indented_code = False
    previous_blank = True
    for line in t.expandtabs(4).splitlines():
        if fence is not None:
            if re.fullmatch(
                r"[ ]*" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}[ \t]*", line
            ):
                fence = None
            lines.append("")
            previous_blank = True
            continue

        indent = len(line) - len(line.lstrip(" "))
        if line.strip():
            while list_indents and indent < list_indents[-1]:
                list_indents.pop()
        base = list_indents[-1] if list_indents else 0
        item = (
            re.match(r"[ ]*(?:[-*+]|\d+[.)])[ ]+", line) if indent - base < 4 else None
        )
        if item:
            list_indents.append(item.end())
            content = line[item.end() :]
            indented_code = False
        else:
            content = line[base:]

        # Four spaces relative to the list item (or document) start code only
        # after a block boundary. Indented continuations remain prose.
        if (
            not item
            and content.startswith("    ")
            and (previous_blank or indented_code)
        ):
            lines.append("")
            indented_code = True
            previous_blank = False
            continue
        if line.strip():
            indented_code = False
        opening = re.match(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$", content)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            lines.append("")
            previous_blank = True
            continue
        lines.append(line)
        previous_blank = not line.strip()

    # Match code spans with equal-length backtick delimiters.
    return re.sub(
        r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", " ", "\n".join(lines), flags=re.DOTALL
    )


def strip_quotes(text: str) -> str:
    """Exclude quoted text without treating apostrophes in words as quotes."""
    return re.sub(
        r'"[^"\n]*"|“[^”\n]*”|(?<!\w)\'[^\'\n]*\'(?!\w)|(?<!\w)‘[^’\n]*’(?!\w)',
        " ",
        text,
    )


def prose_blocks(text: str) -> list[str]:
    """Join soft wraps without joining headings, list items, or table rows."""
    blocks = []
    current = []
    for line in text.splitlines():
        s = line.strip()
        heading = re.match(r"^#{1,6}\s+", s)
        item = re.match(r"^(?:[-*+]|\d+[.)])\s+", s)
        table = s.startswith("|")
        separator = re.fullmatch(
            r"(?:[-*_][ \t]*){3,}|=+|\|?[ :\-]+(?:\|[ :\-]+)+\|?", s
        )
        if (not s or heading or item or table or separator) and current:
            blocks.append(" ".join(current))
            current = []
        if not s or separator:
            continue
        prefix = heading or item
        if prefix is not None:
            s = s[prefix.end() :]
        if heading or table:
            blocks.append(s)
        else:
            current.append(s)
    if current:
        blocks.append(" ".join(current))
    return blocks


def sentences(text: str) -> list[str]:
    out = []
    for s in prose_blocks(text):
        parts = re.split(r"(?<=[.!?:])\s+(?=[A-Z0-9\"'\-])", s)
        for p in parts:
            p = p.strip()
            if p:
                out.append(p)
    return out


def wc(s: str) -> int:
    return len([w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/]*", s)])


def count_ci(text: str, phrases: list[str]) -> tuple[int, list[str]]:
    n = 0
    hits = []
    low = text.lower()
    for ph in phrases:
        for m in re.finditer(r"(?<![a-z])" + re.escape(ph) + r"(?![a-z])", low):
            n += 1
            hits.append(ph)
    return n, hits


def noun_trains(text: str) -> list[str]:
    """Find runs of four or more consecutive lowercase content words."""
    hits = []
    for s in sentences(text):
        words = re.findall(r"[A-Za-z][A-Za-z'\-]*", s)[1:]
        run = []
        for w in words + [""]:
            if w and w.lower() not in FUNC_WORDS and not w[0].isupper():
                run.append(w)
            else:
                if len(run) >= 4:
                    hits.append(" ".join(run))
                run = []
    return hits


def lint(text: str, strict: bool = False) -> LintResult:
    text = strip_quotes("\n\n".join(prose_blocks(strip_code(text))))
    sents = sentences(text)
    words = sum(wc(s) for s in sents) or 1
    v = {}
    # Instructions have a 20-word limit; descriptions have a 25-word limit.
    # Sentence type needs human review, so do not score the ambiguous range.
    longs = [(wc(s), s) for s in sents if wc(s) > 25]
    length_review = [s for s in sents if 20 < wc(s) <= 25]
    v["long_sentence(>25w)"] = len(longs)
    v["semicolon"] = text.count(";")
    # A generic 's match also catches possessives. Only count clear contractions.
    # Ambiguous forms such as "the server's running" need human review.
    v["contraction"] = len(
        re.findall(
            r"\b(?:\w+['’](?:t|re|ve|ll|d|m)|"
            r"(?:he|she|it|that|there|here|what|who|where|when|why|how|let)['’]s)\b",
            text,
            re.IGNORECASE,
        )
    )
    passive_parts = re.findall(rf"\b{BE}\s+(\w+ed|{PP_IRREG})\b", text, re.IGNORECASE)
    v["passive_voice"] = sum(
        1 for p in passive_parts if not re.fullmatch(STATIVE, p, re.IGNORECASE)
    ) + len(re.findall(rf"\b{BE}\s+{STATIVE}\s+by\b", text, re.IGNORECASE))
    v["complex_tense"] = len(
        re.findall(
            rf"\b(?:(?:may|might|could|would|should|must|will|shall|can)\s+)?(?:have|has|had)\s+(?:been\s+)?(?:\w+ed|{PP_IRREG})\b",
            text,
            re.IGNORECASE,
        )
    )
    v["ing_main_verb"] = len(re.findall(rf"\b{BE}\s+\w+ing\b", text, re.IGNORECASE))
    v["nominalization"] = len(
        re.findall(
            r"\b(?:perform(?:s|ed)?|conduct(?:s|ed)?|carry out|carries out|make use of|makes use of)\b",
            text,
            re.IGNORECASE,
        )
    ) + len(re.findall(r"\b\w{4,}(?:tion|ment|ance|ence)\s+of\b", text, re.IGNORECASE))
    v["phrasal_verb"], _ = count_ci(text, PHRASAL)
    v["banned_word"], bh = count_ci(text, BANNED)
    v["marketing_adjective"], mh = count_ci(text, MARKETING)
    v["modal_hedge"], _ = count_ci(text, MODAL_HEDGE)
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    v["long_paragraph(>6s)"] = sum(1 for p in paras if len(sentences(p)) > 6)
    em = text.count("—")
    trains = noun_trains(text)
    if strict:
        n_strict, _ = count_ci(text, STRICT_BANNED)
        # Match lowercase "may"; preserve the month name "May".
        n_strict += len(re.findall(r"(?<![A-Za-z])may(?![a-z])", text))
        v["strict_banned_word"] = n_strict
        v["em_dash"] = em
    total = sum(v.values())
    return {
        "score_version": SCORE_VERSION,
        "mode": "strict" if strict else "flavored",
        "words": words,
        "sentences": len(sents),
        "violations": v,
        "total": total,
        "total_per100w": round(total * 100.0 / words, 2),
        "em_dash(slop-marker)": em,
        "noun_train(>=4w,marker)": len(trains),
        "sentence_21_to25w(marker)": len(length_review),
        "sample_sentence_length_review": length_review[:3],
        "longest_sentence_words": (
            max(longs)[0] if longs else max((wc(s) for s in sents), default=0)
        ),
        "sample_marketing": list(dict.fromkeys(mh))[:6],
        "sample_banned": list(dict.fromkeys(bh))[:6],
        "sample_noun_train": trains[:3],
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    strict = "--strict" in args
    as_json = "--json" in args
    fail_over = None
    if "--fail-over" in args:
        i = args.index("--fail-over")
        fail_over = float(args[i + 1])
        del args[i : i + 2]
    files = [a for a in args if a not in ("--strict", "--json")]
    worst = 0.0
    if not files:
        if isinstance(sys.stdin, io.TextIOWrapper):
            sys.stdin.reconfigure(encoding="utf-8")
        r = lint(sys.stdin.read(), strict=strict)
        print(json.dumps(r, indent=2))
        worst = r["total_per100w"]
    else:
        exp = []
        for f in files:
            matches = sorted(glob.glob(f)) if glob.has_magic(f) else [f]
            if not matches:
                print(f"No files match pattern: {f}", file=sys.stderr)
                sys.exit(2)
            exp += matches
        for f in exp:
            with open(f, encoding="utf-8") as fh:
                r = lint(fh.read(), strict=strict)
            worst = max(worst, r["total_per100w"])
            if as_json:
                print(json.dumps({"file": f, **r}, indent=2))
            else:
                print(
                    f"{os.path.basename(f):32} words={r['words']:4d} total={r['total']:3d} per100w={r['total_per100w']:6.2f} em_dash={r['em_dash(slop-marker)']:2d} length_review={r['sentence_21_to25w(marker)']:2d}"
                )
    if fail_over is not None and worst > fail_over:
        sys.exit(1)

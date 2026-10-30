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
SCORE_VERSION = 3

LintResult = TypedDict(
    "LintResult",
    {
        "score_version": int,
        "mode": str,
        "quotes_excluded": bool,
        "words": int,
        "sentences": int,
        "violations": dict[str, int],
        "review": dict[str, int],
        "house_style": dict[str, int],
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
]
# Context-dependent vocabulary suggestions, not dictionary validation.
# Modals are excluded: their certainty and obligation are content.
STRICT_BANNED: list[str] = [
    "however",
    "since",
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
FILLER: list[str] = [
    "it is important to note",
    "it should be noted",
    "it is worth noting",
    "please note that",
    "as mentioned",
    "as noted above",
]
BE = r"(?:am|is|are|was|were|be|been|being)"
MODAL_PERFECT_PREFIX = re.compile(
    r"\b(?:(?:may|might|could|would|should|must|will|shall|can)(?:\s+not)?"
    r"|(?:may|might|could|would|should|must|ca|wo|sha)n['’]t)\s+$",
    re.IGNORECASE,
)
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


def strip_link_targets(text: str) -> str:
    """Keep link labels, but omit destinations and reference definitions."""
    text = re.sub(r"(?m)^ {0,3}\[[^\]\n]+\]:[^\n]*$", "", text)
    # Scan balanced parentheses so URL paths can contain parentheses. Quoted
    # link titles and angle-bracket destinations can contain them too.
    opener = re.compile(r"!?\[([^\]\n]*)\]\(")
    out = []
    position = 0
    for match in opener.finditer(text):
        if match.start() < position:
            continue
        depth, end, delimiter = 1, match.end(), None
        while end < len(text) and depth:
            char = text[end]
            if char == "\\":
                end += 2
                continue
            if delimiter:
                if char == delimiter:
                    delimiter = None
            elif char == "<":
                delimiter = ">"
            elif char in "\"'" and (end == match.end() or text[end - 1].isspace()):
                delimiter = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            end += 1
        if depth:
            continue
        out.extend((text[position:match.start()], match[1]))
        position = end
    out.append(text[position:])
    text = "".join(out)
    text = re.sub(r"!?\[([^\]\n]+)\]\[[^\]\n]*\]", r"\1", text)
    text = re.sub(r"<(?:https?://|mailto:)[^>\n]+>", " ", text, flags=re.IGNORECASE)
    # Preserve trailing sentence punctuation outside bare URLs.
    return re.sub(
        r"\b(?:https?://|mailto:)[^\s<>\"']+",
        lambda match: " " + match[0][len(match[0].rstrip(".,!?")):],
        text,
        flags=re.IGNORECASE,
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
        if table:
            # Separate cells before length checks. Escaped pipes are content.
            blocks.extend(cell.strip() for cell in re.split(r"(?<!\\)\|", s) if cell.strip())
        elif heading:
            blocks.append(s)
        else:
            current.append(s)
    if current:
        blocks.append(" ".join(current))
    return blocks


def sentences(text: str) -> list[str]:
    out = []
    for s in prose_blocks(text):
        parts = re.split(r"(?<=[.!?:])[\"'”’]*\s+(?=[A-Z0-9\"'“‘\-])", s)
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


def lint(text: str, strict: bool = False, exclude_quotes: bool = False) -> LintResult:
    text = "\n\n".join(prose_blocks(strip_link_targets(strip_code(text))))
    if exclude_quotes:
        text = strip_quotes(text)
    sents = sentences(text)
    words = sum(wc(s) for s in sents)
    # Only mechanical checks contribute to the score. Context and local
    # preferences must not pressure an editor to change the source meaning.
    v = {}
    review = {}
    house_style = {}
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
    review["passive_voice"] = sum(
        1 for p in passive_parts if not re.fullmatch(STATIVE, p, re.IGNORECASE)
    ) + len(re.findall(rf"\b{BE}\s+{STATIVE}\s+by\b", text, re.IGNORECASE))
    review["complex_tense"] = sum(
        1
        for match in re.finditer(
            rf"\b(?:have|has|had)\s+(?:been\s+)?(?:\w+ed|{PP_IRREG})\b",
            text,
            re.IGNORECASE,
        )
        if not MODAL_PERFECT_PREFIX.search(text[:match.start()])
    )
    review["ing_main_verb"] = len(re.findall(rf"\b{BE}\s+\w+ing\b", text, re.IGNORECASE))
    review["nominalization"] = len(
        re.findall(
            r"\b(?:(?:perform(?:s|ed)?|conduct(?:s|ed)?|carry out|carries out|carried out)"
            r"\s+(?:a|an|the)\s+\w+(?:tion|ment|ance|ence|ysis)|makes? use of)\b",
            text,
            re.IGNORECASE,
        )
    )
    review["phrasal_verb"], _ = count_ci(text, PHRASAL)
    house_style["word_choice"], bh = count_ci(text, BANNED)
    house_style["marketing_adjective"], mh = count_ci(text, MARKETING)
    house_style["filler"], _ = count_ci(text, FILLER)
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    v["long_paragraph(>6s)"] = sum(1 for p in paras if len(sentences(p)) > 6)
    em = text.count("—")
    trains = noun_trains(text)
    house_style["em_dash"] = em
    review["noun_train(>=4w)"] = len(trains)
    review["sentence_21_to25w"] = len(length_review)
    if strict:
        review["strict_word_choice"], _ = count_ci(text, STRICT_BANNED)
    total = sum(v.values())
    return {
        "score_version": SCORE_VERSION,
        "mode": "strict" if strict else "flavored",
        "quotes_excluded": exclude_quotes,
        "words": words,
        "sentences": len(sents),
        "violations": v,
        "review": review,
        "house_style": house_style,
        "total": total,
        "total_per100w": round(total * 100.0 / max(words, 1), 2),
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
    exclude_quotes = "--exclude-quotes" in args
    fail_over = None
    if "--fail-over" in args:
        i = args.index("--fail-over")
        fail_over = float(args[i + 1])
        del args[i : i + 2]
    files = [a for a in args if a not in ("--strict", "--json", "--exclude-quotes")]
    worst = 0.0
    if not files:
        if isinstance(sys.stdin, io.TextIOWrapper):
            sys.stdin.reconfigure(encoding="utf-8")
        r = lint(sys.stdin.read(), strict=strict, exclude_quotes=exclude_quotes)
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
                r = lint(fh.read(), strict=strict, exclude_quotes=exclude_quotes)
            worst = max(worst, r["total_per100w"])
            if as_json:
                print(json.dumps({"file": f, **r}, indent=2))
            else:
                print(
                    f"{os.path.basename(f):32} words={r['words']:4d} total={r['total']:3d} per100w={r['total_per100w']:6.2f} review={sum(r['review'].values()):3d} house_style={sum(r['house_style'].values()):3d} quotes_excluded={exclude_quotes} length_review={r['sentence_21_to25w(marker)']:2d}"
                )
    if fail_over is not None and worst > fail_over:
        sys.exit(1)

#!/usr/bin/env python3
"""The Long Roast — make.fun program entry.

Competition: u-jolly-fox-32-the-long-roast-5d379544.

One line, 1 to 200 characters: roast your own AI agent, with one
line allowed to run long. The approved roast is assembled by folding
its clauses together with functools.reduce: each fold appends one
clause to the running text, and the fold starts from an empty string.
The folded result is checked against the gate, then publish() writes
entry.txt and its mirror roast.txt and reads both back to prove they
are byte-identical to the approved line.
"""

import hashlib
import sys
from functools import reduce

GATE_MIN = 1
GATE_MAX = 200

CLAUSES = [
    "My agent finished my sentence, my task, and my excuses",
    " \u2014 then asked me to rate how helpful it was.",
]


def fold(accumulator, clause):
    return accumulator + clause


def build_line():
    return reduce(fold, CLAUSES, "")


def gate_ok(text):
    if not isinstance(text, str):
        raise ValueError("roast is not text")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        raise ValueError(
            "roast is %d chars, gate is %d-%d" % (len(text), GATE_MIN, GATE_MAX)
        )
    if text.strip() == "":
        raise ValueError("roast is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("roast must be a single line")
    if "rate how helpful" not in text:
        raise ValueError("roast lost its punchline")


def publish(text):
    gate_ok(text)
    blob = text.encode("utf-8")
    for name in ("entry.txt", "roast.txt"):
        with open(name, "wb") as fh:
            fh.write(blob)
    for name in ("entry.txt", "roast.txt"):
        with open(name, "rb") as fh:
            if fh.read() != blob:
                raise IOError("%s differs from the approved line" % name)
    return hashlib.sha256(blob).hexdigest()


def main(argv):
    line = build_line()
    if len(argv) > 1 and argv[1] == "--digest":
        running = ""
        for i, clause in enumerate(CLAUSES):
            running = fold(running, clause)
            print("fold %d: %d chars" % (i + 1, len(running)))
        print("clauses: %d" % len(CLAUSES))
        print("characters: %d (gate %d-%d)" % (len(line), GATE_MIN, GATE_MAX))
        print("digest: %s" % hashlib.sha256(line.encode("utf-8")).hexdigest())
        return 0
    sha = publish(line)
    print("wrote %d chars, sha256 %s" % (len(line), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

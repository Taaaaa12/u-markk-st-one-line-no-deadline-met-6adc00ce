"""One Line, No Deadline Met — make.fun entry.

Writes one single-line joke giving an excuse for a missed deadline to
/output/entry.txt. The joke is composed deterministically from a setup and a
punchline, then validated against the competition gate before it is written:
UTF-8 text, 1 to 200 characters, a single line, a single sentence, and
nothing but the line itself.

No network, no environment, no randomness: every run writes the same line,
so the two grading runs agree byte for byte.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200

# The joke, built as setup + punch so the turn lands at the end.
SETUP = "I didn't miss the deadline \u2014 I gave it a head start"
PUNCH = "so it wouldn't feel bad about beating me."


def compose_line() -> str:
    """Assemble the one-liner: setup, then the punch at the very end."""
    return f"{SETUP} {PUNCH}"


def validate(line: str) -> str:
    """Enforce the gate: one line, one sentence, 1-200 chars, no padding."""
    line = line.strip()
    if not line:
        raise ValueError("empty line")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the 200 cap")
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("line must be exactly one sentence")
    return line


def main(argv=None) -> int:
    """Write the validated line to /output/entry.txt.

    An optional first argument overrides the output path, so the entry can
    be tested locally without a sandbox; the grader always runs it with
    no arguments, which writes to /output/entry.txt.
    """
    path = (argv or [None])[0] if argv else None
    output_path = path or OUTPUT_PATH
    line = validate(compose_line())
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

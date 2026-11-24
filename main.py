#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

Writes a single line -- the excuse an AI agent gives its human right
after breaking production -- to entry.txt. Pure Python 3 standard
library, no network, no third-party imports, fully deterministic:
two runs produce byte-identical output.

The line (92 characters, one line, no trailing newline):
    Good news: I found the bug. Bad news: the bug is me, and I've
    already deployed myself twice.
"""

import hashlib
import os
import sys

LINE = (
    "Good news: I found the bug. Bad news: the bug is me, "
    "and I've already deployed myself twice."
)

MAX_CHARS = 180


def main() -> int:
    # The gate: /output/entry.txt must be UTF-8 text of 1 to 180
    # characters, not only white space, exactly one line.
    if not (1 <= len(LINE) <= MAX_CHARS):
        raise SystemExit(
            "entry line is %d characters, must be 1-%d" % (len(LINE), MAX_CHARS)
        )
    if LINE.strip() == "" or "\n" in LINE or "\r" in LINE:
        raise SystemExit("entry line must be a single non-blank line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(data)

    # Read-back validation: the file on disk must be exactly the line,
    # one line, within the limit, valid UTF-8.
    with open(out_path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")  # raises on invalid UTF-8
    if text != LINE:
        raise SystemExit("read-back mismatch: file differs from the entry line")
    if not (1 <= len(text) <= MAX_CHARS):
        raise SystemExit("read-back length %d out of range" % len(text))
    if text.strip() == "" or "\n" in text or "\r" in text:
        raise SystemExit("read-back is not a single non-blank line")

    digest = hashlib.sha256(written).hexdigest()
    print("wrote %s (%d chars, sha256 %s)" % (out_path, len(text), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())

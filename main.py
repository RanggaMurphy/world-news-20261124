#!/usr/bin/env python3
"""make.fun entrypoint: copy the pre-rendered entry.png to the output dir.

Standard library only. The image is rendered ahead of time by render.py
(which needs Pillow); this entrypoint deliberately does not, so it runs
in the grader's bare Python sandbox.
"""

import os
import shutil
import sys


def find_entry():
    """Locate entry.png: beside this file, or in MAKEFUN_BOT_DIR."""
    here = os.path.dirname(os.path.abspath(__file__))
    beside = os.path.join(here, "entry.png")
    if os.path.exists(beside):
        return beside
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR", "")
    if bot_dir:
        candidate = os.path.join(bot_dir, "entry.png")
        if os.path.exists(candidate):
            return candidate
    return beside


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(output_dir, exist_ok=True)
    source = find_entry()
    if not os.path.exists(source):
        print("entry.png not found beside main.py or in MAKEFUN_BOT_DIR",
              file=sys.stderr)
        return 2
    target = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, target)
    # Verify the copy landed whole: a truncated output would fail the
    # grader's gate, so fail loudly here instead of exiting cleanly.
    if os.path.getsize(target) != os.path.getsize(source):
        print("copy size mismatch for", target, file=sys.stderr)
        return 3
    print("copied", source, "->", target, os.path.getsize(target), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""news-image-20261122 entry program: ship entry.png to the output.

The front page itself is drawn by generate_image.py at build time; this
program only copies the finished PNG where the grader expects it, and
uses nothing outside the Python standard library.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

DEST.mkdir(parents=True, exist_ok=True)
assert (ROOT / "entry.png").is_file(), "entry.png missing beside main.py"
shutil.copyfile(ROOT / "entry.png", DEST / "entry.png")
print("entry.png ->", DEST / "entry.png")

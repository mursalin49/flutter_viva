import os
import sys

# Import CHAPTERS from build_guide
sys.path.insert(0, os.path.dirname(__file__))
from build_guide import CHAPTERS

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")
SUMMARY_PATH = os.path.join(BASE_DIR, "SUMMARY.md")
BOOK_TOML_PATH = os.path.join(BASE_DIR, "book.toml")

summary_lines = [
    "# Summary",
    "",
    "- [🎯 ভূমিকা ও গাইড পরিচিতি](README.md)",
    "- [📖 সম্পূর্ণ মাস্টার নোট (All-in-One)](FLUTTER_INTERVIEW_COMPLETE_GUIDE.md)",
    ""
]

for ch in CHAPTERS:
    summary_lines.append(f"# {ch['title']}")
    summary_lines.append("")
    for fname, ftitle in ch['files']:
        fpath = f"{ch['dir']}/{fname}"
        summary_lines.append(f"- [{ftitle}]({fpath})")
    summary_lines.append("")

with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(summary_lines))
print(f"[+] SUMMARY.md created at: {SUMMARY_PATH}")

book_toml_content = """[book]
title = "Flutter Interview Preparation Guide (বাংলা)"
authors = ["Flutter Community"]
description = "সম্পূর্ণ বাংলা Flutter ও Dart ইন্টারভিউ প্রস্তুতি নোট ও প্রশ্নোত্তর"
language = "bn"
multilingual = false
src = "."

[output.html]
git-repository-url = "https://github.com/mursalin49/flutter_viva"
edit-url-template = "https://github.com/mursalin49/flutter_viva/edit/main/{path}"
default-theme = "light"
preferred-dark-theme = "navy"

[output.html.search]
enable = true
limit-results = 30
use-boolean-and = true
boost-title = 2
boost-hierarchy = 1
boost-paragraph = 1
expand = true
heading-split-level = 3

[build]
build-dir = "book"
"""

with open(BOOK_TOML_PATH, "w", encoding="utf-8") as f:
    f.write(book_toml_content)
print(f"[+] book.toml created at: {BOOK_TOML_PATH}")

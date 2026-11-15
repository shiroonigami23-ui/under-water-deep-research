"""Fail if any relative link or image in a Markdown file points at a missing file."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pat = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
bad = 0
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith(".") and d != "connected"]  # connected/ mirrors another repo
    for f in fn:
        if not f.endswith(".md"):
            continue
        p = os.path.join(dp, f)
        for m in pat.finditer(open(p, encoding="utf-8").read()):
            t = m.group(1).split("#")[0]
            if not t or re.match(r"^[a-z]+:", t):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(dp, t))):
                print(f"{os.path.relpath(p, ROOT)} -> missing {t}"); bad += 1
print("broken links:", bad)
sys.exit(1 if bad else 0)

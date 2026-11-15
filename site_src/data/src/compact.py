"""Compact catalog entries: one line per species.
Format:  # Group|emoji   then   Name|Scientific|dmin|dmax|Where|Diet|IUCN|Summary[|sound query]
"""
import re, sys
from sp_helper import load, OUT
import json
IU = {"LC": "Least Concern", "NT": "Near Threatened", "VU": "Vulnerable", "EN": "Endangered", "CR": "Critically Endangered",
      "DD": "Data Deficient", "NE": "Not Evaluated", "EW": "Extinct in the Wild", "EX": "Extinct"}
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")
def parse(text):
    data = {d["slug"]: d for d in load()}
    sci_seen = {d.get("scientific") for d in data.values()}
    group = emoji = None; n = 0
    for ln in text.strip().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("#"):
            group, emoji = [x.strip() for x in ln[1:].split("|")]; continue
        p = [x.strip() for x in ln.split("|")]
        name, sci, dmin, dmax, where, diet, iu, summ = p[:8]
        if sci in sci_seen:
            continue
        slug = slugify(name)
        if slug in data:
            slug = slugify(name + " " + sci.split()[-1])
        d = dict(slug=slug, name=name, scientific=sci, group=group, emoji=emoji, depth_min=int(dmin), depth_max=int(dmax),
                 oceans=[w.strip() for w in where.split(";")], diet=diet, iucn=IU.get(iu, iu), summary=summ,
                 wiki=sci.replace(" ", "_") if not sci.endswith(" sp.") else name.replace(" ", "_"), compact=True)
        if len(p) > 8 and p[8]:
            d["sound"] = p[8]
        data[slug] = d; sci_seen.add(sci); n += 1
    json.dump(sorted(data.values(), key=lambda d: (d["group"], d["name"])), open(OUT, "w"), ensure_ascii=False, indent=0)
    print(f"+{n} -> {len(data)} species")
if __name__ == "__main__":
    parse(open(sys.argv[1], encoding="utf-8").read())

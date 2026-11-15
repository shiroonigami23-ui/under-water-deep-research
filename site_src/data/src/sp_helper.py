import json, os
OUT = os.path.join(os.path.dirname(__file__), "..", "species.json")
F = ["slug","name","scientific","group","emoji","depth_min","depth_max","oceans","size","lifespan","diet","iucn","summary",
     "overview","habitat","feeding","reproduction","migration","behaviour","adaptations","conservation","wiki","fishbase"]
def load():
    return json.load(open(OUT)) if os.path.exists(OUT) else []
def add(rows):
    data = {d["slug"]: d for d in load()}
    for r in rows:
        d = dict(zip(F, r)); d = {k: v for k, v in d.items() if v not in (None, "")}
        data[d["slug"]] = d
    json.dump(sorted(data.values(), key=lambda d: (d["group"], d["name"])), open(OUT, "w"), ensure_ascii=False, indent=0)
    print(len(data), "species")

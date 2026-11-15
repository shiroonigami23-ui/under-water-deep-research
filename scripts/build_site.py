"""Static research-site generator for GitHub Pages (serves from repo root).

Source:   site_src/site.json + site_src/<section>/<page>.md
Output:   index.html, wiki/**.html, assets/site/*  (all relative links -> works under /<repo>/)
Run:      python scripts/build_site.py
Needs:    markdown, jinja2
"""
import json, os, re, shutil, html, datetime, zlib, urllib.parse
import markdown
from jinja2 import Environment, BaseLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "site_src")
CFG = json.load(open(os.path.join(SRC, "site.json"), encoding="utf-8"))
GH = f"https://github.com/{CFG['github']}"
OUT_WIKI = os.path.join(ROOT, "wiki")
ASSETS = os.path.join(ROOT, "assets", "site")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    meta, body = {}, raw
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, body


def callouts(body):
    # :::facts Title  ...  :::   -> styled boxes (markdown inside)
    def rep(m):
        kind, title, inner = m.group(1), (m.group(2) or "").strip(), m.group(3)
        head = f'<div class="callout-title">{html.escape(title)}</div>' if title else ""
        return f'\n<div class="callout {kind}" markdown="1">\n{head}\n\n{inner}\n\n</div>\n'
    def rep2(m):
        title, inner = m.group(1).strip(), m.group(2)
        idattr = ""
        mm = re.match(r"#([\w-]+)\s+(.*)", title)
        if mm:
            idattr, title = f' id="{mm.group(1)}"', mm.group(2)
        op = " open" if title.startswith("!") else ""
        return f'\n<details class="coll trkcard"{idattr}{op}><summary>{html.escape(title.lstrip("!"))}</summary>\n<div class="collin" markdown="1">\n\n{inner}\n\n</div></details>\n'
    body = re.sub(r"^:::collapse[ \t]*(.*?)\n(.*?)^:::[ \t]*$", rep2, body, flags=re.S | re.M)
    return re.sub(r"^:::(\w+)[ \t]*(.*?)\n(.*?)^:::[ \t]*$", rep, body, flags=re.S | re.M)


def include_repo_file(rel, page_url):
    """Pull a Markdown file from the repo and fix its relative links."""
    p = os.path.join(ROOT, rel)
    text = open(p, encoding="utf-8-sig").read()
    base = os.path.dirname(rel)
    def fix(m):
        bang, label, target = m.group(1), m.group(2), m.group(3)
        if re.match(r"^[a-z]+:|^#", target):
            return m.group(0)
        t = os.path.normpath(os.path.join(base, target.split("#")[0])).replace("\\", "/")
        if bang:
            return f"{bang}[{label}](/{t})"
        mapped = CFG.get("repo_map", {}).get(t)
        if mapped:
            return f"[{label}]({mapped})"
        if t.endswith((".html", ".pdf")) or t.startswith(("labs/", "assets/")):
            return f"[{label}](/{t})"
        return f"**{label}**"
    text = re.sub(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)", fix, text)
    text = re.sub(r"^# .*\n", "", text, count=1)  # drop duplicate H1
    return text


def relativize(htmltext, depth):
    pre = "../" * depth if depth else "./"
    return re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{pre}', htmltext)


MD_EXT = ["extra", "toc", "sane_lists", "smarty", "md_in_html"]
MD_CFG = {"toc": {"permalink": "#", "toc_depth": "2-3"}, "footnotes": {"BACKLINK_TEXT": "↩"}}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="{{ cfg.theme_default }}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} · {{ cfg.name }}</title>
<meta name="description" content="{{ summary|e }}">
<link rel="stylesheet" href="{{ root }}assets/site/site.css">
<script>try{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
</head><body class="{{ bodyclass }}">
<header class="topbar"><div class="wrap topin">
 <button class="burger" aria-label="Menu" onclick="document.body.classList.toggle('navopen')">☰</button>
 <a class="brand" href="{{ root }}index.html"><span class="logo">{{ cfg.logo }}</span><span><b>{{ cfg.name }}</b><small>{{ cfg.kicker }}</small></span></a>
 <nav class="mainnav">{% for s in nav %}<a href="{{ root }}wiki/{{ s.id }}/index.html" class="{{ 'on' if s.id==cur_sec }}">{{ s.title }}</a>{% endfor %}</nav>
 <form class="search" action="{{ root }}wiki/search.html"><input name="q" placeholder="Search {{ npages }} articles…" aria-label="Search"></form>
 <button class="themebtn" aria-label="Toggle theme" onclick="const d=document.documentElement;d.dataset.theme=d.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('theme',d.dataset.theme)}catch(e){}">◐</button>
</div></header>
{% if tracker %}<details class="trackbar"{% if bodyclass=='homepage' %} open{% endif %}><summary><span class="live">●</span> Live research tracker <span class="muted">· {{ tracker|length }} streams · updated {{ built }}</span></summary>
<div class="wrap"><div class="trackgrid">{% for t in tracker %}<a class="trk" href="/wiki/{{ cfg.tracker_page }}.html#{{ t.id }}"><span class="ti">{{ t.icon }}</span><b>{{ t.name }}</b><span class="st">{{ t.status }}</span><span class="nx">Next: {{ t.next }}</span></a>{% endfor %}</div>
<p class="small"><a href="/wiki/{{ cfg.tracker_page }}.html">Open the full tracker with sources →</a></p></div></details>{% endif %}
{{ content }}
<footer class="foot"><div class="wrap footgrid">
 <div><div class="brand small"><span class="logo">{{ cfg.logo }}</span><b>{{ cfg.name }}</b></div><p>{{ cfg.footer }}</p>
 <p class="muted">Content reviewed {{ built }} · MIT licensed · <a href="https://github.com/{{ cfg.github }}">Source on GitHub</a></p></div>
 {% for s in sections %}<div><h4><a href="{{ root }}wiki/{{ s.id }}/index.html">{{ s.title }}</a></h4><ul>{% for p in s.pages[:6] %}<li><a href="{{ root }}wiki/{{ s.id }}/{{ p.slug }}.html">{{ p.title }}</a></li>{% endfor %}</ul></div>{% endfor %}
 <div><h4>Reference</h4><ul><li><a href="{{ root }}wiki/glossary.html">Glossary</a></li><li><a href="{{ root }}wiki/timeline.html">Timeline</a></li><li><a href="{{ root }}wiki/sources.html">All sources</a></li><li><a href="{{ root }}wiki/search.html">Search</a></li><li><a href="{{ root }}wiki/about.html">About &amp; method</a></li></ul></div>
</div></footer>
<script src="{{ root }}assets/site/site.js"></script>
</body></html>"""

ARTICLE = r"""<div class="wrap layout">
<aside class="sidebar"><div class="sidehead"><a href="{{ root }}wiki/{{ sec.id }}/index.html">{{ sec.icon }} {{ sec.title }}</a></div>
<ul>{% for p in sec.pages %}<li><a class="{{ 'on' if p.slug==page.slug }}" href="{{ root }}wiki/{{ sec.id }}/{{ p.slug }}.html">{{ p.title }}</a></li>{% endfor %}</ul>
<div class="sidehead other">Other sections</div><ul class="others">{% for s in sections if s.id!=sec.id %}<li><a href="{{ root }}wiki/{{ s.id }}/index.html">{{ s.icon }} {{ s.title }}</a></li>{% endfor %}</ul></aside>
<main class="article">
<div class="crumbs"><a href="{{ root }}index.html">Home</a> › <a href="{{ root }}wiki/{{ sec.id }}/index.html">{{ sec.title }}</a> › {{ page.title }}</div>
<h1>{{ page.title }}</h1>
{% if page.summary %}<p class="lede">{{ page.summary }}</p>{% endif %}
<div class="meta">{% if page.updated %}<span>📅 Reviewed {{ page.updated }}</span>{% endif %}<span>⏱ {{ page.minutes }} min read</span><span>🔗 {{ page.nrefs }} sources</span>{% if page.level %}<span>🎓 {{ page.level }}</span>{% endif %}</div>
{% if sec.pdf %}<div class="pdfbar"><a class="btn" target="_blank" rel="noopener" href="{{ root }}assets/pdf/{{ page.slug }}.pdf">📄 Open PDF in new tab</a><a class="btn alt" download href="{{ root }}assets/pdf/{{ page.slug }}.pdf">⬇ Download PDF</a></div>{% endif %}
<div class="prose">{{ page.html }}</div>
<nav class="pager">{% if prev %}<a class="prev" href="{{ root }}wiki/{{ sec.id }}/{{ prev.slug }}.html">← {{ prev.title }}</a>{% else %}<span></span>{% endif %}{% if next %}<a class="next" href="{{ root }}wiki/{{ sec.id }}/{{ next.slug }}.html">{{ next.title }} →</a>{% endif %}</nav>
</main>
<aside class="toc"><div class="tochead">On this page</div>{{ page.toc }}</aside>
</div>"""

SECTION = r"""<section class="sechero"><div class="wrap"><div class="crumbs"><a href="{{ root }}index.html">Home</a> › {{ sec.title }}</div>
<h1>{{ sec.icon }} {{ sec.title }}</h1><p class="lede">{{ sec.desc }}</p></div></section>
<main class="wrap"><div class="cards">{% for p in sec.pages %}<a class="card" href="{{ root }}wiki/{{ sec.id }}/{{ p.slug }}.html">{% if p.image %}<img src="{{ root }}{{ p.image }}" alt="" loading="lazy">{% endif %}<div class="cb"><h3>{{ p.title }}</h3><p>{{ p.summary }}</p><span class="cm">{{ p.minutes }} min · {{ p.nrefs }} sources</span></div></a>{% endfor %}</div></main>"""

PLAIN = r"""<main class="wrap plain"><div class="crumbs"><a href="{{ root }}index.html">Home</a> › {{ title }}</div><h1>{{ title }}</h1>{{ body }}</main>"""


# ---------------------------------------------------------------- collections (data-driven catalogs)
IMG_EXT = (".webp", ".png", ".jpg", ".jpeg")
PROMPTS = []
PHOTOS = []


def find_img(cid, slug):
    for e in IMG_EXT:
        rel = f"assets/img/{cid}/{slug}{e}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return rel
    return None


def placeholder(icon, name, sub, hue):
    return (f'<svg class="ph" viewBox="0 0 640 360" role="img" aria-label="{html.escape(name)}">'
            f'<defs><linearGradient id="g{hue}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="hsl({hue},70%,32%)"/>'
            f'<stop offset="1" stop-color="hsl({(hue+40)%360},70%,12%)"/></linearGradient></defs>'
            f'<rect width="640" height="360" fill="url(#g{hue})"/><text x="320" y="170" font-size="110" text-anchor="middle">{icon}</text>'
            f'<text x="320" y="250" font-size="30" fill="#fff" text-anchor="middle" font-family="system-ui" font-weight="700">{html.escape(name)}</text>'
            f'<text x="320" y="290" font-size="20" fill="#dde" text-anchor="middle" font-family="system-ui" font-style="italic">{html.escape(sub or "")}</text>'
            f'<text x="320" y="340" font-size="14" fill="#aab" text-anchor="middle" font-family="system-ui">Loading photo…</text></svg>')


def visual(v, it):
    if not v:
        return ""
    if v["type"] == "depth":
        lo, hi = it.get(v["min"]), it.get(v["max"])
        if lo is None or hi is None:
            return ""
        X = lambda d: 40 + 560 * (max(d, 0) / 11000) ** 0.5
        ticks = "".join(f'<line x1="{X(d)}" y1="34" x2="{X(d)}" y2="70" stroke="currentColor" opacity=".25"/><text x="{X(d)}" y="88" font-size="11" text-anchor="middle" fill="currentColor" opacity=".7">{d:,}</text>' for d in (0, 200, 1000, 2000, 4000, 6000, 8000, 11000))
        return (f'<figure class="viz"><svg viewBox="0 0 640 100" class="vizsvg">{ticks}'
                f'<rect x="40" y="44" width="560" height="16" rx="8" fill="currentColor" opacity=".08"/>'
                f'<rect x="{X(lo)}" y="44" width="{max(X(hi)-X(lo),4)}" height="16" rx="8" fill="var(--accent)"/>'
                f'<text x="40" y="24" font-size="13" fill="currentColor">{v.get("label", "Depth range")}: {lo:,}–{hi:,} m (square-root scale)</text></svg></figure>')
    if v["type"] == "size":
        r = it.get(v["key"])
        if not r:
            return ""
        ref = v.get("ref", 6371); refname = v.get("refname", "Earth")
        scale = 120 / max(r, ref)
        return (f'<figure class="viz"><svg viewBox="0 0 640 300" class="vizsvg"><circle cx="190" cy="160" r="{max(ref*scale,1.5)}" fill="#4f9cf0" opacity=".85"/>'
                f'<text x="190" y="295" font-size="13" text-anchor="middle" fill="currentColor">{refname} ({ref:,} km)</text>'
                f'<circle cx="460" cy="160" r="{max(r*scale,1.5)}" fill="var(--accent)" opacity=".9"/>'
                f'<text x="460" y="295" font-size="13" text-anchor="middle" fill="currentColor">{html.escape(it[v.get("label","name")])} ({r:,} km)</text>'
                f'<text x="20" y="22" font-size="13" fill="currentColor">Radius to scale</text></svg></figure>')
    return ""


def build_collections(env, write, sections, search, built):
    out = []
    for c in CFG.get("collections", []):
        items = json.load(open(os.path.join(SRC, c["file"]), encoding="utf-8"))
        cid = c["id"]; nk = c.get("name_key", "name"); sk = c.get("sub_key")
        groups = sorted({it.get(c.get("group_key", "group"), "Other") for it in items})
        cards, rows = [], []
        for i, it in enumerate(items):
            slug = it["slug"]; name = it[nk]; sub = it.get(sk, "") if sk else ""
            hue = zlib.crc32(str(it.get(c.get("group_key", "group"), "")).encode()) % 360
            img = find_img(cid, slug)
            if img:
                pic = f'<img class="hero-img" src="/{img}" alt="{html.escape(name)}">'
                thumb = f'<img src="/{img}" alt="" loading="lazy">'
            else:
                icon = it.get("emoji", c["icon"])
                try:
                    prompt = c["prompt"].format(**{k: (v if not isinstance(v, list) else ", ".join(map(str, v))) for k, v in it.items()})
                except KeyError:
                    prompt = f"Scientific illustration of {name}"
                wk = urllib.parse.unquote(str(it.get(c.get("photo_key", "wiki"), ""))).replace("_", " ") if c.get("live_photos") else ""
                if wk:
                    PHOTOS.append(dict(wiki=wk, name=name, save=f"assets/img/{cid}/{slug}.png", coll=c["title"]))
                da = f' data-wiki="{html.escape(str(wk))}" data-save="assets/img/{cid}/{slug}.png"' if wk else ""
                pic = f'<div class="livepic big"{da}>{placeholder(icon, name, sub, hue)}</div>'
                thumb = f'<div class="livepic"{da}>{placeholder(icon, name, sub, hue)}</div>'
                PROMPTS.append((c["title"], name, f"assets/img/{cid}/{slug}.png", prompt))
            facts = "".join(f"<tr><th>{lab}</th><td>{html.escape(', '.join(map(str, it[k])) if isinstance(it.get(k), list) else str(it[k]))}</td></tr>" for k, lab in c["facts"] if it.get(k) not in (None, "", []))
            body = ""
            for k, lab in c["texts"]:
                if it.get(k):
                    txt = it[k] if isinstance(it[k], str) else "\n".join(f"- {x}" for x in it[k])
                    body += f"\n\n## {lab}\n\n{txt}"
            srcs = []
            for lab, t in c.get("source_tpl", []):
                try:
                    srcs.append((lab, t.format(**{k: urllib.parse.quote(str(v), safe="_(),'") for k, v in it.items()})))
                except KeyError:
                    pass
            srcs += [("Source", u) for u in it.get("sources", [])]
            body += "\n\n## Sources\n\n" + "\n".join(f"{n+1}. {lab}: <{u}>" for n, (lab, u) in enumerate(srcs))
            md = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_CFG)
            h = md.convert(callouts(body))
            prev = items[i - 1] if i else None; nxt = items[i + 1] if i + 1 < len(items) else None
            content = env.from_string(COLL_ITEM).render(c=c, it=it, name=name, sub=sub, pic=pic, facts=facts, viz=visual(c.get("visual"), it),
                                                       body=h, toc=md.toc, prev=prev, next=nxt, nk=nk, n=len(items))
            write(f"wiki/{cid}/{slug}.html", name, content, 2, it.get("summary", ""), cid)
            search.append({"t": name, "s": c["title"], "u": f"wiki/{cid}/{slug}.html", "d": it.get("summary", sub),
                           "x": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))[:3000]})
            grp = it.get(c.get("group_key", "group"), "Other")
            cells = "".join(f'<td>{html.escape(", ".join(map(str, it[k])) if isinstance(it.get(k), list) else str(it.get(k, "")))}</td>' for k, _ in c["columns"])
            rows.append(f'<tr data-g="{html.escape(grp)}"><td><a href="/wiki/{cid}/{slug}.html">{html.escape(name)}</a>{"<br><i class=muted>" + html.escape(sub) + "</i>" if sub else ""}</td>{cells}</tr>')
            cards.append(f'<a class="card" data-g="{html.escape(grp)}" href="/wiki/{cid}/{slug}.html">{thumb}<div class="cb"><span class="tag">{html.escape(grp)}</span><h3>{html.escape(name)}</h3><p>{html.escape(it.get("summary", ""))}</p></div></a>')
        chips = '<button class="chip on" data-g="*">All</button>' + "".join(f'<button class="chip" data-g="{html.escape(g)}">{html.escape(g)}</button>' for g in groups)
        head = "".join(f"<th>{lab}</th>" for _, lab in c["columns"])
        content = env.from_string(COLL_INDEX).render(c=c, n=len(items), chips=chips, cards="".join(cards), rows="".join(rows), head=head, ngroups=len(groups))
        write(f"wiki/{cid}/index.html", c["title"], content, 2, c["desc"], cid)
        out.append((c, len(items)))
    return out


COLL_ITEM = r"""<div class="wrap layout">
<aside class="sidebar"><div class="sidehead"><a href="/wiki/{{ c.id }}/index.html">{{ c.icon }} {{ c.title }}</a></div>
<p class="muted small">{{ n }} entries · use the catalog filters to browse.</p>
{% if prev %}<a class="sidebtn" href="/wiki/{{ c.id }}/{{ prev.slug }}.html">← {{ prev[nk] }}</a>{% endif %}
{% if next %}<a class="sidebtn" href="/wiki/{{ c.id }}/{{ next.slug }}.html">{{ next[nk] }} →</a>{% endif %}</aside>
<main class="article"><div class="crumbs"><a href="/index.html">Home</a> › <a href="/wiki/{{ c.id }}/index.html">{{ c.title }}</a> › {{ name }}</div>
<h1>{{ it.emoji or '' }} {{ name }}</h1>{% if sub %}<p class="sci">{{ sub }}</p>{% endif %}
{% if it.summary %}<p class="lede">{{ it.summary }}</p>{% endif %}
<div class="entry-top"><div class="entry-pic">{{ pic }}</div><table class="factbox">{{ facts }}</table></div>
{{ viz }}
<div class="prose">{{ body }}</div></main>
<aside class="toc"><div class="tochead">On this page</div>{{ toc }}</aside></div>"""

COLL_INDEX = r"""<section class="sechero"><div class="wrap"><div class="crumbs"><a href="/index.html">Home</a> › {{ c.title }}</div>
<h1>{{ c.icon }} {{ c.title }}</h1><p class="lede">{{ c.desc }}</p><p class="muted">{{ n }} entries in {{ ngroups }} groups.</p></div></section>
<main class="wrap"><div class="catbar"><input class="catfilter" placeholder="Filter {{ n }} entries…"><div class="chips">{{ chips }}</div>
<div class="viewtoggle"><button class="chip on" data-v="grid">Cards</button><button class="chip" data-v="table">Table</button></div></div>
<div class="cards catgrid">{{ cards }}</div>
<div class="cattable" hidden><table class="sortable"><thead><tr><th>Name</th>{{ head }}</tr></thead><tbody>{{ rows }}</tbody></table></div></main>"""


def write_prompts():
    json.dump(PHOTOS, open(os.path.join(ASSETS, "photo-index.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump([dict(sec=a, name=b, save=c, prompt=d) for a, b, c, d in PROMPTS],
              open(os.path.join(ASSETS, "prompts.json"), "w", encoding="utf-8"), ensure_ascii=False)
    path = os.path.join(ROOT, "prompts.md")
    lines = ["# Image prompts (Nano Banana)", "",
             "Auto-generated by `scripts/build_site.py`. Catalog entries load a real, openly licensed photo from Wikimedia Commons in the visitor's browser.",
             "**Only generate an image when the site cannot find one.** Open the site's *Photo status* page (wiki/photo-status.html): it checks every entry live and lists exactly which ones still need a picture, with the prompt and a copy button.",
             "Then save the image at the path shown and rerun the build. A local image always takes priority over the live photo.",
             "Generate the image, save it at the path shown (PNG/JPG/WEBP all work, 16:9 recommended), then rerun the build; the placeholder is replaced automatically.", "",
             f"Total pending: **{len(PROMPTS)}**", ""]
    cur = None
    for sec, name, target, prompt in PROMPTS:
        if sec != cur:
            lines += ["", f"## {sec}", ""]; cur = sec
        lines += [f"### {name}", f"- Save as: `{target}`", "```text", prompt, "```", ""]
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def export_pdfs(sections):
    import subprocess, shutil as sh
    chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser") if sh.which(c)), None)
    if not chrome:
        print("PDF export skipped (no Chrome)"); return
    outdir = os.path.join(ROOT, "assets", "pdf"); os.makedirs(outdir, exist_ok=True)
    n = 0
    for sec in sections:
        if not sec.get("pdf"):
            continue
        for p in sec["pages"]:
            src = os.path.join(ROOT, "wiki", sec["id"], p["slug"] + ".html")
            dst = os.path.join(outdir, p["slug"] + ".pdf")
            subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={dst}", "file://" + src], capture_output=True, timeout=120)
            n += os.path.exists(dst)
    print(f"exported {n} PDFs")


def main():
    env = Environment(loader=BaseLoader(), autoescape=False)
    T = env.from_string(TEMPLATE)
    built = CFG.get("reviewed", datetime.date.today().isoformat())
    sections, allpages, search = [], [], []
    global NAV
    NAV = [dict(id=x["id"], title=x["title"]) for x in CFG.get("nav_order", [])] or [dict(id=x["id"], title=x["title"]) for x in CFG["sections"] + CFG.get("collections", [])]
    for s in CFG["sections"]:
        sec = dict(s); sec["pages"] = []
        for slug in s["pages"]:
            meta, body = parse(os.path.join(SRC, s["id"], slug + ".md"))
            url = f"/wiki/{s['id']}/{slug}.html"
            if meta.get("include"):
                body = body + "\n\n" + include_repo_file(meta["include"], url)
            md = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_CFG)
            h = md.convert(callouts(body))
            words = len(re.sub(r"<[^>]+>", " ", h).split())
            refs = re.findall(r'<li id="fn:[^"]+">(.*?)</li>', h, flags=re.S)
            links = re.findall(r'href="(https?://[^"]+)"', "".join(refs))
            p = dict(slug=slug, title=meta.get("title", slug), summary=meta.get("summary", ""), updated=meta.get("updated", built),
                     level=meta.get("level", ""), image=(meta.get("image", "").lstrip("/") or (find_img("articles", slug) or "")), html=h, toc=md.toc,
                     minutes=max(1, round(words / 220)), nrefs=len(refs), links=links, words=words, url=url, sec=s["id"])
            sec["pages"].append(p); allpages.append(p)
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))[:6000]
            search.append({"t": p["title"], "s": s["title"], "u": url.lstrip("/"), "d": p["summary"], "x": text})
        sections.append(sec)

    if os.path.isdir(OUT_WIKI):
        shutil.rmtree(OUT_WIKI)
    os.makedirs(ASSETS, exist_ok=True)
    for f in ("site.css", "site.js"):
        shutil.copy(os.path.join(SRC, "_assets", f), os.path.join(ASSETS, f))
    json.dump(search, open(os.path.join(ASSETS, "search-index.json"), "w"), ensure_ascii=False)

    def write(rel, title, content, depth, summary="", cur_sec="", bodyclass=""):
        root = "../" * depth if depth else ""
        page = T.render(cfg=CFG, nav=NAV, title=title, summary=summary, content=content, root=root, sections=sections,
                        cur_sec=cur_sec, npages=len(allpages), built=built, bodyclass=bodyclass, tracker=CFG.get("tracker", []))
        out = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(relativize(page, depth))

    A, S, P = env.from_string(ARTICLE), env.from_string(SECTION), env.from_string(PLAIN)
    for sec in sections:
        root = "../../"
        write(f"wiki/{sec['id']}/index.html", sec["title"], S.render(sec=sec, root=root), 2, sec["desc"], sec["id"])
        for i, p in enumerate(sec["pages"]):
            prev = sec["pages"][i - 1] if i else None
            nxt = sec["pages"][i + 1] if i + 1 < len(sec["pages"]) else None
            write(f"wiki/{sec['id']}/{p['slug']}.html", p["title"],
                  A.render(sec=sec, page=p, sections=sections, root=root, prev=prev, next=nxt), 2, p["summary"], sec["id"])

    colls = build_collections(env, write, sections, search, built)
    for p in allpages:
        if not p["image"]:
            PROMPTS.append(("Articles", p["title"], f"assets/img/articles/{p['slug']}.png",
                            f"Editorial scientific illustration for an encyclopedia article titled \"{p['title']}\": {p['summary']} "
                            f"{CFG.get('prompt_style', 'Photorealistic, accurate, high detail, 16:9, no text')}"))
    json.dump(search, open(os.path.join(ASSETS, "search-index.json"), "w"), ensure_ascii=False)
    write_prompts()
    # special pages
    for name in ("glossary", "timeline", "about"):
        meta, body = parse(os.path.join(SRC, f"{name}.md"))
        h = markdown.markdown(callouts(body), extensions=MD_EXT, extension_configs=MD_CFG)
        write(f"wiki/{name}.html", meta.get("title", name), P.render(title=meta.get("title", name), body=f'<div class="prose wide">{h}</div>', root="../"), 1, meta.get("summary", ""))
    # bibliography
    biblio = {}
    for p in allpages:
        for l in p["links"]:
            biblio.setdefault(l, []).append(p)
    rows = "".join(f'<li><a href="{html.escape(l)}">{html.escape(re.sub(r"^https?://(www\.)?", "", l)[:110])}</a> <span class="muted">— cited in ' +
                   ", ".join(f'<a href="/wiki/{q["sec"]}/{q["slug"]}.html">{html.escape(q["title"])}</a>' for q in ps[:4]) + "</span></li>"
                   for l, ps in sorted(biblio.items(), key=lambda kv: re.sub(r"^https?://(www\.)?", "", kv[0])))
    write("wiki/sources.html", "All sources", P.render(title=f"All sources ({len(biblio)})",
          body=f'<p class="lede">Every external source cited anywhere on this site, with the articles that cite it.</p><ol class="biblio">{rows}</ol>', root="../"), 1)
    write("wiki/photo-status.html", "Photo status", P.render(title="Photo status", root="../",
          body='<p class="lede">This page checks every catalog entry against Wikipedia / Wikimedia Commons right now. Entries with a real, openly licensed photo are counted; the ones without are listed with a ready-made Nano Banana prompt and the exact path to save the image to.</p><div id="photostatus" class="prose wide"><p>Checking…</p></div>'), 1, bodyclass="photostatus")
    write("wiki/search.html", "Search", P.render(title="Search", root="../", body='<input id="q" class="bigsearch" placeholder="Type to search every article…" autofocus><div id="results"></div>'), 1, bodyclass="searchpage")

    # home
    meta, body = parse(os.path.join(SRC, "home.md"))
    home_html = markdown.markdown(callouts(body), extensions=MD_EXT, extension_configs=MD_CFG)
    stats = "".join(f'<div class="stat"><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>' for a, b in CFG["stats"])
    seccards = "".join(f'<a class="seccard" href="/wiki/{s["id"]}/index.html"><div class="si">{s["icon"]}</div><h3>{s["title"]}</h3><p>{s["desc"]}</p><span class="cm">{len(s["pages"])} articles</span></a>' for s in sections)
    collcards = "".join(f'<a class="seccard coll" href="/wiki/{c["id"]}/index.html"><div class="si">{c["icon"]}</div><h3>{c["title"]}</h3><p>{c["desc"]}</p><span class="cm">{n} entries</span></a>' for c, n in colls)
    nentries = sum(n for _, n in colls)
    feat = [p for p in allpages if p["slug"] in CFG.get("featured", [])]
    featcards = "".join(f'<a class="card" href="{p["url"]}">{('<img src="/' + p["image"] + '" alt="" loading="lazy">') if p["image"] else ""}<div class="cb"><span class="tag">{next(s["title"] for s in sections if s["id"]==p["sec"])}</span><h3>{p["title"]}</h3><p>{p["summary"]}</p></div></a>' for p in feat)
    totalwords = sum(p["words"] for p in allpages)
    content = f'''<section class="hero"><div class="wrap"><div class="kicker">{CFG["kicker"]}</div><h1>{CFG["logo"]} {CFG["name"]}</h1><p class="lede">{CFG["tagline"]}</p>
<form class="herosearch" action="/wiki/search.html"><input name="q" placeholder="Search {len(allpages)} articles and {nentries} catalog entries…"></form>
<div class="stats">{stats}</div></div></section>
<main class="wrap home"><h2>Encyclopedia catalogs</h2><div class="secgrid">{collcards}</div><h2>In-depth articles by section</h2><div class="secgrid">{seccards}</div>
<h2>Featured deep dives</h2><div class="cards">{featcards}</div>
<div class="prose wide homebody">{home_html}</div>
<p class="muted small">{len(allpages)} articles · {nentries} catalog entries · ~{totalwords//1000}k words · {len(biblio)} distinct sources · reviewed {built}</p></main>'''
    write("index.html", CFG["name"], content, 0, CFG["tagline"], bodyclass="homepage")
    if os.environ.get("SKIP_PDF") != "1":
        export_pdfs(sections)
    print(f"built {len(allpages)} articles, {len(biblio)} sources, ~{totalwords} words")


if __name__ == "__main__":
    main()

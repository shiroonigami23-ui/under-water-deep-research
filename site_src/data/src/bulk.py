from sp_helper import add
def B(group, emoji, rows):
    out = []
    for r in rows:
        (slug, name, sci, dmin, dmax, oceans, size, life, diet, iucn, summ, hab, feed, rep, mig, beh) = r[:16]
        wiki = r[16] if len(r) > 16 else sci.replace(" ", "_")
        out.append([slug, name, sci, group, emoji, dmin, dmax, oceans, size, life, diet, iucn, summ,
                    None, hab, feed, rep, mig, beh, None, None, wiki, None])
    add(out)

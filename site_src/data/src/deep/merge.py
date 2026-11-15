import json,importlib.util,glob
P='../../seas.json';d=json.load(open(P));by={x['slug']:x for x in d};n=0
for f in sorted(glob.glob('s*.py')):
    s=importlib.util.spec_from_file_location('m',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    for slug,fields in m.D.items():
        x=by.get(slug)
        if not x: print('missing',slug);continue
        for k,v in fields.items():
            if len(v)>len(str(x.get(k,''))): x[k]=v;n+=1
json.dump(d,open(P,'w'),ensure_ascii=False,indent=0);print('updated fields',n)

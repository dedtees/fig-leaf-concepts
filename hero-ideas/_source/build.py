import re, os, shutil
R='/home/user/fig-leaf-concepts'
W='/tmp/claude-0/-home-user/d005f8da-4ea9-533d-b0be-b21296708ac1/scratchpad/w'
IDEAS=[
 # key, base, title, short name, alt, spots {car:(x,y,cx,cy), ...}
 ('v1','concept-1','Vertical 1','Photos on real fig leaves, stacked',
  'Three real fig leaves stacked down the page, each printed with a photo: a car on a mountain road, a house lit up at dusk and a boat on the water at sunset',
  {'car':(46,21,32,20),'home':(68,46,52,50),'boat':(45,74,29,77)}),
 ('v2','concept-1','Vertical 2','Photo panels on a fig leaf',
  'Three gold-edged photo panels stacked over a large fig leaf: a car on a mountain road, a house lit up at dusk and a boat at sunset',
  {'car':(58,24,38,24),'home':(63,49,44,49),'boat':(58,73,38,73)}),
 ('v3','concept-1','Vertical 3','Logo leaf window, three bands',
  'The Fig Leaf logo leaf as a gold-edged window split into three bands: a car on a mountain road, a house lit up at dusk and a boat at sunset',
  {'car':(68,17,55,17),'home':(62,45,36,45),'boat':(67,70,56,72)}),
 ('h1','concept-3','Horizontal 1','Photos on real fig leaves, in a row',
  'Three real fig leaves side by side, each printed with a photo: a car on a mountain road, a house lit up at dusk and a boat on the water at sunset',
  {'car':(29,41),'home':(51,43),'boat':(76,47)}),
 ('h2','concept-3','Horizontal 2','Arched photos on a fig leaf',
  'Three arched, gold-edged photos in front of a large fig leaf: a car on a mountain road, a house lit up at dusk and a boat at sunset',
  {'car':(26,47),'home':(50,42),'boat':(73,52)}),
 ('h3','concept-3','Horizontal 3','Panorama between two leaves',
  'One gold-framed panorama of a car on a mountain road, a house lit up at dusk and a boat at sunset, held between two fig leaves',
  {'car':(31,42),'home':(50,42),'boat':(69,49)}),
]
def bar(cur):
    lis=[]
    for i,(k,_,lab,name,*_) in enumerate(IDEAS):
        cc=' aria-current="page"' if k==cur else ''
        short=k.upper()
        lis.append(f'<li><a class="review-bar__link" href="../{k}/" data-name="{name}"{cc}><span class="visually-hidden">{lab}: </span>{short}<span class="visually-hidden">, {name}</span></a></li>')
    i=[x[0] for x in IDEAS].index(cur)
    prev=IDEAS[i-1][0]; nxt=IDEAS[(i+1)%len(IDEAS)][0]
    return lis, prev, nxt
for key,base,lab,name,alt,spots in IDEAS:
    s=open(f'{R}/{base}/index.html').read()
    pre=f'../../{base}/'
    def fix(m):
        attr,val=m.group(1),m.group(2)
        if re.match(r'(https?:|tel:|mailto:|#|/|data:)',val): return m.group(0)
        if val.startswith('../concept-'): return f'{attr}="../{val}"'
        if val in ('./','index.html'): return f'{attr}="{pre}"'
        if attr=='srcset': return f'{attr}="'+', '.join(pre+p.strip() for p in val.split(','))+'"'
        return f'{attr}="{pre}{val}"'
    s=re.sub(r'(href|src|srcset)="([^"]*)"',fix,s)
    oldimg='hero-stack.jpg' if base=='concept-1' else 'hero-scene.jpg'
    s=s.replace(f'{pre}assets/{oldimg}','hero.jpg')
    s=re.sub(r'<img class="scene__img" src="hero.jpg" width="\d+" height="\d+"([^>]*?)alt="[^"]*"',
             f'<img class="scene__img" src="hero.jpg" width="1950" height="1536"\\1alt="{alt}"',s)
    # hotspots / leaders / cards
    for k,v in spots.items():
        if base=='concept-1':
            x,y,cx,cy=v
            s=re.sub(rf'(<span class="scene__leader" data-scene="{k}" style=")[^"]*"',rf'\g<1>--x:{x}%;--y:{y}%"',s)
            s=re.sub(rf'(<button class="hotspot" type="button" data-scene="{k}" style=")[^"]*"',rf'\g<1>--x:{x}%;--y:{y}%;--cx:{cx}%;--cy:{cy}%"',s)
            s=re.sub(rf'(<div class="scene__card" id="card-{k}" data-scene="{k}" style=")[^"]*"',rf'\g<1>--y:{y}%"',s)
        else:
            x,y=v
            s=re.sub(rf'(<button class="hotspot" type="button" data-scene="{k}" style=")[^"]*"',rf'\g<1>--x:{x}%;--y:{y}%"',s)
            s=re.sub(rf'(<div class="scene__card" id="card-{k}" data-scene="{k}" style=")[^"]*"',rf'\g<1>--x:{x}%"',s)
    s=re.sub(r'<title>[^<]*·',f'<title>Hero idea {key.upper()} ·',s)
    s=re.sub(r'<p class="review-bar__title">.*?</p>',f'<p class="review-bar__title"><span class="review-bar__label">Hero idea {key.upper()}</span> <span class="review-bar__name">{name}</span></p>',s)
    lis,prev,nxt=bar(key)
    s=re.sub(r'<ul class="review-bar__list">.*?</ul>','<ul class="review-bar__list">\n        '+'\n        '.join(lis)+'</ul>',s,flags=re.S)
    s=re.sub(r'(review-bar__step--prev" href=")[^"]*"',rf'\g<1>../{prev}/"',s)
    s=re.sub(r'(<a class="review-bar__step" href=")[^"]*"',rf'\g<1>../{nxt}/"',s)
    s=s.replace('<meta name="robots"','<meta name="robots"') 
    d=f'{R}/hero-ideas/{key}'; os.makedirs(d,exist_ok=True)
    open(f'{d}/index.html','w').write(s)
    shutil.copy(f'{W}/hero-{key}.jpg',f'{d}/hero.jpg')
    print(key,'ok')

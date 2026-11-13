"""Builds hero-concepts/<a-d>/index.html from Concept 1's homepage.

Each page keeps Concept 1's header, hero text and sections (linked back to
../../concept-1/ for CSS, scripts, images and inner pages) and swaps only the
hero picture for one of the layouts in shared/hero-x.css, run by shared/hero-x.js.
Run from anywhere: python3 hero-concepts/build.py
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BASE = 'concept-1'

ITEMS = [
    ('car', '01', 'Auto', 'Auto insurance',
     'Liability, collision and comprehensive, compared across our carriers.',
     'crq-form/', 'Start a car quote'),
    ('home', '02', 'Home', 'Homeowners insurance',
     'Your house, your belongings and your liability, explained line by line.',
     'crq-form/', 'Start a home quote'),
    ('boat', '03', 'Boat', 'Boat insurance',
     'Hull, liability and on-the-water coverage for weekends on the bay.',
     '#quote', 'Ask about boat coverage'),
]
LENS_AT = {'car': (17, 40), 'home': (50, 40), 'boat': (83, 44)}

CONCEPTS = [
    ('a', 'Horizontal', 'Opening photo panels', 'panels'),
    ('b', 'Vertical', 'Stacked photo bands', 'bands'),
    ('c', 'Horizontal', 'Uncover lens', 'lens'),
    ('d', 'Vertical', 'Card deck', 'deck'),
]


def link(href):
    return href if href.startswith('#') else f'../../{BASE}/{href}'


def item(key, num, label, title, text, href, cta, layout, with_img=True):
    lx, ly = LENS_AT[key]
    img = f'<img class="hx__img" src="../shared/{key}.jpg" alt="" decoding="async">' if with_img else ''
    return f'''
          <div class="hx__item" data-scene="{key}" data-lx="{lx}" data-ly="{ly}">
            {img}
            <span class="hx__tag" aria-hidden="true"><span class="hx__num">{num}</span><span class="hx__label">{label}</span></span>
            <button class="hx__hit" type="button" aria-pressed="false" aria-controls="hx-{key}"><span class="visually-hidden">{title}</span></button>
            <div class="hx__body" id="hx-{key}">
              <span class="hx__num" aria-hidden="true">{num}</span>
              <p class="hx__title">{title}</p>
              <p class="hx__text">{text}</p>
              <a class="hx__link" href="{link(href)}">{cta} <span aria-hidden="true">&rarr;</span></a>
            </div>
            <span class="hx__bar" aria-hidden="true"></span>
          </div>'''


def picture(layout):
    items = ''.join(item(*it, layout=layout, with_img=(layout != 'lens')) for it in ITEMS)
    alt = 'A car on a mountain road at sunset, a house lit up at dusk and a boat on the water at sunset'
    if layout == 'bands':
        dots = ''.join(f'<button class="hx__dot" type="button" tabindex="-1" aria-hidden="true">{n}</button>' for _, n, *_ in ITEMS)
        inner = f'<div class="hx__stack">{items}\n          </div>\n          <div class="hx__rail">{dots}</div>'
    elif layout == 'deck':
        dots = ''.join(f'<button class="hx__dot" type="button" tabindex="-1" aria-hidden="true">{n}</button>' for _, n, *_ in ITEMS)
        inner = f'{items}\n          <div class="hx__dots">{dots}</div>'
    elif layout == 'lens':
        imgs = ''.join(f'<div data-k="{k}"><img src="../shared/{k}.jpg" alt="" decoding="async"></div>' for k, *_ in ITEMS)
        inner = (f'<div class="hx__strip" role="img" aria-label="{alt}">'
                 f'<div class="hx__layer hx__layer--base">{imgs}</div>'
                 f'<div class="hx__layer hx__layer--color">{imgs}</div>'
                 f'<span class="hx__ring" aria-hidden="true"></span></div>'
                 f'{items}\n          <p class="hx__hint" aria-hidden="true">Move across the picture to uncover it</p>')
    else:
        inner = items
    lens = ' data-lens' if layout == 'lens' else ''
    role = '' if layout == 'lens' else f' role="group" aria-label="{alt}"'
    return f'''      <!-- The picture: hover, tap or focus the car, home or boat (shared/hero-x.js) -->
      <div class="scene hx hx--{layout}" data-hx{lens}{role}>
          {inner}
      </div>
'''


def bar(cur):
    lis = []
    for key, orient, name, _ in CONCEPTS:
        cc = ' aria-current="page"' if key == cur else ''
        lis.append(f'<li><a class="review-bar__link" href="../{key}/" data-name="{orient}: {name}"{cc}>'
                   f'<span class="visually-hidden">Hero concept </span>{key.upper()}'
                   f'<span class="visually-hidden">, {orient.lower()}, {name}</span></a></li>')
    keys = [c[0] for c in CONCEPTS]
    i = keys.index(cur)
    return lis, keys[i - 1], keys[(i + 1) % len(keys)]


def build():
    src = open(os.path.join(REPO, BASE, 'index.html'), encoding='utf-8').read()
    pre = f'../../{BASE}/'

    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r'(https?:|tel:|mailto:|#|/|data:)', val):
            return m.group(0)
        if val.startswith('../concept-'):
            return f'{attr}="../{val}"'
        if val in ('./', 'index.html'):
            return f'{attr}="{pre}"'
        if attr == 'srcset':
            return f'{attr}="' + ', '.join(pre + p.strip() for p in val.split(',')) + '"'
        return f'{attr}="{pre}{val}"'

    for key, orient, name, layout in CONCEPTS:
        s = re.sub(r'(href|src|srcset)="([^"]*)"', fix, src)
        s = re.sub(r'\s*<link rel="preload" href="[^"]*hero-stack\.jpg" as="image">', '', s)
        s = s.replace(f'<link rel="stylesheet" href="{pre}styles.css">',
                      f'<link rel="stylesheet" href="{pre}styles.css">\n  <link rel="stylesheet" href="../shared/hero-x.css">')
        s = s.replace(f'<script src="{pre}scene.js"', '<script src="../shared/hero-x.js"')
        # swap the picture: everything from the scene comment to the end of the hero section
        s, n = re.subn(r'      <!-- The picture\..*?(?=    </section>)', picture(layout), s, count=1, flags=re.S)
        assert n == 1, 'hero picture block not found'
        s = re.sub(r'<title>[^<]*·', f'<title>Hero concept {key.upper()} ·', s)
        s = re.sub(r'<p class="review-bar__title">.*?</p>',
                   f'<p class="review-bar__title"><span class="review-bar__label">Hero {key.upper()}</span> '
                   f'<span class="review-bar__name">{orient}: {name}</span></p>', s)
        lis, prev, nxt = bar(key)
        s = re.sub(r'<ul class="review-bar__list">.*?</ul>',
                   '<ul class="review-bar__list">\n        ' + '\n        '.join(lis) + '</ul>', s, flags=re.S)
        s = re.sub(r'(review-bar__step--prev" href=")[^"]*"', rf'\g<1>../{prev}/"', s)
        s = re.sub(r'(<a class="review-bar__step" href=")[^"]*"', rf'\g<1>../{nxt}/"', s)
        out = os.path.join(HERE, key)
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(s)
        print('built', key, layout)


if __name__ == '__main__':
    build()

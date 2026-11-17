"""Builds homepages/<hero>/index.html: every new hero on a full homepage.

Each page is one of the current homepages (concept 1, 2 or 3) exactly as it
is, header, colours, sections and footer, with only the hero <section>
swapped for one of the new hero concepts. Nothing is copied: the page links
back to its homepage's folder for CSS, scripts, images and inner pages, and
to the hero's own folder for the hero's pictures, CSS and script.

Re-run after changing a homepage or a hero:  python3 homepages/build.py
"""
import os
import posixpath
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

HOMEPAGE_NAMES = {
    'concept-1': 'Homepage 1',
    'concept-2': 'Homepage 2',
    'concept-3': 'Homepage 3',
}

# (code, homepage, page the hero comes from, hero name,
#  extra CSS (repo paths), where it goes, hero script(s) in place of scene.js)
X_CSS = ['hero-concepts/shared/hero-x.css']
X_JS = ['hero-concepts/shared/hero-x.js']
HEROES = [
    ('5', 'concept-1', 'concept-5/index.html', 'Pointing fig leaf, black hero',
     ['homepages/shared/hero-5.css'], 'last', ['concept-5/concept.js']),
    ('6', 'concept-3', 'concept-6/index.html', 'Leaf slideshow',
     ['homepages/shared/hero-6.css'], 'last', ['concept-6/concept.js']),
    ('a', 'concept-2', 'hero-concepts/a/index.html', 'Opening photo panels',
     X_CSS, 'after-styles', X_JS),
    ('b', 'concept-2', 'hero-concepts/b/index.html', 'Stacked photo bands',
     X_CSS, 'after-styles', X_JS),
    ('c', 'concept-2', 'hero-concepts/c/index.html', 'Uncover lens',
     X_CSS, 'after-styles', X_JS),
    ('d', 'concept-2', 'hero-concepts/d/index.html', 'Card deck',
     X_CSS, 'after-styles', X_JS),
    ('v1', 'concept-1', 'hero-ideas/v1/index.html', 'Photos on real fig leaves, stacked',
     [], None, None),
    ('v2', 'concept-1', 'hero-ideas/v2/index.html', 'Photo panels on a fig leaf',
     [], None, None),
    ('v3', 'concept-1', 'hero-ideas/v3/index.html', 'Logo leaf window, three bands',
     [], None, None),
    ('h1', 'concept-3', 'hero-ideas/h1/index.html', 'Photos on real fig leaves, in a row',
     [], None, None),
    ('h2', 'concept-3', 'hero-ideas/h2/index.html', 'Arched photos on a fig leaf',
     [], None, None),
    ('h3', 'concept-3', 'hero-ideas/h3/index.html', 'Panorama between two leaves',
     [], None, None),
]

SKIP = ('#', 'http:', 'https:', '//', 'tel:', 'mailto:', 'data:', 'javascript:')


def read(path):
    with open(os.path.join(REPO, path), encoding='utf-8') as f:
        return f.read()


def write(path, text):
    full = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


def rel(url, src_dir, out_dir):
    """A URL written in a file in src_dir, as seen from a file in out_dir."""
    if not url or url.startswith(SKIP):
        return url
    path, sep, tail = _split(url)
    target = posixpath.normpath(posixpath.join(src_dir, path))
    out = posixpath.relpath(target, out_dir)
    if path.endswith('/') and not out.endswith('/'):
        out += '/'
    return out + sep + tail


def _split(url):
    m = re.match(r'([^?#]*)([?#]?)(.*)', url)
    return m.group(1), m.group(2), m.group(3)


def rebase(html, src_dir, out_dir):
    """Rewrite every relative href/src/srcset/url() from src_dir to out_dir."""
    def attr(m):
        return m.group(1) + rel(m.group(2), src_dir, out_dir) + '"'

    def srcset(m):
        parts = []
        for item in m.group(2).split(','):
            bits = item.strip().split(' ', 1)
            bits[0] = rel(bits[0], src_dir, out_dir)
            parts.append(' '.join(bits))
        return m.group(1) + ', '.join(parts) + '"'

    html = re.sub(r'(\s(?:href|src|action|poster)=")([^"]*)"', attr, html)
    html = re.sub(r'(\ssrcset=")([^"]*)"', srcset, html)
    html = re.sub(r'(url\(["\']?)([^"\')]+)', lambda m: m.group(1) + rel(m.group(2), src_dir, out_dir), html)
    return html


def hero_section(html):
    """The page's hero <section>: the first <section> inside <main>."""
    start = html.index('<section', html.index('<main'))
    # back up over the comment block that describes the hero, if there is one
    comment = html.rfind('<!--', 0, start)
    if comment != -1 and html.rfind('-->', comment, start) != -1 and not html[html.rfind('-->', comment, start) + 3:start].strip():
        start = comment
        start = html.rfind('\n', 0, start) + 1
    depth, i = 0, html.index('<section', html.index('<main'))
    for m in re.finditer(r'<(/?)section\b', html[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            end = i + m.end() + html[i + m.end():].index('>') + 1
            return start, end
    raise ValueError('no closing </section>')


# --- hero-only stylesheets for concepts 5 and 6 ---------------------------

def build_hero_css():
    css5 = read('concept-5/concept.css')
    root = css5[css5.index(':root {'):css5.index('}', css5.index(':root {')) + 1]
    hero = css5[css5.index('/* --- hero ----'):css5.index('/* --- homepage sections')]
    black = css5[css5.index('.d-hero { background: var(--c5-black); }'):]
    black = black[:black.index('\n', black.index('.d-hero :focus-visible')) + 1]
    cursor = css5[css5.index('/* --- the mouse pointer'):]
    cursor = (cursor.replace('body.c5 a,', '.d-hero a,')
                    .replace('body.c5 button,', '.d-hero button,')
                    .replace('  body.c5 summary,\n', '')
                    .replace('  body.c5 label,\n', '')
                    .replace('body.c5 [role="button"]', '.d-hero [role="button"]')
                    .replace('body.c5 input,\n  body.c5 textarea', '.d-hero input')
                    .replace('body.c5 {', '.d-hero {'))
    out = ('/* Concept 5\'s hero on its own (built from concept-5/concept.css by\n'
           '   homepages/build.py; edit that file, not this one). The black hero,\n'
           '   the leaf that points at the cursor and the leaf mouse pointer, here\n'
           '   kept to the hero so the rest of the homepage is unchanged. */\n\n'
           + root + '\n\n' + hero + '/* black hero */\n' + black + '\n' + cursor)
    write('homepages/shared/hero-5.css', rebase(out, 'concept-5', 'homepages/shared'))

    css6 = read('concept-6/concept.css')
    out = ('/* Concept 6\'s hero (built from concept-6/concept.css by\n'
           '   homepages/build.py; edit that file, not this one). */\n\n' + css6)
    write('homepages/shared/hero-6.css', rebase(out, 'concept-6', 'homepages/shared'))


# --- one page per hero -----------------------------------------------------

def review_bar(code, current_out):
    names = []
    for c, home, _src, name, *_ in HEROES:
        names.append((c, home, name))
    i = [c for c, *_ in names].index(code)
    prev_c, next_c = names[i - 1][0], names[(i + 1) % len(names)][0]
    home = names[i][1]
    label = f'Hero {code.upper()}'
    title = f'{names[i][2]}, on {HOMEPAGE_NAMES[home].lower()}'
    items = []
    for c, h, n in names:
        cur = ' aria-current="page"' if c == code else ''
        data = f'{n}, on {HOMEPAGE_NAMES[h].lower()}'
        items.append(f'<li><a class="review-bar__link" href="../{c}/" data-name="{data}"{cur}>'
                     f'<span class="visually-hidden">Hero </span>{c.upper()}'
                     f'<span class="visually-hidden">: {data}</span></a></li>')
    return (f'<nav class="review-bar" aria-label="Hero concepts on full homepages">\n'
            f'    <p class="review-bar__title"><span class="review-bar__label">{label}</span> '
            f'<span class="review-bar__name">{title}</span></p>\n'
            f'    <div class="review-bar__controls">\n'
            f'      <ul class="review-bar__list review-bar__list--codes">\n        '
            + '\n        '.join(items) + '</ul>\n'
            f'      <a class="review-bar__step review-bar__step--prev" href="../{prev_c}/" rel="prev" aria-label="Previous hero">'
            f'<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'      <a class="review-bar__step" href="../{next_c}/" rel="next" aria-label="Next hero">'
            f'<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'    </div>\n  </nav>')


def build_page(code, home, src, name, css, css_pos, js):
    out_dir = f'homepages/{code}'
    page = read(f'{home}/index.html')
    hero_src = read(src)
    src_dir = posixpath.dirname(src)

    # 1. swap the hero section (the homepage's own rules stay untouched)
    a, b = hero_section(page)
    ha, hb = hero_section(hero_src)
    new_hero = hero_src[ha:hb]
    if src_dir != home:  # the hero was written for another folder
        new_hero = rebase(new_hero, src_dir, home)
    page = page[:a] + new_hero + page[b:]

    # 2. icons the hero needs that the homepage's sprite lacks
    for sym in re.findall(r'<symbol id="([^"]+)"', hero_src):
        if f'<symbol id="{sym}"' not in page:
            m = re.search(r'<symbol id="%s".*?</symbol>' % re.escape(sym), hero_src, re.S)
            page = page.replace('</defs>', m.group(0) + '</defs>', 1) if '</defs>' in page \
                else page.replace('<symbol ', m.group(0) + '\n    <symbol ', 1)

    # 3. the review bar steps through the heroes instead of the concepts
    rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
    page = page[:rb.start()] + '<!--REVIEW-BAR-->' + page[rb.end():]
    page = re.sub(r'<title>[^<]*</title>',
                  f'<title>Hero {code.upper()} on {HOMEPAGE_NAMES[home].lower()} · The Fig Leaf Agency</title>',
                  page, count=1)
    if 'name="robots"' not in page:
        page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)

    # 4. everything now points from homepages/<code>/ back to the homepage folder
    page = rebase(page, home, out_dir)
    page = page.replace('<!--REVIEW-BAR-->', review_bar(code, out_dir))

    # 5. the hero's stylesheet and script
    links = ''.join(f'\n  <link rel="stylesheet" href="{posixpath.relpath(c, out_dir)}">' for c in css)
    bar = f'\n  <link rel="stylesheet" href="{posixpath.relpath("homepages/shared/homepages.css", out_dir)}">'
    if css_pos == 'after-styles':
        page = re.sub(r'(<link rel="stylesheet" href="[^"]*/styles\.css">)', lambda m: m.group(1) + links, page, count=1)
    elif css_pos == 'last':
        last = list(re.finditer(r'<link rel="stylesheet"[^>]*>', page))[-1]
        page = page[:last.end()] + links + page[last.end():]
    last = list(re.finditer(r'<link rel="stylesheet"[^>]*>', page))[-1]
    page = page[:last.end()] + bar + page[last.end():]
    if js:
        tags = '\n  '.join(f'<script src="{posixpath.relpath(j, out_dir)}"></script>' for j in js)
        page = re.sub(r'<script src="[^"]*/scene\.js"></script>', tags, page, count=1)

    page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                        f'{HOMEPAGE_NAMES[home].lower()} ({home}) with hero {code.upper()} from {src}. '
                        'Edit those, then re-run the script. -->', 1)
    write(f'{out_dir}/index.html', page)


def main():
    build_hero_css()
    for h in HEROES:
        build_page(*h)
    print('built', len(HEROES), 'pages')


if __name__ == '__main__':
    main()

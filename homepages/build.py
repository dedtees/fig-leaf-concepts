"""Builds concept-7 to concept-18: every new hero on a full homepage.

Each page (concepts 7 to 18) is one of the current homepages (concept 1, 2 or 3) exactly as it
is, header, colours, sections and footer, with only the hero <section>
swapped for one of the new hero concepts. Nothing is copied: the page links
back to its homepage's folder for CSS, scripts, images and inner pages, and
to the hero's own folder for the hero's pictures, CSS and script.

It also keeps the concepts review bar on concepts 1 to 6 listing 1 to 18.

Re-run after changing a homepage or a hero:  python3 homepages/build.py
"""
import os
import posixpath
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# The concepts that already have their own folder, for the review bar.
CONCEPTS = [
    (1, 'Stacked leaves, dark header'),
    (2, 'Stacked leaves, transparent header'),
    (3, 'Horizontal leaves, concept 1 reviews'),
    (4, 'Fig leaf photo gallery'),
    (5, 'Daylight: black hero, pointing fig leaf'),
    (6, 'Leaf slideshow: photos slide inside a big fig leaf'),
]

# The hero homepages carry on the numbering from 7, grouped by homepage:
# (concept number, homepage, page the hero comes from, name,
#  extra CSS (repo paths), where it goes, hero script(s) in place of scene.js)
X_CSS = ['hero-concepts/shared/hero-x.css']
X_JS = ['hero-concepts/shared/hero-x.js']
HEROES = [
    (7, 'concept-1', 'concept-5/index.html', "concept 5's pointing fig leaf hero",
     ['homepages/shared/hero-5.css'], 'last', ['concept-5/concept.js']),
    (8, 'concept-1', 'hero-ideas/v1/index.html', 'photos on real fig leaves, stacked (V1)',
     [], None, None),
    (9, 'concept-1', 'hero-ideas/v2/index.html', 'photo panels on a fig leaf (V2)',
     [], None, None),
    (10, 'concept-1', 'hero-ideas/v3/index.html', 'logo leaf window, three bands (V3)',
     [], None, None),
    (11, 'concept-2', 'hero-concepts/a/index.html', 'opening photo panels (A)',
     X_CSS, 'after-styles', X_JS),
    (12, 'concept-2', 'hero-concepts/b/index.html', 'stacked photo bands (B)',
     X_CSS, 'after-styles', X_JS),
    (13, 'concept-2', 'hero-concepts/c/index.html', 'uncover lens (C)',
     X_CSS, 'after-styles', X_JS),
    (14, 'concept-2', 'hero-concepts/d/index.html', 'card deck (D)',
     X_CSS, 'after-styles', X_JS),
    (15, 'concept-3', 'concept-6/index.html', "concept 6's leaf slideshow hero",
     ['homepages/shared/hero-6.css'], 'last', ['concept-6/concept.js']),
    (16, 'concept-3', 'hero-ideas/h1/index.html', 'photos on real fig leaves, in a row (H1)',
     [], None, None),
    (17, 'concept-3', 'hero-ideas/h2/index.html', 'arched photos on a fig leaf (H2)',
     [], None, None),
    (18, 'concept-3', 'hero-ideas/h3/index.html', 'panorama between two leaves (H3)',
     [], None, None),
]


def hero_title(n, home, name):
    """Concept 7: 'Concept 1 homepage, concept 5's pointing fig leaf hero'."""
    return f'Concept {home.split("-")[1]} homepage, {name[0].lower() + name[1:]}'


# Concepts 1 to 4 are archived: still online (7 to 18 are built on the
# homepages of 1 to 3), but out of the main sequence and its arrows.
ARCHIVED = {1, 2, 3, 4}


def all_concepts():
    return CONCEPTS + [(n, hero_title(n, home, name)) for n, home, _s, name, *_ in HEROES]


def sequence(n):
    """The run of concepts the bar on concept n steps through."""
    return [c for c in all_concepts() if (c[0] in ARCHIVED) == (n in ARCHIVED)]


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

def review_bar(n, out_dir):
    """The concepts review bar for the homepage of concept n: 5 to 18, or
    for an archived concept, the archive (1 to 4)."""
    seq = sequence(n)
    nums = [c for c, _ in seq]
    i = nums.index(n)
    href = lambda c: posixpath.relpath(f'concept-{c}/', out_dir) + '/'
    items = []
    for c, name in seq:
        cur = ' aria-current="page"' if c == n else ''
        items.append(f'<li><a class="review-bar__link" href="{href(c)}" data-name="{name}"{cur}>'
                     f'<span class="visually-hidden">Concept </span>{c}'
                     f'<span class="visually-hidden">: {name}</span></a></li>')
    label = f'Archived concept {n}' if n in ARCHIVED else f'Concept {n}'
    long = ' review-bar__list--long' if len(seq) > 8 else ''
    extra = (f' · <a href="{posixpath.relpath("concept-5/", out_dir)}/" style="color:inherit">back to the current concepts</a>'
             if n in ARCHIVED else '')
    return (f'<nav class="review-bar" aria-label="{"Archived concepts" if n in ARCHIVED else "Concepts"}">\n'
            f'    <p class="review-bar__title"><span class="review-bar__label">{label}</span> '
            f'<span class="review-bar__name">{seq[i][1]}{extra}</span></p>\n'
            f'    <div class="review-bar__controls">\n'
            f'      <ul class="review-bar__list{long}">\n        '
            + '\n        '.join(items) + '</ul>\n'
            f'      <a class="review-bar__step review-bar__step--prev" href="{href(nums[i - 1])}" rel="prev" aria-label="Previous concept">'
            f'<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'      <a class="review-bar__step" href="{href(nums[(i + 1) % len(nums)])}" rel="next" aria-label="Next concept">'
            f'<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'    </div>\n  </nav>')


def update_concept_bars():
    """Concepts 5 and 6 list 7 to 18 too, and 1 to 4 list the archive."""
    for n, _name in CONCEPTS:
        path = f'concept-{n}/index.html'
        page = read(path)
        rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
        write(path, page[:rb.start()] + review_bar(n, f'concept-{n}') + page[rb.end():])


def build_page(n, home, src, name, css, css_pos, js):
    out_dir = f'concept-{n}'
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
    page = re.sub(r'<title>Concept \d+ ·', f'<title>Concept {n} ·', page, count=1)
    if 'name="robots"' not in page:
        page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)

    # 4. everything now points from concept-<n>/ back to the homepage folder
    page = rebase(page, home, out_dir)
    page = page.replace('<!--REVIEW-BAR-->', review_bar(n, out_dir))

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
                        f'concept {n}: {home} homepage with the hero from {src}. '
                        'Edit those, then re-run the script. -->', 1)
    write(f'{out_dir}/index.html', page)


def main():
    build_hero_css()
    for h in HEROES:
        build_page(*h)
    update_concept_bars()
    print('built', len(HEROES), 'pages')


if __name__ == '__main__':
    main()

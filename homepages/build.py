"""Builds concept-3 to concept-12: every new hero on a full homepage.

Each page (concepts 3 to 12) is one of the archived homepages (archive A, B
or C) exactly as it is, header, colours, sections and footer, with only the
hero <section> swapped for one of the new hero concepts. Nothing is copied:
the page links back to its homepage's folder for CSS, scripts and images,
and to the hero's own folder for the hero's pictures, CSS and script. Each
also gets its own copy of the quote and Homeowners pages.

It also keeps the review bar on concepts 1 and 2 listing 1 to 12, and the
bar on archives A to D listing the archive.

Re-run after changing a homepage or a hero:  python3 homepages/build.py
"""
import os
import posixpath
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# Pages that have their own folder: (key, folder, name). Keys 1, 2, ... are
# the main run; letters are the archive.
CONCEPTS = [
    ('A', 'archive-a', 'Stacked leaves, dark header'),
    ('B', 'archive-b', 'Stacked leaves, transparent header'),
    ('C', 'archive-c', 'Horizontal leaves, archive A reviews'),
    ('D', 'archive-d', 'Fig leaf photo gallery'),
    (1, 'concept-1', 'Daylight: black hero, pointing fig leaf'),
    (2, 'concept-2', 'Leaf slideshow: photos slide inside a big fig leaf'),
]

# The hero homepages carry on the numbering from 3, grouped by homepage:
# (concept number, homepage, page the hero comes from, name,
#  extra CSS (repo paths), where it goes, hero script(s) in place of scene.js)
X_CSS = ['hero-concepts/shared/hero-x.css']
X_JS = ['hero-concepts/shared/hero-x.js']
HEROES = [
    (3, 'archive-a', 'concept-1/index.html', "concept 1's pointing fig leaf hero",
     ['homepages/shared/hero-5.css'], 'last', ['concept-1/concept.js']),
    (4, 'archive-a', 'hero-ideas/v1/index.html', 'photos on real fig leaves, stacked (V1)',
     [], None, None),
    (5, 'archive-a', 'hero-ideas/v2/index.html', 'photo panels on a fig leaf (V2)',
     [], None, None),
    (6, 'archive-a', 'hero-ideas/v3/index.html', 'logo leaf window, three bands (V3)',
     [], None, None),
    (7, 'archive-b', 'hero-concepts/a/index.html', 'opening photo panels (A)',
     X_CSS, 'after-styles', X_JS),
    (8, 'archive-b', 'hero-concepts/b/index.html', 'stacked photo bands (B)',
     X_CSS, 'after-styles', X_JS),
    (9, 'archive-b', 'hero-concepts/c/index.html', 'uncover lens (C)',
     X_CSS, 'after-styles', X_JS),
    (10, 'archive-b', 'hero-concepts/d/index.html', 'card deck (D)',
     X_CSS, 'after-styles', X_JS),
    (11, 'archive-c', 'concept-2/index.html', "concept 2's leaf slideshow hero",
     ['homepages/shared/hero-6.css'], 'last', ['concept-2/concept.js']),
    (12, 'archive-c', 'hero-ideas/h1/index.html', 'photos on real fig leaves, in a row (H1)',
     [], None, None),
]


def hero_title(n, home, name):
    """Concept 3: 'Archive A homepage, concept 1's pointing fig leaf hero'."""
    return f'Archive {home[-1].upper()} homepage, {name[0].lower() + name[1:]}'


def archived(key):
    return isinstance(key, str)


def folder(key):
    return f'archive-{key.lower()}' if archived(key) else f'concept-{key}'


def label(key):
    return f'Archive {key}' if archived(key) else f'Concept {key}'


def all_concepts():
    return ([(k, name) for k, _f, name in CONCEPTS]
            + [(n, hero_title(n, home, name)) for n, home, _s, name, *_ in HEROES])


def sequence(key):
    """The run of pages the bar on key steps through: the main run or the archive."""
    return [c for c in all_concepts() if archived(c[0]) == archived(key)]


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
    if KEEP_IN is not None:
        target = keep_in(target, KEEP_IN)
    out = posixpath.relpath(target, out_dir)
    if path.endswith('/') and not out.endswith('/'):
        out += '/'
    return out + sep + tail


# Concepts 3 to 12 get their own copies of these pages, so a visitor who
# clicks through from concept 3 stays in concept 3.
SUBPAGES = ('crq', 'crq-form', 'homeowners-insurance')
KEEP_IN = None   # while building concept n: 'concept-<n>'


def keep_in(target, folder):
    """Point a concept's homepage or quote / Homeowners pages at folder's copy."""
    m = re.match(r'(?:concept-\d+|archive-[a-d])(?:/(%s))?(/index\.html)?$' % '|'.join(SUBPAGES), target)
    if m:
        return folder + ('/' + m.group(1) if m.group(1) else '') + (m.group(2) or '')
    return target


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


# --- hero-only stylesheets for concepts 1 and 2 (files keep their old names) ---------------------------

def build_hero_css():
    css5 = read('concept-1/concept.css')
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
    out = ('/* Concept 1\'s hero on its own (built from concept-1/concept.css by\n'
           '   homepages/build.py; edit that file, not this one). The black hero,\n'
           '   the leaf that points at the cursor and the leaf mouse pointer, here\n'
           '   kept to the hero so the rest of the homepage is unchanged. */\n\n'
           + root + '\n\n' + hero + '/* black hero */\n' + black + '\n' + cursor)
    write('homepages/shared/hero-5.css', rebase(out, 'concept-1', 'homepages/shared'))

    css6 = read('concept-2/concept.css')
    out = ('/* Concept 2\'s hero (built from concept-2/concept.css by\n'
           '   homepages/build.py; edit that file, not this one). */\n\n' + css6)
    write('homepages/shared/hero-6.css', rebase(out, 'concept-2', 'homepages/shared'))


# --- one page per hero -----------------------------------------------------

def review_bar(n, out_dir):
    """The review bar for page n: the main run (1 to 12), or for an archived
    page, the archive (A to D)."""
    seq = sequence(n)
    keys = [c for c, _ in seq]
    i = keys.index(n)
    href = lambda c: posixpath.relpath(folder(c) + '/', out_dir) + '/'
    items = []
    for c, name in seq:
        cur = ' aria-current="page"' if c == n else ''
        word = 'Archive ' if archived(c) else 'Concept '
        items.append(f'<li><a class="review-bar__link" href="{href(c)}" data-name="{name}"{cur}>'
                     f'<span class="visually-hidden">{word}</span>{c}'
                     f'<span class="visually-hidden">: {name}</span></a></li>')
    long = ' review-bar__list--long' if len(seq) > 8 else ''
    extra = (f' · <a href="{posixpath.relpath("concept-1/", out_dir)}/" style="color:inherit">back to the current concepts</a>'
             if archived(n) else '')
    return (f'<nav class="review-bar" aria-label="{"Archived concepts" if archived(n) else "Concepts"}">\n'
            f'    <p class="review-bar__title"><span class="review-bar__label">{label(n)}</span> '
            f'<span class="review-bar__name">{seq[i][1]}{extra}</span></p>\n'
            f'    <div class="review-bar__controls">\n'
            f'      <ul class="review-bar__list{long}">\n        '
            + '\n        '.join(items) + '</ul>\n'
            f'      <a class="review-bar__step review-bar__step--prev" href="{href(keys[i - 1])}" rel="prev" aria-label="Previous concept">'
            f'<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'      <a class="review-bar__step" href="{href(keys[(i + 1) % len(keys)])}" rel="next" aria-label="Next concept">'
            f'<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'    </div>\n  </nav>')


def update_concept_bars():
    """Concepts 1 and 2 list 1 to 12, and archives A to D list the archive."""
    for key, path, _name in CONCEPTS:
        page = read(f'{path}/index.html')
        rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
        page = page[:rb.start()] + review_bar(key, path) + page[rb.end():]
        page = re.sub(r'<title>(Concept|Archive) \w+ ·', f'<title>{label(key)} ·', page, count=1)
        write(f'{path}/index.html', page)


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
    page = re.sub(r'<title>(?:Concept|Archive) \w+ ·', f'<title>Concept {n} ·', page, count=1)
    if 'name="robots"' not in page:
        page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)

    # 4. everything now points from concept-<n>/ back to the homepage folder
    global KEEP_IN
    KEEP_IN = out_dir
    page = rebase(page, home, out_dir)
    KEEP_IN = None
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

    if n in EXTRAS:
        page = EXTRAS[n](page, out_dir)

    page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                        f'concept {n}: {home} homepage with the hero from {src}. '
                        'Edit those, then re-run the script. -->', 1)
    write(f'{out_dir}/index.html', page)


# --- changes for one concept only ------------------------------------------

def business_card(page, out_dir):
    """Concept 3: a Business insurance card first under "More Ways We
    Protect You", with the cards three across."""
    img = posixpath.relpath('homepages/shared/assets/business-insurance.jpg', out_dir)
    card = (
        '<article class="hs-service hs-reveal">\n'
        f'            <div class="hs-service__media"><img class="hs-service__img" src="{img}" alt="" width="900" height="600" loading="lazy" decoding="async"></div>\n'
        '            <div class="hs-service__body">\n'
        '              <h3 class="hs-line__title">Business Insurance</h3>\n'
        '              <p>Protection for New Jersey shops, offices and service businesses, from general liability and commercial auto to workers comp and employee benefits.</p>\n'
        '              <a class="hs-more" href="https://figleafagency.com/business-insurance/">Learn more<span class="visually-hidden"> about business insurance</span></a>\n'
        '            </div>\n'
        '          </article>\n          ')
    grid = '<div class="hs-services__grid">\n          '
    assert grid in page
    page = page.replace(grid, '<div class="hs-services__grid hs-services__grid--3">\n          ' + card, 1)
    page = page.replace('Beyond your everyday policies, we help contractors stay covered on the job and drivers keep their records and premiums down.',
                        'Beyond your everyday policies, we protect local businesses, help contractors stay covered on the job, and help drivers keep their records and premiums down.', 1)
    return page


EXTRAS = {3: business_card}


def build_subpages(n, home):
    """concept-<n>/crq, crq-form and homeowners-insurance: the homepage's own
    pages, content unchanged, with links kept inside concept n."""
    global KEEP_IN
    for sub in SUBPAGES:
        src = f'{home}/{sub}'
        out = f'concept-{n}/{sub}'
        page = read(f'{src}/index.html')
        rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
        name = re.search(r'review-bar__name">(.*?)</span></p>', rb.group(0), re.S).group(1)
        name = re.sub(r'(Concept|Archive) \w+ look(, [a-z]+(?: [a-z]+)*)?', 'Homeowners page', name)
        bar = ('<nav class="review-bar" aria-label="Concepts">\n'
               f'    <p class="review-bar__title"><span class="review-bar__label">Concept {n}</span> '
               f'<span class="review-bar__name">{name}</span></p>\n'
               # an empty "long" list: on phones the bar then shows its name
               '    <div class="review-bar__controls"><ul class="review-bar__list review-bar__list--long"></ul></div>\n  </nav>')
        page = page[:rb.start()] + bar + page[rb.end():]
        page = re.sub(r'<title>(?:Concept|Archive) \w+ ·', f'<title>Concept {n} ·', page, count=1)
        KEEP_IN = f'concept-{n}'
        page = rebase(page, src, out)
        KEEP_IN = None
        page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                            f'concept {n}\'s copy of {src}/. Edit that page, then re-run the script. -->', 1)
        write(f'{out}/index.html', page)


def main():
    build_hero_css()
    for h in HEROES:
        build_page(*h)
        build_subpages(h[0], h[1])
    update_concept_bars()
    print('built', len(HEROES), 'pages')


if __name__ == '__main__':
    main()

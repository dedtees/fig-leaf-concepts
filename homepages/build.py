"""Builds concept-2 to concept-10: every new hero on a full homepage.

Each page (concepts 2 to 10) is one of the archived homepages (archive A, B
or C) exactly as it is, header, colours, sections and footer, with only the
hero <section> swapped for one of the new hero concepts. Nothing is copied:
the page links back to its homepage's folder for CSS, scripts and images,
and to the hero's own folder for the hero's pictures, CSS and script. Each
also gets its own copy of the quote and Homeowners pages.

It also keeps the review bar on concepts 1 and 2 listing 1 to 11, and the
bar on archives A to D listing the archive.

Re-run after changing a homepage or a hero:  python3 homepages/build.py
"""
import os
import posixpath
import re

import service_pages as SP

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# Pages that have their own folder: (key, folder, name). Keys 1, 2, ... are
# the main run; letters are the archive.
CONCEPTS = [
    ('A', 'archive-a', 'Stacked leaves, dark header'),
    ('B', 'archive-b', 'Stacked leaves, transparent header'),
    ('C', 'archive-c', 'Horizontal leaves, archive A reviews'),
    ('D', 'archive-d', 'Fig leaf photo gallery'),
    ('E', 'archive-e', 'Daylight: black hero, pointing fig leaf'),
    (1, 'concept-1', 'Leaf slideshow: photos slide inside a big fig leaf'),
]

# The hero homepages carry on the numbering from 2, grouped by homepage:
# (concept number, homepage, page the hero comes from, name,
#  extra CSS (repo paths), where it goes, hero script(s) in place of scene.js)
X_CSS = ['hero-concepts/shared/hero-x.css']
X_JS = ['hero-concepts/shared/hero-x.js']
HEROES = [
    (2, 'archive-a', 'archive-e/index.html', "archive E's pointing fig leaf hero",
     ['homepages/shared/hero-5.css'], 'last', ['archive-e/concept.js']),
    (3, 'archive-a', 'hero-ideas/v1/index.html', 'photos on real fig leaves, stacked (V1)',
     [], None, None),
    (4, 'archive-a', 'hero-ideas/v3/index.html', 'logo leaf window, three bands (V3)',
     [], None, None),
    (5, 'archive-b', 'hero-concepts/a/index.html', 'opening photo panels (A)',
     X_CSS, 'after-styles', X_JS),
    (6, 'archive-b', 'hero-concepts/b/index.html', 'stacked photo bands (B)',
     X_CSS, 'after-styles', X_JS),
    (7, 'archive-b', 'hero-concepts/c/index.html', 'uncover lens (C)',
     X_CSS, 'after-styles', X_JS),
    (8, 'archive-b', 'hero-concepts/d/index.html', 'card deck (D)',
     X_CSS, 'after-styles', X_JS),
    (9, 'archive-c', 'concept-1/index.html', "concept 1's leaf slideshow hero",
     ['homepages/shared/hero-6.css'], 'last', ['concept-1/concept.js']),
    (10, 'archive-c', 'hero-ideas/h1/index.html', 'photos on real fig leaves, in a row (H1)',
     [], None, None),
    # concept 11: built from the client review (see concept_11 below)
    (11, 'archive-a', 'hero-concepts/a/index.html', "Client picks: concept 5's photo panels with Business, on concept 2's page",
     X_CSS, 'after-styles', X_JS + ['homepages/shared/concept-11.js']),
]


OWN_TITLE = {11}   # named in full, not 'Archive X homepage, ...'


def hero_title(n, home, name):
    """Concept 3: 'Archive A homepage, concept 1's pointing fig leaf hero'."""
    if n in OWN_TITLE:
        return name
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


# Concepts 2 to 10 get their own copies of these pages, so a visitor who
# clicks through from concept 2 stays in concept 2.
SUBPAGES = ('crq', 'crq-form', 'homeowners-insurance')
KEEP_IN = None   # while building concept n: 'concept-<n>'


def keep_in(target, folder):
    """Point a concept's homepage or quote / Homeowners pages at folder's copy."""
    # (archive B's Homeowners variants, -fade and -scroll, map to the one page)
    m = re.match(r'(?:concept-\d+|archive-[a-d])(?:/(%s)(?:-fade|-scroll)?)?(/index\.html)?$' % '|'.join(SUBPAGES), target)
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


# --- hero-only stylesheets for archive E and concept 1 (files keep their old names) ---------------------------

def build_hero_css():
    css5 = read('archive-e/concept.css')
    root = css5[css5.index(':root {'):css5.index('}', css5.index(':root {')) + 1]
    hero = css5[css5.index('/* --- hero ----'):css5.index('/* --- homepage sections')]
    black = css5[css5.index('.d-hero { background: var(--c5-black); }'):]
    black = black[:black.index('\n', black.index('.d-hero :focus-visible')) + 1]
    out = ('/* Archive E\'s hero on its own (built from archive-e/concept.css by\n'
           '   homepages/build.py; edit that file, not this one). The black hero,\n'
           '   and the leaf that points at the cursor, here\n'
           '   kept to the hero so the rest of the homepage is unchanged. */\n\n'
           + root + '\n\n' + hero + '/* black hero */\n' + black)
    write('homepages/shared/hero-5.css', rebase(out, 'archive-e', 'homepages/shared'))

    css6 = read('concept-1/concept.css')
    out = ('/* Concept 1\'s hero (built from concept-1/concept.css by\n'
           '   homepages/build.py; edit that file, not this one). */\n\n' + css6)
    write('homepages/shared/hero-6.css', rebase(out, 'concept-1', 'homepages/shared'))


# --- one page per hero -----------------------------------------------------

def review_bar(n, out_dir):
    """The review bar for page n: the main run (1 to 11), or for an archived
    page, the archive (A to E)."""
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
    # everything on this bar is archived now: the current build is build-1 to build-5
    extra = f' · archived · <a href="{posixpath.relpath("build-1/", out_dir)}/" style="color:inherit">see the current build</a>'
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
    """Concept 1 lists 1 to 11, and archives A to D list the archive."""
    for key, path, _name in CONCEPTS:
        page = read(f'{path}/index.html')
        rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
        page = page[:rb.start()] + review_bar(key, path) + page[rb.end():]
        page = re.sub(r'<title>(Concept|Archive) \w+ ·', f'<title>{label(key)} ·', page, count=1)
        write(f'{path}/index.html', page)


def build_page(n, home, src, name, css, css_pos, js, out_dir=None):
    out_dir = out_dir or f'concept-{n}'
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

    # which hero this is, for hero-specific tweaks in homepages.css
    page = page.replace('<html ', f'<html data-hero="{posixpath.basename(src_dir)}" ', 1)

    if n in EXTRAS:
        page = EXTRAS[n](page, out_dir)

    page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                        f'concept {n}: {home} homepage with the hero from {src}. '
                        'Edit those, then re-run the script. -->', 1)
    write(f'{out_dir}/index.html', page)


# --- changes for one concept only ------------------------------------------

def business_card(page, out_dir):
    """Concept 2: a Business insurance card first under "More Ways We
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


def concept_11(page, out_dir):
    """Concept 11, from the client review of concepts 1 to 10: concept 2's
    page (the archive A homepage, header, sections and footer) with concept
    5's opening photo panels hero plus a fourth panel, Business; concept 2's
    three cards under "More Ways We Protect You"; concept 5's movement in the
    dark Comprehensive Coverage section (concept-11.css); and an About picture
    that starts on the old building, its sign now reading Fig Leaf, and fades
    to the team photo (concept-11.js)."""
    page = business_card(page, out_dir)
    up = lambda p: posixpath.relpath(p, out_dir)
    # its own rules load last, after homepages.css
    last = list(re.finditer(r'<link rel="stylesheet"[^>]*>', page))[-1]
    page = page[:last.end()] + f'\n  <link rel="stylesheet" href="{up("homepages/shared/concept-11.css")}">' + page[last.end():]

    # hero: "your business." in the headline and a fourth panel
    boat_word = '<span class="scene-word" data-scene="boat">your <em>boat.</em></span>'
    assert boat_word in page
    page = page.replace(boat_word, boat_word + '\n            <span class="scene-word" data-scene="business">your <em>business.</em></span>', 1)
    page = page.replace('<span class="visually-hidden">your car, your home and your boat.</span>',
                        '<span class="visually-hidden">your car, your home, your boat and your business.</span>', 1)
    page = page.replace('class="scene hx hx--panels" data-hx role="group" aria-label="A car on a mountain road at sunset, a house lit up at dusk and a boat on the water at sunset"',
                        'class="scene hx hx--panels" data-hx data-count="4" role="group" aria-label="A car on a mountain road at sunset, a house lit up at dusk, a boat on the water at sunset and a brick shopfront"', 1)
    panel = (
        '\n          <div class="hx__item" data-scene="business" data-lx="50" data-ly="40">\n'
        f'            <img class="hx__img" src="{up("hero-concepts/shared/business.jpg")}" alt="" decoding="async">\n'
        '            <span class="hx__tag" aria-hidden="true"><span class="hx__num">04</span><span class="hx__label">Business</span></span>\n'
        '            <button class="hx__hit" type="button" aria-pressed="false" aria-controls="hx-business"><span class="visually-hidden">Business insurance</span></button>\n'
        '            <div class="hx__body" id="hx-business">\n'
        '              <span class="hx__num" aria-hidden="true">04</span>\n'
        '              <p class="hx__title">Business insurance</p>\n'
        '              <p class="hx__text">Liability, property, commercial auto and workers comp for local businesses.</p>\n'
        '              <a class="hx__link" href="https://figleafagency.com/business-insurance/">See business coverage <span aria-hidden="true">&rarr;</span></a>\n'
        '            </div>\n'
        '            <span class="hx__bar" aria-hidden="true"></span>\n'
        '          </div>')
    m = re.search(r'<div class="hx__item" data-scene="boat".*?<span class="hx__bar" aria-hidden="true"></span>\n\s*</div>', page, re.S)
    page = page[:m.end()] + panel + page[m.end():]

    # Comprehensive Coverage: fig leaves drifting with the scroll
    cov = '<section class="fl-grid-host hs-section hs-coverage" aria-labelledby="hs-coverage-title">'
    assert cov in page
    page = page.replace(cov, cov + '\n      <div class="c11-leaves" aria-hidden="true">'
                        '<span class="c11-leaf c11-leaf--a" data-hs-px="0.35"></span>'
                        '<span class="c11-leaf c11-leaf--b" data-hs-px="-0.2"></span>'
                        '<span class="c11-leaf c11-leaf--c" data-hs-px="0.25"></span>'
                        '<span class="c11-leaf c11-leaf--d" data-hs-px="-0.35"></span></div>', 1)

    # the stats card straddles the hero and Comprehensive Coverage: it moves
    # to the top of the coverage section and reaches up into the hero
    # (concept-11.css), so the coverage section grows to hold it
    m = re.search(r'\n[ \t]*<section class="hs-statband".*?</section>\n', page, re.S)
    band = m.group(0)
    page = page[:m.start()] + '\n' + page[m.end():]
    leaves_end = page.index('</div>', page.index('<div class="c11-leaves"')) + len('</div>')
    page = page[:leaves_end] + band.replace('<section class="hs-statband"', '<div class="hs-statband c11-statband" role="group"', 1).replace('</section>', '</div>').rstrip('\n') + page[leaves_end:]

    # About: the old building (sign repainted to read Fig Leaf), then the team
    m = re.search(r'<div class="hs-about__media"><img class="hs-about__img"[^>]*></div>', page)
    team = re.search(r'<img [^>]*>', m.group(0)).group(0).replace('class="hs-about__img"', 'class="hs-about__img c11-fade__team"')
    b = 'homepages/shared/assets/old-building-figleaf'
    building = (f'<img class="hs-about__img c11-fade__building" src="{up(b + ".jpg")}" '
                f'srcset="{up(b + "-900.jpg")} 900w, {up(b + ".jpg")} 1800w" sizes="(max-width: 820px) 100vw, 50vw" '
                'alt="Painting of the agency\'s original office, its sign reading Fig Leaf Agency" width="1800" height="1396" loading="lazy" decoding="async">')
    tag = ('<span class="c11-fade__tag" aria-hidden="true"><span class="c11-fade__then">Where we started</span>'
           '<span class="c11-fade__now">Our team today</span></span>')
    page = page[:m.start()] + f'<div class="hs-about__media c11-fade">{building}{team}{tag}</div>' + page[m.end():]
    return page


EXTRAS = {2: business_card, 11: concept_11}


# The five Homeowners page layouts, in turn: concept 1 gets layout 1, 2 gets
# layout 2 and so on to 5, then 6 starts again on layout 1.
HOMEOWNERS = [
    ('archive-a/homeowners-insurance', 'archive A look'),
    ('archive-b/homeowners-insurance', 'archive B look, tabs'),
    ('archive-b/homeowners-insurance-scroll', 'archive B look, scrolling'),
    ('archive-b/homeowners-insurance-fade', 'archive B look, header fade'),
    ('archive-c/homeowners-insurance', 'archive C look'),
]


# concepts that don't take their turn: concept 11 uses concept 2's layout
HOMEOWNERS_PICK = {11: 1}


def homeowners_layout(n):
    return HOMEOWNERS_PICK.get(n, (n - 1) % len(HOMEOWNERS))


def main_run():
    return [c for c, _ in all_concepts() if not archived(c)]


def homeowners_bar(n, out_dir):
    """The bar on concept n's Homeowners page: concepts 1 to 11, each number
    opening that concept's Homeowners page, the arrows stepping through them."""
    keys = main_run()
    i = keys.index(n)
    href = lambda c: posixpath.relpath(f'concept-{c}/homeowners-insurance/', out_dir) + '/'
    items = []
    for c in keys:
        lay = homeowners_layout(c)
        name = f'Concept {c} Homeowners: layout {lay + 1}, {HOMEOWNERS[lay][1]}'
        cur = ' aria-current="page"' if c == n else ''
        items.append(f'<li><a class="review-bar__link" href="{href(c)}" data-name="{name}"{cur}>'
                     f'<span class="visually-hidden">Concept </span>{c}'
                     f'<span class="visually-hidden">: {name}</span></a></li>')
    lay = homeowners_layout(n)
    home = posixpath.relpath(f'concept-{n}/', out_dir) + '/'
    return ('<nav class="review-bar" aria-label="Concepts">\n'
            f'    <p class="review-bar__title"><span class="review-bar__label">Concept {n}</span> '
            f'<span class="review-bar__name">Homeowners layout {lay + 1} of {len(HOMEOWNERS)} · '
            f'<a href="{home}" style="color:inherit">back to the homepage</a></span></p>\n'
            '    <div class="review-bar__controls">\n'
            '      <ul class="review-bar__list review-bar__list--long">\n        '
            + '\n        '.join(items) + '</ul>\n'
            f'      <a class="review-bar__step review-bar__step--prev" href="{href(keys[i - 1])}" rel="prev" aria-label="Previous concept">'
            '<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'      <a class="review-bar__step" href="{href(keys[(i + 1) % len(keys)])}" rel="next" aria-label="Next concept">'
            '<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            '    </div>\n  </nav>')


def build_subpages(n, home):
    """concept-<n>/crq and crq-form: the homepage's own pages, and
    concept-<n>/homeowners-insurance: its Homeowners layout, content unchanged,
    with links kept inside concept n."""
    global KEEP_IN
    for sub in SUBPAGES:
        src = HOMEOWNERS[homeowners_layout(n)][0] if sub == 'homeowners-insurance' else f'{home}/{sub}'
        if sub != 'homeowners-insurance' and home.startswith('concept-'):
            continue  # concept 1 keeps its own quote pages
        out = f'concept-{n}/{sub}'
        page = read(f'{src}/index.html')
        rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
        if sub == 'homeowners-insurance':
            bar = '<!--REVIEW-BAR-->'
        else:
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
        page = page.replace('<!--REVIEW-BAR-->', homeowners_bar(n, out))
        page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                            f'concept {n}\'s copy of {src}/. Edit that page, then re-run the script. -->', 1)
        write(f'{out}/index.html', page)


def landing_bars():
    """Concept 1's quote pages are where visitors land (the root index opens
    concept-1/crq-form/), so their bar lists concepts 1 to 11 too, each
    number opening that concept's homepage."""
    for sub in ('crq', 'crq-form'):
        out = f'concept-1/{sub}'
        page = read(f'{out}/index.html')
        rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
        name = re.search(r'review-bar__name">(.*?)</span></p>', rb.group(0), re.S).group(1)
        bar = review_bar(1, out)
        bar = re.sub(r'(review-bar__name">).*?(</span></p>)', lambda m: m.group(1) + name + m.group(2), bar, count=1, flags=re.S)
        write(f'{out}/index.html', page[:rb.start()] + bar + page[rb.end():])


# --- the current build: concept 11, five ways ------------------------------
# The client kept concept 11. The main bar is now AC (the fig leaf photo
# gallery, archive D, which is also the landing page), GC (the get a quote
# page) and builds 1 to 5: concept 11's homepage, each with one of the five
# Homeowners layouts. Concepts 1 to 11 and archives A to E stay online as
# the archive.
BUILDS = [1, 2, 3, 4, 5]
GALLERY = 'archive-d'

# The four Homeowners versions from Eric's mockups (23 Nov), cut from the
# existing sections of archive B's scrolling page. Builds 1 to 4 show
# versions 1 to 4; build 5 shows version 1. The sources are made by
# build_homeowners_versions() below, from archive-b/homeowners-insurance-scroll.
HOMEOWNERS_VERSIONS = [
    ('archive-b/homeowners-insurance-v1', 'white hero, perils, what it covers, quote form'),
    ('archive-b/homeowners-insurance-v2', 'black hero, perils, what it covers, quote form'),
    ('archive-b/homeowners-insurance-v3', 'black hero, perils, what it covers, quote banner'),
    ('archive-b/homeowners-insurance-v4', 'black hero, perils, quote banner, what it covers, quote form'),
]


def homeowners_version(k):
    """The Homeowners version (1 to 4) build k shows."""
    return k if k <= len(HOMEOWNERS_VERSIONS) else 1


# The black "Get a homeowners quote" band (build 1's quote card, laid out
# full width) and the faint leaf outline behind the black hero's photo.
QUOTE_BAND = '''
    <section class="pg-band" id="{id}" aria-labelledby="pg-band-title">
      <div class="pg-wrap">
        <div class="pg-band__box">
          <div class="pg-band__text">
            <h2 class="pg-band__title" id="pg-band-title">{title}</h2>
            <p>We compare top-rated carriers for you, then walk you through every line of the policy.</p>
          </div>
          <div class="pg-band__actions">
            <a class="pg-btn pg-btn--gold" href="{href}">Start My Quote</a>
            <a class="pg-call" href="tel:+19088623447"><svg class="icon" aria-hidden="true"><use href="#i-phone"></use></svg>Call (908) 862-3447</a>
          </div>
        </div>
      </div>
    </section>
'''
def homeowners_pieces():
    """The scrolling Homeowners page cut into its parts: the page, where its
    <main> starts and ends, and the title band (hero), #quote (the form with
    the "Rather talk it through?" card), #overview (perils) and #covered
    (what it covers)."""
    src = 'archive-b/homeowners-insurance-scroll'
    page = read(f'{src}/index.html')
    main_start = page.index('<main id="main"')
    main_end = page.index('</main>')
    main = page[main_start:main_end]
    head_end = main.index('</header>') + len('</header>')
    hero = main[main.index('<!-- Title band -->'):head_end]
    q0 = main.index('<!-- Scrolling version')
    o0 = main.index('<section class="pg-sec" id="overview"')
    c0 = main.index('<section class="pg-sec" id="covered"')
    quote = main[main.index('<section class="pg-close"', q0):o0].rstrip() + '\n'
    overview = main[o0:c0].rstrip() + '\n'
    covered = main[c0:].rstrip() + '\n'
    return src, page, main_start, main_end, hero, overview, covered, quote


def version_layouts(hero, overview, covered, quote, band_title):
    """The four Homeowners versions' layouts, (main class, hero, sections),
    for any page cut into the same parts."""
    # the call-us card on its own, for the version with no form
    a0 = quote.index('<div class="pg-crq__card">')
    a1 = quote.index('<aside class="pg-crq__aside"')
    talk_only = quote[:a0] + quote[a1:]
    talk_only = talk_only.replace('id="quote" aria-labelledby="pg-close-title"', 'id="talk" aria-label="Rather talk it through?"', 1)
    talk_only = re.sub(r'\s*<div class="pg-sec__head">.*?</div>\n', '\n', talk_only, count=1, flags=re.S)
    talk_only = re.sub(r'\s*<!-- The quote form is.*?-->', '', talk_only, count=1, flags=re.S)
    dark = hero.replace('fl-grid fl-grid--light', 'fl-grid', 1)
    band = lambda id_, href: QUOTE_BAND.format(id=id_, href=href, title=band_title)
    return [
        ('pg--stack', hero, [overview, covered, quote]),
        ('pg--stack pg--fade', dark, [overview, covered, quote]),
        ('pg--stack pg--fade', dark, [overview, covered, band('quote', '../crq-form/'), talk_only]),
        ('pg--stack pg--fade', dark, [overview, band('quote-band', '#quote'), covered, quote]),
    ]


def assemble(page, main_start, main_end, cls, top, secs):
    body = ('<main id="main" class="hs pg pg--v2 ' + cls + '">\n\n    ' + top.strip() + '\n\n    '
            + '\n    '.join(s.strip() + '\n' for s in secs if s) + '\n  ')
    new = page[:main_start] + body + page[main_end:]
    return new.replace('<link rel="stylesheet" href="../palette.css">',
                       '<link rel="stylesheet" href="../palette.css">\n'
                       '  <link rel="stylesheet" href="../../homepages/shared/homeowners-versions.css">', 1)


def build_homeowners_versions():
    """archive-b/homeowners-insurance-v1 to -v4 from the scrolling page."""
    src, page, main_start, main_end, hero, overview, covered, quote = homeowners_pieces()
    for n, (cls, top, secs) in enumerate(version_layouts(hero, overview, covered, quote, 'Get a homeowners quote'), 1):
        out = HOMEOWNERS_VERSIONS[n - 1][0]
        new = assemble(page, main_start, main_end, cls, top, secs)
        new = new.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py (build_homeowners_versions): '
                          f'Homeowners version {n}, from {src}/. Edit that page or the script, then re-run it. -->', 1)
        write(f'{out}/index.html', new)


def service_version(n, s):
    """Personal insurance page s (homepages/service_pages.py) in Homeowners
    version n's layout. Returns the page and the folder its relative links
    are written from (the Homeowners version's, the same depth)."""
    src_dir = HOMEOWNERS_VERSIONS[n - 1][0]
    _, page, main_start, main_end, hero, overview, covered, quote = homeowners_pieces()
    up = lambda path: posixpath.relpath(path, src_dir)
    live = lambda slug: f'https://figleafagency.com/{slug}/'
    hero = SP.hero(s, up)
    article = 'an' if s['short'][0] in 'aeiou' else 'a'
    layouts = version_layouts(hero, SP.overview(s, up), SP.covered(s, up, live), SP.quote(s, quote, up),
                              f'Get {article} {s["short"]} quote')
    cls, top, secs = layouts[n - 1]
    if s.get('contact') and n == 3:
        # version 3's quote band sends people to the Consumer Rate Quotes
        # page, which doesn't cover this page: the contact form (with its
        # call-us card) takes the band's place
        secs = [x for x in secs if 'id="talk"' not in x and 'class="pg-band"' not in x] + [SP.quote(s, quote, up)]
    cls += ' pg--service' + (' pg--draft' if s['draft'] else '')
    new = assemble(page, main_start, main_end, cls, top, secs)
    new = new.replace('  <link rel="stylesheet" href="../../homepages/shared/homeowners-versions.css">',
                      '  <link rel="stylesheet" href="../../homepages/shared/homeowners-versions.css">\n'
                      '  <link rel="stylesheet" href="../../homepages/shared/service-pages.css">', 1)
    # the extra icons, in the page's sprite
    syms = ''.join(f'\n    <symbol id="{i}" viewBox="0 0 24 24">{d}</symbol>' for i, d in SP.ICONS.items())
    m = re.search(r'<symbol id="i-liability".*?</symbol>', new)
    new = new[:m.end()] + syms + new[m.end():]
    # head: title, description, canonical, Open Graph and the breadcrumb
    name, slug = s['name'], s['slug']
    new = re.sub(r'<title>[^<]*</title>', f'<title>Archive B · {name} in New Jersey | The Fig Leaf Agency</title>', new, count=1)
    new = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + s['meta'], new, count=1)
    new = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + f'{name} | The Fig Leaf Agency', new, count=1)
    new = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + s['og'], new, count=1)
    h = new.index('</head>')   # canonical, og:url and the breadcrumb, in the head only
    head = new[:h].replace('https://figleafagency.com/homeowners-insurance/"', live(slug) + '"')
    head = head.replace('"name": "Homeowners Insurance", "item": "' + live(slug), f'"name": "{name}", "item": "' + live(slug))
    new = head + new[h:]
    new = new.replace('Homeowners Insurance (content from figleafagency.com/homeowners-insurance)',
                      f'{name} (copy from homepages/service_pages.py)', 1)
    # menus: Homeowners is no longer the current page, and the pages that
    # had no page yet (plain text in the footer) are links now
    new = new.replace('href="../homeowners-insurance/" aria-current="page"', 'href="' + live('homeowners-insurance') + '"')
    new = new.replace('<a href="./" aria-current="page">Homeowners Insurance</a>', '<a href="' + live('homeowners-insurance') + '">Homeowners Insurance</a>')
    new = link_service_names(new)
    if s.get('contact'):   # the contact form's script (homepages/shared/contact-form.js)
        new = new.replace('  <script src="../insurance-page.js"></script>',
                          '  <script src="../insurance-page.js"></script>\n'
                          '  <script src="../../homepages/shared/contact-form.js"></script>', 1)
    new = new.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py (service_version): '
                      f'{name} in Homeowners version {n}\'s layout; copy in homepages/service_pages.py. -->', 1)
    return new, src_dir


def link_service_names(page):
    """The footer's Renters, Condo, Health, Life and Pet entries (plain text
    while those pages didn't exist) become links."""
    for text, slug in SP.SPAN_NAMES.items():
        page = page.replace(f'<li><span>{text}</span></li>', f'<li><a href="https://figleafagency.com/{slug}/">{text}</a></li>')
    return page


def mark_current(page):
    """aria-current on the menu and footer links to the page itself."""
    return re.sub(r'<a href="\./">', '<a href="./" aria-current="page">', page)


# Build 5's homepage is concept 5 (Eric, 23 Nov): build 1's homepage with a
# video testimonial (landscape, 16:9) beside the written Google reviews, two
# reviews at a time with arrows. (A portrait video card and a full-width
# video were tried as concepts 5 and 7 and dropped.)
VIDEO_BUILD = 5
HOME_ONLY = []
HOME_NAMES = {
    5: "Concept 5: build 1's homepage with a video beside the Google reviews, two at a time",
}


def home_name(k):
    """The bar's name for build k's homepage."""
    return HOME_NAMES.get(k, f'Concept 11 with Homeowners version {homeowners_version(k)}')


PLAY = ('<button class="vr-video__play" type="button" aria-label="Play the video testimonial">'
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg></button>')
POSTER = ('homepages/shared/assets/testimonial-poster.jpg', 'homepages/shared/assets/testimonial-poster-900.jpg', 1600, 896)
# The client's testimonial (a placeholder cut for now), compressed for the web:
# 1280x720 H.264 with AAC audio and faststart, about 6 MB for 70 seconds.
VIDEO = 'homepages/shared/assets/testimonial.mp4'


def video_card(out_dir, cls, poster=POSTER):
    """The video testimonial: the poster with a play button over it. The
    play button swaps in the video with its controls (VIDEO_JS), and
    nothing of the video loads until then."""
    big, small, w, h = poster
    big, small = posixpath.relpath(big, out_dir), posixpath.relpath(small, out_dir)
    video = posixpath.relpath(VIDEO, out_dir)
    return ('          <!-- Video testimonial: the poster and play button until it is played -->\n'
            f'          <figure class="vr-video {cls} hs-reveal" data-vr-video>\n'
            '            <div class="vr-video__frame">\n'
            f'              <video class="vr-video__media" preload="none" playsinline poster="{big}" aria-label="Video testimonial from a Fig Leaf client">\n'
            f'                <source src="{video}" type="video/mp4">\n'
            '              </video>\n'
            f'              <img class="vr-video__poster" src="{big}" srcset="{small} 900w, {big} {w}w" sizes="(max-width: 900px) 100vw, 70vw" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">\n'
            f'              {PLAY}\n'
            '            </div>\n'
            '            <figcaption class="vr-video__cap">\n'
            '              <span class="vr-video__kicker">Video testimonial</span>\n'
            '              <strong>Hear it from our clients</strong>\n'
            '              <span>A client tells their story in their own words.</span>\n'
            + '              <a class="vr-video__more" href="about/testimonials/">See more<span class="visually-hidden"> testimonials</span>'
              '<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            + '            </figcaption>\n'
            '          </figure>\n')


VIDEO_JS = """
  <script>
    /* concept 5: the play button hides the poster and plays the video with
       its own controls */
    document.querySelectorAll('[data-vr-video]').forEach(function (card) {
      var video = card.querySelector('video'), play = card.querySelector('.vr-video__play');
      play.addEventListener('click', function () {
        card.classList.add('is-playing');
        video.controls = true;
        var p = video.play();
        if (p && p.catch) p.catch(function () {});
        video.focus();
      });
    });
  </script>
"""


CAROUSEL_JS = """
  <script>
    /* concept 5: the written reviews, two at a time (one on phones); the
       arrows step one review at a time */
    document.querySelectorAll('[data-vr-carousel]').forEach(function (box) {
      var slides = box.querySelectorAll('.vr-slide'), count = box.querySelector('.vr-carousel__count'), i = 0,
          narrow = window.matchMedia('(max-width: 640px)');
      var prev = box.querySelector('.vr-carousel__prev'), next = box.querySelector('.vr-carousel__next');
      function show(n) {
        var per = Math.min(narrow.matches ? 1 : 2, slides.length), last = slides.length - per;
        i = Math.max(0, Math.min(n, last));
        slides.forEach(function (s, k) {
          var on = k >= i && k < i + per;
          s.classList.toggle('is-active', on);
          s.setAttribute('aria-hidden', on ? 'false' : 'true');
        });
        prev.disabled = i === 0;
        next.disabled = i === last;
        count.textContent = (per > 1 ? (i + 1) + '\u2013' + (i + per) : (i + 1)) + ' of ' + slides.length;
      }
      prev.addEventListener('click', function () { show(i - 1); });
      next.addEventListener('click', function () { show(i + 1); });
      narrow.addEventListener('change', function () { show(i); });
      show(0);
    });
  </script>
"""


def video_reviews(page, out_dir):
    """Concept 5's Google reviews section (homepages/shared/video-reviews.css):
    a 16:9 video testimonial on the left, the written reviews two at a time
    on the right (one on phones), with arrows to step through them."""
    head = '<link rel="stylesheet" href="' + posixpath.relpath('homepages/shared/concept-11.css', out_dir) + '">'
    assert head in page
    css = posixpath.relpath('homepages/shared/video-reviews.css', out_dir)
    page = page.replace(head, head + f'\n  <link rel="stylesheet" href="{css}">', 1)
    m = re.search(r'(        <ul class="hs-reviews__list">.*?        </ul>\n)', page, re.S)
    assert m
    slides = m.group(1).replace('<ul class="hs-reviews__list">', '<ul class="vr-carousel__list">', 1) \
                       .replace('<li class="hs-review hs-reveal">', '<li class="hs-review vr-slide" aria-roledescription="slide">')
    slides = slides.replace('<li class="hs-review vr-slide"', '<li class="hs-review vr-slide is-active"', 2)
    slides = re.sub(r'(?m)^', '  ', slides)
    new = ('        <div class="vr-wide">\n'
           + video_card(out_dir, 'vr-video--wide')
           + '          <div class="vr-carousel hs-reveal" data-vr-carousel aria-roledescription="carousel" aria-label="Google reviews">\n'
           + slides
           + '            <div class="vr-carousel__nav">\n'
           '              <button class="vr-carousel__prev" type="button" aria-label="Previous review"><svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></button>\n'
           '              <span class="vr-carousel__count" aria-live="polite">1\u20132 of 3</span>\n'
           '              <button class="vr-carousel__next" type="button" aria-label="Next review"><svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></button>\n'
           '            </div>\n'
           '          </div>\n'
           '        </div>\n')
    page = page.replace('</body>', CAROUSEL_JS + VIDEO_JS + '</body>', 1)
    return page[:m.start()] + new + page[m.end():]


def testimonials_page(page, out_dir):
    """<build>/about/testimonials/ (under About, Eric 24 Nov): where the
    homepage video card's "See more" goes.
    For now the page header, the video and the Google reviews from the
    homepage; more client videos and reviews are to come (Eric, 24 Nov)."""
    out = f'{out_dir}/about/testimonials'
    page = rebase(page, out_dir, out)
    a, b = page.index('<main id="main">'), page.index('</main>') + len('</main>')
    main = page[a:b]
    reviews = re.search(r'    <section class="hs-section hs-reviews".*?\n    </section>\n', main, re.S).group(0)
    reviews = re.sub(r' *<a class="vr-video__more".*?</a>\n', '', reviews)   # no "See more" on the page itself
    defs = re.search(r'    <svg class="hs-defs".*?</svg>\n', main, re.S)   # the stars and shields
    new = ('<main id="main">\n'
           '  <div class="hs hs--v1" id="home-sections">\n\n'
           '    <!-- Testimonials: a placeholder until more client videos come in -->\n'
           '    <section class="hs-section tm-head" aria-labelledby="tm-title">\n'
           '      <div class="hs-wrap">\n'
           '        <p class="tm-head__eyebrow">Testimonials</p>\n'
           '        <h1 class="tm-head__title" id="tm-title">What our clients say</h1>\n'
           '        <p class="tm-head__text">Hear it from the people we protect. More client videos are on the way.</p>\n'
           '      </div>\n'
           '    </section>\n\n'
           + reviews + '\n' + (defs.group(0) if defs else '') +
           '\n  </div>\n\n  </main>')
    page = page[:a] + new + page[b:]
    vr = '<link rel="stylesheet" href="' + posixpath.relpath('homepages/shared/video-reviews.css', out) + '">'
    assert vr in page
    page = page.replace(vr, vr + '\n  <link rel="stylesheet" href="' + posixpath.relpath('homepages/shared/testimonials.css', out) + '">', 1)
    # no hero on this page: drop the hero scripts
    page = re.sub(r'\s*<script src="[^"]*/(?:hero-x|concept-11)\.js"></script>', '', page)
    page = re.sub(r'<title>[^<]*</title>', '<title>Concept 5 · Testimonials | The Fig Leaf Agency</title>', page, count=1)
    page = re.sub(r'(<!-- Built by homepages/build.py)[^>]*-->',
                  r'\1 (testimonials_page): from the build 5 homepage\'s reviews. Edit the script, then re-run it. -->', page, count=1)
    page = mark_current(page)
    write(f'{out}/index.html', page)


def build_dir(k):
    return f'build-{k}'


def main_bar(cur, out_dir, page='home', build=1):
    """The bar on the current build's pages. cur is 'AC', 'GC' or a build
    number. On Homeowners pages the numbers open each build's Homeowners
    page, so the five layouts can be compared side by side."""
    rel_ = lambda target: posixpath.relpath(target, out_dir) + '/'
    gc_build = cur if cur in BUILDS else build  # GC stays inside the build you came from
    entries = [('AC', 'AC', 'Fig leaf photo gallery', rel_(GALLERY)),
               ('GC', 'GC', 'Get a quote', rel_(f'{build_dir(gc_build)}/crq-form'))]
    sub = PAGE_PATH[page]
    if page == 'homeowners' or page in SP.BY_SLUG:   # the numbers are the four Homeowners versions
        for v, (_, name) in enumerate(HOMEOWNERS_VERSIONS, 1):
            entries.append((v, str(v), f'Homeowners version {v}: {name}', rel_(build_dir(v) + sub)))
    else:
        for k in BUILDS + (HOME_ONLY if page == 'home' else []):
            entries.append((k, str(k), home_name(k) if page == 'home' else f'Concept 11 with Homeowners version {homeowners_version(k)}', rel_(build_dir(k) + sub)))
    keys = [e[0] for e in entries]
    i = keys.index(cur) if cur in keys else keys.index(homeowners_version(cur))
    items = []
    for key, text, name, href in entries:
        here = ' aria-current="page"' if key == cur else ''
        items.append(f'<li><a class="review-bar__link" href="{href}" data-name="{name}"{here}>'
                     f'{text}<span class="visually-hidden">: {name}</span></a></li>')
    if cur == 'AC':
        label, title = 'Gallery', 'Fig leaf photo gallery'
    elif cur == 'GC':
        label, title = 'Get a quote', 'Get a quote'
    else:
        label = f'Build {cur}'
        back = f' · <a href="{rel_(build_dir(cur))}" style="color:inherit">back to the homepage</a>'
        if page == 'homeowners':
            v = homeowners_version(cur)
            title = f'Homeowners version {v} of {len(HOMEOWNERS_VERSIONS)}: {HOMEOWNERS_VERSIONS[v - 1][1]}' + back
        elif page in SP.BY_SLUG:
            v = homeowners_version(cur)
            title = (f'{SP.BY_SLUG[page]["name"]} in Homeowners version {v}\'s layout: {HOMEOWNERS_VERSIONS[v - 1][1]}'
                     + (' (draft copy)' if SP.BY_SLUG[page]['draft'] else '') + back)
        elif page in BIOS or page == 'about':
            a, b = ABOUT_CONCEPTS[cur]
            title = (f'About concept {cur}: {a}' if page == 'about' else f'{BIOS[page][0]} bio, concept {cur}: {b}') + back
        else:
            title = home_name(cur)
    return ('<nav class="review-bar" aria-label="Current build">\n'
            f'    <p class="review-bar__title"><span class="review-bar__label">{label}</span> '
            f'<span class="review-bar__name">{title}</span></p>\n'
            '    <div class="review-bar__controls">\n'
            '      <ul class="review-bar__list review-bar__list--long">\n        '
            + '\n        '.join(items) + '</ul>\n'
            f'      <a class="review-bar__step review-bar__step--prev" href="{entries[i - 1][3]}" rel="prev" aria-label="Previous">'
            '<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            f'      <a class="review-bar__step" href="{entries[(i + 1) % len(entries)][3]}" rel="next" aria-label="Next">'
            '<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a>\n'
            '    </div>\n  </nav>')


# Pages each build has, as paths under build-N/ (for the bar's numbers)
# team bio pages under about/: slug -> (name, title). Burke has no bio sheet,
# so his title is his own nickname from his bio.
BIOS = {'chris-oliveira': ('Chris Oliveira', 'Account Executive'),
        'danielle-mohr': ('Danielle Mohr', 'Business Development Manager'),
        'jarihana-abreu': ('Jarihana Abreu', 'Licensed Insurance Agent'),
        'les-silverman': ('Les Silverman', 'Sr. Account Executive'),
        'burke': ('Burke', 'The Insurance Guy')}
# Each build has its own About and bio design (homepages/about/about-v<k>.html,
# <bio>-v<k>.html; styles about.css plus about-<k>.css)
ABOUT_CONCEPTS = {1: ('Layout A, our story', 'Photo and details'),
                  2: ('Layout B, how we got here', 'Contact card'),
                  3: ('Editorial', 'Split screen'),
                  4: ('Chapters', 'Q and A'),
                  5: ('By the numbers', 'Fig leaf portrait')}
PAGE_PATH = {'home': '', 'homeowners': '/homeowners-insurance', 'about': '/about',
             **{slug: f'/about/{slug}' for slug in BIOS},
             **{s['slug']: '/' + s['slug'] for s in SP.SERVICES}}


def about_links(page, out, build):
    """Point About links at the build's own About page: the header's About
    (which pointed at a folder that doesn't exist), the footer's About Us and
    Meet Our Team, and the homepage About section's values button."""
    to = lambda target: posixpath.relpath(f'{build}/about', out) + '/' + target
    page = re.sub(r'href="(?:\.\./)*archive-[a-e]/about/"', f'href="{to("")}"', page)
    page = page.replace('href="https://figleafagency.com/about/"', f'href="{to("")}"')
    page = page.replace('href="https://figleafagency.com/meet-our-team/"', f'href="{to("#team")}"')
    # the header's About gets a sub-menu, built like Personal Insurance's
    page = page.replace(f'<li><a class="site-nav__link" href="{to("")}">About</a></li>',
        '<li class="site-nav__item">\n'
        f'            <a class="site-nav__link" href="{to("")}">About</a>\n'
        '            <button class="site-nav__sub-toggle" type="button" aria-expanded="false" aria-controls="sub-about">\n'
        '              <svg class="icon" aria-hidden="true"><use href="#i-chevron"></use></svg>\n'
        '              <span class="visually-hidden">About pages</span>\n'
        '            </button>\n'
        '            <ul class="site-nav__sub" id="sub-about">\n'
        f'              <li><a href="{to("")}">About The Fig Leaf</a></li>\n'
        f'              <li><a href="{to("#team")}">Meet the Team</a></li>\n'
        '            </ul>\n'
        '          </li>', 1)
    # (the homepage's values button keeps pointing at the About page: Our Values is gone)
    if build == build_dir(VIDEO_BUILD) and '>Testimonials</a>' not in page:   # its Testimonials page sits under About
        page = page.replace(f'<li><a href="{to("#team")}">Meet the Team</a></li>',
                            f'<li><a href="{to("#team")}">Meet the Team</a></li>\n'
                            f'              <li><a href="{to("testimonials/")}">Testimonials</a></li>', 1)
        page = page.replace(f'<li><a href="{to("#team")}">Meet Our Team</a></li>',
                            f'<li><a href="{to("#team")}">Meet Our Team</a></li><li><a href="{to("testimonials/")}">Testimonials</a></li>', 1)
    return page


def build_about(k):
    """build-N/about/ and build-N/about/<bio>/: concept 11's header and
    footer (from the build's homepage) around the About page and the team
    bios in homepages/about/. Styles: homepages/shared/about.css."""
    out_dir = build_dir(k)
    home = read(f'{out_dir}/index.html')
    body = home[home.index('<body>'):home.index('<main id="main">')]
    tail = home[home.index('</main>') + len('</main>'):]
    body = body[:body.index('<nav class="review-bar"')] + '<!--REVIEW-BAR-->' + body[body.index('</nav>', body.index('<nav class="review-bar"')) + len('</nav>'):]
    tail = re.sub(r'\s*<script src="[^"]*hero-x\.js"></script>', '', tail)
    pages = [('about', 'about', 'About Us | The Fig Leaf Agency',
              'The Fig Leaf Agency is an independent insurance agency in Hazlet, NJ. Our story and the team behind your policy.',
              'https://figleafagency.com/about/')]
    pages += [(slug, f'about/{slug}', f'{name}, {role} | The Fig Leaf Agency',
               f'Meet {name} of The Fig Leaf Agency in Hazlet, NJ.', f'https://figleafagency.com/about/{slug}/')
              for slug, (name, role) in BIOS.items()]
    for key, sub, title, desc, canon in pages:
        out = f'{out_dir}/{sub}'
        up = lambda p: posixpath.relpath(p, out)
        sheets = ['archive-a/styles.css', 'archive-a/home-sections.css', 'archive-a/grid.css', 'archive-a/palette.css',
                  'homepages/shared/concept-11.css', 'homepages/shared/about.css']
        if k != 1:
            sheets.append(f'homepages/shared/about-{k}.css')
        if key == 'about' and k in (1, 2):   # layouts A and B use concept 5's hero and story path
            sheets.append('homepages/shared/about-5.css')
        css = ''.join(f'\n  <link rel="stylesheet" href="{up(c)}">' for c in sheets)
        head = ('<!DOCTYPE html>\n<!-- Built by homepages/build.py: build ' + str(k) + "'s " + sub +
                f' page, from homepages/about/{key}-v{k}.html in concept 11\'s header and footer. '
                'Edit that file, then re-run the script. -->\n'
                '<html lang="en" data-header="a"><head><meta charset="utf-8">\n'
                '  <meta name="robots" content="noindex">\n'
                '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
                f'  <title>Build {k} · {title}</title>\n'
                f'  <meta name="description" content="{desc}">\n'
                f'  <link rel="canonical" href="{canon}">\n'
                f'  <link rel="icon" href="{up("archive-a/assets/fig-leaf-fill.svg")}" type="image/svg+xml">\n'
                '  <link rel="preconnect" href="https://fonts.googleapis.com/">\n'
                '  <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">\n'
                '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&amp;family=Montserrat:wght@400;500;600;700&amp;family=Lato:wght@400;700&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap">'
                + css + '\n</head>\n')
        main = read(f'homepages/about/{key}-v{k}.html').replace('{B}', out_dir)
        icons = read('homepages/about/_icons.html')
        main = re.sub(r'(<main [^>]*>\n)', lambda m: m.group(1) + icons, main, count=1)
        main = rebase(main, '', out)
        shell = rebase(body + '<!--MAIN-->' + tail, out_dir, out)
        page = head + shell.replace('<!--MAIN-->', '\n' + main.strip('\n').lstrip() + '\n', 1)
        page = about_links(page, out, out_dir)
        here = posixpath.relpath(f'{out_dir}/about', out) + '/'
        page = page.replace(f'<a class="site-nav__link" href="{here}">About</a>',
                            f'<a class="site-nav__link" href="{here}" aria-current="page">About</a>', 1)
        if key == 'about':
            page = page.replace(f'<li><a href="{here}">About The Fig Leaf</a></li>',
                                f'<li><a href="{here}" aria-current="page">About The Fig Leaf</a></li>', 1)
        page = page.replace('<!--REVIEW-BAR-->', main_bar(k, out, key))
        page = page.replace('</body>', f'  <script src="{up("homepages/shared/about.js")}"></script>\n</body>', 1)
        page = keep_links_in(page, out, out_dir)
        write(f'{out}/index.html', page)


def swap_bar(page, bar):
    rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
    return page[:rb.start()] + bar + page[rb.end():]


# Links on the current build stay inside it: reviewers shouldn't land on the
# live figleafagency.com site or anywhere else. A figleafagency.com page the
# build has its own copy of opens that copy; every other link that leaves the
# build (other sites, the live site, pages that don't exist here) becomes a
# dead link: href="#", no new tab, and a click does nothing. The button or
# menu item stays where it is. tel:, mailto: and data: links are left alone.
IN_BUILD = {  # figleafagency.com path -> the same page under build-N/
    '': '', 'about/': 'about/', 'meet-our-team/': 'about/#team',
    'homeowners-insurance/': 'homeowners-insurance/',
    'crq/': 'crq-form/', 'get-a-quote/': 'crq-form/',
    **{s['slug'] + '/': s['slug'] + '/' for s in SP.SERVICES},   # the personal insurance pages
}
LIVE = re.compile(r'(?:https?:)?//(?:www\.)?figleafagency\.com/(.*)$')
QUOTE_FORM = 'secure.consumerratequotes.com/'   # the quote form, which the build frames on crq-form/
STAY_IN = tuple(build_dir(k) for k in BUILDS + HOME_ONLY) + (GALLERY,)


def keep_links_in(page, out, build):
    """Make every <a> on a current-build page (out) point inside the build."""
    def fix(m):
        tag, href = m.group(0), m.group(2)
        if href.startswith(('#', 'tel:', 'mailto:', 'data:', 'javascript:')):
            return tag
        target = None
        live = LIVE.match(href)
        if live and live.group(1).split('#')[0] in IN_BUILD:
            target = f'{build}/{IN_BUILD[live.group(1).split("#")[0]]}'
        elif QUOTE_FORM in href:
            target = f'{build}/crq-form/'
        elif not re.match(r'(?:https?:)?//', href):
            path = href.split('#')[0].split('?')[0]
            t = posixpath.normpath(posixpath.join(out, path)) if path else out
            if t == f'{build_dir(VIDEO_BUILD)}/about/testimonials':
                return tag   # made later in the run (testimonials_page)
            if t.split('/')[0] in STAY_IN and os.path.exists(os.path.join(REPO, t, 'index.html') if not t.endswith('.html') else os.path.join(REPO, t)):
                return tag   # already inside the build
            sub = t.split('/', 1)[1] + '/' if '/' in t else ''
            if sub in IN_BUILD and sub:   # e.g. the gallery's about/, which it doesn't have
                target = f'{build}/{IN_BUILD[sub]}' + ('#' + href.split('#')[1] if '#' in href else '')
        if target:
            new = posixpath.relpath(target.split('#')[0], out) + '/' + ('#' + target.split('#')[1] if '#' in target else '')
            return tag.replace(f'href="{href}"', f'href="{new}"', 1)
        tag = re.sub(r'\s(?:target|rel)="[^"]*"', '', tag)
        return tag.replace(f'href="{href}"', 'href="#" onclick="return false" data-offsite', 1)
    return re.sub(r'<a\b[^>]*?\shref=(["\'])(.*?)\1[^>]*>', fix, page)


# --- client review round 2 (Reviewer a9lh, 19 Nov): builds only ------------
# Concept 11 itself stays as it was (archived); these run on build-1 to
# build-5 after the page is made.

def round2_home(page, out_dir):
    """Every build's homepage: Business before Boat in the hero, and a fourth
    card, Life Insurance, under "More Ways We Protect You"."""
    # hero: car, home, business, boat
    words = ('<span class="scene-word" data-scene="boat">your <em>boat.</em></span>\n'
             '            <span class="scene-word" data-scene="business">your <em>business.</em></span>')
    assert words in page
    page = page.replace(words, '<span class="scene-word" data-scene="business">your <em>business.</em></span>\n'
                        '            <span class="scene-word" data-scene="boat">your <em>boat.</em></span>', 1)
    page = page.replace('your car, your home, your boat and your business.</span>',
                        'your car, your home, your business and your boat.</span>', 1)
    page = page.replace('Your car, your home, your boat, your business.', 'Your car, your home, your business, your boat.', 1)
    page = page.replace('a boat on the water at sunset and a brick shopfront"', 'a brick shopfront and a boat on the water at sunset"', 1)
    boat = re.search(r'\n[ \t]*<div class="hx__item" data-scene="boat".*?<span class="hx__bar" aria-hidden="true"></span>\n\s*</div>', page, re.S)
    biz = re.search(r'\n[ \t]*<div class="hx__item" data-scene="business".*?<span class="hx__bar" aria-hidden="true"></span>\n\s*</div>', page, re.S)
    assert boat and biz and boat.end() <= biz.start()
    b_html = boat.group(0).replace('<span class="hx__num">03</span>', '<span class="hx__num">04</span>') \
                          .replace('<span class="hx__num" aria-hidden="true">03</span>', '<span class="hx__num" aria-hidden="true">04</span>')
    z_html = biz.group(0).replace('<span class="hx__num">04</span>', '<span class="hx__num">03</span>') \
                         .replace('<span class="hx__num" aria-hidden="true">04</span>', '<span class="hx__num" aria-hidden="true">03</span>')
    page = page[:boat.start()] + z_html + page[boat.end():biz.start()] + b_html + page[biz.end():]

    # More Ways We Protect You: four cards
    img = posixpath.relpath('homepages/shared/assets/life-insurance.jpg', out_dir)
    card = (
        '          <article class="hs-service hs-reveal">\n'
        f'            <div class="hs-service__media"><img class="hs-service__img" src="{img}" alt="" width="900" height="600" loading="lazy" decoding="async"></div>\n'
        '            <div class="hs-service__body">\n'
        '              <h3 class="hs-line__title">Life Insurance</h3>\n'
        '              <p>Term and whole life policies that keep your family secure, compared across our carriers and explained before you sign.</p>\n'
        '              <a class="hs-more" href="https://figleafagency.com/life-insurance/">Learn more<span class="visually-hidden"> about life insurance</span></a>\n'
        '            </div>\n'
        '          </article>\n')
    m = re.search(r'(<div class="hs-services__grid) hs-services__grid--3(">.*?)(        </div>\n      </div>\n    </section>)', page, re.S)
    assert m
    page = page[:m.start()] + m.group(1) + ' hs-services__grid--4' + m.group(2) + card + m.group(3) + page[m.end():]
    page = page.replace('we protect local businesses, help contractors stay covered on the job, and help drivers keep their records and premiums down.',
                        'we protect local businesses and families, help contractors stay covered on the job, and help drivers keep their records and premiums down.', 1)
    return page


R2_COVERS = [('01', 'i-home', 'Dwelling', 'The physical structure of your home.'),
             ('02', 'i-garage', 'Other Structures', 'Additional structures on your property, such as swimming pools and detached garages.'),
             ('03', 'i-receipt', 'Additional Costs', 'Incurred as a result of a covered loss.'),
             ('04', 'i-sofa', 'Personal Property', 'Your personal belongings, including clothing, furniture and electronics.'
              '<span class="r2-covers__note">Items such as jewelry, watches and fine art may need to be covered separately.</span>'),
             ('05', 'i-liability', 'Personal Liability', 'Occurrences that arise from being a homeowner.')]


def round2_homeowners(k, page, out):
    """Build 1: no "A homeowners policy generally covers" section. Build 3:
    that section merged with build 1's black quote card and its Personal
    insurance links, as one full-width black band (round-2.css)."""
    if k == 1:
        m = re.search(r'\n\n[ \t]*<section class="pg-block" aria-labelledby="pg-covers-title">.*?</section>', page, re.S)
        assert m
        page = page[:m.start()] + page[m.end():]
    if k == 3:
        m = re.search(r'[ \t]*<section class="pg-sec" id="covered".*?</section>\n', page, re.S)
        assert m
        items = '\n'.join(
            f'            <li class="hs-reveal"><span class="r2-covers__num" aria-hidden="true">{n}</span>'
            f'<span class="r2-covers__icon" aria-hidden="true"><svg class="icon" aria-hidden="true"><use href="#{i}"></use></svg></span>'
            f'<div><h3 class="r2-covers__title">{t}</h3><p>{d}</p></div></li>' for n, i, t, d in R2_COVERS)
        links = '\n'.join(
            f'              <li><a href="{h}">{name}<svg class="icon" aria-hidden="true"><use href="#i-arrow"></use></svg></a></li>'
            for name, h in [('Auto Insurance', 'https://figleafagency.com/auto-insurance/'),
                            ('Homeowners Insurance', './'),
                            ('Boat Insurance', 'https://figleafagency.com/boat-insurance/'),
                            ('Personal Umbrella Insurance', 'https://figleafagency.com/personal-umbrella-insurance/')])
        links = links.replace('<a href="./">', '<a href="./" aria-current="page">', 1)
        band = (
            '    <!-- Client review round 2: "A homeowners policy generally covers" merged\n'
            "         with build 1's black quote card, full width (homepages/shared/round-2.css) -->\n"
            '    <section class="pg-sec r2-covered" id="covered" aria-labelledby="pg-covered-title">\n'
            '      <div class="pg-wrap r2-covered__grid">\n'
            '        <div class="r2-covered__main">\n'
            '          <p class="r2-covered__eyebrow">Keeping you protected</p>\n'
            '          <h2 class="r2-covered__title" id="pg-covered-title">A homeowners policy generally covers:</h2>\n'
            '          <ol class="r2-covers">\n' + items + '\n          </ol>\n'
            '        </div>\n'
            '        <aside class="r2-quote" aria-label="Quote and other coverage">\n'
            '          <div class="r2-quote__card">\n'
            '            <h3 class="r2-quote__title">Get a homeowners quote</h3>\n'
            '            <p>We compare top-rated carriers for you, then walk you through every line of the policy.</p>\n'
            '            <a class="pg-btn pg-btn--primary" href="#quote">Start My Quote</a>\n'
            '            <a class="r2-quote__call" href="tel:+19088623447"><svg class="icon" aria-hidden="true"><use href="#i-phone"></use></svg>Call (908) 862-3447</a>\n'
            '          </div>\n'
            '          <nav class="r2-quote__links" aria-label="Personal insurance">\n'
            '            <h3 class="r2-quote__head">Personal insurance</h3>\n'
            '            <ul>\n' + links + '\n            </ul>\n'
            '          </nav>\n'
            '        </aside>\n'
            '      </div>\n'
            '    </section>\n')
        page = page[:m.start()] + band + page[m.end():]
        last = list(re.finditer(r'<link rel="stylesheet"[^>]*>', page))[-1]
        page = page[:last.end()] + f'\n  <link rel="stylesheet" href="{posixpath.relpath("homepages/shared/round-2.css", out)}">' + page[last.end():]
    return page


def build_builds():
    """build-1 to build-5: concept 11's homepage, quote pages and one
    Homeowners version each (build k gets version k, build 5 version 1)."""
    global KEEP_IN
    c11 = next(h for h in HEROES if h[0] == 11)
    for k in BUILDS + HOME_ONLY:
        out_dir = build_dir(k)
        links = out_dir if k in BUILDS else build_dir(1)   # 6 and 7 are homepages only
        build_page(*c11, out_dir=out_dir)
        page = read(f'{out_dir}/index.html')
        page = swap_bar(page, main_bar(k, out_dir))
        page = round2_home(page, out_dir)
        page = re.sub(r'<title>Concept 11 ·', f'<title>Build {k} ·', page, count=1)
        page = about_links(page, out_dir, links)
        page = keep_links_in(link_service_names(page), out_dir, links)
        if k in HOME_NAMES:
            page = video_reviews(page, out_dir)
            page = re.sub(rf'<title>Build {k} ·', f'<title>Concept {k} ·', page, count=1)
        page = page.replace('<!-- Built by homepages/build.py: concept 11:',
                            f'<!-- Built by homepages/build.py: build {k} (concept 11, Homeowners version {homeowners_version(k)}):'
                            if k in BUILDS else f'<!-- Built by homepages/build.py: homepage concept {k} (build 1\'s homepage, links to build 1):', 1)
        write(f'{out_dir}/index.html', page)
        if k in HOME_NAMES:
            testimonials_page(page, out_dir)
        if k not in BUILDS:
            continue
        for sub in SUBPAGES:
            src = HOMEOWNERS_VERSIONS[homeowners_version(k) - 1][0] if sub == 'homeowners-insurance' else f'{c11[1]}/{sub}'
            out = f'{out_dir}/{sub}'
            page = read(f'{src}/index.html')
            page = swap_bar(page, '<!--REVIEW-BAR-->')
            title = f'Build {k}' if sub == 'homeowners-insurance' else 'Get a quote'
            page = re.sub(r'<title>(?:Concept|Archive) \w+ ·', f'<title>{title} ·', page, count=1)
            if 'name="robots"' not in page:
                page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)
            if sub == 'homeowners-insurance':   # the footer's link to the page itself
                page = page.replace('<a href="./" aria-current="page">Homeowners Insurance</a>',
                                    '<a href="https://figleafagency.com/homeowners-insurance/" aria-current="page">Homeowners Insurance</a>', 1)
            KEEP_IN = out_dir
            page = rebase(page, src, out)
            KEEP_IN = None
            if sub == 'homeowners-insurance':
                bar = main_bar(k, out, 'homeowners')
            else:
                bar = main_bar('GC', out, build=k)
                if sub == 'crq':
                    bar = bar.replace('review-bar__name">Get a quote<', 'review-bar__name">Get a quote · quote request page<', 1)
            page = page.replace('<!--REVIEW-BAR-->', bar)
            # round2_homeowners() (client review round 2, 19 Nov) is not run:
            # the four Homeowners versions from Eric's mockups (23 Nov) replace
            # the Homeowners layouts it changed on builds 1 and 3.
            page = about_links(page, out, out_dir)
            page = keep_links_in(link_service_names(page), out, out_dir)
            page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                                f'build {k}\'s copy of {src}/. Edit that page, then re-run the script. -->', 1)
            write(f'{out}/index.html', page)
        build_services(k)
        build_about(k)
    # the gallery (archive D) is AC: the landing page, with the current bar
    page = read(f'{GALLERY}/index.html')
    page = keep_links_in(swap_bar(page, main_bar('AC', GALLERY)), GALLERY, build_dir(1))
    write(f'{GALLERY}/index.html', page)


def build_services(k):
    """build-N/<slug>/: the personal insurance pages (service_pages.py) in
    the layout of the build's Homeowners version."""
    global KEEP_IN
    out_dir = build_dir(k)
    for s in SP.SERVICES:
        out = f'{out_dir}/{s["slug"]}'
        page, src = service_version(homeowners_version(k), s)
        page = swap_bar(page, '<!--REVIEW-BAR-->')
        page = re.sub(r'<title>Archive B ·', f'<title>Build {k} ·', page, count=1)
        if 'name="robots"' not in page:
            page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)
        KEEP_IN = out_dir
        page = rebase(page, src, out)
        KEEP_IN = None
        page = page.replace('<!--REVIEW-BAR-->', main_bar(k, out, s['slug']))
        page = about_links(page, out, out_dir)
        page = mark_current(keep_links_in(page, out, out_dir))
        write(f'{out}/index.html', page)



# Hero photo frame on the insurance pages, right of the title (client
# review: three to pick from). Arch is the original shape; snapshot and
# block are in homepages/shared/homeowners-versions.css.
HERO_PHOTO = {1: 'snapshot', 2: 'block', 3: 'arch', 4: 'snapshot', 5: 'block'}


def mark_hero_photos():
    """Adds pg--photo-<frame> to <main> on every build's insurance pages."""
    for k, frame in HERO_PHOTO.items():
        root = os.path.join(REPO, build_dir(k))
        for sub in sorted(os.listdir(root)):
            path = os.path.join(root, sub, 'index.html')
            if not os.path.isfile(path):
                continue
            page = read(os.path.relpath(path, REPO))
            if 'pg-head__photo' not in page:
                continue
            page = re.sub(r'(<main id="main" class="[^"]*?)(?: pg--photo-\w+)?"', rf'\1 pg--photo-{frame}"', page, count=1)
            write(os.path.relpath(path, REPO), page)


# Personal Insurance navigation (Eric, 24 Nov): on these builds the header's
# Personal Insurance menu lists all nine personal pages, the Personal
# Insurance link itself goes to the homepage's Comprehensive Coverage
# section, and every insurance page gets a breadcrumb above its title
# (Home / Personal Insurance / <page>). Styles: homeowners-versions.css (.pg-crumbs).
NAV_BUILDS = [1]


def personal_nav():
    names = {**{s['slug']: s['name'] for s in SP.SERVICES}, 'homeowners-insurance': 'Homeowners Insurance'}
    order = ['auto-insurance', 'homeowners-insurance', 'boat-insurance', 'personal-umbrella-insurance',   # the footer's order
             'renters-insurance', 'condo-insurance', 'health-insurance', 'life-insurance', 'pet-insurance']
    pages = [(slug, names[slug]) for slug in order]
    for k in NAV_BUILDS:
        root = build_dir(k)
        subs = [None] + sorted(d for d in os.listdir(os.path.join(REPO, root))
                               if os.path.isfile(os.path.join(REPO, root, d, 'index.html')))
        for sub in subs:
            path = f'{root}/index.html' if sub is None else f'{root}/{sub}/index.html'
            page = read(path)
            up = '' if sub is None else '../'
            items = '\n'.join(f'              <li><a href="./" aria-current="page">{n}</a></li>' if slug == sub
                              else f'              <li><a href="{up}{slug}/">{n}</a></li>' for slug, n in pages)
            page, n = re.subn(r'<ul class="site-nav__sub" id="sub-personal">.*?</ul>',
                              lambda m: '<ul class="site-nav__sub" id="sub-personal">\n' + items + '\n            </ul>',
                              page, count=1, flags=re.S)
            assert n == 1, path
            page = page.replace('<a class="site-nav__link" href="#" onclick="return false" data-offsite>Personal Insurance</a>',
                                f'<a class="site-nav__link" href="{up}#coverage">Personal Insurance</a>', 1)
            if sub is None:
                page = page.replace('<section class="fl-grid-host hs-section hs-coverage" aria-labelledby',
                                    '<section class="fl-grid-host hs-section hs-coverage" id="coverage" aria-labelledby', 1)
            elif sub in names and 'pg-crumbs' not in page:
                crumbs = ('      <nav class="pg-wrap pg-crumbs" aria-label="Breadcrumb">\n'
                          '        <ol>\n'
                          '          <li><a href="../">Home</a></li>\n'
                          '          <li><a href="../#coverage">Personal Insurance</a></li>\n'
                          f'          <li><span aria-current="page">{names[sub]}</span></li>\n'
                          '        </ol>\n'
                          '      </nav>\n')
                page, n = re.subn(r'(?m)^(      <div class="pg-wrap pg-head__grid">)', lambda m: crumbs + m.group(1), page, count=1)
                assert n == 1, path
            write(path, page)


def main():
    build_hero_css()
    build_subpages(1, 'concept-1')  # concept 1's Homeowners page only
    for h in HEROES:
        build_page(*h)
        build_subpages(h[0], h[1])
    update_concept_bars()
    landing_bars()
    build_homeowners_versions()
    build_builds()
    mark_hero_photos()
    personal_nav()
    print('built', len(HEROES), 'concept pages and builds', BUILDS)


if __name__ == '__main__':
    main()

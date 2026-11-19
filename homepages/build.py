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


def build_dir(k):
    return f'build-{k}'


def main_bar(cur, out_dir, page='home', build=1):
    """The bar on the current build's pages. cur is 'AC', 'GC' or a build
    number. On Homeowners pages the numbers open each build's Homeowners
    page, so the five layouts can be compared side by side."""
    rel_ = lambda target: posixpath.relpath(target, out_dir) + '/'
    gc_build = cur if isinstance(cur, int) else build  # GC stays inside the build you came from
    entries = [('AC', 'AC', 'Fig leaf photo gallery', rel_(GALLERY)),
               ('GC', 'GC', 'Get a quote', rel_(f'{build_dir(gc_build)}/crq-form'))]
    for k in BUILDS:
        lay = HOMEOWNERS[k - 1][1]
        sub = PAGE_PATH[page]
        entries.append((k, str(k), f'Concept 11 with Homeowners layout {k} ({lay})', rel_(build_dir(k) + sub)))
    keys = [e[0] for e in entries]
    i = keys.index(cur)
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
            title = f'Homeowners layout {cur} of {len(BUILDS)}, {HOMEOWNERS[cur - 1][1]}' + back
        elif page in BIOS or page == 'about':
            title = ('About page' if page == 'about' else f'Bio page: {BIOS[page]}') + back
        else:
            title = f'Concept 11 with Homeowners layout {cur}'
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
BIOS = {'chris-oliveira': 'Chris Oliveira'}   # team bio pages under about/
PAGE_PATH = {'home': '', 'homeowners': '/homeowners-insurance', 'about': '/about',
             **{slug: f'/about/{slug}' for slug in BIOS}}


def about_links(page, out, build):
    """Point About links at the build's own About page: the header's About
    (which pointed at a folder that doesn't exist), the footer's About Us and
    Meet Our Team, and the homepage About section's values button."""
    to = lambda target: posixpath.relpath(f'{build}/about', out) + '/' + target
    page = re.sub(r'href="(?:\.\./)*archive-[a-e]/about/"', f'href="{to("")}"', page)
    page = page.replace('href="https://figleafagency.com/about/"', f'href="{to("")}"')
    page = page.replace('href="https://figleafagency.com/meet-our-team/"', f'href="{to("#team")}"')
    page = page.replace('<a class="hs-btn hs-btn--outline" href="' + to("") + '">Learn More About Our Values</a>',
                        '<a class="hs-btn hs-btn--outline" href="' + to("#values") + '">Learn More About Our Values</a>')
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
              'The Fig Leaf Agency is an independent insurance agency in Hazlet, NJ. Our story, our values and the team behind your policy.',
              'https://figleafagency.com/about/')]
    pages += [(slug, f'about/{slug}', f'{name}, Account Executive | The Fig Leaf Agency',
               f'Meet {name} of The Fig Leaf Agency in Hazlet, NJ.', f'https://figleafagency.com/about/{slug}/')
              for slug, name in BIOS.items()]
    for key, sub, title, desc, canon in pages:
        out = f'{out_dir}/{sub}'
        up = lambda p: posixpath.relpath(p, out)
        css = ''.join(f'\n  <link rel="stylesheet" href="{up(c)}">' for c in (
            'archive-a/styles.css', 'archive-a/home-sections.css', 'archive-a/grid.css', 'archive-a/palette.css',
            'homepages/shared/concept-11.css', 'homepages/shared/about.css'))
        head = ('<!DOCTYPE html>\n<!-- Built by homepages/build.py: build ' + str(k) + "'s " + sub +
                f' page, from homepages/about/{"about" if key == "about" else key}.html in concept 11\'s header and footer. '
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
                '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&amp;family=Montserrat:wght@400;500;600;700&amp;family=Lato:wght@400;700&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap">'
                + css + '\n</head>\n')
        main = read(f'homepages/about/{"about" if key == "about" else key}.html').replace('{B}', out_dir)
        main = rebase(main, '', out)
        shell = rebase(body + '<!--MAIN-->' + tail, out_dir, out)
        page = head + shell.replace('<!--MAIN-->', '\n' + main.strip('\n').lstrip() + '\n', 1)
        page = about_links(page, out, out_dir)
        here = posixpath.relpath(f'{out_dir}/about', out) + '/'
        page = page.replace(f'<a class="site-nav__link" href="{here}">About</a>',
                            f'<a class="site-nav__link" href="{here}" aria-current="page">About</a>', 1)
        page = page.replace('<!--REVIEW-BAR-->', main_bar(k, out, key))
        write(f'{out}/index.html', page)


def swap_bar(page, bar):
    rb = re.search(r'<nav class="review-bar".*?</nav>', page, re.S)
    return page[:rb.start()] + bar + page[rb.end():]


def build_builds():
    """build-1 to build-5: concept 11's homepage, quote pages and one
    Homeowners layout each (build k gets layout k)."""
    global KEEP_IN
    c11 = next(h for h in HEROES if h[0] == 11)
    for k in BUILDS:
        out_dir = build_dir(k)
        build_page(*c11, out_dir=out_dir)
        page = read(f'{out_dir}/index.html')
        page = swap_bar(page, main_bar(k, out_dir))
        page = re.sub(r'<title>Concept 11 ·', f'<title>Build {k} ·', page, count=1)
        page = about_links(page, out_dir, out_dir)
        page = page.replace('<!-- Built by homepages/build.py: concept 11:',
                            f'<!-- Built by homepages/build.py: build {k} (concept 11, Homeowners layout {k}):', 1)
        write(f'{out_dir}/index.html', page)
        for sub in SUBPAGES:
            src = HOMEOWNERS[k - 1][0] if sub == 'homeowners-insurance' else f'{c11[1]}/{sub}'
            out = f'{out_dir}/{sub}'
            page = read(f'{src}/index.html')
            page = swap_bar(page, '<!--REVIEW-BAR-->')
            title = f'Build {k}' if sub == 'homeowners-insurance' else 'Get a quote'
            page = re.sub(r'<title>(?:Concept|Archive) \w+ ·', f'<title>{title} ·', page, count=1)
            if 'name="robots"' not in page:
                page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)
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
            page = about_links(page, out, out_dir)
            page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Built by homepages/build.py: '
                                f'build {k}\'s copy of {src}/. Edit that page, then re-run the script. -->', 1)
            write(f'{out}/index.html', page)
        build_about(k)
    # the gallery (archive D) is AC: the landing page, with the current bar
    page = read(f'{GALLERY}/index.html')
    write(f'{GALLERY}/index.html', swap_bar(page, main_bar('AC', GALLERY)))


def main():
    build_hero_css()
    build_subpages(1, 'concept-1')  # concept 1's Homeowners page only
    for h in HEROES:
        build_page(*h)
        build_subpages(h[0], h[1])
    update_concept_bars()
    landing_bars()
    build_builds()
    print('built', len(HEROES), 'concept pages and builds', BUILDS)


if __name__ == '__main__':
    main()

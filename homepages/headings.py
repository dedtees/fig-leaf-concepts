"""Fig Leaf's own headings for builds 1 to 5.

Many build pages are assembled from the archive pages, whose section headings
are the old generic ones (and the same on every insurance page). build.py's
write() passes every build-N page through rewrite(), which swaps those
headings for each page's own: the table below is (old text, new text) per
page, matched against whole <h1>-<h6> texts, the .pg-sec__kicker and
.b5-head__lead lines, aria-labels, build 4's About contents list and two
og:descriptions. Text that no longer matches is left alone, so editing a
heading at its source still works.
"""
import html
import re

R = '&rsquo;'


def n(s):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\xa0', ' ').replace('\u2019', "'").split())


M={
'home':[
 ('Comprehensive Coverage','One agency for everything you insure'),
 ('Select One or Bundle!','Home on its own, or bundled with auto'),
 ('About The Fig Leaf Agency','Why we started Fig Leaf'),
 ('More Ways We Protect You','Beyond the everyday policies'),
 ('Google Reviews','Rated 5.0 by our clients'),
 ('Our Carriers','Dozens of carriers, one agent on your side'),
],
'auto-insurance':[
 ("Your car gets you everywhere. Your policy should too.",'Every mile you drive. <span>Covered by people you know.</span>'),
 ("What's in a standard policy",f'What you{R}re actually paying for'),
 ('A standard auto policy is made up of:','Seven parts of a car policy'),
 ('Keeping you protected','Line by line'),
 ('Related coverage','Often paired with auto'),
 ('Get your auto insurance quote','Quote your car'),
 ('Get an auto insurance quote','See what your car would cost with us'),
 ('Fast, free and no obligation','Free, and about 3 to 5 minutes online'),
 ('Rather talk it through?',f'Questions about your car{R}s coverage?'),
],
'homeowners-insurance':[
 ('Protect your home. Preserve what matters.','Your home, <span>covered from the ground up.</span>'),
 ('A homeowners policy generally covers:','Five things a home policy pays for'),
 ('Keeping you protected','From the roof to the fence line'),
 ('Get your homeowners quote','Quote your home'),
 ('Get a homeowners quote','See what your home would cost with us'),
 ('Fast, free and no obligation','Free, with an agent to walk you through it'),
 ('Rather talk it through?','Want to go over your home by phone?'),
],
'boat-insurance':[
 ('A combination of coverages','Hull, liability and the people aboard'),
 ('Additional coverages often include:','Extras worth adding for the water'),
 ('Keeping you protected',f'For the days that don{R}t go to plan'),
 ('Related coverage','For life back on shore'),
 ('Get your boat insurance quote','Quote your boat'),
 ('Get a boat insurance quote','See what your boat would cost with us'),
 ('Fast, free and no obligation','Free, before your next launch'),
 ('Rather talk it through?','Questions before you launch?'),
],
'personal-umbrella-insurance':[
 ('When do you need umbrella insurance?','Three signs you need an umbrella'),
 ("Protecting what you've built",'What a lawsuit could reach'),
 ('Related coverage','What sits under the umbrella'),
 ('Get your personal umbrella insurance quote','Quote your umbrella'),
 ('Get a personal umbrella insurance quote','See what an umbrella would cost you'),
 ('Fast, free and no obligation','Free, and sized to what you own'),
 ('Rather talk it through?','Not sure how much extra you need?'),
],
'renters-insurance':[
 ("Renters insurance protects what's yours.",f'You don{R}t own the building. <span>You own everything in it.</span>'),
 ('Select one or bundle','On its own or with auto'),
 ('Renters insurance typically covers:',f'What your landlord{R}s policy won{R}t'),
 ('Keeping you protected',f'Yours, not the landlord{R}s'),
 ('Related coverage','When you buy, or add a car'),
 ('Get your renters insurance quote','Quote your rental'),
 ('Get a renters insurance quote','See what renters cover would cost'),
 ('Fast, free and no obligation','No cost, no commitment'),
 ('Rather talk it through?','Renting and not sure what you need?'),
],
'condo-insurance':[
 ('Select one or bundle','Alone or bundled with auto'),
 ('Condo insurance typically covers:',f'Where your association{R}s policy stops'),
 ('Keeping you protected','From the walls in'),
 ('Related coverage','Pairs well with condo cover'),
 ('Get your condo insurance quote','Quote your condo'),
 ('Get a condo insurance quote','See what your condo would cost with us'),
 ('Fast, free and no obligation','Free, and explained line by line'),
 ('Rather talk it through?','Not sure where the HOA policy ends?'),
],
'health-insurance':[
 ('Plans we can help you compare:',f'Plans we{R}ll compare side by side'),
 ('Related coverage','More ways to look after your family'),
 ('Get your health insurance quote','Quote your health plan'),
 ('Get a health insurance quote','See which plans fit your budget'),
 ('Fast, free and no obligation','Free, with plain-English answers'),
 ('Rather talk it through?','Rather hear the options out loud?'),
],
'life-insurance':[
 ('Types we can help you compare:','Picking the right kind of policy'),
 ('Related coverage',f'Round out your family{R}s protection'),
 ('Get your life insurance quote','Quote your life policy'),
 ('Get a life insurance quote','See what life cover would cost'),
 ('Fast, free and no obligation','Free, with time to think it over'),
 ('Rather talk it through?','A big decision. Want to talk it over?'),
],
'pet-insurance':[
 ('Pet insurance plans typically cover:','What a pet plan pays for'),
 ('Keeping them protected','Nose to tail'),
 ('Related coverage','Cover for the humans, too'),
 ('Get your pet insurance quote',f'Quote your pet{R}s plan'),
 ('Get a pet insurance quote',f'See what your pet{R}s plan would cost'),
 ('Fast, free and no obligation','Free, for dogs and cats'),
 ('Rather talk it through?','Questions about your dog or cat?'),
],
'crq':[('Rather talk it through?','Prefer to do this by phone?')],
'about':[
 ('Our story','Why Fig Leaf exists'),          # h2 only (eyebrows are <p>)
 ('How we got here','From the trading floor to Hazlet'),
 ('What we learned','Your word is your bond'),
 ('About us','The Fig Leaf story'),
 ('Our team',f'Who you{R}ll work with'),
 ('Meet our team',f'Who you{R}ll work with'),
 ('Visit us','Come see us in Hazlet'),
],
'about/testimonials':[
 ('What our clients say',f'In our clients{R} own words'),
 ('Google Reviews','Straight from Google'),
 ('Rated 5.0 by our clients','Straight from Google'),  # section copied from the rewritten homepage
],
'about/burke':[
 ('From Wall Street to Main Street','From the trading floor to your kitchen table'),
 ('Wall Street experience, Main Street service.','Trading-floor discipline, hometown service.'),
 ('Have a question about your coverage?','Put the Insurance Guy to work'),
],
'about/chris-oliveira':[('Have a question about your coverage?','Get a clear answer from Chris')],
'about/danielle-mohr':[
 ('Coverage you understand, from someone you trust','Know exactly what your policy does'),
 ('Have a question about your coverage?','Let Danielle walk you through it'),
],
'about/jarihana-abreu':[
 ('Coverage that fits your needs and budget','The right fit for your home, car and family'),
 ('Have a question about your coverage?','Find your fit with Jarihana'),
],
'about/les-silverman':[('Have a question about your coverage?','Sixteen years of answers, one call away')],
}

EL = re.compile(r'(<(h[1-6]|p)\b([^>]*)>)(.*?)(</\2>)', re.S)
OG = {
    'auto-insurance': ('content="Your car gets you everywhere. Auto', 'content="Every mile you drive, covered. Auto'),
    'homeowners-insurance': ('content="Protect your home. Preserve what matters. Homeowners', 'content="Your home, covered from the ground up. Homeowners'),
}
TOC = [('Our story', 'Why Fig Leaf exists'), ('Our team', f'Who you{R}ll work with'), ('Visit us', 'Come see us in Hazlet')]


def page_key(path):
    """'build-2/about/burke/index.html' -> 'about/burke'; None if not a build page."""
    m = re.match(r'build-([1-5])/(?:(.*)/)?index\.html$', path.replace('\\', '/'))
    if not m:
        return None, None
    return m.group(1), m.group(2) or 'home'


def rewrite(path, s):
    build, page = page_key(path)
    rules = M.get(page) if page else None
    if not rules:
        return s
    d = dict(rules)

    def rep(m):
        tag, attrs, inner = m.group(2), m.group(3), m.group(4)
        if tag == 'p' and not re.search(r'pg-sec__kicker|b5-head__lead', attrs):
            return m.group(0)
        if 'footer__head' in attrs:
            return m.group(0)
        t = n(inner)
        return m.group(1) + d[t] + m.group(5) if t in d else m.group(0)

    s = EL.sub(rep, s)
    for k, v in rules:
        for cand in {k, html.escape(k, quote=True).replace("'", R), k.replace("'", '\u2019')}:
            s = s.replace(f'aria-label="{cand}"', f'aria-label="{n(v)}"')
    if page == 'about' and build == '4':
        for a, c in TOC:
            s = s.replace(f'</span>{a}</a>', f'</span>{c}</a>')
    if page in OG:
        s = s.replace(*OG[page])
    return s

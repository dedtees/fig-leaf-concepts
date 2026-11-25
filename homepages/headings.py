"""Fig Leaf's own headings for builds 1 to 5.

Many build pages are assembled from the archive pages, whose section headings
are the old generic ones (and the same on every insurance page). build.py's
write() passes every build-N page through rewrite(), which swaps those
headings for each page's own: the table below lists each page's headings,
with up to three wordings for the client to choose from, matched against whole <h1>-<h6> texts, the .pg-sec__kicker and
.b5-head__lead lines, aria-labels, build 4's About contents list and two
og:descriptions. Text that no longer matches is left alone, so editing a
heading at its source still works.
"""
import html
import re

R = '&rsquo;'


def n(s):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\xa0', ' ').replace('\u2019', "'").split())


# Builds 1 and 4 show option A, builds 2 and 5 option B, build 3 option C, so
# the client's ticks on each build say which wording they prefer. An entry is
# (old text, new text) or (old text, (A, B, C)); old text may be a tuple.
OPTION = {'1': 0, '2': 1, '3': 2, '4': 0, '5': 1}


def q(*a):
    return tuple(a)


def talk(thing):
    return f'Rather ask an agent about {thing}?'


M = {
'home': [
 ('Comprehensive Coverage', q('Everything you insure', 'Every policy you need', 'Car, home, boat, business')),
 ('Select One or Bundle!', q('Solo or bundled', 'Bundle your home and car', 'One policy or two, your call')),
 ('About The Fig Leaf Agency', q('Why we started Fig Leaf', 'A better way to buy insurance in New Jersey', 'Built on keeping our word')),
 ('More Ways We Protect You', q('Other ways we help', 'Beyond home and auto', f'There{R}s more we can cover')),
 ('Google Reviews', q('Rated 5.0 by our clients', '140+ five-star reviews', 'What clients tell Google')),
 ('Special Contractor Policies', 'Contractor Policies'),
 ('Our Carriers', q('One agent, many carriers', 'We shop the carriers', 'The carriers we compare')),
],
'auto-insurance': [
 ('Your car gets you everywhere. Your policy should too.', q('Every mile you drive. <span>Covered by people you know.</span>', 'Insurance for the way <span>you actually drive.</span>', 'From the daily commute <span>to the long way home.</span>')),
 ("What's in a standard policy", q(f'What you{R}re actually paying for', 'The pieces of your policy', 'How your policy breaks down')),
 ('A standard auto policy is made up of:', q('Seven parts of a car policy', 'What each part of your auto policy does', 'Seven coverages, explained')),
 ('Keeping you protected', q('Line by line', 'Plain-English answers', 'Bumper to bumper')),
 ('Related coverage', q('Often paired with auto', 'Bundle it with', 'Drivers also ask about')),
 ('Get your auto insurance quote', 'Get your Free Insurance Quote'),   # the CRQ form's heading (client, 25 Nov)
 ('Get an auto insurance quote', q('See what your car insurance would cost with us', 'See what your car insurance would cost with us', 'What would your car insurance cost with us?')),
 ('Fast, free and no obligation', q('Free, and about 3 to 5 minutes online', 'Takes about 3 to 5 minutes', 'Free to ask, free to walk away')),
 ('Rather talk it through?', q(f'Questions about your car{R}s coverage?', talk('your car'), 'Call us about your car')),
],
'homeowners-insurance': [
 ('Protect your home. Preserve what matters.', q('Your home, <span>covered from the ground up.</span>', 'Everything under your roof, <span>looked after.</span>', 'The place you come home to, <span>properly covered.</span>')),
 ('A homeowners policy generally covers:', q('Five things a home policy pays for', 'What your home policy covers', 'Your home policy, in five parts')),
 ('Keeping you protected', q('From the roof to the fence line', 'The house, your things and you', 'Roof, belongings and liability')),
 ('Get your homeowners quote', 'Get your Free Insurance Quote'),   # the CRQ form's heading (client, 25 Nov)
 ('Get a homeowners quote', q('See what your home insurance would cost with us', 'See what your home insurance would cost with us', 'What would your home insurance cost with us?')),
 ('Fast, free and no obligation', q('Free, with an agent to walk you through it', 'An agent walks you through it', 'Free, and explained line by line')),
 ('Rather talk it through?', q('Want to go over your home by phone?', talk('your home'), 'Call us about your home')),
 ('Related coverage', q('Often paired with home', 'Bundle it with', 'Homeowners also ask about')),
],
'boat-insurance': [
 ('A combination of coverages', q('Hull, liability and the people aboard', 'Several coverages in one policy', 'For the boat and everyone on it')),
 ('Additional coverages often include:', q('Extras worth adding for the water', 'Extra coverage for life on the water', 'Add-ons boaters ask about')),
 ('Keeping you protected', q(f'For the days that don{R}t go to plan', 'When things go wrong on the water', 'Breakdowns, salvage and more')),
 ('Related coverage', q('For life back on shore', 'Back on dry land', 'Also for boat owners')),
 ('Get your boat insurance quote', q('Quote your boat insurance', 'Price your boat insurance with us', 'See your boat insurance rate')),
 ('Get a boat insurance quote', 'See what your boat insurance would cost with us'),
 ('Fast, free and no obligation', q('Free, before your next launch', 'Free, and ready before the season', 'No cost to ask')),
 ('Rather talk it through?', q('Questions before you launch?', talk('your boat'), 'Call us about your boat')),
],
'personal-umbrella-insurance': [
 ('When do you need umbrella insurance?', q('Three signs you need an umbrella', 'Who an umbrella policy is for', 'When extra liability makes sense')),
 ("Protecting what you've built", q('What a lawsuit could reach', 'Your savings and your future pay', 'Assets, earnings and gaps')),
 ('Related coverage', q('What sits under the umbrella', 'The policies it sits over', 'Underneath your umbrella')),
 ('Get your personal umbrella insurance quote', q('Quote your umbrella', 'Price an umbrella policy', 'See your umbrella rate')),
 ('Get a personal umbrella insurance quote', 'See what an umbrella would cost you'),
 ('Fast, free and no obligation', q('Free, and sized to what you own', 'Sized to your assets', 'No cost to ask')),
 ('Rather talk it through?', q('Not sure how much extra you need?', 'How much umbrella do you need?', 'Call us about an umbrella')),
],
'renters-insurance': [
 ("Renters insurance protects what's yours.", q(f'You don{R}t own the building. <span>You own everything in it.</span>', f'Your landlord insures the walls. <span>We{R}ll insure the rest.</span>', 'Renting? <span>Your things still need cover.</span>')),
 ('Select one or bundle', q('On its own or with auto', 'Bundle it with your car', 'Alone or with auto')),
 ('Renters insurance typically covers:', q(f'What your landlord{R}s policy won{R}t', 'What renters cover pays for', 'Three things renters cover handles')),
 ('Keeping you protected', q(f'Yours, not the landlord{R}s', 'Your things, your liability, your rent', f'Beyond the landlord{R}s policy')),
 ('Related coverage', q('When you buy, or add a car', 'Next steps after renting', 'Also for renters')),
 ('Get your renters insurance quote', 'Get your Free Insurance Quote'),   # the CRQ form's heading (client, 25 Nov)
 ('Get a renters insurance quote', q('See what renters cover would cost', 'See what renters cover would cost', 'What would renters cover cost?')),
 ('Fast, free and no obligation', q('No cost, no commitment', 'Free to ask', 'Free, with an agent to follow up')),
 ('Rather talk it through?', q('Renting and not sure what you need?', talk('renting'), 'Call us about renters cover')),
],
'condo-insurance': [
 ('Select one or bundle', q('Alone or bundled with auto', 'Bundle it with your car', 'On its own or with auto')),
 ('Condo insurance typically covers:', q(f'Where your association{R}s policy stops', 'What condo cover pays for', 'From your walls inward')),
 ('Keeping you protected', q('From the walls in', 'Your unit, your things, your share', 'Past the master policy')),
 ('Related coverage', q('Pairs well with condo cover', 'Condo owners also ask about', 'Moving, renting or driving?')),
 ('Get your condo insurance quote', 'Get your Free Insurance Quote'),   # the CRQ form's heading (client, 25 Nov)
 ('Get a condo insurance quote', q('See what your condo insurance would cost with us', 'See what your condo insurance would cost with us', 'What would your condo insurance cost with us?')),
 ('Fast, free and no obligation', q('Free, and explained line by line', 'An agent walks you through it', 'Free to ask')),
 ('Rather talk it through?', q('Not sure where the HOA policy ends?', talk('your condo'), 'Call us about your condo')),
],
'health-insurance': [
 ('Plans we can help you compare:', q(f'Plans we{R}ll compare side by side', 'Health plans we can compare', 'Your plan options')),
 ('Related coverage', q('More ways to look after your family', 'Also for your family', 'Protect the rest of the household')),
 ('Get your health insurance quote', q('Quote your health plan', 'Price a health plan', 'See your health plan options')),
 ('Get a health insurance quote', 'See which plans fit your budget'),
 ('Fast, free and no obligation', q('Free, with plain-English answers', 'No jargon, no cost', 'Free to ask')),
 ('Rather talk it through?', q('Rather hear the options out loud?', talk('health plans'), 'Call us about health plans')),
],
'life-insurance': [
 ('Types we can help you compare:', q('Picking the right kind of policy', 'Two kinds of life cover', 'Which policy fits your family?')),
 ('Related coverage', q(f'Round out your family{R}s protection', 'Also for your family', 'More ways to plan ahead')),
 ('Get your life insurance quote', q('Quote your life policy', 'Price a life policy', 'See your life insurance options')),
 ('Get a life insurance quote', 'See what life cover would cost'),
 ('Fast, free and no obligation', q('Free, with time to think it over', 'No pressure, no cost', 'Free to ask')),
 ('Rather talk it through?', q('A big decision. Want to talk it over?', talk('life cover'), 'Call us about life insurance')),
],
'pet-insurance': [
 ('Pet insurance plans typically cover:', q('What a pet plan pays for', 'What pet cover helps with', 'From check-ups to emergencies')),
 ('Keeping them protected', q('Nose to tail', 'For dogs and cats', 'Accidents, illness and care')),
 ('Related coverage', q('Cover for the humans, too', 'For the rest of the family', 'For the people who love them')),
 ('Get your pet insurance quote', q(f'Quote your pet{R}s plan', 'Price a pet plan', f'See your pet{R}s rate')),
 ('Get a pet insurance quote', f'See what your pet{R}s plan would cost'),
 ('Fast, free and no obligation', q('Free, for dogs and cats', 'No cost to ask', 'Free, with an agent to follow up')),
 ('Rather talk it through?', q('Questions about your dog or cat?', talk('pet cover'), 'Call us about your pet')),
],
'crq': [('Rather talk it through?', q('Prefer to do this by phone?', 'Rather ask an agent?', 'Call us instead'))],
'about': [
 ('Our story', 'Why Fig Leaf exists'),
 ('How we got here', 'From the trading floor to Hazlet'),
 ('What we learned', 'Your word is your bond'),
 ('About us', 'The Fig Leaf story'),
 ('Our team', f'Who you{R}ll work with'),
 ('Meet our team', f'Who you{R}ll work with'),
 ('Visit us', 'Come see us in Hazlet'),
],
'about/testimonials': [
 ('What our clients say', q(f'In our clients{R} own words', 'Hear it from our clients', 'Real clients, real stories')),
 # the reviews section is copied from this build's homepage, already reworded
 (('Google Reviews', 'Rated 5.0 by our clients', '140+ five-star reviews', 'What clients tell Google'), q('Straight from Google', 'Reviews from Google', 'What they say on Google')),
],
'about/burke': [
 ('From Wall Street to Main Street', 'From the trading floor to your kitchen table'),
 ('Wall Street experience, Main Street service.', 'Trading-floor discipline, hometown service.'),
 ('Have a question about your coverage?', q('Put the Insurance Guy to work', 'Talk to Burke about your coverage', 'Talk to Burke about your coverage')),
],
'about/chris-oliveira': [('Have a question about your coverage?', q('Get a clear answer from Chris', 'Talk to Chris about your coverage', 'Talk to Chris about your coverage'))],
'about/danielle-mohr': [
 ('Coverage you understand, from someone you trust', 'Know exactly what your policy does'),
 ('Have a question about your coverage?', q('Let Danielle walk you through it', 'Talk to Danielle about your coverage', 'Talk to Danielle about your coverage')),
],
'about/jarihana-abreu': [
 ('Coverage that fits your needs and budget', 'The right fit for your home, car and family'),
 ('Have a question about your coverage?', q('Find your fit with Jarihana', 'Talk to Jarihana about your coverage', 'Talk to Jarihana about your coverage')),
],
'about/les-silverman': [('Have a question about your coverage?', q('Sixteen years of answers, one call away', 'Talk to Les about your coverage', 'Talk to Les about your coverage'))],
}


def options(new):
    return new if isinstance(new, tuple) else (new,) * 3


def table(page, build):
    """{old or option text (normalised): this build's heading} for one page."""
    d = {}
    for old, new in M.get(page, []):
        opts = options(new)
        pick = opts[OPTION[build]]
        for t in (old if isinstance(old, tuple) else (old,)) + opts:
            d[n(t)] = pick
    return d


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
    if page not in M:
        return s
    d = table(page, build)

    def rep(m):
        tag, attrs, inner = m.group(2), m.group(3), m.group(4)
        if tag == 'p' and not re.search(r'pg-sec__kicker|b5-head__lead', attrs):
            return m.group(0)
        if 'footer__head' in attrs:
            return m.group(0)
        t = n(inner)
        return m.group(1) + d[t] + m.group(5) if t in d else m.group(0)

    s = EL.sub(rep, s)
    for k, v in d.items():
        for cand in {k, html.escape(k, quote=True).replace("'", R), k.replace("'", '\u2019')}:
            s = s.replace(f'aria-label="{cand}"', f'aria-label="{n(v)}"')
    if page == 'about' and build == '4':
        for a, c in TOC:
            s = s.replace(f'</span>{a}</a>', f'</span>{c}</a>')
    if page in OG:
        s = s.replace(*OG[page])
    return s

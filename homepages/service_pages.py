"""The personal insurance pages (Auto, Boat, Personal Umbrella, Renters,
Condo, Life, Health, Pet), laid out like the Homeowners page.

Each page is the Homeowners version of its build (build_homeowners_versions
in build.py) with the sections swapped for the page's own: the title band
(hero), the overview ("perils") band, the "generally covers" grid, and the
quote form with the "Rather talk it through?" card.

Copy sources:
- Auto, Boat and Personal Umbrella: the agency's content map
  (Fig_Leaf_New_Website_Content_Map.docx, 1 Sep 2026), lightly edited the
  same way the Homeowners page is, with intros from the website build brief.
- 'contact': pages the Consumer Rate Quotes form doesn't cover (Boat, Personal
  Umbrella, Life, Health and Pet; it covers Auto, Homeowners, Renters, Condo). They get a short contact form in place of the quote
  form (contact_form() below; sent by homepages/shared/contact-form.js), and
  the value is the hint in its message box.
- Renters, Condo, Life, Health and Pet: the build brief's DRAFT copy (these
  pages aren't in the content map). draft=True shows a "Draft copy" tag in
  the hero; the agency needs to confirm the copy before launch.
Anything in [square brackets] is a placeholder still waiting on copy.
"""

LIVE = 'https://figleafagency.com/'

# Photos (paths from the repo root). None = a "photo to come" placeholder.
CAR = 'archive-e/assets/photo-car.jpg'
CAR_ROAD = 'hero-concepts/shared/car.jpg'
BOAT = 'archive-e/assets/photo-boat.jpg'
BOAT_SEA = 'hero-concepts/shared/boat.jpg'
HOUSE = 'archive-e/assets/photo-home.jpg'
FAMILY_BEACH = 'homepages/shared/assets/life-insurance.jpg'
MOVING = 'archive-b/assets/homeowners/home-cta.jpg'
AGENT = 'archive-b/assets/homeowners/home-4.jpg'

# Adobe Stock picks for review: watermarked previews (comps) straight from
# Adobe until the agency licenses them; then the licensed files go in
# homepages/shared/assets/stock/ and these point there.
def COMP(path_id):
    d, n = path_id
    return f'https://as1.ftcdn.net/v2/jpg/{d}/1000_F_{n}.jpg'
RENTERS_HOME = COMP(('07/54/95/66', '754956689_XTzCo4E2LfqMFvHwXKp5qCXOqcMXwaaY'))
CONDO_ROOM = COMP(('04/71/48/71', '471487131_YzMQZZUTC1HArwsoQtp7PVLuXKqnfwgc'))
CONDO_BUILDING = COMP(('21/49/97/47', '2149974736_Fsfjc7BdeFGIBEXuDaNHVSP32aDANmCU'))
LIFE_FAMILY = COMP(('05/31/00/23', '531002360_RWIQ8FMWxLU6l9MWiC5nhjvN2TU2uPkS'))
HEALTH_VISIT = COMP(('05/92/61/93', '592619383_AB8zJvSWQgBoQgicryrcytZxvbFy5Qbv'))
HEALTH_PEDIATRIC = COMP(('04/84/86/95', '484869531_B79MGsEMR6KgiO6hSbcpwCNSux12qk13'))
PET_VET = COMP(('21/00/25/78', '2100257871_fe6cWogBPhc7OTcIWmCFyPQQjKlfzO4Y'))
PET_SOFA = COMP(('14/02/42/86', '1402428625_z0CYnvI6nhJXa0L9tdkNFnptgjRCwyQt'))

# The "Rather talk it through?" photo, where the house one doesn't fit.
TALK_PHOTOS = {
    'auto-insurance': (COMP(('02/31/04/89', '231048974_VOYhhhLWbWyxeTu2MQA71pFfPGRDdFly')), 'An agent talking with a couple beside their car'),
    'boat-insurance': (COMP(('02/79/90/46', '279904629_KsZXVvInhmMdcTLOxPhzSDJvg1Zmdi8n')), 'An agent shaking hands with a couple at a marina'),
}

# Photos for the overview tiles (the small cards beside the dark intro card),
# drawn like Homeowners' Fire, Wind and Theft. Same order as each page's tiles.
TILE_PHOTOS = {
    'auto-insurance': [
        (COMP(('06/33/55/79', '633557956_HqTpzz2yv0sAnxm1yifHmsMrqR2r6gDp')), 'Two drivers exchanging insurance details after a crash'),
        (COMP(('18/04/91/67', '1804916783_6jkezR6X06tQhPb6q8f8Hc2Q5L6djsIR')), 'A car with a dented rear quarter after a collision'),
        (COMP(('05/44/94/20', '544942077_Vm870HjGJEe3q16Ox3Hb6r8Ww8NJuOTv')), 'A car that has crashed into a fence'),
    ],
    'boat-insurance': [
        (COMP(('07/40/39/61', '740396120_QVU15RJxvJhv55DYEfZpFaC2FXZbvqpl')), 'Damaged boats piled against a marina after a storm'),
        (COMP(('07/54/81/90', '754819020_TMfLQTCaKWX3mQC3okc2lF9lwvTtnOF7')), 'The bow of a yacht damaged in a collision'),
        (COMP(('01/20/77/90', '120779074_c0DbmTfrT47BHmws1Y6dACK87oIOPBcs')), 'A paramedic helping an injured woman'),
    ],
    'personal-umbrella-insurance': [
        (COMP(('04/39/89/39', '439893945_zcVoAbyXtTGRvQJIAdl7hRWZgP9Otc8j')), 'Friends at a backyard pool party'),
        (COMP(('04/59/37/27', '459372773_VyB43khG7MkpRUHfp9SFElvEN0moSo6U')), 'An intersection crash involving a car and a semi truck'),
        (COMP(('20/77/63/96', '2077639693_Mjxqnojlh5D2Vmx4bXN57AgcJIfCVgZy')), 'A lawyer reviewing legal papers beside a gavel'),
    ],
    'life-insurance': [
        (COMP(('00/93/70/20', '93702077_pfqlsHF7kO5nXzhJBcoVzfUAS3Zh8Xhn')), 'A mother holding her baby while working at the kitchen table'),
        (COMP(('20/80/19/29', '2080192959_pt4Hx2A3n8zGGcFc6i7JLKbCpx7bsaba')), 'A family receiving the keys to their new home'),
        (COMP(('03/24/35/15', '324351546_YsHbxfuu9WzNV127oIgu4stem3ImLR6k')), 'A coffin decorated with flowers'),
        (COMP(('21/97/61/72', '2197617222_9uWSn7mKXQSvUCdfNYDvkNgPEKMA9tCl')), 'A graduate in cap and gown with proud parents'),
    ],
}

# Extra line icons for these pages, drawn like the rest of the sprite
# (24px box, stroked with currentColor).
ICONS = {
    'i-medical': '<rect x="4" y="4" width="16" height="16" rx="4"></rect><path d="M12 8.5v7M8.5 12h7"></path>',
    'i-boat': '<path d="M3 15.5h18l-2.6 4H5.6z"></path><path d="M11.5 3v12.5"></path><path d="M11.5 4.5 18 13h-6.5"></path>',
    'i-umbrella': '<path d="M3 12a9 9 0 0 1 18 0z"></path><path d="M12 12v6.5a2 2 0 0 0 4 0"></path><path d="M12 3v-.5"></path>',
    'i-lifebuoy': '<circle cx="12" cy="12" r="8.5"></circle><circle cx="12" cy="12" r="3.5"></circle><path d="m6 6 3.5 3.5M14.5 14.5 18 18M18 6l-3.5 3.5M9.5 14.5 6 18"></path>',
    'i-wrench': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94z"></path>',
    'i-dollar': '<path d="M12 2.5v19"></path><path d="M17 5.5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>',
    'i-cap': '<path d="M22 10 12 5 2 10l10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path><path d="M22 10v5"></path>',
    'i-paw': '<circle cx="6.5" cy="10" r="1.8"></circle><circle cx="10" cy="6" r="1.8"></circle><circle cx="14.5" cy="6" r="1.8"></circle><circle cx="18" cy="10" r="1.8"></circle><path d="M8 17.2c0-3 2-5.7 4.2-5.7s4.3 2.7 4.3 5.7c0 1.8-1.4 2.3-4.3 2.3S8 19 8 17.2z"></path>',
    'i-heart': '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7z"></path>',
    'i-people': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"></path>',
    'i-clock': '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path>',
    'i-infinity': '<path d="M7 9a3 3 0 1 0 0 6c2.5 0 7.5-6 10-6a3 3 0 1 1 0 6c-2.5 0-7.5-6-10-6z"></path>',
    'i-layers': '<path d="m12 3 9 5-9 5-9-5z"></path><path d="m3 13 9 5 9-5"></path>',
}

# Each page: slug (as on figleafagency.com), name, draft flag, head
# metadata, hero, overview band (None = no band), covered grid, quote copy
# and related links. Covered items: (icon, title, text, note); the first
# item is the big card and gets cover_photo.
SERVICES = [
    {
        'slug': 'auto-insurance', 'name': 'Auto Insurance', 'short': 'auto insurance', 'draft': False,
        'meta': 'Auto insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Liability, PIP, collision, comprehensive and more, compared across top carriers and explained line by line.',
        'og': 'Your car gets you everywhere. Auto insurance from an independent agency in Hazlet, NJ.',
        'h1': ('Your car gets you everywhere.', 'Your policy should too.'),
        'lead': 'Your auto policy should be just as dependable as your car, and you should know exactly what&rsquo;s in it. A standard auto insurance policy is made up of the coverages below, and we&rsquo;ll walk you through every one.',
        'cta': 'Get Auto Insurance Quote',
        'photo': (CAR, 'A white SUV parked on a dirt road below red rock cliffs'),
        'overview': {
            'kicker': 'What&rsquo;s in a standard policy',
            'text': 'A standard auto policy protects <em>people, your car and other people&rsquo;s property.</em>',
            'tiles': [('i-liability', 'People'), ('i-car', 'Your car'), ('i-home', 'Property')],
        },
        'covered_title': 'A standard auto policy is made up of:',
        'covered_kicker': 'Keeping you protected',
        'cover_photo': CAR_ROAD,
        'covered': [
            ('i-liability', 'Bodily Injury Liability',
             'Protects you if you harm or kill someone while driving, and provides a legal defense if a lawsuit is filed against you.',
             'It covers injury to people, not your vehicle.'),
            ('i-medical', 'Medical Payments (PIP)',
             'No-fault personal injury protection pays the medical expenses of the injured driver and passengers in your car. There may also be coverage if you&rsquo;re hit by a car.', None),
            ('i-shield', 'Uninsured Motorists', 'Pays for your injuries caused by an uninsured driver.', None),
            ('i-key', 'Comprehensive Physical Damage',
             'Pays for damage to your car from flood, fire or animals, plus transportation expenses if your insured vehicle is stolen.', None),
            ('i-car', 'Collision',
             'Covers your car when it collides with another vehicle or object. Collision losses are paid regardless of fault.',
             'To keep your premiums low, take the highest deductible you can afford to pay out of pocket.'),
            ('i-home', 'Property Damage Liability',
             'Protects you if your car damages someone else&rsquo;s property, and provides a legal defense if another party sues you.', None),
            ('i-receipt', 'Rental Car Reimbursement',
             'Pays car rental expenses while your car is being repaired because of an accident.', None),
        ],
        'related': ['homeowners-insurance', 'boat-insurance', 'personal-umbrella-insurance'],
    },
    {
        'slug': 'boat-insurance', 'name': 'Boat Insurance', 'short': 'boat insurance', 'draft': False,
        'meta': 'Boat insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Liability, physical damage, medical payments and uninsured boaters coverage, explained before you buy.',
        'og': 'Boat insurance as ready for the water as you are. From an independent agency in Hazlet, NJ.',
        'h1': ('Boat insurance', 'as ready for the water as you are.'),
        'lead': 'Whether it&rsquo;s the Shore or the bay, a boat owner&rsquo;s policy brings together the coverages you need on the water, and we&rsquo;ll show you exactly what yours includes.',
        'cta': 'Get Boat Insurance Quote',
        'contact': 'Anything else we should know, like its length, where you keep it and how you use it.',
        'photo': (BOAT, 'A white motor yacht with people on deck, cruising on open water'),
        'overview': {
            'kicker': 'A combination of coverages',
            'text': 'Most boat owner&rsquo;s policies provide coverage for <em>liability, physical damage and medical payments.</em>',
            'tiles': [('i-liability', 'Liability'), ('i-boat', 'Physical damage'), ('i-medical', 'Medical payments')],
        },
        'covered_title': 'Additional coverages often include:',
        'covered_kicker': 'Keeping you protected',
        'cover_photo': BOAT_SEA,
        'covered': [
            ('i-shield', 'All-Risk Protection',
             'Most boat owner&rsquo;s policies are written on an all-risk basis: the insurer pays for any direct physical loss or damage to the covered property, except what the policy specifically excludes.',
             'We&rsquo;ll show you exactly what those exclusions are.'),
            ('i-liability', 'Uninsured Boaters',
             'Compensates you for bodily injury damages you&rsquo;re legally entitled to after an accident with an uninsured boater.', None),
            ('i-phone', 'Emergency Service', None, None),
            ('i-lifebuoy', 'Life Salvage', None, None),
            ('i-wrench', 'Repairs After a Loss', None, None),
            ('i-medical', 'Emergency First Aid', None, None),
        ],
        'covered_foot': 'Other additional coverages are offered for an additional premium.',
        'related': ['auto-insurance', 'personal-umbrella-insurance', 'homeowners-insurance'],
    },
    {
        'slug': 'personal-umbrella-insurance', 'name': 'Personal Umbrella Insurance', 'short': 'personal umbrella insurance', 'draft': False,
        'meta': 'Personal umbrella insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Extra liability coverage above your home and auto policies, to protect your savings and future earnings.',
        'og': 'An extra layer over everything else. Personal umbrella insurance from an independent agency in Hazlet, NJ.',
        'h1': ('An extra layer', 'over everything else.'),
        'lead': 'Personal umbrella insurance provides additional liability coverage above the limits of your homeowners and auto insurance policies. It can also cover claims your other liability policies may exclude.',
        'cta': 'Get Personal Umbrella Quote',
        'contact': 'Tell us which policies you have now (home, auto, boat) and how much extra coverage you have in mind.',
        'photo': (HOUSE, 'A brick family home with a green lawn under a blue sky'),
        'overview': {
            'kicker': 'Above your other policies',
            'text': 'Umbrella coverage sits <em>on top of</em> the liability limits of the policies you already have.',
            'tiles': [('i-home', 'Above your homeowners limits'), ('i-car', 'Above your auto limits'), ('i-shield', 'Claims other policies exclude')],
        },
        'covered_title': 'When do you need umbrella insurance?',
        'covered_kicker': 'Protecting what you&rsquo;ve built',
        'covered_intro': 'If you&rsquo;re found liable for a major catastrophe, a jury could order you to pay a settlement reaching into the millions of dollars. A lawsuit like that could wipe out your possessions and your future earnings.',
        'cover_photo': FAMILY_BEACH,
        'covered': [
            ('i-home', 'Your Current Assets', 'An umbrella policy is designed to protect what you own today.', None),
            ('i-dollar', 'Your Future Earnings', 'It&rsquo;s also designed to protect what you&rsquo;ll earn in the years ahead.', None),
            ('i-layers', 'Gaps in Other Policies', 'It can cover some claims your homeowners and auto liability policies exclude.', None),
        ],
        'related': ['commercial-umbrella-insurance', 'homeowners-insurance', 'auto-insurance'],
    },
    {
        'slug': 'renters-insurance', 'name': 'Renters Insurance', 'short': 'renters insurance', 'draft': True,
        'meta': 'Renters insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Protect your belongings and liability, and bundle with auto to save.',
        'og': 'Your landlord covers the building. Renters insurance covers your things.',
        'h1': ('Renters insurance', 'protects what&rsquo;s yours.'),
        'lead': 'Your landlord&rsquo;s policy covers the building. It doesn&rsquo;t cover your things. Renters insurance does, usually for less than you&rsquo;d expect.',
        'cta': 'Get Renters Quote',
        'photo': (MOVING, 'A laughing little boy riding in a moving box pushed by his dad'),
        'overview': {
            'kicker': 'Select one or bundle',
            'text': 'Select renters insurance on its own, or <em>bundle it with auto</em> and save.',
            'tiles': [],
        },
        'covered_title': 'Renters insurance typically covers:',
        'covered_kicker': 'Keeping you protected',
        'cover_photo': RENTERS_HOME,
        'covered': [
            ('i-sofa', 'Personal Property', 'Your furniture, electronics, clothing and other belongings.', None),
            ('i-liability', 'Personal Liability', 'If someone is injured in your rental, or you accidentally damage someone else&rsquo;s property.', None),
            ('i-receipt', 'Additional Living Expenses', 'Help with costs if a covered loss makes your rental unlivable.', None),
        ],
        'related': ['condo-insurance', 'homeowners-insurance', 'auto-insurance'],
    },
    {
        'slug': 'condo-insurance', 'name': 'Condo Owners Insurance', 'short': 'condo insurance', 'draft': True,
        'meta': 'Condo insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Cover your unit, belongings and liability where the association&rsquo;s master policy stops.',
        'og': 'Your association covers the building. What&rsquo;s inside your walls is up to you.',
        'h1': ('What&rsquo;s inside your walls', 'is up to you.'),
        'lead': 'Your association&rsquo;s master policy covers the building and common areas. Condo insurance fills the gap.',
        'cta': 'Get Condo Quote',
        'photo': (CONDO_BUILDING, 'A modern condo building with glass balconies at sunset'),
        'overview': {
            'kicker': 'Select one or bundle',
            'text': 'Select condo insurance on its own, or <em>bundle it with auto</em> and save.',
            'tiles': [],
        },
        'covered_title': 'Condo insurance typically covers:',
        'covered_kicker': 'Keeping you protected',
        'cover_photo': CONDO_ROOM,
        'covered': [
            ('i-building', 'Your Unit&rsquo;s Interior', 'Walls, floors, fixtures and improvements you&rsquo;ve made.', None),
            ('i-sofa', 'Personal Property', 'Your belongings inside the unit.', None),
            ('i-liability', 'Personal Liability', 'If someone is injured in your unit.', None),
            ('i-receipt', 'Loss Assessment', 'Your share of certain costs the association passes on to owners after a covered loss.', None),
        ],
        'related': ['homeowners-insurance', 'renters-insurance', 'auto-insurance'],
    },
    {
        'slug': 'life-insurance', 'name': 'Life Insurance', 'short': 'life insurance', 'draft': True,
        'meta': 'Life insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Compare term and permanent life insurance, explained in plain English.',
        'og': 'Keep looking after the people you love. Life insurance from an independent agency in Hazlet, NJ.',
        'h1': ('Keep looking after the people you love,', 'even when you can&rsquo;t be there.'),
        'lead': 'That&rsquo;s what life insurance is for. We&rsquo;ll help you understand your options in plain English.',
        'cta': 'Get Life Insurance Quote',
        'contact': 'Tell us who you want to protect and roughly how much coverage you have in mind.',
        'photo': (FAMILY_BEACH, 'A large family holding hands on the beach at sunset'),
        'overview': {
            'kicker': 'Why people buy it',
            'text': 'Common reasons people buy <em>life insurance:</em>',
            'tiles': [('i-dollar', 'Replacing income for your family'), ('i-home', 'Paying off a mortgage or debts'),
                      ('i-receipt', 'Covering final expenses'), ('i-cap', 'Funding a child&rsquo;s education')],
        },
        'covered_title': 'Types we can help you compare:',
        'covered_kicker': 'Term or permanent',
        'cover_photo': LIFE_FAMILY,
        'covered': [
            ('i-clock', 'Term Life', 'Coverage for a set number of years.', None),
            ('i-infinity', 'Permanent Life', 'Lifelong coverage that may build cash value.', None),
        ],
        'related': ['health-insurance', 'personal-umbrella-insurance'],
    },
    {
        'slug': 'health-insurance', 'name': 'Health Insurance', 'short': 'health insurance', 'draft': True,
        'meta': 'Health insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Compare individual and family plans and understand what each one covers.',
        'og': 'Health plans are confusing on purpose. We&rsquo;re not.',
        'h1': ('Health plans are confusing on purpose.', 'We&rsquo;re not.'),
        'lead': 'We&rsquo;ll help you compare individual and family options and understand what each plan really covers before you choose.',
        'cta': 'Get Health Insurance Quote',
        'contact': 'Tell us who needs coverage (just you, or your family) and anything you need the plan to include.',
        'photo': (HEALTH_PEDIATRIC, 'A mother holding her baby during a visit to the pediatrician'),
        'overview': None,
        'covered_title': 'Plans we can help you compare:',
        'covered_kicker': 'Individual or family',
        'cover_photo': HEALTH_VISIT,
        'covered': [
            ('i-people', 'Individual Plans', '[Copy to come: what an individual plan covers]', None),
            ('i-heart', 'Family Plans', '[Copy to come: what a family plan covers]', None),
        ],
        'related': ['life-insurance', 'pet-insurance'],
    },
    {
        'slug': 'pet-insurance', 'name': 'Pet Insurance', 'short': 'pet insurance', 'draft': True,
        'meta': 'Pet insurance in New Jersey from The Fig Leaf Agency in Hazlet, NJ. Help with vet bills when your dog or cat is sick or injured.',
        'og': 'They&rsquo;re family. Pet insurance from an independent agency in Hazlet, NJ.',
        'h1': ('They&rsquo;re family.', 'Vet bills can arrive without warning.'),
        'lead': 'Pet insurance helps cover the cost of care when your dog or cat is sick or injured.',
        'cta': 'Get Pet Insurance Quote',
        'contact': 'Tell us about your pet: the type, breed and age.',
        'photo': (PET_SOFA, 'A smiling woman hugging her dog on the sofa at home'),
        'overview': None,
        'covered_title': 'Pet insurance plans typically cover:',
        'covered_kicker': 'Keeping them protected',
        'cover_photo': PET_VET,
        'covered': [
            ('i-paw', 'Accidents', '[Copy to come]', None),
            ('i-medical', 'Illnesses', '[Copy to come]', None),
            ('i-heart', 'Routine Wellness Care', '[Copy to come]', 'Available as an add-on with some plans.'),
        ],
        'related': ['health-insurance', 'life-insurance'],
    },
]
BY_SLUG = {s['slug']: s for s in SERVICES}
NAMES = {**{s['slug']: s['name'] for s in SERVICES},
         'homeowners-insurance': 'Homeowners Insurance',
         'commercial-umbrella-insurance': 'Commercial Umbrella Insurance'}
# footer and menu entries that are plain text in the source pages
SPAN_NAMES = {'Renters Insurance': 'renters-insurance', 'Condo Owners Insurance': 'condo-insurance',
              'Health Insurance': 'health-insurance', 'Life Insurance': 'life-insurance', 'Pet Insurance': 'pet-insurance'}


def img(src, alt, w, h, up, extra=''):
    url = src if src.startswith('http') else up(src)
    return f'<img src="{url}" alt="{alt}" width="{w}" height="{h}" decoding="async"{extra}>'


def icon(i):
    return f'<svg class="icon" aria-hidden="true"><use href="#{i}"></use></svg>'


def hero(s, up):
    """The title band, in the markup of the Homeowners hero."""
    src, alt = s['photo']
    if src:
        photo = f'<figure class="pg-head__photo">{img(src, alt, 430, 483, up)}</figure>'
    else:
        photo = (f'<figure class="pg-head__photo pg-head__photo--todo"><span>{alt}</span></figure>')
    draft = ('\n          <p class="pg-draft">Draft copy · for the agency to confirm</p>' if s['draft'] else '')
    a, b = s['h1']
    return f'''<!-- Title band -->
    <header class="fl-grid-host pg-head">
      <div class="fl-grid fl-grid--light" aria-hidden="true"><span class="fl-grid__lines" data-hs-px="0.15"></span></div>
      <div class="hs-px" aria-hidden="true"><span class="hs-px__layer hs-px__blob hs-px__blob--a" data-hs-px="0.2"></span></div>
      <div class="pg-wrap pg-head__grid">
        <div>{draft}
          <h1 class="pg-head__title" id="pg-title">{a} <span>{b}</span></h1>
          <p class="pg-head__lead">{s['lead']}</p>
          <div class="pg-head__actions">
            <a class="pg-btn pg-btn--primary" href="#quote">{s['cta']}</a>
            <a class="pg-call" href="tel:+19088623447">{icon('i-phone')}Call (908) 862-3447</a>
          </div>
        </div>
        {photo}
      </div>
    </header>'''


def overview(s, up=None):
    o = s['overview']
    if not o:
        return ''
    tiles = ''
    if o['tiles']:
        photos = TILE_PHOTOS.get(s['slug'])
        if photos:
            lis = '\n'.join(f'              <li class="pg-peril">{img(src, alt, 900, 600, up, " loading=\"lazy\"")}'
                             f'<span class="pg-peril__label">{icon(i)}{t}</span></li>'
                             for (i, t), (src, alt) in zip(o['tiles'], photos))
        else:
            lis = '\n'.join(f'              <li>{icon(i)}{t}</li>' for i, t in o['tiles'])
        tiles = (f'\n          <ul class="pg-perils pg-perils--n{len(o["tiles"])}" aria-label="{s["name"]}">\n{lis}\n            </ul>')
    solo = '' if o['tiles'] else ' pg-overview--solo'
    return f'''<section class="pg-sec" id="overview" aria-labelledby="pg-overview-title">
      <div class="pg-wrap">
        <div class="pg-sec__head">
          <h2 class="pg-sec__title" id="pg-overview-title">{s['name']}</h2>
          <p class="pg-sec__kicker">{o['kicker']}</p>
        </div>
        <div class="pg-overview{solo} hs-reveal">
          <p class="pg-overview__text">{o['text']}</p>{tiles}
        </div>
      </div>
    </section>
'''


def covered(s, up, href):
    items = []
    for n, (i, title, text, note) in enumerate(s['covered'], 1):
        photo = ''
        if n == 1 and s['cover_photo']:
            photo = f'<figure class="pg-cover__photo">{img(s["cover_photo"], "", 430, 483, up, " loading=\"lazy\"")}</figure>'
        body = text or ''
        if note:
            body += f'<span class="pg-cover__note">{note}</span>'
        p = f'<p>{body}</p>' if body else ''
        items.append(f'<li class="pg-cover hs-reveal">{photo}<span class="pg-cover__num" aria-hidden="true">{n:02d}</span>'
                     f'<span class="pg-cover__icon" aria-hidden="true">{icon(i)}</span>'
                     f'<h3 class="pg-cover__title">{title}</h3>{p}</li>')
    plain = '' if s['cover_photo'] else ' pg-bento--plain'
    intro = f'\n        <p class="pg-sec__intro">{s["covered_intro"]}</p>' if s.get('covered_intro') else ''
    foot = f'\n        <p class="pg-foot">{s["covered_foot"]}</p>' if s.get('covered_foot') else ''
    links = ''.join(f'<li><a href="{href(r)}">{NAMES[r]}{icon("i-arrow")}</a></li>' for r in s['related'])
    return f'''<section class="pg-sec" id="covered" aria-labelledby="pg-covered-title">
      <div class="pg-wrap">
        <div class="pg-sec__head">
          <h2 class="pg-sec__title" id="pg-covered-title">{s['covered_title']}</h2>
          <p class="pg-sec__kicker">{s['covered_kicker']}</p>
        </div>{intro}
        <ol class="pg-bento pg-bento--n{len(s['covered'])}{plain}">
          {(chr(10) + '          ').join(items)}
        </ol>{foot}
        <nav class="pg-related" aria-label="Related coverage">
          <h3 class="pg-related__head">Related coverage</h3>
          <ul>{links}</ul>
        </nav>
      </div>
    </section>
'''


def quote(s, homeowners_quote, up):
    """The Homeowners quote section with this page's words and photo."""
    q = homeowners_quote
    q = q.replace('Get your homeowners quote', f'Get your {s["short"]} quote', 1)
    # the agent going over a house with a couple, or the page's own photo
    talk_src, talk_alt = TALK_PHOTOS.get(s['slug'], (AGENT, 'An agent with a tablet showing a couple something on their house'))
    talk_url = talk_src if talk_src.startswith('http') else up(talk_src)
    q = q.replace('<img src="../assets/homeowners/home-cta.jpg" alt="A laughing little boy riding in a moving box pushed by his dad" width="800" height="800"',
                  f'<img src="{talk_url}" alt="{talk_alt}" width="416" height="483"', 1)
    old = 'For more information about homeowners insurance, condominium insurance and renters insurance, call us and an agent will run the quote with you.'
    assert old in q
    if s.get('contact'):
        q = q.replace(old, f'For more information about {s["short"]}, call us and an agent will run the quote with you. '
                      'Or send the form and an agent will get back to you to go over the details.', 1)
        return contact_form(s, q)
    q = q.replace(old, f'For more information about {s["short"]}, call us and an agent will run the quote with you. '
                  'Online, the quote takes about 3&ndash;5 minutes, and an agent follows up to walk you through it.', 1)
    return q


# Insurance types for the contact form's menu (the page's own is selected).
# Auto, Homeowners, Renters and Condo go through the Consumer Rate Quotes form,
# so the menu lists the personal lines it doesn't cover.
CONTACT_TYPES = ['Boat Insurance', 'Personal Umbrella Insurance', 'Life Insurance', 'Health Insurance', 'Pet Insurance', 'Something else']
CONTACT_EMAIL = 'quotes@figleafagency.com'


def contact_form(s, q):
    """The quote section with a contact form in place of the Consumer Rate
    Quotes iframe, for the pages that form doesn't cover. Same card, same
    bar; the form posts to data-endpoint once there is one (see
    homepages/shared/contact-form.js) and opens an email until then."""
    import re
    opts = ''.join(f'\n                  <option{" selected" if t == s["name"] else ""}>{t}</option>' for t in CONTACT_TYPES)
    uid = s['slug'].split('-')[0]
    f = lambda n: f'cf-{uid}-{n}'
    card = f'''<!-- {s["name"]} isn't on the Consumer Rate Quotes form, so this page
             has a short contact form in its place. homepages/shared/contact-form.js
             sends it: set data-endpoint below to the form service's URL to have it
             post there; until then it opens an email to {CONTACT_EMAIL}. -->
        <div class="pg-crq pg-crq--contact">
          <div class="pg-crq__card">
            <div class="pg-crq__bar">
              <span class="pg-crq__secure">{icon('i-lock')}Quote request</span>
              <span class="pg-crq__alt">Prefer email? <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></span>
            </div>
            <form class="pg-contact" data-contact-form data-endpoint="" data-mailto="{CONTACT_EMAIL}" method="post" novalidate>
              <p class="pg-contact__intro">{s["short"][0].upper() + s["short"][1:]} quotes are done one-on-one. Send us a few details and an agent will get back to you to put yours together.</p>
              <div class="pg-contact__grid">
                <div class="pg-field">
                  <label for="{f('name')}">Full name</label>
                  <input id="{f('name')}" name="name" type="text" autocomplete="name" required>
                </div>
                <div class="pg-field">
                  <label for="{f('type')}">Insurance type</label>
                  <select id="{f('type')}" name="insurance_type">{opts}
                  </select>
                </div>
                <div class="pg-field">
                  <label for="{f('email')}">Email</label>
                  <input id="{f('email')}" name="email" type="email" autocomplete="email" required>
                </div>
                <div class="pg-field">
                  <label for="{f('phone')}">Phone</label>
                  <input id="{f('phone')}" name="phone" type="tel" autocomplete="tel" required>
                </div>
                <fieldset class="pg-contact__more" data-show-for="Boat Insurance"{'' if s['name'] == 'Boat Insurance' else ' hidden disabled'}>
                  <legend>Your boat</legend>
                  <div class="pg-field">
                    <label for="{f('boat-year')}">Year</label>
                    <input id="{f('boat-year')}" name="boat_year" type="text" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required>
                  </div>
                  <div class="pg-field">
                    <label for="{f('boat-make')}">Make</label>
                    <input id="{f('boat-make')}" name="boat_make" type="text" required>
                  </div>
                  <div class="pg-field">
                    <label for="{f('boat-model')}">Model</label>
                    <input id="{f('boat-model')}" name="boat_model" type="text" required>
                  </div>
                </fieldset>
                <div class="pg-field pg-field--wide">
                  <label for="{f('message')}">Message <span>(optional)</span></label>
                  <textarea id="{f('message')}" name="message" rows="4" placeholder="{s['contact']}"></textarea>
                </div>
              </div>
              <div class="pg-contact__trap" aria-hidden="true"><label>Leave this empty <input name="company_website" type="text" tabindex="-1" autocomplete="off"></label></div>
              <div class="pg-contact__foot">
                <button class="pg-btn pg-btn--primary" type="submit">Send My Request</button>
                <p class="pg-contact__status" role="status" aria-live="polite"></p>
              </div>
            </form>
          </div>'''
    q, n = re.subn(r'<!-- The quote form is.*?-->\s*<div class="pg-crq">\s*<div class="pg-crq__card">.*?</iframe>\s*</div>\s*</div>',
                   lambda m: card, q, count=1, flags=re.S)
    assert n == 1
    return q

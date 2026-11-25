"""The carriers on figleafagency.com/carriers/ (read 25 Nov 2026), for the
build pages' Carriers page (carriers_page() in build.py).

One entry per carrier and line. The live page has a card for each carrier and
line (30 cards); where a carrier's Auto and Homeowners cards share the same
claim, payment and phone details they are merged into one card here, with
both lines as tags. Logos are the live site's own files.
"""

UP = 'https://figleafagency.com/wp-content/uploads/'

# (name, logo file, lines, claim url, pay url, customer service phone)
CARRIERS = [
    ('American Collectors Insurance', 'provider_logo_american_collectors_insurance.png', ['auto'],
     'https://americancollectors.com/filing-a-claim/', 'https://member.americancollectors.com/login', '866-422-9498'),
    ('American Modern', 'provider_logo_american_modern-300x129.png', ['surplus'],
     'https://myclaim.amig.com/claim', 'https://amig.com/customer/make-a-payment/', '855-469-2644'),
    ('Bristol West', 'provider_logo_bristol_west-300x129.png', ['auto'],
     'https://www.bristolwest.com/home/claims/', 'https://www.bristolwest.com/payments/', '888-888-0080'),
    ('Cabrillo Coastal', 'provider_logo_cabrillo_coastal-300x129.png', ['surplus'],
     'https://cabgen.com/after-a-loss/', 'https://insured.cabgen.com/payment/', '866-896-7233'),
    ('Cabrillo Coastal', 'provider_logo_cabrillo_coastal-300x129.png', ['home'],
     'https://cabgen.com/policyholders/', 'https://insured.cabgen.com/payment/', '866-896-7233'),
    ('Cincinnati Insurance', 'provider_logo_cincinnati-300x129.png', ['home'],
     'https://www.cinfin.com/cincinnati-insurance-claims',
     'https://onlineservice.cinfin.com/b2c/Account_Self_Service/QuickPayment.aspx?billpaytype=PLD', '888-242-8811'),
    ('Cumberland Insurance Group', 'provider_logo_cumberland_insurance_group-300x129.png', ['home'],
     'https://www.cumberlandmutual.com/report-a-claim/', 'https://www.cumberlandmutual.com/make-a-payment/', '856-451-4050'),
    ('CURE', 'provider_logo_cure-300x129.png', ['auto'],
     'https://www.cure.com/claims', 'https://payments.cure.com/', '800-535-2873'),
    ('Foremost', 'provider_logo_foremost-300x129.png', ['auto', 'home'],
     'https://www.foremost.com/contact/', 'https://www.foremost.com/portal.asp', '800-237-2060'),
    ('Foremost STAR', 'provider_logo_foremost_star-300x129.png', ['home'],
     'https://www.foremost.com/contact/', 'https://www.foremost.com/portal.asp', '800-237-2060'),
    ('Franklin Mutual', 'provider_logo_franklin_mutual-300x129.png', ['home'],
     'https://www.fmiweb.com/html/property.cfm', 'https://www.fmiweb.com/html/payments.html', '800-336-3642'),
    ('Great Bay', 'provider_logo_great_bay-300x129.png', ['home'],
     'https://greatbayinsurancegroup.com/report-a-claim/', 'https://greatbayinsurancegroup.com/contact/payment-inquiry/', '609-535-8000'),
    ('Hagerty', 'provider_logo_hagerty-300x129.png', ['auto'],
     'https://www.hagerty.com/insurance/claims', 'https://login.hagerty.com/', '800-922-4050'),
    ('Jimcor', 'provider_logo_jimcor-300x129.png', ['surplus'],
     'https://www.jimcor.com/claims', 'https://www.jimcor.com/make-a-payment', '201-573-8200'),
    ('Mercury Insurance', 'provider_logo_mercury_insurance-300x129.png', ['auto', 'home'],
     'https://www.mercuryinsurance.com/claims/', 'https://www.mercuryinsurance.com/myaccount/', '800-503-3724'),
    ('MSI', 'provider_logo_msi-300x129.png', ['surplus'],
     'https://apps.msimga.com/fileaclaim', 'https://msimga.com/make-a-payment/', '844-788-0873'),
    ('National General', 'provider_logo_national_general-300x129.png', ['auto', 'home'],
     'https://claims.nationalgeneral.com/report', 'https://nationalgeneral.com/policyholders/my-policy/', '888-325-1190'),
    ('Orchid', 'provider_logo_orchid-300x129.png', ['surplus'],
     'https://orchidinsurance.com/claims/', 'https://orchidinsurance.com/apps/paymentlookup/', '866-370-6505'),
    ('Plymouth Rock', 'provider_logo_plymouth_rock-300x129.png', ['auto'],
     'https://efnolmod.plymouthrock.com/', 'https://www.plymouthrock.com/customer-service/manage-policy', '844-346-1225'),
    ('Plymouth Rock', 'provider_logo_plymouth_rock-300x129.png', ['home'],
     'https://www.plymouthrock.com/claims', 'https://www.plymouthrock.com/customer-service/manage-policy', '844-242-3555'),
    ('Progressive', 'provider_logo_progressive-300x129.png', ['auto'],
     'https://www.progressive.com/claims/', 'https://www.progressive.com/manage-policy/', '888-671-4405'),
    ('Providence Mutual', 'provider_logo_providence_mutual-300x129.png', ['home'],
     'https://www.providencemutual.com/claims-billing', 'https://mypmfic.com/policyholder/login', '877-763-1800'),
    ('Steadily', 'provider_logo_steadily.png', ['surplus'],
     'https://www.steadily.com/claims', 'https://pay.steadily.com/', '888-966-1611'),
    ('Swyfft', 'provider_logo_swyfft.png', ['surplus'],
     'https://www.swyfft.com/claims/', 'https://swyfft.com/MakeAPayment', '855-479-9338'),
    ('The Philadelphia Contributionship', 'provider_logo_philadelphia_contributionship.png', ['home'],
     'https://1752.com/submit-a-claim/', 'https://mykey.contributionship.com/', '888-627-1752'),
    ('Travelers', 'provider_logo_travellers.png', ['auto', 'home'],
     'https://www.travelers.com/claims', 'https://www.travelers.com/online-service', '888-564-5043'),
]

LINES = [('auto', 'Auto'), ('home', 'Homeowners'), ('surplus', 'Surplus')]

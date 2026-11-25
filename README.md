# The Fig Leaf Agency website

Plain HTML, CSS and JavaScript, no build step. Live at https://fig-leaf-concepts.vercel.app/.

This is the one site, made from build 5 (the client-approved layout) on 25 Nov 2026, with the approved wording
and the option B headings. The earlier builds, concepts, archives, gallery and client review tools were removed
then. They are still in the git history if anything needs to be looked up (`git log -- build-1`).

## Pages

- `index.html`: the homepage
- `about/` with the team bios and `about/testimonials/`
- `carriers/`: claims and payments by carrier
- Personal insurance: `auto-insurance/`, `homeowners-insurance/`, `renters-insurance/`, `condo-insurance/`,
  `boat-insurance/`, `personal-umbrella-insurance/`, `health-insurance/`, `life-insurance/`, `pet-insurance/`
- Business insurance: `commercial-auto-insurance/`, `workers-comp-insurance/`, `general-liability-insurance/`,
  `commercial-umbrella-insurance/`, `employee-benefits/`, `contractors-policies/`
- `crq/`: the quote request page, and `crq-form/`: the quote form on its own (every Get a Quote button goes here)
- `checklist/`: "Still needed from the agency", not linked from the site. Ticks are kept in each browser.

## Quick-links bar

A slim bar above the header on every page has three buttons: AC (`/checklist/`), GC (`/crq-form/`) and Site
(the homepage), with the current one highlighted. Its markup is at the top of each page's `<body>`, and its look is
`.review-bar` in the stylesheets plus a pill tweak in `assets/shared/approved.css`.

## Shared files

- `assets/home/`: the main stylesheets and scripts, logo and badges
- `assets/pages/`: the inner pages' stylesheets and scripts
- `assets/shared/`: the approved-layout styles and the shared scripts (office status, floating buttons,
  contact form, About and Carriers), with photos and the testimonial video in `assets/shared/assets/`
- `assets/hero/`: the homepage hero's layout and photos
- `assets/photos/`: the car, home, boat and business photos

## Office status and announcements

The open/closed badge and the announcements bell in the top bar read their settings from
`assets/shared/office-config.js`, the one file to edit for hours, closures and news. Preview with
`?office=open`, `?office=snow`, `?office=holiday`, `?office=night`, or `?news=reset`.

## Old links

`vercel.json` sends the old review links to the one site: `/build-1/` to `/build-5/` go to the same page here,
`/archive-d/` goes to `/checklist/`, and the old concept and archive pages go to the homepage.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

Business photos on the Business Insurance pages are Adobe Stock picks; the business photo in `assets/photos/` is
from Unsplash, [ZmzH-M7B6Vk](https://unsplash.com/photos/red-building-ZmzH-M7B6Vk), under the Unsplash License.

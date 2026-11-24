# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens the photo gallery (`archive-d/`);
each `build-N/`, `concept-N/` or `archive-X/` folder is one page:

- `archive-a/`, `archive-b/`: homepage concepts
- `archive-c/`: archive B with the horizontal leaves hero (from the old concept 1) and archive A's Google Reviews layout (`hs-reviews--split`)
- `archive-a/homeowners-insurance/`, `archive-b/…`, `archive-c/…`: the Homeowners Insurance page in each concept
  (content from figleafagency.com/homeowners-insurance). These are interior pages: solid dark header, a light title
  band and a document layout instead of the homepage's dark hero, in the concept's colours and type.
  Styles in `insurance-page.css`, archive B's in-place tabs and archive C's section highlighting in `insurance-page.js`; the `pg--v1` / `pg--v2` / `pg--v3`
  class on `<main>` picks the layout. Linked from the header under Personal Insurance.
- `archive-b/homeowners-insurance-scroll/`: archive B's Homeowners page without tabs; the same sections stacked
  (quote first) so the page scrolls. For comparing with the tabbed version.
- `archive-b/homeowners-insurance-fade/`: the tabbed archive B Homeowners page with a title band that continues the
  header's black and fades into the light page (`pg--fade`), instead of a hard black-to-white edge.
- `archive-a/crq/`, `archive-b/crq/`, `archive-c/crq/`: the quote request page (figleafagency.com/crq). The form is the same
  Consumer Rate Quotes iframe the live page uses (we can't style inside it), framed in each concept's look.
  Styles in `quote-page.css`; the `qp--v1` / `qp--v2` / `qp--v3` class on `<main>` picks the look. Reached from the review bar.
- `archive-a/crq-form/`, `archive-b/…`, `archive-c/…`: the quote form on its own, the same iframe exactly as it looks live,
  between each concept's header and footer (no extra copy). Styles in `quote-page.css` (`.qp-plain`).
  Every Get a Quote / Start My Quote button links here.
- `hero-concepts/`: four hero directions without the fig leaf artwork, same interaction (hover, tap or focus the car,
  home or boat). `a` opening photo panels and `c` uncover lens are horizontal; `b` stacked bands and `d` card deck are vertical.
  Built from Archive A's homepage by `hero-concepts/build.py`; the layouts are `shared/hero-x.css`, the behaviour `shared/hero-x.js`.
- `hero-ideas/`: six replacement hero pictures with the same interactive hero, three vertical (`v1`–`v3`, on Archive A)
  and three horizontal (`h1`–`h3`, on Archive C). `hero-ideas/index.html` shows them side by side; each page reuses its
  concept's CSS, scripts and inner pages and only swaps `hero.jpg` and the hotspot positions. Sources in `hero-ideas/_source/`.
- `archive-d/`: the photo gallery
- `archive-e/`: **Daylight**. A black header and hero (the client's preference) with the agency's studio fig leaf (gallery leaf 1) inside gold rings, labels for Auto, Home, Boat and Business around it, and a headline whose last word rotates through car, home, boat and business. The leaf's tip points at the cursor wherever it is. The car, house and boat photos show through the big leaf in its shape (`assets/leaf-mask.png`), in step with the headline; pointing at a label jumps to it. Below the hero the page is light, with sections in the rounded tile layout (`hs--v5`) and a dark green footer. Its own Homeowners and quote pages.
- `concept-1/`: **Leaf slideshow**. The hero is one big Fig Leaf (the logo's leaf, `assets/fig-leaf-fill.svg`, larger than the hero art on any other concept) used as a frame: photos of a car, a house and a boat slide through it every few seconds, with a gold edge and a dark green offset leaf behind it. The headline matches the other concepts, "We cover your car.", and its last word changes in step with the photo (car, home, boat). Arrows, dots, a pause button, swipe and the arrow keys move it by hand (`concept.js`). Header, sections (`hs--v2`), footer and the inner pages use archive C's look. Its own Homeowners and quote pages.

**Client review ticks**: every page loads `review/review.js`, which puts a small ✓ / ✕ / comment
tick on each section and a "Your review" panel in the bottom corner for sending the picks. Setup and the optional
Google Sheet collection are in `review/google-sheet-setup.md`. `?review=off` hides them.

Archive A is the dark theme. `archive-a/palette.css` loads last on all its pages (home, Homeowners, both quote
pages) and holds them to four colours, one shade each: gold #e8c27e, black #070d0f, white #fff and dark green
#17402b, plus a light green #a9c7b4 used sparingly. No gradients, see-through colours or soft shadows, except the
faint fig leaf silhouettes in the background, which use archive B's leaf green #3f8a5a. It overrides
the shared stylesheets for archive A only, so those stay identical copies.

Archive B uses the same palette: `archive-b/palette.css` loads last on all its pages and holds them to gold, black,
white and dark green, with light green used sparingly, and no gradients, glows or soft shadows. The exceptions are the
leaf silhouettes, which keep their own greens, and the grid behind "Select One or Bundle!".

Archive C uses the same palette too: `archive-c/palette.css` loads last on all its pages (home, Homeowners, both quote pages). Its homepage shares archive B's rules. The Homeowners guide page gets a white title band with a solid gold top stripe, flat cards with light green edges, accordion icons with no tile behind them, and a solid dark green quote panel. The gradient rules beside headings are now solid gold.

The homepage concepts share the sections in `home-sections.css` / `home-sections.js`
(identical copies in each folder); the `hs--v1` / `hs--v2` class on `#home-sections`
picks the section layout.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

**Grid background (`grid.css`).** The faint grid from archive B's "Select One or Bundle" section is now a reusable layer, with an identical `grid.css` in archives A, B and C and concepts 1 and 2. A section gets the class `fl-grid-host` and a first child `<div class="fl-grid" aria-hidden="true"><span class="fl-grid__lines" data-hs-px="0.15"></span></div>`. Add `fl-grid--light` for green lines on light sections. It's used on archive A's Comprehensive Coverage, Select One or Bundle and More Ways We Protect You sections, on archive C's Comprehensive Coverage and More Ways We Protect You sections, and on the title area of every Homeowners page. Archive A's and archive C's Homeowners pages also have it on the closing quote band.

**Concept 1 and archive E.** Both start from archive C's files and keep its content and pages. Each folder's `concept.css` loads last on all its pages
(after `palette.css`) and holds it to the same four colours (gold, black, white, dark green, light green sparingly), no gradients or soft shadows.
`concept.js` drives each hero (archive E's rotating word, concept 1's slideshow); `scene.js` isn't used there. Both use the current
logo, `assets/figleaf-logo-full.png`. Archive E's business photo (`assets/photo-business.jpg`) is from Unsplash, [ZmzH-M7B6Vk](https://unsplash.com/photos/red-building-ZmzH-M7B6Vk), under the Unsplash License. The gold line under the changing headline word is as long as the word showing (`--uw`, set by each `concept.js`).

**All heroes together (`heroes/`).** One page that links every homepage hero idea, with a screenshot of each: concepts 2 to 10, concept 1 and archive E,
the photo heroes A to D (`hero-concepts/`) and the six fig leaf pictures V1 to H3 (`hero-ideas/`).

## The current build: AC, GC and 1 to 5

The client kept concept 11. The review bar now runs AC, GC, 1, 2, 3, 4, 5:

- **AC**: the Fig Leaf photo gallery (`archive-d/`), which is also the landing page (`index.html` redirects there).
- **GC**: the Get a Quote page (`build-N/crq-form/`). It stays inside the build you came from.
- **1 to 5**: concept 11's homepage in `build-1/` to `build-5/`. They differ only in the Homeowners page:
  1 archive A's layout, 2 archive B with tabs, 3 archive B scrolling, 4 archive B with the header fade, 5 archive C's layout.
  On a Homeowners page the numbers step between the five Homeowners layouts.

**Homeowners versions 1 to 4 (from Eric's mockups, 23 Nov).** The five old layouts on the builds are replaced by four
versions cut from archive B's scrolling page, in `archive-b/homeowners-insurance-v1/` to `-v4/` (made by
`build_homeowners_versions` in `build.py`; styles in `homepages/shared/homeowners-versions.css`). Builds 1 to 4 show
versions 1 to 4 and build 5 shows version 1. On a Homeowners page the bar's numbers 1 to 4 are the four versions.

| Version | Hero | Then |
|---|---|---|
| 1 | white, light green Fig Leaf outline behind the photo | perils, what a policy covers, the quote form with "Rather talk it through?" |
| 2 | black, gold "Preserve what matters." | same as 1 |
| 3 | black, as 2 | perils, what a policy covers, black "Get a homeowners quote" band (Start My Quote + call), "Rather talk it through?" |
| 4 | black, as 2 | perils, the black quote band, what a policy covers, the quote form with "Rather talk it through?" |

The black band is build 1's quote card laid out full width. Every hero has a thin outline of the logo's fig leaf (the path from `fig-leaf-fill.svg`) behind the photo, from Eric's sketch: grey on black, light green on white. The old layouts are still in `archive-a/b/c` for the archive.

`homepages/build.py` makes them (`build_builds`, `main_bar`). Review labels are "Gallery", "Get a quote" and "Build N".

**About and bio pages.** Each build has an About page (`build-N/about/`) and a bio page for each team member under it
(`build-N/about/chris-oliveira/`), in concept 11's header, footer, colours and type (Fraunces headings, Source Sans body).
Each build shows a different design, so there are five About concepts and five bio concepts (`ABOUT_CONCEPTS` in `build.py`):

| Build | About | Bio |
|---|---|---|
| 1 | Story and values: black title band, the homepage's About picture, green values cards, team cards | Photo and details: portrait beside name, facts and contact; bio with a "Chris can help you" card |
| 2 | Then and now: drag a handle across one frame from the painting of the first office to today's team; big NYSE quote; ruled values list; round team photos | Contact card: a business card across a green band with every way to reach him and a Save contact (vCard) button |
| 3 | Editorial: light magazine layout, drop cap, painting set into the text, team photo across the page, icon tiles, team as a list | Split screen: photo fills the left half and stays put while the right half scrolls |
| 4 | Chapters: four numbered chapters beside a sticky chapter list that marks where you are, ending with Visit us | Q and A: name set huge behind an arched photo, then his bio sheet as four questions |
| 5 | By the numbers: split hero with the team photo, the homepage's three numbers, a three-step story path, values on black | Fig leaf portrait: photo cut into the fig leaf (archive E's leaf mask) on green, with number tiles |

The content is in `homepages/about/` (`about-v<N>.html`, `chris-oliveira-v<N>.html`: main content only, paths from the
repo root, `{B}` for the build folder; `_icons.html` is the extra icons every page gets). Styles: `homepages/shared/about.css`
(shared, and concept 1) plus `about-<N>.css` for builds 2 to 5; behaviour (the then/now handle, the chapter list) in
`about.js`. `build_about` in `build.py` wraps them in the build's header and footer. Team photos are in
`homepages/shared/assets/team/`. The header's About, the footer's About Us and Meet Our Team and the homepage's
"Learn More About Our Values" link to these pages on every build page. To add a bio: write
`homepages/about/<slug>-v1.html` to `-v5.html`, add it to `BIOS` in `build.py`, add a card to the team section of each
`about-v<N>.html`, and re-run the script. Screenshots are in `screenshots/about/`.
**Client review round 2 (Reviewer a9lh, 19 Nov).** Applied to the builds only (concept 11 itself is unchanged), by
`round2_home` and `round2_homeowners` in `build.py`:

- **Homepage, every build**: the hero panels run Car, Home, Business, Boat (Business and Boat swapped, headline words
  and numbers to match), and "More Ways We Protect You" has four cards: Business, Special Contractor Policies, Defensive
  Driving Course and a new Life Insurance card (`homepages/shared/assets/life-insurance.jpg`, from Unsplash,
  photo-1511895426328-dc8714191300, Unsplash License). Four across from 1200px, two by two below that (`concept-11.css`).
- **Build 1 Homeowners**: the "A homeowners policy generally covers" section is gone.
- **Build 3 Homeowners**: "A homeowners policy generally covers" is merged with build 1's quote card and its Personal
  insurance links in one full-width black band (`homepages/shared/round-2.css`).
- **Build 5 About**: the hero uses build 3's headline and intro ("Insurance, explained by people who keep their word."),
  and the agency-in-numbers band now shows build 3's "at a glance" facts (Where, What, How) instead (`about-v5.html`, `about-5.css`).

**Links stay inside the build.** `keep_links_in` in `build.py` runs on every build page and the gallery. A link to a
figleafagency.com page the build has (About, Meet Our Team, Homeowners, the quote form) opens the build's copy; every other
link that leaves the build (the live site's other pages, Google Maps and reviews, Facebook, Drive Safe Today, carriers,
folders that don't exist here) becomes `href="#"` with `onclick="return false"` and `data-offsite`, so the button or menu
item stays put but does nothing. `tel:`, `mailto:` and the review sheet are untouched. To link a new in-build page, add it to `IN_BUILD`.

Everything else (concepts 1 to 11, archives A to E) is archived: still online so old links work, with "archived · see the current build" in its bar.

## Numbering (archived concepts)

The main run is concepts 1 to 11 (`concept-1/` to `concept-11/`). The site's front page opens concept 1's Get a Quote page (`concept-1/crq-form/`); the review bar and the logo lead on to the concepts. Earlier concepts are the archive, labelled with letters so no two pages share a number: Archive A to E (`archive-a/` to `archive-e/`).

How the numbers have moved, in order: old 1 to 4 became Archive A to D and old 5 and 6 became 1 and 2, with the hero homepages following from 3; then V2, H2 and H3 on full homepages were dropped (they are still on their own at `hero-ideas/`); then concept 1 (Daylight) moved to Archive E and everything after it moved down one. `vercel.json` sends the old `homepages/<code>/` links and `concept-12/` to `concept-18/` to the page they show now, or to concept 1 for a dropped one. Links to `concept-1/` to `concept-11/` open whatever has that number now. (`concept-11/` used to redirect to concept 10; it is now the new concept 11.)

## Concept 11: built from the client review

`concept-11/` puts together what the client liked in the review sheet (Fig Leaf concept review, mostly reviewer prp9's comments).
It's built by `homepages/build.py` like concepts 2 to 10 (the `concept_11` function there), on the archive A homepage, so it has concept 2's header, sections and footer:

- **Hero**: concept 5's opening photo panels (hero A) with a fourth panel, Business ("add business here"), and "your business." in the rotating headline. The quote button is gold, as on concept 5.
- **Comprehensive Coverage**: concept 2's dark section with concept 5's movement ("likes movement, but not white background"): fig leaf silhouettes drifting with the scroll, each line lifting with a gold edge on hover, the lines coming in one after another, and the moving icons.
- **More Ways We Protect You**: three cards, with concept 2's Business insurance card.
- **About**: photo on the left, text on the right. The picture starts on the painting of the agency's old building and fades to the team photo, then they take turns while the section is on screen (`homepages/shared/concept-11.js`). The painting's sign now reads "Fig Leaf agency, Personal / Business Insurance" instead of "Walgert's agency, Real Estate / Insurance" (`homepages/shared/assets/old-building-figleaf.jpg`, edited from `archive-b/assets/old-building.jpg`).
- **Stats card**: straddles the hero and Comprehensive Coverage. `build.py` moves it to the top of the coverage section and it reaches 70px up into the hero (56px on phones), with about 95px clear between the photo panels and the card (85px on phones). The hero and the coverage section are taller to make room. `--c11-lap` and `--c11-gap` in `concept-11.css` set both.
- **Homeowners page**: concept 2's layout (archive B look, tabs), set in `HOMEOWNERS_PICK` in `build.py`.

Its own rules are in `homepages/shared/concept-11.css`, which loads last on concept 11's homepage only.

## Archive A to E

Archives A to E are still online but out of the main run. Their review bar steps through the archive only, and the heroes page lists them at the bottom. They stay because concepts 2 to 10 use the homepages (and Homeowners and quote pages) of archives A to C, and concept 2 uses archive E's hero.

## Concepts 2 to 10: every new hero on a full homepage

`concept-2/` to `concept-10/` put each new hero on one of the archived homepages, unchanged apart from the hero, and carry on the numbering from concept 1:

- 2 to 4, on the archive A homepage: archive E's pointing fig leaf hero, then V1 and V3
- 5 to 8, on the archive B homepage: photo heroes A, B, C and D
- 9 and 10, on the archive C homepage: concept 1's leaf slideshow hero, then H1

They link back to their homepage's folder for styles and images and to the hero's own files. Each has its own copy of the quote, quote form and Homeowners pages (content unchanged), so a visitor clicking the menu, the hero or the quote buttons stays inside that concept.

**Homeowners layouts.** The five Homeowners layouts take turns (`HOMEOWNERS` in `homepages/build.py`): layout 1 is archive A's page, 2 archive B's with tabs, 3 archive B's scrolling page, 4 archive B's header fade page and 5 archive C's. Concepts 1 to 5 get layouts 1 to 5, and 6 to 10 start again from layout 1. Each Homeowners page has the concept bar, 1 to 10, where each number opens that concept's Homeowners page; build.py writes concept 1's Homeowners page too. `homepages/build.py` builds them, keeps the review bar on concept 1 listing 1 to 10 and the archive's bar listing A to E; re-run it after changing a homepage or a hero. `homepages/shared/` holds archive E's and concept 1's hero styles on their own (`hero-5.css`, `hero-6.css`, named for their old numbers), the rules that give the new heroes room under the see-through header on the archive B and C homepages, and small per-hero size and position tweaks (by the `data-hero` attribute build.py puts on `<html>`).

Concept 8's card deck (hero D) has a fourth card, Business, with the headline word "business." in step; the photo (`hero-concepts/shared/business.jpg`) is archive E's business photo. The deck rules for four cards are in `hero-concepts/shared/hero-x.css` and only apply when a business card is there, so the three-card heroes are unchanged. `hero-concepts/build.py` still builds from the old concept 1, so don't re-run it; edit `hero-concepts/d/index.html` and re-run `homepages/build.py`.

Concept 2 alone adds a Business insurance card under "More Ways We Protect You" (three cards across), from `EXTRAS` in `homepages/build.py`. Its photo, `homepages/shared/assets/business-insurance.jpg`, is from Unsplash, [GFrBMipOd_E](https://unsplash.com/photos/two-women-near-tables-GFrBMipOd_E), under the Unsplash License.

**Personal insurance pages (builds 1 to 5).** Each build has Auto, Boat, Personal Umbrella, Renters, Condo, Life, Health and Pet
pages (`build-N/auto-insurance/` and so on), laid out like that build's Homeowners version: the same hero,
overview band, "generally covers" grid, quote form or band, and "Rather talk it through?" card. The copy and photos for every page
live in `homepages/service_pages.py`; `service_version()` in `homepages/build.py` swaps them into the Homeowners layout, and
`homepages/shared/service-pages.css` adds grids for other numbers of cards, the related coverage links, a "photo to come" placeholder
and the draft tag. Auto, Boat and Umbrella copy comes from the agency's content map; Renters, Condo, Life, Health and Pet are the
build brief's draft copy (marked "Draft copy" in the hero) and need the agency's review. Text in [square brackets] is a placeholder.
The header and footer links to these pages now open the build's own copies. Edit the data file, then run `python3 homepages/build.py`.

Homepage concept 5 (build 5's homepage) has a video testimonial beside the
Google reviews: a 16:9 video on the left, the written reviews two at a time
on the right (`video_reviews()` in `homepages/build.py`, styles in
`homepages/shared/video-reviews.css`). The poster is a frame from the video;
swap in the video when it arrives.

**Personal Insurance navigation (build 1).** Build 1's header menu lists all nine personal insurance pages (desktop dropdown and phone menu), the Personal Insurance link goes to the homepage's Comprehensive Coverage section (`#coverage`), and every build 1 insurance page has a breadcrumb above its title: Home / Personal Insurance / page. Made by `personal_nav()` in `homepages/build.py` (`NAV_BUILDS` picks the builds); breadcrumb styles are `.pg-crumbs` in `homepages/shared/homeowners-versions.css`.

**Headings (builds 1 to 5).** Each build page's section headings come from `homepages/headings.py`: `build.py`'s `write()` swaps the archive pages' generic headings for each page's own. Most headings have three wordings for the client to choose from: option A on builds 1 and 4, B on builds 2 and 5, C on build 3, so a review tick on a section records the wording seen. Edit a heading there (or at its source, which then wins) and re-run `python3 homepages/build.py`.

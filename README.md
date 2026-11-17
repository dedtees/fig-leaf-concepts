# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens archive E;
each `concept-N/` or `archive-X/` folder is one page:

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
- `archive-e/`: **Daylight**. A black header and hero (the client's preference) with the agency's studio fig leaf (gallery leaf 1) inside gold rings, labels for Auto, Home, Boat and Business around it, and a headline whose last word rotates through car, home, boat and business. The leaf's tip points at the cursor wherever it is, and the mouse pointer itself is a small fig leaf whose tip is the click point (`assets/leaf-cursor.png`). The car, house and boat photos show through the big leaf in its shape (`assets/leaf-mask.png`), in step with the headline; pointing at a label jumps to it. Below the hero the page is light, with sections in the rounded tile layout (`hs--v5`) and a dark green footer. Its own Homeowners and quote pages.
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

## Numbering

The main run is concepts 1 to 10 (`concept-1/` to `concept-10/`). The site's front page opens concept 1's Get a Quote page (`concept-1/crq-form/`); the review bar and the logo lead on to the concepts. Earlier concepts are the archive, labelled with letters so no two pages share a number: Archive A to E (`archive-a/` to `archive-e/`).

How the numbers have moved, in order: old 1 to 4 became Archive A to D and old 5 and 6 became 1 and 2, with the hero homepages following from 3; then V2, H2 and H3 on full homepages were dropped (they are still on their own at `hero-ideas/`); then concept 1 (Daylight) moved to Archive E and everything after it moved down one. `vercel.json` sends the old `homepages/<code>/` links and `concept-11/` to `concept-18/` to the page they show now, or to concept 1 for a dropped one. Links to `concept-1/` to `concept-10/` open whatever has that number now.

## Archive A to E

Archives A to E are still online but out of the main run. Their review bar steps through the archive only, and the heroes page lists them at the bottom. They stay because concepts 2 to 10 use the homepages (and Homeowners and quote pages) of archives A to C, and concept 2 uses archive E's hero.

## Concepts 2 to 10: every new hero on a full homepage

`concept-2/` to `concept-10/` put each new hero on one of the archived homepages, unchanged apart from the hero, and carry on the numbering from concept 1:

- 2 to 4, on the archive A homepage: archive E's pointing fig leaf hero, then V1 and V3
- 5 to 8, on the archive B homepage: photo heroes A, B, C and D
- 9 and 10, on the archive C homepage: concept 1's leaf slideshow hero, then H1

They link back to their homepage's folder for styles and images and to the hero's own files. Each has its own copy of the quote, quote form and Homeowners pages (content unchanged), so a visitor clicking the menu, the hero or the quote buttons stays inside that concept.

**Homeowners layouts.** The five Homeowners layouts take turns (`HOMEOWNERS` in `homepages/build.py`): layout 1 is archive A's page, 2 archive B's with tabs, 3 archive B's scrolling page, 4 archive B's header fade page and 5 archive C's. Concepts 1 to 5 get layouts 1 to 5, and 6 to 10 start again from layout 1. Each Homeowners page has the concept bar, 1 to 10, where each number opens that concept's Homeowners page; build.py writes concept 1's Homeowners page too. `homepages/build.py` builds them, keeps the review bar on concept 1 listing 1 to 10 and the archive's bar listing A to E; re-run it after changing a homepage or a hero. `homepages/shared/` holds archive E's and concept 1's hero styles on their own (`hero-5.css`, `hero-6.css`, named for their old numbers), the rules that give the new heroes room under the see-through header on the archive B and C homepages, and small per-hero size and position tweaks (by the `data-hero` attribute build.py puts on `<html>`).

Concept 2 alone adds a Business insurance card under "More Ways We Protect You" (three cards across), from `EXTRAS` in `homepages/build.py`. Its photo, `homepages/shared/assets/business-insurance.jpg`, is from Unsplash, [GFrBMipOd_E](https://unsplash.com/photos/two-women-near-tables-GFrBMipOd_E), under the Unsplash License.

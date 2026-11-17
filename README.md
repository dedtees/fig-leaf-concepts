# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens concept 1;
each `concept-N/` or `archive-X/` folder is one page:

- `archive-a/`, `archive-b/`: homepage concepts
- `archive-c/`: archive B with the horizontal leaves hero (from the old concept 2) and archive A's Google Reviews layout (`hs-reviews--split`)
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
- `concept-1/`: **Daylight**. A black header and hero (the client's preference) with the agency's studio fig leaf (gallery leaf 1) inside gold rings, labels for Auto, Home, Boat and Business around it, and a headline whose last word rotates through car, home, boat and business. The leaf's tip points at the cursor wherever it is, and the mouse pointer itself is a small fig leaf whose tip is the click point (`assets/leaf-cursor.png`). The car, house and boat photos show through the big leaf in its shape (`assets/leaf-mask.png`), in step with the headline; pointing at a label jumps to it. Below the hero the page is light, with sections in the rounded tile layout (`hs--v5`) and a dark green footer. Its own Homeowners and quote pages.
- `concept-2/`: **Leaf slideshow**. The hero is one big Fig Leaf (the logo's leaf, `assets/fig-leaf-fill.svg`, larger than the hero art on any other concept) used as a frame: photos of a car, a house and a boat slide through it every few seconds, with a gold edge and a dark green offset leaf behind it. The headline matches the other concepts, "We cover your car.", and its last word changes in step with the photo (car, home, boat). Arrows, dots, a pause button, swipe and the arrow keys move it by hand (`concept.js`). Header, sections (`hs--v2`), footer and the inner pages use archive C's look. Its own Homeowners and quote pages.

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

**Concepts 1 and 2.** Both start from archive C's files and keep its content and pages. Each folder's `concept.css` loads last on all its pages
(after `palette.css`) and holds it to the same four colours (gold, black, white, dark green, light green sparingly), no gradients or soft shadows.
`concept.js` drives each hero (concept 1's rotating word, concept 2's slideshow); `scene.js` isn't used there. Both use the current
logo, `assets/figleaf-logo-full.png`.

**All heroes together (`heroes/`).** One page that links every homepage hero idea, with a screenshot of each: concepts 1 and 2,
the photo heroes A to D (`hero-concepts/`) and the six fig leaf pictures V1 to H3 (`hero-ideas/`).

## Numbering

The main run is concepts 1 to 14 (`concept-1/` to `concept-14/`); the site's front page opens concept 1. The four earlier concepts are the archive, labelled with letters so no two pages share a number: Archive A to D (`archive-a/` to `archive-d/`). Old numbers map like this: old 5 and 6 are now 1 and 2, old 7 to 18 are now 3 to 14, and old 1 to 4 are Archive A to D. Old links to `concept-15/` to `concept-18/` and to `homepages/<code>/` redirect to the new numbers (`vercel.json`).

## Archive A to D

Archives A to D are still online but out of the main run. Their review bar steps through the archive only, and the heroes page lists them at the bottom. They stay because concepts 3 to 14 use the homepages (and Homeowners and quote pages) of archives A to C.

## Concepts 3 to 14: every new hero on a full homepage

`concept-3/` to `concept-14/` put each new hero on one of the archived homepages, unchanged apart from the hero, and carry on the numbering from concepts 1 and 2:

- 3 to 6, on the archive A homepage: concept 1's pointing fig leaf hero, then V1, V2 and V3
- 7 to 10, on the archive B homepage: photo heroes A, B, C and D
- 11 to 14, on the archive C homepage: concept 2's leaf slideshow hero, then H1, H2 and H3

They link back to their homepage's folder for styles and images and to the hero's own files. Each has its own copy of the quote, quote form and Homeowners pages (content unchanged), so a visitor stays inside that concept. `homepages/build.py` builds them, keeps the review bar on concepts 1 and 2 listing 1 to 14 and the archive's bar listing A to D; re-run it after changing a homepage or a hero. `homepages/shared/` holds concept 1's and 2's hero styles on their own (`hero-5.css`, `hero-6.css`, named for their old numbers), and the rules that give the new heroes room under the see-through header on the archive B and C homepages.

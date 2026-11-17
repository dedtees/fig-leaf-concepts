# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens Concept 1;
each `concept-N/` folder is one page:

- `concept-1/`, `concept-2/`: homepage concepts
- `concept-3/`: concept 2 with the horizontal leaves hero (from the old concept 6) and concept 1's Google Reviews layout (`hs-reviews--split`)
- `concept-1/homeowners-insurance/`, `concept-2/…`, `concept-3/…`: the Homeowners Insurance page in each concept
  (content from figleafagency.com/homeowners-insurance). These are interior pages: solid dark header, a light title
  band and a document layout instead of the homepage's dark hero, in the concept's colours and type.
  Styles in `insurance-page.css`, concept 2's in-place tabs and concept 3's section highlighting in `insurance-page.js`; the `pg--v1` / `pg--v2` / `pg--v3`
  class on `<main>` picks the layout. Linked from the header under Personal Insurance.
- `concept-2/homeowners-insurance-scroll/`: concept 2's Homeowners page without tabs; the same sections stacked
  (quote first) so the page scrolls. For comparing with the tabbed version.
- `concept-2/homeowners-insurance-fade/`: the tabbed concept 2 Homeowners page with a title band that continues the
  header's black and fades into the light page (`pg--fade`), instead of a hard black-to-white edge.
- `concept-1/crq/`, `concept-2/crq/`, `concept-3/crq/`: the quote request page (figleafagency.com/crq). The form is the same
  Consumer Rate Quotes iframe the live page uses (we can't style inside it), framed in each concept's look.
  Styles in `quote-page.css`; the `qp--v1` / `qp--v2` / `qp--v3` class on `<main>` picks the look. Reached from the review bar.
- `concept-1/crq-form/`, `concept-2/…`, `concept-3/…`: the quote form on its own, the same iframe exactly as it looks live,
  between each concept's header and footer (no extra copy). Styles in `quote-page.css` (`.qp-plain`).
  Every Get a Quote / Start My Quote button links here.
- `hero-concepts/`: four hero directions without the fig leaf artwork, same interaction (hover, tap or focus the car,
  home or boat). `a` opening photo panels and `c` uncover lens are horizontal; `b` stacked bands and `d` card deck are vertical.
  Built from Concept 1's homepage by `hero-concepts/build.py`; the layouts are `shared/hero-x.css`, the behaviour `shared/hero-x.js`.
- `hero-ideas/`: six replacement hero pictures with the same interactive hero, three vertical (`v1`–`v3`, on Concept 1)
  and three horizontal (`h1`–`h3`, on Concept 3). `hero-ideas/index.html` shows them side by side; each page reuses its
  concept's CSS, scripts and inner pages and only swaps `hero.jpg` and the hotspot positions. Sources in `hero-ideas/_source/`.
- `concept-4/`: the photo gallery (the old `concept-7/` link redirects here, see `vercel.json`)
- `concept-5/`: **Daylight**. A black header and hero (the client's preference) with the agency's studio fig leaf (gallery leaf 1) inside gold rings, labels for Auto, Home, Boat and Business around it, and a headline whose last word rotates through car, home, boat and business. The leaf's tip points at the cursor wherever it is, and the mouse pointer itself is a small fig leaf whose tip is the click point (`assets/leaf-cursor.png`). The car, house and boat photos show through the big leaf in its shape (`assets/leaf-mask.png`), in step with the headline; pointing at a label jumps to it. Below the hero the page is light, with sections in the rounded tile layout (`hs--v5`) and a dark green footer. Its own Homeowners and quote pages.
- `concept-6/`: **Leaf slideshow**. The hero is one big Fig Leaf (the logo's leaf, `assets/fig-leaf-fill.svg`, larger than the hero art on any other concept) used as a frame: photos of a car, a house and a boat slide through it every few seconds, with a gold edge and a dark green offset leaf behind it. The headline matches the other concepts, "We cover your car.", and its last word changes in step with the photo (car, home, boat). Arrows, dots, a pause button, swipe and the arrow keys move it by hand (`concept.js`). Header, sections (`hs--v2`), footer and the inner pages use concept 3's look. Its own Homeowners and quote pages.

Concept 1 is the dark theme. `concept-1/palette.css` loads last on all its pages (home, Homeowners, both quote
pages) and holds them to four colours, one shade each: gold #e8c27e, black #070d0f, white #fff and dark green
#17402b, plus a light green #a9c7b4 used sparingly. No gradients, see-through colours or soft shadows, except the
faint fig leaf silhouettes in the background, which use concept 2's leaf green #3f8a5a. It overrides
the shared stylesheets for concept 1 only, so those stay identical copies.

Concept 2 uses the same palette: `concept-2/palette.css` loads last on all its pages and holds them to gold, black,
white and dark green, with light green used sparingly, and no gradients, glows or soft shadows. The exceptions are the
leaf silhouettes, which keep their own greens, and the grid behind "Select One or Bundle!".

Concept 3 uses the same palette too: `concept-3/palette.css` loads last on all its pages (home, Homeowners, both quote pages). Its homepage shares concept 2's rules. The Homeowners guide page gets a white title band with a solid gold top stripe, flat cards with light green edges, accordion icons with no tile behind them, and a solid dark green quote panel. The gradient rules beside headings are now solid gold.

The homepage concepts share the sections in `home-sections.css` / `home-sections.js`
(identical copies in each folder); the `hs--v1` / `hs--v2` class on `#home-sections`
picks the section layout.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

**Grid background (`grid.css`).** The faint grid from concept 2's "Select One or Bundle" section is now a reusable layer, with an identical `grid.css` in concepts 1, 2 and 3. A section gets the class `fl-grid-host` and a first child `<div class="fl-grid" aria-hidden="true"><span class="fl-grid__lines" data-hs-px="0.15"></span></div>`. Add `fl-grid--light` for green lines on light sections. It's used on concept 1's Comprehensive Coverage, Select One or Bundle and More Ways We Protect You sections, on concept 3's Comprehensive Coverage and More Ways We Protect You sections, and on the title area of every Homeowners page. Concept 1's and concept 3's Homeowners pages also have it on the closing quote band.

**Concepts 5 and 6.** Both start from concept 3's files and keep its content and pages. Each folder's `concept.css` loads last on all its pages
(after `palette.css`) and holds it to the same four colours (gold, black, white, dark green, light green sparingly), no gradients or soft shadows.
`concept.js` drives each hero (concept 5's rotating word, concept 6's slideshow); `scene.js` isn't used there. Both use the current
logo, `assets/figleaf-logo-full.png`.

**All heroes together (`heroes/`).** One page that links every homepage hero idea, with a screenshot of each: concepts 5 and 6,
the photo heroes A to D (`hero-concepts/`) and the six fig leaf pictures V1 to H3 (`hero-ideas/`).

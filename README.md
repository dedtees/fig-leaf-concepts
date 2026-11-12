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
- `concept-4/`: the photo gallery (the old `concept-7/` link redirects here, see `vercel.json`)

Concept 1 is the dark theme. `concept-1/palette.css` loads last on all its pages (home, Homeowners, both quote
pages) and holds them to four colours, one shade each: gold #e8c27e, black #070d0f, white #fff and dark green
#17402b, plus a light green #a9c7b4 used sparingly. No gradients, see-through colours or soft shadows, except the
faint fig leaf silhouettes in the background, which use concept 2's leaf green #3f8a5a. It overrides
the shared stylesheets for concept 1 only, so those stay identical copies.

Concept 2 uses the same palette: `concept-2/palette.css` loads last on all its pages and holds them to gold, black,
white and dark green, with light green used sparingly, and no gradients, glows or soft shadows. The exceptions are the
leaf silhouettes, which keep their own greens, and the grid behind "Select One or Bundle!".

The homepage concepts share the sections in `home-sections.css` / `home-sections.js`
(identical copies in each folder); the `hs--v1` / `hs--v2` class on `#home-sections`
picks the section layout.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

**Grid background (`grid.css`).** The faint grid from concept 2's "Select One or Bundle" section is now a reusable layer, with an identical `grid.css` in concepts 1, 2 and 3. A section gets the class `fl-grid-host` and a first child `<div class="fl-grid" aria-hidden="true"><span class="fl-grid__lines" data-hs-px="0.15"></span></div>`. Add `fl-grid--light` for green lines on light sections. It's used on concept 1's Comprehensive Coverage, Select One or Bundle and More Ways We Protect You sections, on concept 3's Comprehensive Coverage and More Ways We Protect You sections, and on the title area of every Homeowners page. Concept 1's and concept 3's Homeowners pages also have it on the closing quote band.

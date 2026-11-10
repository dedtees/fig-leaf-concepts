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
- `concept-4/`: the photo gallery (the old `concept-7/` link redirects here, see `vercel.json`)

The homepage concepts share the sections in `home-sections.css` / `home-sections.js`
(identical copies in each folder); the `hs--v1` / `hs--v2` class on `#home-sections`
picks the section layout.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

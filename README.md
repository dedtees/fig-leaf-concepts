# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens Concept 1;
each `concept-N/` folder is one page:

- `concept-1/`, `concept-2/`: homepage concepts
- `concept-3/`: concept 2 with the horizontal leaves hero (from the old concept 6) and concept 1's Google Reviews layout (`hs-reviews--split`)
- `concept-1/homeowners-insurance/`, `concept-2/…`, `concept-3/…`: the Homeowners Insurance page in each concept's theme
  (content from figleafagency.com/homeowners-insurance). Styles in `insurance-page.css`, layered on `home-sections.css`;
  the `pg--v1` / `pg--v2` / `pg--v3` class on `<main>` picks the look. Linked from the header under Personal Insurance.
- `concept-4/`: the photo gallery (the old `concept-7/` link redirects here, see `vercel.json`)

The homepage concepts share the sections in `home-sections.css` / `home-sections.js`
(identical copies in each folder); the `hs--v1` / `hs--v2` class on `#home-sections`
picks the section layout.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens Concept 1;
each `concept-N/` folder is one page:

- `concept-1/`, `concept-2/`: homepage concepts
- `concept-3/`: concept 2 with concept 1's Google Reviews layout (`hs-reviews--split`)
- `concept-4/`: the photo gallery (the old `concept-7/` link redirects here, see `vercel.json`)
- `concept-5/`: the sidebar concept that used to be concept 3

The homepage concepts share the sections in `home-sections.css` / `home-sections.js`
(identical copies in each folder); the `hs--v1` / `hs--v2` / `hs--v3` class on
`#home-sections` picks the section layout (concept 5 uses `hs--v3`).

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

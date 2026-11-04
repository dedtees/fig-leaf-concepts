# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens Concept 1;
each `concept-N/` folder is one concept: 1, 2 and 3, plus the photo gallery
at `concept-4/`. The gallery used to be `concept-7/`; `vercel.json` redirects
that old link to `concept-4/`. Concepts 1 to 3 share the homepage
sections in `home-sections.css` / `home-sections.js` (identical copies in each folder); the
`hs--v1` … `hs--v3` class on `#home-sections` picks each concept's section layout.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

# Fig Leaf Agency: homepage concepts

Plain HTML, CSS and JavaScript, no build step. `index.html` opens Concept 1;
each `concept-N/` folder is one concept. Concepts 1 to 6 share the homepage
sections in `home-sections.css` / `home-sections.js` (identical copies in each folder); the
`hs--v1` … `hs--v6` class on `#home-sections` picks each concept's section layout. Concept 7 is
the photo gallery.

Vercel settings: Framework Preset "Other", no build command, output directory = repo root.

# Hero idea sources

Each hero picture is laid out as an HTML page (`v1.html` … `h3.html`, shared `base.css`) and
rendered with Chromium at 1300 × 1024 CSS px, device scale 1.5, to `hero-<id>.jpg` (1950 × 1536).
To re-render, put these next to the source images and screenshot each page:

- `car.jpg`, `home.jpg`, `boat.jpg`: the Unsplash photos credited on `hero-ideas/index.html`, downloaded at 2400 px wide
- `leafcut-01/02.png`: gallery leaves 1 and 2 cut out from their white background; `leafin-*.png` is the same
  shape shrunk ~40 px and feathered (where the photo shows), `leafhp-*.png` a high-pass of the leaf (vein texture)
- `fig-leaf-fill.svg`: `concept-1/assets/fig-leaf-fill.svg` with the fill set to white

`build.py` makes each `hero-ideas/<id>/index.html` from Concept 1 (vertical) or Concept 3 (horizontal):
it points every link and asset back at that concept, swaps in `hero.jpg`, and sets the hotspot positions.

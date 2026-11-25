# Client review ticks

The live site (one site since build 5 moved to the root) has a small ✓ / ✕ /
comment tick on every section of every page: the homepage, all fifteen
insurance pages, Carriers, the quote pages, About, Testimonials, every bio,
Contact, Privacy Policy and Terms & Conditions. The `/checklist/` page is left
out (it has its own review items). Picks go into the sheet under the concept
**Website**, one page per address. Some parts get a tick of their own inside
their section: the video testimonial, the bios' can help you and Off the clock
cards, the floating Get a Quote buttons, the office open/closed badge and the
announcements bell. Any element can opt in with `data-review="Label"`.

A **Your review** button in the bottom-right corner lists all the picks, with
**Send my feedback**, **Copy** and **Download** (a CSV for Excel or Sheets).

- Picks are saved in the reviewer's browser as they go, so they survive reloads
  and moving between concepts. They are per browser: a reviewer should use one
  browser for the whole review.
- `?review=off` on any address hides everything (for clean screenshots).
  **Hide the ticks** in the panel does the same for that browser.
- The code is `review/review.js` and `review/review.css`, loaded by one line at the
  end of each page. Nothing else on the pages changed.

## Without setup (how it works now)

**Send my feedback** opens an email with the summary already written. To fill in
the To line, put the address in `EMAIL` at the top of `review/review.js`.

## Live collection in a Google Sheet

The sheet is "Fig Leaf concept review (client picks)" in Eric's Google Drive.
`review/google-apps-script.gs` keeps four tabs up to date after every tick:

- **Overview**: a scoreboard per concept (likes, don't likes, score, comments,
  best liked sections), then a grid of every section (rows, grouped by page) by
  concept (columns). Green ✓, red ✕, amber when reviewers disagree. A corner
  mark on a cell means it has comments: hover to read them.
- **By concept**: choose a concept in the dropdown to list just its picks.
- **Comments**: every written comment, in concept and page order.
- **All picks**: the raw list, one row per reviewer and section. Changing a tick
  updates its row and taking it back removes the row, so there are no duplicates.

Installing it (once):

1. Either open the sheet and choose **Extensions → Apps Script**, or (if that
   won't open) go to **script.google.com → New project**. The script works both
   ways: on its own it opens the review sheet by its ID (`SHEET_ID`). Delete
   what's in the editor, paste in the whole of `review/google-apps-script.gs`,
   and save.
2. **Deploy → New deployment**, type **Web app**, Execute as **Me**, Who has
   access **Anyone**. Press **Deploy** and allow the permissions (Google warns the
   app is unverified because it's your own script: Advanced → Go to project).
3. Copy the **Web app URL** (ends in `/exec`) into `ENDPOINT` at the top of
   `review/review.js` and push.

**Updating the script** (after a change to `review/google-apps-script.gs`):
open the Apps Script project, paste the new file over the old one, save, then
**Deploy → Manage deployments → ✎ Edit → Version: New version → Deploy**. The
web app URL stays the same, so `review/review.js` doesn't change. The script
from 24 Nov 2026 sorts the builds and the nine insurance pages in menu order
and puts Heading font and Stock photos last; picks still arrive without it.

Optional: in the Apps Script editor, run `addSampleData` once to see the layout
with three sample picks, then delete those rows from All picks and choose
**Review → Rebuild the overview**.

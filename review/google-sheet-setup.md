# Client review ticks

Every section of every concept page (homepages 1 to 10, the Homeowners pages,
both quote pages and the archives) has a small ✓ / ✕ / comment tick in its top
corner. The header's tick sits under its bottom-left edge. A **Your review**
button in the bottom-right corner lists all the picks across every concept, with
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

## Live collection in a Google Sheet (optional, about 5 minutes)

Every tick then lands in a sheet as it's made, one row per reviewer, page and
section, so you can watch the review happen and filter by concept.

1. Create a new Google Sheet, for example "Fig Leaf concept review".
2. **Extensions → Apps Script**. Delete what's there, paste in the whole of
   `review/google-apps-script.gs`, and save.
3. **Deploy → New deployment**. Type: **Web app**. Execute as: **Me**.
   Who has access: **Anyone**. Press **Deploy** and allow the permissions
   (Google warns that the app is unverified, because it's your own script:
   Advanced → Go to project).
4. Copy the **Web app URL** (it ends in `/exec`).
5. Paste it into `ENDPOINT` at the top of `review/review.js` (or send it to
   Claude to do it), and push.

The sheet gets a **Picks** tab with Reviewer, Concept, Page, Section, Verdict,
Comment and Link columns. Taking a tick back clears that row's verdict.

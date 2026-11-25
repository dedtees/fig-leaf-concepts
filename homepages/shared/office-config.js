/* ==========================================================================
   Office status and announcements: the ONE file the agency edits.
   (On the WordPress site these become a settings page with the same fields.)

   The site shows one of three states, worked out from the settings below:
     open     office open, phones answered        green   "Open now · until 5 PM"
     phones   office closed, phones answered      amber   "Office closed · Phones open: (908) 862-3447"
              (a snow day)
     closed   office closed, phones off           grey    "Closed for Thanksgiving · reopens Fri 9 AM"
              (holidays; ordinary evenings and weekends too, see afterHoursPhones)

   Builds 1 and 2 show it as a badge in the top bar, left of the address.
   Builds 3 and 4 show it as a banner above the header on a snow day or a
   holiday, and otherwise the news message in `banner` (if it's on).

   Preview without editing (add to any build 1 to 4 page's address):
     ?office=open     ?office=snow     ?office=holiday     ?office=night
     ?banner=show     bring back a banner you have closed
   ========================================================================== */
window.FIG_LEAF_OFFICE = {

  phone: '(908) 862-3447',
  phoneLink: 'tel:+19088623447',

  /* Office hours, in the office's own time zone, so a visitor in another
     state still sees Hazlet time. 24-hour clock. null = closed all day.
     Source: the agency's Google Business Profile (Mon to Fri, 9 AM to 5 PM).
     To confirm with the agency. */
  timeZone: 'America/New_York',
  hours: {
    mon: ['09:00', '17:00'],
    tue: ['09:00', '17:00'],
    wed: ['09:00', '17:00'],
    thu: ['09:00', '17:00'],
    fri: ['09:00', '17:00'],
    sat: null,
    sun: null
  },

  /* Are the phones answered outside office hours (evenings, weekends)?
     Assumed no until the agency says otherwise: after hours shows as
     "closed" (grey), not "phones open" (amber). */
  afterHoursPhones: false,

  /* Days the office is closed that the weekly hours don't know about.
     phones: true if calls are still answered that day (amber instead of grey).
     To confirm with the agency. */
  closedDates: [
    { date: '2026-11-26', label: 'Thanksgiving', phones: false },
    { date: '2026-12-25', label: 'Christmas', phones: false },
    { date: '2027-01-01', label: 'New Year’s Day', phones: false },
    { date: '2027-05-31', label: 'Memorial Day', phones: false },
    { date: '2027-07-05', label: 'Independence Day', phones: false },
    { date: '2027-09-06', label: 'Labor Day', phones: false },
    { date: '2027-11-25', label: 'Thanksgiving', phones: false },
    { date: '2027-12-24', label: 'Christmas', phones: false }
  ],

  /* Manual override: a snow day, a power cut, an early close.
     office: 'auto' (use the hours), 'closed' or 'open'.
     phones: 'on' or 'off' while the office is closed by this override.
             A snow day is office 'closed' + phones 'on'.
     note:   why, in a few words ('snow', 'a power outage').
     until:  'YYYY-MM-DD', the last day it applies; after that it switches
             itself off, so nobody has to remember to undo it.
             '' = today only. */
  override: {
    office: 'auto',
    phones: 'on',
    note: 'snow',
    until: ''
  },

  /* News banner (builds 3 and 4), shown when there is no closure to report.
     show: false hides it. Give each new message a new id: a visitor who
     closed the last one will still see the new one.
     icon: 'info' or 'star'.
     link: a page of this site, from the site's root ('carriers/'), or a full URL. */
  banner: {
    show: false,
    id: 'safeco-2026',
    icon: 'star',
    title: 'Now offering Safeco.',
    text: 'One more carrier we can shop for you.',
    linkText: 'See all our carriers',
    link: 'carriers/'
  },

  /* For the client review only: builds 3 and 4 show this state's banner on an
     ordinary day so it can be seen ('snow', 'holiday' or ''). Set to '' on the
     live site. A real closure or holiday always wins over it. */
  bannerSample: 'snow'
};

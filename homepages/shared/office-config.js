/* ==========================================================================
   Office status and announcements: the ONE file the agency edits.
   (On the WordPress site these become a settings page with the same fields.)

   The site shows one of three states, worked out from the settings below:
     open     office open, phones answered        green   "Open now · until 5 PM"
     phones   office closed, phones answered      amber   "Office closed · Phones open: (908) 862-3447"
              (a snow day)
     closed   office closed, phones off           grey    "Closed for Thanksgiving · reopens Fri 9 AM"
              (holidays; ordinary evenings and weekends too, see afterHoursPhones)

   Builds 1 to 4 show it as a badge in the top bar, left of the address, with
   a bell beside it for announcements (see `announcements` at the bottom).

   Preview without editing (add to any build 1 to 4 page's address):
     ?office=open     ?office=snow     ?office=holiday     ?office=night
     ?news=reset      show the bell's red dot again, as a first-time visitor sees it
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

  /* Announcements: the bell beside the badge. A red dot shows until the
     visitor opens it; it comes back when there is something they haven't
     seen. The bell lists, in this order:
       - a closure today (from the override or a holiday), automatically
       - holidays coming up within holidayNoticeDays, automatically
       - these items, newest first, each from its `from` date to its `until`
         date (inclusive; leave either out for no limit)
     Give each item its own id: a new id is what brings the red dot back.
     icon: 'star', 'info', 'calendar' or 'phone'.
     link: a page of this site, from the site's root ('carriers/'), or a full URL. */
  holidayNoticeDays: 7,
  announcements: [
    {
      id: 'safeco-2026-11',
      from: '2026-11-24',
      until: '2027-01-31',
      icon: 'star',
      title: 'Now offering Safeco.',             // sample for the review: swap in the real new carrier
      text: 'One more carrier we can shop for you.',
      linkText: 'See all our carriers',
      link: 'carriers/'
    }
  ]
};

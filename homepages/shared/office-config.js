/* ==========================================================================
   Office status and announcements: the ONE file the agency edits.
   (On the WordPress site these become a settings page with the same fields.)

   Builds 1 and 2 show the open / closed badge in the top bar, worked out
   from `hours` below. Builds 3 and 4 show the announcement banner above
   the header. Both read this file; office-status.js does the rest.

   Preview without editing (add to any build page's address):
     ?office=snow     badge as it looks with the snow-day override on
     ?office=open     / ?office=closed   force the badge either way
     ?banner=show     bring back a banner you have closed
   ========================================================================== */
window.FIG_LEAF_OFFICE = {

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

  /* Days the office is closed that the weekly hours don't know about.
     The badge says "Closed today · <label>" on these. To confirm with the agency. */
  closedDates: [
    { date: '2026-11-26', label: 'Thanksgiving' },
    { date: '2026-12-25', label: 'Christmas' },
    { date: '2027-01-01', label: 'New Year’s Day' },
    { date: '2027-05-31', label: 'Memorial Day' },
    { date: '2027-07-05', label: 'Independence Day' },
    { date: '2027-09-06', label: 'Labor Day' },
    { date: '2027-11-25', label: 'Thanksgiving' },
    { date: '2027-12-24', label: 'Christmas' }
  ],

  /* Manual override for the badge: a snow day, a power cut, an early close.
     status: 'auto' (use the hours), 'closed' or 'open'.
     note:   a few words shown after "Closed today ·", e.g. 'Snow day'.
     until:  'YYYY-MM-DD'; the override switches itself off after this day,
             so nobody has to remember to undo it. Leave '' for no end. */
  override: {
    status: 'auto',
    note: 'Snow day',
    until: ''
  },

  /* What the badge's drop-down adds under the hours, on every day. */
  stillReachable: 'Closed? We still answer calls and email: (908) 862-3447.',

  /* Announcement banner (builds 3 and 4). show: false hides it.
     Give each new message a new id: a visitor who closed the last one
     will still see the new one.
     icon: 'snow', 'info' or 'star'.
     link: a page of this site, from the site's root ('carriers/'), or a full URL. */
  banner: {
    show: true,
    id: 'snow-day-sample',
    icon: 'snow',
    title: 'Office closed today for snow.',
    text: 'We’re still answering calls and email. Stay safe out there.',
    linkText: 'Need to file a claim?',
    link: 'carriers/'
  }

  /* Another example, for a new carrier:
  banner: {
    show: true, id: 'safeco-2026', icon: 'star',
    title: 'Now offering Safeco.',
    text: 'One more carrier we can shop for you.',
    linkText: 'See all our carriers', link: 'carriers/'
  }
  */
};

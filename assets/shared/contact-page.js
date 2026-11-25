/* Contact page (contact/index.html): fills in the office hours card from
   assets/shared/office-config.js, so the hours only ever need changing there,
   and shows whether the office is open right now (the same wording as the
   badge in the top bar). Without JavaScript the page keeps the hours written
   into its HTML. */
(function () {
  'use strict';
  var cfg = window.FIG_LEAF_OFFICE;
  var api = window.FIG_LEAF_OFFICE_STATUS;
  var list = document.querySelector('[data-ct-hours]');
  if (!cfg || !list) return;

  var KEYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
  var NAMES = { mon: 'Monday', tue: 'Tuesday', wed: 'Wednesday', thu: 'Thursday', fri: 'Friday', sat: 'Saturday', sun: 'Sunday' };
  function fmt(hhmm) {
    if (api && api.fmt) return api.fmt(hhmm);
    var p = hhmm.split(':'), h = +p[0], m = +p[1] || 0, ap = h >= 12 ? 'PM' : 'AM';
    return (h % 12 || 12) + (m ? ':' + (m < 10 ? '0' : '') + m : '') + ' ' + ap;
  }

  // runs of days with the same hours: "Monday to Friday  9 AM to 5 PM"
  var rows = [];
  KEYS.forEach(function (key) {
    var h = (cfg.hours || {})[key];
    var text = h ? fmt(h[0]) + ' to ' + fmt(h[1]) : 'Closed';
    var last = rows[rows.length - 1];
    if (last && last.text === text) last.to = key;
    else rows.push({ from: key, to: key, text: text });
  });

  // today's row, in the office's time zone
  var today = new Intl.DateTimeFormat('en-US', { timeZone: cfg.timeZone || 'America/New_York', weekday: 'short' })
    .format(new Date()).slice(0, 3).toLowerCase();
  var idx = KEYS.indexOf(today);

  list.innerHTML = '';
  rows.forEach(function (r) {
    var from = KEYS.indexOf(r.from), to = KEYS.indexOf(r.to);
    var days = from === to ? NAMES[r.from]
      : to - from === 1 ? NAMES[r.from] + ' and ' + NAMES[r.to]
      : NAMES[r.from] + ' to ' + NAMES[r.to];
    var row = document.createElement('div');
    if (idx >= from && idx <= to) row.className = 'is-today';
    var dt = document.createElement('dt'); dt.textContent = days;
    var dd = document.createElement('dd'); dd.textContent = r.text;
    row.appendChild(dt); row.appendChild(dd);
    list.appendChild(row);
  });

  // "Open now until 5 PM" / "Closed for Thanksgiving ..." above the hours
  var now = document.querySelector('[data-ct-now]');
  if (now && api) {
    var s = api.status();
    now.innerHTML = '<span class="ct-now__dot" aria-hidden="true"></span><span>' + api.sentence(s) + '</span>';
    now.setAttribute('data-state', s.state);
    now.hidden = false;
  }
})();

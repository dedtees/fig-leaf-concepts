/* ==========================================================================
   Office status and announcements (builds 1 to 4).
   The settings are in office-config.js; this file only draws them.

   Three states:  open    office open, phones answered     (green)
                  phones  office closed, phones answered   (amber, a snow day)
                  closed  office closed, phones off        (grey, holidays and after hours)

   On builds 1 to 4 (<html data-office="badge">), in the top bar left of the
   address (a slim strip across the top of the header on phones):
     the badge   the state, with the week's hours in a drop-down
     the bell    announcements in a drop-down, with a red dot while there is
                 one this visitor hasn't seen (remembered in their browser):
                 a closure today, a holiday coming up, and the news items
                 in office-config.js
   ========================================================================== */
(function () {
  'use strict';
  var cfg = window.FIG_LEAF_OFFICE;
  var mode = document.documentElement.getAttribute('data-office');
  if (!cfg || !mode) return;

  var params = new URLSearchParams(location.search);
  var preview = params.get('office');   // open | snow | holiday | night (also phones, closed)
  if (preview === 'phones') preview = 'snow';
  if (preview === 'closed') preview = 'holiday';
  var DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
  var DAY_NAMES = { sun: 'Sun', mon: 'Mon', tue: 'Tue', wed: 'Wed', thu: 'Thu', fri: 'Fri', sat: 'Sat' };
  var PHONE = cfg.phone || '(908) 862-3447';
  var TEL = cfg.phoneLink || 'tel:+19088623447';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function telLink() { return '<a href="' + esc(TEL) + '">' + esc(PHONE) + '</a>'; }

  /* The site's root (the build folder), from the logo's home link. */
  function siteUrl(link) {
    var home = document.querySelector('.site-header__brand');
    try { return new URL(link, home ? home.href : location.href).href; } catch (e) { return link; }
  }

  /* ---- time in the office's time zone ----------------------------------- */
  function officeNow() {
    var parts = {};
    new Intl.DateTimeFormat('en-US', {
      timeZone: cfg.timeZone || 'America/New_York',
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
    return { y: +parts.year, m: +parts.month, d: +parts.day, mins: (+parts.hour % 24) * 60 + (+parts.minute) };
  }
  /* The office's calendar day k days from today: its key ('mon') and ISO date. */
  function dayAt(now, k) {
    var t = new Date(Date.UTC(now.y, now.m - 1, now.d + k));
    return { key: DAYS[t.getUTCDay()], iso: t.toISOString().slice(0, 10) };
  }
  function toMins(hhmm) { var p = hhmm.split(':'); return +p[0] * 60 + (+p[1] || 0); }
  function fmt(hhmm) {
    var m = toMins(hhmm), h = Math.floor(m / 60), mm = m % 60;
    var ap = h >= 12 ? 'PM' : 'AM';
    h = h % 12 || 12;
    return h + (mm ? ':' + (mm < 10 ? '0' : '') + mm : '') + ' ' + ap;
  }
  function holiday(iso) {
    var list = cfg.closedDates || [];
    for (var i = 0; i < list.length; i++) if (list[i].date === iso) return list[i];
    return null;
  }

  /* ---- the state ---------------------------------------------------------- */
  function status() {
    var now = officeNow();
    var today = dayAt(now, 0);
    var ov = cfg.override || {};
    var ovOffice = ov.office || 'auto';
    var ovLast = ov.until || today.iso;                      // '' = today only
    if (ovOffice !== 'auto' && today.iso > ovLast) ovOffice = 'auto';
    var fakeHoliday = null;
    if (preview === 'snow') { ovOffice = 'closed'; ov = { phones: 'on', note: 'snow' }; ovLast = today.iso; }
    if (preview === 'open') ovOffice = 'open';
    if (preview === 'holiday') { ovOffice = 'auto'; fakeHoliday = { label: 'Thanksgiving', phones: false }; }
    var night = preview === 'night';

    function closedBy(day, k) {           // is the office shut all day on this day?
      if (k === 0 && fakeHoliday) return true;
      if (ovOffice === 'closed' && day.iso <= ovLast) return true;
      if (holiday(day.iso)) return true;
      return !(cfg.hours || {})[day.key];
    }
    /* the next opening: "9 AM" (later today), "tomorrow 9 AM", "Mon 9 AM" */
    function reopen(fromToday) {
      var h = (cfg.hours || {})[today.key];
      if (fromToday && h && !closedBy(today, 0) && now.mins < toMins(h[0])) return fmt(h[0]);
      for (var k = 1; k <= 21; k++) {
        var d = dayAt(now, k);
        if (!closedBy(d, k)) return (k === 1 ? 'tomorrow' : DAY_NAMES[d.key]) + ' ' + fmt(cfg.hours[d.key][0]);
      }
      return '';
    }

    var hours = (cfg.hours || {})[today.key];
    if (ovOffice === 'open') {
      return { state: 'open', until: hours ? fmt(hours[1]) : '' };
    }
    if (ovOffice === 'closed') {
      return { state: ov.phones === 'off' ? 'closed' : 'phones', why: 'override', note: ov.note || '', reopen: reopen(false) };
    }
    var hol = fakeHoliday || holiday(today.iso);
    if (hol) {
      return { state: hol.phones ? 'phones' : 'closed', why: 'holiday', note: hol.label, reopen: reopen(false) };
    }
    if (!night && hours && now.mins >= toMins(hours[0]) && now.mins < toMins(hours[1])) {
      return { state: 'open', until: fmt(hours[1]) };
    }
    return { state: cfg.afterHoursPhones ? 'phones' : 'closed', why: 'after', reopen: night ? reopen(false) : reopen(true) };
  }

  /* One sentence for the drop-downs. */
  function sentence(s) {
    if (s.state === 'open') return 'Open now' + (s.until ? ' until ' + s.until : '') + '. Call ' + telLink() + '.';
    var why = s.why === 'holiday' ? 'Closed for ' + esc(s.note)
      : s.why === 'override' ? 'Office closed today' + (s.note ? ' due to ' + esc(s.note) : '')
      : 'Office closed now';
    if (s.state === 'phones') return why + '. Our phones are open: call ' + telLink() + '.';
    var when = !s.reopen ? '' : s.reopen.indexOf(' ') > 0 ? s.reopen.replace(' ', ' at ') : 'at ' + s.reopen;
    return why + '. Phones are off' + (when ? '; we ' + (s.why === 'after' ? 'open ' : 'reopen ') + when : '') + '.';
  }

  /* for the Contact page's office hours card (contact-page.js) */
  window.FIG_LEAF_OFFICE_STATUS = { status: status, sentence: sentence, fmt: fmt };

  /* The week as rows: "Mon – Fri  9 AM – 5 PM", "Sat – Sun  Closed". */
  function weekRows() {
    var rows = [];
    ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'].forEach(function (key) {
      var h = (cfg.hours || {})[key];
      var text = h ? fmt(h[0]) + ' – ' + fmt(h[1]) : 'Closed';
      var last = rows[rows.length - 1];
      if (last && last.text === text) last.to = key;
      else rows.push({ from: key, to: key, text: text });
    });
    return rows.map(function (r) {
      var days = r.from === r.to ? DAY_NAMES[r.from] : DAY_NAMES[r.from] + ' – ' + DAY_NAMES[r.to];
      return '<li><span>' + days + '</span><span>' + r.text + '</span></li>';
    }).join('');
  }

  var ICON = {
    phone: '<svg class="office-badge__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 16.4v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.6 5.2 2 2 0 0 1 4.6 3h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.6 10.8a16 16 0 0 0 4.6 4.6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
  };

  /* ---- dates ---------------------------------------------------------------- */
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function isoDate(iso) { var p = iso.split('-'); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
  function shortDate(iso) { var d = isoDate(iso); return MONTHS[d.getUTCMonth()] + ' ' + d.getUTCDate(); }
  function longDate(iso) { var d = isoDate(iso); return DAY_NAMES[DAYS[d.getUTCDay()]] + ', ' + shortDate(iso); }
  /* the first day after iso with office hours: "Fri 9 AM" */
  function openAfter(iso) {
    var d = isoDate(iso);
    for (var k = 1; k <= 21; k++) {
      var t = new Date(d.getTime() + k * 864e5), day = { key: DAYS[t.getUTCDay()], iso: t.toISOString().slice(0, 10) };
      var h = (cfg.hours || {})[day.key];
      if (h && !holiday(day.iso)) return DAY_NAMES[day.key] + ' at ' + fmt(h[0]);
    }
    return '';
  }

  /* ---- the announcements ----------------------------------------------- */
  var ICONS = {
    snow: '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11"/><path d="m9 3.5 3 2.5 3-2.5M9 20.5l3-2.5 3 2.5M3.6 10l3.7 1.3-.8 3.8M20.4 14l-3.7-1.3.8-3.8M3.6 14l3.7-1.3-.8-3.8M20.4 10l-3.7 1.3.8 3.8"/>',
    phone: '<path d="M21 16.4v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.6 5.2 2 2 0 0 1 4.6 3h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.6 10.8a16 16 0 0 0 4.6 4.6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    closed: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    calendar: '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    star: '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>',
    bell: '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>'
  };

  function announcements() {
    var now = officeNow(), today = dayAt(now, 0).iso, out = [];
    var s = status();
    // 1. a closure today (snow day, holiday): the same words as the badge
    if (s.state !== 'open' && s.why !== 'after') {
      var parts = sentence(s).split(/\.\s/);
      out.push({
        id: 'status-' + s.state + '-' + (s.note || '') + '-' + today, tone: s.state,
        icon: s.state === 'phones' ? (/snow/i.test(s.note || '') ? 'snow' : 'phone') : 'closed',
        when: 'Today', title: parts[0] + '.', html: parts.slice(1).join('. '),
        linkText: s.state === 'phones' ? 'Need to file a claim?' : 'Claims: call your carrier', link: 'carriers/'
      });
    }
    // 2. holidays in the next few days
    var ahead = cfg.holidayNoticeDays == null ? 7 : cfg.holidayNoticeDays;
    (cfg.closedDates || []).forEach(function (h) {
      if (preview === 'holiday' || h.date <= today || (isoDate(h.date) - isoDate(today)) / 864e5 > ahead) return;
      out.push({
        id: 'holiday-' + h.date, tone: 'closed', icon: 'calendar', when: 'Coming up',
        title: 'Closed ' + longDate(h.date) + ' for ' + h.label + '.',
        html: h.phones ? 'Our phones stay open: call ' + telLink() + '.'
          : 'Phones are off that day; we reopen ' + openAfter(h.date) + '.'
      });
    });
    // 3. the agency's own news, newest first
    (cfg.announcements || []).filter(function (a) {
      return (!a.from || a.from <= today) && (!a.until || today <= a.until);
    }).sort(function (a, b) { return (b.from || '') < (a.from || '') ? -1 : 1; }).forEach(function (a) {
      out.push({
        id: a.id, tone: 'news', icon: a.icon || 'info', when: a.from ? shortDate(a.from) : '',
        title: a.title || '', html: esc(a.text || ''), linkText: a.linkText, link: a.link
      });
    });
    return out;
  }

  var SEEN = 'fl-office-news-seen';
  function seen() {
    try { return JSON.parse(localStorage.getItem(SEEN) || '[]'); } catch (e) { return []; }
  }
  function markSeen(ids) {
    try { localStorage.setItem(SEEN, JSON.stringify(ids.concat(seen()).slice(0, 50))); } catch (e) {}
  }
  if (params.get('news') === 'reset') { try { localStorage.removeItem(SEEN); } catch (e) {} }

  /* ---- the badge and the bell -------------------------------------------- */
  function dropdown(wrap, onOpen) {
    var btn = wrap.querySelector('button'), panel = wrap.querySelector('.office-badge__panel, .office-bell__panel');
    function shut() { btn.setAttribute('aria-expanded', 'false'); panel.hidden = true; }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = btn.getAttribute('aria-expanded') !== 'true';
      // only one drop-down open at a time
      document.querySelectorAll('.office-badge__toggle[aria-expanded="true"], .office-bell__toggle[aria-expanded="true"]').forEach(function (b) {
        if (b !== btn) b.click();
      });
      btn.setAttribute('aria-expanded', String(open));
      panel.hidden = !open;
      if (open && onOpen) onOpen();
    });
    document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) shut(); });
    wrap.addEventListener('keydown', function (e) { if (e.key === 'Escape') { shut(); btn.focus(); } });
  }

  function status_ui() {
    var bar = document.querySelector('.utility__inner');
    var header = document.querySelector('.site-header');
    if (!bar && !header) return;
    var uid = 0;

    function makeBadge(variant) {
      var id = 'office-panel-' + (++uid);
      var wrap = document.createElement('div');
      wrap.className = 'office-badge office-badge--' + variant;
      wrap.setAttribute('data-review', 'Office open / closed badge');
      wrap.innerHTML =
        '<button type="button" class="office-badge__toggle" aria-expanded="false" aria-controls="' + id + '">' +
          '<span class="office-badge__mark" aria-hidden="true"></span>' +
          '<span class="office-badge__text"></span>' +
        '</button>' +
        '<div class="office-badge__panel" id="' + id + '" hidden>' +
          '<p class="office-badge__now"></p>' +
          '<p class="office-badge__head">Office hours</p>' +
          '<ul class="office-badge__week">' + weekRows() + '</ul>' +
          '<p class="office-badge__reach">Phones are answered during office hours, and on snow days when the office is closed.</p>' +
        '</div>';
      dropdown(wrap);
      return wrap;
    }

    function makeBell(variant) {
      var id = 'office-news-' + (++uid);
      var wrap = document.createElement('div');
      wrap.className = 'office-bell office-bell--' + variant;
      wrap.setAttribute('data-review', 'Announcements bell');
      wrap.innerHTML =
        '<button type="button" class="office-bell__toggle" aria-expanded="false" aria-controls="' + id + '">' +
          '<svg class="office-bell__icon" viewBox="0 0 24 24" aria-hidden="true">' + ICONS.bell + '</svg>' +
          '<span class="office-bell__label">News</span>' +
          '<span class="office-bell__dot" aria-hidden="true" hidden></span>' +
        '</button>' +
        '<div class="office-bell__panel" id="' + id + '" hidden>' +
          '<p class="office-bell__head">Announcements</p>' +
          '<ul class="office-bell__list"></ul>' +
        '</div>';
      dropdown(wrap, function () {
        markSeen(current.map(function (a) { return a.id; }));
        paintDots();
      });
      return wrap;
    }

    var badges = [], bells = [];
    if (bar) {
      var address = bar.querySelector('.utility__item');
      var b1 = makeBadge('bar'), n1 = makeBell('bar');
      bar.insertBefore(b1, address || bar.firstChild);        // left of the address
      bar.insertBefore(n1, address || null);
      badges.push(b1); bells.push(n1);
    }
    if (header) {                                              // phones and tablets: a slim strip atop the header
      var strip = document.createElement('div');
      strip.className = 'office-strip';
      var b2 = makeBadge('strip'), n2 = makeBell('strip');
      strip.appendChild(b2); strip.appendChild(n2);
      header.insertBefore(strip, header.firstChild);
      badges.push(b2); bells.push(n2);
    }

    function words(s) {
      if (s.state === 'open') return ['Open now', s.until ? 'until ' + s.until : ''];
      if (s.state === 'phones') return ['Office closed', 'Phones open', ': ' + PHONE];
      var lead = s.why === 'holiday' ? 'Closed for ' + s.note : s.why === 'override' ? 'Office closed' : 'Closed';
      return [lead, s.reopen ? (s.why === 'after' ? 'opens ' : 'reopens ') + s.reopen : ''];
    }

    var current = [];
    function paintDots() {
      var was = seen();
      var fresh = current.filter(function (a) { return was.indexOf(a.id) < 0; });
      bells.forEach(function (el) {
        el.querySelector('.office-bell__dot').hidden = !fresh.length;
        el.classList.toggle('has-news', !!fresh.length);
        el.querySelector('button').setAttribute('aria-label', 'Announcements' +
          (fresh.length ? ', ' + fresh.length + ' new' : current.length ? '' : ', none right now'));
      });
      return fresh;
    }

    function render() {
      var s = status();
      var w = words(s);
      badges.forEach(function (el) {
        el.classList.remove('is-open', 'is-phones', 'is-closed');
        el.classList.add('is-' + s.state);
        el.querySelector('.office-badge__mark').innerHTML = s.state === 'phones' ? ICON.phone : '<span class="office-badge__dot"></span>';
        el.querySelector('.office-badge__text').innerHTML =
          '<strong>' + esc(w[0]) + '</strong>' + (w[1] ? '<span> · ' + esc(w[1]) +
          (w[2] ? '<span class="office-badge__tel">' + esc(w[2]) + '</span>' : '') + '</span>' : '');
        el.querySelector('button').setAttribute('aria-label', w[0] + (w[1] ? ', ' + w[1] + (w[2] || '') : '') + '. Show office hours');
        el.querySelector('.office-badge__now').innerHTML = sentence(s);
      });

      current = announcements();
      var fresh = paintDots().map(function (a) { return a.id; });
      var html = current.length ? current.map(function (a) {
        return '<li class="office-news office-news--' + a.tone + '">' +
          '<svg class="office-news__icon" viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[a.icon] || ICONS.info) + '</svg>' +
          '<div class="office-news__body">' +
            '<p class="office-news__meta">' + esc(a.when || '') + (fresh.indexOf(a.id) > -1 ? ' <span class="office-news__new">New</span>' : '') + '</p>' +
            '<p class="office-news__title">' + esc(a.title) + '</p>' +
            (a.html ? '<p class="office-news__text">' + a.html + '</p>' : '') +
            (a.link && a.linkText ? '<a class="office-news__link" href="' + esc(siteUrl(a.link)) + '">' + esc(a.linkText) + '</a>' : '') +
          '</div></li>';
      }).join('') : '<li class="office-news office-news--empty">No announcements right now.</li>';
      bells.forEach(function (el) {
        // don't redraw an open list under the visitor's eyes (the "New" tags stay until it closes)
        if (el.querySelector('button').getAttribute('aria-expanded') !== 'true') el.querySelector('.office-bell__list').innerHTML = html;
      });
    }
    render();
    setInterval(render, 60 * 1000);
  }

  status_ui();
})();

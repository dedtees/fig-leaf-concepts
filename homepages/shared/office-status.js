/* ==========================================================================
   Office status and announcements (builds 1 to 4).
   The settings are in office-config.js; this file only draws them.

   Three states:  open    office open, phones answered     (green)
                  phones  office closed, phones answered   (amber, a snow day)
                  closed  office closed, phones off        (grey, holidays and after hours)

   <html data-office="badge">   builds 1 and 2: the state in the top bar, left
                                of the address (a slim strip across the top of
                                the header on phones), with the week's hours
                                in a drop-down.
   <html data-office="banner">  builds 3 and 4: a dismissible banner above the
                                header for a closure or holiday, or else the
                                news message; closing it is remembered.
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

  /* One sentence for the drop-down and the banner. */
  function sentence(s) {
    if (s.state === 'open') return 'Open now' + (s.until ? ' until ' + s.until : '') + '. Call ' + telLink() + '.';
    var why = s.why === 'holiday' ? 'Closed for ' + esc(s.note)
      : s.why === 'override' ? 'Office closed today' + (s.note ? ' due to ' + esc(s.note) : '')
      : 'Office closed now';
    if (s.state === 'phones') return why + '. Our phones are open: call ' + telLink() + '.';
    var when = !s.reopen ? '' : s.reopen.indexOf(' ') > 0 ? s.reopen.replace(' ', ' at ') : 'at ' + s.reopen;
    return why + '. Phones are off' + (when ? '; we ' + (s.why === 'after' ? 'open ' : 'reopen ') + when : '') + '.';
  }

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

  /* ---- builds 1 and 2: the badge ---------------------------------------- */
  function badge() {
    var bar = document.querySelector('.utility__inner');
    if (!bar && !document.querySelector('.site-header')) return;
    var uid = 0;

    function make(variant) {
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
      var btn = wrap.querySelector('button'), panel = wrap.querySelector('.office-badge__panel');
      function shut() { btn.setAttribute('aria-expanded', 'false'); panel.hidden = true; }
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open));
        panel.hidden = !open;
      });
      document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) shut(); });
      wrap.addEventListener('keydown', function (e) { if (e.key === 'Escape') { shut(); btn.focus(); } });
      return wrap;
    }

    var items = [];
    if (bar) {
      var full = make('bar');
      var address = bar.querySelector('.utility__item');
      bar.insertBefore(full, address || bar.firstChild);        // left of the address
      items.push(full);
    }
    var header = document.querySelector('.site-header');
    if (header) {                                              // phones and tablets: a slim strip atop the header
      var strip = make('strip');
      header.insertBefore(strip, header.firstChild);
      items.push(strip);
    }

    function words(s) {
      if (s.state === 'open') return ['Open now', s.until ? 'until ' + s.until : ''];
      if (s.state === 'phones') return ['Office closed', 'Phones open', ': ' + PHONE];
      var lead = s.why === 'holiday' ? 'Closed for ' + s.note : s.why === 'override' ? 'Office closed' : 'Closed';
      return [lead, s.reopen ? (s.why === 'after' ? 'opens ' : 'reopens ') + s.reopen : ''];
    }

    function render() {
      var s = status();
      var w = words(s);
      items.forEach(function (el) {
        el.classList.remove('is-open', 'is-phones', 'is-closed');
        el.classList.add('is-' + s.state);
        el.querySelector('.office-badge__mark').innerHTML = s.state === 'phones' ? ICON.phone : '<span class="office-badge__dot"></span>';
        el.querySelector('.office-badge__text').innerHTML =
          '<strong>' + esc(w[0]) + '</strong>' + (w[1] ? '<span> \u00b7 ' + esc(w[1]) +
          (w[2] ? '<span class="office-badge__tel">' + esc(w[2]) + '</span>' : '') + '</span>' : '');
        el.querySelector('button').setAttribute('aria-label', w[0] + (w[1] ? ', ' + w[1] + (w[2] || '') : '') + '. Show office hours');
        el.querySelector('.office-badge__now').innerHTML = sentence(s);
      });
    }
    render();
    setInterval(render, 60 * 1000);
  }

  /* ---- builds 3 and 4: the banner ---------------------------------------- */
  var ICONS = {
    snow: '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11"/><path d="m9 3.5 3 2.5 3-2.5M9 20.5l3-2.5 3 2.5M3.6 10l3.7 1.3-.8 3.8M20.4 14l-3.7-1.3.8-3.8M3.6 14l3.7-1.3-.8-3.8M20.4 10l-3.7 1.3.8 3.8"/>',
    phone: '<path d="M21 16.4v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.6 5.2 2 2 0 0 1 4.6 3h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.6 10.8a16 16 0 0 0 4.6 4.6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    closed: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    star: '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>'
  };
  var KEY = 'fl-office-banner-closed';
  function store(get, val) {
    try {
      if (get) return localStorage.getItem(KEY);
      localStorage.setItem(KEY, val);
    } catch (e) { return null; }
  }

  /* What the banner says now: a closure, else the news message, else nothing. */
  function bannerContent() {
    var s = status();
    var today = dayAt(officeNow(), 0).iso;
    var closure = s.state !== 'open' && s.why !== 'after';
    var sample = !closure && !preview && cfg.bannerSample;
    if (sample === 'snow') s = { state: 'phones', why: 'override', note: 'snow' };
    if (sample === 'holiday') s = { state: 'closed', why: 'holiday', note: 'Thanksgiving', reopen: 'Fri 9 AM' };
    if (closure || sample) {
      var snow = /snow/i.test(s.note || '');
      return {
        id: (sample ? 'sample-' : 'status-') + s.state + '-' + (sample || today),
        tone: s.state,
        icon: s.state === 'phones' ? (snow ? 'snow' : 'phone') : 'closed',
        html: '<strong>' + sentence(s).replace(/\. /, '.</strong> '),
        linkText: s.state === 'phones' ? 'Need to file a claim?' : 'Claims: call your carrier',
        link: 'carriers/'
      };
    }
    var b = cfg.banner;
    if (b && (b.show || params.get('banner') === 'news')) {
      return {
        id: b.id, tone: 'news', icon: b.icon || 'info',
        html: (b.title ? '<strong>' + esc(b.title) + '</strong> ' : '') + esc(b.text || ''),
        linkText: b.linkText, link: b.link
      };
    }
    return null;
  }

  function banner() {
    var c = bannerContent();
    if (!c) return;
    if (params.get('banner') === 'show') store(false, '');
    if (c.id && store(true) === c.id) return;
    var header = document.querySelector('.site-header');
    if (!header) return;

    var el = document.createElement('div');
    el.className = 'office-banner office-banner--' + c.tone;
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', 'Announcement');
    el.setAttribute('data-review', 'Announcement banner');
    el.innerHTML =
      '<div class="office-banner__inner">' +
        '<svg class="office-banner__icon office-banner__icon--' + c.icon + '" viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[c.icon] || ICONS.info) + '</svg>' +
        '<p class="office-banner__text">' + c.html +
          (c.link && c.linkText ? ' <a class="office-banner__link" href="' + esc(siteUrl(c.link)) + '">' + esc(c.linkText) + '</a>' : '') +
        '</p>' +
        '<button type="button" class="office-banner__close" aria-label="Close this announcement">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>' +
        '</button>' +
      '</div>';
    el.querySelector('.office-banner__close').addEventListener('click', function () {
      if (c.id) store(false, c.id);
      el.remove();
      window.dispatchEvent(new Event('resize'));   // review ticks re-place themselves
    });
    header.parentNode.insertBefore(el, header);
  }

  if (mode === 'badge') badge();
  if (mode === 'banner') banner();
})();

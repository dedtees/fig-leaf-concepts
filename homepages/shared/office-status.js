/* ==========================================================================
   Office status and announcements (builds 1 to 4).
   The settings are in office-config.js; this file only draws them.

   <html data-office="badge">   builds 1 and 2: "Open now · until 5 PM" in the
                                top bar (and a compact pill beside the phone
                                and menu buttons on phones), with the week's
                                hours in a drop-down.
   <html data-office="banner">  builds 3 and 4: a dismissible announcement
                                above the header; closing it is remembered
                                per message id.
   ========================================================================== */
(function () {
  'use strict';
  var cfg = window.FIG_LEAF_OFFICE;
  var mode = document.documentElement.getAttribute('data-office');
  if (!cfg || !mode) return;

  var params = new URLSearchParams(location.search);
  var DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
  var DAY_NAMES = { sun: 'Sun', mon: 'Mon', tue: 'Tue', wed: 'Wed', thu: 'Thu', fri: 'Fri', sat: 'Sat' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

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
    return {
      y: +parts.year, m: +parts.month, d: +parts.day,
      mins: (+parts.hour % 24) * 60 + (+parts.minute)
    };
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
  function hoursOn(day) {
    if (holiday(day.iso)) return null;
    return (cfg.hours || {})[day.key] || null;
  }

  /* ---- what the badge says ---------------------------------------------- */
  function status() {
    var now = officeNow();
    var today = dayAt(now, 0);
    var ov = cfg.override || {};
    var forced = params.get('office');            // preview: ?office=snow|open|closed
    var ovStatus = ov.status || 'auto';
    if (ovStatus !== 'auto' && ov.until && today.iso > ov.until) ovStatus = 'auto';
    if (forced === 'snow' || forced === 'closed') ovStatus = 'closed';
    if (forced === 'open') ovStatus = 'open';

    if (ovStatus === 'closed') {
      var note = forced === 'closed' ? '' : (ov.note || '');
      return { open: false, label: 'Closed today', detail: note, short: 'Closed', note: note };
    }
    if (ovStatus === 'open') return { open: true, label: 'Open now', detail: '', short: 'Open' };

    var h = hoursOn(today);
    if (h && now.mins >= toMins(h[0]) && now.mins < toMins(h[1])) {
      return { open: true, label: 'Open now', detail: 'until ' + fmt(h[1]), short: 'Open', shortDetail: 'till ' + fmt(h[1]) };
    }
    var hol = holiday(today.iso);
    if (hol) return { open: false, label: 'Closed today', detail: hol.label, short: 'Closed', note: hol.label };
    if (h && now.mins < toMins(h[0])) {
      return { open: false, label: 'Closed', detail: 'opens ' + fmt(h[0]), short: 'Closed', shortDetail: 'opens ' + fmt(h[0]) };
    }
    for (var k = 1; k <= 14; k++) {
      var d = dayAt(now, k), dh = hoursOn(d);
      if (dh) {
        var when = k === 1 ? 'tomorrow' : DAY_NAMES[d.key];
        return { open: false, label: 'Closed', detail: 'opens ' + when + ' ' + fmt(dh[0]), short: 'Closed' };
      }
    }
    return { open: false, label: 'Closed', detail: '', short: 'Closed' };
  }

  /* The week as rows: "Mon – Fri  9 AM – 5 PM", "Sat – Sun  Closed". */
  function weekRows() {
    var order = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
    var rows = [];
    order.forEach(function (key) {
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

  /* ---- builds 1 and 2: the badge ---------------------------------------- */
  function badge() {
    var bar = document.querySelector('.utility__inner');
    var actions = document.querySelector('.site-header__actions');
    if (!bar && !actions) return;
    var uid = 0;

    function make(variant) {
      var id = 'office-panel-' + (++uid);
      var wrap = document.createElement('div');
      wrap.className = 'office-badge office-badge--' + variant;
      wrap.setAttribute('data-review', 'Office open / closed badge');
      wrap.innerHTML =
        '<button type="button" class="office-badge__toggle" aria-expanded="false" aria-controls="' + id + '">' +
          '<span class="office-badge__dot" aria-hidden="true"></span>' +
          '<span class="office-badge__text"></span>' +
        '</button>' +
        '<div class="office-badge__panel" id="' + id + '" hidden>' +
          '<p class="office-badge__head">Office hours</p>' +
          '<p class="office-badge__note" hidden></p>' +
          '<ul class="office-badge__week">' + weekRows() + '</ul>' +
          (cfg.stillReachable ? '<p class="office-badge__reach">' + esc(cfg.stillReachable) + '</p>' : '') +
        '</div>';
      var btn = wrap.querySelector('button'), panel = wrap.querySelector('.office-badge__panel');
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open));
        panel.hidden = !open;
      });
      document.addEventListener('click', function (e) {
        if (!wrap.contains(e.target)) { btn.setAttribute('aria-expanded', 'false'); panel.hidden = true; }
      });
      wrap.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { btn.setAttribute('aria-expanded', 'false'); panel.hidden = true; btn.focus(); }
      });
      return wrap;
    }

    var items = [];
    if (bar) {
      var full = make('bar');
      var address = bar.querySelector('.utility__item');
      bar.insertBefore(full, address ? address.nextSibling : bar.firstChild);
      items.push({ el: full, compact: false });
    }
    if (actions) {
      var pill = make('compact');
      actions.insertBefore(pill, actions.firstChild);
      items.push({ el: pill, compact: true });
    }

    function render() {
      var s = status();
      items.forEach(function (it) {
        it.el.classList.toggle('is-open', s.open);
        it.el.classList.toggle('is-closed', !s.open);
        var detail = it.compact ? (s.shortDetail || '') : s.detail;
        var label = it.compact ? s.short : s.label;
        it.el.querySelector('.office-badge__text').innerHTML =
          '<strong>' + esc(label) + '</strong>' + (detail ? '<span> · ' + esc(detail) + '</span>' : '');
        it.el.querySelector('button').setAttribute('aria-label',
          'Office ' + s.label.toLowerCase() + (s.detail ? ', ' + s.detail : '') + '. Show office hours');
        var note = it.el.querySelector('.office-badge__note');
        note.hidden = !s.note;
        note.textContent = s.note ? 'Closed today: ' + s.note + '.' : '';
      });
    }
    render();
    setInterval(render, 60 * 1000);
  }

  /* ---- builds 3 and 4: the announcement banner --------------------------- */
  var ICONS = {
    snow: '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11"/><path d="m9 3.5 3 2.5 3-2.5M9 20.5l3-2.5 3 2.5M3.6 10l3.7 1.3-.8 3.8M20.4 14l-3.7-1.3.8-3.8M3.6 14l3.7-1.3-.8-3.8M20.4 10l-3.7 1.3.8 3.8"/>',
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

  function banner() {
    var b = cfg.banner;
    if (!b || !b.show) return;
    if (params.get('banner') === 'show') store(false, '');
    if (b.id && store(true) === b.id) return;
    var header = document.querySelector('.site-header');
    if (!header) return;

    var el = document.createElement('div');
    el.className = 'office-banner office-banner--' + (b.icon || 'info');
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', 'Announcement');
    el.setAttribute('data-review', 'Announcement banner');
    el.innerHTML =
      '<div class="office-banner__inner">' +
        '<svg class="office-banner__icon" viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[b.icon] || ICONS.info) + '</svg>' +
        '<p class="office-banner__text">' +
          (b.title ? '<strong>' + esc(b.title) + '</strong> ' : '') + esc(b.text || '') +
          (b.link && b.linkText ? ' <a class="office-banner__link" href="' + esc(siteUrl(b.link)) + '">' + esc(b.linkText) + '</a>' : '') +
        '</p>' +
        '<button type="button" class="office-banner__close" aria-label="Close this announcement">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>' +
        '</button>' +
      '</div>';
    el.querySelector('.office-banner__close').addEventListener('click', function () {
      if (b.id) store(false, b.id);
      el.remove();
      window.dispatchEvent(new Event('resize'));   // review ticks re-place themselves
    });
    header.parentNode.insertBefore(el, header);
  }

  if (mode === 'badge') badge();
  if (mode === 'banner') banner();
})();

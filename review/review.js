/* Client review ticks
   ---------------------------------------------------------------------------
   For the review round only, not part of the site design. Every section of a
   page gets a small tick in its top corner: a check (I like this), a cross
   (I don't) and a note button for an optional comment. A "Review" button in
   the bottom corner lists every pick across all the concepts and sends them.

   Picks are kept in the browser (localStorage), so they survive moving
   between pages and reloading. To also collect them live in a Google Sheet,
   paste the Apps Script web app URL into ENDPOINT below (setup steps are in
   review/google-sheet-setup.md). With no URL the "Send my feedback" button
   opens an email with the summary instead.

   Turn the ticks off for a visit with ?review=off in the address.
   ------------------------------------------------------------------------- */
(function () {
  'use strict';

  var CONFIG = {
    // Google Apps Script web app URL (ends in /exec). Empty = no live collection.
    ENDPOINT: 'https://script.google.com/macros/s/AKfycbxhR85z71EIh1GCcazCWNsgTBIpHDseSJRehvXUt2VI1PVWvlwKM5IR-z283Xid4DCBaQ/exec',
    // Who the "Send my feedback" email goes to when there is no ENDPOINT.
    EMAIL: '',
    EMAIL_SUBJECT: 'Fig Leaf website concepts: my feedback'
  };

  var STORE_KEY = 'flReview.v1';
  var params = new URLSearchParams(location.search);
  if (params.get('review') === 'off') return;

  /* ---- storage --------------------------------------------------------- */
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(STORE_KEY));
      if (s && s.picks) return s;
    } catch (e) {}
    return { reviewer: '', rid: '', hidden: false, picks: {} };
  }
  function save() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) {}
  }
  var state = load();
  if (!state.rid) { state.rid = Math.random().toString(36).slice(2, 10); save(); }

  /* ---- which page is this ---------------------------------------------- */
  var path = location.pathname.replace(/index\.html$/, '');
  if (!/\/$/.test(path)) path += '/';
  var parts = path.split('/').filter(Boolean);
  // One site now (build 5 at the root): every pick goes under "Website" and
  // the page is named from its address.
  var PAGE_NAMES = {
    '': 'Homepage',
    'crq': 'Quote page',
    'crq-form': 'Quote form',
    'about': 'About',
    'testimonials': 'Testimonials',
    'carriers': 'Carriers',
    'contact': 'Contact',
    'privacy-policy': 'Privacy Policy',
    'terms-conditions': 'Terms & Conditions',
    'workers-comp-insurance': "Workers' Comp Insurance"
  };
  function titleCase(s) { return s.replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); }); }
  var root = document.documentElement;
  var conceptLabel = root.getAttribute('data-review-concept') || 'Website';
  var tail = parts.length ? parts[parts.length - 1] : '';
  var pageLabel = PAGE_NAMES.hasOwnProperty(tail) ? PAGE_NAMES[tail] : titleCase(tail);
  // a team bio sits under about/: label it as that person's bio
  if (parts.length > 1 && parts[parts.length - 2] === 'about' && !PAGE_NAMES.hasOwnProperty(tail)) pageLabel = 'Bio: ' + titleCase(tail);
  if (root.getAttribute('data-review-page')) pageLabel = root.getAttribute('data-review-page');

  /* ---- styles ---------------------------------------------------------- */
  var me = document.currentScript;
  var css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = (me && me.src ? me.src.replace(/review\.js(\?.*)?$/, '') : '/review/') + 'review.css';
  document.head.appendChild(css);

  /* ---- icons ------------------------------------------------------------ */
  var ICON = {
    like: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    dislike: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/></svg>',
    note: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.5 5.5h15v10h-8l-4.5 3.5v-3.5h-2.5z"/></svg>'
  };

  /* ---- find the sections ----------------------------------------------- */
  function slug(s, n) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, n || 40) || 'section'; }
  function textOf(el) {
    if (!el) return '';
    var c = el.cloneNode(true);
    c.querySelectorAll('.visually-hidden, [aria-hidden="true"]').forEach(function (n) { n.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  function labelFor(el, i) {
    if (el.matches('.site-header')) return 'Header and menu';
    if (el.matches('footer, .hs-footer')) return 'Footer';
    if (el.matches('main')) return el.querySelector('iframe') ? 'Quote form' : 'Page content';
    if (el.querySelector('h1')) return 'Hero';
    if (el.matches('.pg-strip')) return 'Photo strip';
    var t = '';
    var by = el.getAttribute('aria-labelledby');
    if (by) t = textOf(document.getElementById(by.split(' ')[0]));
    if (!t) t = el.getAttribute('aria-label') || '';
    if (!t) t = textOf(el.querySelector('h2, h3, legend'));
    t = t || 'Section ' + (i + 1);
    return t.length > 60 ? t.slice(0, 57) + '…' : t;
  }
  // Smaller parts that get a tick of their own inside their section: things
  // the client was asked about by name. Any element can opt in with
  // data-review="Label".
  var SUB_ITEMS = [
    ['.vr-video', 'Video testimonial'],
    ['.fla', 'Floating Get a Quote and back-to-top buttons'],
    ['.ab-card--help, .b3-help, .b5-help', 'Can help you card'],
    ['.ab-card--offclock, .b2-offclock, .b5-offclock', 'Off the clock card'],
    ['[data-review]', null]
  ];
  function findSubItems() {
    var out = [];
    SUB_ITEMS.forEach(function (s) {
      document.querySelectorAll(s[0]).forEach(function (el) {
        if (el.closest('.flr-ui') || out.some(function (o) { return o.el === el; })) return;
        if (el.offsetHeight < 20) return;
        var label = s[1] || el.getAttribute('data-review');
        var n = out.filter(function (o) { return o.base === label; }).length;
        out.push({ el: el, base: label, label: n ? label + ' ' + (n + 1) : label });
      });
    });
    return out;
  }
  function findSections() {
    var main = document.querySelector('main') || document.body;
    var list = [].slice.call(document.querySelectorAll(
      '.site-header, main section, main.ab > article, main > header, main > .pg-strip, main > .pg-body > aside, footer.hs-footer, body > footer'));
    list = list.filter(function (el) {
      if (el.closest('.flr-ui')) return false;
      if (el.hasAttribute('data-review-skip')) return false;   // e.g. a breadcrumb-only band
      if (el.offsetHeight < 50) return false;
      // keep only the outermost: skip anything inside another candidate
      for (var p = el.parentElement; p; p = p.parentElement) if (list.indexOf(p) > -1) return false;
      return true;
    });
    var inMain = list.some(function (el) { return main.contains(el); });
    if (!inMain && main !== document.body) {
      var at = list.findIndex(function (el) { return main.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING; });
      list.splice(at < 0 ? list.length : at, 0, main);
    }
    return list;
  }

  /* ---- send to the sheet (when ENDPOINT is set) ------------------------- */
  function rowFor(key, p) {
    return {
      reviewer: state.reviewer || '',
      reviewerId: state.rid,
      concept: p.concept,
      page: p.page,
      section: p.section,
      verdict: p.verdict === 'like' ? 'Like' : p.verdict === 'dislike' ? "Don't like" : '',
      comment: p.note || '',
      url: p.url,
      order: p.order || 0,
      key: key,
      at: p.at
    };
  }
  function post(rows) {
    if (!CONFIG.ENDPOINT) return Promise.resolve(false);
    return fetch(CONFIG.ENDPOINT, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify({ rows: rows })
    }).then(function () { return true; }, function () { return false; });
  }
  var pending = {}, timer = null;
  function queueSync(key) {
    if (!CONFIG.ENDPOINT) return;
    pending[key] = true;
    clearTimeout(timer);
    timer = setTimeout(function () {
      // a pick that was taken back is sent as a delete, so its row goes too
      var rows = Object.keys(pending).map(function (k) {
        return state.picks[k] ? rowFor(k, state.picks[k]) : { reviewerId: state.rid, key: k, deleted: true };
      });
      pending = {};
      post(rows);
    }, 800);
  }

  /* ---- the tick on each section ----------------------------------------- */
  var openNote = null;
  function closeNote() {
    if (!openNote) return;
    openNote.classList.remove('is-open');
    var b = openNote.parentNode.querySelector('.flr-btn--note');
    if (b) b.setAttribute('aria-expanded', 'false');
    openNote = null;
  }

  function build(el, i, used, given) {
    var label = given || labelFor(el, i);
    var id = slug(label, given ? 90 : 40);
    while (used[id]) id += '-2';
    used[id] = true;
    var key = path + '#' + id;

    // a pick made before a label changed (e.g. the quote pages were "Get a
    // quote") takes this page's current names, here and in the sheet
    var old = state.picks[key];
    if (old && (old.concept !== conceptLabel || old.page !== pageLabel)) {
      old.concept = conceptLabel; old.page = pageLabel; save(); queueSync(key);
    }

    if (getComputedStyle(el).position === 'static') el.classList.add('flr-host');
    var box = document.createElement('div');
    box.className = 'flr-ui flr-tick';
    box.setAttribute('role', 'group');
    box.setAttribute('aria-label', 'Your view of this section: ' + label);
    box.innerHTML =
      '<button type="button" class="flr-btn flr-btn--like" aria-pressed="false" title="I like this section">' + ICON.like + '<span class="flr-vh">Like</span></button>' +
      '<button type="button" class="flr-btn flr-btn--dislike" aria-pressed="false" title="I don\'t like this section">' + ICON.dislike + '<span class="flr-vh">Don\'t like</span></button>' +
      '<button type="button" class="flr-btn flr-btn--note" aria-expanded="false" title="Add a comment">' + ICON.note + '<span class="flr-vh">Comment</span></button>' +
      '<div class="flr-note"><label class="flr-note__label">' + escapeHtml(label) +
      '<textarea rows="3" placeholder="Optional: what do you like or want changed?"></textarea></label>' +
      '<div class="flr-note__row"><span class="flr-note__saved" aria-live="polite"></span><button type="button" class="flr-note__done">Done</button></div></div>';
    if (el.matches('.site-header')) box.classList.add('flr-tick--header');
    if (given) box.classList.add('flr-tick--sub');
    el.appendChild(box);

    var like = box.querySelector('.flr-btn--like');
    var dislike = box.querySelector('.flr-btn--dislike');
    var noteBtn = box.querySelector('.flr-btn--note');
    var note = box.querySelector('.flr-note');
    var ta = note.querySelector('textarea');
    var saved = note.querySelector('.flr-note__saved');

    function current() { return state.picks[key]; }
    function update(changes) {
      var p = current() || { concept: conceptLabel, page: pageLabel, section: label, url: location.origin + path, verdict: null, note: '' };
      for (var k in changes) p[k] = changes[k];
      p.section = label; p.order = i; p.at = new Date().toISOString();
      if (!p.verdict && !p.note) delete state.picks[key]; else state.picks[key] = p;
      save(); paint(); queueSync(key); refreshPanel();
    }
    function paint() {
      var p = current() || {};
      like.setAttribute('aria-pressed', String(p.verdict === 'like'));
      dislike.setAttribute('aria-pressed', String(p.verdict === 'dislike'));
      box.classList.toggle('is-set', !!p.verdict);
      noteBtn.classList.toggle('has-note', !!p.note);
      if (document.activeElement !== ta) ta.value = p.note || '';
    }
    function openTheNote() {
      if (openNote && openNote !== note) closeNote();
      note.classList.add('is-open'); noteBtn.setAttribute('aria-expanded', 'true'); openNote = note;
      setTimeout(function () { ta.focus(); }, 0);
    }

    like.addEventListener('click', function () {
      update({ verdict: (current() || {}).verdict === 'like' ? null : 'like' });
    });
    dislike.addEventListener('click', function () {
      var on = (current() || {}).verdict !== 'dislike';
      update({ verdict: on ? 'dislike' : null });
      if (on && !(current() || {}).note) openTheNote();
    });
    noteBtn.addEventListener('click', function () {
      if (note.classList.contains('is-open')) closeNote(); else openTheNote();
    });
    note.querySelector('.flr-note__done').addEventListener('click', closeNote);
    var t2;
    ta.addEventListener('input', function () {
      update({ note: ta.value.trim() });
      saved.textContent = 'Saved';
      clearTimeout(t2); t2 = setTimeout(function () { saved.textContent = ''; }, 1200);
    });
    paint();
    return { paint: paint, place: function () { place(el, box); } };
  }

  // Keep a tick clear of anything drawn over its section, such as a header
  // that sits on top of the hero: move it down until nothing covers it.
  // The header's tick goes in its top-right corner, at the first height where
  // it touches none of the header's links, buttons, logo or text.
  function placeHeader(el, box) {
    box.style.top = '';
    var er = el.getBoundingClientRect();
    var bh = box.offsetHeight, bw = box.offsetWidth;
    if (!bw) return;
    var right = er.right - 20, left = right - bw;
    var items = [].slice.call(el.querySelectorAll('a, button, img, svg, input, select, p, span, li'))
      .filter(function (n) {
        if (box.contains(n)) return false;
        if (/^(P|SPAN|LI)$/.test(n.tagName) && !n.textContent.trim()) return false;
        for (var a = n; a && a !== el; a = a.parentElement) {
          var cs = getComputedStyle(a);
          if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
        }
        var r = n.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      })
      .map(function (n) { return n.getBoundingClientRect(); });
    for (var y = 8; y + bh <= er.height - 4; y += 2) {
      var top = er.top + y, bottom = top + bh;
      var clash = items.some(function (r) {
        return r.left < right + 8 && r.right > left - 8 && r.top < bottom + 4 && r.bottom > top - 4;
      });
      if (!clash) { box.style.top = y + 'px'; return; }
    }
    // no free spot inside: hang it just under the header's bottom edge
    box.style.top = (er.height - bh / 2) + 'px';
  }

  function place(el, box) {
    if (box.classList.contains('flr-tick--header')) return placeHeader(el, box);
    box.style.top = '';
    var r = box.getBoundingClientRect();
    if (!r.width) return;
    var er = el.getBoundingClientRect();
    var shift = 0;
    // a header or the concept bar drawn over the top of this section
    document.querySelectorAll('.site-header, .review-bar, .flr-tick--header').forEach(function (c) {
      if (el.contains(c) || c.contains(el)) return;
      var cr = c.getBoundingClientRect();
      if (cr.bottom > r.top + shift && cr.top < r.bottom + shift && cr.left < r.right && cr.right > r.left) {
        shift = Math.max(shift, cr.bottom - r.top + 12);
      }
    });
    if (shift) box.style.top = (r.top - er.top + shift) + 'px';
  }

  /* ---- the review panel -------------------------------------------------- */
  var fab, panel, listEl, countEl;
  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function sortedPicks() {
    return Object.keys(state.picks).map(function (k) { return [k, state.picks[k]]; })
      .sort(function (a, b) {
        var pa = a[0].split('#')[0], pb = b[0].split('#')[0];
        if (pa !== pb) return pa.localeCompare(pb, undefined, { numeric: true });
        return (a[1].order || 0) - (b[1].order || 0);
      });
  }
  function summaryText() {
    var out = [], last = '';
    out.push('Feedback on the Fig Leaf website concepts' + (state.reviewer ? ' from ' + state.reviewer : ''));
    sortedPicks().forEach(function (e) {
      var p = e[1], head = p.concept + ', ' + p.page;
      if (head !== last) { out.push(''); out.push(head); last = head; }
      var v = p.verdict === 'like' ? 'Like' : p.verdict === 'dislike' ? "Don't like" : 'Comment';
      out.push('- ' + p.section + ': ' + v + (p.note ? '. "' + p.note + '"' : ''));
    });
    return out.join('\n');
  }
  function csv() {
    var head = ['Reviewer', 'Concept', 'Page', 'Section', 'Verdict', 'Comment', 'Link', 'When'];
    var rows = sortedPicks().map(function (e) {
      var r = rowFor(e[0], e[1]);
      return [r.reviewer, r.concept, r.page, r.section, r.verdict, r.comment, r.url, r.at];
    });
    return [head].concat(rows).map(function (r) {
      return r.map(function (c) { c = String(c == null ? '' : c); return /[",\n]/.test(c) ? '"' + c.replace(/"/g, '""') + '"' : c; }).join(',');
    }).join('\r\n');
  }

  function refreshPanel() {
    if (!fab) return;
    var all = sortedPicks();
    var likes = all.filter(function (e) { return e[1].verdict === 'like'; }).length;
    var dislikes = all.filter(function (e) { return e[1].verdict === 'dislike'; }).length;
    countEl.textContent = all.length ? likes + ' ✓  ' + dislikes + ' ✕' : '';
    fab.classList.toggle('has-count', !!all.length);
    if (!panel.classList.contains('is-open')) return;
    if (!all.length) { listEl.innerHTML = '<p class="flr-empty">Nothing picked yet. Use the ✓ and ✕ in the corner of each section as you look through the concepts.</p>'; return; }
    var html = '', last = '';
    all.forEach(function (e) {
      var p = e[1], head = p.concept + ' · ' + p.page;
      if (head !== last) {
        if (last) html += '</ul>';
        html += '<h3 class="flr-group"><a href="' + escapeHtml(p.url) + '">' + escapeHtml(head) + '</a></h3><ul class="flr-list">';
        last = head;
      }
      var cls = p.verdict === 'like' ? 'is-like' : p.verdict === 'dislike' ? 'is-dislike' : 'is-note';
      var mark = p.verdict === 'like' ? '✓' : p.verdict === 'dislike' ? '✕' : '…';
      html += '<li class="' + cls + '"><span class="flr-mark" aria-hidden="true">' + mark + '</span><span><strong>' + escapeHtml(p.section) + '</strong>' +
        (p.note ? '<span class="flr-list__note">' + escapeHtml(p.note) + '</span>' : '') + '</span></li>';
    });
    listEl.innerHTML = html + '</ul>';
  }

  function flash(btn, text) {
    var old = btn.textContent; btn.textContent = text;
    setTimeout(function () { btn.textContent = old; }, 1600);
  }

  function buildPanel() {
    fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'flr-ui flr-fab';
    fab.setAttribute('aria-expanded', 'false');
    fab.innerHTML = '<span class="flr-fab__dot" aria-hidden="true">' + ICON.like + '</span><span>Your review</span><span class="flr-fab__count"></span>';
    countEl = fab.querySelector('.flr-fab__count');

    panel = document.createElement('section');
    panel.className = 'flr-ui flr-panel';
    panel.setAttribute('aria-label', 'Your review');
    panel.innerHTML =
      '<div class="flr-panel__head"><h2>Your review</h2><button type="button" class="flr-x" aria-label="Close">' + ICON.dislike + '</button></div>' +
      '<p class="flr-panel__intro">Tick ✓ or ✕ in the corner of any section, on any concept. Your picks are saved as you go' +
      (CONFIG.ENDPOINT ? ' and sent to the Fig Leaf team automatically.' : '. Press Send when you\'re done.') + '</p>' +
      '<label class="flr-name">Your name <input type="text" autocomplete="name" placeholder="So we know whose picks these are"></label>' +
      '<div class="flr-panel__list"></div>' +
      '<div class="flr-panel__actions">' +
        '<button type="button" class="flr-act flr-act--send">Send my feedback</button>' +
        '<button type="button" class="flr-act flr-act--copy">Copy</button>' +
        '<button type="button" class="flr-act flr-act--csv">Download</button>' +
      '</div>' +
      '<div class="flr-panel__foot"><button type="button" class="flr-link flr-act--hide"></button><button type="button" class="flr-link flr-act--clear">Clear all picks</button></div>';
    listEl = panel.querySelector('.flr-panel__list');

    var name = panel.querySelector('.flr-name input');
    name.value = state.reviewer || '';
    name.addEventListener('change', function () {
      state.reviewer = name.value.trim(); save();
      if (CONFIG.ENDPOINT) post(sortedPicks().map(function (e) { return rowFor(e[0], e[1]); }));
    });

    function setOpen(on) {
      panel.classList.toggle('is-open', on);
      fab.setAttribute('aria-expanded', String(on));
      if (on) { refreshPanel(); } else { fab.focus(); }
    }
    fab.addEventListener('click', function () { setOpen(!panel.classList.contains('is-open')); });
    panel.querySelector('.flr-x').addEventListener('click', function () { setOpen(false); });

    panel.querySelector('.flr-act--send').addEventListener('click', function () {
      var btn = this;
      state.reviewer = name.value.trim(); save();
      if (CONFIG.ENDPOINT) {
        btn.textContent = 'Sending…';
        post(sortedPicks().map(function (e) { return rowFor(e[0], e[1]); })).then(function (ok) {
          btn.textContent = ok ? 'Sent. Thank you!' : 'Could not send. Try Copy instead';
          setTimeout(function () { btn.textContent = 'Send my feedback'; }, 2500);
        });
        return;
      }
      var body = summaryText();
      if (body.length > 1800) {
        copy(body);
        body = body.slice(0, 1700) + '\n\n(The full list is on your clipboard. Paste it here to replace this.)';
      }
      location.href = 'mailto:' + encodeURIComponent(CONFIG.EMAIL) + '?subject=' + encodeURIComponent(CONFIG.EMAIL_SUBJECT) + '&body=' + encodeURIComponent(body);
    });
    function copy(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
      var t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); } catch (e) {}
      t.remove(); return Promise.resolve();
    }
    panel.querySelector('.flr-act--copy').addEventListener('click', function () {
      var btn = this;
      Promise.resolve(copy(summaryText())).then(function () { flash(btn, 'Copied'); }, function () { flash(btn, 'Copy failed'); });
    });
    panel.querySelector('.flr-act--csv').addEventListener('click', function () {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob(['﻿' + csv()], { type: 'text/csv' }));
      a.download = 'fig-leaf-review' + (state.reviewer ? '-' + slug(state.reviewer) : '') + '.csv';
      document.body.appendChild(a); a.click(); a.remove();
    });
    var hideBtn = panel.querySelector('.flr-act--hide');
    function paintHidden() {
      document.documentElement.classList.toggle('flr-hidden', !!state.hidden);
      hideBtn.textContent = state.hidden ? 'Show the ticks' : 'Hide the ticks';
    }
    hideBtn.addEventListener('click', function () { state.hidden = !state.hidden; save(); paintHidden(); });
    paintHidden();
    var clearBtn = panel.querySelector('.flr-act--clear'), armed = null;
    clearBtn.addEventListener('click', function () {
      if (!armed) {
        clearBtn.textContent = 'Press again to clear everything';
        armed = setTimeout(function () { armed = null; clearBtn.textContent = 'Clear all picks'; }, 3000);
        return;
      }
      clearTimeout(armed); armed = null;
      var keys = Object.keys(state.picks);
      state.picks = {}; save();
      keys.forEach(queueSync);
      ticks.forEach(function (t) { t.paint(); });
      clearBtn.textContent = 'Clear all picks';
      refreshPanel();
    });

    document.body.appendChild(panel);
    document.body.appendChild(fab);
  }

  /* ---- for other review tools ------------------------------------------- */
  // A pick that isn't tied to a section on this page. key is site-wide.
  window.flReview = {
    get: function (key) { return state.picks[key] || null; },
    set: function (key, p) {
      if (p) {
        var cur = state.picks[key] || {};
        state.picks[key] = { concept: p.concept, page: p.page, section: p.section, url: p.url || location.origin + path,
          verdict: p.verdict || null, note: p.note || cur.note || '', order: p.order || 0, at: new Date().toISOString() };
      } else {
        delete state.picks[key];
      }
      save(); queueSync(key); refreshPanel();
    }
  };

  /* ---- start ------------------------------------------------------------ */
  var ticks = [];
  function start() {
    var used = {};
    var sections = findSections();
    sections.forEach(function (el, i) { ticks.push(build(el, i, used)); });
    // sub-items sort just after the section they sit in
    findSubItems().forEach(function (s) {
      var at = sections.findIndex(function (sec) { return sec.contains(s.el); });
      if (at < 0) at = sections.length;
      ticks.push(build(s.el, at + 0.5, used, s.label));
    });
    buildPanel();
    refreshPanel();
    function placeAll() { ticks.forEach(function (t) { t.place(); }); ticks.forEach(function (t) { t.place(); }); }
    var pt;
    function placeSoon() { clearTimeout(pt); pt = setTimeout(placeAll, 150); }
    window.addEventListener('load', placeSoon);
    window.addEventListener('resize', placeSoon);
    placeSoon();

    // Keys typed into the review UI must not drive the page (the concept bar
    // and slideshows listen for the arrow keys).
    ['keydown', 'keyup', 'keypress'].forEach(function (type) {
      document.addEventListener(type, function (e) {
        if (e.target.closest && e.target.closest('.flr-ui')) {
          if (e.key === 'Escape') closeNote();
          e.stopPropagation();
        }
      }, true);
    });
    document.addEventListener('click', function (e) {
      if (openNote && !openNote.parentNode.contains(e.target)) closeNote();
    });
    // Picks made in another tab show up here too.
    window.addEventListener('storage', function (e) {
      if (e.key !== STORE_KEY) return;
      state = load(); ticks.forEach(function (t) { t.paint(); }); refreshPanel();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();

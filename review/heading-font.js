/* Heading font picker
   ---------------------------------------------------------------------------
   For the review round only, not part of the site design. Loaded by
   review.js on every page that has the review ticks. A small "Aa" button in
   the bottom left corner swaps the large serif used for page titles, section
   headings and names, so the options can be compared on the real pages.

   Lora is the site default (set in the CSS). A page whose <html> has
   data-heading-font (builds 1 to 5: "gelasio", approved 25 Nov) starts on
   that font instead. The choice is kept in the
   browser, so it follows you from page to page. A link can also set it:
   ?font=lora, ?font=source-serif, ?font=gelasio or ?font=fraunces.
   ------------------------------------------------------------------------- */
(function () {
  'use strict';

  var FONTS = [
    { id: 'lora', name: 'Lora', note: 'Recommended', family: '"Lora", Georgia, serif', css: null },
    { id: 'source-serif', name: 'Source Serif 4', note: 'Matches the body text',
      family: '"Source Serif 4", Georgia, serif',
      css: 'family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700' },
    { id: 'gelasio', name: 'Gelasio', note: 'Sturdy, Georgia-like (approved)',
      family: '"Gelasio", Georgia, serif', css: 'family=Gelasio:wght@500;600;700' },
    { id: 'fraunces', name: 'Fraunces', note: 'The old font',
      family: '"Fraunces", Georgia, serif',
      css: 'family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700' }
  ];
  var KEY = 'flHeadingFont';

  function byId(id) {
    for (var i = 0; i < FONTS.length; i++) if (FONTS[i].id === id) return FONTS[i];
    return null;
  }
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function store(id) { try { localStorage.setItem(KEY, id); } catch (e) {} }

  var fromUrl = byId((new URLSearchParams(location.search).get('font') || '').toLowerCase());
  if (fromUrl) store(fromUrl.id);
  // the font the page's own CSS sets: no override needed for it
  var base = byId(document.documentElement.getAttribute('data-heading-font') || '') || FONTS[0];
  var current = fromUrl || byId(stored()) || base;

  var loaded = {};
  var style = document.createElement('style');
  style.id = 'fl-heading-font';
  document.head.appendChild(style);

  function apply(font) {
    current = font;
    if (font.css && !loaded[font.id]) {
      loaded[font.id] = true;
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/css2?' + font.css + '&display=swap';
      document.head.appendChild(link);
    }
    // The default needs no override; every other choice replaces the three
    // heading variables the pages use, on every element so no section's own
    // definition wins.
    style.textContent = font.id === base.id ? '' :
      'html, html * { --font-heading: ' + font.family + ' !important; ' +
      '--hs-heading: ' + font.family + ' !important; ' +
      '--ab-serif: ' + font.family + ' !important; }';
    paintPrefer();
    if (btn) {
      btn.setAttribute('title', 'Heading font: ' + font.name);
      var items = menu.querySelectorAll('[data-font]');
      for (var i = 0; i < items.length; i++) {
        items[i].setAttribute('aria-checked', items[i].getAttribute('data-font') === font.id ? 'true' : 'false');
      }
    }
  }

  var btn = null, menu = null, prefer = null;

  // "I prefer this one": goes into the review (review.js) as a pick, one font
  // at a time, so the client's choice reaches the review sheet.
  function prefKey(id) { return '/heading-font/#' + id; }
  function preferred() {
    if (!window.flReview) return null;
    for (var i = 0; i < FONTS.length; i++) if (window.flReview.get(prefKey(FONTS[i].id))) return FONTS[i];
    return null;
  }
  function paintPrefer() {
    if (!prefer) return;
    prefer.hidden = !window.flReview;
    var mine = preferred();
    var on = mine && mine.id === current.id;
    prefer.setAttribute('aria-pressed', on ? 'true' : 'false');
    prefer.textContent = on ? '\u2713 Your pick: ' + current.name : '\u2713 I prefer ' + current.name;
    var items = menu.querySelectorAll('[data-font]');
    for (var i = 0; i < items.length; i++) items[i].classList.toggle('is-pick', !!mine && items[i].getAttribute('data-font') === mine.id);
  }
  function togglePrefer() {
    if (!window.flReview) return;
    var mine = preferred();
    FONTS.forEach(function (f) { if (window.flReview.get(prefKey(f.id))) window.flReview.set(prefKey(f.id), null); });
    if (!mine || mine.id !== current.id) {
      window.flReview.set(prefKey(current.id), { concept: 'Heading font', page: 'Heading font', section: current.name,
        verdict: 'like', order: FONTS.indexOf(current), url: location.origin + '/build-5/?font=' + current.id });
    }
    paintPrefer();
  }
  function build() {
    var css = document.createElement('style');
    css.textContent =
      '.flhf{position:fixed;left:16px;bottom:16px;z-index:2147483000;font:14px/1.3 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
      '.flhf__btn{width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.25);background:#070d0f;color:#e8c27e;' +
      'font:600 18px/1 Georgia,serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.3)}' +
      '.flhf__btn:focus-visible,.flhf__item:focus-visible{outline:2px solid #e8c27e;outline-offset:2px}' +
      '.flhf__menu{position:absolute;left:0;bottom:54px;width:250px;padding:8px;border-radius:12px;background:#070d0f;color:#fff;' +
      'border:1px solid rgba(255,255,255,.15);box-shadow:0 10px 30px rgba(0,0,0,.35)}' +
      '.flhf__menu[hidden]{display:none}' +
      '.flhf__head{margin:4px 8px 8px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#e8c27e}' +
      '.flhf__item{display:block;width:100%;text-align:left;padding:8px 10px 8px 30px;border:0;border-radius:8px;background:none;color:inherit;cursor:pointer;position:relative}' +
      '.flhf__item:hover{background:rgba(255,255,255,.08)}' +
      '.flhf__item[aria-checked="true"]::before{content:"";position:absolute;left:10px;top:50%;width:10px;height:10px;margin-top:-5px;border-radius:50%;background:#e8c27e}' +
      '.flhf__name{display:block;font-size:22px;line-height:1.2;font-weight:600}' +
      '.flhf__note{display:block;font-size:12px;color:rgba(255,255,255,.6)}' +
      '.flhf__item.is-pick .flhf__note::after{content:" \u00b7 your pick";color:#e8c27e}' +
      '.flhf__prefer{display:block;width:100%;margin-top:6px;padding:9px 10px;border-radius:8px;border:1px solid #e8c27e;background:none;color:#e8c27e;font:600 14px/1.2 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;cursor:pointer}' +
      '.flhf__prefer[aria-pressed="true"]{background:#e8c27e;color:#070d0f}' +
      '.flhf__prefer[hidden]{display:none}' +
      '.flhf__prefer:focus-visible{outline:2px solid #e8c27e;outline-offset:2px}';
    document.head.appendChild(css);

    var wrap = document.createElement('div');
    wrap.className = 'flhf';
    btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'flhf__btn';
    btn.textContent = 'Aa';
    btn.setAttribute('aria-haspopup', 'true');
    btn.setAttribute('aria-expanded', 'false');
    menu = document.createElement('div');
    menu.className = 'flhf__menu';
    menu.setAttribute('role', 'menu');
    menu.hidden = true;
    var html = '<p class="flhf__head">Heading font</p>';
    FONTS.forEach(function (f) {
      html += '<button type="button" role="menuitemradio" class="flhf__item" data-font="' + f.id + '">' +
        '<span class="flhf__name" style="font-family:' + f.family.replace(/"/g, '&quot;') + '">' + f.name + '</span>' +
        '<span class="flhf__note">' + f.note + '</span></button>';
    });
    html += '<button type="button" class="flhf__prefer" aria-pressed="false"></button>';
    menu.innerHTML = html;
    prefer = menu.querySelector('.flhf__prefer');
    prefer.addEventListener('click', function (e) { e.stopPropagation(); togglePrefer(); });
    wrap.appendChild(menu);
    wrap.appendChild(btn);
    document.body.appendChild(wrap);

    function toggle(open) {
      menu.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) FONTS.forEach(function (f) { if (f.css && !loaded[f.id]) { loaded[f.id] = true; preload(f); } });
    }
    btn.addEventListener('click', function () { toggle(menu.hidden); });
    menu.addEventListener('click', function (e) {
      var item = e.target.closest('[data-font]');
      if (!item) return;
      var f = byId(item.getAttribute('data-font'));
      store(f.id);
      apply(f);
      toggle(false);
    });
    document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) toggle(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') toggle(false); });
    apply(current);
  }

  function preload(f) {
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?' + f.css + '&display=swap';
    document.head.appendChild(link);
  }

  apply(current);
  if (document.body) build();
  else document.addEventListener('DOMContentLoaded', build);
})();

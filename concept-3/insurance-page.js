/* Fig Leaf interior pages. No dependencies; identical copies live in each
   concept folder.
   1. Tabs (concept 2): each tab shows its panel in place, in the same
      section, instead of scrolling the page. A link to #overview, #covered
      or #quote (like the header's "Get a Quote") opens that tab.
   2. "On this page" rail (concept 3): marks the section you're reading. */
(function () {
  'use strict';

  /* ---- 1. Tabs ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-pg-tabs]'), function (set) {
    var tabs = Array.prototype.slice.call(set.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    if (!tabs.length || panels.indexOf(null) !== -1) return;
    var bar = set.querySelector('.pg-tabs') || set;
    set.classList.add('is-tabbed');

    function select(i, focusTab) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
        if (on) panels[j].tabIndex = 0;
      });
      // show anything in the panel that was waiting to be revealed on scroll
      Array.prototype.forEach.call(panels[i].querySelectorAll('.hs-reveal'), function (el) { el.classList.add('is-in'); });
      if (focusTab) tabs[i].focus();
    }
    function indexForHash() {
      var id = location.hash.slice(1);
      for (var i = 0; i < panels.length; i++) if (panels[i].id === id) return i;
      return -1;
    }

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function (e) {
        e.preventDefault();
        select(i, false);
        if (history.replaceState) history.replaceState(null, '', '#' + panels[i].id);
      });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = tabs.length, to = -1;
        if (k === 'ArrowRight') to = (i + 1) % n;
        else if (k === 'ArrowLeft') to = (i - 1 + n) % n;
        else if (k === 'Home') to = 0;
        else if (k === 'End') to = n - 1;
        if (to < 0) return;
        e.preventDefault();
        select(to, true);
      });
    });

    // other links on the page that point at a panel open its tab, then
    // bring the tab bar into view
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a || set.contains(a)) return;
      var id = a.getAttribute('href').slice(1);
      for (var i = 0; i < panels.length; i++) {
        if (panels[i].id === id) {
          e.preventDefault();
          select(i, false);
          if (history.replaceState) history.replaceState(null, '', '#' + id);
          bar.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
          return;
        }
      }
    });

    var start = indexForHash();
    select(start < 0 ? 0 : start, false);
    if (start >= 0) {
      // land on the tab bar, not partway into the panel (the browser's own
      // jump to the #id runs too, so repeat once the page has loaded)
      bar.scrollIntoView({ block: 'start' });
      window.addEventListener('load', function () { bar.scrollIntoView({ block: 'start' }); });
    }
  });

  /* ---- 2. "On this page" rail ---- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.pg-rail ol a[href^="#"]'));
  if (!links.length) return;
  var targets = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var queued = false;

  function update() {
    queued = false;
    var line = window.innerHeight * 0.35;
    var current = 0;
    targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top <= line) current = i; });
    // at the very bottom, the last section is the one being read
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) current = targets.length - 1;
    links.forEach(function (a, i) {
      var on = targets[i] === targets[current];
      a.classList.toggle('is-active', on);
      if (on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', queue, { passive: true });
  window.addEventListener('resize', queue);
  update();
})();

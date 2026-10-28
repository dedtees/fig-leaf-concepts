/* Fig Leaf homepage sections: reveal on scroll, counting stats,
   image fallbacks and the footer year. No dependencies. */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;

  /* ---- image fallbacks -------------------------------------------------- */
  // Carrier logos fall back to the carrier's name, footer badges to their
  // alt text, and photos to a green placeholder, so a missing file never
  // leaves a broken-image icon.
  function fallback(img) {
    if (img.dataset.failed) return;
    img.dataset.failed = '1';
    var carrier = img.closest('.hs-carrier');
    if (carrier) { carrier.classList.add('is-fallback'); return; }
    if (img.dataset.fallback === 'text') {
      var span = document.createElement('span');
      span.className = img.classList.contains('hs-footer__logo') ? 'hs-footer__logo-text' : 'hs-footer__badge-text';
      span.textContent = img.alt;
      img.replaceWith(span);
      return;
    }
    var media = img.closest('.hs-service__media, .hs-about__media');
    if (media) media.classList.add('is-fallback');
    img.classList.add('hs-img-missing');
  }

  var imgs = document.querySelectorAll('img[data-fallback]');
  for (var i = 0; i < imgs.length; i++) {
    var img = imgs[i];
    if (img.complete && img.naturalWidth === 0 && img.currentSrc) fallback(img);
    else img.addEventListener('error', fallback.bind(null, img), { once: true });
  }

  /* ---- footer year ------------------------------------------------------ */
  var years = document.querySelectorAll('[data-year]');
  for (var y = 0; y < years.length; y++) years[y].textContent = String(new Date().getFullYear());

  /* ---- counting stats --------------------------------------------------- */
  function countUp(el) {
    var target = parseFloat(el.dataset.count);
    var decimals = parseInt(el.dataset.decimals || '0', 10);
    if (isNaN(target)) return;
    var start = null;
    var duration = 1400;
    function frame(t) {
      if (start === null) start = t;
      var p = Math.min(1, (t - start) / duration);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(target * eased);
      if (p < 1) requestAnimationFrame(frame);
    }
    // 1000 shows as 1,000
    function format(n) { return n.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }); }
    el.textContent = format(0);
    requestAnimationFrame(frame);
  }

  var counters = document.querySelectorAll('.hs [data-count]');
  if (counters.length && canObserve && !reduceMotion) {
    var countObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        countObserver.unobserve(entry.target);
        countUp(entry.target);
      });
    }, { threshold: 0.6 });
    for (var c = 0; c < counters.length; c++) countObserver.observe(counters[c]);
  }

  /* ---- reveal on scroll ------------------------------------------------- */
  if (!canObserve || reduceMotion) return;

  var reveals = document.querySelectorAll('.hs-reveal');
  root.classList.add('hs-js');

  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      revealObserver.unobserve(entry.target);
      // stagger items that come into view together, like a row of cards
      var siblings = entry.target.parentElement ? entry.target.parentElement.children : [];
      var index = Array.prototype.indexOf.call(siblings, entry.target);
      entry.target.style.transitionDelay = Math.min(index % 6, 5) * 70 + 'ms';
      entry.target.classList.add('is-in');
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  for (var r = 0; r < reveals.length; r++) revealObserver.observe(reveals[r]);

  // anything already scrolled past (e.g. a jump to #quote) shows at once
  window.addEventListener('load', function () {
    for (var k = 0; k < reveals.length; k++) {
      if (reveals[k].getBoundingClientRect().bottom < 0) reveals[k].classList.add('is-in');
    }
  });
})();

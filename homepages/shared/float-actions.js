/* Floating Get a Quote and back-to-top buttons (float-actions.css).
   - the arrow shows once the page has scrolled past about one screen, and
     takes you back to the top (from the keyboard, focus goes to the skip link)
   - on pages whose Get a Quote goes to the form further down (#quote), the
     button steps aside while that form is on screen, since it's right there
   - marks <html> so the review tools (review/) can move out of the way */
(function () {
  'use strict';
  var box = document.querySelector('.fla');
  if (!box) return;
  var root = document.documentElement;
  var top = box.querySelector('.fla__top');
  var quote = box.querySelector('.fla__quote');
  if (!box.classList.contains('fla--only-top')) root.classList.add('fla-bar');

  // the review tools load on their own; watch for their button
  function review() { if (document.querySelector('.flr-fab, .flhf')) root.classList.add('fla-review'); }
  review();
  if (!root.classList.contains('fla-review') && window.MutationObserver) {
    var mo = new MutationObserver(function () { review(); if (root.classList.contains('fla-review')) mo.disconnect(); });
    mo.observe(document.body, { childList: true });
    setTimeout(function () { mo.disconnect(); }, 10000);
  }

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ticking = false;
  function update() {
    ticking = false;
    var y = window.pageYOffset || root.scrollTop;
    var shown = y > Math.min(600, window.innerHeight * 0.8);
    if (top) top.classList.toggle('is-shown', shown);
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  update();

  if (top) {
    top.addEventListener('click', function (e) {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      if (e.detail !== 0) return;   // mouse or touch: no need to move focus
      var first = document.querySelector('.skip-link, .site-header a');
      if (first) try { first.focus({ preventScroll: true }); } catch (e) { first.focus(); }
    });
  }

  // a Get a Quote that points at this page's own form
  var hash = quote && quote.getAttribute('href');
  var form = hash && hash.charAt(0) === '#' ? document.getElementById(hash.slice(1)) : null;
  if (form && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      var on = entries[0].isIntersecting;
      quote.classList.toggle('is-away', on);
      box.classList.toggle('is-away', on);
      if (on) quote.setAttribute('tabindex', '-1'); else quote.removeAttribute('tabindex');
    }, { threshold: 0.25 }).observe(form);
  }
})();

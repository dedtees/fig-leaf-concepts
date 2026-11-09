/* Fig Leaf interior pages: marks the section you're reading in the
   "On this page" links (concept 2's tabs, concept 3's rail). No dependencies.
   Identical copies live in each concept folder. */
(function () {
  'use strict';
  var links = Array.prototype.slice.call(document.querySelectorAll('.pg-tabs a[href^="#"], .pg-rail ol a[href^="#"]'));
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

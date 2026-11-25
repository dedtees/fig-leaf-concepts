// About and bio pages.
// 1. The then / now frame (About, concept 2): the range input moves the line.
// 2. The chapter list (About, concept 4): marks the chapter on screen.
(function () {
  'use strict';

  document.querySelectorAll('[data-compare]').forEach(function (box) {
    var range = box.querySelector('input[type="range"]');
    if (!range) return;
    function set() { box.style.setProperty('--pos', range.value + '%'); }
    range.addEventListener('input', set);
    set();
  });

  var toc = document.querySelector('[data-toc]');
  if (toc && 'IntersectionObserver' in window) {
    var links = {};
    toc.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        if (current) current.removeAttribute('aria-current');
        current = links[e.target.id];
        if (current) current.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    Object.keys(links).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }
})();

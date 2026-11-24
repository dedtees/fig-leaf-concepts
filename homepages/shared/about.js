// About and bio pages (homepages/build.py links this on every one).
// 1. The then / now frame (About, concept 2): the range input moves the line.
// 2. The chapter list (About, concept 4): marks the chapter on screen.
// 3. The photo shape picker (bio, concept 4).
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

  // 3. Bio photo shape options (bio, concept 4): a review-only picker under
  //    the photo. The choice is kept for the other bios (and ?shape=name).
  var stage = document.querySelector('.b4-stage');
  if (stage) {
    var shapes = [['arch', 'Arch (current)'], ['leaf', 'Leaf'], ['circle', 'Circle'], ['frame', 'Gold block'], ['window', 'Gold line'], ['tilt', 'Snapshot']];
    var pick = document.createElement('div');
    pick.className = 'b4-shapes';
    pick.setAttribute('role', 'group');
    pick.setAttribute('aria-label', 'Photo shape (review only)');
    pick.innerHTML = '<span class="b4-shapes__label">Photo shape</span>';
    var saved = null;
    try { saved = new URLSearchParams(location.search).get('shape') || localStorage.getItem('b4-shape'); } catch (e) {}
    function apply(name) {
      if (name === 'arch') stage.removeAttribute('data-shape'); else stage.setAttribute('data-shape', name);
      pick.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.value === name)); });
      try { localStorage.setItem('b4-shape', name); } catch (e) {}
    }
    shapes.forEach(function (s) {
      var b = document.createElement('button');
      b.type = 'button'; b.value = s[0]; b.textContent = s[1];
      b.addEventListener('click', function () { apply(s[0]); });
      pick.appendChild(b);
    });
    stage.insertAdjacentElement('afterend', pick);
    apply(shapes.some(function (s) { return s[0] === saved; }) ? saved : 'arch');
  }
})();

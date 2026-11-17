// Concept 2 hero: a slideshow inside the big Fig Leaf.
// Photos slide through the leaf every few seconds; the last word of the
// headline (car, home, boat) changes to match. Arrows, dots, swipe and the arrow keys (when the slideshow has
// focus) move it by hand; pointing at the leaf or the pause button stops
// it. With reduced motion it doesn't advance on its own.
(function () {
  'use strict';
  var show = document.querySelector('.l-show');
  if (!show) return;
  var slides = Array.prototype.slice.call(show.querySelectorAll('.l-slide'));
  var dots = Array.prototype.slice.call(show.querySelectorAll('.l-dot'));
  var words = Array.prototype.slice.call(document.querySelectorAll('.l-rotate__word'));
  var pauseBtn = show.querySelector('.l-pause');
  var n = slides.length;
  if (n < 2) return;

  var STEP_MS = 4500;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var i = 0, timer = null, paused = reduce, hovering = false;

  function go(next) {
    var prev = i;
    i = (next + n) % n;
    slides.forEach(function (s, k) {
      s.style.setProperty('--i', i);
      s.classList.toggle('is-active', k === i);
      s.setAttribute('aria-hidden', k === i ? 'false' : 'true');
    });
    dots.forEach(function (d, k) {
      d.classList.toggle('is-active', k === i);
      if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
    });
    if (prev !== i && words[prev] && words[i]) {
      var old = words[prev];
      old.classList.remove('is-active');
      old.classList.add('is-leaving');
      setTimeout(function () { old.classList.remove('is-leaving'); }, 600);
      words[i].classList.remove('is-leaving');
      words[i].classList.add('is-active');
    }
  }
  function tick() { go(i + 1); }
  function restart() {
    clearInterval(timer); timer = null;
    if (!paused && !hovering) timer = setInterval(tick, STEP_MS);
  }

  show.querySelector('.l-arrow--prev').addEventListener('click', function () { go(i - 1); restart(); });
  show.querySelector('.l-arrow:not(.l-arrow--prev)').addEventListener('click', function () { go(i + 1); restart(); });
  dots.forEach(function (d) {
    d.addEventListener('click', function () { go(+d.dataset.go); restart(); });
  });
  if (pauseBtn) {
    if (reduce) { pauseBtn.setAttribute('aria-pressed', 'true'); pauseBtn.setAttribute('aria-label', 'Play the slideshow'); }
    pauseBtn.addEventListener('click', function () {
      paused = !paused;
      pauseBtn.setAttribute('aria-pressed', paused ? 'true' : 'false');
      pauseBtn.setAttribute('aria-label', paused ? 'Play the slideshow' : 'Pause the slideshow');
      restart();
    });
  }

  var leaf = show.querySelector('.l-leaf');
  leaf.addEventListener('mouseenter', function () { hovering = true; restart(); });
  leaf.addEventListener('mouseleave', function () { hovering = false; restart(); });

  show.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      e.preventDefault();   // keep the page's concept switcher from firing
      e.stopPropagation();
      go(i + (e.key === 'ArrowRight' ? 1 : -1));
      restart();
    }
  });

  // swipe on touch screens
  var x0 = null;
  leaf.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  leaf.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) { go(i + (dx < 0 ? 1 : -1)); restart(); }
    x0 = null;
  });

  // stop stepping while the hero is off screen or the tab is hidden
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { clearInterval(timer); timer = null; } else restart();
  });

  go(0);
  restart();
})();

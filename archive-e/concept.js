// Archive E hero.
// 1. The last word of the headline steps through car, home, boat and
//    business, and the leaf shows the matching photo cut to its shape
//    Pointing at a label jumps to it.
// 2. With a mouse, the leaf turns so its tip points at the cursor wherever
//    it is on the page. Without one, it sways on its own (CSS).
// Reduced motion: no stepping, no following; the car photo stays.
(function () {
  'use strict';
  var media = document.querySelector('.d-hero__media');
  var leaf = document.querySelector('.d-leaf');
  var words = Array.prototype.slice.call(document.querySelectorAll('.d-rotate__word'));
  var tags = Array.prototype.slice.call(document.querySelectorAll('.d-tag[data-key]'));
  if (!media || !leaf || !words.length) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var STEP_MS = 3000, RESUME_MS = 2500;

  // ---- stepping through car, home, boat, business ------------------------
  var i = 0, timer = null, resumeTimer = null;
  function show(key) {
    var next = -1;
    words.forEach(function (w, k) { if (w.dataset.key === key) next = k; });
    if (next < 0) return;
    if (next !== i) {
      var old = words[i];
      old.classList.remove('is-active');
      old.classList.add('is-leaving');
      setTimeout(function () { old.classList.remove('is-leaving'); }, 600);
      words[next].classList.add('is-active');
      i = next;
    }
    fit();
    leaf.dataset.active = key;
    tags.forEach(function (t) { t.classList.toggle('is-active', t.dataset.key === key); });
  }
  // the underline is as long as the word showing (in em, so it scales)
  var slot = words[0].parentNode;
  function fit() {
    var w = words[i], fs = parseFloat(getComputedStyle(w).fontSize);
    if (fs) slot.style.setProperty('--uw', (w.offsetWidth / fs).toFixed(3));
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  function start() {
    if (reduce || timer) return;
    timer = setInterval(function () { show(words[(i + 1) % words.length].dataset.key); }, STEP_MS);
  }
  function stop() { clearInterval(timer); timer = null; }
  show(words[0].dataset.key);
  start();

  tags.forEach(function (t) {
    function enter() { clearTimeout(resumeTimer); stop(); show(t.dataset.key); }
    function leave() { clearTimeout(resumeTimer); resumeTimer = setTimeout(start, RESUME_MS); }
    t.addEventListener('mouseenter', enter);
    t.addEventListener('focus', enter);
    t.addEventListener('mouseleave', leave);
    t.addEventListener('blur', leave);
  });

  // ---- the leaf's tip points at the cursor ---------------------------------
  if (reduce || !fine) return;
  media.classList.add('is-following');
  // Where the tip is at rest, measured from the point the leaf turns
  // around (its centre of mass, the transform-origin in concept.css):
  // down and to the right, 58.35 degrees clockwise from pointing right.
  var PIVOT_X = 0.464, PIVOT_Y = 0.499, TIP_ANGLE = 58.35;
  var target = 0, cur = 0, raf = null;

  function wrap(a) { return ((a + 540) % 360) - 180; }

  window.addEventListener('mousemove', function (e) {
    var r = media.getBoundingClientRect();
    // the leaf box is inset 4% inside the media box
    var px = r.left + r.width * (0.04 + 0.92 * PIVOT_X);
    var py = r.top + r.height * (0.04 + 0.92 * PIVOT_Y);
    var ang = Math.atan2(e.clientY - py, e.clientX - px) * 180 / Math.PI;
    // keep turning the short way round, so it never spins back the long way
    target = cur + wrap(ang - TIP_ANGLE - cur);
    if (!raf) raf = requestAnimationFrame(tick);
  }, { passive: true });

  function tick() {
    raf = null;
    cur += (target - cur) * 0.12;
    leaf.style.setProperty('--turn', cur.toFixed(2) + 'deg');
    if (Math.abs(target - cur) > 0.05) raf = requestAnimationFrame(tick);
  }
})();

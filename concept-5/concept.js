// Concept 5 hero.
// 1. The last word of the headline steps through car, home, boat and
//    business, and the leaf shows the matching photo cut to its shape
//    (business shows the plain leaf). Pointing at a label jumps to it.
// 2. With a mouse, the leaf turns and tilts toward the cursor wherever it
//    is on the page. Without one, it sways on its own (CSS).
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
    leaf.dataset.active = key;
    tags.forEach(function (t) { t.classList.toggle('is-active', t.dataset.key === key); });
  }
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

  // ---- leaf follows the cursor ----------------------------------------------
  if (reduce || !fine) return;
  media.classList.add('is-following');
  var MAX_TURN = 32;   // most the leaf turns, in degrees
  var MAX_TILT = 10;   // most it leans toward the cursor in 3D
  var target = { turn: 0, tx: 0, ty: 0 }, cur = { turn: 0, tx: 0, ty: 0 };
  var raf = null;

  window.addEventListener('mousemove', function (e) {
    var r = media.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    var dx = e.clientX - cx, dy = e.clientY - cy;
    // turn: the leaf's tip points up and to the right at rest; swing it
    // round toward wherever the cursor is, within MAX_TURN either way
    var ang = Math.atan2(dy, dx) * 180 / Math.PI;          // -180..180, 0 = right
    var rel = ang - (-45);                                    // relative to the resting tip
    rel = ((rel + 540) % 360) - 180;
    target.turn = Math.max(-MAX_TURN, Math.min(MAX_TURN, rel * 0.4));
    // tilt: lean toward the cursor, more when it's close to the leaf
    var reach = Math.max(r.width, 1) * 1.5;
    target.ty = Math.max(-1, Math.min(1, dx / reach)) * MAX_TILT;
    target.tx = Math.max(-1, Math.min(1, -dy / reach)) * MAX_TILT;
    if (!raf) raf = requestAnimationFrame(tick);
  }, { passive: true });

  function tick() {
    raf = null;
    cur.turn += (target.turn - cur.turn) * 0.08;
    cur.tx += (target.tx - cur.tx) * 0.08;
    cur.ty += (target.ty - cur.ty) * 0.08;
    leaf.style.setProperty('--turn', cur.turn.toFixed(2) + 'deg');
    leaf.style.setProperty('--tilt-x', cur.tx.toFixed(2) + 'deg');
    leaf.style.setProperty('--tilt-y', cur.ty.toFixed(2) + 'deg');
    if (Math.abs(target.turn - cur.turn) > 0.05 || Math.abs(target.tx - cur.tx) > 0.05 || Math.abs(target.ty - cur.ty) > 0.05) {
      raf = requestAnimationFrame(tick);
    }
  }
})();

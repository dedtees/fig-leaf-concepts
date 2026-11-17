// Hero concepts: one behaviour for all four layouts.
// Hover (mouse), tap or focus the car, home or boat to bring it forward; the
// headline's last words follow along. With nobody interacting it steps through
// them on its own. The layouts differ only in markup and CSS (hero-x.css).
// Concept C also moves a "lens" with the cursor: --lx / --ly on the root.

const AUTO_MS = 3600;   // time on each item while nobody is interacting
const RESUME_MS = 2500; // wait after the pointer leaves before stepping again
const WORD_MS = 480;    // headline words sliding

(function () {
  'use strict';

  const hero = document.querySelector('.hero');
  const root = document.querySelector('[data-hx]');
  if (!hero || !root) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const EASE = 'cubic-bezier(0.65, 0, 0.35, 1)';
  const EASE_OUT = 'cubic-bezier(0.22, 1, 0.36, 1)';

  const items = Array.prototype.map.call(root.querySelectorAll('.hx__item'), function (el) {
    const key = el.dataset.scene;
    return {
      key: key,
      el: el,
      hit: el.querySelector('.hx__hit'),
      word: hero.querySelector('.scene-word[data-scene="' + key + '"]'),
      // where the lens sits for this item (concept C), in % of the root
      lx: parseFloat(el.dataset.lx || '50'),
      ly: parseFloat(el.dataset.ly || '50')
    };
  });
  if (!items.length) return;
  const dots = Array.prototype.slice.call(root.querySelectorAll('.hx__dot'));

  let active = -1;
  let wordShown = 0;
  let autoTimer = 0, resumeTimer = 0;
  let interacting = false, onScreen = true;

  function setActive(i) {
    if (i === active) return;
    active = i;
    items.forEach(function (it, n) {
      it.el.classList.toggle('is-active', n === i);
      if (it.hit) it.hit.setAttribute('aria-pressed', String(n === i));
    });
    dots.forEach(function (d, n) { d.classList.toggle('is-active', n === i); });
    root.dataset.active = items[i].key;
    root.style.setProperty('--i', i);
    if (!root.classList.contains('is-tracking')) {
      root.style.setProperty('--lx', items[i].lx + '%');
      root.style.setProperty('--ly', items[i].ly + '%');
    }
    // restart the progress line on the active item
    root.classList.remove('is-ticking');
    void root.offsetWidth;
    if (!interacting && !reduceMotion.matches) root.classList.add('is-ticking');
    swapWords(i);
  }

  function swapWords(i) {
    if (i === wordShown) return;
    const out = items[wordShown].word;
    const inn = items[i].word;
    wordShown = i;
    if (!out || !inn) return;
    out.getAnimations().forEach(function (a) { a.cancel(); });
    inn.getAnimations().forEach(function (a) { a.cancel(); });
    if (reduceMotion.matches) {
      out.classList.remove('is-active');
      inn.classList.add('is-active');
      return;
    }
    out.animate([{ transform: 'translateY(0)' }, { transform: 'translateY(-135%)' }],
      { duration: WORD_MS * 0.8, easing: EASE, fill: 'forwards' })
      .finished.then(function () {
        if (items[wordShown].word !== out) {
          out.classList.remove('is-active');
          out.getAnimations().forEach(function (a) { a.cancel(); });
        }
      }, function () {});
    inn.classList.add('is-active');
    inn.animate([{ transform: 'translateY(135%)' }, { transform: 'translateY(0)' }],
      { duration: WORD_MS, delay: WORD_MS * 0.3, easing: EASE_OUT, fill: 'both' })
      .finished.then(function () {
        inn.getAnimations().forEach(function (a) { a.cancel(); });
      }, function () {});
  }

  // ---- Stepping on its own while idle -----------------------------------
  function stopAuto() {
    clearTimeout(autoTimer); clearTimeout(resumeTimer);
    autoTimer = resumeTimer = 0;
    root.classList.remove('is-ticking');
  }
  function step() {
    autoTimer = 0;
    if (!interacting && onScreen && !document.hidden) setActive((active + 1) % items.length);
    autoTimer = setTimeout(step, AUTO_MS);
  }
  function startAuto(delay) {
    if (reduceMotion.matches) return;
    stopAuto();
    resumeTimer = setTimeout(function () {
      resumeTimer = 0;
      interacting = false;
      step();
    }, delay);
  }
  function take(n) {
    interacting = true;
    stopAuto();
    setActive(n);
  }

  // ---- Mouse: hovering an item brings it forward --------------------------
  items.forEach(function (it, n) {
    it.el.addEventListener('pointerenter', function (e) {
      if (e.pointerType === 'mouse' || e.pointerType === 'pen') take(n);
    });
    if (it.hit) {
      it.hit.addEventListener('click', function () { take(n); });
      it.hit.addEventListener('focus', function () { take(n); });
    }
  });
  dots.forEach(function (d, n) { d.addEventListener('click', function () { take(n); }); });

  // Concept C: the lens follows the cursor and lights the item under it
  if (root.hasAttribute('data-lens')) {
    root.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;
      const r = root.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width * 100;
      const py = (e.clientY - r.top) / r.height * 100;
      root.classList.add('is-tracking');
      root.style.setProperty('--lx', px + '%');
      root.style.setProperty('--ly', py + '%');
      let best = 0, bestD = Infinity;
      items.forEach(function (it, n) {
        const d = Math.abs(px - it.lx);
        if (d < bestD) { bestD = d; best = n; }
      });
      take(best);
    });
  }

  root.addEventListener('pointerleave', function () {
    if (root.classList.contains('is-tracking') && active >= 0) {
      root.classList.remove('is-tracking');
      root.style.setProperty('--lx', items[active].lx + '%');
      root.style.setProperty('--ly', items[active].ly + '%');
    }
    startAuto(RESUME_MS);
  });
  root.addEventListener('focusout', function (e) {
    if (!root.contains(e.relatedTarget)) startAuto(RESUME_MS);
  });
  document.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'touch' && !root.contains(e.target) && interacting) startAuto(RESUME_MS);
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) { onScreen = entries[0].isIntersecting; }).observe(hero);
  }

  root.style.setProperty('--auto-ms', AUTO_MS + 'ms');
  setActive(0);
  if (!reduceMotion.matches) {
    root.classList.add('is-ticking');
    autoTimer = setTimeout(step, AUTO_MS);
  }
})();

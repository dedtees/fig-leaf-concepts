// Interactive scene: move over the car, house or boat in the picture (or tap
// a dot) to light it up. The headline's last words and the card underneath
// follow along. With no one interacting, it steps through them on its own.
// On mouse devices the picture also tilts a touch toward the cursor.

const AUTO_MS = 3200;    // time on each spot while nobody is interacting
const RESUME_MS = 2500;  // wait after the pointer leaves before stepping again
const TILT_DEG = 5;      // most the picture tilts, in degrees
const WORD_MS = 480;     // headline words sliding

(function () {
  'use strict';

  const hero = document.querySelector('.hero--scene');
  if (!hero) return;

  const scene = hero.querySelector('.scene');
  const tilt = scene.querySelector('.scene__tilt');
  const spots = Array.prototype.slice.call(scene.querySelectorAll('.hotspot'));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const EASE = 'cubic-bezier(0.65, 0, 0.35, 1)';
  const EASE_OUT = 'cubic-bezier(0.22, 1, 0.36, 1)';

  const items = spots.map(function (btn) {
    const key = btn.dataset.scene;
    return {
      key: key,
      btn: btn,
      card: scene.querySelector('.scene__card[data-scene="' + key + '"]'),
      word: hero.querySelector('.scene-word[data-scene="' + key + '"]'),
      x: parseFloat(btn.style.getPropertyValue('--x')),
      y: parseFloat(btn.style.getPropertyValue('--y'))
    };
  });
  if (!items.length) return;

  items.forEach(function (it) { if (it.card) it.card.hidden = false; });

  let active = -1;
  let wordShown = 0; // the headline starts on the first spot's words
  let autoTimer = 0;
  let resumeTimer = 0;
  let interacting = false;
  let onScreen = true;

  // ---- Focus a spot ------------------------------------------------------

  function setActive(i) {
    if (i === active) return;
    active = i;
    items.forEach(function (it, n) {
      it.btn.setAttribute('aria-pressed', String(n === i));
      if (it.card) it.card.classList.toggle('is-shown', n === i);
    });
    scene.classList.toggle('has-focus', i >= 0);
    if (i >= 0) {
      scene.style.setProperty('--sx', items[i].x + '%');
      scene.style.setProperty('--sy', items[i].y + '%');
      swapWords(i);
    }
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

  // ---- Stepping on its own while idle ------------------------------------

  function stopAuto() {
    clearTimeout(autoTimer);
    clearTimeout(resumeTimer);
    autoTimer = resumeTimer = 0;
  }

  function step() {
    autoTimer = 0;
    if (!interacting && onScreen && !document.hidden) {
      setActive((active + 1) % items.length);
    }
    autoTimer = setTimeout(step, AUTO_MS);
  }

  function startAuto(delay) {
    if (reduceMotion.matches) return; // stays where the visitor left it
    stopAuto();
    resumeTimer = setTimeout(function () {
      resumeTimer = 0;
      interacting = false;
      step();
    }, delay);
  }

  // ---- Pointer over the picture: pick the nearest spot, tilt, sheen ------

  let rx = 0, ry = 0, trx = 0, try_ = 0, rafId = 0;

  function tick() {
    rafId = 0;
    rx += (trx - rx) * 0.12;
    ry += (try_ - ry) * 0.12;
    if (Math.abs(trx - rx) < 0.01 && Math.abs(try_ - ry) < 0.01) { rx = trx; ry = try_; }
    tilt.style.transform = (rx || ry) ? 'rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)' : '';
    if (rx !== trx || ry !== try_) rafId = requestAnimationFrame(tick);
  }
  function kick() { if (!rafId) rafId = requestAnimationFrame(tick); }

  function nearest(px, py) {
    // only the band where the car, house and boat sit counts
    if (py < 18 || py > 78) return -1;
    let best = -1, bestD = Infinity;
    items.forEach(function (it, n) {
      const d = Math.abs(px - it.x);
      if (d < bestD) { bestD = d; best = n; }
    });
    return bestD < 12 ? best : -1;
  }

  scene.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;
    const r = scene.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width * 100;
    const py = (e.clientY - r.top) / r.height * 100;
    scene.style.setProperty('--mx', px + '%');
    scene.style.setProperty('--my', py + '%');
    scene.classList.add('is-hovered');

    if (!e.target.closest('.scene__card')) {
      const n = nearest(px, py);
      if (n >= 0) {
        interacting = true;
        stopAuto();
        setActive(n);
      }
    }

    if (finePointer.matches && !reduceMotion.matches) {
      try_ = (px / 100 - 0.5) * 2 * TILT_DEG;
      trx = -(py / 100 - 0.5) * 2 * TILT_DEG * 0.6;
      kick();
    }
  });

  scene.addEventListener('pointerleave', function () {
    scene.classList.remove('is-hovered');
    trx = try_ = 0;
    kick();
    startAuto(RESUME_MS);
  });

  // Dots: tap, click or keyboard
  items.forEach(function (it, n) {
    it.btn.addEventListener('click', function () {
      interacting = true;
      stopAuto();
      setActive(n);
      if (it.card) {
        const link = it.card.querySelector('a');
        // keyboard users go straight to the card's link
        if (link && it.btn.matches(':focus-visible')) link.focus({ preventScroll: true });
      }
    });
    it.btn.addEventListener('focus', function () {
      interacting = true;
      stopAuto();
      setActive(n);
    });
  });

  scene.addEventListener('focusout', function (e) {
    if (!scene.contains(e.relatedTarget)) startAuto(RESUME_MS);
  });

  // Touch: a tap anywhere outside the picture lets it step on its own again
  document.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'touch' && !scene.contains(e.target) && interacting) startAuto(RESUME_MS);
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      onScreen = entries[0].isIntersecting;
    }).observe(hero);
  }

  // Start on the first spot, then step through the rest
  setActive(0);
  if (!reduceMotion.matches) autoTimer = setTimeout(step, AUTO_MS);
})();

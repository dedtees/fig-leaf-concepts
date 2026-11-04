// Fig leaf gallery: selecting a photo opens it full size. In the viewer the
// arrow buttons, the keyboard's left and right arrows, or a swipe step
// through the photos; Esc, the close button or a click outside closes it.

(function () {
  'use strict';

  const viewer = document.querySelector('.viewer');
  const buttons = Array.prototype.slice.call(document.querySelectorAll('.gallery__open'));
  if (!viewer || !buttons.length || typeof viewer.showModal !== 'function') return;

  const img = viewer.querySelector('.viewer__img');
  const count = viewer.querySelector('.viewer__count');
  const title = viewer.querySelector('.viewer__title');
  const meta = viewer.querySelector('.viewer__meta');

  const photos = buttons.map(function (btn) {
    const fig = btn.closest('.gallery__figure');
    const thumb = btn.querySelector('img');
    return {
      btn: btn,
      src: thumb.dataset.full,
      thumb: thumb.getAttribute('src'),
      alt: thumb.alt,
      title: fig.querySelector('.gallery__title').textContent,
      meta: fig.querySelector('.gallery__meta').textContent,
      studio: !!btn.closest('.gallery__item--studio')
    };
  });
  let current = 0;

  function show(i) {
    current = (i + photos.length) % photos.length;
    const p = photos[current];
    // if the full-size file isn't uploaded, show the thumbnail instead
    img.onerror = function () { img.onerror = null; img.src = p.thumb; };
    img.src = p.src;
    img.alt = p.alt;
    img.classList.toggle('is-studio', p.studio);
    count.textContent = (current + 1) + ' / ' + photos.length;
    title.textContent = p.title;
    meta.textContent = p.meta;
    // load the neighbours so stepping is instant
    [current + 1, current - 1].forEach(function (n) {
      new Image().src = photos[(n + photos.length) % photos.length].src;
    });
  }

  buttons.forEach(function (btn, i) {
    btn.addEventListener('click', function () {
      show(i);
      viewer.showModal();
    });
  });

  viewer.querySelector('.viewer__close').addEventListener('click', function () { viewer.close(); });
  viewer.querySelector('.viewer__prev').addEventListener('click', function () { show(current - 1); });
  viewer.querySelector('.viewer__next').addEventListener('click', function () { show(current + 1); });

  // click on the dark area around the photo closes
  let swiped = false;
  viewer.addEventListener('click', function (e) {
    if (swiped) { swiped = false; return; }
    if (e.target === viewer || e.target.classList.contains('viewer__frame')) viewer.close();
  });

  // arrows step photos while the viewer is open (and not the page's concepts)
  document.addEventListener('keydown', function (e) {
    if (!viewer.open) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1); }
  }, true);

  // swipe on touch screens
  let startX = null;
  viewer.addEventListener('pointerdown', function (e) { if (e.pointerType === 'touch') startX = e.clientX; });
  viewer.addEventListener('pointerup', function (e) {
    if (startX === null) return;
    const dx = e.clientX - startX;
    startX = null;
    if (Math.abs(dx) > 50) {
      swiped = true;
      show(current + (dx < 0 ? 1 : -1));
    }
  });

  // back to the photo that was opened
  viewer.addEventListener('close', function () {
    photos[current].btn.focus({ preventScroll: true });
  });
})();

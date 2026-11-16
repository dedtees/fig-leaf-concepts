// Concept 6 hero: the photo drifts a touch slower than the page as you
// scroll, so the leaf seems to sit behind the black panel.
(function () {
  'use strict';
  var photo = document.querySelector('.f-hero__photo');
  if (!photo || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var ticking = false;
  function update() {
    ticking = false;
    var y = Math.min(window.scrollY, window.innerHeight);
    photo.style.transform = 'translate3d(0,' + (y * 0.25).toFixed(1) + 'px,0) scale(1.06)';
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
  update();
})();

// Concept 11: the About picture starts on the agency's old building (the
// painting, with its sign now reading Fig Leaf) and fades to the team photo,
// then keeps taking turns while the section is on screen.
(function () {
  'use strict';
  var media = document.querySelector('.c11-fade');
  if (!media) return;
  var FIRST_MS = 2200;  // the building shows this long before the team fades in
  var EACH_MS = 5000;   // then each picture shows this long
  var timer = 0, started = false;

  function flip() {
    media.classList.toggle('is-team');
    timer = setTimeout(flip, EACH_MS);
  }
  function start() { if (!timer) timer = setTimeout(flip, started ? EACH_MS : FIRST_MS); started = true; }
  function stop() { clearTimeout(timer); timer = 0; }

  if (!('IntersectionObserver' in window)) { start(); return; }
  new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) start(); else stop(); });
  }, { threshold: 0.4 }).observe(media);
})();

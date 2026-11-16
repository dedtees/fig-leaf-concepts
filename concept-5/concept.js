// Concept 5 hero: the last word of the headline steps through car, home,
// boat and business. Stays on "car." when reduced motion is asked for.
(function () {
  'use strict';
  var words = document.querySelectorAll('.d-rotate__word');
  if (words.length < 2) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var i = 0;
  setInterval(function () {
    words[i].classList.remove('is-active');
    words[i].classList.add('is-leaving');
    var old = words[i];
    setTimeout(function () { old.classList.remove('is-leaving'); }, 600);
    i = (i + 1) % words.length;
    words[i].classList.add('is-active');
  }, 2600);
})();

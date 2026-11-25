/* Carriers page: the All / Auto / Homeowners / Surplus buttons, and the
   carrier's name in place of a logo that doesn't load. */
(function () {
  var cards = document.querySelectorAll('.cr-card');
  var buttons = document.querySelectorAll('[data-cr-filter]');
  var status = document.querySelector('[data-cr-status]');
  function show(key) {
    var n = 0;
    for (var i = 0; i < cards.length; i++) {
      var on = key === 'all' || (' ' + cards[i].getAttribute('data-cr-lines') + ' ').indexOf(' ' + key + ' ') > -1;
      cards[i].hidden = !on;
      if (on) { cards[i].classList.add('is-in'); n++; }
    }
    for (var j = 0; j < buttons.length; j++)
      buttons[j].setAttribute('aria-pressed', String(buttons[j].getAttribute('data-cr-filter') === key));
    if (status) status.textContent = 'Showing ' + n + ' carriers';
  }
  for (var b = 0; b < buttons.length; b++)
    buttons[b].addEventListener('click', function () { show(this.getAttribute('data-cr-filter')); });

  var logos = document.querySelectorAll('img[data-cr-logo]');
  function missing(img) { img.parentNode.classList.add('is-missing'); }
  for (var k = 0; k < logos.length; k++) {
    var img = logos[k];
    if (img.complete && img.naturalWidth === 0) missing(img);
    else img.addEventListener('error', missing.bind(null, img), { once: true });
  }
})();

/* Header menus with a dropdown (Personal Insurance, Business Insurance) are
   labels, not links (Eric, 25 Nov): pointing at one or tabbing to its arrow
   opens the dropdown (main.js and the CSS), and a click or tap on the label
   does what the arrow does. About stays a link to the About page. */
(function () {
  document.querySelectorAll('[data-menu-label]').forEach(function (label) {
    var toggle = label.parentNode.querySelector('.site-nav__sub-toggle');
    if (!toggle) return;
    label.addEventListener('click', function (e) {
      e.preventDefault();
      toggle.click();
    });
  });
})();

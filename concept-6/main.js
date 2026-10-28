// Homepage behavior: mobile menu, language selector, quote starter.
// The animated fig leaf and its changing headline live in anim.js.

// CRQ quote system. Still to be supplied by the agency (brief, open item 1).
// Once it's set, the quote starter opens it in a new tab with the chosen
// coverage and address as URL parameters (confirm the parameter names too).
const CRQ_URL = '';

(function () {
  'use strict';

  // ---- Footer year --------------------------------------------------------
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // ---- Mobile menu --------------------------------------------------------
  const menuButton = document.querySelector('.site-header__menu');
  const nav = document.getElementById('site-nav');

  function setMenu(open) {
    menuButton.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  }

  if (menuButton && nav) {
    menuButton.addEventListener('click', function () {
      setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setMenu(false);
        menuButton.focus();
      }
    });
  }

  // ---- Language selector (Google Translate loads only when opened) --------
  const translateToggle = document.querySelector('.translate__toggle');
  const translatePanel = document.getElementById('translate-panel');
  let translateLoaded = false;

  window.figleafTranslateInit = function () {
    /* global google */
    new google.translate.TranslateElement(
      { pageLanguage: 'en', layout: google.translate.TranslateElement.InlineLayout.SIMPLE },
      'google_translate_element'
    );
  };

  function setTranslate(open) {
    translateToggle.setAttribute('aria-expanded', String(open));
    translatePanel.hidden = !open;
    if (open && !translateLoaded) {
      translateLoaded = true;
      const s = document.createElement('script');
      s.src = 'https://translate.google.com/translate_a/element.js?cb=figleafTranslateInit';
      s.async = true;
      s.onerror = function () {
        translatePanel.querySelector('.translate__loading').textContent =
          'Translation is unavailable right now.';
      };
      document.head.appendChild(s);
    }
  }

  if (translateToggle && translatePanel) {
    translateToggle.addEventListener('click', function () {
      setTranslate(translateToggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('click', function (e) {
      if (!translatePanel.hidden && !e.target.closest('.translate')) setTranslate(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !translatePanel.hidden) {
        setTranslate(false);
        translateToggle.focus();
      }
    });
  }

  // ---- Quote starter ------------------------------------------------------
  const form = document.getElementById('quote-form');
  if (form) {
    const address = form.querySelector('#quote-address');
    const error = form.querySelector('#quote-address-error');
    const status = form.querySelector('#quote-status');

    function showError(show) {
      error.hidden = !show;
      if (show) address.setAttribute('aria-invalid', 'true');
      else address.removeAttribute('aria-invalid');
    }

    address.addEventListener('input', function () {
      if (address.value.trim()) showError(false);
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      status.hidden = true;

      if (!address.value.trim()) {
        showError(true);
        address.focus();
        return;
      }
      showError(false);

      const coverage = form.querySelector('input[name="coverage"]:checked').value;

      if (!CRQ_URL) {
        status.textContent =
          'Online quotes are almost ready. For now, call us at 877-9-THE-FIG and we’ll get your ' +
          coverage + ' quote started.';
        status.hidden = false;
        return;
      }

      const url = new URL(CRQ_URL);
      url.searchParams.set('coverage', coverage);
      url.searchParams.set('address', address.value.trim());
      window.open(url.toString(), '_blank', 'noopener');
    });
  }

})();

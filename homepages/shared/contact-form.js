/* Contact form on the insurance pages the Consumer Rate Quotes form doesn't
   cover (Boat and Personal Umbrella), in place of that form. Markup:
   contact_form() in homepages/service_pages.py.

   TO MAKE IT SEND ON ITS OWN
   The site is static, so there is nothing on the server to receive the form
   yet. Set data-endpoint on the <form> (in contact_form(), then re-run
   homepages/build.py) to the URL of anything that accepts a POST of the
   form's fields and answers 2xx, for example:
     - a form service: Formspree, Basin, Getform or Web3Forms (sign up with
       quotes@figleafagency.com, paste the URL it gives you), or
     - a small Vercel function (api/contact.js) that emails the agency
       through Resend, SendGrid or similar.
   Fields sent: name, email, phone, insurance_type, message, page (the page's
   address) and company_website (a hidden spam trap; drop anything that has
   it filled in).

   UNTIL THEN (data-endpoint empty), or if the endpoint fails, the form opens
   the visitor's email app with the request filled in, addressed to
   data-mailto, so a request is never lost. */
(function () {
  'use strict';

  function field(form, name) {
    var el = form.elements[name];
    return el ? String(el.value || '').trim() : '';
  }

  function say(form, text, kind) {
    var status = form.querySelector('.pg-contact__status');
    if (!status) return;
    status.textContent = text;
    status.className = 'pg-contact__status' + (kind ? ' is-' + kind : '');
  }

  function email(form) {
    var type = field(form, 'insurance_type') || 'Insurance';
    var body = [
      'Name: ' + field(form, 'name'),
      'Email: ' + field(form, 'email'),
      'Phone: ' + field(form, 'phone'),
      'Insurance type: ' + type,
      '',
      field(form, 'message') || '(no message)',
      '',
      'Sent from ' + location.href
    ].join('\n');
    location.href = 'mailto:' + (form.getAttribute('data-mailto') || 'quotes@figleafagency.com') +
      '?subject=' + encodeURIComponent(type + ' quote request: ' + field(form, 'name')) +
      '&body=' + encodeURIComponent(body);
    say(form, 'Your email app should open with your request ready to send. If it doesn’t, email ' +
      (form.getAttribute('data-mailto') || 'quotes@figleafagency.com') + ' or call (908) 862-3447.', 'ok');
  }

  function done(form) {
    var keep = field(form, 'insurance_type');
    form.reset();
    if (form.elements.insurance_type) form.elements.insurance_type.value = keep;
    form.classList.add('is-sent');
    say(form, 'Thanks! Your request is on its way, and an agent will be in touch soon.', 'ok');
  }

  function submit(e) {
    var form = e.currentTarget;
    e.preventDefault();
    form.classList.add('was-checked');
    if (!form.checkValidity()) {
      say(form, 'Please fill in your name, email and phone so we can reach you.', 'error');
      var bad = form.querySelector(':invalid');
      if (bad) bad.focus();
      return;
    }
    if (field(form, 'company_website')) { done(form); return; }   // spam trap

    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint || !window.fetch || !window.FormData) { email(form); return; }

    var data = new FormData(form);
    data.append('page', location.href);
    var button = form.querySelector('[type="submit"]');
    if (button) button.disabled = true;
    say(form, 'Sending…');
    fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); done(form); })
      .catch(function () { email(form); })
      .then(function () { if (button) button.disabled = false; });
  }

  var forms = document.querySelectorAll('[data-contact-form]');
  for (var i = 0; i < forms.length; i++) forms[i].addEventListener('submit', submit);
})();

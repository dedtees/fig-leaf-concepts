/* The "Still needed from the agency" checklist on the gallery (AC), made by
   outstanding_items() in homepages/build.py. Ticks are kept in this browser
   (localStorage), so they stay after a reload. Items marked done in
   build.py are ticked for everyone and can't be unticked here. */
(function () {
  'use strict';
  var list = document.querySelector('[data-todo-list]');
  if (!list) return;
  var KEY = 'flOutstandingTicks';
  var items = [].slice.call(list.querySelectorAll('[data-todo]'));
  var got = list.querySelector('[data-todo-got]'), left = list.querySelector('[data-todo-left]');
  var bar = list.querySelector('.todo__bar'), reset = list.querySelector('[data-todo-reset]');

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(t) { try { localStorage.setItem(KEY, JSON.stringify(t)); } catch (e) {} }

  var ticks = load();
  function paint() {
    var n = 0, mine = 0;
    items.forEach(function (li) {
      var box = li.querySelector('.todo__check');
      if (!li.hasAttribute('data-fixed')) box.checked = !!ticks[li.getAttribute('data-todo')];
      if (box.checked) n++;
      if (box.checked && !li.hasAttribute('data-fixed')) mine++;
      li.classList.toggle('is-done', box.checked);
    });
    got.textContent = n;
    left.textContent = items.length - n;
    bar.setAttribute('aria-valuenow', n);
    bar.firstElementChild.style.width = (100 * n / items.length) + '%';
    reset.hidden = mine === 0;
  }
  items.forEach(function (li) {
    var box = li.querySelector('.todo__check');
    box.addEventListener('change', function () {
      var k = li.getAttribute('data-todo');
      if (box.checked) ticks[k] = new Date().toISOString(); else delete ticks[k];
      save(ticks); paint();
    });
  });
  reset.addEventListener('click', function () { ticks = {}; save(ticks); paint(); });
  paint();
})();

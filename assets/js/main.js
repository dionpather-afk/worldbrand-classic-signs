/* Worldbrand Classic Signs — site behaviour (no tracking, no data stored) */
(function () {
  'use strict';
  var WA_NUMBER = '27814002417';

  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Gallery filter
  var filterBtns = document.querySelectorAll('.filters button');
  var figures = Array.prototype.slice.call(document.querySelectorAll('.gallery figure'));
  filterBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      filterBtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      figures.forEach(function (fig) {
        var cats = (fig.getAttribute('data-cat') || '').split(' ');
        fig.classList.toggle('hide', f !== 'all' && cats.indexOf(f) === -1);
      });
    });
  });

  // Lightbox
  var lb = document.querySelector('.lightbox');
  if (lb && figures.length) {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('p'), idx = 0;
    var visible = function () { return figures.filter(function (f) { return !f.classList.contains('hide'); }); };
    var show = function (i) {
      var list = visible(); if (!list.length) return;
      idx = (i + list.length) % list.length;
      var img = list[idx].querySelector('img');
      lbImg.src = img.getAttribute('src'); lbImg.alt = img.alt;
      lbCap.textContent = list[idx].querySelector('figcaption') ? list[idx].querySelector('figcaption').textContent : '';
      lb.classList.add('open'); document.body.style.overflow = 'hidden';
    };
    var close = function () { lb.classList.remove('open'); document.body.style.overflow = ''; };
    figures.forEach(function (fig) {
      fig.setAttribute('tabindex', '0');
      var open = function () { show(visible().indexOf(fig)); };
      fig.addEventListener('click', open);
      fig.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  // Forms -> pre-filled WhatsApp message (nothing is stored on this website)
  function val(form, name) {
    var el = form.elements[name];
    if (!el) return '';
    if (el.length && el[0] && el[0].type === 'radio') {
      for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value;
      return '';
    }
    return (el.value || '').trim();
  }
  document.querySelectorAll('form[data-wa]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (el) {
        var bad = el.type === 'checkbox' ? !el.checked : !el.value.trim();
        if (el.type === 'email' && el.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value)) bad = true;
        el.classList.toggle('err', bad);
        if (bad) ok = false;
      });
      if (!ok) {
        var first = form.querySelector('.err'); if (first) first.focus();
        return;
      }
      var lines = [form.getAttribute('data-wa')];
      form.querySelectorAll('[data-label]').forEach(function (el) {
        var v = val(form, el.getAttribute('name'));
        if (v) lines.push('*' + el.getAttribute('data-label') + ':* ' + v);
      });
      var url = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
      var msg = form.querySelector('.form-msg');
      if (msg) msg.classList.add('show');
      window.open(url, '_blank', 'noopener');
    });
  });
})();

// Pre-select service on quote page from ?service=slug
(function () {
  var sel = document.getElementById('q-service');
  if (!sel) return;
  var m = /[?&]service=([a-z0-9-]+)/.exec(location.search);
  if (!m) return;
  for (var i = 0; i < sel.options.length; i++) {
    if (sel.options[i].getAttribute('data-slug') === m[1]) { sel.selectedIndex = i; break; }
  }
})();

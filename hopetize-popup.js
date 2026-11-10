/* Hopetize: Twingle-Spendenformular im Spenden-Pop-up der Webflow-Seite.
   Fuellt das Element mit data-twingle-slot (in .donate_modal) mit Kopfzeile + Twingle-iframe.
   Einbinden: <script src="https://cdn.jsdelivr.net/gh/dxnielhrf/hopetize-twingle-style@vX/hopetize-popup.js" defer></script> */
(function () {
  'use strict';
  var FORM = 'https://spenden.twingle.de/hopetize-kinderkrebshilfe-e-v/weihnachtsaktion-2026/tw6af34c1b4d503/form';
  var CSS = '' +
    '.donate_form[data-twingle-slot]{padding:2em 1.5em 1em}' +
    '.donate_form[data-twingle-slot] .tw-head{display:flex;flex-direction:column;align-items:flex-start;gap:.25em;padding:0 3.5em 0 .5em}' +
    '.donate_form[data-twingle-slot] .tw-sub{font-size:.875em;color:#6B6175}' +
    '.donate_form[data-twingle-slot] .tw-frame{display:block;width:100%;min-height:640px;border:0;margin-top:.75em}' +
    '@media (max-width:767px){.donate_form[data-twingle-slot]{padding:1.5em .5em .5em}}';

  function init() {
    var slot = document.querySelector('[data-twingle-slot]');
    if (!slot || slot.querySelector('.tw-frame')) return;

    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    slot.innerHTML = '<div class="donate_form-head tw-head"><div class="donate_form-title">Deine Spende</div>' +
      '<div class="tw-sub">einmalig · sicher über Twingle</div></div>' +
      '<iframe class="tw-frame" title="Spendenformular Weihnachtsaktion 2026" allow="payment"></iframe>';
    var frame = slot.querySelector('.tw-frame');

    // Twingle meldet seine Hoehe; +40px Puffer, damit im iframe nichts scrollt (iOS-Scrollhaenger)
    window.addEventListener('message', function (e) {
      if (e.source !== frame.contentWindow) return;
      var d = e.data; if (d && d.type === 'size' && +d.value > 0) frame.style.height = (Math.ceil(+d.value) + 40) + 'px';
    });

    // Formular vorladen, wenn die Seite fertig ist (Pop-up ist dann sofort bereit)
    var load = function () { if (!frame.getAttribute('src')) frame.src = FORM + '?tw_amount=40'; };
    if (document.readyState === 'complete') setTimeout(load, 300); else window.addEventListener('load', function () { setTimeout(load, 300); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

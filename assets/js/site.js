// OBTS website: mobile menu, remembered language, and the registration form
// (the form stores nothing: it opens WhatsApp with the message filled in).
(function () {
  var button = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (button && nav) {
    button.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
        button.focus();
      }
    });
  }

  // Remember the language the visitor chose (a convenience only).
  document.querySelectorAll('.lang a').forEach(function (link) {
    link.addEventListener('click', function () {
      try { localStorage.setItem('obts-lang', link.getAttribute('hreflang')); } catch (e) { /* storage blocked */ }
    });
  });


  // Persistent OBTS AI help button: open the school's WhatsApp assistant
  // with the current page context so learners can ask about a course or lesson.
  var pageLanguage = (document.documentElement.lang || 'sw').toLowerCase().split('-')[0];
  var pageHeading = document.querySelector('main h1');
  var pageTitle = ((pageHeading && pageHeading.textContent) || document.title || 'OBTS').trim().slice(0, 120);
  var aiMessages = {
    sw: 'Nahitaji msaada wa AI kuhusu somo au usajili wa OBTS. Ukurasa nilipo: ' + pageTitle + ' (' + window.location.href + '). Nifafanulie hatua kwa hatua; usinipatie majibu ya tathmini.',
    en: 'I need OBTS AI help with a lesson or registration. Page: ' + pageTitle + ' (' + window.location.href + '). Please explain step by step and do not give me assessment answers.',
    fr: 'J’ai besoin de l’aide IA de l’OBTS pour une leçon ou l’inscription. Page : ' + pageTitle + ' (' + window.location.href + '). Expliquez étape par étape sans donner les réponses aux évaluations.'
  };
  var aiLabels = { sw: 'Uliza AI', en: 'Ask AI', fr: 'Demander à l’IA' };
  var aiHelpLink = document.createElement('a');
  aiHelpLink.className = 'ai-float';
  aiHelpLink.href = 'https://wa.me/255704686885?text=' + encodeURIComponent(aiMessages[pageLanguage] || aiMessages.sw);
  aiHelpLink.textContent = aiLabels[pageLanguage] || aiLabels.sw;
  aiHelpLink.setAttribute('aria-label', aiLabels[pageLanguage] || aiLabels.sw);
  aiHelpLink.target = '_blank';
  aiHelpLink.rel = 'noopener';
  document.body.appendChild(aiHelpLink);

  var form = document.getElementById('registration');
  if (!form) return;
  var t = JSON.parse(form.getAttribute('data-text'));
  var prepared = document.getElementById('registration-prepared');
  var continueLink = document.getElementById('registration-continue');
  // A changed form must never leave a previous student's message ready to open.
  function clearPrepared() {
    if (prepared) prepared.hidden = true;
    if (continueLink) continueLink.removeAttribute('href');
    form.removeAttribute('data-last-url');
  }
  form.addEventListener('input', clearPrepared);
  form.addEventListener('change', clearPrepared);
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    clearPrepared();
    var error = form.querySelector('.error');
    form.querySelectorAll('[aria-invalid]').forEach(function (field) { field.removeAttribute('aria-invalid'); });
    var get = function (name) { var el = form.elements[name]; return el ? el.value.trim() : ''; };
    var courses = Array.prototype.slice.call(form.querySelectorAll('input[name=course]:checked:not(:disabled)'))
      .map(function (box) { return box.value; });
    var missing = [];
    var firstInvalid;
    function invalid(name, label) {
      missing.push(label);
      var field = form.elements[name];
      if (field && field.setAttribute) {
        field.setAttribute('aria-invalid', 'true');
        if (!firstInvalid) firstInvalid = field;
      }
    }
    if (!get('name')) invalid('name', t.name);
    // Count digits, not spaces; accept common pasted phone formatting.
    // International country code is required, as shown next to this field.
    var phone = get('phone').replace(/[\s().-]/g, '');
    if (!/^\+?[1-9][0-9]{7,14}$/.test(phone)) invalid('phone', t.phone);
    if (!get('place')) invalid('place', t.place);
    if (!courses.length) missing.push(t.courses);
    if (!form.elements.consent.checked) invalid('consent', t.consent);
    if (missing.length) {
      error.textContent = t.missing + ' ' + missing.join(', ');
      if (firstInvalid) firstInvalid.focus();
      return;
    }
    error.textContent = '';
    var lines = [t.intro, t.name + ': ' + get('name'), t.phone + ': ' + get('phone'), t.place + ': ' + get('place'),
      t.language + ': ' + get('language'), t.courses + ': ' + courses.join('; ')];
    if (get('message')) lines.push(t.message + ': ' + get('message'));
    var url = 'https://wa.me/' + form.getAttribute('data-wa') + '?text=' + encodeURIComponent(lines.join('\n'));
    form.setAttribute('data-last-url', url);
    // Always keep a visible continuation link: some phone browsers block popups.
    if (continueLink && prepared) {
      continueLink.href = url;
      prepared.hidden = false;
    }
    window.open(url, '_blank', 'noopener');
  });
})();

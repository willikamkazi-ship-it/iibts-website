// The personal link stays in memory: never save it to browser storage or logs.
(function (root) {
  function campusUrl(value, origin, target, language) {
    var url;
    try { url = new URL(value.trim()); } catch (_) { return null; }
    if (url.protocol !== 'https:' || url.origin !== origin || url.username || url.password ||
        url.pathname !== '/dashboard' || url.hash || url.searchParams.getAll('t').length !== 1 ||
        !['/dashboard', '/library'].includes(target) || !['sw', 'en', 'fr'].includes(language)) return null;
    var token = url.searchParams.get('t');
    if (!token || !/^[A-Za-z0-9_.:-]+$/.test(token) || token.length > 4096) return null;
    var destination = new URL(target, origin);
    destination.searchParams.set('t', token);
    destination.searchParams.set('lang', language);
    return destination.href;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { campusUrl: campusUrl };
  if (!root.document) return;
  var form = root.document.getElementById('campus-entry');
  if (!form) return;
  var input = root.document.getElementById('campus-link');
  var error = form.querySelector('.error');
  form.querySelector('button[type=submit]').disabled = false;
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var destination = campusUrl(input.value, form.dataset.origin, form.dataset.target, form.dataset.language);
    if (!destination) {
      error.textContent = form.dataset.error;
      input.setAttribute('aria-invalid', 'true');
      input.focus();
      return;
    }
    error.textContent = '';
    input.removeAttribute('aria-invalid');
    // No external site receives the personal link as a referrer.
    root.location.assign(destination);
  });
})(typeof window === 'undefined' ? {} : window);

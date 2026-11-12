// Tests the OBTS website in Chromium at phone, tablet and desktop widths.
//   NODE_PATH=$(npm root -g) node tools/check_site.cjs [screenshot_dir]
// Checks every page in EN, SW and FR: no script errors, no sideways scroll,
// every internal link and image resolves, the logo is not stretched, the
// menu and language switch work, every WhatsApp link is the school number,
// the registration form refuses an incomplete form and builds the WhatsApp
// message, and no page carries fees, e-mail addresses, partnership or
// accreditation claims, IIBTS leftovers or draft material.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const shots = process.argv[2];
const langs = { en: '', sw: 'sw/', fr: 'fr/' };
const pages = ['index', 'about', 'courses', 'how-to-learn', 'admissions', 'contact', 'faq', 'privacy', 'terms',
  'library', 'bookstore', 'portal', 'assistant', 'syllabus', 'learn', 'join-obts', 'research', 'campus', 'news', 'scholarships', 'standards', 'support', 'policies'];
const viewports = { phone: { width: 360, height: 780 }, tablet: { width: 820, height: 1180 }, desktop: { width: 1366, height: 900 } };
const WA = 'https://wa.me/255704686885';
const currency = /TZS|Tsh\b|USD\b|shilingi/i;
const forbidden = [/[\w.]+@[\w.]+\.\w+/, /partner|partenaire|ushirikiano/i, /guaranteed scholarships|bourses garanties|ufadhili wa uhakika/i,
  /accredit|ithibati|accrédit/i, /IIBTS|International Institute/i, /lorem|ipsum|TODO|placeholder text/i,
  /RASIMU|INASUBIRI UKAGUZI|majibu\.pdf|mwongozo\.pdf|answer key\.pdf/];
const failures = [];
let checks = 0;
const fail = (where, what) => failures.push(`${where}: ${what}`);
const ok = (condition, where, what) => { checks++; if (!condition) fail(where, what); };

(async () => {
  // Static checks on the HTML source.
  for (const [lang, folder] of Object.entries(langs)) {
    for (const page of pages) {
      const file = path.join(root, folder, page + '.html');
      const html = fs.readFileSync(file, 'utf8');
      const text = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '');
      // Sample exercises may use currency in teaching examples.
      const publicCopy = text.replace(/<details class="sample-lesson">[\s\S]*?<\/details>/g, '');
      ok(!currency.test(publicCopy), `${lang}/${page}`, 'no public enrollment prices');
      for (const pattern of forbidden) ok(!pattern.test(text), `${lang}/${page}`, `forbidden content ${pattern}`);
      ok(new RegExp(`<html lang="${lang}">`).test(html), `${lang}/${page}`, 'html lang attribute');
      // the school's official name, in every language: "Online Bible & Theology School" (never "... and Theology ...")
      ok(text.includes('Online Bible &amp; Theology School'), `${lang}/${page}`, 'official name Online Bible & Theology School');
      ok(!/Online Bible and Theology/.test(text), `${lang}/${page}`, 'old name "Online Bible and Theology School"');
      ok(/<meta property="og:site_name" content="OBTS — Online Bible &amp; Theology School">/.test(html), `${lang}/${page}`, 'og:site_name');
    }
  }

  const browser = await chromium.launch();
  for (const [device, viewport] of Object.entries(viewports)) {
    const context = await browser.newContext({ viewport });
    // Offline test: external requests (web fonts) are refused; the fallback fonts are used.
    await context.route(/^https?:\/\//, (route) => route.abort());
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    for (const [lang, folder] of Object.entries(langs)) {
      for (const name of pages) {
        const where = `${device} ${lang}/${name}`;
        const file = path.join(root, folder, name + '.html');
        errors.length = 0;
        await page.goto('file://' + file);
        await page.waitForLoadState('load');
        ok(errors.length === 0, where, 'script errors: ' + errors.join('; '));
        const width = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        ok(width <= 0, where, `page scrolls sideways by ${width}px`);
        if (name === 'learn') {
          const lessons = page.locator('.sample-course .sample-lesson');
          ok(await lessons.count() === 35, where, 'all 35 sample lessons are present');
          const firstLesson = lessons.first();
          await firstLesson.locator('summary').click();
          ok(await firstLesson.locator('.sample-body').isVisible(), where, 'sample lesson opens');
          await firstLesson.locator('summary').click();
          ok(!(await firstLesson.locator('.sample-body').isVisible()), where, 'sample lesson closes');
        }
        if (name === 'courses') {
          const samples = await page.locator('.card a[href^="learn.html#"]').evaluateAll(
            (links) => links.map((link) => link.hash.slice(1)));
          const learningPage = fs.readFileSync(path.join(root, folder, 'learn.html'), 'utf8');
          ok(samples.length === 7 && new Set(samples).size === 7 &&
            samples.every((id) => learningPage.includes(`class="sample-course" id="${id}"`)),
            where, 'each course links to its own sample lessons');
        }
        // Links and images.
        const links = await page.$$eval('a[href]', (as) => as.map((a) => a.getAttribute('href')));
        for (const href of links) {
          if (href.startsWith('https://wa.me/')) {
            const url = new URL(href);
            const command = { portal: 'DASHBOARD', library: 'MAKTABA', 'join-obts': 'NAHITAJI KUJIUNGA' }[name];
            ok(href === WA || (command && url.origin + url.pathname === WA &&
              url.searchParams.size === 1 && url.searchParams.get('text') === command && !url.hash),
              where, 'WhatsApp link ' + href);
            continue;
          }
          if (name === 'library' && href === `https://odm-ai-asistant.onrender.com/library?lang=${lang}`) continue;
          if (/^(https?:|mailto:|tel:)/.test(href)) { fail(where, 'external link not allowed: ' + href); continue; }
          if (href.startsWith('#')) { ok(await page.$(href) !== null, where, 'anchor ' + href); continue; }
          ok(fs.existsSync(path.resolve(path.dirname(file), href.split('#')[0])), where, 'broken link ' + href);
        }
        for (const image of await page.locator('img[loading="lazy"]').all()) {
          await image.scrollIntoViewIfNeeded();
          await image.evaluate((element) => element.decode().catch(() => {}));
        }
        await page.evaluate(() => window.scrollTo(0, 0));
        const images = await page.$$eval('img', (imgs) => imgs.map((i) => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0,
          ratio: i.getBoundingClientRect().width / Math.max(1, i.getBoundingClientRect().height), natural: i.naturalWidth / Math.max(1, i.naturalHeight),
          visible: i.getBoundingClientRect().width > 0 })));
        for (const image of images) {
          ok(image.ok, where, 'image not loaded ' + image.src);
          if (image.visible) ok(Math.abs(image.ratio - image.natural) < 0.03, where, `image stretched ${image.src} ${image.ratio.toFixed(2)} vs ${image.natural.toFixed(2)}`);
        }
        // Menu.
        const menuVisible = await page.isVisible('.menu-btn');
        if (device === 'phone' || (device === 'tablet' && menuVisible)) {
          // Phone: always a menu button. Tablet: a menu button or the full menu, and a menu button must work.
          ok(menuVisible, where, 'menu button hidden on phone');
          ok(!(await page.isVisible('#site-nav')), where, 'menu open before tapping');
          await page.click('.menu-btn');
          ok(await page.isVisible('#site-nav a[href="courses.html"]'), where, 'menu does not open');
          ok((await page.getAttribute('.menu-btn', 'aria-expanded')) === 'true', where, 'aria-expanded not updated');
        } else {
          ok(!menuVisible, where, 'menu button shown on desktop');
          ok(await page.isVisible('#site-nav a[href="courses.html"]'), where, 'navigation hidden on desktop');
        }
        for (const section of ['library', 'research']) {
          ok(await page.isVisible(`#site-nav a[href="${section}.html"]`), where, `${section} is available in the main menu`);
        }
        // Language switch: each link opens the same page in that language.
        const switches = await page.$$eval('.lang a', (as) => as.map((a) => [a.getAttribute('hreflang'), a.getAttribute('href')]));
        ok(switches.length === 3, where, 'language switch');
        for (const [code, href] of switches) {
          const target = path.resolve(path.dirname(file), href);
          ok(target === path.join(root, langs[code], name + '.html'), where, `language link ${code} -> ${href}`);
        }
        if (shots && (name === 'index' || name === 'admissions' || name === 'courses')) {
          fs.mkdirSync(shots, { recursive: true });
          await page.screenshot({ path: path.join(shots, `${device}-${lang}-${name}.png`), fullPage: true });
        }
      }
    }
    // Registration form, in each language.
    for (const [lang, folder] of Object.entries(langs)) {
      const where = `${device} ${lang}/admissions form`;
      await page.goto('file://' + path.join(root, folder, 'admissions.html'));
      await page.evaluate(() => { window.__opened = []; window.open = (url) => { window.__opened.push(url); return null; }; });
      await page.click('#registration button[type=submit]');
      ok((await page.textContent('#registration .error')).trim().length > 0, where, 'incomplete form accepted');
      ok((await page.evaluate(() => window.__opened.length)) === 0, where, 'WhatsApp opened for an incomplete form');
      await page.fill('#f-name', 'Test Student');
      await page.fill('#f-phone', '+255 700 000 000');
      await page.fill('#f-place', 'Dodoma, Tanzania');
      await page.check('#registration input[name=course] >> nth=0');
      ok(await page.isDisabled('#registration input[name=course] >> nth=6'), where, 'AI course should not be selectable yet');
      await page.check('#f-consent');
      await page.click('#registration button[type=submit]');
      const opened = await page.evaluate(() => window.__opened);
      ok(opened.length === 1 && opened[0].startsWith(WA + '?text='), where, 'WhatsApp message not opened: ' + opened);
      if (opened.length) {
        const message = decodeURIComponent(opened[0].split('?text=')[1]);
        ok(message.includes('Test Student') && message.includes('+255 700 000 000') && message.includes('Dodoma'), where, 'message content');
      }
    }
    await context.close();
  }
  // Pages of the earlier site now redirect to their OBTS replacement.
  for (const old of ['programs']) {
    const html = fs.readFileSync(path.join(root, old + '.html'), 'utf8');
    const target = (html.match(/url=([\w-]+\.html)/) || [])[1];
    ok(target && fs.existsSync(path.join(root, target)), old, 'redirect target');
  }
  // The old library.html is now the real library page (old links keep working).
  ok(/<h1>Library<\/h1>/.test(fs.readFileSync(path.join(root, 'library.html'), 'utf8')), 'library', 'old library link opens the library page');
  // Library/campus use the verified production routes; closed services say so.
  const notOpen = { en: 'Not yet open', sw: 'Bado haijafunguliwa', fr: 'Pas encore ouvert' };
  for (const [lang, folder] of Object.entries(langs)) {
    for (const name of ['library', 'bookstore', 'portal', 'assistant']) {
      const html = fs.readFileSync(path.join(root, folder, name + '.html'), 'utf8');
      const buttons = [...html.matchAll(/class="btn[^"]*" href="([^"]+)"/g)].map((m) => m[1]);
      const campusOpen = ['library', 'portal'].includes(name) && html.includes('id="campus-entry"');
      if (campusOpen) {
        const command = name === 'library' ? 'MAKTABA' : 'DASHBOARD';
        ok(!html.includes(notOpen[lang]) && html.includes(`text=${command}`), `${lang}/${name}`, 'personal link requested through the school WhatsApp');
        const allowed = [WA, WA + '?text=' + command, 'https://odm-ai-asistant.onrender.com/library?lang=' + lang];
        ok(buttons.length > 0 && buttons.every((href) => allowed.includes(href)), `${lang}/${name}`, 'only verified service/WhatsApp buttons');
      } else {
        ok(html.includes(notOpen[lang]), `${lang}/${name}`, 'service shows that it is not yet open');
        ok(buttons.length > 0 && buttons.every((href) => href === WA), `${lang}/${name}`, 'only WhatsApp buttons: ' + buttons.join(' '));
      }
    }
    const home = fs.readFileSync(path.join(root, folder, 'index.html'), 'utf8');
    ok(['library', 'bookstore', 'portal', 'assistant'].every((p) => home.includes(`href="${p}.html"`)), `${lang}/index`, 'home links every online service');
  }
  await browser.close();
  console.log(`${checks} checks, ${failures.length} failures`);
  failures.slice(0, 60).forEach((f) => console.log('FAIL ' + f));
  process.exit(failures.length ? 1 : 0);
})().catch((error) => { console.error(error); process.exit(1); });

"""Validate generated pages, local links/assets and language metadata without a browser."""
from html.parser import HTMLParser
from pathlib import Path
import build_site as builder
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


assert 'staging' not in builder.SERVICE_BASE.lower(), 'SERVICE_BASE must be the production address, never staging'
for lang in builder.LANGS:  # with an address, the library opens in the same language
    builder_base, builder.SERVICE_BASE = builder.SERVICE_BASE, builder.CAMPUS_ORIGIN
    try:
        assert f'{builder.CAMPUS_ORIGIN}/library?lang={lang}' in builder.service_page(lang, 'library')[2]
        assert f'data-language="{lang}"' in builder.campus_entry(lang, 'portal')
        assert 'text=DASHBOARD' in builder.service_page(lang, 'portal')[2]
        assert 'text=MAKTABA' in builder.service_page(lang, 'library')[2]
        assert builder.UI[lang]['not_open'] not in builder.service_page(lang, 'portal')[2]
        assert not builder.is_open('bookstore') and not builder.is_open('assistant')
    finally:
        builder.SERVICE_BASE = builder_base

builder_base, builder.SERVICE_BASE = builder.SERVICE_BASE, ''
try:
    assert not builder.is_open('portal') and not builder.is_open('library')
    assert not builder.campus_entry('sw', 'portal')
finally:
    builder.SERVICE_BASE = builder_base

for refused in ('http://odm-ai-asistant.onrender.com', 'https://odm-ai-asistant-staging.onrender.com',
                builder.CAMPUS_ORIGIN + '.example.com', builder.CAMPUS_ORIGIN + '/dashboard',
                builder.CAMPUS_ORIGIN + '?t=private', 'https://user:password@odm-ai-asistant.onrender.com'):
    builder_base, builder.SERVICE_BASE = builder.SERVICE_BASE, refused
    try:
        try:
            builder.service_origin()
        except ValueError:
            pass
        else:
            raise AssertionError('unsafe service address accepted')
    finally:
        builder.SERVICE_BASE = builder_base

checks = 0
for lang, folder in builder.LANGS.items():
    for name in builder.PAGES:
        file = ROOT / folder / (name + '.html')
        text = file.read_text()
        assert text == builder.page_html(lang, name), f'stale generated page: {file}'
        parsed = Page(text)
        assert any(t == 'html' and a.get('lang') == lang for t,a in parsed.tags)
        assert sum(t == 'h1' for t,a in parsed.tags) == 1
        expected = f'https://{builder.DOMAIN}/{folder}{"" if name == "index" else name + ".html"}'
        assert any(t == 'link' and a.get('rel') == 'canonical' and a.get('href') == expected for t,a in parsed.tags)
        for target_lang, target_folder in builder.LANGS.items():
            url = f'https://{builder.DOMAIN}/{target_folder}{"" if name == "index" else name + ".html"}'
            assert any(t == 'link' and a.get('hreflang') == target_lang and a.get('href') == url for t,a in parsed.tags)
        for tag, attrs in parsed.tags:
            value = attrs.get('src') if tag in ('img','script') else attrs.get('href') if tag in ('a','link') else None
            if not value or urlsplit(value).scheme or value.startswith('#'):
                continue
            target = (file.parent / unquote(urlsplit(value).path)).resolve()
            assert target.is_relative_to(ROOT) and target.exists(), f'{file}: missing {value}'
        # the school system is linked only once SERVICE_BASE names the checked production address
        if not builder.SERVICE_BASE:
            assert '/library?lang=' not in text, f'{file}: links to the school system while SERVICE_BASE is empty'
            assert 'id="campus-entry"' not in text, f'{file}: campus entry enabled before production verification'
        if name == 'admissions':
            assert 'id="registration-continue"' in text and '<noscript>' in text
        checks += 1
print(f'{checks} pages passed: source generation, links, assets, headings and language/canonical metadata')

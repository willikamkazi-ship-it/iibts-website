"""Validate generated pages, local links/assets and language metadata without a browser."""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'tools/build_site.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


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
        if name == 'admissions':
            assert 'id="registration-continue"' in text and '<noscript>' in text
        checks += 1
print(f'{checks} pages passed: source generation, links, assets, headings and language/canonical metadata')

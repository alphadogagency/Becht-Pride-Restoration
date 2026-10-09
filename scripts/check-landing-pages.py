#!/usr/bin/env python3
"""Check the static campaign pages without a browser or third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

SITE = Path(__file__).resolve().parents[1] / 'site-v2'
PHONE = 'tel:+14632384357'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags, self.ids, self.faqs, self.scripts = [], [], [], []
        self.detail, self.part, self.script = None, None, None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'details':
            self.detail = {'question': '', 'answer': ''}
        if self.detail is not None and tag in ('summary', 'p'):
            self.part = 'question' if tag == 'summary' else 'answer'
        if tag == 'script':
            self.script = [a, '']

    def handle_data(self, data):
        if self.detail is not None and self.part:
            self.detail[self.part] += data
        if self.script is not None:
            self.script[1] += data

    def handle_endtag(self, tag):
        if tag == 'details':
            self.faqs.append(self.detail)
            self.detail, self.part = None, None
        elif tag in ('summary', 'p'):
            self.part = None
        if tag == 'script':
            self.scripts.append(self.script)
            self.script = None


for slug in ('ppc-remodeling', 'ppc-restoration', 'ppc-insurance'):
    source = (SITE / (slug + '.html')).read_text()
    page = Page(source)
    assert sum(t == 'h1' for t, _ in page.tags) == 1, slug
    assert len(page.ids) == len(set(page.ids)), f'{slug}: duplicate IDs'
    assert not any(t in ('form', 'nav', 'iframe') for t, _ in page.tags), slug
    assert any(t == 'meta' and a.get('name') == 'robots' and a.get('content') == 'noindex, follow' for t, a in page.tags)
    assert any(t == 'link' and a.get('rel') == 'canonical' and a.get('href') == f'https://bechtpriderestoration.com/{slug}' for t, a in page.tags)
    placements = []
    for tag, a in page.tags:
        if tag == 'a':
            href = a.get('href', '')
            assert href in (PHONE, '#main', '/ppc-privacy'), f'{slug}: unwanted exit {href}'
            if href == PHONE:
                assert 'call-cta' in a.get('class', '').split()
                placements.append(a['data-cta'])
        if tag == 'img':
            assert a.get('alt') and a.get('width') and a.get('height'), f'{slug}: image metadata'
        paths = [a[k] for k in ('src', 'href') if k in a and a[k].startswith('/')]
        paths += [part.strip().split()[0] for part in a.get('srcset', '').split(',') if part.strip()]
        for path in paths:
            local = SITE / urlsplit(path).path.lstrip('/')
            assert local.is_file() or local.with_suffix('.html').is_file(), f'{slug}: missing {path}'
    assert len(placements) == len(set(placements)), f'{slug}: ambiguous call placement'
    schema = next(json.loads(s) for a, s in page.scripts if a.get('type') == 'application/ld+json')
    faq = next(item for item in schema['@graph'] if item['@type'] == 'FAQPage')['mainEntity']
    assert len(faq) == len(page.faqs)
    for data, visible in zip(faq, page.faqs):
        assert data['name'] == visible['question']
        assert data['acceptedAnswer']['text'] == visible['answer']
    assert 'AggregateRating' not in json.dumps(schema)
    default_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', source).group(1)
    assert len(re.sub('<[^>]+>', '', default_h1)) > 20, 'No-JS headline missing'
    print(f'{slug}: passed — {len(placements)} phone CTAs, {len(faq)} matching FAQs, assets present')

for match in re.finditer(r'url\([\'"]?(/[^)\'\"]+)', (SITE/'ppc/landing.css').read_text()):
    assert (SITE/match.group(1).lstrip('/')).is_file(), match.group(1)
print('Shared CSS assets: passed')

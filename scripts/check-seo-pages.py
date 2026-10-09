#!/usr/bin/env python3
"""Crawl rendered organic pages for indexing, links, schema, and brief coverage."""
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urljoin, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site-v2'
DOMAIN = 'https://bechtpriderestoration.com'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids, self.links, self.assets, self.images, self.forms = [], [], [], [], []
        self.title, self.h1, self.description, self.canonical = '', [], '', ''
        self.schemas, self.text, self.scripts = [], [], []
        self._title, self._h1, self._json, self._script = False, False, False, ''
        self.feed((SITE / path.lstrip('/') / 'index.html').read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'img':
            self.images.append(a)
            if a.get('src'): self.assets.append(a['src'])
        if tag == 'source': self.assets += [p.strip().split()[0] for p in a.get('srcset', '').split(',') if p.strip()]
        if tag == 'script' and a.get('src'): self.assets.append(a['src'])
        if tag == 'link':
            if a.get('rel') == 'canonical': self.canonical = a['href']
            elif a.get('href', '').startswith('/'): self.assets.append(a['href'])
        if tag == 'meta':
            if a.get('name') == 'description': self.description = a['content']
            assert a.get('name') != 'robots' or 'noindex' not in a.get('content', ''), f'{self.path}: noindex'
        if tag == 'form': self.forms.append(a)
        if tag == 'title': self._title = True
        if tag == 'h1': self._h1 = True; self.h1.append('')
        if tag == 'script': self._json = a.get('type') == 'application/ld+json'; self._script = ''

    def handle_endtag(self, tag):
        if tag == 'title': self._title = False
        if tag == 'h1': self._h1 = False
        if tag == 'script' and self._json:
            self.schemas.append(json.loads(self._script))
            self._json = False

    def handle_data(self, value):
        if self._title: self.title += value
        if self._h1: self.h1[-1] += value
        if self._json: self._script += value
        else: self.text.append(value)


urls = [e.text for e in ET.parse(SITE / 'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls) == len(set(urls)) == 31
pages = {urlsplit(u).path: Page(urlsplit(u).path) for u in urls}
assert len({p.title for p in pages.values()}) == len(pages), 'Duplicate titles'
assert len({p.description for p in pages.values()}) == len(pages), 'Duplicate descriptions'
inbound = defaultdict(set)
faq_count = 0

for path, page in pages.items():
    assert path.endswith('/') and path == path.lower(), f'{path}: URL format'
    assert len(page.h1) == 1, f'{path}: H1 count'
    assert len(page.title) < 60, f'{path}: title length {len(page.title)}'
    assert 140 <= len(page.description) <= 155, f'{path}: description length {len(page.description)}'
    assert '(463) 238-4357' in page.description, f'{path}: meta phone missing'
    assert page.canonical == DOMAIN + path, f'{path}: canonical'
    assert not [x for x, n in Counter(page.ids).items() if n > 1], f'{path}: duplicate IDs'
    assert len(page.forms) == 1 and page.forms[0].get('id') == 'contact-form', f'{path}: estimate form'
    assert {'name', 'phone', 'email', 'service', 'message'}.issubset(page.ids), f'{path}: form fields'
    for img in page.images:
        assert img.get('alt', '').strip(), f'{path}: empty image alt'
    for asset in page.assets:
        assert (SITE / unquote(urlsplit(asset).path).lstrip('/')).is_file(), f'{path}: missing {asset}'
    for link in page.links:
        resolved = urlsplit(urljoin(DOMAIN + path, link))
        if resolved.netloc != urlsplit(DOMAIN).netloc or resolved.scheme not in ['http', 'https']: continue
        assert resolved.path in pages, f'{path}: internal link not canonical: {link}'
        if resolved.fragment: assert unquote(resolved.fragment) in pages[resolved.path].ids, f'{path}: missing anchor {link}'
        inbound[resolved.path].add(path)
    assert len(page.schemas) == 1
    graph = page.schemas[0]['@graph']
    company = next(x for x in graph if x['@id'] == DOMAIN + '/#business')
    assert company['telephone'] == '+14632384357'
    assert company['address']['addressLocality'] == 'Indianapolis', f'{path}: invented branch'
    assert len(company['sameAs']) >= 2
    assert '24/7' in company['description']
    for node in graph:
        if node['@type'] == 'FAQPage':
            for faq in node['mainEntity']:
                text = ' '.join(page.text)
                assert faq['name'] in text and faq['acceptedAnswer']['text'] in text, f'{path}: invisible FAQ schema'
                faq_count += 1
        if node['@type'] == 'Service':
            assert node['provider']['@id'] == company['@id']
            assert node['url'] == page.canonical
    if path.startswith('/services/'):
        assert any(x['@type'] == 'Service' for x in graph)
        for heading in ['What’s included', 'Our process', 'Insurance help', 'Service area', 'Related services']:
            assert heading in ' '.join(page.text), f'{path}: missing {heading}'

cities = json.loads((ROOT / 'content/seo/cities.json').read_text())
assert len(cities) == 14
normalized = []
for city in cities:
    path = '/service-areas/' + city['slug'] + '/'
    page = pages[path]
    assert 200 <= sum(len(p.split()) for p in city['paragraphs']) <= 300
    assert len(inbound[path] - {path}) >= 3, f'{path}: insufficient inbound links'
    assert '/service-areas/' in inbound[path]
    assert any(p.startswith('/services/') for p in inbound[path])
    assert page.forms[0]['data-location'] == city['name']
    graph = page.schemas[0]['@graph']
    assert graph[0]['areaServed']['name'] == city['name'] + ', Indiana'
    for slug in ['water-damage', 'fire-damage', 'mold-remediation', 'storm-damage', 'home-remodeling', 'kitchen-bathroom-remodeling']:
        assert '/services/' + slug + '/' in page.links
    normalized.append(' '.join(city['paragraphs']).replace(city['name'], '[city]'))
assert len(set(normalized)) == 14, 'City copy is only a name swap'

rules = {}
for line in (SITE / '_redirects').read_text().splitlines():
    if not line or line.startswith('#'): continue
    source, target, status = line.split()
    assert status == '301'
    assert source not in rules, f'Duplicate redirect: {source}'
    rules[source] = target
for source, target in rules.items():
    assert target not in rules, f'Redirect chain: {source} -> {target}'
    assert target in pages or target.startswith('https://bechtpride.com/'), f'Redirect to missing page: {target}'
for alias, final in [('handyman', 'handyman-repairs'), ('remodeling', 'home-remodeling')]:
    for old in [f'/services/{alias}', f'/services/{alias}.html', f'/services/{alias}/']:
        assert rules[old] == f'/services/{final}/'

for p in SITE.glob('ppc-*.html'):
    assert 'noindex' in p.read_text(), f'{p}: campaign accidentally indexable'
print(f'PASS: {len(pages)} canonical pages; unique metadata; {faq_count} visible/schema FAQ pairs; all local assets and links; 14 city forms and copy ranges; {len(rules)} one-hop redirects.')

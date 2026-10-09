#!/usr/bin/env python3
"""Verify deployed or local canonical URLs and migration redirects over HTTP."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url):
    try:
        # Cloudflare rejects Python's generic default UA (1010). Identify this
        # first-party validation crawl explicitly; do not impersonate Googlebot.
        req = Request(url, method='GET', headers={'User-Agent': 'BechtSEOValidation/1.0'})
        with build_opener(NoRedirect).open(req, timeout=25) as response:
            return response.status, response.headers, response.read().decode('utf-8', errors='replace')
    except HTTPError as error:
        return error.code, error.headers, error.read().decode('utf-8', errors='replace')


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base', default='http://127.0.0.1:3002')
parser.add_argument('--all-redirects', action='store_true')
args = parser.parse_args()
base = args.base.rstrip('/')
urls = [e.text for e in ET.parse(ROOT/'site-v2/sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
checks = [(urlsplit(url).path, 200, None) for url in urls]
checks += [(p, 200, None) for p in ['/sitemap.xml', '/robots.txt', '/css/seo.css', '/js/main.js', '/ppc-remodeling', '/ppc-restoration', '/ppc-insurance']]
for line in (ROOT/'site-v2/_redirects').read_text().splitlines():
    if not line or line.startswith('#'): continue
    source, target, status = line.split()
    if '*' in source or target.startswith('https://'): continue
    if args.all_redirects or (source.startswith('/services/') and not source.endswith('/index.html')):
        checks.append((source, 301, target))
checks.append(('/services/handyman.html?utm_source=seo-check', 301, '/services/handyman-repairs/?utm_source=seo-check'))
checks.append(('/this-page-does-not-exist-seo-check', 404, None))


def check(row):
    path, expected, target = row
    status, headers, body = request(base + path)
    assert status == expected, f'{path}: expected {expected}, got {status}'
    if target:
        location = headers.get('Location', '')
        if location.startswith(base): location = location[len(base):]
        assert location == target, f'{path}: expected redirect {target}, got {location}'
    if status == 200 and (path == '/' or path.endswith('/')):
        assert 'noindex' not in headers.get('X-Robots-Tag', '').lower(), f'{path}: X-Robots-Tag noindex'
        assert 'name="robots" content="noindex' not in body, f'{path}: noindex meta'
        assert 'https://bechtpriderestoration.com' + path in body, f'{path}: missing canonical URL'
        assert 'id="contact-form"' in body, f'{path}: missing estimate form'
    return path


with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(check, checks))
print(f'PASS: {len(results)} HTTP checks at {base}: canonical pages, assets, campaigns, redirects, query preservation, and real 404 status.')

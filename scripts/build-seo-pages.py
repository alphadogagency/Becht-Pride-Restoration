#!/usr/bin/env python3
"""Build checked-in organic pages from shared components; no production build.

Edit content/seo/cities.json, content/seo/home.html, or seo_services.py, then run
python3 scripts/build-seo-pages.py. Campaign landing pages remain independent.
"""
from html import escape
from pathlib import Path
import csv
import io
import json
import re
from seo_services import SERVICES, RESTORATION, CORE

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site-v2'
CONTENT = ROOT / 'content' / 'seo'
CITIES = json.loads((CONTENT / 'cities.json').read_text())
DOMAIN = 'https://bechtpriderestoration.com'
# Search Console ownership for info@alphadogagency.com; retain after verification.
GOOGLE_SITE_VERIFICATION = '9d8Z1p8XgNCl3iZ0h0evzbvof7oB0WAaes02WWZXjBI'
PHONE = '(463) 238-4357'
TEL = 'tel:+14632384357'
BRAND = 'Becht Pride Restoration'
COUNTIES = ['Boone', 'Hamilton', 'Hancock', 'Hendricks', 'Johnson', 'Madison', 'Marion', 'Morgan', 'Shelby']
BY_SLUG = {s['slug']: s for s in SERVICES}
ALIASES = {'handyman': 'handyman-repairs', 'remodeling': 'home-remodeling'}
TODAY = '2026-10-09'
PAGES = []

DESCRIPTIONS = {
    'water-damage': 'Water damage restoration in Indianapolis: extraction, drying and repairs with 24/7 emergency help. Call (463) 238-4357 for your free estimate today.',
    'fire-damage': 'Fire damage restoration in Indianapolis: smoke cleanup, soot removal and rebuilding after a fire. Call (463) 238-4357 to discuss a free estimate.',
    'mold-remediation': 'Mold remediation in Indianapolis: assessment, containment, cleanup and repairs with moisture in mind. Call (463) 238-4357 for a free project estimate.',
    'storm-damage': 'Storm damage restoration in Indianapolis: tarping, water cleanup and repairs after wind or rain. Call (463) 238-4357 for emergency help and an estimate.',
    'home-remodeling': 'Home remodeling in Indianapolis: full renovations, basement finishing and post-damage rebuilding. Call (463) 238-4357 for a free project estimate.',
    'kitchen-bathroom-remodeling': 'Kitchen and bathroom remodeling in Indianapolis: showers, cabinets, tile and room updates. Call (463) 238-4357 to arrange your free project estimate.',
    'handyman-repairs': 'Handyman repairs in Indianapolis: drywall, painting, flooring and exterior home maintenance. Call (463) 238-4357 to discuss your free repair estimate.',
    'decks': 'Deck building and repair in Indianapolis: new decks, replacement and repairs to outdoor spaces. Call (463) 238-4357 to arrange a free project estimate.',
    'deck-and-fence-staining': 'Deck and fence staining in Indianapolis with surface preparation and finish options for your wood. Call (463) 238-4357 for a free project estimate.',
    'fence-repair': 'Fence repair and installation in Indianapolis: discuss damaged sections, gates and replacement. Call (463) 238-4357 to arrange a free project estimate.',
    'drywall': 'Drywall repair and installation in Indianapolis: wall patches, ceilings, finishing and painting. Call (463) 238-4357 for a free home repair estimate.',
    'painting': 'Interior and exterior painting in Indianapolis with surface preparation and drywall repair options. Call (463) 238-4357 for a free project estimate.',
    'power-washing': 'Power washing in Indianapolis for exterior surfaces and preparation before painting or staining. Call (463) 238-4357 to discuss a free project estimate.',
    'gutter-cleaning': 'Gutter cleaning in Indianapolis: discuss debris removal, downspouts and exterior maintenance. Call (463) 238-4357 for your free home service estimate.',
    'window-cleaning': 'Window cleaning in Indianapolis: discuss interior and exterior windows, access and maintenance. Call (463) 238-4357 to arrange a free project estimate.',
}


def esc(value):
    return escape(str(value), quote=True)


def service_path(slug):
    return f'/services/{slug}/'


def city_path(city):
    return f'/service-areas/{city["slug"]}/'


def anchor(url, label, css=''):
    return f'<a href="{esc(url)}"' + (f' class="{esc(css)}"' if css else '') + f'>{esc(label)}</a>'


def city_links():
    return '<ul class="seo-area-links">' + ''.join(f'<li>{anchor(city_path(c), c["name"])}</li>' for c in CITIES) + '</ul>'


def buttons(estimate='#contact'):
    return '<div class="seo-actions">' + anchor(TEL, f'Call {PHONE}', 'btn btn-primary') + anchor(estimate, 'Get a free estimate', 'btn seo-outline') + '</div>'


def business(city=None):
    return {
        '@type': ['LocalBusiness', 'GeneralContractor'], '@id': DOMAIN + '/#business',
        'name': BRAND, 'url': DOMAIN + '/', 'telephone': '+14632384357',
        'description': 'Indianapolis-based restoration and remodeling company. Emergency restoration calls are answered 24/7; office hours are Monday–Friday, 8am–4pm.',
        'logo': DOMAIN + '/image-assets/Becht_restoration_logo-01.svg',
        'image': DOMAIN + '/image-assets/hero-firedamage2.jpg',
        'address': {'@type': 'PostalAddress', 'streetAddress': '5601 S Meridian Street, Suite D', 'addressLocality': 'Indianapolis', 'addressRegion': 'IN', 'postalCode': '46217', 'addressCountry': 'US'},
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '00:00', 'closes': '23:59'}],
        'areaServed': {'@type': 'City', 'name': city + ', Indiana'} if city else [{'@type': 'AdministrativeArea', 'name': c + ' County, Indiana'} for c in COUNTIES],
        'sameAs': ['https://www.facebook.com/Becht-Pride-Residential', 'https://www.google.com/maps?q=place_id:ChIJe-L2WNFba4gRygWFgHQ8Qls&place_id=ChIJe-L2WNFba4gRygWFgHQ8Qls'],
    }


def structured(path, title, crumbs, service=None, city=None, faqs=None):
    url = DOMAIN + path
    graph = [business(city), {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'about': {'@id': DOMAIN + '/#business'}}]
    if crumbs:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'name': name, 'item': DOMAIN + route} for n, (name, route) in enumerate(crumbs)]})
    if service:
        graph.append({'@type': 'Service', '@id': url + '#service', 'name': service['name'], 'serviceType': service['name'], 'url': url, 'provider': {'@id': DOMAIN + '/#business'}, 'areaServed': [{'@type': 'AdministrativeArea', 'name': c + ' County, Indiana'} for c in COUNTIES]})
    if faqs:
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]})
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2).replace('<', '\\u003c')


def head(path, title, description, data):
    verification = (f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">\n'
                    if path == '/' else '')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{verification}<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{DOMAIN}{path}">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="preload" href="/ppc/assets/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/styles.css">
<link rel="stylesheet" href="/css/seo.css">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:image" content="{DOMAIN}/image-assets/hero-firedamage2.jpg">
<script type="application/ld+json">{data}</script>
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
'''


def nav_groups():
    groups = [
        ('Restoration', [(service_path(s), BY_SLUG[s]['name']) for s in RESTORATION]),
        ('Reconstruction', [(service_path('home-remodeling') + '#reconstruction', 'Rebuild after property damage'), (service_path('drywall'), 'Drywall repairs'), (service_path('painting'), 'Painting & finishing')]),
        ('Remodeling', [(service_path('home-remodeling'), 'Home remodeling'), (service_path('kitchen-bathroom-remodeling'), 'Kitchens & bathrooms')]),
        ('Handyman', [(service_path(s['slug']), s['name']) for s in SERVICES if s['group'] == 'handyman']),
    ]
    return ''.join('<div class="seo-nav-group"><p class="seo-nav-label">' + label + '</p>' + ''.join(anchor(url, name) for url, name in links) + '</div>' for label, links in groups)


def header():
    groups = nav_groups()
    return f'''<header class="header seo-header"><div class="container header-inner">
<a href="/" class="logo"><img src="/image-assets/Becht_restoration_logo-01.svg" alt="Becht Pride Restoration and Remodeling" width="150" height="70"></a>
<nav class="nav-links" aria-label="Main navigation">
<details class="seo-services-menu"><summary>Services</summary><div class="seo-mega-menu">{groups}</div></details>
<a href="/service-areas/">Service Areas</a><a href="/#about">About</a><a href="/#gallery">Our Work</a><a href="/#contact">Contact</a>
</nav><div class="header-cta">{anchor(TEL, 'Call ' + PHONE, 'btn btn-primary')}</div>
<button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-navigation"><span></span><span></span><span></span></button>
</div></header>
<nav class="mobile-nav" id="mobile-navigation" aria-label="Mobile navigation" inert>
<a href="/service-areas/">Service Areas</a><details><summary>Browse services</summary>{groups}</details>
<a href="/#about">About Becht Pride</a><a href="/#gallery">Our Work</a><a href="/#contact">Contact</a>{anchor(TEL, 'Call ' + PHONE, 'btn btn-primary')}
</nav>'''


def footer():
    core_links = ''.join(anchor(service_path(s), BY_SLUG[s]['name']) for s in CORE + ['handyman-repairs'])
    return f'''<footer class="footer"><div class="container"><div class="footer-grid seo-footer-grid">
<div class="footer-brand"><a class="logo" href="/"><img src="/image-assets/Becht_restoration_logo-01.svg" alt="Becht Pride Restoration and Remodeling" width="150" height="70" loading="lazy"></a><p>From cleanup to reconstruction. Restoration, remodeling, and home repairs across Central Indiana.</p><p>Based in Indianapolis. Serving homeowners across nine counties.</p></div>
<div><h2>Services</h2><div class="footer-links">{core_links}</div></div>
<div><h2>{anchor('/service-areas/', 'Service Areas')}</h2>{city_links()}</div>
<div class="footer-contact"><h2>Contact Becht Pride</h2><p>{anchor(TEL, PHONE)}</p><p>5601 S Meridian Street, Suite D<br>Indianapolis, IN 46217</p><p><strong>Emergency restoration: 24/7</strong><br>Office: Mon–Fri, 8am–4pm<br>Office closed Saturday and Sunday</p><p>{anchor('https://bechtpride.com/privacy-policy/', 'Privacy policy')}</p></div>
</div><div class="footer-bottom">© 2026 Becht Pride Restoration and Remodeling. All rights reserved.</div></div></footer>
<script src="/js/main.js" defer></script></body></html>'''


def picture(key, alt, eager=False):
    galleries = {'deck': '/gallery/decks-fences-boat-docksandmore/newdeckbuild.avif', 'fence': '/gallery/decks-fences-boat-docksandmore/fencebuild.avif', 'painting': '/gallery/painting/livingroom.avif'}
    priority = 'fetchpriority="high"' if eager else 'loading="lazy"'
    if key in galleries:
        return f'<img src="{galleries[key]}" alt="{esc(alt)}" {priority} decoding="async">'
    dimensions = {'water': (800, 533), 'fire': (800, 1200), 'mold': (800, 450), 'storm': (800, 533), 'remodeling': (800, 533), 'bathroom': (946, 1255), 'flooring': (1008, 567), 'restoration': (1160, 756)}
    w, h = dimensions[key]
    return f'<picture><source type="image/webp" srcset="/ppc/assets/{key}-480.webp {min(w,480)}w, /ppc/assets/{key}-960.webp {min(w,960)}w" sizes="(max-width: 760px) 100vw, 48vw"><img src="/ppc/assets/{key}.jpg" width="{w}" height="{h}" alt="{esc(alt)}" {priority} decoding="async"></picture>'


def hero(title, summary, eyebrow, crumbs, image='restoration', alt='Fire-damaged kitchen and its restored interior'):
    trail = '<nav class="seo-breadcrumb" aria-label="Breadcrumb">' + '<span aria-hidden="true"> / </span>'.join(anchor(route, name) for name, route in crumbs[:-1]) + '<span aria-hidden="true"> / </span><span aria-current="page">' + esc(crumbs[-1][0]) + '</span></nav>'
    return f'''<section class="seo-hero"><div class="container">{trail}<div class="seo-hero-grid"><div><p class="seo-eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1><p class="seo-lead">{esc(summary)}</p>{buttons()}<p class="seo-hero-note">Insured &amp; bonded · Free estimates</p></div><div class="seo-hero-photo">{picture(image, alt, True)}</div></div></div></section>'''


def cards(slugs=CORE):
    alts = {'water': 'Interior affected by water damage', 'fire': 'Fire-damaged interior before cleanup', 'mold': 'Visible mold on an interior surface', 'storm': 'Storm damage affecting a home', 'remodeling': 'Interior remodeling inspiration', 'bathroom': 'Bathroom vanity and tile from the Becht Pride project gallery'}
    return '<div class="services-grid seo-service-grid">' + ''.join(f'<article class="service-card"><div class="service-card-image">{picture(BY_SLUG[s]["image"], alts.get(BY_SLUG[s]["image"], BY_SLUG[s]["name"]))}</div><div class="service-card-body"><h3>{anchor(service_path(s), BY_SLUG[s]["name"])}</h3><p>{esc(BY_SLUG[s]["included"][0])}.</p>{anchor(service_path(s), "Explore " + BY_SLUG[s]["name"].lower(), "service-card-link")}</div></article>' for s in slugs) + '</div>'


def faqs_html(faqs, heading='Frequently asked questions'):
    return '<section class="seo-faq" id="faq"><h2>' + esc(heading) + '</h2>' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs) + '</section>'


def form(location='Indianapolis', service=''):
    options = '<option value="">Select a service</option>' + ''.join(f'<option value="{esc(s["slug"])}"' + (' selected' if s['slug'] == service else '') + f'>{esc(s["name"])}</option>' for s in SERVICES) + '<option value="other">Other</option>'
    return f'''<section class="section seo-contact" id="contact"><div class="container contact-grid">
<div class="contact-info"><p class="seo-eyebrow">Let’s talk about your home</p><h2>Request a free estimate in {esc(location)}</h2><p>Describe the damage or the improvements you have in mind. Include your address and the rooms involved so we can discuss the next step.</p><p><strong>Need emergency restoration help?</strong> Call {anchor(TEL, PHONE)}. We answer restoration calls 24/7. For urgent needs, call rather than waiting for a form response.</p><p>Office hours: Monday–Friday, 8am–4pm.</p></div>
<div class="contact-form-wrapper"><h3>Tell us about your project</h3>
<form id="contact-form" data-location="{esc(location)}">
<div class="form-row"><div class="form-group"><label for="name">Full name *</label><input id="name" name="name" autocomplete="name" required maxlength="150" aria-describedby="name-error"><p class="error-msg" id="name-error">Please enter your name.</p></div>
<div class="form-group"><label for="phone">Phone *</label><input id="phone" name="phone" type="tel" autocomplete="tel" required maxlength="40" aria-describedby="phone-error"><p class="error-msg" id="phone-error">Please enter your phone number.</p></div></div>
<div class="form-group"><label for="email">Email *</label><input id="email" name="email" type="email" autocomplete="email" required maxlength="200" aria-describedby="email-error"><p class="error-msg" id="email-error">Please enter a valid email.</p></div>
<div class="form-group"><label for="service">Service</label><select id="service" name="service">{options}</select></div>
<div class="form-group"><label for="message">Address and project details *</label><textarea id="message" name="message" required maxlength="5000" placeholder="Your address, affected rooms, or remodeling goals" aria-describedby="message-error"></textarea><p class="error-msg" id="message-error">Please describe your project.</p></div>
<p class="seo-form-note">By submitting, you ask Becht Pride to contact you about this request. {anchor('https://bechtpride.com/privacy-policy/', 'Privacy policy')}.</p>
<button type="submit" class="btn btn-primary form-submit">Request my free estimate</button><p class="form-status" role="status" aria-live="polite"></p>
</form><div class="form-success" role="status" tabindex="-1"><h3>Thank you for contacting Becht Pride.</h3><p>Your request has been received. Our team will follow up about your project. For emergency restoration, call {anchor(TEL, PHONE)}.</p></div>
<noscript><p>Please call {anchor(TEL, PHONE)} to request an estimate. The online form requires JavaScript.</p></noscript>
</div></div></section>'''


def write_page(path, title, description, body, crumbs=None, service=None, city=None, faqs=None):
    data = structured(path, title, crumbs, service, city, faqs)
    html = head(path, title, description, data) + header() + '<main id="main">' + body + '</main>' + footer()
    dest = SITE / path.lstrip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    PAGES.append({'path': path, 'title': title, 'description': description, 'kind': 'city' if city else 'service' if service else 'hub' if path == '/service-areas/' else 'home'})


def service_page(s):
    path = service_path(s['slug'])
    crumbs = [('Home', '/'), (s['name'], path)]
    emergency = s['group'] == 'restoration'
    summary = '24/7 emergency help, a clear repair plan, and one company from cleanup through reconstruction.' if emergency else 'Thoughtful improvements, a clear scope, and one local team to coordinate the work.'
    body = hero(s['name'] + ' in Indianapolis & Central Indiana', summary, 'Restoration • Indianapolis, IN' if emergency else 'Home improvements • Indianapolis, IN', crumbs, s['image'], s['name'] + ' — service illustration' if s['image'] in ['water','fire','mold','storm','remodeling'] else s['name'] + ' project detail')
    body += '<section class="service-content"><div class="container seo-reading-grid"><div class="service-main">'
    body += '<h2>' + esc(s['name']) + ' for your home</h2><p>' + esc(s['intro']) + '</p><p>' + esc(s['detail']) + '</p>'
    body += '<h2>What’s included</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in s['included']) + '</ul>'
    if s['slug'] == 'kitchen-bathroom-remodeling':
        body += '<section class="seo-project-photos"><h2>Bathroom details from our project gallery</h2><div class="service-gallery-grid">'
        for filename, alt in [('customshowertile.avif', 'Custom tile shower from the Becht Pride project gallery'), ('bluevanity.avif', 'Bathroom with a blue vanity and tile floor'), ('newshower.avif', 'Tiled shower installation'), ('twinremodel.avif', 'Bathroom remodeling detail')]:
            body += f'<img src="/gallery/bathroom-remodels/{filename}" alt="{alt}" loading="lazy" decoding="async">'
        body += '</div></section>'
    body += '<h2>Our process</h2><ol class="seo-process">' + ''.join(f'<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for a, b in s['steps']) + '</ol>'
    if s['slug'] == 'home-remodeling':
        body += '<section id="reconstruction"><h2>Reconstruction after property damage</h2><p>Our restoration and remodeling teams connect cleanup with rebuilding. Once affected areas are ready, we can repair or replace drywall, flooring, cabinets, trim, and other finishes. We discuss the repair scope and any optional upgrades separately, including how to keep insurance-related repairs distinct from planned improvements.</p><p>Tell us about the loss and the rooms involved so the assessment and estimate can account for the complete project.</p></section>'
    body += '<h2>Insurance help and repair estimates</h2><p>' + ('We can document the damage, provide repair estimates, and communicate with your adjuster about the scope of work. Your insurer determines policy coverage, deductibles, and payment. Optional upgrades should be discussed separately from the damage-related repair estimate.' if emergency else 'For work connected to an insured property loss, we can document the proposed repairs and provide an estimate for your adjuster. Routine maintenance and planned improvements are quoted as their own projects. Coverage depends on your policy and is decided by your insurer.') + '</p>'
    body += '<h2>Service area</h2><p>Based in Indianapolis, we serve homeowners across ' + ', '.join(COUNTIES[:-1]) + ', and ' + COUNTIES[-1] + ' Counties. Explore your city for local information and estimate requests.</p>' + city_links()
    body += faqs_html(s['faqs'], s['name'] + ': common questions')
    related = [x for x in RESTORATION if x != s['slug']] + ['home-remodeling'] if emergency else [x['slug'] for x in SERVICES if x['group'] != 'restoration' and x['slug'] != s['slug']]
    body += '<h2>Related services</h2><ul class="seo-related">' + ''.join('<li>' + anchor(service_path(x) + ('#reconstruction' if emergency and x == 'home-remodeling' else ''), 'Reconstruction after damage' if emergency and x == 'home-remodeling' else BY_SLUG[x]['name']) + '</li>' for x in related) + '</ul></div>'
    body += '<aside><div class="service-sidebar-card"><h2>Talk through your project</h2><p>Share the location, the affected rooms, and your priorities. We’ll discuss the work and next steps.</p>' + buttons() + '</div></aside></div></section>'
    body += form('Indianapolis', s['slug'])
    write_page(path, s['title'], DESCRIPTIONS[s['slug']], body, crumbs, service=s, faqs=s['faqs'])


def city_page(c):
    city, path = c['name'], city_path(c)
    title = f'Restoration in {city}, IN | Becht Pride'
    description = f'Water, fire, mold and storm restoration in {city}, IN, plus home remodeling. Call (463) 238-4357 for 24/7 emergency help or a free project estimate.'
    crumbs = [('Home', '/'), ('Service Areas', '/service-areas/'), (city, path)]
    body = hero(f'Restoration & Remodeling Services in {city}, IN', f'Water, fire, mold, and storm damage help in {city}, with remodeling services to put your home back together.', f'{c["county"]} County • Emergency restoration calls answered 24/7', crumbs)
    body += '<section class="section"><div class="container seo-local-copy"><p class="seo-eyebrow">Your home. Your next step.</p><h2>' + esc(c['heading']) + '</h2><div class="seo-local-paragraphs">' + ''.join('<p>' + esc(p) + '</p>' for p in c['paragraphs']) + '</div><p class="seo-source">Local reference: ' + anchor(c['source'], c['source_label']) + '.</p></div></section>'
    body += '<section class="section seo-white"><div class="container"><div class="section-header"><h2>How we can help in ' + city + '</h2><p>Choose a service to learn about the process, repair scope, and common questions.</p></div>' + cards() + '</div></section>'
    body += '<section class="section"><div class="container seo-two-up"><div><p class="seo-eyebrow">From damage to a repair plan</p><h2>Insurance documentation and repair estimates</h2><p>We can document affected materials, prepare an estimate, and communicate with your adjuster about the repairs. Your insurance company decides coverage and payment. If you want upgrades while rebuilding, we discuss those separately from the damage-related scope.</p></div><div class="seo-note"><h2>One team through the next stage</h2><p>Cleanup, drying, and reconstruction are connected steps. Our restoration and remodeling services help you plan the work in order, with clear communication about the spaces involved.</p>' + anchor(service_path('home-remodeling') + '#reconstruction', 'Learn about reconstruction') + '</div></div></section>'
    body += form(city)
    nearby = [x for x in CITIES if x['county'] == c['county'] and x != c]
    body += '<section class="section seo-area-return"><div class="container"><h2>Serving ' + city + ' and Central Indiana</h2><p>' + anchor('/service-areas/', 'View all service areas') + '</p>'
    if nearby:
        body += '<p>Also serving: ' + ' · '.join(anchor(city_path(x), x['name']) for x in nearby) + '.</p>'
    body += '</div></section>'
    write_page(path, title, description, body, crumbs, city=city)


def hub_page():
    path = '/service-areas/'
    crumbs = [('Home', '/'), ('Service Areas', path)]
    title = 'Restoration Service Areas in Indiana | Becht Pride'
    description = 'Explore restoration and remodeling in 14 Central Indiana cities, including Indianapolis. Call (463) 238-4357 for emergency help or a free estimate.'
    body = hero('Restoration & Remodeling Across Central Indiana', 'Find your city, explore our services, and talk with our Indianapolis-based team about damage repairs or your next home improvement.', '14 cities • Nine counties • One restoration and remodeling team', crumbs)
    body += '<section class="section"><div class="container"><div class="section-header"><h2>Find your service area</h2><p>We serve homeowners across Boone, Hamilton, Hancock, Hendricks, Johnson, Madison, Marion, Morgan, and Shelby Counties. These city guides explain our restoration and remodeling services with local context. For addresses outside the listed cities, call to discuss coverage and scheduling.</p></div><div class="seo-city-grid">'
    for c in CITIES:
        body += f'<a class="seo-city-card" href="{city_path(c)}"><span>{esc(c["county"])} County</span><h3>{esc(c["name"])}, IN</h3><p>Restoration, reconstruction &amp; remodeling</p><strong>Explore services <span aria-hidden="true">→</span></strong></a>'
    body += '</div></div></section><section class="section seo-white"><div class="container"><div class="section-header"><h2>Help for the damage. A plan for the repairs.</h2><p>Call 24/7 for emergency restoration, or request a free estimate for a planned improvement.</p></div>' + cards() + '</div></section>' + form()
    write_page(path, title, description, body, crumbs)


def home_page():
    body = (CONTENT / 'home.html').read_text()
    body = body[:body.index('  <!-- ====== CONTACT')]
    body = body.replace('Full-Service Restoration in Indianapolis', 'Restoration &amp; Remodeling in Indianapolis, IN')
    body = body.replace('Becht Pride Residential Services', 'Becht Pride Restoration')
    body = re.sub(r'href="/services/([^".]+)\.html"', lambda m: 'href="' + service_path(ALIASES.get(m[1], m[1])) + '"', body)
    body = body.replace('alt="Becht Pride Service Awards and Certifications"', 'alt="Becht Pride service recognition badges"')
    body = body.replace('Mold spreads fast and puts your family\'s health at risk.', 'Mold growth needs attention to both the affected materials and the moisture source.')
    body = body.replace('Becht Pride Restoration has served thousands of homeowners across Central Indiana since 2012', 'Becht Pride Restoration serves homeowners across Central Indiana')
    # Use the supplied, named campaign reviews; their cities are not established.
    start = body.index('  <!-- ====== TESTIMONIALS') if '  <!-- ====== TESTIMONIALS' in body else body.index('  <section id="testimonials"')
    body = body[:start]
    reviews = [('Michael Woodward', 'We couldn’t be happier with Becht Pride Restoration. Their communication was top-notch from start to finish, and their professionalism truly stood out. They did an excellent job, showed up when they said they would, and delivered exactly what they promised. Highly recommend!'), ('Griffin Smith', 'Becht Pride has helped with numerous projects around my house including full bathroom remodels, painting, main line plumbing, and getting into my tight attic to repair a screen.'), ('Kelly Mccoy', 'Becht Pride — always responsive, on time, friendly, quality work and excellent pricing!')]
    body += '<section class="section seo-white" id="testimonials"><div class="container"><div class="section-header"><h2>What our customers say</h2><p>Feedback from Becht Pride customers.</p></div><div class="seo-reviews">' + ''.join(f'<figure><blockquote>“{esc(q)}”</blockquote><figcaption>{esc(n)} · Google review' + (' excerpt' if n == 'Griffin Smith' else '') + '</figcaption></figure>' for n, q in reviews) + '</div></div></section>'
    body += '<section class="section"><div class="container"><h2>Restoration and remodeling in your community</h2><p>Explore our Central Indiana service areas for local information and ways to get help.</p>' + city_links() + '<p>' + anchor('/service-areas/', 'View the Service Areas guide') + '</p></div></section>' + form()
    body += '<div class="lightbox" role="dialog" aria-modal="true" aria-label="Project photo"><button class="lightbox-close" aria-label="Close photo">×</button><button class="lightbox-prev" aria-label="Previous photo">‹</button><button class="lightbox-next" aria-label="Next photo">›</button><img alt="Selected Becht Pride project photo"></div>'
    title = 'Restoration & Remodeling Indianapolis, IN | Becht Pride'
    description = 'Restoration and remodeling in Indianapolis: water, fire, mold, storm cleanup and home repairs. Call (463) 238-4357 for 24/7 help or a free estimate.'
    write_page('/', title, description, body)


def redirects():
    lines = ['# Generated by scripts/build-seo-pages.py. Specific redirects precede legacy fallbacks.']
    # Every historical spelling goes directly to its canonical destination.
    for old in [s['slug'] for s in SERVICES] + list(ALIASES):
        dest = service_path(ALIASES.get(old, old))
        for prefix in ['', '/site', '/site-v1', '/site-v2']:
            for suffix in ['', '.html', '/', '/index.html']:
                src = f'{prefix}/services/{old}{suffix}'
                if src != dest:
                    lines.append(f'{src} {dest} 301')
    lines.extend(['/index.html / 301', '/service-areas /service-areas/ 301', '/service-areas/index.html /service-areas/ 301'])
    for c in CITIES:
        dest = city_path(c)
        lines.extend([f'{dest.rstrip("/")} {dest} 301', f'{dest}index.html {dest} 301'])
    lines.extend(['/site/* / 301', '/site-v1/* / 301', '/site-v2/* / 301', '/INSTRUCTIONS.md / 301', '/ppc-privacy https://bechtpride.com/privacy-policy/ 301', '/ppc-privacy.html https://bechtpride.com/privacy-policy/ 301'])
    (SITE / '_redirects').write_text('\n'.join(lines) + '\n')
    # Superseded HTML files are removed so only canonical pages are served.
    for old in [s['slug'] for s in SERVICES] + list(ALIASES):
        (SITE / 'services' / (old + '.html')).unlink(missing_ok=True)


def reports():
    urls = [DOMAIN + p['path'] for p in PAGES]
    (SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    (SITE / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + DOMAIN + '/sitemap.xml\n')
    report = io.StringIO()
    writer = csv.writer(report)
    writer.writerow(['URL', 'Page type', 'Title', 'Title characters', 'Meta description', 'Description characters'])
    for p in PAGES:
        writer.writerow([DOMAIN + p['path'], p['kind'], p['title'], len(p['title']), p['description'], len(p['description'])])
    (ROOT / 'docs' / 'seo-url-inventory.csv').write_text(report.getvalue())
    (ROOT / 'docs' / 'seo-rank-tracking-urls.txt').write_text('\n'.join(urls) + '\n')
    print(f'Generated {len(PAGES)} canonical pages: home, {len(SERVICES)} services, hub, {len(CITIES)} cities.')
    for p in PAGES:
        if len(p['title']) >= 60 or not 140 <= len(p['description']) <= 155:
            print(f'Metadata length: {p["path"]}: title={len(p["title"])} description={len(p["description"])}')


if __name__ == '__main__':
    home_page()
    for service in SERVICES:
        service_page(service)
    hub_page()
    for city in CITIES:
        city_page(city)
    redirects()
    reports()

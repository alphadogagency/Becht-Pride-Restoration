#!/usr/bin/env python3
"""Generate three standalone static campaign pages. No production build required.

Edit the content below and run python3 scripts/build-landing-pages.py.
Generated pages are checked in and deploy directly from site-v2.
"""
from html import escape as esc
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site-v2'
PHONE = '(463) 238-4357'
TEL = 'tel:+14632384357'
DOMAIN = 'https://bechtpriderestoration.com'

PATHS = {
 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 2 .7 2.9a2 2 0 0 1-.5 2.1L8 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.4 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/>',
 'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
 'check': '<path d="m5 12 4 4L19 6"/>',
 'cross': '<path d="m6 6 12 12M6 18 18 6"/>',
 'shield': '<path d="M12 3 3 7v5c0 6 9 10 9 10s9-4 9-10V7l-9-4z"/><path d="m8 12 3 3 5-6"/>',
 'home': '<path d="m3 10 9-7 9 7v11H3V10z"/><path d="M9 21v-8h6v8"/>',
 'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="2.5"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'file': '<path d="M14 2H5v20h14V7l-5-5zM14 2v6h5M8 12h8M8 16h8"/>',
 'tools': '<path d="m14 5 5 5M3 21l9-9M14 2l-4 4 8 8 4-4-8-8zM3 3l5 5M3 3v4l4 1"/>',
 'drop': '<path d="M12 2S4 11 4 15a8 8 0 0 0 16 0c0-4-8-13-8-13z"/><path d="M8 15a4 4 0 0 0 4 4"/>',
 'kitchen': '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 10h18M11 10v10M16 13v4M7 13v4M5 7h2M11 7h2M17 7h2"/>',
 'basement': '<path d="m3 9 9-6 9 6v12H3V9zM4 14h16M7 18h2m3 0h2m3 0h2"/>',
 'shower': '<path d="M5 21V6a3 3 0 0 1 6 0v1M8 8h6M9 12v1m4-1v1m-4 3v1m4-1v1m-4 3v1m4-1v1"/>',
 'hail': '<path d="M7 13a5 5 0 1 1 9-5 3 3 0 1 1 2 6H7"/><path d="m7 17-1 3m6-3-1 3m6-3-1 3"/>',
 'star': '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3z"/>',
}


def icon(name, extra=''):
    return f'<svg {extra} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PATHS.get(name, PATHS["home"])}</svg>'


def cta(location, label=None, dark=False, text=False):
    label = label or f'Call {PHONE}'
    classes = 'text-link' if text else 'button' + (' dark' if dark else '')
    leading = '' if text else icon('phone')
    return f'<a class="{classes} call-cta" href="{TEL}" data-cta="{esc(location)}">{leading}<span>{esc(label)}</span>{icon("arrow", "class=\"arrow\"") if text else ""}</a>'


SIZES = {'bathroom':(946,1255),'shower':(448,336),'flooring':(1008,567),'water':(800,533),'fire':(800,1200),'mold':(800,450),'storm':(800,533),'remodeling':(800,533),'restoration':(1160,756)}


def picture(name, alt, eager=False, sizes='(max-width: 767px) 100vw, 50vw'):
    width, height = SIZES[name]
    low, high = min(480,width), min(960,width)
    srcset = f'/ppc/assets/{name}-480.webp {low}w'
    if high > low:
        srcset += f', /ppc/assets/{name}-960.webp {high}w'
    loading = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}"><img src="/ppc/assets/{name}.jpg" alt="{esc(alt)}" width="{width}" height="{height}" {loading} decoding="async"></picture>'


def head(label, title, description='', wide=False):
    return f'<div class="section-head{" wide" if wide else ""}"><div><div class="eyebrow">{esc(label)}</div><h2>{esc(title)}</h2>{f"<p>{esc(description)}</p>" if description else ""}</div>{"<span class=small-label>One local team. Every detail.</span>" if wide else ""}</div>'


def checks(items):
    return '<ul class="checks">' + ''.join(f'<li>{icon("check")}<span>{esc(item)}</span></li>' for item in items) + '</ul>'


def section(content, classes='', ident=''):
    return f'<section {f"id={ident}" if ident else ""} class="section reveal {classes}"><div class="container">{content}</div></section>'


def banner(title, sub):
    return f'<section class="banner"><div class="container"><div><h2>{esc(title)}</h2><p>{esc(sub)}</p></div>{cta("midbanner",dark=True)}</div></section>'


REVIEWS = {
 'griffin': ('Griffin Smith', 'GS', 'Becht Pride has helped with numerous projects around my house including full bathroom remodels, painting, main line plumbing, and getting into my tight attic to repair a screen. … They’re reliable, skilled, and can genuinely fix anything. What sets them apart is Ben’s commitment to satisfaction — if something isn’t right, he makes sure his team comes back and takes care of it. No runaround.', 'Google Local Guide · Excerpt'),
 'michael': ('Michael Woodward', 'MW', 'We couldn’t be happier with Becht Pride Restoration. Their communication was top-notch from start to finish, and their professionalism truly stood out. They did an excellent job, showed up when they said they would, and delivered exactly what they promised. Highly recommend!', 'Google Local Guide'),
 'kelly': ('Kelly Mccoy', 'KM', 'Becht Pride — always responsive, on time, friendly, quality work and excellent pricing!', 'Google Review'),
}


def reviews(page):
    order = ['griffin','michael','kelly'] if page == 'remodeling' else ['michael','griffin','kelly']
    cards = []
    for n,key in enumerate(order):
        name, initials, quote, source = REVIEWS[key]
        if key == 'griffin' and page != 'remodeling':
            quote = 'They’re reliable, skilled, and can genuinely fix anything. What sets them apart is Ben’s commitment to satisfaction — if something isn’t right, he makes sure his team comes back and takes care of it. No runaround.'
        cards.append(f'<article class="review {"featured" if n==0 else ""}"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>“{esc(quote)}”</blockquote><div class="review-author"><div class="avatar" aria-hidden="true">{initials}</div><div><strong>{name}</strong><span>{source}</span></div></div><div class="review-source">Google customer review</div></article>')
    return section(head('Good work. In their words.', 'Indianapolis homeowners recommend Becht Pride.', 'Clear communication. People who show up. Work that speaks for itself.') + '<div class="review-grid">'+''.join(cards)+'</div><div class="section-foot">'+cta('reviews')+'</div>','navy reviews')


def services(page):
    cards = []
    for n,card in enumerate(page['cards'],1):
        key,title,copy,img,ico,matches,bullets = card
        visual = picture(img, page['image_alts'].get(img,title), sizes='(max-width: 767px) 100vw, 33vw') if img else icon(ico)
        bullet_html = '<ul>'+''.join(f'<li>{esc(b)}</li>' for b in bullets)+'</ul>' if bullets else ''
        cards.append(f'<article class="service-card" data-matches="{esc(matches)}"><div class="service-picture {"icon-picture" if not img else ""}">{visual}<span class="number">{n:02d}</span></div><div class="card-body"><h3>{esc(title)}</h3><p>{esc(copy)}</p>{bullet_html}{cta("svc-"+key,"Call about "+page["call_about"].get(key,key.replace("-"," ")),text=True)}</div></article>')
    reorder = '''<script>(()=>{const p=window.bechtLanding;if(!p.matched)return;const grid=document.querySelector('.service-grid');const card=[...grid.children].find(c=>c.dataset.matches.split(' ').includes(p.service));if(card){grid.prepend(card);card.classList.add('matched');}})();</script>'''
    return section(head('The right help for your home',page['services_title'],page['services_sub'],True)+f'<div class="service-grid {"four" if len(cards)==4 else ""}">'+''.join(cards)+'</div>'+reorder,'white', 'services')


def process(title, sub, steps, insurance=False):
    items = []
    for n,(heading,copy) in enumerate(steps,1):
        content = f'<div class="step-index">STEP {n:02d}</div><h3>{esc(heading)}</h3><p>{esc(copy)}</p>'
        items.append(f'<li>{content}</li>' if insurance else f'<article class="step">{content}</article>')
    if insurance:
        intro = head('A clear path forward',title,sub)
        body = '<div class="insurance-timeline">'+intro+'<ol class="timeline">'+''.join(items)+'</ol></div>'
    else:
        body = head('From first call to final walkthrough',title,sub)+'<div class="steps">'+''.join(items)+'</div>'
    return section(body+'<div class="section-foot">'+cta('process',f'Start with a call — {PHONE}')+'</div>')


CITIES = ['Indianapolis','Carmel','Fishers','Noblesville','Westfield','Zionsville','Lawrence','Greenwood','Franklin','Plainfield','Avon','Brownsburg','Danville','Greenfield','Shelbyville','Martinsville','Lebanon','Anderson','Speedway','Beech Grove','Mooresville','McCordsville']


def area(page):
    copy = 'We help homeowners in Indianapolis and nearby Central Indiana communities. Call to confirm availability for your address and project.'
    return section('<div class="area-layout"><div class="area-copy"><div class="eyebrow">Local roots. Central Indiana reach.</div><h2>'+esc(page['area_title'])+'</h2><p>'+copy+'</p>'+cta('area',f'Call {PHONE}',text=True)+'</div><div><div class="cities">'+''.join(f'<span class="city">{city}</span>' for city in CITIES)+'</div><p class="county-note">Marion · Hamilton · Hendricks · Johnson · Boone · Hancock · Madison · Morgan · Shelby counties</p></div></div>','white')


def faq(page):
    answers=[]
    for n,(q,a) in enumerate(page['faq']):
        answer=esc(a).replace(PHONE, f'<a class="call-cta" data-cta="faq-{n+1}" href="{TEL}">{PHONE}</a>')
        answers.append(f'<details><summary>{esc(q)}</summary><p>{answer}</p></details>')
    return section('<div class="faq-layout"><div class="faq-intro"><div class="eyebrow">A few things you may be wondering</div><h2>'+esc(page['faq_title'])+'</h2><p>Have a question about your home? Talk it through with our team.</p>'+cta('faq-intro')+'</div><div class="faq-list">'+''.join(answers)+'</div></div>')


def local_team(page):
    return section('<div class="split"><div class="local-panel"><img class="van" src="/ppc/assets/company-van.jpg" alt="Becht Pride branding on a company van" width="390" height="285" loading="lazy"><div class="small-label">Your neighbors. Your team.</div><h3>Local, owner-led<br>and proud of it.</h3><p>Serving homeowners across Central Indiana since 2012.</p></div><div class="split-copy"><div class="eyebrow">The Becht Pride difference</div><h2>'+esc(page['why_title'])+'</h2><p>'+esc(page['why_copy'])+'</p>'+checks(page['why_checks'])+cta('why')+'</div></div>','white')


def final_cta(page):
    return '<section class="final-cta" id="final-call"><div class="container"><div class="eyebrow">Your home. Our pride.</div><h2>'+esc(page['final_title'])+'</h2><p>'+esc(page['final_sub'])+'</p>'+cta('final')+'<div class="final-note">Insured &amp; bonded &nbsp; · &nbsp; Free estimates &nbsp; · &nbsp; Serving Central Indiana since 2012</div></div></section>'


def footer(page):
    disclaimer = '<p class="disclaimer">Becht Pride Residential Services is a restoration and repair contractor, not an insurance company or public adjuster. Coverage is determined by your insurance policy.</p>' if page['id']=='insurance' else ''
    return f'<footer class="site-footer"><div class="container"><div class="footer-top"><div><div class="footer-name">Becht Pride Residential Services, LLC</div><p>Indianapolis, IN · Serving Central Indiana</p><p>Office hours: Mon–Fri, 8am–4pm</p></div><a class="footer-phone call-cta" data-cta="footer" href="{TEL}">{PHONE}</a></div>{disclaimer}<div class="footer-bottom"><span>© 2026 Becht Pride Residential Services, LLC. All rights reserved.</span><a href="/ppc-privacy">Privacy policy</a></div></div></footer><aside class="sticky-call" aria-label="Call Becht Pride" aria-hidden="true" inert><p>{esc(page["sticky_note"])}</p>{cta("sticky-mobile",page["sticky_label"])}</aside>'


def remodeling_content(p):
    intro = '<div class="intro-grid"><div><div class="eyebrow">A better remodeling experience</div><h2>Home remodeling contractors who show up. And follow through.</h2></div><div class="intro-copy"><p>A remodel is one of the biggest investments you’ll make in your home. You deserve a clear estimate, a clean job site and a team that keeps you in the loop.</p><p>At Becht Pride, we treat every home as if it were our own — from the first conversation to the final walkthrough.</p>'+cta('painrelief',f'Get your free estimate — {PHONE}',text=True)+'</div></div>'
    columns=[]
    for positive,title,lines in [(False,'The frustrations you want to avoid',['Missed appointments and unanswered calls','Unclear responsibility between trades','Vague quotes and surprise charges','A mess left for you to deal with']),(True,'What to expect with Becht Pride',['Clear communication from start to finish','One point of contact for your project','A detailed, transparent estimate','Respect for your home and a clean job site'])]:
        columns.append(f'<div class="compare-column {"positive" if positive else ""}"><h3>{title}</h3><ul>'+''.join(f'<li>{icon("check" if positive else "cross")}<span>{line}</span></li>' for line in lines)+'</ul></div>')
    intro += '<div class="comparison">'+''.join(columns)+'</div>'
    spotlight = '<div class="split"><figure class="photo-frame">'+picture('shower','Custom tile shower from the Becht Pride project gallery')+'<span class="photo-tag">The details make the difference</span><figcaption>Custom shower tile · Becht Pride project gallery</figcaption></figure><div class="split-copy"><div class="eyebrow">Your everyday, upgraded</div><h2>Bathroom remodeling contractors who see the whole picture.</h2><p>Update a powder room, plan a tub to shower conversion or create a primary bath retreat. We coordinate the details — from plumbing and tile to fixtures and finishing — with one point of contact.</p>'+checks(['Custom tile showers','Tub to shower conversions','Vanities & fixtures','Heated floors','Accessibility upgrades','Full gut renovations'])+cta('bath-spotlight',f'Plan your bathroom remodel — {PHONE}')+'</div></div>'
    gallery=head('Real spaces. Thoughtful details.','Recent remodeling projects in Central Indiana.','A closer look at work from our project gallery.')+'<div class="gallery">'
    for img,title,sub in [('bathroom','A fresh take on the everyday','Bathroom vanity & finishes'),('shower','Built around the details','Custom shower tile'),('flooring','A new foundation for your room','Flooring installation')]:
        gallery+='<figure>'+picture(img,title)+'<figcaption><strong>'+title+'</strong><span>'+sub+'</span></figcaption></figure>'
    gallery+='</div><div class="section-foot">'+cta('gallery',f'Want results like these? Call {PHONE}')+'</div>'
    return section(intro)+services(p)+section(spotlight)+banner('Ready to love your home again?','Start with a free, no-obligation in-home estimate.')+section(gallery,'white')+process('How your remodel works.','A clear plan. Open communication. Pride in every detail.',p['steps'])+reviews(p['id'])+local_team(p)+area(p)+faq(p)


def restoration_content(p):
    urgency=head('Every step starts with a call','Water damage gets worse when it waits.','A burst pipe, failed sump pump or sewage backup can turn your day upside down. We help you move from “what now?” to a clear plan for cleanup and repairs.')
    urgency+='<div class="urgency-grid">'
    for ico,label,title,copy in [('drop','Stop the spread','Extract the water.','Standing water can travel into walls, flooring and hidden spaces.'),('home','Protect your home','Dry the structure.','Moisture left behind needs professional attention, even when a surface looks dry.'),('tools','Get back to normal','Repair and rebuild.','Cleanup is only the beginning. We help put the affected spaces back together.')]:
        urgency+=f'<article class="urgency-card"><div class="small-label">{icon(ico)}{label}</div><h3>{title}</h3><p>{copy}</p></article>'
    urgency+='</div><div class="section-foot">'+cta('urgency',f'Call for restoration help — {PHONE}')+'</div>'
    insurance='<div class="split"><div class="split-copy"><div class="eyebrow">One less thing on your shoulders</div><h2>We work directly with your insurance company.</h2><p>Damage is stressful enough without trying to organize every repair yourself. We document the damage, provide detailed estimates and communicate with your adjuster, so you can focus on your family.</p>'+checks(['Photo & moisture documentation','Detailed, itemized estimates','Communication with your adjuster','Free repair estimates'])+cta('insurance',f'Questions about repairs? Call {PHONE}')+'</div><figure class="photo-frame">'+picture('restoration','Fire-damaged kitchen and restored kitchen shown side by side')+'<figcaption>Fire damage · Restoration through reconstruction</figcaption></figure></div>'
    return section(urgency)+services(p)+banner('Water in your home right now?','Call our Indianapolis team to discuss the damage and the next steps.')+process('Our water damage restoration process.','From the first gallon of water to the final coat of paint.',p['steps'])+section(insurance,'white')+reviews(p['id'])+local_team(p)+area(p)+faq(p)


CHOOSE_ANSWER = 'Your insurer may recommend a contractor. Ask your agent about any contractor-selection requirements in your policy before you decide. Becht Pride can provide a detailed repair estimate and explain how we coordinate the restoration work with your adjuster.'


def insurance_content(p):
    answer='<section class="answer-section" id="choose-contractor"><div class="container"><div class="answer-card"><div class="answer-mark" aria-hidden="true">Q</div><div><h2>Can I choose my own contractor for an insurance claim?</h2><p>'+CHOOSE_ANSWER+'</p>'+cta('answer-choose',f'Talk to us before you decide — {PHONE}',text=True)+'</div></div></div></section>'
    relief='<div class="intro-grid"><div><div class="eyebrow">Repairs are our part of the process</div><h2>Insurance claims are stressful.<br>Your repairs don’t have to be.</h2></div><div class="intro-copy"><p>After a storm, fire or water loss, there’s a lot to take in: damage to your home, a claim to open and an adjuster’s schedule.</p><p>As a local insurance restoration contractor, we document the damage and coordinate the repair work — with one point of contact from mitigation through rebuild.</p>'+cta('problem',f'Get help with repairs — {PHONE}',text=True)+'</div></div><div class="urgency-grid">'
    for ico,title,copy in [('file','Documented.','Photos, moisture readings and itemized repair estimates.'),('phone','Coordinated.','Direct communication with your insurance adjuster.'),('home','Completed.','Cleanup, structural repairs and reconstruction with one team.')]:
        relief+=f'<article class="urgency-card">{icon(ico)}<h3>{title}</h3><p>{copy}</p></article>'
    relief+='</div>'
    before=head('Mitigation through rebuild','From damage to done.','Fire damage, followed by a fresh start.')+'<figure class="before-after">'+picture('restoration','Side-by-side views of a fire-damaged kitchen and a finished kitchen')+'<figcaption class="image-labels"><span>Before · fire damage</span><span>After · reconstruction</span></figcaption></figure><div class="section-foot">'+cta('beforeafter',f'Start your restoration — {PHONE}')+'</div>'
    return answer+section(relief)+process('A contractor that works with insurance companies. Here’s how.','You handle the claim with your insurer. We focus on documenting the damage and getting the repairs right.',p['steps'],True)+services(p)+banner('Just had damage? Let’s talk next steps.','A clear repair estimate. Thorough documentation. One local team.')+local_team(p)+reviews(p['id'])+section(before,'white')+area(p)+faq(p)


PAGES = [
 {
  'id':'remodeling','slug':'ppc-remodeling','default':'home',
  'title':'Bathroom & Kitchen Remodeling Contractors Indianapolis | Becht Pride',
  'description':'Indianapolis home remodeling contractors for bathroom remodels, kitchen remodels, tub to shower conversions and basement finishing. Call (463) 238-4357 for a free estimate.',
  'eyebrow':'Indianapolis homeowners · Trusted since 2012',
  'variants':{
   'home':['Indianapolis Home Remodeling Contractors','Home Remodeling','Bathrooms, kitchens and basements — thoughtfully remodeled by one local team, with a clear plan from the start.'],
   'bathroom':['Bathroom Remodeling in Indianapolis','Bathroom Remodeling','From new vanities to full gut renovations with custom tile showers — one point of contact and up-front pricing.'],
   'bathroom-contractor':['Bathroom Remodeling Contractors You Can Trust','You Can Trust','Insured, bonded and focused on the details — Indianapolis homeowners have trusted Becht Pride since 2012.'],
   'kitchen':['Kitchen Remodeling in Indianapolis','Kitchen Remodeling','Cabinets, countertops, backsplashes, flooring, lighting and layout changes — built around your space and budget.'],
   'shower':['Tub to Shower Conversions in Indianapolis','Tub to Shower','Trade an old tub for a thoughtfully designed walk-in shower, with custom tile and finishes that feel like you.'],
   'basement':['Basement Finishing in Indianapolis','Basement Finishing','Turn your unfinished basement into a family room, guest suite or home office you’ll actually use.']},
  'hero_image':'bathroom','hero_alt':'Blue accent wall, round mirror and new vanity from the Becht Pride bathroom project gallery',
  'photo_label':'A closer look at our work','photo_title':'Your space.<br>Your style. Our pride.','photo_sub':'Bathroom remodel · Becht Pride project gallery',
  'hero_checks':['Free in-home estimates with up-front pricing','One point of contact for your project','Insured & bonded · Respect for your home'],
  'micro':'A free, no-obligation estimate. A good place to start.',
  'header_note':'Free in-home estimates','header_sub':'Let’s talk about your project',
  'trust':[('file','Free estimates'),('shield','Insured & bonded'),('clock','Serving Indy since 2012'),('tools','One point of contact'),('pin','Central Indiana')],
  'services_title':'Bathroom, kitchen & basement remodeling in Indianapolis.',
  'services_sub':'One local team for the rooms you use every day.',
  'cards':[
   ('bathroom','Bathroom Remodel','From new vanities and fixtures to full gut renovations with custom tile showers, heated floors and modern layouts.','bathroom','home','bathroom bathroom-contractor',[]),
   ('shower','Tub to Shower Conversion','Replace a dated tub with a walk-in shower, custom tile and accessibility options designed around your needs.','shower','shower','shower',[]),
   ('kitchen','Kitchen Remodel','Cabinetry, countertops, backsplashes, flooring, lighting and layout changes — built around how your family lives.',None,'kitchen','kitchen',[]),
   ('basement','Basement Finishing','Make room for a family space, guest suite or office, with framing, drywall, flooring, lighting and finishing.',None,'basement','basement',[]),
   ('fullhome','Full-Home Renovations','A coordinated plan for transforming your living space, managed by one local team.','remodeling','home','home',[]),
   ('flooring','Flooring, Paint & Trim','Hardwood, tile, luxury vinyl plank and laminate, plus fresh paint, new trim and finishing details.','flooring','tools','flooring',[])],
  'call_about':{'bathroom':'your bathroom','shower':'your shower','kitchen':'your kitchen','basement':'your basement','fullhome':'your renovation','flooring':'your finishes'},
  'image_alts':{'bathroom':'Bathroom vanity from the Becht Pride project gallery','shower':'Custom shower tile from the Becht Pride project gallery','remodeling':'Interior remodeling inspiration','flooring':'New flooring from the Becht Pride project gallery'},
  'steps':[
   ('Call us','Tell us about your project. We’ll answer your questions and arrange a time to discuss your space.'),
   ('Free in-home consultation','We look at your home and talk through your goals, priorities and budget.'),
   ('Detailed, up-front estimate','A clear scope and transparent pricing, so you know what is included before work begins.'),
   ('Build it right','We coordinate the work, communicate along the way and treat your home with care.'),
   ('Final walkthrough','We review the finished work with you and discuss any details that need attention.')],
  'why_title':'Good craftsmanship starts with people who care.',
  'why_copy':'Since 2012, we’ve helped homeowners across Central Indiana improve their homes. Our restoration and remodeling experience gives us a practical eye for what is behind the walls, as well as the finishes you see every day.',
  'why_checks':['Free in-home estimates','Transparent pricing','One point of contact','Insured & bonded','Clean job sites','Local, owner-led team'],
  'area_title':'Remodeling contractors serving the Indianapolis area.',
  'faq_title':'Remodeling questions, answered.',
  'faq':[
   ('How much does a bathroom remodel cost in Indianapolis?','It depends on the size of the room, layout changes and finishes. We provide a free, detailed estimate with up-front pricing so you can understand the scope before work begins. Call (463) 238-4357.'),
   ('How long does a tub to shower conversion take?','Timing depends on your design, tile selections and any plumbing changes. We’ll discuss a realistic schedule with your estimate and keep you informed throughout the project.'),
   ('Do you handle kitchen remodels from start to finish?','Yes. We coordinate cabinetry, countertops, backsplashes, flooring, lighting and layout changes with one point of contact for the project.'),
   ('Can you finish my basement?','Yes. We help turn unfinished basements into functional living space with framing, drywall, flooring, lighting and trim. We also discuss moisture concerns before finishing the space.'),
   ('Are you insured and bonded?','Yes. Becht Pride Residential Services is insured and bonded.'),
   ('Who will coordinate the different trades?','Our team is your point of contact for coordinating the project. Ask us about the crew and trade arrangements for your specific scope during your consultation.'),
   ('Are estimates really free?','Yes. Call (463) 238-4357 to arrange a free consultation and no-obligation estimate.')],
  'final_title':'Let’s build the space you’ve been picturing.',
  'final_sub':'Bathrooms, kitchens, basements and more. Your next chapter at home starts with a conversation.',
  'sticky_note':'Free, no-obligation estimates · Office hours Mon–Fri, 8am–4pm',
  'sticky_label':'Free estimate — (463) 238-4357',
  'renderer':remodeling_content
 },
 {
  'id':'restoration','slug':'ppc-restoration','default':'water',
  'title':'Water Damage Restoration Indianapolis | Becht Pride',
  'description':'Water damage restoration in Indianapolis. Flooded basement, sewage backup, fire, mold and storm damage repairs. Call Becht Pride at (463) 238-4357.',
  'eyebrow':'Indianapolis’ local restoration team · Since 2012',
  'variants':{
   'water':['Water Damage Restoration in Indianapolis','Water Damage','Water extraction, drying and full repairs — one local team from first call to final walkthrough.'],
   'basement':['Flooded Basement? Let’s Get Your Home Back.','Flooded Basement?','Flooded basement cleanup, structural drying and repairs across Indianapolis and Central Indiana.'],
   'sewage':['Sewage Backup Cleanup in Indianapolis','Sewage Backup','Professional extraction, sanitizing and repairs to help you move forward after a sewage backup.'],
   'fire':['Fire Damage Restoration in Indianapolis','Fire Damage','Board-up, soot and smoke cleanup, odor removal and reconstruction — one team from damage to repairs.'],
   'mold':['Mold Removal & Remediation in Indianapolis','Mold Removal','We identify the moisture source, contain the affected area and plan professional removal and repairs.'],
   'storm':['Storm Damage Repair in Indianapolis','Storm Damage','Emergency tarping, water extraction and restoration after wind, hail and severe weather.']},
  'hero_image':'water','hero_alt':'Floodwater surrounding homes, an illustrative water damage image',
  'photo_label':'Extraction. Drying. Reconstruction.','photo_title':'One call.<br>A clear path forward.','photo_sub':'Water damage · Mitigation through repair',
  'hero_checks':['Water extraction, drying and reconstruction','We work directly with your insurance adjuster','Insured & bonded · Free repair estimates'],
  'micro':'Tell us what happened. Ask about current response availability.',
  'header_note':'Restoration & repair','header_sub':'Talk to our local team',
  'trust':[('drop','Water damage restoration'),('shield','Insured & bonded'),('file','We work with insurance'),('clock','Since 2012'),('pin','Central Indiana')],
  'services_title':'Water damage restoration & emergency cleanup in Indianapolis.',
  'services_sub':'From flooded basements to fire and storm repairs, we help put your home back together.',
  'cards':[
   ('water','Water Damage Restoration','Burst pipes, leaks and appliance failures. Water extraction, structural drying and repairs for the affected areas.','water','drop','water',[]),
   ('basement','Flooded Basement Cleanup','Sump pump failure or heavy rain? Professional extraction, drying and repairs to help you reclaim your basement.',None,'basement','basement',[]),
   ('sewage','Sewage Backup Cleanup','Contaminated water needs professional attention. Removal, antimicrobial treatment, sanitizing and odor control.',None,'drop','sewage',[]),
   ('fire','Fire Damage Restoration','Board-up, soot and smoke cleanup, odor removal and structural repairs after a fire.','fire','home','fire',[]),
   ('mold','Mold Removal','We identify the moisture source, contain the area and remove mold, with treatment to help prevent regrowth.','mold','shield','mold',[]),
   ('storm','Storm Damage Repair','Wind, hail, fallen trees and heavy rain. Tarping, water extraction, drying and complete repairs.','storm','hail','storm',[])],
  'call_about':{'water':'water damage','basement':'your basement','sewage':'sewage cleanup','fire':'fire damage','mold':'mold removal','storm':'storm repairs'},
  'image_alts':{'water':'Flooded residential street illustrating water damage','fire':'Fire-damaged interior illustrating restoration needs','mold':'Mold remediation work','storm':'Storm damage and restoration'},
  'steps':[
   ('You call, we plan','Tell us what happened and where you are. We’ll discuss availability and the next steps for your home.'),
   ('Inspect & document','Moisture meters and inspection tools help find affected areas. We document the damage for your repair estimate.'),
   ('Extract the water','Professional extraction equipment removes standing water from affected spaces.'),
   ('Dry & dehumidify','Air movers and dehumidifiers help dry walls, floors and hidden cavities.'),
   ('Clean & sanitize','Treatment, cleaning and odor-control work address the affected areas.'),
   ('Repair & rebuild','Drywall, flooring and finishes are repaired as part of a coordinated restoration plan.')],
  'why_title':'We don’t just dry your home. We help rebuild it.',
  'why_copy':'We’ve served homeowners across Central Indiana since 2012. Our restoration and remodeling teams help you through cleanup and reconstruction with one point of contact — and a practical understanding of Indianapolis homes.',
  'why_checks':['Mitigation through rebuild','Insurance documentation','Free repair estimates','Insured & bonded','Professional equipment','Local, owner-led team'],
  'area_title':'Water damage restoration in Indy and nearby communities.',
  'faq_title':'Water damage restoration FAQs.',
  'faq':[
   ('How fast can you get to my home?','Call (463) 238-4357 with your location and a description of the damage. Our team can discuss current availability and an arrival estimate. Response times vary with location, conditions and demand.'),
   ('Does homeowners insurance cover water damage?','Coverage depends on your policy and the cause of the damage. Contact your insurance agent for an explanation of your coverage. We can document the damage and provide a detailed repair estimate.'),
   ('What should I do while I wait?','Put safety first. Stay out of floodwater and sewage-contaminated areas. Never handle wet electrical equipment or touch electrical controls while standing in water. Photograph damage only from a safe location. For an immediate threat to life or safety, contact emergency services.'),
   ('Can you clean up a flooded basement?','Yes. We extract standing water, dry the structure, address affected materials and plan repairs to drywall, flooring and finishes.'),
   ('Do you handle sewage backup cleanup?','Yes. Sewage-contaminated areas need professional extraction, cleaning and sanitizing. Keep people and pets away from the affected area while arranging help.'),
   ('Do you also handle fire, mold and storm damage?','Yes. We offer fire damage restoration, mold removal and storm damage repair, from mitigation and cleanup through reconstruction.'),
   ('Do you offer free estimates?','Yes, repair estimates are free. Call (463) 238-4357 to discuss your home.')],
  'final_title':'Get your home back to normal.',
  'final_sub':'Water, fire, mold or storm damage — talk to a local team that can help with the cleanup and the rebuild.',
  'sticky_note':'Water · Fire · Mold · Storm — talk to our team',
  'sticky_label':'Call for help — (463) 238-4357',
  'renderer':restoration_content
 },
 {
  'id':'insurance','slug':'ppc-insurance','default':'insurance',
  'title':'Insurance Restoration & Repair Contractor Indianapolis | Becht Pride',
  'description':'Indianapolis insurance restoration contractor for storm, hail, water and fire damage. Documentation, repair estimates and reconstruction. Call (463) 238-4357.',
  'eyebrow':'Insurance claim repairs · Indianapolis since 2012',
  'variants':{
   'insurance':['Indianapolis Insurance Restoration & Repair Contractor','Insurance Restoration','We document the damage, work directly with your adjuster and coordinate the repairs — from mitigation to the final rebuild.'],
   'works-with-insurance':['The Contractor That Works With Your Insurance Company','Works With Your Insurance','Detailed documentation, clear estimates and communication with your adjuster — so you’re not stuck in the middle.'],
   'storm':['Storm Damage Insurance Claim Contractor in Indianapolis','Storm Damage','Tarping, documentation for your claim and coordinated storm damage repairs.'],
   'hail':['Hail Damage Repair for Your Insurance Claim','Hail Damage Repair','Roof, siding, gutter and window damage — talk to us about an estimate and documentation for your repair needs.'],
   'water':['Water Damage Insurance Claim Help in Indianapolis','Water Damage','Water extraction and drying, thorough damage documentation and complete repairs.'],
   'fire':['Rebuild After Fire Damage — One Team, Start to Finish','Rebuild After Fire Damage','Board-up, smoke and soot cleanup, and reconstruction coordinated with your insurance company.'],
   'choose':['Choosing a Contractor for Your Insurance Claim?','Choosing a Contractor','Get a clear repair estimate and a local team that can walk you through the restoration process.']},
  'hero_image':'restoration','hero_alt':'Side-by-side comparison of a fire-damaged kitchen and a finished kitchen',
  'photo_label':'From the first call to the final detail','photo_title':'The cleanup.<br>The repairs. The rebuild.','photo_sub':'Fire damage · Restoration & reconstruction',
  'hero_checks':['Direct communication with your adjuster','Damage documentation & itemized estimates','Mitigation through full reconstruction'],
  'micro':'Free repair estimates. Clear next steps.',
  'header_note':'Insurance claim repairs','header_sub':'One point of contact',
  'trust':[('file','Insurance coordination'),('shield','Insured & bonded'),('tools','Mitigation through rebuild'),('clock','Since 2012'),('pin','Central Indiana')],
  'services_title':'An insurance repair contractor for the damage you’re facing.',
  'services_sub':'Storm, hail, water or fire — clear documentation and a coordinated repair plan.',
  'cards':[
   ('storm','Storm Damage Insurance Claim Repairs','Wind, fallen trees and severe weather. We help protect your home and document the damage for repairs.','storm','hail','storm',['Tarping & board-up','Tree & debris removal','Wind damage repairs','Structural repairs']),
   ('hail','Hail Damage Repair & Insurance Claims','Hail damage can be easy to miss. Talk to our team about documenting the affected areas and planning repairs.',None,'hail','hail',['Roof damage assessment','Siding & gutter repairs','Window damage','Photo documentation']),
   ('water','Water Damage Insurance Claim Help','Burst pipes, flooding and sewage backups. Extraction, drying and the moisture documentation needed for repair estimates.','water','drop','water',['Water extraction','Structural drying','Moisture documentation','Full repairs']),
   ('fire','Rebuild After Fire Damage','Fire, smoke and firefighting water. We help clean up, restore what can be saved and rebuild the rest.','fire','home','fire',['Board-up & tarping','Smoke & odor cleanup','Contents cleaning','Reconstruction'])],
  'call_about':{'storm':'storm repairs','hail':'hail damage','water':'water repairs','fire':'fire repairs'},
  'image_alts':{'storm':'Storm-damaged property illustrating insurance repair needs','water':'Floodwater illustrating a water damage repair need','fire':'Fire-damaged interior'},
  'steps':[
   ('Call our team','Tell us what happened. We’ll discuss the damage, your location and the work your home may need.'),
   ('Protect the property','We discuss temporary protection such as tarping, board-up or water extraction when appropriate.'),
   ('Inspect & document','Photos, moisture readings and a detailed estimate create a clear record of the repair work.'),
   ('Open your insurance claim','You contact your insurance company to open the claim and ask about your policy and next steps.'),
   ('Coordinate with the adjuster','We provide documentation and repair estimates and communicate about the restoration work.'),
   ('Restore & rebuild','Our team coordinates the agreed repairs, from affected drywall and flooring to reconstruction.'),
   ('Final walkthrough','We review the finished work with you and discuss any remaining details.')],
  'why_title':'A local team, here for the whole repair.',
  'why_copy':'We’ve served Central Indiana since 2012. With restoration and remodeling experience under one roof, we can coordinate cleanup and reconstruction through a single point of contact. You know who to call and who is accountable for the work.',
  'why_checks':['Adjuster communication','Damage documentation','Mitigation through rebuild','Insured & bonded','Free repair estimates','Local, owner-led team'],
  'area_title':'Insurance restoration repairs across the Indianapolis area.',
  'faq_title':'Insurance claim repair FAQs.',
  'faq':[
   ('Can I choose my own contractor for an insurance claim?',CHOOSE_ANSWER),
   ('Do you work with insurance companies?','Yes. We document the damage, prepare a detailed repair estimate and communicate with your adjuster about the restoration work. Your insurer determines coverage under your policy.'),
   ('Should I call my insurance company or a contractor first?','Put immediate safety first. Contact your insurer promptly for claim instructions. If your property needs temporary protection or mitigation, call (463) 238-4357 to discuss the work and current availability.'),
   ('Can you help with my water damage insurance claim?','We provide repair documentation, such as photos, moisture readings and itemized estimates. Your insurance company handles your claim and explains whether your policy covers the cause of the damage.'),
   ('Do you repair hail damage for insurance claims?','We can discuss hail damage affecting roofing, siding, gutters and windows, document the damage and explain the repair options available for your property.'),
   ('Can you rebuild after fire damage?','Yes. Our services include board-up, smoke and soot cleanup, odor removal, contents cleaning and reconstruction.'),
   ('Will you pay or waive my deductible?','No. Your deductible is your responsibility. We provide a repair estimate; your insurer can explain how your deductible and coverage apply to your claim.'),
   ('Do you file the claim for me?','You open the claim with your insurance company. We provide documentation and repair estimates, communicate with your adjuster and keep you informed about the restoration work.')],
  'final_title':'Get your home restored. With less stress.',
  'final_sub':'Storm, hail, water or fire damage — call the Indianapolis team that can help you move from damage to repairs.',
  'sticky_note':'Damage documentation · Repair estimates · Reconstruction',
  'sticky_label':'Talk to our team — (463) 238-4357',
  'renderer':insurance_content
 }
]


def render(page):
    title,highlight,sub = page['variants'][page['default']]
    h1 = esc(title).replace(esc(highlight),f'<span class="highlight">{esc(highlight)}</span>')
    config = json.dumps({k:page[k] for k in ['id','default','variants']},ensure_ascii=False).replace('</','<\\/')
    intent_script = f'''<script>window.bechtLanding={config};(()=>{{const p=window.bechtLanding;const svc=new URLSearchParams(location.search).get('svc');p.matched=Object.prototype.hasOwnProperty.call(p.variants,svc);p.service=p.matched?svc:p.default;document.documentElement.dataset.service=p.service;}})();</script>'''
    hero_script = '''<script>(()=>{const p=window.bechtLanding;const [title,accent,sub]=p.variants[p.service];const el=document.getElementById('hero-title');const at=title.indexOf(accent);if(at>=0){const span=document.createElement('span');span.className='highlight';span.textContent=accent;el.replaceChildren(document.createTextNode(title.slice(0,at)),span,document.createTextNode(title.slice(at+accent.length)));}else el.textContent=title;document.getElementById('hero-sub').textContent=sub;})();</script>'''
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'HomeAndConstructionBusiness','@id':DOMAIN+'/#business','name':'Becht Pride Restoration & Remodeling','legalName':'Becht Pride Residential Services, LLC','url':DOMAIN,'logo':DOMAIN+'/image-assets/Becht_restoration_logo-01.svg','telephone':'+1-463-238-4357','foundingDate':'2012','areaServed':[{'@type':'City','name':name} for name in CITIES],'openingHoursSpecification':{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday'],'opens':'08:00','closes':'16:00'}},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in page['faq']]}
    ]}
    schema['@graph'] += [{'@type':'Service','name':card[1],'provider':{'@id':DOMAIN+'/#business'},'areaServed':'Indianapolis and Central Indiana'} for card in page['cards']]
    trust=''.join(f'<div class="trust-item">{icon(ico)}<span>{esc(label)}</span></div>' for ico,label in page['trust'])
    hero_checks=''.join(f'<li>{icon("check")}<span>{esc(line)}</span></li>' for line in page['hero_checks'])
    header=f'''<a href="#main" class="skip-link">Skip to content</a><div class="utility"><div class="container"><span>Becht Pride · Indianapolis &amp; Central Indiana</span><span>Local, owner-led · Since 2012</span></div></div>
<header class="site-header"><div class="container header-inner"><div class="brand"><img src="/image-assets/Becht_restoration_logo-01.svg" alt="Becht Pride" width="66" height="66"><div class="brand-name">BECHT PRIDE<span>Restoration &amp; Remodeling</span></div></div><div class="header-action"><div class="header-note"><strong>{page['header_note']}</strong>{page['header_sub']}</div><a class="button call-cta" data-cta="header" href="{TEL}" aria-label="Call Becht Pride at {PHONE}">{icon('phone')}<span class="header-call-desktop">{PHONE}</span><span class="header-call-mobile">Call now</span></a></div></div></header>'''
    hero=f'''<main id="main"><section class="hero hero-{page['id']}"><div class="container hero-layout"><div class="hero-copy"><div class="eyebrow">{page['eyebrow']}</div><h1 id="hero-title">{h1}</h1><p class="hero-sub" id="hero-sub">{esc(sub)}</p>{hero_script}<ul class="hero-checks">{hero_checks}</ul>{cta('hero')}<p class="hero-micro">{esc(page['micro'])}</p><div class="hero-proof"><span class="line"></span><span><strong>Your home. Our pride.</strong> &nbsp; Since 2012.</span></div></div><figure class="hero-photo">{picture(page['hero_image'],page['hero_alt'],True)}<figcaption class="hero-photo-caption"><span class="small-label">{page['photo_label']}</span><strong>{page['photo_title']}</strong><p>{page['photo_sub']}</p></figcaption></figure></div></section><div class="trustbar"><div class="container trust-items">{trust}</div></div>'''
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(page['title'])}</title><meta name="description" content="{esc(page['description'])}"><meta name="robots" content="noindex, follow"><meta name="format-detection" content="telephone=no"><meta name="theme-color" content="#1f2569"><link rel="canonical" href="{DOMAIN}/{page['slug']}"><link rel="icon" href="/favicon.png"><link rel="preload" href="/ppc/assets/inter-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/ppc/landing.css">{intent_script}<style>.service-card.matched{{border:2px solid #fff102;box-shadow:0 0 0 2px #fff10240}}</style><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script><script defer src="/ppc/landing.js"></script></head><body data-page="{page['id']}">
<!-- Local review build. See docs/landing-pages.md for unresolved launch confirmations.
CONFIRM: 24/7 phone coverage, service radius, trade arrangements, approved reviews,
Google Ads/CallRail configuration, and privacy policy. Unconfirmed promotional claims
and the unnamed review are omitted. No external tracking script is installed. -->
{header}{hero}{page['renderer'](page)}{final_cta(page)}</main>{footer(page)}</body></html>'''
    (SITE/(page['slug']+'.html')).write_text(html)


if __name__ == '__main__':
    for page in PAGES:
        render(page)
        print('Generated', page['slug']+'.html')

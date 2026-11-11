#!/usr/bin/env python3
"""Builds the Worldbrand Classic Signs static site.

Run:  python3 _build/build.py            (preview build: noindex, GitHub Pages base path)
      python3 _build/build.py --live     (live build for the client's own domain)

All pages are generated from the data below so header/footer/branding stay identical.
Folders starting with "_" are not published by GitHub Pages.
"""
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = '--live' in sys.argv
BASE_404 = '/' if LIVE else '/worldbrand-classic-signs/'
SITE_URL = 'https://www.worldbrandsigns.co.za/' if LIVE else 'https://dionpather-afk.github.io/worldbrand-classic-signs/'

BIZ = {
    'name': 'Worldbrand Classic Signs',
    'short': 'WCS',
    'phone_display': '+27 81 400 2417',
    'phone_tel': '+27814002417',
    'wa': '27814002417',
    'email': 'info@worldbrandsigns.co.za',
    'street': '25 Sedgemoor Pl, Woodlands',
    'city': 'Durban',
    'postal': '4004',
    'region': 'KwaZulu-Natal',
    'reg': '2021/117042/07',
    'est': '2019',
    'facebook': '',  # add the real Facebook page URL when the client supplies it
    'instagram': 'https://www.instagram.com/worldbrandsigns/',
    'tiktok': 'https://www.tiktok.com/@worldbrands1',
}
ADDR_ONE_LINE = f"{BIZ['street']}, {BIZ['city']}, {BIZ['postal']}"
WA_LINK = f"https://wa.me/{BIZ['wa']}?text=" + 'Hi%20Worldbrand%20Classic%20Signs%2C%20I%27d%20like%20a%20quote%20for%20a%20sign.'

e = html.escape

# ------------------------------------------------------------------ icons
ICON = {
 'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm0-21.6A11.8 11.8 0 0 0 1.9 17.9L.2 24l6.3-1.6A11.8 11.8 0 1 0 12 .2z"/></svg>',
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 'fb': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6c0-.9.6-1.1 1-1.1h2.6V1H14c-4 0-4.9 3-4.9 4.9V8H6.6v4h2.5v11H14V12h3.3l.4-4H14z"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1" fill="currentColor"/></svg>',
 'tt': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.6 6.7a4.8 4.8 0 0 1-3.8-4.2V2h-3.4v13.6a2.9 2.9 0 1 1-2-2.7V9.4a6.3 6.3 0 1 0 5.4 6.2V8.7a8.2 8.2 0 0 0 3.8 1.2V6.7z"/></svg>',
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

# ------------------------------------------------------------------ services
SERVICES = [
 {'slug':'3d-fabricated-signs','name':'3D Fabricated Signs','img':'saranos-3d-letters',
  'short':'Raised, built-up letters and logos that jump off the wall — lit or unlit.',
  'intro':'Nothing says “we mean business” like letters you can reach out and touch. We design and fabricate built-up 3D lettering and logos in our workshop, then install them on your shopfront, reception wall or building face. Add face-lit, back-lit or edge-lit LEDs and your brand keeps working after dark.',
  'list':['Built-up channel letters and logos','Face-lit, back-lit (halo) and edge-lit LED options','Acrylic, ACM and painted finishes matched to your brand colours','Shopfront fascias, reception walls and building signage','Full design, fabrication and installation by our own team'],
  'gallery':['phoenix-tyres-install','seaview-liquors-shopfront','saranos-3d-letters','chicken-tikka-3d-letters','fight-club-umhlanga','eikay-entertainment']},
 {'slug':'billboards','name':'Billboards','img':'atlas-battery-shopfront',
  'short':'Big, bold boards that get your message seen from the road.',
  'intro':'When you need to be seen from across the street or down the highway, size matters. We print and install large-format boards and fascia billboards that carry your brand, your offer and your contact details clearly — built to handle Durban sun, wind and rain.',
  'list':['Large-format printed billboard skins','Fascia and roadside boards','Weather-resistant materials and inks','Frame supply, flighting changes and replacements','Design help so your message reads at a glance'],
  'gallery':['atlas-battery-shopfront','durban-bumper-clinic','eikay-entertainment','unicopy-shopfront']},
 {'slug':'pylon-signs','name':'Pylon Signs','img':'bio-tech-pylon',
  'short':'Free-standing pylons, illuminated or non-illuminated, plus flags and wayfinding.',
  'intro':'A pylon is your landmark — the sign people look for from the road or the parking lot. We build illuminated and non-illuminated pylons, directory boards and wayfinding signs, plus telescopic flags for campaigns and forecourts.',
  'list':['Illuminated and non-illuminated pylons','Directory and multi-tenant boards','Wayfinding and information signage','Telescopic and feather flags','Foundations and installation handled for you'],
  'gallery':['bio-tech-pylon-front','ba-ga-mothibi-pylon','frangeros-flags','ba-ga-mothibi-entrance']},
 {'slug':'perspex-signs','name':'Perspex Signs','img':'perception-perspex',
  'short':'Clean, glossy acrylic signs for salons, offices, clinics and stores.',
  'intro':'Perspex (acrylic) gives you that clean, premium finish — glossy colour, crisp edges and plenty of options. From cut-out logos on a feature wall to layered panels and stand-off plaques, perspex is a favourite for salons, offices and retail.',
  'list':['Laser-cut perspex letters and logos','Layered and stand-off panels','Reception and feature-wall signs','Door, office and directional signs','Lit and unlit options'],
  'gallery':['perception-perspex','iphone-drip-install','heart-feature-sign','lotus-shopfront']},
 {'slug':'lightboxes','name':'Lightboxes','img':'cold-meat-deli-lightbox',
  'short':'Glowing boxes and shapes that light up your brand day and night.',
  'intro':'A lightbox turns your logo into a beacon. We build single- and double-sided lightboxes, custom-shaped light signs and projecting signs with energy-efficient LEDs — so your brand glows long after the shop lights go down.',
  'list':['Single- and double-sided lightboxes','Custom-shaped and cut-out light signs','Projecting (blade) signs','Energy-efficient LED illumination','Fabricated and tested in our workshop'],
  'gallery':['cold-meat-deli-lightbox','atlas-battery-shopfront','bull-skull-lightbox','lightbox-fabrication','prince-wholesalers-night']},
 {'slug':'digital-printing','name':'Digital Printing','img':'gatti-window-branding',
  'short':'Window graphics, banners, flags, posters and printed branding.',
  'intro':'Sharp colour, big or small. We digitally print window graphics, vinyl decals, banners, flags, posters and promotional branding — and we install it too, so it goes up straight and stays up.',
  'list':['Window graphics and frosting','Vinyl decals and stickers','Banners, flags and posters','Promotional and event branding','Design, print and installation'],
  'gallery':['gatti-window-branding','frangeros-flag-closeup','the-image-salon-shopfront']},
 {'slug':'wallpaper','name':'Wallpaper & Wall Branding','img':'pizza-hut-wall-install',
  'short':'Custom printed wallpaper and wall murals that set the mood.',
  'intro':'Your walls can tell your brand story. We print custom wallpaper and wall graphics — murals, feature walls and branded interiors — for restaurants, salons, offices and retail spaces.',
  'list':['Custom printed wallpaper','Feature walls and murals','Branded interiors for stores and restaurants','Office and reception wall graphics','Professional surface prep and installation'],
  'gallery':['pizza-hut-wall-install','the-image-salon-interior','market-fresh-interior']},
 {'slug':'vehicle-branding','name':'Vehicle Branding','img':'hydraulics-van-branding',
  'short':'Turn your bakkie, van or fleet into a moving billboard.',
  'intro':'Your vehicle is on the road every day — make it work for you. We design and apply vehicle branding from simple door decals to full fleet branding, using quality vinyl that looks sharp and lasts.',
  'list':['Full and partial vehicle wraps','Door and window decals','Fleet branding for vans and bakkies','Custom decals and pinstripes','Design and professional application'],
  'gallery':['hydraulics-van-branding','amg-vehicle-decal']},
]

# ------------------------------------------------------------------ projects (all real, from the company profile)
PROJECTS = [
 ('bio-tech-pylon','Bio Tech Fuel & Gas','Forecourt pylon sign','pylon illuminated'),
 ('phoenix-tyres-install','Phoenix Tyres','Illuminated 3D letters — installation','3d illuminated'),
 ('atlas-battery-shopfront','Atlas Battery','Fascias, lightboxes & roadside board','shopfront illuminated'),
 ('seaview-liquors-shopfront','Seaview Liquors','3D letters & shaped bottle sign','3d shopfront'),
 ('pizza-hut-malvern','Pizza Hut','KwaZulu-Natal','3d illuminated shopfront'),
 ('saranos-3d-letters','Saranos','3D fabricated letters','3d'),
 ('prince-wholesalers-night','Prince Wholesalers','Illuminated signage','3d illuminated'),
 ('ba-ga-mothibi-pylon','Ba-Ga Mothibi Community Health Centre','North West Province','pylon'),
 ('iphone-drip-illuminated','iPhone Drip','Illuminated 3D letters','3d illuminated'),
 ('fight-club-umhlanga','Fight Club','Umhlanga','3d shopfront'),
 ('cold-meat-deli-lightbox','Cold Meat Deli','Round lightbox','illuminated'),
 ('chicken-tikka-3d-letters','Chicken Tikka & Schwarma','3D letters before install','3d'),
 ('the-image-salon-shopfront','The Image Salon','Shopfront & print','shopfront print'),
 ('hydraulics-van-branding','Hydraulics (Jacobs) cc','Van branding','vehicle'),
 ('perception-perspex','Perception Hair, Beauty & Aesthetic','Perspex sign','3d shopfront'),
 ('frangeros-flags','Frangeros','Telescopic flags','pylon print'),
 ('bull-skull-lightbox','Custom bull-skull light sign','Lightbox','illuminated'),
 ('revival-ministries-illuminated','Revival Ministries','Illuminated letters','3d illuminated'),
 ('gatti-window-branding','Gatti Ice Cream','Window branding','print shopfront'),
 ('pizza-hut-wall-install','Pizza Hut','Wall branding install','print'),
 ('unicopy-shopfront','UniCopy','Shopfront signage','shopfront'),
 ('lotus-shopfront','Lotus — Fresh Produce & Prayer Goods','Shopfront signage','shopfront 3d'),
 ('amg-vehicle-decal','AMG decal','Vehicle decal','vehicle'),
 ('eikay-entertainment','Eikay Entertainment','3D letters','3d shopfront'),
 ('frozen-foods-illuminated','Frozen Foods','Illuminated in-store sign','illuminated'),
 ('market-fresh-interior','Market Fresh','In-store branding','print'),
 ('gillitts-pharmacy','Gillitts Pharmacy','Shopfront signage','shopfront'),
 ('heart-feature-sign','Heart feature sign','Custom fabrication','3d'),
 ('durban-bumper-clinic','Durban Bumper Clinic','Fascia board','shopfront print'),
 ('iphone-drip-install','iPhone Drip','Installation in progress','3d'),
 ('the-image-salon-interior','The Image Salon','Illuminated interior','illuminated'),
 ('fight-club-workshop','Fight Club','Letters in our workshop','3d'),
 ('lightbox-fabrication','Lightbox fabrication','In our workshop','illuminated'),
 ('frangeros-flag-closeup','Frangeros','Printed flag','print'),
]
FILTERS = [('all','All work'),('3d','3D & Perspex'),('illuminated','Illuminated'),('shopfront','Shopfronts'),('print','Print & Wallpaper'),('pylon','Pylons & Flags'),('vehicle','Vehicles')]

CLIENTS = [
 ('Pizza Hut','5 KZN outlets'),('Department of Health','North West Provincial Government'),('Prince Wholesalers','Health & Beauty'),
 ('Saranos','Pizza · Pasta · Chicken'),('Frangeros','Flags & branding'),('UniCopy','Shopfront'),
 ('Lotus','Fresh Produce · Prayer Goods'),("Sultan's",'Pizza · Pasta · Grills'),("The Original Govender's",'Curry Kitchen'),
 ('Durban Schwarma','Signage'),('Hydraulics (Jacobs) cc','Vehicle branding'),
 ('Bio Tech Fuel & Gas','Forecourt pylon'),('Phoenix Tyres','Illuminated 3D letters'),('Atlas Battery','Fascias & roadside board'),('Seaview Liquors','3D shopfront sign'),
]
BRANDS_MARQUEE = ['Pizza Hut','Bio Tech Fuel & Gas','Phoenix Tyres','Atlas Battery','Seaview Liquors','Prince Wholesalers','Saranos','Frangeros','UniCopy','Lotus',"Sultan's","Govender's",'Durban Schwarma','Fight Club','The Image Salon','Gatti Ice Cream','Eikay Entertainment','Market Fresh','Gillitts Pharmacy','Durban Bumper Clinic','iPhone Drip','Perception','Revival Ministries','Hydraulics (Jacobs) cc']

# DEMO testimonials — placeholders until the client supplies real reviews (see README).
TESTIMONIALS = [
 ('Our new 3D sign changed the whole look of the shop. People stop and take photos of it at night!','Restaurant owner','Durban'),
 ('They handled everything — design, building and installation. On time and exactly what we asked for.','Retail store manager','KwaZulu-Natal'),
 ('Professional team, fair price, and the lightbox still looks brand new. Highly recommended.','Salon owner','Durban'),
]

NAV = [('index.html','Home'),('about.html','About'),('services.html','Services'),('projects.html','Projects'),('clients.html','Clients'),('contact.html','Contact')]

# ------------------------------------------------------------------ layout
def head(title, desc, page, base=None):
    t = f"{title} | {BIZ['name']}" if page != 'index.html' else f"{BIZ['name']} — 3D Signs, Lightboxes & Branding in Durban"
    robots = '<meta name="robots" content="index,follow">' if LIVE else '<meta name="robots" content="noindex,nofollow">'
    canon = SITE_URL + ('' if page == 'index.html' else page)
    base_tag = f'<base href="{base}">' if base else ''
    csp = ("default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
           "font-src 'self'; script-src 'self'; frame-src https://www.google.com https://maps.google.com; "
           "connect-src 'self'; base-uri 'self'; form-action 'none'; object-src 'none'")
    return f'''<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{base_tag}
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{e(t)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#050507">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}assets/img/og-image.jpg">
<meta property="og:url" content="{canon}">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/anton-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(page):
    cur = ' aria-current="page"'
    items = ''.join(
        '<li><a href="%s"%s>%s</a></li>' % (href, cur if (href == page or (href == 'services.html' and page.startswith('svc:'))) else '', label)
        for href, label in NAV)
    return f'''<header class="site-header">
 <nav class="wrap nav" aria-label="Main">
  <a class="brand" href="index.html" aria-label="{BIZ['name']} home">
   <img src="assets/img/wcs-logo.png" alt="WCS — World Brand Classic Signs logo" width="72" height="58">
   <span>Worldbrand<small>CLASSIC SIGNS</small></span>
  </a>
  <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links"><span></span></button>
  <ul class="nav-links" id="nav-links">{items}<li><a class="btn" href="quote.html">Get a Quote</a></li></ul>
 </nav>
</header>
<main id="main">
'''

def footer():
    svc = ''.join(f'<li><a href="{s["slug"]}.html">{e(s["name"])}</a></li>' for s in SERVICES)
    return f'''</main>
<footer class="site-footer">
 <div class="wrap">
  <div class="foot-grid">
   <div class="foot-brand">
    <img src="assets/img/wcs-logo.png" alt="WCS logo" width="150" height="122" loading="lazy">
    <p>Custom signs designed, fabricated and installed in Durban since {BIZ['est']}. Your signs, our expertise — making a statement that stands out.</p>
    <div class="socials">
     <a href="{BIZ['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ICON['ig']}</a>
     <a href="{BIZ['tiktok']}" target="_blank" rel="noopener" aria-label="TikTok">{ICON['tt']}</a>
    </div>
   </div>
   <div><h4>Services</h4><ul>{svc}</ul></div>
   <div><h4>Explore</h4><ul>
    <li><a href="about.html">About us</a></li><li><a href="projects.html">Projects</a></li><li><a href="clients.html">Clients</a></li>
    <li><a href="quote.html">Get a quote</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy policy</a></li></ul></div>
   <div><h4>Get in touch</h4><ul>
    <li><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></li>
    <li><a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp us</a></li>
    <li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
    <li><span style="color:var(--muted);font-size:.95rem">{e(ADDR_ONE_LINE)}<br>{BIZ['region']}</span></li></ul></div>
  </div>
  <div class="foot-bottom">
   <span>© <span id="year">2026</span> {BIZ['name']} · Reg. No. {BIZ['reg']}</span>
   <span>Website by <a href="https://talentlearnconsult.com" target="_blank" rel="noopener">Talent Learn Consult</a></span>
  </div>
 </div>
</footer>
<a class="wa-float" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{ICON['wa']}</a>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def page_hero(title_html, lead, img, crumbs):
    c = ' / '.join(f'<a href="{h}">{e(l)}</a>' if h else e(l) for h, l in crumbs)
    return f'''<section class="page-hero">
 <div class="hero-bg" style="background-image:url('assets/img/{img}.jpg')"></div>
 <div class="wrap">
  <p class="crumbs">{c}</p>
  <h1>{title_html}</h1>
  <p class="lead" style="margin-top:1.2rem">{lead}</p>
 </div>
</section>
'''

def cta(title='Ready to light up your brand?', text='Tell us what you need — we\'ll come back with ideas and a quote.'):
    return f'''<section class="section-tight"><div class="wrap">
 <div class="cta reveal">
  <p class="eyebrow">Let's talk signs</p>
  <h2 class="chrome">{title}</h2>
  <p class="lead" style="margin:0 auto">{text}</p>
  <div class="btn-row">
   <a class="btn" href="quote.html">Get a free quote {ICON['arrow']}</a>
   <a class="btn btn-lime" href="{WA_LINK}" target="_blank" rel="noopener">{ICON['wa']} WhatsApp us</a>
  </div>
 </div>
</div></section>
'''

def svc_card(s):
    return f'''<a class="card svc-card reveal" href="{s['slug']}.html">
 <div class="ph"><img src="assets/img/{s['img']}.jpg" alt="{e(s['name'])} by Worldbrand Classic Signs" loading="lazy"></div>
 <div class="body"><h3>{e(s['name'])}</h3><p>{e(s['short'])}</p><span class="more">Explore →</span></div>
</a>'''

def figure(img, title, sub, cats):
    return f'''<figure data-cat="{cats}"><img src="assets/img/{img}.jpg" alt="{e(title)} — {e(sub)}" loading="lazy"><figcaption><small>{e(sub)}</small>{e(title)}</figcaption></figure>'''

LIGHTBOX = '''<div class="lightbox" role="dialog" aria-modal="true" aria-label="Project photo">
 <button class="lb-btn lb-close" aria-label="Close">✕</button>
 <button class="lb-btn lb-prev" aria-label="Previous photo">‹</button>
 <img src="assets/img/wcs-logo.png" alt="">
 <button class="lb-btn lb-next" aria-label="Next photo">›</button>
 <p></p>
</div>'''

STEPS = '''<div class="steps">
 <div class="step reveal"><h3>Design</h3><p>Collaborative design sessions to craft a concept that tells your brand's story.</p></div>
 <div class="step reveal"><h3>Fabricate</h3><p>Skilled artisans in our workshop build your sign with meticulous attention to detail.</p></div>
 <div class="step reveal"><h3>Install</h3><p>Seamless, safe installation — positioned for maximum impact.</p></div>
 <div class="step reveal"><h3>Support</h3><p>Open communication throughout, and we're here after the lights go on.</p></div>
</div>'''

def jsonld():
    data = {
        "@context":"https://schema.org","@type":"LocalBusiness","name":BIZ['name'],
        "image":SITE_URL+"assets/img/og-image.jpg","url":SITE_URL,"telephone":BIZ['phone_tel'],"email":BIZ['email'],
        "foundingDate":BIZ['est'],
        "address":{"@type":"PostalAddress","streetAddress":BIZ['street'],"addressLocality":BIZ['city'],"postalCode":BIZ['postal'],"addressRegion":BIZ['region'],"addressCountry":"ZA"},
        "areaServed":"South Africa","sameAs":[BIZ['instagram'],BIZ['tiktok']],
        "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s['name']}} for s in SERVICES]}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>'

# ------------------------------------------------------------------ pages
def page_home():
    marquee = ''.join(f'<span>{e(b)}</span>' for b in BRANDS_MARQUEE) * 2
    featured = [p for p in PROJECTS if p[0] in ('bio-tech-pylon','phoenix-tyres-install','pizza-hut-malvern','atlas-battery-shopfront','seaview-liquors-shopfront','prince-wholesalers-night','iphone-drip-illuminated','ba-ga-mothibi-pylon','cold-meat-deli-lightbox')]
    tests = ''.join(f'''<div class="card quote-card reveal"><div class="stars">★★★★★</div><blockquote>“{e(q)}”</blockquote><p class="who">{e(w)}<small>{e(l)}</small></p></div>''' for q, w, l in TESTIMONIALS)
    body = f'''
<section class="hero">
 <div class="hero-bg" style="background-image:url('assets/img/prince-wholesalers-night.jpg')"></div>
 <div class="wrap hero-grid">
  <div>
   <p class="eyebrow">Durban · Est. {BIZ['est']}</p>
   <h1><span class="chrome">Signs that make<br>the street look twice</span><span class="neon flicker">your brand, lit up.</span></h1>
   <p class="lead">3D fabricated signs, lightboxes, pylons, billboards, wallpaper and vehicle branding — designed, built in our workshop and installed by our own team.</p>
   <div class="btn-row">
    <a class="btn" href="quote.html">Get a free quote {ICON['arrow']}</a>
    <a class="btn btn-ghost" href="projects.html">See our work</a>
   </div>
   <div class="hero-meta">
    <span><i class="dot"></i><b>Design</b> → <b>Build</b> → <b>Install</b></span>
    <span><i class="dot"></i>Trusted by <b>Pizza Hut</b> &amp; <b>Dept. of Health</b></span>
   </div>
  </div>
  <div class="hero-logo">
   <span class="open-sign" aria-hidden="true">Open</span>
   <img src="assets/img/wcs-logo.png" alt="Worldbrand Classic Signs neon logo" width="440" height="357">
  </div>
 </div>
</section>

<div class="marquee" aria-label="Brands we have worked with"><div class="marquee-track">{marquee}</div></div>

<section>
 <div class="wrap">
  <div class="section-head center reveal">
   <p class="eyebrow">What we make</p>
   <h2 class="chrome">Signage solutions that get noticed</h2>
   <p class="lead">From concept to installation, we elevate your brand visibility with innovative, tailored sign solutions that captivate and communicate.</p>
  </div>
  <div class="grid g4">{''.join(svc_card(s) for s in SERVICES)}</div>
 </div>
</section>

<section class="alt section-tight">
 <div class="wrap stats">
  <div class="stat reveal"><b>{BIZ['est']}</b><span>Established</span></div>
  <div class="stat reveal"><b>5</b><span>Pizza Hut outlets branded</span></div>
  <div class="stat reveal"><b>2</b><span>Provinces · KZN &amp; North West</span></div>
  <div class="stat reveal"><b>8</b><span>Sign services under one roof</span></div>
 </div>
</section>

<section>
 <div class="wrap">
  <div class="section-head reveal">
   <p class="eyebrow">Featured work</p>
   <h2 class="chrome">Lit up &amp; looking good</h2>
  </div>
  <div class="gallery">{''.join(figure(*p) for p in featured)}</div>
  <div class="btn-row" style="justify-content:center"><a class="btn btn-lime" href="projects.html">View all projects {ICON['arrow']}</a></div>
 </div>
</section>

<section class="alt">
 <div class="wrap split">
  <div class="reveal">
   <p class="eyebrow">Who we are</p>
   <h2 class="chrome">Where creativity meets craftsmanship</h2>
   <p class="lead" style="margin-top:1.2rem">We specialise in designing and crafting custom signs that leave a lasting impression. From eye-catching storefront displays to personalised 3-dimensional signs, we bring your vision to life with precision and flair.</p>
   <ul class="ticks">
    <li>In-house design, fabrication and installation</li>
    <li>Small or large scale — one shop or a whole chain</li>
    <li>Cost-effective solutions without cutting corners</li>
   </ul>
   <div class="btn-row"><a class="btn" href="about.html">About us {ICON['arrow']}</a></div>
  </div>
  <div class="media-frame reveal"><img src="assets/img/iphone-drip-illuminated.jpg" alt="Illuminated 3D iPhone Drip sign" loading="lazy"></div>
 </div>
</section>

<section>
 <div class="wrap">
  <div class="section-head center reveal"><p class="eyebrow">How it works</p><h2 class="chrome">From idea to glowing sign</h2></div>
  {STEPS}
 </div>
</section>

<section class="alt">
 <div class="wrap">
  <div class="section-head center reveal"><p class="eyebrow">Kind words</p><h2 class="chrome">What clients say <span class="demo-chip">Demo content</span></h2>
  <p class="lead">Sample reviews for this preview — to be replaced with real client reviews.</p></div>
  <div class="grid g3">{tests}</div>
 </div>
</section>
{cta()}
{jsonld()}
'''
    return ('index.html', 'Home', 'Worldbrand Classic Signs, Durban: 3D fabricated signs, lightboxes, pylons, billboards, perspex signs, digital printing, wallpaper and vehicle branding. Designed, built and installed.', body)

def page_about():
    body = page_hero('<span class="chrome">About</span> <span class="neon">us</span>',
        'Welcome to our sign company, where creativity meets craftsmanship. Your signs, our expertise — making a statement that stands out.',
        'fight-club-umhlanga', [('index.html','Home'),('','About')]) + f'''
<section>
 <div class="wrap split">
  <div class="reveal">
   <p class="eyebrow">Who are we?</p>
   <h2 class="chrome">We provide signage solutions</h2>
   <p class="lead" style="margin-top:1.2rem">We specialise in designing and crafting custom signs that leave a lasting impression. From eye-catching storefront displays to personalised 3-dimensional signs, we bring your vision to life with precision and flair.</p>
   <p style="margin-top:1rem">Empowering businesses with impactful signage solutions — from concept to installation, we elevate your brand visibility with innovative and tailored sign solutions that captivate and communicate. Your success, our signage expertise.</p>
  </div>
  <div class="media-frame reveal"><img src="assets/img/chicken-tikka-3d-letters.jpg" alt="3D letters fabricated by Worldbrand Classic Signs" loading="lazy"></div>
 </div>
</section>

<section class="alt">
 <div class="wrap split">
  <div class="media-frame reveal"><img src="assets/img/prince-wholesalers-night.jpg" alt="Prince Wholesalers illuminated signage at night" loading="lazy"></div>
  <div class="reveal">
   <p class="eyebrow">Our commitment</p>
   <h2 class="chrome">The best signage expertise &amp; service</h2>
   <p style="margin-top:1.2rem">Dedicated to exceeding expectations, our team is committed to providing unparalleled signage expertise and service — so every project is cost-effective and successful.</p>
   <p style="margin-top:1rem">We work closely with clients to understand their unique needs. From concept to seamless execution, we take pride in delivering signage that doesn't just meet your expectations — it exceeds them. Your project's success is our goal, and we're here to make your vision a reality with precision and excellence.</p>
  </div>
 </div>
</section>

<section>
 <div class="wrap">
  <div class="section-head center reveal"><p class="eyebrow">We believe in and promote</p><h2 class="chrome">Quality delivery</h2></div>
  <div class="grid g3">
   <div class="card reveal"><span class="num">01</span><h3>Our Vision</h3><p>Revolutionising visual communication — crafting innovative and impactful signage solutions that redefine standards and elevate brands.</p></div>
   <div class="card reveal"><span class="num">02</span><h3>Our Mission</h3><p>Empowering businesses with dynamic signage — delivering visually compelling and effective signs that contribute to our clients' success through creativity and precision.</p></div>
   <div class="card reveal"><span class="num">03</span><h3>Our Values</h3><p>Creativity, integrity and client satisfaction. We prioritise ethical standards, collaboration and passion, fostering lasting client relationships.</p></div>
  </div>
 </div>
</section>

<section class="alt">
 <div class="wrap split">
  <div class="reveal">
   <p class="eyebrow">Our capacity</p>
   <h2 class="chrome">Small job or big rollout</h2>
   <p class="lead" style="margin-top:1.2rem">Equipped with a workshop and a skilled team, we meet diverse signage needs with efficiency and precision — whether it's a single shopfront or a multi-site rollout like our five Pizza Hut outlets across KwaZulu-Natal.</p>
   <ul class="ticks">
    <li>Established {BIZ['est']} · Reg. No. {BIZ['reg']}</li>
    <li>Based in Woodlands, Durban</li>
    <li>Projects delivered in KwaZulu-Natal and the North West Province</li>
   </ul>
  </div>
  <div class="media-frame reveal"><img src="assets/img/lightbox-fabrication.jpg" alt="Lightbox being fabricated in the workshop" loading="lazy"></div>
 </div>
</section>

<section><div class="wrap"><div class="section-head center reveal"><p class="eyebrow">How we work</p><h2 class="chrome">Design · Fabricate · Install</h2></div>{STEPS}</div></section>
{cta()}
'''
    return ('about.html','About','About Worldbrand Classic Signs — a Durban sign company where creativity meets craftsmanship. Our vision, mission, values and capacity.', body)

def page_services():
    body = page_hero('<span class="chrome">Our</span> <span class="neon">services</span>',
        'Our services start with collaborative design sessions, then skilled artisans bring the vision to life in our workshop, and we finish with a seamless installation that positions your sign for maximum impact.',
        'revival-ministries-illuminated', [('index.html','Home'),('','Services')]) + f'''
<section><div class="wrap"><div class="grid g4">{''.join(svc_card(s) for s in SERVICES)}</div></div></section>
<section class="alt"><div class="wrap"><div class="section-head center reveal"><p class="eyebrow">Our process</p><h2 class="chrome">One team, start to finish</h2></div>{STEPS}</div></section>
{cta()}
'''
    return ('services.html','Services','Signage services in Durban: 3D fabricated signs, billboards, pylons, perspex signs, lightboxes, digital printing, wallpaper and vehicle branding.', body)

def page_service(s):
    others = [x for x in SERVICES if x['slug'] != s['slug']][:4]
    gal = ''.join(f'<figure data-cat="all"><img src="assets/img/{g}.jpg" alt="{e(s["name"])} example" loading="lazy"><figcaption><small>{e(s["name"])}</small>Our work</figcaption></figure>' for g in s['gallery'])
    items = ''.join(f'<li>{e(i)}</li>' for i in s['list'])
    body = page_hero(f'<span class="chrome">{e(s["name"])}</span>', e(s['short']), s['img'],
        [('index.html','Home'),('services.html','Services'),('',s['name'])]) + f'''
<section>
 <div class="wrap split">
  <div class="reveal">
   <p class="eyebrow">{e(s['name'])}</p>
   <h2 class="chrome">Built to be seen</h2>
   <p class="lead" style="margin-top:1.2rem">{e(s['intro'])}</p>
   <ul class="ticks">{items}</ul>
   <div class="btn-row"><a class="btn" href="quote.html?service={s['slug']}">Quote me for this {ICON['arrow']}</a></div>
  </div>
  <div class="media-frame reveal"><img src="assets/img/{s['img']}.jpg" alt="{e(s['name'])} by Worldbrand Classic Signs" loading="lazy"></div>
 </div>
</section>
<section class="alt">
 <div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Related work</p><h2 class="chrome">From our portfolio</h2></div>
  <div class="gallery">{gal}</div>
 </div>
</section>
<section>
 <div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">More services</p><h2 class="chrome">You might also need</h2></div>
  <div class="grid g4">{''.join(svc_card(o) for o in others)}</div>
 </div>
</section>
{cta(f"Let's build your {e(s['name'].lower())}")}
{LIGHTBOX}
'''
    return (f"{s['slug']}.html", s['name'], f"{s['name']} in Durban by Worldbrand Classic Signs — {s['short']}", body, 'svc:')

def page_projects():
    filters = ''.join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{e(l)}</button>' for k, l in FILTERS)
    body = page_hero('<span class="chrome">Our</span> <span class="neon">projects</span>',
        'Our projects epitomise innovation and excellence. Diverse in scope and meticulous in execution, each one reflects our commitment to quality.',
        'pizza-hut-fascia', [('index.html','Home'),('','Projects')]) + f'''
<section>
 <div class="wrap">
  <div class="case reveal">
   <div class="case-media">
    <img src="assets/img/pizza-hut-malvern.jpg" alt="Pizza Hut storefront signage" loading="lazy">
    <img src="assets/img/pizza-hut-fascia.jpg" alt="Pizza Hut fascia sign" loading="lazy">
    <img src="assets/img/pizza-hut-outlet.jpg" alt="Pizza Hut outlet sign" loading="lazy">
   </div>
   <div>
    <p class="eyebrow">Case study</p>
    <h2 class="chrome">Pizza Hut</h2>
    <p class="lead" style="margin-top:1rem">We branded five Pizza Hut outlets in KwaZulu-Natal — Malvern, Bluff, Glenwood, Amanzimtoti and Scottburgh.</p>
    <p style="margin-top:1rem">Vibrant, appetising visuals that draw customers in. From strategic placement to eye-catching design, the signage enhances the Pizza Hut experience and builds brand recognition on every street.</p>
    <div class="tags"><span>Illuminated 3D letters</span><span>Fascia signage</span><span>Wall branding</span><span>Multi-site rollout</span></div>
   </div>
  </div>
  <div class="case rev reveal">
   <div class="case-media">
    <img src="assets/img/ba-ga-mothibi-entrance.jpg" alt="Ba-Ga Mothibi Community Health Centre entrance sign" loading="lazy">
    <img src="assets/img/ba-ga-mothibi-pylon.jpg" alt="Ba-Ga Mothibi information pylon" loading="lazy">
    <img src="assets/img/ba-ga-mothibi-building.jpg" alt="Ba-Ga Mothibi building signage" loading="lazy">
   </div>
   <div>
    <p class="eyebrow">Case study · Government</p>
    <h2 class="chrome">Ba-Ga Mothibi Community Health Centre</h2>
    <p class="lead" style="margin-top:1rem">For the North West Department of Health, we branded the Ba-Ga Mothibi Community Health Centre in Sekhing Village, North West Province.</p>
    <p style="margin-top:1rem">Clear wayfinding signs improve the patient experience and informative displays promote health awareness — creating a welcoming, efficient environment that builds trust within the community.</p>
    <div class="tags"><span>Entrance signage</span><span>Information pylon</span><span>Wayfinding</span><span>Public sector</span></div>
   </div>
  </div>
 </div>
</section>
<section class="alt">
 <div class="wrap">
  <div class="section-head center reveal"><p class="eyebrow">Gallery</p><h2 class="chrome">Other projects</h2></div>
  <div class="filters" role="group" aria-label="Filter projects">{filters}</div>
  <div class="gallery">{''.join(figure(*p) for p in PROJECTS)}</div>
 </div>
</section>
{cta('Want your brand up here next?')}
{LIGHTBOX}
'''
    return ('projects.html','Projects','Signage projects by Worldbrand Classic Signs — Pizza Hut KZN, Ba-Ga Mothibi Community Health Centre, Prince Wholesalers, Saranos and more.', body)

def page_clients():
    wall = ''.join(f'<div class="client reveal">{e(n)}<small>{e(s)}</small></div>' for n, s in CLIENTS)
    others = ''.join(f'<span>{e(b)}</span>' for b in BRANDS_MARQUEE) * 2
    body = page_hero('<span class="chrome">Our</span> <span class="neon">clients</span>',
        "In our clients' success stories, our role is pivotal. Tailoring solutions to their unique needs, we've elevated brands, increased visibility and forged lasting partnerships.",
        'unicopy-shopfront', [('index.html','Home'),('','Clients')]) + f'''
<section>
 <div class="wrap">
  <div class="section-head center reveal"><p class="eyebrow">Proud to work with</p><h2 class="chrome">Brands that trust us</h2>
  <p class="lead">From national franchises to provincial government and local favourites.</p></div>
  <div class="client-wall">{wall}</div>
 </div>
</section>
<div class="marquee" aria-label="More brands we have signed"><div class="marquee-track">{others}</div></div>
<section>
 <div class="wrap center reveal" style="max-width:820px">
  <div class="tube"></div>
  <p class="lead" style="margin:2rem auto">Our journey is defined by client success, innovative projects and unwavering commitment. As we continue to exceed expectations, we invite you to be part of the next chapter — where your vision meets our expertise.</p>
  <div class="tube lime"></div>
 </div>
</section>
{cta('Join the brands that glow')}
'''
    return ('clients.html','Clients','Clients of Worldbrand Classic Signs including Pizza Hut, the North West Department of Health, Prince Wholesalers, Saranos, Frangeros and UniCopy.', body)

def page_quote():
    opts = ''.join(f'<option value="{e(s["name"])}" data-slug="{s["slug"]}">{e(s["name"])}</option>' for s in SERVICES)
    body = page_hero('<span class="chrome">Get a</span> <span class="neon">quote</span>',
        'Tell us about your sign. Hit send and your details open in WhatsApp, ready to go to our team — attach your logo or a photo of the site there.',
        'iphone-drip-install', [('index.html','Home'),('','Get a quote')]) + f'''
<section>
 <div class="wrap split" style="align-items:start">
  <form class="form card reveal" data-wa="*New quote request — website*" novalidate>
   <div class="row">
    <div><label for="q-name">Your name <span class="req">*</span></label><input id="q-name" name="name" data-label="Name" autocomplete="name" required></div>
    <div><label for="q-company">Business name</label><input id="q-company" name="company" data-label="Business" autocomplete="organization"></div>
   </div>
   <div class="row">
    <div><label for="q-phone">Phone / WhatsApp <span class="req">*</span></label><input id="q-phone" name="phone" type="tel" data-label="Phone" autocomplete="tel" required></div>
    <div><label for="q-email">Email</label><input id="q-email" name="email" type="email" data-label="Email" autocomplete="email"></div>
   </div>
   <div><label for="q-service">What do you need? <span class="req">*</span></label>
    <select id="q-service" name="service" data-label="Service" required><option value="">Choose a sign type…</option>{opts}<option value="Not sure — need advice">Not sure — need advice</option></select></div>
   <div><label>Illuminated?</label>
    <div class="choice" name="lit" data-label="Illuminated">
     <label><input type="radio" name="lit" value="Yes, lit"> Yes, lit</label>
     <label><input type="radio" name="lit" value="No, not lit"> No</label>
     <label><input type="radio" name="lit" value="Not sure"> Not sure</label>
    </div></div>
   <div class="row">
    <div><label for="q-size">Approximate size</label><input id="q-size" name="size" data-label="Size" placeholder="e.g. 3m x 0.8m"></div>
    <div><label for="q-location">Install location</label><input id="q-location" name="location" data-label="Location" placeholder="Suburb / city"></div>
   </div>
   <div><label for="q-when">When do you need it?</label>
    <select id="q-when" name="when" data-label="Timeline"><option value="">Choose…</option><option>As soon as possible</option><option>Within 2–4 weeks</option><option>Within 1–3 months</option><option>Just planning</option></select></div>
   <div><label for="q-details">Tell us more</label><textarea id="q-details" name="details" data-label="Details" placeholder="Wording, colours, where it goes, anything else…"></textarea></div>
   <div class="choice"><label class="consent"><input type="checkbox" name="consent" required> I agree my details may be used to respond to this request (<a href="privacy.html" style="color:var(--lime)">privacy policy</a>)</label></div>
   <button class="btn" type="submit">{ICON['wa']} Send via WhatsApp</button>
   <p class="form-msg" role="status">WhatsApp should now open with your request filled in — just press send. Don't forget to attach your logo or a photo of the site.</p>
   <p class="form-note">Nothing is stored on this website — your request goes straight to our WhatsApp.</p>
  </form>
  <div class="reveal">
   <p class="eyebrow">Prefer to talk?</p>
   <h2 class="chrome">Call, WhatsApp or email</h2>
   <ul class="contact-list" style="margin-top:2rem">
    <li><span class="ic">{ICON['phone']}</span><div><b>Call us</b><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></div></li>
    <li><span class="ic">{ICON['wa']}</span><div><b>WhatsApp</b><a href="{WA_LINK}" target="_blank" rel="noopener">Chat to us now</a></div></li>
    <li><span class="ic">{ICON['mail']}</span><div><b>Email</b><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
   </ul>
   <div class="media-frame" style="margin-top:2.5rem"><img src="assets/img/the-image-salon-interior.jpg" alt="Illuminated salon interior by Worldbrand Classic Signs" loading="lazy"></div>
  </div>
 </div>
</section>
'''
    return ('quote.html','Get a Quote','Request a free signage quote from Worldbrand Classic Signs in Durban — 3D signs, lightboxes, pylons, billboards, printing and vehicle branding.', body)

def page_contact():
    q = 'https://maps.google.com/maps?q=' + '25+Sedgemoor+Pl,+Woodlands,+Durban,+4004' + '&output=embed'
    body = page_hero('<span class="chrome">Contact</span> <span class="neon">us</span>',
        "For enquiries, please get in touch — we'd love to hear about your next sign.",
        'cold-meat-deli-lightbox', [('index.html','Home'),('','Contact')]) + f'''
<section>
 <div class="wrap split" style="align-items:stretch">
  <div class="reveal">
   <p class="eyebrow">For enquiries</p>
   <h2 class="chrome">Let's get your sign up</h2>
   <ul class="contact-list" style="margin-top:2rem">
    <li><span class="ic">{ICON['phone']}</span><div><b>Phone</b><a href="tel:{BIZ['phone_tel']}">{BIZ['phone_display']}</a></div></li>
    <li><span class="ic">{ICON['wa']}</span><div><b>WhatsApp</b><a href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></div></li>
    <li><span class="ic">{ICON['mail']}</span><div><b>Email</b><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
    <li><span class="ic">{ICON['pin']}</span><div><b>Workshop</b>{e(BIZ['street'])}<br>{BIZ['city']}, {BIZ['region']}, {BIZ['postal']}</div></li>
   </ul>
   <h3 style="margin-top:2.5rem;color:#fff">Find us on social media</h3>
   <ul class="contact-list" style="margin-top:1rem">
    <li><span class="ic">{ICON['ig']}</span><div><b>Instagram</b><a href="{BIZ['instagram']}" target="_blank" rel="noopener">@WorldbrandSigns</a></div></li>
    <li><span class="ic">{ICON['tt']}</span><div><b>TikTok</b><a href="{BIZ['tiktok']}" target="_blank" rel="noopener">@worldbrands1</a></div></li>
   </ul>
  </div>
  <div class="map reveal"><iframe src="{q}" title="Map to Worldbrand Classic Signs, Woodlands, Durban" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
 </div>
</section>
<section class="alt section-tight">
 <div class="wrap">
  <form class="form card reveal" data-wa="*New message — website contact form*" novalidate style="max-width:820px;margin:0 auto">
   <h2 class="chrome" style="font-size:2.2rem">Send us a message</h2>
   <div class="row">
    <div><label for="c-name">Name <span class="req">*</span></label><input id="c-name" name="name" data-label="Name" autocomplete="name" required></div>
    <div><label for="c-phone">Phone <span class="req">*</span></label><input id="c-phone" name="phone" type="tel" data-label="Phone" autocomplete="tel" required></div>
   </div>
   <div><label for="c-msg">Message <span class="req">*</span></label><textarea id="c-msg" name="message" data-label="Message" required></textarea></div>
   <div class="choice"><label class="consent"><input type="checkbox" name="consent" required> I agree my details may be used to respond (<a href="privacy.html" style="color:var(--lime)">privacy policy</a>)</label></div>
   <button class="btn" type="submit">{ICON['wa']} Send via WhatsApp</button>
   <p class="form-msg" role="status">WhatsApp should now open with your message — just press send.</p>
  </form>
 </div>
</section>
'''
    return ('contact.html','Contact','Contact Worldbrand Classic Signs — 25 Sedgemoor Pl, Woodlands, Durban. Call or WhatsApp +27 81 400 2417 or email info@worldbrandsigns.co.za.', body)

def page_privacy():
    body = page_hero('<span class="chrome">Privacy</span> <span class="neon">policy</span>',
        'How we handle your personal information, in line with the Protection of Personal Information Act (POPIA).',
        'gillitts-pharmacy', [('index.html','Home'),('','Privacy policy')]) + f'''
<section><div class="wrap prose">
 <p><em>Last updated: November 2026</em></p>
 <h2>Who we are</h2>
 <p>{BIZ['name']} (Reg. No. {BIZ['reg']}), {e(ADDR_ONE_LINE)}, {BIZ['region']}, South Africa. Contact: <a href="mailto:{BIZ['email']}" style="color:var(--lime)">{BIZ['email']}</a>.</p>
 <h2>What we collect</h2>
 <p>When you use our quote or contact form, you choose to send us your name, phone number, email address (optional) and details about your signage project. The form opens WhatsApp with your message — this website does not store your information on any server.</p>
 <h2>Why we use it</h2>
 <ul><li>To respond to your enquiry and prepare a quote.</li><li>To plan, deliver and install your signage.</li><li>To keep records required for invoicing and tax.</li></ul>
 <p>We do not sell your information, and we don't send marketing without your permission.</p>
 <h2>Third parties</h2>
 <p>Messages sent through WhatsApp are handled under WhatsApp's own privacy policy. Our contact page shows a Google Maps map, which is subject to Google's privacy policy. This website uses no tracking or advertising cookies.</p>
 <h2>Your rights</h2>
 <p>Under POPIA you may ask to see the personal information we hold about you, ask us to correct or delete it, or object to how we use it. Email us at the address above. You may also lodge a complaint with the Information Regulator of South Africa.</p>
 <h2>Keeping it safe</h2>
 <p>We keep your information only as long as we need it for the purposes above and take reasonable steps to protect it.</p>
</div></section>
'''
    return ('privacy.html','Privacy Policy','Privacy policy for Worldbrand Classic Signs — how we handle personal information under POPIA.', body)

def page_404():
    body = f'''<section class="notfound"><div class="wrap">
 <div class="big flicker">404</div>
 <h1 class="chrome" style="font-size:clamp(2rem,5vw,3rem);margin-top:1rem">This sign's switched off</h1>
 <p class="lead" style="margin:1rem auto">The page you're looking for doesn't exist or has moved.</p>
 <div class="btn-row" style="justify-content:center"><a class="btn" href="index.html">Back to home</a><a class="btn btn-ghost" href="quote.html">Get a quote</a></div>
</div></section>'''
    return ('404.html','Page not found','Page not found.', body, None, BASE_404)

# ------------------------------------------------------------------ build
def build():
    pages = [page_home(), page_about(), page_services()] + [page_service(s) for s in SERVICES] + \
            [page_projects(), page_clients(), page_quote(), page_contact(), page_privacy(), page_404()]
    urls = []
    for p in pages:
        fname, title, desc, body = p[0], p[1], p[2], p[3]
        navkey = (p[4] + fname) if len(p) > 4 and p[4] else fname
        base = p[5] if len(p) > 5 else None
        out = head(title, desc, fname, base) + header(navkey) + body + footer()
        with open(os.path.join(ROOT, fname), 'w', encoding='utf-8') as f:
            f.write(out)
        if fname != '404.html':
            urls.append(SITE_URL + ('' if fname == 'index.html' else fname))
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
        f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n' if LIVE else 'User-agent: *\nDisallow: /\n')
    print(f'Built {len(pages)} pages ({"LIVE" if LIVE else "PREVIEW"})')

if __name__ == '__main__':
    build()

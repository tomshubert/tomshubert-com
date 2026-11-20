#!/usr/bin/env python3
"""Builds the site's pages from src/ fragments. Run: python3 build.py
Edit src/*.html (and the PAGES table below), never the generated .html files at the root."""
import re, pathlib
ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
import hashlib
import sys; sys.path.insert(0, str(ROOT)); from icons import add_icons
CSSV = hashlib.md5((ROOT / "site.css").read_bytes()).hexdigest()[:8]
PREVIEW = False  # Launched 2026-11-14 with Tom's approval.

NAV = [("/", "Home"), ("/microsoft-365", "Microsoft 365"), ("/security", "Security"), ("/phone-service", "Phone Service"), ("/services", "Services"),
       ("/clients", "Clients"), ("/about", "About"), ("/contact", "Contact")]

PAGES = [
  # (file, path, title, description, sections)
  ("index.html", "/", "Tom Shubert IT Consulting | IT Consultant in Calabasas & Los Angeles",
   "Hands-on IT support for small businesses, based in Calabasas, CA and supporting clients across the U.S.: Microsoft 365, networks, computers, phones and websites. No help desk, no monthly contract required.",
   ["hero", "personal", "anywhere", "overview", "how", "cta"]),
  ("microsoft-365.html", "/microsoft-365", "Microsoft 365, SharePoint & OneDrive Support | Tom Shubert IT",
   "Microsoft 365 support for small businesses: moving off old servers to SharePoint, OneDrive, Exchange Online and Teams, set up right and looked after, with optional backup and 24/7 monitoring.",
   ["m365", "cta"]),
  ("security.html", "/security", "Small Business IT Security & Backups | Tom Shubert IT",
   "Practical security for small offices: multifactor sign-in, email filtering, protected computers, optional 24/7 Microsoft 365 monitoring, backups and help when something goes wrong.",
   ["security", "cta"]),
  ("phone-service.html", "/phone-service", "Business Phone Service: Nextiva & RingCentral | Tom Shubert IT",
   "Cloud business phone service from a Nextiva and RingCentral channel partner: choosing the right service, keeping your numbers, setup, training and ongoing support.",
   ["phone-service", "cta-phone-service"]),
  ("remote-help.html", "/remote-help", "Get Remote Help Now | Tom Shubert IT Consulting",
   "Need IT help right away? Call Tom, download the free RustDesk remote support app, and he can see your screen and fix the problem while you talk.",
   ["remote-help"]),
  ("services.html", "/services", "Small Business IT Services in Calabasas & L.A. | Tom Shubert IT",
   "Hands-on IT services for small businesses from Calabasas to anywhere in the U.S.: computers, networks and Wi-Fi, business phone service, malware help, office technology and websites.",
   ["services", "tech", "cta"]),
  ("clients.html", "/clients", "Industries Served & Client Stories | Tom Shubert IT Consulting",
   "The industries Tom Shubert IT Consulting serves, client stories, and real examples of recent work.",
   ["work", "clients-band", "week", "cta"]),
  ("about.html", "/about", "About Tom Shubert, IT Consultant Since 1982 | Tom Shubert IT",
   "Tom Shubert has been doing IT since 1982, from mainframes at Coca-Cola to today's cloud. Hands-on, relationship-driven support for small businesses.",
   ["about", "cta"]),
  ("contact.html", "/contact", "Contact Tom Shubert IT Consulting | Calabasas, CA",
   "Call 818.635.6777, email info@tomshubert.com or send a message to Tom Shubert IT Consulting in Calabasas, CA. Remote support nationwide, onsite in Southern California.",
   ["contact"]),
]
LEGAL = [("privacy.html", "/privacy"), ("terms.html", "/terms"), ("agreement.html", "/agreement")]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">'
LDJSON = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"Tom Shubert IT Consulting","url":"https://tomshubert.com/","telephone":"+1-818-635-6777","email":"info@tomshubert.com","foundingDate":"1982","founder":{"@type":"Person","name":"Tom Shubert"},"address":{"@type":"PostalAddress","postOfficeBoxNumber":"8922","addressLocality":"Calabasas","addressRegion":"CA","postalCode":"91372","addressCountry":"US"},"areaServed":"United States","description":"Hands-on IT support for small businesses: Microsoft 365, networks, computers, business phones and websites."}</script>'

def esc(t): return t.replace("&", "&amp;").replace('"', "&quot;")

def head(path, title, desc, home=False):
    url = "https://tomshubert.com" + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title.replace("&", "&amp;")}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex, nofollow">' if PREVIEW else ''}
<meta name="theme-color" content="#0b0e13">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://tomshubert.com/tom.jpg">
{LDJSON if home else ''}
{'<meta name="msvalidate.01" content="045E76972C7051B702E14DC8FF2CEDDC">' if home else ''}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/site.css?v={CSSV}">
</head>
<body>
{'<div class="preview-banner">Preview of the new site. The current tomshubert.com stays live until Tom approves this one.</div>' if PREVIEW else ''}'''

def header(path, overlay):
    links = "\n".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{n}</a>' for h, n in NAV)
    return f'''<header class="top wrap{'' if overlay else ' top-static'}">
  <a class="brand" href="/"><span class="brand-name">Tom Shubert<span>IT Consulting</span></span></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" aria-label="Main">
{links}
      <a class="nav-call" href="tel:+18186356777">818.635.6777</a>
  </nav>
</header>'''

FOOTER = '''<footer class="wrap site-footer">
  <div class="footer-row">
    <p>&copy; <span id="yr">2026</span> Tom Shubert IT Consulting &middot; 818.635.6777 &middot; <a href="mailto:info@tomshubert.com">info@tomshubert.com</a></p>
    <p><a href="/remote-help"><b>Get remote help</b></a> &middot; <a href="/privacy">Privacy</a> &middot; <a href="/terms">Terms of Use</a> &middot; <a href="/agreement">Client Service Agreement</a> &middot; Free scam alerts at <a href="https://fakes.com">FAKES.COM</a> &middot; Websites by <a href="https://yourweb.com">YourWEB Services</a></p>
  </div>
</footer>'''

def frag(name): return (SRC / f"{name}.html").read_text()

def first_h2_to_h1(html):
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", r"<h1 class=\"page-title\"\1>\2</h1>", html, count=1, flags=re.S)

def build():
    script = frag("_script")
    for fn, path, title, desc, sections in PAGES:
        home = path == "/"
        body = []
        for i, name in enumerate(sections):
            h = add_icons(frag(name))
            if i == 0 and not home: h = first_h2_to_h1(h)
            body.append(h)
        if home:
            top = '<div class="hero-band">\n' + header(path, True) + "\n" + body[0] + '  <p class="since" aria-hidden="true">CALABASAS, CA &middot; CLIENTS NATIONWIDE</p>\n</div>\n<main>\n' + "\n".join(body[1:]) + "</main>"
        else:
            top = header(path, False) + '\n<main class="subpage">\n' + "\n".join(body) + "</main>"
        (ROOT / fn).write_text(head(path, title, desc, home) + "\n" + top + "\n" + FOOTER + "\n" + script + "\n</body>\n</html>\n")
    for fn, path in LEGAL:
        s = (ROOT / fn).read_text()
        main = s[s.index('<main'):s.index('</main>') + 7]
        t = re.search(r"<title>(.*?)</title>", s).group(1).replace("&amp;", "&")
        d = re.search(r'<meta name="description" content="(.*?)">', s).group(1).replace("&quot;", '"').replace("&amp;", "&")
        (ROOT / fn).write_text(head(path, t, d) + "\n" + header(path, False) + "\n" + main + "\n" + FOOTER + "\n" + script + "\n</body>\n</html>\n")
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if PREVIEW else "User-agent: *\nAllow: /\nSitemap: https://tomshubert.com/sitemap.xml\n")
    urls = [p for _, p, *_ in PAGES] + [p for _, p in LEGAL]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>https://tomshubert.com{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    print("built", len(PAGES) + len(LEGAL), "pages")

if __name__ == "__main__":
    build()

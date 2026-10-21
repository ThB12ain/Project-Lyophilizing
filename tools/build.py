#!/usr/bin/env python3
"""Generate the static Sublyra Sciences site.

Shared header, footer and service pages are built from templates here, the
service copy lives in tools/services.json, and the home, quality and contact
page bodies live in tools/partials/. Run from the repo root:

    python3 tools/build.py              # writes the *.html pages at the repo root
    python3 tools/build.py --inline DIR # also writes a self-contained copy (CSS/JS inlined) to DIR
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
BRAND = "Sublyra Sciences"
SERVICES = json.loads((TOOLS / "services.json").read_text())
ORDER = ["washing", "sterilizing", "mixing", "filling", "lyophilization",
         "capping", "labeling", "rnd", "synthesis"]
CHAIN = [k for k in ORDER if SERVICES[k].get("step")]
CHAIN_HINT = {"washing": "Vials, stoppers", "sterilizing": "Depyrogenation",
              "mixing": "Compounding", "filling": "Aseptic fill",
              "lyophilization": "Primary and secondary drying", "capping": "Seal and inspect",
              "labeling": "Label and pack"}
FILE = {k: f"{k}.html" for k in ORDER}
FILE["synthesis"] = "custom-synthesis.html"
e = html.escape

LOGO_MARK = """<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
        <path d="M31.3 15.5v13L20 35 8.7 28.5v-13L20 9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        <path class="cake" d="M20 17.2l5 2.9v5.8l-5 2.9-5-2.9v-5.8z"/>
        <circle class="vapor" cx="25.6" cy="10.4" r="2"/><circle class="vapor" cx="30.6" cy="7.6" r="1.55"/><circle class="vapor" cx="34.6" cy="4.6" r="1.15"/>
      </svg>"""


def head(title, description):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;600;700;800&family=Source+Sans+3:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


COMPANY_NAV = [("about.html", "About us", "about"), ("how-we-work.html", "How we work", "how-we-work"),
               ("quality.html", "Quality", "quality")]
RESOURCE_NAV = [("index.html#faq", "FAQ", None), ("contact.html", "Contact", "contact")]
SERVICE_GROUPS = [("all", "services.html", "Services overview")]


def header(active):
    def cur(k):
        return ' aria-current="page"' if k == active else ""
    tabs = []
    for k in ORDER:
        s = SERVICES[k]
        if s.get("featured"):
            tabs.append(f'<a href="{FILE[k]}" class="featured"{cur(k)}>{e(s["title"])}<span class="star">CORE</span></a>')
        else:
            tabs.append(f'<a href="{FILE[k]}"{cur(k)}>{e(s["title"])}</a>')
    svc_links = (f'<a href="services.html"{cur("services")}>Services overview</a>'
                 + "".join(f'<a href="{FILE[k]}"{cur(k)}>{e(SERVICES[k]["title"])}</a>' for k in ORDER))
    co_links = "".join(f'<a href="{h}"{cur(k)}>{t}</a>' for h, t, k in COMPANY_NAV)
    res_links = "".join(f'<a href="{h}"{cur(k) if k else ""}>{t}</a>' for h, t, k in RESOURCE_NAV)
    in_services = active == "services" or active in SERVICES
    in_company = active in {k for _, _, k in COMPANY_NAV}

    def top(label, ident, links, on):
        mark = ' data-active="true"' if on else ""
        return f"""<div class="dd"{mark}>
          <button type="button" class="nav-top" aria-expanded="false" aria-controls="dd-{ident}">{label}<svg viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
          <div class="dd-panel" id="dd-{ident}">{links}</div>
        </div>"""
    return f"""<header class="site">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="{BRAND} home">
      {LOGO_MARK}
      <span class="brand-name">Sublyra <span>Sciences</span></span>
    </a>
    <nav class="mainnav" aria-label="Main">
      <a class="nav-top" href="index.html"{cur("home")}>Home</a>
      {top("Services", "services", svc_links, in_services)}
      {top("About", "about", co_links, in_company)}
      {top("Resources", "resources", res_links, active == "contact")}
    </nav>
    <div class="bar-links">
      <a class="btn btn-primary btn-talk caps" href="contact.html">Talk to an expert <span aria-hidden="true">›</span></a>
      <button type="button" class="menu-btn" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="mobile-menu" id="mobile-menu" hidden>
    <div class="wrap">
      <div><h4>Services</h4>{svc_links}</div>
      <div><h4>About</h4>{co_links}</div>
      <div><h4>Resources</h4>{res_links}</div>
    </div>
  </div>
  <div class="tabs-scroll">
    <nav class="wrap tabs" aria-label="Services">
      {chr(10).join("      " + t for t in tabs).strip()}
    </nav>
  </div>
</header>
"""


CTA = """<section class="cta-band on-ink">
    <div class="wrap">
      <div><p class="eyebrow">Contact</p><h2>Speak with one of our experts.</h2><p>Share your formulation and timeline. We'll map the steps and cost with you.</p></div>
      <a class="btn btn-primary caps" href="contact.html">Talk to an expert <span aria-hidden="true">›</span></a>
    </div>
  </section>"""

DOT_MAP = "".join(
    f'<circle cx="{14 + c * 12}" cy="{14 + r * 12}" r="2.2"/>'
    for r, row in enumerate([
        "....xxxxxxxxxxxxxxx.......",
        "...xxxxxxxxxxxxxxxxxxx....",
        "..xxxxxxxxxxxxxxxxxxxxxxx.",
        "..xxxxxxxxxxxxxxxxxxxxxxxx",
        "...xxxxxxxxxxxxxxxxxxxxxx.",
        "...xxxxxxxxxxxxxxxxxxxxx..",
        "....xxxxxxxxxxxxxxxxxxx...",
        ".....xxxxxxxxxxxxx..xxx...",
        "........xxxxx........xx...",
    ])
    for c, ch in enumerate(row) if ch == "x"
)

COMPANY = f"""<section class="company">
    <div class="wrap company-grid">
      <div class="hq">
        <p class="eyebrow">Find us</p>
        <h2>Headquartered in Anytown, California</h2>
        <svg class="dot-map" viewBox="0 0 330 124" role="img" aria-label="Map of the United States with our California site marked">
          <g class="dots">{DOT_MAP}</g>
          <circle class="pin-ring" cx="50" cy="74" r="9"/><circle class="pin" cx="50" cy="74" r="4.5"/>
        </svg>
      </div>
      <div class="company-copy">
        <p>Sublyra Sciences works as an extension of your team. We take on the lyophilization and fill-finish steps that are hardest to get right, lower the risk in your program and help you reach the market on time.</p>
        <a class="btn btn-solid caps" href="contact.html">Talk to an expert <span aria-hidden="true">›</span></a>
        <div class="accred">
          <p class="eyebrow">Accreditations</p>
          <ul><li>cGMP</li><li>ISO 13485</li><li>FDA registered</li></ul>
        </div>
        <div class="address"><p class="eyebrow">Address</p><p>1200 Example Way, Suite 100<br>Anytown, CA 90000</p></div>
      </div>
    </div>
  </section>"""


def footer():
    svc = "".join(f'<li><a href="{FILE[k]}">{e(SERVICES[k]["title"])}</a></li>' for k in ORDER)
    co = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in COMPANY_NAV) + '<li><a href="contact.html">Contact</a></li>'
    return f"""<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html">{LOGO_MARK}<span class="brand-name">Sublyra <span>Sciences</span></span></a>
        <p style="margin-top:12px;max-width:28em">Lyophilization-led contract manufacturing, from component washing to labeled product.</p>
        <p style="margin-top:12px">1200 Example Way, Anytown, CA 90000</p>
      </div>
      <div><h4>Company</h4><ul>{co}</ul></div>
      <div style="grid-column:span 2"><h4>Services</h4><ul class="two-up"><li><a href="services.html">Services overview</a></li>{svc}</ul></div>
    </div>
    <div class="foot-legal"><span>© <span data-year>2026</span> {BRAND}</span><span>Privacy Policy · Cookie Policy · Accessibility</span></div>
  </div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""




def chain(active=None):
    items = []
    for k in CHAIN:
        cls = ' class="on"' if k == active else ""
        items.append(f'<li{cls}><a href="{FILE[k]}">{e(SERVICES[k]["title"])}</a><small>{CHAIN_HINT[k]}</small></li>')
    return '<ol class="chain">' + "".join(items) + "</ol>"


def dl(pairs):
    return "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in pairs)


def service_grid():
    out = []
    for k in ORDER:
        sv = SERVICES[k]
        core = '<span class="core-tag">Core</span>' if sv.get("featured") else ""
        out.append(f"""<a class="svc-tile{' is-core' if sv.get('featured') else ''}" href="{FILE[k]}">
          <span class="tile-top"><svg aria-hidden="true"><use href="#{sv['icon']}"/></svg>{core}<svg class="arrow" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12L12 4M6 4h6v6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></span>
          <h3>{e(sv['title'])}</h3><p>{e(sv['card'])}</p><span class="more caps">More <span aria-hidden="true">›</span></span></a>""")
    return '<div class="svc-tiles">' + "\n        ".join(out) + "</div>"


ICONS = (TOOLS / "partials" / "icons.svg").read_text()


def service_body(k):
    s = SERVICES[k]
    fit = (f"{s['title']} feeds the line before step 01." if s.get("support")
           else f"Step {s['step']:02d} of 7 on one floor.")
    caps = "".join(f'<div class="cap"><span class="idx"></span><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in s["caps"])
    spec = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in s["spec"])
    body = "".join(f"<p>{e(p)}</p>" for p in s["specBody"])
    deliv = "".join(f"<li>{e(d)}</li>" for d in s["deliverables"])
    return f"""<section class="page-hero on-ink">
    <div class="wrap">
      <div>
        <p class="crumb"><a href="index.html">Home</a> » <a href="services.html">Services</a> » {e(s['title'])}</p>
        <h1>{e(s['headline'])}</h1>
        <p class="lede">{e(s['lede'])}</p>
        <div class="ctas"><a class="btn btn-primary caps" href="contact.html">Talk to an expert <span aria-hidden="true">›</span></a></div>
      </div>
      <dl class="keyfacts">{dl(s['keyfacts'])}</dl>
    </div>
  </section>
  <section class="band">
    <div class="wrap"><div class="cap-grid">{caps}</div></div>
  </section>
  <section class="band alt">
    <div class="wrap two-col">
      <div>
        <p class="eyebrow">Capabilities</p>
        <h2>{e(s['specTitle'])}</h2>
        <div class="body" style="margin-top:14px">{body}</div>
      </div>
      <div class="table-wrap"><table class="spec"><tbody>{spec}</tbody></table></div>
    </div>
  </section>
  <section class="band">
    <div class="wrap two-col">
      <div><p class="eyebrow">Why Sublyra</p><h2>Why choose us for {e(s['title'].lower() if s['title'] != 'R&D' else s['title'])}</h2><p style="color:var(--muted);margin-top:14px">Every project includes these deliverables.</p></div>
      <ul class="checklist">{deliv}</ul>
    </div>
  </section>
  <section class="band alt">
    <div class="wrap">
      <div class="section-head" style="margin-bottom:28px">
        <div><p class="eyebrow">Where this fits</p><h2>{e(fit)}</h2></div>
      </div>
      {chain(k)}
      <div class="chain-support">Feeding the line: <a href="rnd.html">R&amp;D and formulation</a><a href="custom-synthesis.html">Custom synthesis</a></div>
    </div>
  </section>"""


def services_overview_list():
    return "".join(f'<li><a href="{FILE[k]}">{e(SERVICES[k]["title"])}</a></li>' for k in ORDER)


def services_overview_rows():
    rows = []
    for i, k in enumerate(ORDER, 1):
        sv = SERVICES[k]
        rows.append(f"""<article class="ov-row">
          <span class="ov-num">{i:02d}</span>
          <div class="ov-icon"><svg aria-hidden="true"><use href="#{sv['icon']}"/></svg></div>
          <div><h3><a href="{FILE[k]}">{e(sv['title'])}</a></h3><p>{e(sv['lede'])}</p></div>
          <a class="more caps" href="{FILE[k]}">More <span aria-hidden="true">›</span></a>
        </article>""")
    return "".join(rows)


def page(active, title, description, body, cta=True):
    return (head(title, description).replace('<html lang="en">', '<html lang="en" class="theme-v1">')
            + ICONS + header(active)
            + f'<main id="main">\n  {body}\n  {CTA if cta else ""}\n  {COMPANY}\n</main>\n' + footer())


def partial(name):
    return (TOOLS / "partials" / f"{name}.html").read_text()


def build():
    pages = {}
    home = (partial("home")
            .replace('<div class="svc-grid" id="svc-grid"></div>', service_grid())
            .replace('<ol class="chain" data-chain></ol>', chain()))
    pages["index.html"] = page(
        "home", BRAND,
        "Sublyra Sciences is a contract manufacturer specializing in lyophilization, with washing, "
        "sterilizing, mixing, filling, capping, labeling, R&D and custom synthesis under one roof.", home, cta=False)
    for k in ORDER:
        s = SERVICES[k]
        pages[FILE[k]] = page(k, f"{s['title']} · {BRAND}", s["card"], service_body(k))
    overview = partial("services").replace("<!--SERVICE-LIST-->", services_overview_list()).replace("<!--SERVICE-ROWS-->", services_overview_rows())
    pages["services.html"] = page("services", f"Services · {BRAND}",
                                  "End-to-end contract manufacturing services led by lyophilization.", overview)
    pages["about.html"] = page("about", f"About us · {BRAND}",
                               "Who Sublyra Sciences is, and why we built a lyophilization-led CDMO.", partial("about"))
    pages["how-we-work.html"] = page("how-we-work", f"How we work · {BRAND}",
                                     "How Sublyra Sciences runs programs: candor, communication and program management.",
                                     partial("how-we-work"))
    pages["quality.html"] = page("quality", f"Quality · {BRAND}",
                                 "One quality system across every manufacturing step.", partial("quality"))
    chips = "".join(f'<label><input type="checkbox" id="svc-{k}" name="services" value="{k}">{e(SERVICES[k]["title"])}</label>'
                    for k in ORDER)
    contact = partial("contact").replace("<legend>Services you need</legend>",
                                         "<legend>Services you need</legend>" + chips)
    pages["contact.html"] = page("contact", f"Contact · {BRAND}",
                                 "Talk to a Sublyra Sciences lyophilization expert.", contact, cta=False)
    for name, text in pages.items():
        (ROOT / name).write_text(text)
    return pages


def inline(pages, out):
    """Self-contained copies for previews: CSS, JS, favicon and image tiles inlined."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    css = (ROOT / "assets/css/styles.css").read_text()
    js = (ROOT / "assets/js/main.js").read_text()
    fav = (ROOT / "assets/img/favicon.svg").read_text()
    import urllib.parse
    fav_uri = "data:image/svg+xml," + urllib.parse.quote(fav)
    for name, text in pages.items():
        t = (text.replace('<link rel="stylesheet" href="assets/css/styles.css">', f"<style>\n{css}</style>")
                 .replace('<script src="assets/js/main.js"></script>', f"<script>\n{js}</script>")
                 .replace('href="assets/img/favicon.svg"', f'href="{fav_uri}"'))
        for img in (ROOT / "assets/img").glob("tile-*.svg"):
            t = t.replace(f'src="assets/img/{img.name}"',
                          f'src="data:image/svg+xml,{urllib.parse.quote(img.read_text())}"')
        (out / name).write_text(t)


if __name__ == "__main__":
    built = build()
    print(f"Built {len(built)} pages")
    if "--inline" in sys.argv:
        inline(built, sys.argv[sys.argv.index("--inline") + 1])

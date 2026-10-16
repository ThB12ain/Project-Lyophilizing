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
              "lyophilization": "Freeze-drying", "capping": "Seal and inspect",
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
    return f"""<header class="site">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="{BRAND} home">
      {LOGO_MARK}
      <span class="brand-name">Sublyra <span>Sciences</span></span>
    </a>
    <div class="bar-links">
      <a class="plain" href="index.html"{cur("home")}>Overview</a>
      <a class="plain" href="quality.html"{cur("quality")}>Quality</a>
      <a class="plain" href="contact.html"{cur("contact")}>Contact</a>
      <a class="btn btn-primary btn-talk" href="contact.html">Talk to an expert</a>
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
      <div><h2>Let's plan your next batch.</h2><p>Share your formulation and timeline. We'll map the steps and cost with you.</p></div>
      <a class="btn btn-primary" href="contact.html">Talk to an expert</a>
    </div>
  </section>"""

FOOTER = f"""<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html">{LOGO_MARK}<span class="brand-name">Sublyra <span>Sciences</span></span></a>
        <p style="margin-top:12px;max-width:28em">Contract lyophilization and fill-finish, from component washing to labeled product.</p>
        <p style="margin-top:12px">1200 Example Way, Anytown, CA 90000</p>
      </div>
      <div><h4>Process</h4><ul>
        <li><a href="washing.html">Washing</a></li><li><a href="sterilizing.html">Sterilizing</a></li><li><a href="mixing.html">Mixing</a></li><li><a href="filling.html">Filling</a></li>
      </ul></div>
      <div><h4>Finish</h4><ul>
        <li><a href="lyophilization.html">Lyophilization</a></li><li><a href="capping.html">Capping</a></li><li><a href="labeling.html">Labeling</a></li>
      </ul></div>
      <div><h4>Science</h4><ul>
        <li><a href="rnd.html">R&amp;D</a></li><li><a href="custom-synthesis.html">Custom synthesis</a></li><li><a href="quality.html">Quality</a></li><li><a href="contact.html">Contact</a></li>
      </ul></div>
    </div>
    <div class="foot-legal"><span>© <span data-year>2026</span> {BRAND}</span><span>Privacy · Terms · Accessibility</span></div>
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
    lyo = SERVICES["lyophilization"]
    out = [f"""<a class="svc feature" href="{FILE['lyophilization']}">
          <div style="display:flex;flex-direction:column;gap:12px">
            <span class="tag">Our core specialty</span>
            <svg aria-hidden="true"><use href="#i-lyo"/></svg>
            <h3>Lyophilization</h3>
            <p>{e(lyo['card'])} Most programs start here and add the steps around it.</p>
            <span class="more">See lyophilization capabilities →</span>
          </div>
          <dl class="feature-specs">{dl(lyo['keyfacts'])}</dl>
        </a>"""]
    for k in ORDER:
        if k == "lyophilization":
            continue
        s = SERVICES[k]
        out.append(f"""<a class="svc" href="{FILE[k]}">
          <div class="top"><svg aria-hidden="true"><use href="#{s['icon']}"/></svg></div>
          <h3>{e(s['title'])}</h3><p>{e(s['card'])}</p><span class="more">Learn more →</span></a>""")
    return '<div class="svc-grid">' + "\n        ".join(out) + "</div>"


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
        <p class="crumb"><a href="index.html">Services</a> / {e(s['title'])}</p>
        <h1>{e(s['headline'])}</h1>
        <p class="lede">{e(s['lede'])}</p>
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
      <div><p class="eyebrow">What you get</p><h2>Deliverables</h2></div>
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


def page(active, title, description, body, cta=True):
    return (head(title, description) + ICONS + header(active)
            + f'<main id="main">\n  {body}\n  {CTA if cta else ""}\n</main>\n' + FOOTER)


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
        "sterilizing, mixing, filling, capping, labeling, R&D and custom synthesis under one roof.", home)
    for k in ORDER:
        s = SERVICES[k]
        pages[FILE[k]] = page(k, f"{s['title']} · {BRAND}", s["card"], service_body(k))
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
    """Self-contained copies for previews: CSS, JS and favicon inlined."""
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
        (out / name).write_text(t)


if __name__ == "__main__":
    built = build()
    print(f"Built {len(built)} pages")
    if "--inline" in sys.argv:
        inline(built, sys.argv[sys.argv.index("--inline") + 1])

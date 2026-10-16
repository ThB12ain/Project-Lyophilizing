#!/usr/bin/env python3
"""Generate Version 2 of the site: a lyophilization-only Sublyra Sciences.

Pages are written to v2/ and share the brand stylesheet, script and images in
assets/ with Version 1. Service copy lives in tools/v2/services.json and the
home page body in tools/v2/partials/home.html. Run from the repo root:

    python3 tools/build_v2.py              # writes v2/*.html
    python3 tools/build_v2.py --inline DIR # also writes self-contained copies to DIR
"""
import json
import sys
from pathlib import Path

import build
from build import BRAND, LOGO_MARK, dl, e, head

ROOT = build.ROOT
V2 = ROOT / "tools" / "v2"
OUT = ROOT / "v2"
SERVICES = json.loads((V2 / "services.json").read_text())
ORDER = list(SERVICES)
FILE = {k: f"{k}.html" for k in ORDER}
SECTIONS = [("formats", "Formats"), ("applications", "Applications"), ("capabilities", "Capabilities"),
            ("prototyping", "Bead Prototyping"), ("swabs", "Swabs & Surfaces"), ("process", "Working Together"),
            ("support", "Support Services"), ("faq", "FAQ")]
ICONS = (V2 / "partials" / "icons.svg").read_text()
CHAIN_HINT = {"feasibility": "Is lyo right?", "characterization": "Tc, Tg′",
              "cycle-development": "Recipe and optimization", "scale-up": "Pilot to production",
              "gmp": "Clinical and commercial", "testing": "Moisture, stability"}


def v2_head(title, description):
    return head(title, description).replace('href="assets/', 'href="../assets/')


def header(active):
    def cur(k):
        return ' aria-current="page"' if k == active else ""
    base = "" if active == "home" else "index.html"
    tabs = [f'<a href="{base}#{anchor}">{label}</a>' for anchor, label in SECTIONS]
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
    <nav class="wrap tabs" aria-label="Lyophilization sections">
      {chr(10).join("      " + t for t in tabs).strip()}
    </nav>
  </div>
</header>
"""


CTA = """<section class="cta-band on-ink">
    <div class="wrap">
      <div><h2>Frozen, chilled or room temperature. You decide how it ships.</h2><p>Have your experts talk with ours about taking your product dry.</p></div>
      <a class="btn btn-primary" href="contact.html">Talk to an expert</a>
    </div>
  </section>"""


def footer():
    items = "".join(f'<li><a href="{FILE[k]}">{e(SERVICES[k]["title"])}</a></li>' for k in ORDER)
    return f"""<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html">{LOGO_MARK}<span class="brand-name">Sublyra <span>Sciences</span></span></a>
        <p style="margin-top:12px;max-width:28em">Lyophilization specialists, from feasibility to commercial supply.</p>
        <p style="margin-top:12px">1200 Example Way, Anytown, CA 90000</p>
      </div>
      <div style="grid-column:span 2"><h4>Lyophilization</h4><ul>{items}</ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="quality.html">Quality</a></li><li><a href="contact.html">Contact</a></li>
        <li><a href="../index.html">Full-service site</a></li>
      </ul></div>
    </div>
    <div class="foot-legal"><span>© <span data-year>2026</span> {BRAND}</span><span class="version-note">Version 2 · <a href="../index.html">See Version 1</a></span></div>
  </div>
</footer>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""


def chain(active=None):
    items = []
    for k in ORDER:
        cls = ' class="on"' if k == active else ""
        items.append(f'<li{cls}><a href="{FILE[k]}">{e(SERVICES[k]["short"])}</a><small>{CHAIN_HINT[k]}</small></li>')
    return '<ol class="chain chain-6">' + "".join(items) + "</ol>"


def service_grid():
    out = []
    for k in ORDER:
        s = SERVICES[k]
        out.append(f"""<a class="svc" href="{FILE[k]}">
          <div class="top"><svg aria-hidden="true"><use href="#{s['icon']}"/></svg><span class="mono" style="font-size:12px;color:var(--muted)">STAGE {s['step']:02d}</span></div>
          <h3>{e(s['title'])}</h3><p>{e(s['card'])}</p><span class="more">Learn more →</span></a>""")
    return '<div class="svc-grid">' + "\n        ".join(out) + "</div>"


def service_body(k):
    s = SERVICES[k]
    caps = "".join(f'<div class="cap"><span class="idx"></span><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in s["caps"])
    spec = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in s["spec"])
    body = "".join(f"<p>{e(p)}</p>" for p in s["specBody"])
    deliv = "".join(f"<li>{e(d)}</li>" for d in s["deliverables"])
    return f"""<section class="page-hero on-ink">
    <div class="wrap">
      <div>
        <p class="crumb"><a href="index.html">Lyophilization</a> / <a href="index.html#process">How we work</a> / {e(s['title'])}</p>
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
        <div><p class="eyebrow">Where this fits</p><h2>Stage {s['step']:02d} of 6 in a lyophilized program.</h2></div>
      </div>
      {chain(k)}
    </div>
  </section>"""


def page(active, title, description, body, cta=True):
    return (v2_head(title, description) + ICONS + header(active)
            + f'<main id="main">\n  {body}\n  {CTA if cta else ""}\n</main>\n' + footer())


def build_v2():
    OUT.mkdir(exist_ok=True)
    pages = {}
    home = ((V2 / "partials" / "home.html").read_text()
            .replace('<div class="svc-grid" id="svc-grid"></div>', service_grid())
            .replace('<ol class="chain" data-chain></ol>', chain()))
    pages["index.html"] = page(
        "home", f"{BRAND} · Lyophilization",
        "Sublyra Sciences is a lyophilization specialist: feasibility, thermal characterization, "
        "cycle development, scale-up, GMP lyophilization and release testing.", home)
    for k in ORDER:
        s = SERVICES[k]
        pages[FILE[k]] = page(k, f"{s['title']} · {BRAND}", s["card"], service_body(k))
    pages["quality.html"] = page("quality", f"Quality · {BRAND}",
                                 "One quality system across every lyophilization stage.",
                                 build.partial("quality").replace("Overview</a> / Quality", "Lyophilization</a> / Quality"))
    chips = "".join(f'<label><input type="checkbox" id="svc-{k}" name="services" value="{k}">{e(SERVICES[k]["title"])}</label>'
                    for k in ORDER)
    contact = (build.partial("contact")
               .replace("<legend>Services you need</legend>", "<legend>Services you need</legend>" + chips)
               .replace("Overview</a> / Contact", "Lyophilization</a> / Contact"))
    pages["contact.html"] = page("contact", f"Contact · {BRAND}",
                                 "Talk to a Sublyra Sciences lyophilization scientist.", contact, cta=False)
    for name, text in pages.items():
        (OUT / name).write_text(text)
    return pages


if __name__ == "__main__":
    built = build_v2()
    print(f"Built {len(built)} Version 2 pages in v2/")
    if "--inline" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--inline") + 1])
        fixed = {n: t.replace('href="../assets/', 'href="assets/').replace('src="../assets/', 'src="assets/')
                 for n, t in built.items()}
        build.inline(fixed, out)

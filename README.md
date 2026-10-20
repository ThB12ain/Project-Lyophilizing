# Sublyra Sciences website

Static marketing site for **Sublyra Sciences**, a contract manufacturer that specializes in lyophilization and offers washing, sterilizing, mixing, filling, capping, labeling, R&D and custom synthesis under one roof.

> "Sublyra Sciences" is a working brand name. The address, phone, email and all capacity figures on the site are sample values to replace before launch.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Services overview | `services.html` |
| Washing | `washing.html` |
| Sterilizing | `sterilizing.html` |
| Mixing | `mixing.html` |
| Filling | `filling.html` |
| Lyophilization (core service) | `lyophilization.html` |
| Capping | `capping.html` |
| Labeling | `labeling.html` |
| R&D | `rnd.html` |
| Custom Synthesis | `custom-synthesis.html` |
| About us | `about.html` |
| How we work | `how-we-work.html` |
| Quality | `quality.html` |
| Contact | `contact.html` |

Version 1 follows the page structure of a full-service lyophilization CDMO site: an uppercase dropdown menu (Services, About, Resources), a home page with hero shortcuts, positioning, stats, service tiles, contact band and FAQ, and a "Headquartered in" block with accreditations above the footer on every page. The service tab strip under the menu is kept.

## Version 2: lyophilization only

`v2/` holds a second version of the site that covers lyophilization alone, live at `/v2/` next to Version 1. Its home page is one long lyophilization landing page (why lyophilize, benefits, formats, how we work, applications, fit check, FAQ), modeled on the structure of a specialist CDMO's lyophilization service page. The six detail pages below sit behind the "How we work" section. It shares the logo, stylesheet and script in `assets/`.

| Page | File |
|---|---|
| Home (lyophilization landing page) | `v2/index.html` |
| Feasibility & Formulation | `v2/feasibility.html` |
| Thermal Characterization | `v2/characterization.html` |
| Cycle Development | `v2/cycle-development.html` |
| Scale-up & Tech Transfer | `v2/scale-up.html` |
| GMP Lyophilization | `v2/gmp.html` |
| Release Testing | `v2/testing.html` |
| Quality | `v2/quality.html` |
| Contact | `v2/contact.html` |

Edit `tools/v2/services.json` or `tools/v2/partials/home.html`, then run `python3 tools/build_v2.py`. Version 2 reuses Version 1's Quality and Contact content from `tools/partials/`.

## Project layout

```
assets/css/styles.css   all styling, brand tokens at the top
assets/js/main.js       dropdown and phone menus, active-tab scrolling, the contact form
assets/img/             logo, logo-white, logo-mark, favicon (SVG)
tools/build.py          generates every .html page
tools/services.json     copy and specs for the nine service pages
tools/partials/         body content for home, services, about, how-we-work, quality and contact, plus the icon set
```

## Editing content

The HTML pages are generated, so edit the sources and rebuild:

1. Service copy, key facts and spec tables: `tools/services.json`
2. Home, Services, About, How we work, Quality or Contact page content: `tools/partials/*.html`
3. Header, menus, footer, "Headquartered in" block and the service-page layout: `tools/build.py`

Then run:

```sh
python3 tools/build.py
```

No dependencies beyond Python 3. Commit the regenerated `.html` files with your source change.

## Previewing locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## Before launch

- Replace the sample address, phone and email (`tools/partials/contact.html`, footer and `COMPANY` block in `tools/build.py`).
- Replace the sample accreditations (cGMP, ISO 13485, FDA registered) in the `COMPANY` block of `tools/build.py`.
- Replace sample capacity figures in `tools/services.json` and the home page stats.
- Confirm the compliance list on the home and Quality pages matches certifications actually held.
- Connect the contact form in `assets/js/main.js` to a form service or CRM; it currently validates input but sends nothing.

## Hosting

Any static host works (GitHub Pages, Azure Static Web Apps, Netlify, S3). For GitHub Pages: Settings → Pages → deploy from the `main` branch, root folder.

See [BRAND.md](BRAND.md) for the logo, colors and type.

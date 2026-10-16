# Sublyra Sciences website

Static marketing site for **Sublyra Sciences**, a contract manufacturer that specializes in lyophilization (freeze-drying) and offers washing, sterilizing, mixing, filling, capping, labeling, R&D and custom synthesis under one roof.

> "Sublyra Sciences" is a working brand name. The address, phone, email and all capacity figures on the site are sample values to replace before launch.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Washing | `washing.html` |
| Sterilizing | `sterilizing.html` |
| Mixing | `mixing.html` |
| Filling | `filling.html` |
| Lyophilization (core service) | `lyophilization.html` |
| Capping | `capping.html` |
| Labeling | `labeling.html` |
| R&D | `rnd.html` |
| Custom Synthesis | `custom-synthesis.html` |
| Quality | `quality.html` |
| Contact | `contact.html` |

## Project layout

```
assets/css/styles.css   all styling, brand tokens at the top
assets/js/main.js       active-tab scrolling and the contact form
assets/img/             logo, logo-white, logo-mark, favicon (SVG)
tools/build.py          generates every .html page
tools/services.json     copy and specs for the nine service pages
tools/partials/         body content for home, quality and contact, plus the icon set
```

## Editing content

The HTML pages are generated, so edit the sources and rebuild:

1. Service copy, key facts and spec tables: `tools/services.json`
2. Home, Quality or Contact page content: `tools/partials/*.html`
3. Header, footer and the service-page layout: `tools/build.py`

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

- Replace the sample address, phone and email (`tools/partials/contact.html`, footer in `tools/build.py`).
- Replace sample capacity figures in `tools/services.json` and the home page stats.
- Confirm the compliance list on the home and Quality pages matches certifications actually held.
- Connect the contact form in `assets/js/main.js` to a form service or CRM; it currently validates input but sends nothing.

## Hosting

Any static host works (GitHub Pages, Azure Static Web Apps, Netlify, S3). For GitHub Pages: Settings → Pages → deploy from the `main` branch, root folder.

See [BRAND.md](BRAND.md) for the logo, colors and type.

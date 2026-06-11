# BiblioQ Marketing Website

Static landing page and interactive demo for BiblioQ v3.0.

## Pages

| File | Description |
|------|-------------|
| `index.html` | Marketing landing page |
| `demo.html` | App-like dashboard preview with floating AI chat |
| `faq.html` | FAQ |
| `legal/privacy.html` | Privacy stub |
| `legal/terms.html` | Terms stub |

## Local preview

```powershell
cd website
py -m http.server 8080
```

Open http://localhost:8080

## Deployment

Pushes to `main` that change `website/**` deploy automatically via GitHub Actions (`.github/workflows/pages.yml`).

Live site: https://jengu.github.io/BiblioQ/

## Download links

Download buttons fetch the latest URL from:

https://raw.githubusercontent.com/JENGUEL/-BiblioQ-Updates/main/version.json

Fallback values are embedded in `js/main.js` if the fetch fails.

# Ultra Clean PNW website

Static, mobile-first site for Ultra Clean PNW, serving Vancouver, WA, Portland, OR and the surrounding areas.

## Pages (clean URLs, no .html)
- `/` home
- `/services/` all services
- `/services/<service>/` one page per service (7 total)
- `/contact/` quote form

Every page is an `index.html` inside its own folder, so any static host (GitHub Pages, Netlify, Vercel, Cloudflare Pages) serves `/services/deep-cleaning/` without `.html` in the address bar.

## Editing
Page content lives in `_src/build.py` (services, copy, FAQs, service areas, contact details). After editing run:

    python _src/build.py

Styles are in `css/styles.css`, behavior in `js/main.js`, images in `assets/`.

## Before going live
1. Domain: canonicals, Open Graph, JSON-LD, `sitemap.xml` and `robots.txt` use `https://ultracleanpnw.com`. Change `SITE` in `_src/build.py` if the domain differs and rebuild.
2. Contact details: set `EMAIL` and `PHONE` in `_src/build.py` (phone links stay hidden while `PHONE` is blank), and update `CONTACT_EMAIL` in `js/main.js`.
3. Quote form: it opens the visitor's email app pre-filled. To collect submissions directly, create a Formspree form and add `action="https://formspree.io/f/XXXX" method="POST"` to the `quote-form` in `_src/build.py`.
4. Swap stock photos in `assets/img/` for real job photos when available (keep the same file names).
5. Add the site to Google Search Console and Google Business Profile.

# Cardinal

A free, account-free daily affirmations site: 160 original affirmations across eight categories (success, health, wealth, happiness, confidence, relationships, sleep, gratitude), a card generator, and a "write your own" journal tool. Plain HTML/CSS/JS — no framework, no build step required to deploy, built the same way as your sudostudy.online project.

"Cardinal" is a placeholder brand name (plays on "card" + "primary/cardinal direction") — easy to rename. See **Renaming the brand** below.

## What's here

```
index.html              homepage — today's card + category tabs + tool teasers
categories/              8 category pages + an index of all categories
tools/                   generator.html (pull a card) + journal.html (write your own)
blog/                    3 starter posts + index
shop.html                digital products page (not wired to checkout yet)
about.html, disclosure.html, privacy.html, terms.html, 404.html
data/affirmations.json   all 160 affirmations + category metadata — edit this to add more
css/style.css            shared stylesheet
js/main.js               shared script (card pull, favorites, journal, nav)
build.py                 regenerates every HTML page from the data + templates below
```

To add or edit affirmations: edit `data/affirmations.json`, then run `python3 build.py` to regenerate every page. To edit page copy (homepage hero text, blog posts, about page, etc.), edit the relevant function in `build.py` and re-run it. No dependencies beyond Python 3's standard library.

## Local preview

Affirmations are loaded via `fetch()`, which most browsers block on `file://` URLs. Serve the folder locally instead:

```
cd cardinal
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploying to Vercel (free)

Same model as sudostudy.online:

1. Push this folder to a new GitHub repository.
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New → Project**, and import that repo.
3. Framework preset: choose **Other** (it's plain static HTML — no build command, no output directory override needed).
4. Click **Deploy**. You'll get a free `.vercel.app` URL immediately; add your own domain under **Settings → Domains** once you've registered one.

## Before you launch — replace these placeholders

- **Domain**: `robots.txt` and `sitemap.xml` both reference `https://YOURDOMAIN.com` — find/replace once you've picked a real domain.
- **Social links**: the footer links to `instagram.com/` and `youtube.com/` with no handle — update those in `build.py`'s `footer()` function once those accounts exist, then re-run `python3 build.py`.
- **Amazon affiliate links**: the `READING` dictionary near the top of `build.py` has real book recommendations with placeholder links like `?tag=YOUR-ASSOCIATE-TAG`. Replace `YOUR-ASSOCIATE-TAG` with your real Amazon Associates tracking ID (the same kind of tag you set up for sudostudy — if you're targeting Canadian traffic too, set up the separate `associates.ca` program and consider OneLink, as discussed previously) and re-run the build.
- **Contact email**: the footer/legal pages reference "the contact link in the footer" but no email is actually wired up — add a real `mailto:` link once you have one.

## Setting up monetization

**Display ads (Google AdSense)**
1. Apply at [google.com/adsense](https://www.google.com/adsense) once the site is live with real content (the privacy policy already covers ad cookies, which AdSense requires).
2. Once approved, replace the `.ad-slot` placeholder `<div>`s (currently in each category page) with your AdSense `<script>`/`<ins>` snippet.

**Affiliate links (Amazon Associates)**
Already wired into each category page via the `READING` dictionary in `build.py` — just swap in your real tag (see above). Each link already includes `rel="nofollow sponsored noopener"` and a visible disclosure, both of which matter for Amazon's program terms and FTC compliance.

**Digital products (shop.html)**
The shop page has three placeholder products with "Notify me" buttons that scroll to an email capture — there's no checkout yet. Two simple options:
- **Gumroad** — fastest to set up. Create a product, get the checkout link, and swap each product's "Notify me" button for a direct link to that Gumroad checkout page.
- **Stripe Payment Links** — slightly more setup, lower fees at higher volume, no Gumroad branding.
Either way, you'd actually need to create the PDFs/audio first — the product names and descriptions in `shop.html` (Affirmation Card Deck, 30-Day Filed Journal, Audio Pack) are real proposed products, not filler.

**Email list**
The newsletter form on the homepage, shop page, and footer is currently a stub (see `initNewsletterForms()` in `js/main.js`) — it just shows a "Thanks" toast and doesn't send anywhere. To connect it for real:
1. Pick a provider with a free tier — Beehiiv, ConvertKit, and Mailchimp all work well for this kind of list.
2. Most providers give you either a hosted form (swap the `<form>` action) or an API endpoint. Update `initNewsletterForms()` in `js/main.js` to POST to that endpoint instead of just showing the toast.
3. Update `privacy.html`'s "Email subscriptions" section to name the actual provider you chose.

## Content & growth roadmap

- **More categories**: manifestation/spirituality, career & productivity, parenting, and grief/healing all came up in research as natural next additions once the core eight are getting traffic.
- **More blog posts**: three are live as a starting structure (`build.py`'s `BLOG_POSTS` list) — each new post needs a slug, date, title, excerpt, and HTML body added there.
- **Instagram/YouTube**: short-form video performs best in this space — think a 5–10 second card-pull clip with the affirmation as on-screen text, posted daily, pulling directly from `data/affirmations.json` so social and site content stay identical. Founder-story content (why this exists, the research behind it) tends to outperform pure quote graphics, similar to how your sudostudy LinkedIn posts worked — consider a recurring "why I built this" or "the research behind today's card" series.
- **Future app**: the generator and journal tools are deliberately framework-free and built directly against `data/affirmations.json`, so that same data file can be reused as-is in a future React Native or Capacitor-wrapped app without re-authoring content.

## A note on the audience

Research across comparable sites (ThinkUp, "I Am", affirmations.online) points toward breadth-by-category outperforming a narrow demographic focus for this kind of content — people don't browse affirmations as "a millennial" or "a parent," they browse by what they're dealing with that day. That's why this site is organized as eight life-domain categories for a broad self-improvement audience, rather than narrowed to one age group, gender, or niche. If you want to specialize later, the category structure makes it easy to lean into whichever drawer is actually getting traffic.

## Renaming the brand

"Cardinal" appears in `build.py` (page titles, the logo in `nav()`/`footer()`), `data/affirmations.json` is brand-agnostic, and `css/style.css`/`js/main.js` don't reference the name at all. To rename: update the title strings and `<a class="logo">Cardinal<span class="dot">.</span></a>` markup in `build.py`, then re-run `python3 build.py`.

#!/usr/bin/env python3
"""
build.py — generates the Motivation Affirmation static site.

Run this whenever you edit data/affirmations.json or the page content
below, and it will rewrite the HTML files. No dependencies beyond the
Python standard library. No build step is required to *deploy* the
site — the output is plain HTML/CSS/JS that Vercel (or any static host)
serves as-is.

Usage:
    python3 build.py
"""
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT_DIR, "data", "affirmations.json"), encoding="utf-8"))
CATS = {c["slug"]: c for c in DATA["categories"]}
AFFS = DATA["affirmations"]

FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&'
    'family=Poppins:wght@300;400;500;600&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
)


def head(title, description, root="", body_class=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Motivation Affirmation</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
<meta property="og:title" content="{title} — Motivation Affirmation">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
{FONTS_LINK}
<link rel="stylesheet" href="/css/style.css">
</head>
<body data-root="/"{(' class="' + body_class + '"') if body_class else ''}>
'''


def nav(root="", current=""):
    items = [
        ("home", "/index.html", "Today\u2019s Card"),
        ("categories", "/categories/index.html", "Categories"),
        ("tools", "/tools/index.html", "Tools"),
        ("blog", "/blog/index.html", "Blog"),
        ("shop", "/shop.html", "Shop"),
        ("about", "/about.html", "About"),
    ]
    links = "".join(
        f'<a href="{path}"{" class=\"current\"" if key == current else ""}>{label}</a>'
        for key, path, label in items
    )
    return f'''<nav class="site-nav">
  <div class="wrap">
    <a href="/index.html" class="logo"><img src="/images/logo.png" alt="Motivation Affirmation" class="logo-img"></a>
    <button class="nav-toggle" aria-label="Toggle navigation">MENU</button>
    <div class="nav-links">{links}</div>
  </div>
</nav>
'''


def footer(root=""):
    return f'''<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a href="/index.html" class="logo"><img src="/images/logo.png" alt="Motivation Affirmation" class="logo-img"></a>
        <p style="margin-top:14px;color:var(--canvas-text-faint);max-width:280px;">
          Daily affirmations for women ready to rise. Pull one when you need it, or write your own.
        </p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/categories/success.html">Success</a></li>
          <li><a href="/categories/health.html">Health</a></li>
          <li><a href="/categories/wealth.html">Wealth</a></li>
          <li><a href="/categories/index.html">All categories</a></li>
        </ul>
      </div>
      <div>
        <h4>Motivation Affirmation</h4>
        <ul>
          <li><a href="/tools/index.html">Tools</a></li>
          <li><a href="/blog/index.html">Blog</a></li>
          <li><a href="/shop.html">Shop</a></li>
          <li><a href="/about.html">About</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="/privacy.html">Privacy</a></li>
          <li><a href="/terms.html">Terms</a></li>
          <li><a href="/disclosure.html">Affiliate disclosure</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Motivation Affirmation.</span>
      <span><a href="https://instagram.com/motivationaffirmation" target="_blank" rel="noopener">Instagram</a> &middot; <a href="https://youtube.com/@motivationaffirmation" target="_blank" rel="noopener">YouTube</a> &middot; <a href="https://pinterest.com/motivationaffirmation" target="_blank" rel="noopener">Pinterest</a></span>
    </div>
  </div>
</footer>
<script src="/js/main.js"></script>
</body>
</html>
'''


def page(title, description, root, current, body_html, body_class=""):
    return head(title, description, root, body_class) + nav(root, current) + body_html + footer(root)


def write(path, html):
    full = os.path.join(ROOT_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def pad(n):
    return str(n).zfill(4)


def affirmation_card(a, with_actions=True, root=""):
    actions = (
        '<div class="card-actions">'
        '<button class="icon-btn" data-fav-toggle>\u2606 Save</button>'
        '<button class="icon-btn" data-copy-toggle>Copy</button>'
        '</div>' if with_actions else ""
    )
    cat = CATS[a["category"]]
    cat_slug = a["category"]
    img_header = (
        f'<div class="card-image-header">'
        f'<img src="/images/categories/{cat_slug}.jpg" alt="" loading="lazy" '
        f'onerror="this.parentElement.style.display=\'none\'">'
        f'</div>'
    )
    logo_mark = (
        f'<img src="/images/logo.png" alt="" class="card-logo" loading="lazy">'
    )
    return f'''<div class="card card--img" data-card-id="{a['id']}">
  {img_header}
  <div class="card-meta"><span>CARD NO. {pad(a['id'])}</span><span>FILED: {cat['tab']}</span></div>
  <div class="card-body">
    <p class="card-quote">\u201c{a['text']}\u201d</p>
    {actions}
  </div>
  {logo_mark}
</div>'''


# ---------------------------------------------------------------------------
# Per-category "further reading" — one real, relevant book + a placeholder
# Amazon affiliate link. Swap in your own Associates tag (see README.md).
# ---------------------------------------------------------------------------
READING = {
    "success": ("Atomic Habits", "James Clear", "https://www.amazon.com/dp/0735211299?tag=YOUR-ASSOCIATE-TAG"),
    "health": ("Why We Sleep", "Matthew Walker", "https://www.amazon.com/dp/1501144316?tag=YOUR-ASSOCIATE-TAG"),
    "wealth": ("I Will Teach You to Be Rich", "Ramit Sethi", "https://www.amazon.com/dp/1523505745?tag=YOUR-ASSOCIATE-TAG"),
    "happiness": ("The Happiness Project", "Gretchen Rubin", "https://www.amazon.com/dp/0061583251?tag=YOUR-ASSOCIATE-TAG"),
    "confidence": ("The Confidence Gap", "Russ Harris", "https://www.amazon.com/dp/1590309792?tag=YOUR-ASSOCIATE-TAG"),
    "relationships": ("Attached", "Amir Levine & Rachel Heller", "https://www.amazon.com/dp/1585429139?tag=YOUR-ASSOCIATE-TAG"),
    "sleep": ("Why We Sleep", "Matthew Walker", "https://www.amazon.com/dp/1501144316?tag=YOUR-ASSOCIATE-TAG"),
    "gratitude": ("The Gratitude Diaries", "Janice Kaplan", "https://www.amazon.com/dp/1101906583?tag=YOUR-ASSOCIATE-TAG"),
}

BLOG_LINK_FOR_CATEGORY = {
    "success": ("affirmations-for-career-growth", "Affirmations for Career Growth: What to Say Before the Meeting"),
    "health": ("build-affirmation-practice-that-survives-bad-week", "How to Build an Affirmation Practice That Survives a Bad Week"),
    "wealth": ("wealth-affirmations-that-dont-feel-fake", "How to Write Wealth Affirmations That Don't Feel Like Lies"),
    "happiness": ("gratitude-behind-every-affirmation", "The Gratitude Practice Behind Every Effective Affirmation"),
    "confidence": ("confidence-loop-how-affirmations-build-self-trust", "The Confidence Loop: How Affirmations Build Self-Trust Over Time"),
    "relationships": ("relationship-affirmations-boundaries", "Relationship Affirmations: Setting Boundaries Without the Guilt Spiral"),
    "sleep": ("sleep-affirmations-wind-down", "Sleep Affirmations: How to Use Words to Wind Down Your Nervous System"),
    "gratitude": ("gratitude-behind-every-affirmation", "The Gratitude Practice Behind Every Effective Affirmation"),
}


def build_home():
    cats_tabs = "".join(
        f'<a href="categories/{c["slug"]}.html" class="tab">{c["tab"]}</a>' for c in DATA["categories"]
    )
    blog_cards = "".join(
        f'''<div class="card">
  <div class="card-meta"><span>{p['date']}</span><span>FILED: BLOG</span></div>
  <div class="card-body">
    <h3 style="font-family:var(--font-display);font-style:italic;font-size:1.15rem;margin-bottom:8px;">{p['title']}</h3>
    <p style="color:var(--ink-faint);font-size:0.92rem;">{p['excerpt']}</p>
    <div class="card-actions"><a class="icon-btn" href="blog/{p['slug']}.html">Read \u2192</a></div>
  </div>
</div>''' for p in BLOG_POSTS[:3]
    )
    body = f'''
<header class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">YOUR DAILY AFFIRMATION \u2014 RE-FILED EVERY MORNING</p>
      <h1>Pull today\u2019s card.</h1>
      <p class="lede">480 affirmations across success, health, wealth, happiness, confidence, relationships, sleep, and gratitude. Pull one when you need it, or write your own \u2014 the one that\u2019s actually true for you today.</p>
      <div class="hero-actions">
        <a href="categories/index.html" class="btn btn-outline">Browse the drawer</a>
        <a href="tools/journal.html" class="btn btn-outline">Write your own</a>
      </div>
    </div>
    <div class="card-stack" data-hero-pull>
      <div class="card ghost-1"></div>
      <div class="card ghost-2"></div>
      <div class="card pulled">
        <div class="card-meta"><span>CARD NO. \u2014</span><span>FILED: \u2014</span></div>
        <div class="card-body">
          <p class="card-quote">Loading\u2026</p>
        </div>
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="card-stack pull-btn-row" style="height:auto;max-width:none;">
      <button class="btn btn-stamp" data-pull-btn>Pull another card</button>
    </div>
  </div>
  <div class="wrap">
    <p class="eyebrow moss" style="margin-top:40px;">FILED UNDER</p>
    <div class="tab-row">{cats_tabs}</div>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">THE TOOLS</p>
        <h2>Two ways to use Motivation Affirmation</h2>
      </div>
    </div>
    <div class="tool-grid">
      <div class="tool-card">
        <p class="eyebrow">GENERATOR</p>
        <h3>Pull a card from any drawer</h3>
        <p>Filter by category, generate a card, save your favorites. No account, nothing leaves your browser.</p>
        <a href="tools/generator.html" class="btn btn-stamp">Open the generator</a>
      </div>
      <div class="tool-card">
        <p class="eyebrow moss">JOURNAL</p>
        <h3>Write the one that\u2019s actually true</h3>
        <p>Self-written affirmations tend to outperform generic ones \u2014 this tool gives you a simple framework and files what you write.</p>
        <a href="tools/journal.html" class="btn btn-outline">Start writing</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">FROM THE BLOG</p>
        <h2>Notes on the practice</h2>
      </div>
      <a href="blog/index.html" class="see-all">All posts \u2192</a>
    </div>
    <div class="fan-grid">{blog_cards}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="subscribe-card">
      <div>
        <p class="eyebrow">DAILY DISPATCH</p>
        <h2>One card, picked for you, every morning.</h2>
        <p style="color:var(--ink-faint);margin-top:10px;">Free, always. One affirmation delivered to your inbox each day \u2014 specific to a category you can actually use that morning.</p>
      </div>
      <div>
        <form class="subscribe-form" data-newsletter-form>
          <input type="email" placeholder="you@email.com" required aria-label="Email address">
          <button type="submit" class="btn btn-ink">Subscribe</button>
        </form>
        <p class="form-note">Free, always. Unsubscribe in one click.</p>
      </div>
    </div>
  </div>
</section>
'''
    write("index.html", page("Daily Affirmations & Motivation", "Pull a daily affirmation across success, health, wealth, happiness, confidence, relationships, sleep, and gratitude. Free generator and self-write journal tool.", "", "home", body))


def build_categories_index():
    cards = "".join(
        f'''<div class="card" style="min-height:170px;">
  <div class="card-meta"><span>DRAWER</span><span>{c['tab']}</span></div>
  <div class="card-body">
    <h3 style="font-family:var(--font-display);font-style:italic;">{c['label']}</h3>
    <p style="color:var(--ink-faint);font-size:0.92rem;margin:8px 0 14px;">{c['dek']}</p>
    <a class="icon-btn" href="/categories/{c['slug']}.html">Open drawer \u2192</a>
  </div>
</div>''' for c in DATA["categories"]
    )
    personal_card = '''<div class="card" style="min-height:170px;">
  <div class="card-meta"><span>DRAWER</span><span>YOURS</span></div>
  <div class="card-body">
    <h3 style="font-family:var(--font-display);font-style:italic;">My Personal Affirmations</h3>
    <p style="color:var(--ink-faint);font-size:0.92rem;margin:8px 0 14px;">Affirmations you wrote yourself, filed here in your browser. Private, always.</p>
    <a class="icon-btn" href="/categories/personal.html">Open drawer \u2192</a>
  </div>
</div>'''
    body = f'''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">THE FULL DRAWER</p>
    <h1>Eight categories. One drawer.</h1>
    <p class="lede">Affirmations work best when they\u2019re specific to what you\u2019re actually facing \u2014 these are sorted so you can go straight to it instead of scrolling past 150 that don\u2019t apply.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="fan-grid">{cards}{personal_card}</div>
  </div>
</section>
'''
    write("categories/index.html", page("All Categories", "Browse all eight affirmation categories: success, health, wealth, happiness, confidence, relationships, sleep, and gratitude.", "/", "categories", body))


def build_category_pages():
    for slug, cat in CATS.items():
        items = [a for a in AFFS if a["category"] == slug]
        cards = "".join(affirmation_card(a, root="/") for a in items)
        book_title, book_author, book_link = READING[slug]
        blog_slug, blog_title = BLOG_LINK_FOR_CATEGORY[slug]
        body = f'''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">FILED: {cat['tab']}</p>
    <h1>{cat['label']}</h1>
    <p class="lede">{cat['intro']}</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="fan-grid" data-category-grid>{cards}</div>

    <div class="ad-slot">AD SLOT \u2014 e.g. Google AdSense in-feed unit (300\u00d7250 or responsive)</div>

    <div class="tool-card" style="margin-top:36px;">
      <p class="eyebrow moss">KEEP READING</p>
      <h3 style="margin-bottom:10px;">{blog_title}</h3>
      <p style="margin-bottom:18px;">More on how to actually use these \u2014 not just read them.</p>
      <a href="/blog/{blog_slug}.html" class="btn btn-outline">Read the post</a>
    </div>

    <p class="affiliate-note">
      If you want to go deeper on {cat['label'].lower()}, we recommend <a href="{book_link}" target="_blank" rel="nofollow sponsored noopener">{book_title} by {book_author}</a>.
      That\u2019s an affiliate link \u2014 if you buy through it, Motivation Affirmation earns a small commission at no extra cost to you. See our <a href="/disclosure.html">affiliate disclosure</a>.
    </p>
  </div>
</section>
'''
        write(f"categories/{slug}.html", page(cat["label"], f"{len(items)} {cat['label'].lower()} affirmations you can read, save, or copy. {cat['dek']}", "/", "categories", body))


# ---------------------------------------------------------------------------
# Blog posts. Add more entries here (and to BLOG_POSTS) to grow the blog —
# each needs a unique slug, date, title, excerpt, and an html "body".
# ---------------------------------------------------------------------------
BLOG_POSTS = [
    {
        "slug": "why-affirmations-actually-work",
        "date": "Jun 3, 2026",
        "title": "Why Affirmations Actually Work",
        "excerpt": "The psychology behind self-affirmation, why generic ones can backfire, and what actually makes a statement stick.",
        "body": '''
<p>The research behind affirmations didn\u2019t come from the self-help shelf. It came out of a Stanford psychology lab in the late 1980s, where a researcher named Claude Steele was trying to understand something narrower than \u201chow to feel good\u201d \u2014 he wanted to know how people protect their sense of being a fundamentally decent, capable person when they\u2019re confronted with something that threatens that belief.</p>
<p>What he found became known as self-affirmation theory, and the mechanism is a little different from what most affirmation apps imply. It\u2019s not that repeating a sentence enough times tricks your brain into believing it. It\u2019s that affirming something true and important about yourself in one area of life \u2014 your values, a past success, a relationship \u2014 makes you less defensive and more open when something else feels threatening. You\u2019re not erasing the threat. You\u2019re reminding yourself that the threat isn\u2019t the whole story.</p>
<h2>Why some affirmations feel fake</h2>
<p>This explains why a certain kind of affirmation falls flat. \u201cI am a millionaire\u201d, said by someone checking their overdraft fee, isn\u2019t affirming anything \u2014 it\u2019s contradicting observable reality, and most people\u2019s brains push back on that rather than absorb it. The statements that hold up are the ones you could defend in an argument: not \u201cI am wealthy\u201d but \u201cI\u2019m someone who\u2019s learning to manage money well.\u201d One is a claim. The other is closer to a fact you\u2019re actively building evidence for.</p>
<blockquote>The brain doesn\u2019t need to be fooled. It needs to be reminded of evidence it already has.</blockquote>
<h2>Specific beats generic</h2>
<p>This is also the case for writing your own affirmations rather than only picking from a list. A template can\u2019t know that your version of patience shows up specifically at 7pm with a toddler who needs one more book, or that your version of discipline is answering the hard email after four drafts instead of zero. When you write the specific version, you\u2019re forced to locate a real moment as proof \u2014 and that proof is what makes the statement land differently than a generic one ever could.</p>
<p>That doesn\u2019t mean pre-written affirmations are useless \u2014 they\u2019re a fast way to cover ground on a day you don\u2019t have the energy to write anything, and a good starting point for noticing which categories you actually need. But the version that does the most work is usually the one you wrote yourself, about something that actually happened.</p>
<h2>How to use both</h2>
<p>A practical split: use the <a href="/tools/generator.html">generator</a> on busy mornings when you need something fast and broadly relevant. Use the <a href="/tools/journal.html">journal</a> tool on the days something specific is on your mind \u2014 a hard conversation coming up, a goal you\u2019re wavering on \u2014 and write the one sentence that\u2019s actually true about how you\u2019ve handled this kind of thing before.</p>
'''
    },
    {
        "slug": "two-minute-morning-ritual",
        "date": "May 22, 2026",
        "title": "A 2-Minute Morning Affirmation Ritual You\u2019ll Actually Keep",
        "excerpt": "Most affirmation routines die in week two because they\u2019re too long. Here\u2019s a version short enough to survive a Tuesday.",
        "body": '''
<p>Most affirmation routines fail for a boring reason: they\u2019re designed for the version of you that has a calm, unhurried morning, and most mornings aren\u2019t that. A 15-minute journaling-plus-affirmations-plus-visualization routine sounds great on a Sunday and gets skipped by Wednesday. The fix isn\u2019t more willpower. It\u2019s a smaller ritual that survives contact with an actual weekday.</p>
<h2>The whole thing, in four steps</h2>
<p><strong>1. Pull one card (10 seconds).</strong> Before you check your phone \u2014 not after \u2014 open the <a href="/tools/generator.html">generator</a> or grab today\u2019s card on the homepage. Don\u2019t overthink the category. Whatever shows up, shows up.</p>
<p><strong>2. Say it out loud, once, slowly (20 seconds).</strong> Not in your head. Out loud, even quietly. Hearing your own voice say it engages a different part of attention than silently reading does.</p>
<p><strong>3. Name where it applies today (30 seconds).</strong> This is the step people skip, and it\u2019s the one that matters most. If the card says something about confidence, name the actual meeting or conversation today where that\u2019s relevant. This turns an abstract sentence into a specific intention.</p>
<p><strong>4. One breath, then go.</strong> That\u2019s it. The ritual ends here on purpose \u2014 it should feel almost too short, not impressively long.</p>
<h2>Anchor it to something you already do</h2>
<p>The version of this that actually survives long-term isn\u2019t the one you remember to do \u2014 it\u2019s the one attached to something you were already going to do anyway. Pull your card while the coffee brews. While you wait for the shower to heat up. While your toothbrush timer runs. Borrowing two minutes from an existing habit removes the need to remember a new one.</p>
<h2>Aim for return rate, not streaks</h2>
<p>Streak culture quietly punishes you for missing one day by making the whole habit feel broken. A more honest goal: how many days out of seven did you come back to it, on average, over a month? Four out of seven, sustained for months, beats a seven-day streak that collapses and never restarts. Missing a morning doesn\u2019t undo the ones before it.</p>
'''
    },
    {
        "slug": "write-your-own-affirmations",
        "date": "Jun 17, 2026",
        "title": "Write Your Own Affirmations: A Simple Framework That Actually Works",
        "excerpt": "Situation, strength, statement \u2014 a three-step way to write an affirmation that's actually true instead of just hopeful.",
        "body": '''
<p>\u201cWrite your own affirmations\u201d is good advice that\u2019s rarely followed, mostly because nobody explains what to actually write. Staring at a blank line and trying to invent a confident-sounding sentence about your own life is harder than it sounds \u2014 it either comes out vague (\u201cI am strong\u201d) or wishful (\u201cI am completely fearless\u201d), and neither version holds up under any real pressure.</p>
<p>A more reliable approach is to work backward from something that actually happened, using three short prompts.</p>
<h2>The framework</h2>
<p><strong>Situation \u2014 </strong>what specifically are you facing, or did you recently face? Not \u201clife in general\u201d \u2014 one real moment. \u201cAsking my manager for a raise.\u201d \u201cThe morning my kid wouldn\u2019t get in the car and we were already late.\u201d \u201cLooking at my bank balance before payday.\u201d</p>
<p><strong>Strength \u2014 </strong>what did you actually draw on, or could you draw on, to handle it? Be specific and modest \u2014 \u201cI stayed calm for ninety more seconds than I wanted to\u201d counts more than \u201cI was a perfect parent.\u201d</p>
<p><strong>Statement \u2014 </strong>now write one present-tense sentence that connects the two. Not a prediction (\u201cI will handle this\u201d) and not a fantasy (\u201cI never struggle with this\u201d) \u2014 a present-tense claim you can actually defend: \u201cI can stay calm longer than I think I can.\u201d</p>
<h2>Two worked examples</h2>
<p><em>Situation:</em> Sending a pitch email I\u2019d rewritten four times. <em>Strength:</em> I sent it anyway instead of waiting for a fifth draft. <em>Statement:</em> \u201cI finish and send, even when it isn\u2019t perfect yet.\u201d</p>
<p><em>Situation:</em> A friend canceled plans last-minute, again. <em>Strength:</em> I said how I felt instead of pretending it was fine. <em>Statement:</em> \u201cI can say something hurt without making it a bigger fight than it needs to be.\u201d</p>
<h2>Where to put it</h2>
<p>Once you\u2019ve got a statement you\u2019d actually stand behind, file it in the <a href="/tools/journal.html">journal tool</a> \u2014 it walks you through these same three prompts and keeps everything you write filed in your browser, with nothing sent anywhere. Write one a week, not one a day. The framework works because each one is specific; specific takes a little longer, and that\u2019s fine.</p>
'''
    },
    {
        "slug": "morning-affirmations-science",
        "date": "Jun 10, 2026",
        "title": "The Science of Morning Affirmations: Why Timing Actually Matters",
        "excerpt": "Your brain is most receptive to new input in the first hour after waking. Here's how to use that window on purpose.",
        "body": '''
<p>The idea that mornings are special isn\u2019t just motivational-poster wisdom. There\u2019s a real neurological reason why the first hour after waking is different from any other hour of the day \u2014 and once you understand it, the timing of when you do your affirmation practice starts to make more sense.</p>
<h2>The alpha-wave window</h2>
<p>When you first wake up, your brain spends roughly twenty to thirty minutes in a transitional state between the theta waves of sleep and the beta waves of alert, focused thinking. During this window, the brain produces elevated alpha waves \u2014 the same state associated with meditation, light hypnosis, and creative flow. It\u2019s a state of relaxed, open receptivity rather than critical analysis.</p>
<p>This matters for affirmations because the prefrontal cortex \u2014 the part of the brain responsible for skeptical evaluation and internal self-criticism \u2014 is less dominant in this window. A sentence like \u201cI handle difficult conversations calmly\u201d is more likely to land as plausible in this state than it would at 3pm when your critical thinking is in full gear and you can immediately name three counterexamples.</p>
<h2>It\u2019s not magic, but the mechanism is real</h2>
<p>None of this means mornings are magic and that reading affirmations at 7am will automatically reprogram your subconscious. What it means is that the morning window is lower-friction for taking in new self-referential information. Your brain is primed to absorb input rather than evaluate it.</p>
<blockquote>The affirmation doesn\u2019t work better at 7am. You\u2019re less likely to argue with it at 7am.</blockquote>
<h2>How to use the window</h2>
<p>The key is catching it before your phone catches you. Every notification you check after waking pulls your brain into beta-wave alertness \u2014 the critical, responsive, problem-solving state \u2014 before the alpha window has had time to do anything useful. Checking social media before your affirmation practice is essentially skipping the practice.</p>
<p>A practical sequence: phone face-down until after you\u2019ve done your card pull. Even two minutes before you look at anything is better than zero. Pull a card from the <a href="/tools/generator.html">generator</a>, say it once out loud slowly, and then go ahead and check your phone. The whole thing takes ninety seconds and costs nothing.</p>
<h2>What about evening?</h2>
<p>The other useful window is just before sleep, when your brain is moving in the opposite direction \u2014 back into theta waves as you drift off. The statements you say to yourself in the last ten minutes before sleep have an outsized influence on how your brain consolidates the day\u2019s experience. Gratitude affirmations work especially well here: they give your brain something to file as significant rather than leaving the unconscious to categorize the day on its own.</p>
'''
    },
    {
        "slug": "wealth-affirmations-that-dont-feel-fake",
        "date": "Jun 5, 2026",
        "title": "How to Write Wealth Affirmations That Don\u2019t Feel Like Lies",
        "excerpt": "\"I am a millionaire\" lands differently when you're checking your overdraft. Here's what actually works instead.",
        "body": '''
<p>Wealth affirmations have a credibility problem. Most of the popular ones \u2014 \u201cmoney flows to me easily,\u201d \u201cI am a money magnet,\u201d \u201cI am abundant in all areas of my life\u201d \u2014 feel absurd to say when you\u2019re actively stressed about money. And when an affirmation feels absurd, your brain doesn\u2019t absorb it. It argues with it.</p>
<p>The reason isn\u2019t that affirmations don\u2019t work for wealth. It\u2019s that most wealth affirmations are claims, not truths. And your brain knows the difference.</p>
<h2>The gap problem</h2>
<p>When the distance between what you\u2019re saying and what\u2019s demonstrably true is too large, an affirmation triggers something called psychological reactance \u2014 your brain pushes back against a statement it reads as false. \u201cI am wealthy\u201d said while looking at a bank balance that contradicts it doesn\u2019t create belief. It creates resistance.</p>
<p>The statements that work are the ones you could defend in a conversation. Not \u201cI am wealthy\u201d but \u201cI am someone who is actively building a better relationship with money.\u201d Not \u201cmoney flows easily to me\u201d but \u201cI make clearer money decisions than I did a year ago.\u201d These aren\u2019t as exciting to say. They hold up under scrutiny.</p>
<h2>Three frameworks that work</h2>
<p><strong>Identity-based:</strong> \u201cI am the kind of person who checks my finances clearly and without shame.\u201d You\u2019re not claiming a result. You\u2019re claiming a behavior that\u2019s already at least partially true.</p>
<p><strong>Direction-based:</strong> \u201cEvery decision I make today is moving me toward financial security.\u201d This is present-tense and true as long as you make one good decision today \u2014 even a small one.</p>
<p><strong>Capacity-based:</strong> \u201cI am capable of learning to earn more, save more, and manage money well.\u201d Nobody can argue this is false. It\u2019s the same sentence that\u2019s true for almost anyone with a functioning brain and internet access.</p>
<h2>What to do with the big dreams</h2>
<p>The big aspirational statements (\u201cI am a millionaire\u201d) aren\u2019t useless \u2014 they\u2019re just better used as visualization fuel than as morning affirmations. In a journaling context, where you\u2019re deliberately building a mental picture of a future state, they have a place. As a statement you say to yourself every morning while your bank account disagrees, they don\u2019t.</p>
<p>Start with the affirmations in the <a href="/categories/wealth.html">Wealth drawer</a> \u2014 they\u2019re written to be true at multiple income levels and stages of the financial journey.</p>
'''
    },
    {
        "slug": "affirmations-for-anxiety",
        "date": "May 30, 2026",
        "title": "Affirmations for Anxiety: What the Research Says vs. What Actually Helps",
        "excerpt": "Anxiety doesn\u2019t respond to \u201cI am calm.\u201d Here\u2019s what to say to a nervous system that\u2019s already on high alert.",
        "body": '''
<p>If you\u2019ve ever tried to talk yourself out of anxiety with a positive statement and had it make things worse, you\u2019re not alone and you\u2019re not doing it wrong. Anxiety has a specific relationship with positive self-talk that\u2019s different from how it responds to other kinds of cognitive reframing \u2014 and understanding the difference explains why some affirmations help and others backfire.</p>
<h2>The problem with \u201cI am calm\u201d</h2>
<p>When you\u2019re anxious, your nervous system is in a state of perceived threat. Saying \u201cI am calm\u201d while your heart is racing and your thoughts are spiraling doesn\u2019t calm the nervous system \u2014 it creates a contradiction that the nervous system reads as additional information to process. Research by Joanne Wood at the University of Waterloo found that self-affirming positive statements can actually increase negative mood in people with low self-esteem or in states of emotional distress \u2014 exactly the population most likely to be reaching for an anxiety affirmation.</p>
<h2>What works instead: acceptance framing</h2>
<p>The affirmations that actually reduce anxiety are the ones that don\u2019t try to replace the anxious feeling \u2014 they acknowledge it while reframing the relationship to it. Compare:</p>
<p><strong>Doesn\u2019t work:</strong> \u201cI am calm and at peace.\u201d (Your body knows this isn\u2019t true right now.)</p>
<p><strong>Works better:</strong> \u201cI can be anxious and still handle this.\u201d (True. Has been true before. Your body can\u2019t argue.)</p>
<p>The second version doesn\u2019t try to eliminate the anxiety. It removes the anxiety about being anxious \u2014 which is often what\u2019s actually making things worse.</p>
<h2>Grounding affirmations vs. aspiration affirmations</h2>
<p>For anxiety specifically, grounding affirmations outperform aspiration affirmations almost every time. A grounding affirmation is any statement anchored to present reality: \u201cI have handled situations like this before.\u201d \u201cRight now, in this moment, I am safe.\u201d \u201cMy nervous system is doing its job. I don\u2019t have to fix it \u2014 I just have to let it run.\u201d</p>
<p>These work because they give the nervous system accurate information rather than contradictory information. The nervous system responds to evidence. Give it evidence.</p>
<h2>The breath connection</h2>
<p>The most effective anxiety affirmation practice pairs the statement with a physiological intervention. Say your grounding affirmation on the exhale of a slow, extended breath (five counts in, seven counts out). The extended exhale activates the parasympathetic nervous system directly \u2014 and the affirmation anchors to that physical shift rather than fighting the anxiety independently.</p>
<p>The <a href="/categories/sleep.html">Sleep and Calm</a> drawer has affirmations written specifically for high-anxiety moments \u2014 notice they\u2019re all written as acknowledgments rather than contradictions.</p>
'''
    },
    {
        "slug": "say-affirmations-out-loud",
        "date": "May 26, 2026",
        "title": "Why Saying Affirmations Out Loud Works Better Than Reading Them",
        "excerpt": "There\u2019s a specific reason hearing your own voice say something is more effective than silently reading the same words.",
        "body": '''
<p>Most people read their affirmations. A smaller number say them out loud. The ones who say them out loud tend to report that the practice feels more real and more sticky \u2014 and there\u2019s a straightforward neurological reason why.</p>
<h2>The production effect</h2>
<p>Memory and learning researchers have studied something called the \u201cproduction effect\u201d \u2014 the consistent finding that words you speak aloud are remembered better and processed more deeply than words you read silently. When you say something out loud, you engage motor processing (your lips, throat, and breath), auditory processing (you hear yourself), and the additional attention that speaking requires. The combination creates a richer encoding in memory than silent reading does alone.</p>
<p>For affirmations, this means the statement you say aloud is more likely to become part of your working self-concept than the statement you only read. It registers differently in the brain \u2014 not just as text, but as something you\u2019ve done and heard.</p>
<h2>Your voice has authority over other voices</h2>
<p>There\u2019s a second reason that\u2019s less about neuroscience and more about psychology. Most people have internal critic voices that they recognize as \u201cinternal.\u201d When you read a positive statement silently, that same internal-voice register is doing the reading \u2014 so the affirmation and the self-critic are, in some sense, competing on the same channel.</p>
<p>When you say the affirmation out loud and hear it, you\u2019re hearing a version of your voice making a claim about you. The brain processes this differently from internal self-talk. It\u2019s closer to how you process what other people say about you \u2014 which tends to carry more weight than what we say to ourselves internally.</p>
<h2>The volume question</h2>
<p>You don\u2019t need to say it loudly. A quiet voice, a whisper even, still engages the production effect. The key is that the sound exits your body and re-enters through your ears. This can be done privately, in a parked car, in the shower, in the first quiet moment of a morning before other people wake up.</p>
<blockquote>The version of this practice that works is the one quiet enough to do anywhere.</blockquote>
<h2>Adding specific intention</h2>
<p>After you say the affirmation out loud, add one specific sentence: where does this apply today? \u201cI handle difficult conversations calmly\u201d becomes \u201cI handle difficult conversations calmly \u2014 specifically the one I have with my manager at 2pm today.\u201d The specificity takes ten seconds and the anchoring effect is significantly stronger.</p>
<p>The <a href="/tools/generator.html">generator tool</a> is built for exactly this two-step practice: pull a card, say it out loud, name where it applies.</p>
'''
    },
    {
        "slug": "confidence-loop-how-affirmations-build-self-trust",
        "date": "May 20, 2026",
        "title": "The Confidence Loop: How Affirmations Build Self-Trust Over Time",
        "excerpt": "Confidence isn\u2019t a feeling you wait for. It\u2019s a pattern you build \u2014 and affirmations are one way to build it deliberately.",
        "body": '''
<p>Confidence is misunderstood. Most people experience it as a feeling \u2014 a warm certainty that they can handle what\u2019s coming \u2014 and assume you either have it or you don\u2019t in a given situation. But that\u2019s not how confidence actually develops. It\u2019s a pattern, not a state, and it\u2019s built through a specific mechanism that affirmations are well-positioned to reinforce.</p>
<h2>The loop</h2>
<p>Behavioral psychologists describe confidence as a loop: action leads to evidence, evidence updates self-belief, updated self-belief makes the next action easier, which generates more evidence. The loop runs in either direction \u2014 a history of avoidance generates its own kind of self-belief (\u201cI\u2019m someone who can\u2019t handle X\u201d) just as a history of action does.</p>
<p>Where affirmations enter this loop is at the self-belief stage. They\u2019re not a replacement for action or evidence \u2014 you can\u2019t affirmation your way to competence without doing the work. But they can shift the self-belief piece in a direction that makes action more likely, which generates the evidence that eventually makes the belief unnecessary.</p>
<h2>What \u201cbuilding self-trust\u201d actually means</h2>
<p>Self-trust isn\u2019t a general feeling of confidence. It\u2019s a specific record of instances where you made a commitment to yourself and kept it \u2014 where you said you\u2019d do the thing and you did it. This is why \u201cI am confident\u201d is a weaker affirmation than \u201cI do the things I said I\u2019d do.\u201d The second one is pointing at an actual track record. The first is making a claim about a feeling.</p>
<p>The most confidence-building affirmations are the ones that reference your own behavior and history rather than your internal states. \u201cI have walked into hard rooms before and come out okay\u201d is an invitation to recall specific evidence. \u201cI am bold and fearless\u201d is not.</p>
<h2>The gap between feeling and doing</h2>
<p>The confidence loop also explains why \u201cact confident even when you don\u2019t feel it\u201d is better advice than it sounds. When you act in spite of nervousness, you generate evidence that nervousness doesn\u2019t stop you \u2014 which is the most useful kind of evidence. An affirmation before the action is a way of mentally rehearsing the doing, not waiting for the feeling.</p>
<p>Read the affirmation, say it out loud, walk in. The confidence catches up after, not before.</p>
<p>Browse the <a href="/categories/confidence.html">Confidence drawer</a> \u2014 those affirmations are written specifically for the moment before you need them, not the moment after.</p>
'''
    },
    {
        "slug": "sleep-affirmations-wind-down",
        "date": "May 14, 2026",
        "title": "Sleep Affirmations: How to Use Words to Wind Down Your Nervous System",
        "excerpt": "A racing mind at 11pm isn\u2019t broken. Here\u2019s how to give it something useful to do instead of reviewing the day.",
        "body": '''
<p>Lying awake at 11pm replaying the meeting, the conversation, the thing you should have said or shouldn\u2019t have \u2014 this is a sign of a nervous system that doesn\u2019t know the day is over. It\u2019s not broken. It\u2019s doing exactly what it evolved to do: running scenarios, solving problems, preparing for what comes next. The issue is that it\u2019s using your rest time to do it.</p>
<h2>Why the mind races at night</h2>
<p>In the day, external demands give your mind something to direct its attention toward. At night, that structure disappears and the brain fills the space with whatever it considers unfinished. Research on default mode network activity \u2014 the neural network that activates when you\u2019re not focused on a task \u2014 shows that it tends to return to self-referential processing at night. Without distractions, this can become a loop.</p>
<h2>What affirmations do to the loop</h2>
<p>An affirmation used at night isn\u2019t trying to solve the problems the mind is circling. It\u2019s giving the mind a different, intentional object to land on \u2014 one that\u2019s less activating than a list of unresolved worries. The mechanism is similar to a mantra in meditation: you\u2019re not stopping thoughts, you\u2019re offering the attention somewhere to return to each time it wanders.</p>
<p>The most effective sleep affirmations are ones that signal completion and safety rather than aspiration. \u201cI\u2019ve done what I can today\u201d works better than \u201cI am successful\u201d because the first one tells the nervous system something is finished. The second one prompts it to start evaluating whether that\u2019s true.</p>
<h2>The practice</h2>
<p>Read slowly. Out loud if you can do so without disturbing anyone \u2014 even a whisper counts. One affirmation is enough. Repeat it a few times on the exhale. Don\u2019t try to believe it completely. Just give your attention something to rest on other than the day\u2019s unfinished list.</p>
<blockquote>You\u2019re not trying to solve anything. You\u2019re giving the mind an off-ramp.</blockquote>
<p>The statements in the <a href="/categories/sleep.html">Sleep and Calm drawer</a> are written specifically for this \u2014 short, non-aspirational, present-tense, focused on release rather than achievement. Read them slowly, not quickly.</p>
'''
    },
    {
        "slug": "gratitude-behind-every-affirmation",
        "date": "May 5, 2026",
        "title": "The Gratitude Practice Behind Every Effective Affirmation",
        "excerpt": "Gratitude and affirmations work through the same mechanism. Once you understand that, both practices get a lot more useful.",
        "body": '''
<p>Gratitude and affirmations are usually treated as separate practices. Gratitude journals on one side, affirmation cards on the other. But they work through the same core mechanism, and understanding that makes both of them more useful.</p>
<h2>The shared mechanism: directed attention</h2>
<p>Gratitude practice doesn\u2019t make your life objectively better. What it does is train your attentional system to notice what\u2019s working \u2014 to register the good alongside the bad rather than filtering it out. Research by Robert Emmons at UC Davis consistently shows that gratitude practitioners don\u2019t report fewer problems; they report noticing more positive things alongside those problems.</p>
<p>Affirmations work the same way. \u201cI am capable of figuring out things I don\u2019t know yet\u201d isn\u2019t creating capability. It\u2019s directing attention toward evidence of capability that already exists \u2014 the times you figured things out, the skills you built that you didn\u2019t have before. You\u2019re training your attention to find the evidence, not generating the evidence from nothing.</p>
<h2>Why this matters for how you write them</h2>
<p>If both practices work through directed attention, then the most effective affirmations are the ones that give your attention something real to find. \u201cI am grateful for my body that got me through today, however it felt\u201d points at actual evidence. \u201cI am perfectly healthy and vibrant\u201d sends your attention looking for evidence that may not exist yet.</p>
<p>The gratitude framing is often easier to land in because it has a built-in humility: \u201cI notice this,\u201d rather than \u201cI claim this.\u201d For people who find affirmations feel fake or forced, reframing them through gratitude often removes the resistance. \u201cI am confident\u201d can feel like a lie. \u201cI am grateful for the times I\u2019ve walked into hard rooms and come out okay\u201d is almost impossible to argue with.</p>
<h2>A combined practice</h2>
<p>One of the most effective short practices: at the end of each day, write one gratitude that also functions as an affirmation. \u201cI\u2019m grateful I sent the email I\u2019d been avoiding \u2014 I do hard things even when I don\u2019t feel like it.\u201d You\u2019re combining the attention-training of gratitude with the identity reinforcement of an affirmation, anchored to real, recent evidence.</p>
<p>Browse both the <a href="/categories/gratitude.html">Gratitude drawer</a> and the <a href="/tools/journal.html">journal tool</a> \u2014 they\u2019re designed to work together.</p>
'''
    },
    {
        "slug": "how-long-do-affirmations-take-to-work",
        "date": "Apr 28, 2026",
        "title": "How Long Does It Take for Affirmations to Work?",
        "excerpt": "The honest answer: it depends on what you mean by \u2018work\u2019 and what you\u2019re measuring. Here\u2019s what the research suggests.",
        "body": '''
<p>This is one of the most common questions about affirmations, and the answer is more nuanced than most sites want to admit. The truthful version: it depends on what you\u2019re measuring, and the timeline is different for different kinds of change.</p>
<h2>What \u201cworking\u201d actually means</h2>
<p>Affirmations don\u2019t work the same way a pill works. There\u2019s no single measurable outcome that appears at week four and confirms the practice is doing something. What tends to happen instead is a gradual shift in the internal narrative \u2014 the automatic stories you tell yourself about your capabilities, your worth, your patterns. These shifts are subtle and often noticed retrospectively.</p>
<p>The changes people typically report: starting to catch self-critical thoughts before they spiral; feeling slightly less resistant to hard tasks; noticing more evidence of the thing they\u2019ve been affirming; feeling less derailed by setbacks. None of these are dramatic. All of them compound.</p>
<h2>What the research timeframes look like</h2>
<p>Studies on self-affirmation typically use one-time or week-long interventions and measure immediate effects on things like stress response, openness to information, and problem-solving behavior. These show measurable effects in short windows \u2014 sometimes within a single session. But these are laboratory effects, not the cumulative real-world changes that people are usually asking about.</p>
<p>For the kind of sustained identity-shift work that most people are looking for \u2014 genuinely feeling different about themselves in a specific area \u2014 most practitioners who report real change describe a timeline of six to twelve weeks of consistent daily practice.</p>
<h2>The consistency problem</h2>
<p>The reason most people don\u2019t get to week twelve is week two. The novelty has worn off, there\u2019s no dramatic evidence of change yet, and the practice feels like it\u2019s not working. This is the dropout point for most behavior-change practices \u2014 not just affirmations. The practices that survive this window are short enough to do on a bad day, attached to something that already exists in the routine, and with a low-enough bar that missing one day doesn\u2019t feel like failure.</p>
<blockquote>Aim for return rate, not perfection. Four out of seven days, sustained, beats seven-day streaks that collapse.</blockquote>
<h2>Measuring the right thing</h2>
<p>One practical way to track progress: at the start of a month, write down one specific belief you\u2019d like to shift (e.g., \u201cI tend to avoid financial conversations\u201d). At the end of the month, compare. You\u2019re not asking whether you feel totally different \u2014 you\u2019re asking whether you\u2019re slightly less automatic, slightly more likely to catch the pattern. Small shifts are the signal.</p>
'''
    },
    {
        "slug": "relationship-affirmations-boundaries",
        "date": "Apr 22, 2026",
        "title": "Relationship Affirmations: Setting Boundaries Without the Guilt Spiral",
        "excerpt": "Saying no to someone you love feels wrong. Here\u2019s what to say to yourself before, during, and after the hard conversation.",
        "body": '''
<p>Boundaries are easier to talk about than to keep. Most people who\u2019ve done any personal development work know intellectually that setting limits with the people they love is healthy and necessary \u2014 and still feel sick with guilt after doing it. The gap between knowing and feeling is exactly where affirmations are most useful.</p>
<h2>Why boundary-setting triggers guilt</h2>
<p>For most people, especially women, the guilt around saying no is not irrational. It\u2019s a learned response to years of messaging \u2014 often from family, culture, and relationships \u2014 that equates care with availability. \u201cIf I really loved this person, I wouldn\u2019t need this limit\u201d is an automatic thought that runs in a lot of people\u2019s minds when they try to hold a boundary, even a completely reasonable one.</p>
<p>Affirmations in this context aren\u2019t trying to eliminate the guilt. They\u2019re offering a counter-narrative to the automatic one \u2014 something to return to when the guilt arrives.</p>
<h2>Before the conversation</h2>
<p>\u201cI can love this person and still hold this limit.\u201d This is worth saying out loud before the conversation because it names what you\u2019re actually doing \u2014 not withdrawing love, not punishing, just maintaining something you need. The guilt comes partly from conflating limits with rejection. Separating them in your own mind first makes the conversation easier.</p>
<h2>During the aftermath</h2>
<p>The guilt usually peaks after, not during. After the conversation, when you\u2019re replaying it and second-guessing, the useful affirmation shifts: \u201cI communicated what I needed, clearly and without cruelty. That\u2019s what I\u2019m supposed to do.\u201d The emphasis is on how you did it, not whether you did it.</p>
<h2>For when the other person pushes back</h2>
<p>\u201cTheir discomfort with my limit is not evidence that the limit is wrong.\u201d This is one of the most important sentences for people who struggle with boundaries \u2014 it reframes the other person\u2019s reaction as information about them rather than feedback on your decision.</p>
<p>Browse the <a href="/categories/relationships.html">Relationships drawer</a> \u2014 those affirmations are written for the full arc of relational life, including the hard parts.</p>
'''
    },
    {
        "slug": "build-affirmation-practice-that-survives-bad-week",
        "date": "Apr 15, 2026",
        "title": "How to Build an Affirmation Practice That Survives a Bad Week",
        "excerpt": "Most habits die in week two. Here\u2019s how to design a practice with enough flex that a hard Tuesday won\u2019t end it.",
        "body": '''
<p>The habits that last aren\u2019t the ones built for ideal conditions. They\u2019re built for bad weeks \u2014 for the mornings you\u2019re running late, the evenings you\u2019re depleted, the Tuesdays where the last thing you want to do is pull a card and say something optimistic to yourself.</p>
<h2>The design problem with most affirmation practices</h2>
<p>Most affirmation practices are designed for ideal versions of the day: \u201cSit in a quiet space. Breathe deeply. Read each affirmation slowly three times. Journal your reflection.\u201d That practice is useful when it happens. It doesn\u2019t survive contact with a real week.</p>
<p>The design principle that makes any habit durable: it should be possible to complete on the worst reasonable day you could have. If the habit requires twenty minutes of quiet reflection and your life doesn\u2019t reliably produce twenty minutes of quiet, the habit is precarious.</p>
<h2>The minimum viable version</h2>
<p>Define what your practice is at its absolute minimum. One card. One read. One breath. That\u2019s it. On easy days you might do more \u2014 say it out loud, anchor it to a specific situation, write a sentence about it. But the minimum version is the anchor. You do the minimum even when you do nothing else.</p>
<p>The minimum version isn\u2019t \u201csettling.\u201d It\u2019s the version that keeps the habit wired, and keeps you a person who does this \u2014 so that on the good days, there\u2019s somewhere to return to.</p>
<h2>Detach from streaks</h2>
<p>Streak culture punishes missing one day by making the habit feel broken. Reframe the metric: how many days out of the last fourteen did you come back to it? Ten out of fourteen is a strong practice. It doesn\u2019t feel like one, but it is.</p>
<blockquote>Missing a day doesn\u2019t undo the ones before it. It\u2019s just a gap, not a reset.</blockquote>
<h2>The re-entry practice</h2>
<p>When you miss a few days and notice it, the re-entry shouldn\u2019t be dramatic. Don\u2019t restart with a long aspirational session to compensate. Just do the minimum version. One card. One read. The practice restarts from where it paused, not from zero.</p>
<p>The <a href="/tools/generator.html">generator</a> is built for exactly this \u2014 fast, frictionless, no account. It should take under sixty seconds to pull a card and say it once.</p>
'''
    },
    {
        "slug": "manifestation-myth-what-affirmations-actually-do",
        "date": "Apr 8, 2026",
        "title": "The Manifestation Myth: What Affirmations Are Actually Doing to Your Brain",
        "excerpt": "Affirmations aren\u2019t magic. The way they actually work is more interesting and more useful than the magic version.",
        "body": '''
<p>Affirmations have an image problem. On one side, there\u2019s the manifesting community, which sometimes implies that saying positive statements will attract external circumstances toward you through energetic alignment. On the other side, there are the skeptics who read those claims and dismiss the entire practice as pseudoscience. Both groups are missing what\u2019s actually happening.</p>
<h2>What affirmations don\u2019t do</h2>
<p>There\u2019s no credible evidence that saying positive statements attracts circumstances from the external world toward you. Saying \u201cI am wealthy\u201d doesn\u2019t cause money to arrive. The universe isn\u2019t listening to your self-talk.</p>
<p>This matters to say clearly because a lot of people approach affirmations with that expectation and then feel like failures when the circumstances don\u2019t change. The practice fails for the wrong reason.</p>
<h2>What affirmations actually do</h2>
<p>What affirmations demonstrably do is influence your behavior, attention, and access to your own capabilities. Self-affirmation research from the past three decades shows consistent effects: reduced defensiveness when receiving critical information; increased persistence on difficult tasks; reduced physiological stress response; improved problem-solving after threat induction.</p>
<p>These effects happen through real mechanisms. Affirming your own values or competence reduces the self-threat that typically causes defensive, avoidant behavior. With less threat in the system, you process information more clearly, take on more challenges, and persist longer. Your behavior changes \u2014 which changes your outcomes \u2014 which changes your circumstances. The external world does shift, but through your changed behavior, not through energetic attraction.</p>
<blockquote>Affirmations work through your actions, not instead of them. That\u2019s more powerful, not less.</blockquote>
<h2>The attention effect</h2>
<p>The second mechanism is attentional. What you train yourself to notice affects what you perceive as possible. An affirmation about capability trains your attention to register evidence of capability \u2014 which was always there, but previously filtered out. You start noticing the times you did handle something, the skills you have that you discount.</p>
<h2>The practical takeaway</h2>
<p>Use affirmations for what they actually do: reduce internal friction on hard tasks, shift your attention toward evidence of your own competence, and reduce defensive avoidance. Don\u2019t use them as a substitute for action. They\u2019re an internal support system for a person who\u2019s already doing the work.</p>
'''
    },
    {
        "slug": "generic-vs-specific-affirmations",
        "date": "Apr 1, 2026",
        "title": "Why Generic Affirmations Work Less Than Specific Ones",
        "excerpt": "\u201cI am enough\u201d is comforting but vague. The more specific the affirmation, the harder it is to argue with.",
        "body": '''
<p>There\u2019s a reason \u201cI am enough\u201d is the most popular affirmation and also one of the least effective ones. It\u2019s comforting in the abstract and almost impossible to anchor to anything concrete. Your brain can agree with it in the moment and then have no idea what to do with it afterward.</p>
<h2>The specificity-credibility connection</h2>
<p>The mechanism behind affirmations involves your brain\u2019s implicit self-concept \u2014 the running model of who you are and what you\u2019re capable of that operates below conscious awareness. When you repeat a statement, you\u2019re either reinforcing an existing belief, introducing a new one, or contradicting an existing one.</p>
<p>Generic statements (\u201cI am confident,\u201d \u201cI am worthy of love,\u201d \u201cI am enough\u201d) are processed abstractly. They don\u2019t point at evidence. They make a claim without supporting it. Your brain can agree with them while simultaneously maintaining the opposite belief in the specific context where it matters.</p>
<h2>How specificity changes this</h2>
<p>A specific affirmation points at evidence. \u201cI have walked into difficult conversations before and said what I needed to say\u201d isn\u2019t a claim \u2014 it\u2019s a recall prompt. Your brain starts looking for instances where this was true. When it finds them, the belief is reinforced by evidence rather than just asserted.</p>
<p>\u201cI am enough\u201d doesn\u2019t give your brain anywhere to look. \u201cI am enough for the work in front of me today, even if I don\u2019t feel ready\u201d gives it a specific claim to evaluate \u2014 and in many cases, that specific claim is true in a way the abstract version isn\u2019t.</p>
<h2>The practical split</h2>
<p>Use the affirmations in the <a href="/categories/index.html">category drawers</a> as fast, broadly applicable options for ordinary days. Use the <a href="/tools/journal.html">journal tool</a> on the days something specific is weighing on you \u2014 when the generic option feels hollow, the specific one you write yourself will do more work.</p>
<h2>The most specific affirmation you can write</h2>
<p>The most powerful format: \u201cThe last time I faced [specific situation], I [specific action]. That\u2019s who I am.\u201d It\u2019s backwards-looking, evidence-based, and almost impossible to argue with \u2014 because you\u2019re not predicting anything. You\u2019re describing something that already happened.</p>
'''
    },
    {
        "slug": "from-skeptic-to-practitioner",
        "date": "Mar 24, 2026",
        "title": "From Sceptic to Practitioner: What Changed When I Started Taking This Seriously",
        "excerpt": "If you find affirmations cringey, you\u2019re in good company. Here\u2019s what the research says and what shifted for people who gave it a real shot.",
        "body": '''
<p>If your first reaction to affirmations is skepticism, that\u2019s a rational starting point. The popular version of the practice \u2014 \u201cI am a magnet for abundance\u201d said in a mirror \u2014 is genuinely strange, and the wellness industry has wrapped it in enough woo that a reasonable person has every right to raise an eyebrow.</p>
<p>But skepticism of the manifesting framing isn\u2019t the same as skepticism of the underlying practice. The research base for self-affirmation is solid, the mechanism is well-understood, and the practice that emerges from the research looks almost nothing like the mirror version.</p>
<h2>What changes when you take it seriously</h2>
<p><strong>You start catching the loop.</strong> The internal narrative that runs on autopilot \u2014 \u201cI always screw up presentations,\u201d \u201cI\u2019m bad at money,\u201d \u201cI\u2019m not a morning person\u201d \u2014 starts to become audible. Not because affirmations are louder, but because you\u2019ve spent time deliberately saying something different. The contrast makes the automatic version more visible.</p>
<p><strong>You get slightly less avoidant.</strong> Tasks you\u2019ve been putting off become marginally less impossible. It\u2019s not a revelation. It\u2019s more like the friction on the first step is slightly lower than it was last month.</p>
<p><strong>You collect evidence differently.</strong> The attention-training effect is real. You start noticing the times you did handle something well more readily than you notice the times you didn\u2019t. You\u2019re not forgetting the failures. You\u2019re giving the successes equal airtime, which they weren\u2019t getting before.</p>
<h2>What doesn\u2019t change</h2>
<p>Your circumstances don\u2019t rearrange themselves. The difficult people in your life don\u2019t become easier. The practice isn\u2019t changing the external world \u2014 it\u2019s changing how you navigate it, which is both more modest and more useful than the manifesting version implies.</p>
<h2>The entry point</h2>
<p>If you\u2019re still skeptical but curious, start with the smallest possible version: one affirmation from the <a href="/tools/generator.html">generator</a>, said out loud once, in the morning before you check your phone. Give it three weeks. You\u2019re not committing to believing it. You\u2019re running an experiment. Notice what changes, if anything, in your internal experience of hard days.</p>
'''
    },
    {
        "slug": "affirmations-for-career-growth",
        "date": "Mar 17, 2026",
        "title": "Affirmations for Career Growth: What to Say Before the Meeting",
        "excerpt": "What you tell yourself in the sixty seconds before walking into a high-stakes moment matters more than you think.",
        "body": '''
<p>The sixty seconds before a high-stakes professional moment \u2014 a presentation, a difficult conversation with a manager, a job interview, a pitch \u2014 are when most people are doing the most damage to themselves. The mental rehearsal happening in that window tends to be catastrophic rather than supportive: running through what could go wrong, replaying previous failures.</p>
<p>You have the option of using that sixty seconds differently. Not to eliminate the nerves \u2014 trying to eliminate nerves in sixty seconds is a losing fight \u2014 but to change what your nervous system is processing alongside them.</p>
<h2>What to say before, not after</h2>
<p>The research on pre-performance affirmations shows that timing matters. Affirmations used as post-hoc reassurance are less effective than affirmations used as pre-priming. The brain is more receptive to self-supporting information before a challenge than in the middle of or after it.</p>
<p>The pre-moment affirmation isn\u2019t trying to make you feel fearless. It\u2019s trying to remind your nervous system that fear doesn\u2019t equal inability. Those two things can coexist \u2014 nervousness and competence \u2014 and the affirmation\u2019s job is to hold both in the frame.</p>
<h2>Three that hold up under pressure</h2>
<p><strong>\u201cI\u2019ve prepared what I can. What happens next, I handle as it comes.\u201d</strong> This one works because it acknowledges the unknown rather than pretending everything is under control. It separates preparation (done) from execution (ongoing).</p>
<p><strong>\u201cI belong in this room.\u201d</strong> Short. Addresses the imposter fear most professionals carry into high-stakes spaces. The answer to that fear isn\u2019t a long argument. It\u2019s a short, direct claim.</p>
<p><strong>\u201cI have something useful to contribute here, and I\u2019m going to contribute it.\u201d</strong> This shifts focus from self-evaluation (how am I coming across?) to task-orientation (what am I here to do?). Task-orientation reliably reduces performance anxiety.</p>
<h2>The post-meeting practice</h2>
<p>After the meeting, before you debrief with anyone else, name one specific thing you did well. Not everything. One thing. This is the evidence-building that makes the next pre-meeting affirmation land more truthfully.</p>
<p>Browse the <a href="/categories/confidence.html">Confidence drawer</a> and the <a href="/categories/success.html">Success drawer</a> for affirmations written for professional moments.</p>
'''
    },
]


def build_blog():
    cards = "".join(
        f'''<div class="card" style="min-height:auto;padding:0;overflow:hidden;">
  <a href="/blog/{p['slug']}.html" style="display:block;text-decoration:none;color:inherit;">
    <div style="aspect-ratio:16/9;overflow:hidden;background:var(--canvas-alt);">
      <img src="/images/blog/{p['slug']}.jpg" alt="{p['title']}" loading="lazy"
           style="width:100%;height:100%;object-fit:cover;"
           onerror="this.parentElement.style.background=\'var(--canvas-alt)\'">
    </div>
    <div class="card-body" style="padding:18px 20px 20px;">
      <p class="eyebrow" style="margin-bottom:6px;">{p['date']}</p>
      <h3 style="font-family:var(--font-display);font-style:italic;font-size:1.1rem;margin-bottom:8px;">{p['title']}</h3>
      <p style="color:var(--ink-faint);font-size:0.9rem;line-height:1.5;">{p['excerpt']}</p>
      <div class="card-actions" style="margin-top:14px;"><span class="icon-btn">Read →</span></div>
    </div>
  </a>
</div>''' for p in BLOG_POSTS
    )
    body = f'''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">THE BLOG</p>
    <h1>Notes on the practice</h1>
    <p class="lede">Short, practical writing on affirmations, habits, and the small rituals that actually survive a real week.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="fan-grid">{cards}</div>
  </div>
</section>
'''
    write("blog/index.html", page("Blog", "Practical writing on affirmations, morning rituals, and how to write affirmations that actually work.", "/", "blog", body))

    for i, p in enumerate(BLOG_POSTS):
        body = f'''
<section>
  <div class="wrap">
    <article class="post-body">
      <img src="/images/blog/{p['slug']}.jpg" alt="{p['title']}" class="blog-hero-img" loading="lazy" onerror="this.style.display=\'none\'">
      <h1>{p['title']}</h1>
      <p class="post-meta">{p['date']} \u00b7 MOTIVATION AFFIRMATION</p>
      {p['body']}
      <div class="post-footer-logo"><img src="/images/logo.png" alt="Motivation Affirmation" loading="lazy"></div>
    </article>
  </div>
</section>
'''
        write(f"blog/{p['slug']}.html", page(p["title"], p["excerpt"], "/", "blog", body))


def build_tools_index():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">TOOLS</p>
    <h1>Two ways to use Motivation Affirmation</h1>
    <p class="lede">Both run entirely in your browser \u2014 no account, no data leaving your device. Pull a card when you need one, or write the affirmation that\u2019s actually true for your life right now.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="tool-grid">
      <div class="tool-card">
        <p class="eyebrow">GENERATOR</p>
        <h3>Pull a card from any drawer</h3>
        <p>Filter by category, generate a card, save your favorites for later.</p>
        <a href="/tools/generator.html" class="btn btn-stamp">Open the generator</a>
      </div>
      <div class="tool-card">
        <p class="eyebrow moss">JOURNAL</p>
        <h3>Write the one that\u2019s actually true</h3>
        <p>A simple situation &rarr; strength &rarr; statement framework for writing affirmations that hold up.</p>
        <a href="/tools/journal.html" class="btn btn-outline">Start writing</a>
      </div>
    </div>
  </div>
</section>
'''
    write("tools/index.html", page("Tools", "Free affirmation generator and self-write journal tool. No account needed.", "/", "tools", body))


def build_generator_page():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">TOOL \u2014 GENERATOR</p>
    <h1>Pull a card from any drawer.</h1>
    <p class="lede">Pick a category (or leave it on all 480) and generate a card. Save the ones worth keeping.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="tool-panel" data-generator>
      <label for="gen-category">Filed under</label>
      <select id="gen-category"><option value="all">All categories</option></select>
      <div style="margin-top:20px;"><button class="btn btn-stamp" data-generate-btn>Generate a card</button></div>

      <div class="result-card" style="display:none;">
        <div class="card-meta"><span>CARD NO. \u2014</span><span>FILED: \u2014</span></div>
        <p class="card-quote">\u2014</p>
        <div class="card-actions">
          <button class="icon-btn" data-fav-btn>\u2606 Save card</button>
          <button class="icon-btn" data-copy-btn>Copy text</button>
        </div>
      </div>

      <div class="saved-list">
        <h3 style="margin-bottom:14px;">Your saved cards</h3>
        <div data-favorites-list></div>
      </div>
    </div>
  </div>
</section>
'''
    write("tools/generator.html", page("Affirmation Generator", "Free daily affirmation generator. Filter by category, generate a card, save your favorites \u2014 no account needed.", "/", "tools", body))


def build_journal_page():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow moss">TOOL \u2014 JOURNAL</p>
    <h1>Write the one that\u2019s actually true.</h1>
    <p class="lede">Self-written affirmations tend to outperform generic ones because they're specific to your actual life. This walks you through a simple three-part framework \u2014 read the <a href="/blog/write-your-own-affirmations.html">full breakdown</a> if you want the reasoning behind it.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <form class="tool-panel" data-journal-form>
      <label for="j-situation">What\u2019s the situation or challenge?</label>
      <input type="text" id="j-situation" placeholder="e.g. Asking for a deadline extension">

      <label for="j-strength">What strength or value does this draw on?</label>
      <input type="text" id="j-strength" placeholder="e.g. Honesty, follow-through, calm">

      <label for="j-statement">Write it as one present-tense statement</label>
      <textarea id="j-statement" placeholder="e.g. I can ask for what I need without over-explaining."></textarea>

      <div style="margin-top:20px;"><button type="submit" class="btn btn-stamp">File this card</button></div>
    </form>

    <div class="saved-list" style="max-width:720px;margin:36px auto 0;">
      <h3 style="margin-bottom:14px;color:var(--canvas-text);">Your filed cards</h3>
      <div data-journal-list></div>
    </div>
  </div>
</section>
'''
    write("tools/journal.html", page("Write Your Own Affirmations", "A simple situation, strength, statement framework for writing affirmations that actually hold up \u2014 saved privately in your browser.", "/", "tools", body))


def build_personal_page():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow moss">DRAWER \u2014 YOURS</p>
    <h1>My Personal Affirmations</h1>
    <p class="lede">Affirmations you wrote yourself, filed here. Stored only in this browser \u2014 nothing leaves your device. <a href="/tools/journal.html">Write a new one \u2192</a></p>
  </div>
</header>
<section>
  <div class="wrap">
    <div data-journal-list></div>
    <p style="margin-top:32px;color:var(--ink-faint);font-size:0.92rem;">
      Want to write your own? Use the <a href="/tools/journal.html">Journal tool</a> \u2014 it walks you through a simple situation \u2192 strength \u2192 statement framework.
    </p>
  </div>
</section>
'''
    write("categories/personal.html", page("My Personal Affirmations", "Your self-written affirmation cards, stored privately in your browser.", "/", "categories", body))


def build_shop():
    products = [
        {
            "title": "The Affirmation Card Deck",
            "format": "PDF \u00b7 64 printable cards",
            "price": "$9",
            "desc": "All eight categories, laid out as actual cut-and-keep cards \u2014 print at home, stick them on a mirror, a wallet, a desk.",
        },
        {
            "title": "The 30-Day Filed Journal",
            "format": "PDF \u00b7 guided workbook",
            "price": "$14",
            "desc": "A page a day using the situation \u2192 strength \u2192 statement framework from the journal tool, printable or fillable.",
        },
        {
            "title": "Morning & Night Audio Pack",
            "format": "Audio \u00b7 coming soon",
            "price": "Notify me",
            "desc": "Two short audio tracks \u2014 a 2-minute morning card pull and a wind-down gratitude practice for night.",
        },
    ]
    cards = "".join(
        f'''<div class="product-card">
  <div class="product-cover">{p['title']}</div>
  <div class="pc-body">
    <span class="price-tag">{p['format']} \u2014 {p['price']}</span>
    <h3>{p['title']}</h3>
    <p>{p['desc']}</p>
    <div style="margin-top:16px;"><a href="#subscribe" class="btn btn-outline">Notify me</a></div>
  </div>
</div>''' for p in products
    )
    body = f'''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">SHOP</p>
    <h1>Digital products, filed for download.</h1>
    <p class="lede">No checkout is wired up yet \u2014 these are launching soon. Join the list below and you\u2019ll be the first to know. (Building this out? See README.md for connecting Gumroad or Stripe.)</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="product-grid">{cards}</div>
  </div>
</section>
<section id="subscribe">
  <div class="wrap">
    <div class="subscribe-card">
      <div>
        <p class="eyebrow">GET NOTIFIED</p>
        <h2>We\u2019ll email you the day these launch.</h2>
      </div>
      <div>
        <form class="subscribe-form" data-newsletter-form>
          <input type="email" placeholder="you@email.com" required aria-label="Email address">
          <button type="submit" class="btn btn-ink">Notify me</button>
        </form>
        <p class="form-note">Free, always. Unsubscribe in one click.</p>
      </div>
    </div>
  </div>
</section>
'''
    write("shop.html", page("Shop", "Printable affirmation card decks, guided journals, and audio packs from Motivation Affirmation.", "", "shop", body))


def build_about():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">ABOUT</p>
    <h1>About Motivation Affirmation</h1>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="prose-panel">
      <p>Motivation Affirmation exists for one person: the woman who is done waiting to feel ready. The one who knows something needs to shift but hasn\u2019t found the right words yet. This site gives her words she can carry into her day \u2014 and the tools to write the ones that are specifically, actually true for her life.</p>
      <h2>What\u2019s here</h2>
      <p>480 affirmations across eight life categories \u2014 success, health, wealth, happiness, confidence, relationships, sleep, and gratitude \u2014 plus two tools: a generator for when you need something fast, and a journal for when you want to write the one that\u2019s true about your own life. No account required. Nothing leaves your browser.</p>
      <h2>Why it\u2019s organized by category</h2>
      <p>Affirmations work better when they\u2019re specific to what you\u2019re actually facing today. A generic \u201cI am enough\u201d does less than a sentence aimed at the exact challenge in front of you. The category structure lets you go straight to what you need instead of scrolling past 150 that don\u2019t apply.</p>
      <h2>How this is funded</h2>
      <p>Motivation Affirmation is supported by display ads and affiliate links to books and programs we genuinely recommend \u2014 full details are in the <a href="disclosure.html">affiliate disclosure</a>. There are also digital products in the <a href="shop.html">shop</a>. These keep the site free for everyone.</p>
      <h2>What\u2019s next</h2>
      <p>More categories, more blog posts, and a weekly email with one curated affirmation every Sunday. If you have a category you wish existed, reach us at hello@motivationaffirmation.com.</p>
    </div>
  </div>
</section>
'''
    write("about.html", page("About", "About Motivation Affirmation \u2014 a free, research-informed daily affirmations site organized by category, with a generator and a self-write journal tool.", "", "about", body))


def build_disclosure():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">DISCLOSURE</p>
    <h1>Affiliate disclosure</h1>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="prose-panel">
      <p>Motivation Affirmation is free to use, and we\u2019d like to keep it that way. To cover hosting and the time spent on content, this site uses two forms of monetization, both disclosed here in full.</p>
      <h2>Affiliate links</h2>
      <p>Some links on category pages and in blog posts \u2014 most often book recommendations \u2014 are affiliate links, including links to Amazon through the Amazon Associates program. If you click one of these links and make a purchase, Motivation Affirmation may earn a small commission. This comes at no extra cost to you; the price you pay is the same either way.</p>
      <h2>Display advertising</h2>
      <p>Some pages may show ads served by a third-party advertising network (such as Google AdSense). These networks may use cookies or similar technology to show relevant ads \u2014 see our <a href="privacy.html">privacy policy</a> for details on what that involves.</p>
      <h2>Editorial independence</h2>
      <p>Book and product recommendations on this site are chosen because we think they\u2019re genuinely useful, not because they pay the most commission. If a recommendation isn\u2019t working for the content around it, we\u2019d rather cut it than keep it.</p>
      <h2>Questions</h2>
      <p>If you have questions about any link on this site, the contact link in the footer reaches a real inbox.</p>
    </div>
  </div>
</section>
'''
    write("disclosure.html", page("Affiliate Disclosure", "How Cardinal is funded: affiliate links and display advertising, fully disclosed.", "", "", body))


def build_privacy():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">PRIVACY</p>
    <h1>Privacy policy</h1>
    <p class="lede">Last updated June 2026.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="prose-panel">
      <h2>What we don\u2019t collect</h2>
      <p>Cardinal doesn\u2019t require an account, and we don\u2019t collect names, passwords, or personal profiles. Favorited cards and journal entries you write are stored only in your browser\u2019s local storage \u2014 they\u2019re never sent to a server, and we have no access to them.</p>
      <h2>Email subscriptions</h2>
      <p>If you subscribe to updates, your email address is collected and stored by our email service provider so we can send you that email. You can unsubscribe at any time using the link in any email we send. <em>[Site owner: name your actual provider here once it\u2019s connected \u2014 e.g. Beehiiv, ConvertKit, Mailchimp \u2014 and link to their privacy policy.]</em></p>
      <h2>Cookies and advertising</h2>
      <p>This site may show ads from third-party networks (such as Google AdSense), which may set cookies or use similar technology to show ads based on your visits to this and other sites. You can opt out of personalized advertising through your browser settings or via <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>.</p>
      <h2>Analytics</h2>
      <p>We may use privacy-respecting analytics to understand which pages are useful, in aggregate, without identifying individual visitors. <em>[Site owner: update this section to match whatever analytics tool you actually add.]</em></p>
      <h2>Children\u2019s privacy</h2>
      <p>This site is not directed at children under 13, and we do not knowingly collect information from children under 13.</p>
      <h2>Contact</h2>
      <p>Questions about this policy can be sent to the contact address in the footer.</p>
    </div>
  </div>
</section>
'''
    write("privacy.html", page("Privacy Policy", "Cardinal's privacy policy \u2014 what we collect, what we don't, and how cookies and advertising work on this site.", "", "", body))


def build_terms():
    body = '''
<header class="page-head">
  <div class="wrap">
    <p class="eyebrow">TERMS</p>
    <h1>Terms of use</h1>
    <p class="lede">Last updated June 2026.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="prose-panel">
      <h2>Personal use</h2>
      <p>Cardinal\u2019s content \u2014 affirmations, blog posts, and tools \u2014 is provided for personal, non-commercial use. You\u2019re welcome to print or share individual cards; please don\u2019t republish the site\u2019s content in bulk elsewhere without permission.</p>
      <h2>Not professional advice</h2>
      <p>Cardinal is not a substitute for professional medical, psychological, or financial advice. Content related to health, sleep, or money is general and educational in nature. If you\u2019re dealing with a medical or mental health concern, or making a significant financial decision, please consult a qualified professional.</p>
      <h2>No guarantees</h2>
      <p>We make no promises about specific outcomes from using this site or its tools. Affirmations are a self-reflection practice, not a guaranteed method for achieving any particular result.</p>
      <h2>Your data, your browser</h2>
      <p>Favorites and journal entries are stored locally in your browser. Clearing your browser data, or using a different device or browser, will not carry these entries over \u2014 we don\u2019t store a backup.</p>
      <h2>Changes</h2>
      <p>We may update these terms from time to time; continued use of the site after changes means you accept the updated terms.</p>
    </div>
  </div>
</section>
'''
    write("terms.html", page("Terms of Use", "Cardinal's terms of use, including the not-professional-advice disclaimer for health, sleep, and money content.", "", "", body))


def build_404():
    body = '''
<section style="padding-top:120px;">
  <div class="wrap text-center">
    <p class="eyebrow">CARD NOT FOUND</p>
    <h1>This card isn\u2019t filed here.</h1>
    <p class="lede" style="margin:0 auto 28px;">Whatever you were looking for might have moved drawers.</p>
    <a href="index.html" class="btn btn-stamp">Back to today\u2019s card</a>
  </div>
</section>
'''
    write("404.html", page("Card Not Found", "Page not found.", "", "", body))


if __name__ == "__main__":
    build_home()
    build_categories_index()
    build_category_pages()
    build_personal_page()
    build_blog()
    build_tools_index()
    build_generator_page()
    build_journal_page()
    build_shop()
    build_about()
    build_disclosure()
    build_privacy()
    build_terms()
    build_404()
    print("\nDone. Open index.html (via a local server, not file://) to preview.")

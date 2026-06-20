# UNITUR — Yakuniy dizayn integratsiyasi (buyurtmachi tasdiqlagan, v3)

Buyurtmachi tasdiqladi: **Navbar (yuqori) + CTA banner + Footer (pastki)** — uchalasi ham "Yumshoq dengiz ko'k + sokin sariq" pattern bilan, YUMSHOQ quvvatda (matn aniq o'qilishi uchun). Sahifaning qolgan barcha qismi (hero, tours, destinations, why us, reviews) — oq + nozik ko'k pattern, bir xilda davom etadi.

## RANGLAR

### Asosiy sayt (barcha sahifalar, hero, sectionlar)
```
Ko'k (rasmiy):    #4497CB
Sariq (rasmiy):   #FFB81C
Oq fon:           #FFFFFF
Matn:             #1D2939
```

### CTA banner + Footer (buyurtmachi tasdiqlagan alohida rang)
```
Fon (dengiz ko'k):     #3E6C8F
Chiziq (sokin sariq):  #ECB456
```

### Bitta maxsus sahifa uchun (Guides/MICE/About — birini tanlang)
```
Oq fon + rasmiy sariq chiziq: pattern-subtle-yellow.png
```

## PATTERN FAYLLARI (paketda)

| Fayl | Qayerda ishlatiladi |
|------|----------------------|
| `pattern-subtle-blue.png` | Asosiy fon — hero, tours, hotels, destinations va boshqa barcha sahifalar |
| `pattern-tint-blue.png` | "Why UNITUR" kabi ajratilgan sectionlar |
| `pattern-subtle-yellow.png` | FAQAT bitta tanlangan sahifa (Guides/MICE/About) |
| `pattern-footer-cta.png` | FAQAT CTA banner va Footer — dengiz ko'k + sokin sariq |

---

## CLAUDE CODE UCHUN PROMPT — nusxalab bering

```
You are a senior frontend developer working on the UNITUR Django tour agency website (live at http://35.154.77.124/). The client has REVIEWED and APPROVED the design direction. This is the final color/pattern specification — implement exactly as described, no improvisation.

## APPROVED COLOR SYSTEM

### Site-wide (hero, sections, buttons, links, card content)
--c-blue:        #4497CB   /* official brand blue */
--c-blue-dark:   #2B7BAD
--c-blue-light:  #B4D2E8
--c-blue-pale:   #E4F0F9
--c-yellow:      #FFB81C   /* official brand yellow */
--c-yellow-dark: #D89A0E
--c-yellow-pale: #FFF6E0
--c-ink:         #1D2939
--c-text-muted:  #667085

### Navbar + CTA banner + Footer ONLY (client-approved muted palette)
--c-cta-bg:      #3E6C8F   /* muted sea-blue */
--c-cta-line:    #ECB456   /* calm yellow */

This muted palette is RESERVED for exactly THREE places: the top navbar, the "Ready for Your Next Adventure?" CTA banner, and the site footer. These three elements share the same pattern and color treatment, creating a consistent "bookend" frame around the page (dark top, white/blue middle, dark bottom — with the CTA banner as a third dark accent before the footer). Do not apply --c-cta-bg or --c-cta-line anywhere else (not on hero, not on section backgrounds, not on cards).

IMPORTANT — strength level: on the navbar and footer, the pattern must be SOFT/MUTED so text stays crisp and readable — apply a near-opaque tint overlay (~75-80% opacity of --c-cta-bg) over the pattern so the leaf motif is only faintly visible, not competing with the logo/nav text/footer text. The CTA banner can be slightly more visible than navbar/footer since it has less text density, but still legible — use a lighter overlay there (~35% opacity).

## PATTERN FILES (provided, place in static/img/patterns/)
  pattern-subtle-blue.png     148×385px — white bg + soft blue lines (MAIN site-wide pattern)
  pattern-tint-blue.png       148×385px — pale blue bg + blue lines (alternate section pattern)
  pattern-subtle-yellow.png   148×385px — white bg + soft yellow lines (ONE dedicated page only)
  pattern-footer-cta.png      148×385px — muted sea-blue bg + calm yellow lines (CTA + footer ONLY)

DO NOT recreate or redraw these. Use the files as-is.

## CSS — static/css/brand.css

  :root {
    --c-blue: #4497CB; --c-blue-dark: #2B7BAD; --c-blue-light: #B4D2E8; --c-blue-pale: #E4F0F9;
    --c-yellow: #FFB81C; --c-yellow-dark: #D89A0E; --c-yellow-pale: #FFF6E0;
    --c-ink: #1D2939; --c-text-muted: #667085;
    --c-cta-bg: #3E6C8F; --c-cta-line: #ECB456;
  }

  .bg-pattern-subtle-blue,
  .bg-pattern-tint-blue,
  .bg-pattern-subtle-yellow,
  .bg-pattern-frame,
  .bg-pattern-cta {
    background-repeat: repeat;
    background-size: 110px 286px;
  }
  @media (max-width: 768px) {
    .bg-pattern-subtle-blue,
    .bg-pattern-tint-blue,
    .bg-pattern-subtle-yellow,
    .bg-pattern-frame,
    .bg-pattern-cta { background-size: 88px 229px; }
  }

  .bg-pattern-subtle-blue   { background-image: url("/static/img/patterns/pattern-subtle-blue.png"); background-color: #FFFFFF; }
  .bg-pattern-tint-blue     { background-image: url("/static/img/patterns/pattern-tint-blue.png"); background-color: #E4F0F9; }
  .bg-pattern-subtle-yellow { background-image: url("/static/img/patterns/pattern-subtle-yellow.png"); background-color: #FFFFFF; }

  /* Navbar & Footer — SOFT/MUTED pattern strength so text stays crisp */
  .bg-pattern-frame {
    background-image:
      linear-gradient(rgba(62,108,143,0.78), rgba(62,108,143,0.78)),
      url("/static/img/patterns/pattern-footer-cta.png");
    background-color: #3E6C8F;
  }

  /* CTA banner — slightly more visible pattern than navbar/footer (less text density) */
  .bg-pattern-cta {
    background-image:
      linear-gradient(rgba(40,65,90,0.35), rgba(40,65,90,0.35)),
      url("/static/img/patterns/pattern-footer-cta.png");
    background-color: #3E6C8F;
  }

  /* Hero — same muted palette as navbar/CTA/footer, with overlay tuned for large heading text */
  .bg-pattern-hero {
    background-image:
      linear-gradient(rgba(62,108,143,0.51), rgba(62,108,143,0.51)),
      url("/static/img/patterns/pattern-footer-cta.png");
    background-color: #3E6C8F;
  }
  .bg-pattern-hero h1,
  .bg-pattern-hero .hero-heading-white {
    color: #FFFFFF;
    text-shadow: 0 2px 6px rgba(20,35,50,0.35);
  }
  .bg-pattern-hero .hero-heading-accent {
    color: #ECB456; /* calm yellow accent line, e.g. "With Confidence" / "Ishonch bilan" */
    text-shadow: 0 2px 6px rgba(20,35,50,0.35);
  }
  .bg-pattern-hero .hero-subtitle {
    color: #DCE8F2; /* soft light blue-white for the subtitle paragraph */
  }

Link in base.html: <link rel="stylesheet" href="{% static 'css/brand.css' %}">

## TAILWIND CONFIG
extend.colors:
  brand: {
    blue: '#4497CB', blueDark: '#2B7BAD', blueLight: '#B4D2E8', bluePale: '#E4F0F9',
    yellow: '#FFB81C', yellowDark: '#D89A0E', yellowPale: '#FFF6E0',
    ink: '#1D2939',
    ctaBg: '#3E6C8F', ctaLine: '#ECB456',
  }

## PAGE-BY-PAGE APPLICATION

### HOME PAGE
1. Navbar              → bg-pattern-frame (muted sea-blue + soft yellow pattern, SOFT strength). White logo text, white nav links, yellow "Book Now" button using --c-cta-line
2. Hero                → bg-pattern-hero (muted sea-blue + calm yellow, SAME palette as navbar/CTA/footer, with a tint overlay so text reads clearly). White heading text ("Discover the World"), --c-cta-line colored accent line ("With Confidence"), soft light-blue subtitle text. This is the ONLY place besides navbar/CTA/footer that uses the muted palette — it makes the very top of the page (navbar + hero) feel like one connected, branded opening, before the page transitions to white+blue for the rest of the content.
3. Stats strip         → bg-white, numbers in brand-blue
4. Featured Tours      → bg-white, cards white with shadow, yellow category/discount badges
5. Top Destinations    → bg-pattern-subtle-blue
6. Why UNITUR          → bg-pattern-tint-blue (pale blue variant for contrast)
7. Featured Hotels     → bg-white
8. Customer Reviews    → bg-pattern-subtle-blue
9. Latest Guides       → bg-white
10. CTA "Ready for..." → bg-pattern-cta (muted sea-blue + yellow, matches navbar/hero/footer)
11. Footer             → bg-pattern-frame (SAME treatment as navbar — soft/muted, white text)

The navbar, hero, CTA banner, and footer all share the same muted sea-blue + calm yellow palette — this creates a strong branded "frame" at the very top and bottom of the page, while everything in between (tours, destinations, reviews, etc.) stays clean white + soft blue. This is intentional.

### ALL OTHER PAGES (Tours, Destinations, Hotels, MICE, Reviews, About, Contact)
- Navbar            → bg-pattern-frame (same as home, every page)
- Hero/title strip  → bg-pattern-hero (same muted palette as home hero — NOT bg-pattern-subtle-blue; keep the branded top consistent across all pages)
- Body content      → bg-white (or bg-pattern-subtle-blue for alternating sections, per existing site structure)
- Footer            → bg-pattern-frame (same as home, every page)

### ONE DEDICATED PAGE — bg-pattern-subtle-yellow
Choose exactly ONE page to feel distinct using the yellow pattern instead of blue:
  → Use it for the GUIDES (Travel Guides / Articles) page — hero AND body background.
  This is the only page where bg-pattern-subtle-yellow appears. All other pages use blue.

### LOGIN / DASHBOARD LOGIN
  → bg-pattern-subtle-blue (consistent with main site, not the muted CTA palette)

## BUTTON SYSTEM (site-wide, brand colors)
.btn-primary { background: #4497CB; color: #fff; }              /* Search, View actions on white/blue backgrounds */
.btn-primary:hover { background: #2B7BAD; }
.btn-accent  { background: #FFB81C; color: #fff; }               /* category badges, discount tags on cards */
.btn-accent:hover { background: #D89A0E; }

Inside the navbar, CTA banner, and footer (the muted-palette zones), buttons use --c-cta-line instead of the bright site-wide yellow, so they match the muted backdrop:
.btn-frame-accent  { background: #ECB456; color: #fff; }   /* "Book Now" in navbar, "Plan My Trip" in CTA */
.btn-frame-outline { border: 2px solid #fff; color: #fff; background: transparent; }  /* "Browse Tours" etc. */

## REMOVE
- All old background photos/overlays on hero and CTA sections
- Any previous bright-orange (#F4733D) or dark-blue (#4F91C6) color references from earlier iterations
- Old full-strength dark pattern backgrounds site-wide (replaced by the subtle versions above)

## KEEP
- Real tour/hotel/destination/article photos (cards, content images)
- Logo
- Existing layout structure, just recolored and re-backgrounded

## DELIVERABLES (in order)
1. Place 4 pattern files in static/img/patterns/
2. static/css/brand.css with the system above (including .bg-pattern-frame and .bg-pattern-cta)
3. Updated tailwind.config.js
4. Updated base.html — navbar now uses bg-pattern-frame with white text/links, footer uses bg-pattern-frame with white text; link the new CSS
5. Updated home.html — full section-by-section per the mapping above, CTA banner uses bg-pattern-cta
6. Updated Guides page — bg-pattern-subtle-yellow applied
7. Updated Tours/Destinations/Hotels/MICE/Reviews/About/Contact — navbar/footer consistent bg-pattern-frame, hero bg-pattern-subtle-blue, body white
8. Updated login/dashboard login — bg-pattern-subtle-blue (navbar still bg-pattern-frame if a navbar is present on these pages)
9. Summary of all files changed

## REVIEW CHECKPOINT
Complete the HOME PAGE first only. Stop and notify me. I will check http://35.154.77.124/ before approving you to continue to the remaining pages.

Start with brand.css + tailwind.config.js, then base.html, then home.html.
```

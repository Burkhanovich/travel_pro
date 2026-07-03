# Travel Pro — Audit hisoboti (BOSQICH 1)

Sana: 2026-07-04 · Auditor: Senior Full-Stack Django review
Metod: sozlama fayllari, `apps/*`, `templates/*` qo'lda ko'rib chiqildi;
`pip-audit` (CVE), git-tracked env fayllar, rate-limit va queryset tahlili.

## Umumiy xulosa
Loyiha **umuman yaxshi qurilgan**: ro'yxat view'larida `select_related/prefetch_related`
izchil ishlatilgan, formalarda rate-limiting bor, admin URL yashirilgan, CSP + xavfsizlik
headerlari sozlangan, cookie'lar HTTPS'da secure. Asosiy muammo — **eskirgan bog'liqliklar**
va **production'da HTTPS o'chiqligi** (infratuzilma).

---

## KRITIK

| # | Muammo | Joy | Nega muhim | Yechim |
|---|--------|-----|-----------|--------|
| C1 | **Django 5.2.2 da 72 ma'lum CVE** (PYSEC-2025/2026-*) | `requirements/base.txt:7` | SQL/DoS/ma'lumot oshkor bo'lish zaifliklari; ekspluatatsiya qilinishi mumkin | Django'ni **5.2.15** ga (LTS patch, orqaga mos) yangilash |
| C2 | Yana 5 paketda CVE: `django-allauth 65.5.0`, `pillow 11.2.1`, `requests 2.32.3`, `urllib3 2.4.0`, `deep-translator 1.11.4` | `requirements/base.txt` | allauth = autentifikatsiya; urllib3/requests = TLS/so'rovlar; pillow = rasm parsing (RCE xavfi) | allauth→65.14.1, pillow→11.3.0, requests→2.32.4, urllib3→2.5.0. deep-translator uchun rasmiy fix yo'q (past ta'sir, faqat server tarjimasi) |

## O'RTA (asosan infratuzilma — serverda qo'lda)

| # | Muammo | Joy | Nega | Yechim |
|---|--------|-----|------|--------|
| M1 | **Production HTTPS o'chiq** (`HTTPS_ENABLED=False`), sayt `http://35.154.77.124` da ishlaydi | server `.env`; `production.py:20` | Login/parol/form ma'lumotlari **ochiq matnda** uzatiladi; cookie secure emas, HSTS off | TLS sertifikat (Let's Encrypt/nginx) o'rnatib `.env` da `HTTPS_ENABLED=True` va `SECURE_SSL_REDIRECT=True` qilish |
| M2 | Server bazasi paroli zaif: `TravelPro2024!` | server `.env` `DATABASE_URL` | Oson taxmin qilinadigan parol | Kuchli parolga almashtirish (server + Postgres) |
| M3 | `.env.production` git'da tracked | repo ildizi | Hozir **faqat placeholder** (real sir yo'q ✅), lekin kelajakda real qiymat commit qilinishi xavfi | `.gitignore` ga qo'shib, `.env.production` → `.env.production.example` sifatida qoldirish |

## KICHIK

| # | Muammo | Joy | Nega | Yechim |
|---|--------|-----|------|--------|
| L1 | Telefon maydonida format validatsiyasi yo'q | `apps/bookings/models.py:97` (`phone = CharField`) | Ixtiyoriy matn qabul qilinadi | Yumshoq `RegexValidator` qo'shish |
| L2 | Home "testimonials" da N+1 | `apps/core/views.py:52` | Har bir sharh uchun `review.tour`/`hotel` alohida so'rov (≤6 element) | `.select_related("tour","hotel")` qo'shish |
| L3 | `{{ article.content|safe }}` | `templates/guides/detail.html:35` | Saqlangan-XSS xavfi (lekin faqat **staff** CKEditor orqali yozadi) | Qabul qilinadi; kelajakda `bleach` bilan sanitatsiya tavsiya |
| L4 | `mice` app'ida view/test yo'q | `apps/mice/` | Bo'sh/tugallanmagan modul | Kerak bo'lsa to'ldirish yoki olib tashlash |

## Ijobiy tomonlar (buzmaslik kerak)
- Rate-limiting: login/register (`accounts/views.py:55` 5/10m), booking + inquiry (`bookings/views.py:43,110` 5/h). Public sharh formasi yo'q → rate-limit shart emas.
- Xavfsizlik headerlari: `X_FRAME_OPTIONS=DENY`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`, CSP (`base.py`), HSTS (HTTPS'da).
- `ADMIN_URL` default `secret-admin-xyz123/` (yashirilgan).
- Indekslar: slug (SlugField default), FK (default), `is_active/is_featured/order` (mixin `db_index=True`).
- N+1: hotels/guides/reviews/tours list view'lari to'g'ri `select_related/prefetch_related` ishlatadi.
- Kesh: tours list `cache_page(60*5)`; test settings'da network/tarjima o'chirilgan.
- Testlar: **202 passed**. Zaif qoplama: `mice` (view yo'q), ba'zi model method'lar.

## Qo'shimcha (BOSQICH 2 da aniqlangan)

| # | Muammo | Joy | Nega | Yechim |
|---|--------|-----|------|--------|
| M4 | **CKEditor 4** (django-ckeditor 6.7.1, CKEditor 4.22.1) — tuzatilmagan XSS zaifliklari | `manage.py check` (ckeditor.W001) | CKEditor 4 EOL, XSS xavfi (staff editor) | `django-ckeditor-5` yoki CKEditor 4 LTS ga o'tish (alohida ish — maqola editorini o'zgartiradi) |

---

## ✅ BOSQICH 2 natijasi (kod darajasida bajarildi)

| Topilma | Harakat | Natija |
|---------|---------|--------|
| **C1+C2 CVE** | Django 5.2.2→**5.2.15**, allauth→65.14.1, Pillow→12.2.0, requests→2.33.0, urllib3→2.7.0 | **72 → 1 CVE** (98.6%↓). Qolgan: `deep-translator` PYSEC-2022-252 (upstream'da fix yo'q, past ta'sir — qabul qilinadi/kuzatiladi) |
| **M3** | `.env.production` → `.env.production.example`, `.gitignore` ga `.env.production` | Kelajakda real sir commit bo'lmaydi |
| **L1** | `Inquiry.phone` ga `RegexValidator` (+ migratsiya `0003`) | Telefon formati tekshiriladi |
| **L2** | Testimonials `select_related("user","tour","hotel")` | Home'da N+1 yo'q |
| Testlar | Har tuzatishdan keyin | **203 passed** (yangi test: telefon validatsiyasi) |

**Faqat qo'lda (server, kod bilan hal bo'lmaydi):** M1 (HTTPS/TLS), M2 (DB parol), M4 (CKEditor migratsiyasi — alohida reja).

## Tavsiya etilgan BOSQICH 2 tuzatishlar (kod darajasida)
1. **C1+C2** — `requirements/base.txt` bog'liqliklarni yangilash (eng yuqori ustuvorlik).
2. **M3** — `.env.production` ni gitignore qilish.
3. **L1** — telefon `RegexValidator`.
4. **L2** — testimonials `select_related`.

**Faqat qo'lda (server)**: M1 (HTTPS), M2 (DB parol) — kod bilan hal qilinmaydi.

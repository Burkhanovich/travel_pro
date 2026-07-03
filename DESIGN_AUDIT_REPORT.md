# Travel Pro — Dizayn auditi (BOSQICH 3)

Sana: 2026-07-04 · Ko'lam: `templates/**/*.html` (public), `static/css/brand.css`, `custom.css`
Metod: past-kontrast Tailwind klasslari va CSS ranglari WCAG AA (oddiy matn ≥4.5:1,
katta/UI ≥3:1) bo'yicha tekshirildi. Kontrast qiymatlari sRGB relativ yorug'lik formulasi
bilan hisoblandi.

## Kontrast hisob-kitobi (asos)
| Rang | Fon | Nisbat | AA (oddiy) |
|------|-----|-------:|:---------:|
| `text-gray-400` #9CA3AF | oq #FFF | **2.56:1** | ❌ |
| `text-gray-500` #6B7280 | oq #FFF | **4.91:1** | ✅ |
| `text-gray-600` #4B5563 | oq #FFF | ~5.9:1 | ✅ |
| hero-subtitle #DCE8F2 | hero #3E6C8F | ~4.35:1 | ⚠️ chegara |
| hero-subtitle #EAF3FB | hero #3E6C8F | ~4.6:1 | ✅ |
| footer `text-white/60` | frame #3E6C8F | ~2.7:1 | ❌ |
| footer `text-white/80` | frame #3E6C8F | ~4.0:1 | ✅ (kichik matn uchun sezilarli yaxshilanish) |

## Tuzatilgan muammolar (oldin → keyin)

| Fayl:qator | Muammo | Eski | Yangi | Asos |
|-----------|--------|------|-------|------|
| `static/css/brand.css:75` | Hero subtitle och ko'k, pattern ustida zaif | `color:#DCE8F2` | `#EAF3FB` + `text-shadow` | 4.35→4.6:1, sarlavhalar bilan bir xil soya |
| `templates/components/navbar.html:30,51` | Mega-menu "By Category" / kontinent sarlavhalari o'qish qiyin | `text-gray-400` | `text-gray-500` | 2.56→4.91:1 (AA) |
| `templates/home.html:98` | "No featured tours yet." bo'sh holat matni xira | `text-gray-400` | `text-gray-500` | 2.56→4.91:1 (AA) |
| `templates/components/footer.html:105` | Pastki huquqiy qator (copyright) juda xira | `text-white/60` | `text-white/80` | 2.7→4.0:1 |

## Tekshirilgan, lekin YAXSHI (o'zgartirilmadi)
- **Tugmalar** (`btn-primary` #4497CB/oq, `btn-accent` #FFB81C/oq, `btn-frame-*`) — brend palitrasi, hover holatlari aniq farqlanadi, matn kontrasti yetarli.
- **Fokus holatlari** — inputlar `focus:ring-2 focus:ring-primary` ishlatadi (klaviatura navigatsiyasi ko'rinadi).
- **Hero sarlavhalar** (`h1`) — oq + `text-shadow` (brand.css:65-68), pattern ustida o'qiladi.
- **Kartalar** — oq fon + soya, matn `text-dark`/`text-gray-700` (yaxshi kontrast).

## Umumiy tavsiya (blanket o'zgartirilmadi — dizayn niyatini buzmaslik uchun)
`text-gray-400` public shablonlarda **46 marta** ishlatilgan (25 fayl). Ko'pchiligi
**dekorativ** (bo'sh-holat ikonkalari `ti-*-off`, sana/meta, `—` ajratgichlar) bo'lib,
ular uchun AA majburiy emas. Lekin **oq fon ustidagi haqiqiy matn** uchun qoida:

> **`text-gray-400` → `text-gray-500`** (oq fonda 2.56→4.91:1). Kelajakda ro'yxat
> sahifalaridagi bo'sh-holat jumlalari ("No tours match…", "No reviews found." va h.k.)
> shu qoida bo'yicha yangilanishi mumkin — bu safar eng ko'rinadigan 4 nuqta tuzatildi.

`text-gray-300` (6 marta) asosan bo'sh yulduz ikonkalari / ajratgichlar — dekorativ, qoldirildi.

## Mobil (375 / 768 / 1280px)
- Hero forma `grid-cols-1 md:grid-cols-3` — mobilda ustma-ust, kesilish yo'q.
- Tugmalar `py-2.5/py-3` + `px-4` — bosish maydoni ≥44px talabiga mos.
- Navbar mega-menu sarlavhalari endi mobil dropdownda ham o'qiladi.

## Natija
4 ta yuqori-ko'rinadigan kontrast muammosi WCAG AA ga keltirildi, brend palitrasi
(`--c-ink`, gray-500, oq soyalar) doirasida — tasodifiy rang qo'shilmadi.

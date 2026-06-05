"""Download hero images from Unsplash CDN to static/images/."""
import os
import ssl
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "static" / "images"
OUT.mkdir(parents=True, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TravelPro/1.0"}

IMAGES = {
    "hero-home.jpg":         "https://images.unsplash.com/photo-1488085061387-422e29b40080?w=1920&q=85&fit=crop",
    "hero-tours.jpg":        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=85&fit=crop",
    "hero-hotels.jpg":       "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1920&q=85&fit=crop",
    "hero-destinations.jpg": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1920&q=85&fit=crop",
    "hero-about.jpg":        "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=1920&q=85&fit=crop",
    "hero-contact.jpg":      "https://images.unsplash.com/photo-1423666639041-f56000c27a9a?w=1920&q=85&fit=crop",
    "hero-guides.jpg":       "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920&q=85&fit=crop",
    "hero-mice.jpg":         "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920&q=85&fit=crop",
    "hero-reviews.jpg":      "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920&q=85&fit=crop",
}

ok = 0
for fname, url in IMAGES.items():
    path = OUT / fname
    if path.exists() and path.stat().st_size > 10_000:
        print(f"  ok (cached)  {fname}")
        ok += 1
        continue
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=25) as r:
            data = r.read()
        path.write_bytes(data)
        print(f"  downloaded   {fname}  ({len(data)//1024} KB)")
        ok += 1
    except Exception as e:
        print(f"  FAILED       {fname}  {e}")
    time.sleep(0.3)

print(f"\n{ok}/{len(IMAGES)} hero images ready in {OUT}")

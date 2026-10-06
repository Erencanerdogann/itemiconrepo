# -*- coding: utf-8 -*-
# REHBER GORSELLERI (patron 3 Eki: "gorsellerini kaydet, duzgun kes"). Oyundaki Rehber penceresi = sexyko.com/guide (WebView2).
# Oyun icinde WebView'e programla tiklanamadi (2 deneme, sekme degismedi) -> ayni sayfalar oyundaki pencere boyutunda (1620x980) buradan cekilir.
# Cikti: rehber/web/gorsel/<bolum>.png (icerik alani, tam boy) + <bolum>_ekran.png (oyundaki gibi tek ekran)
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, time
from playwright.sync_api import sync_playwright

KOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KOK, "rehber", "web", "gorsel"); os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
BOLUM = ["book", "monsters", "quests", "upgrade", "drops", "fragment", "cross-exchange", "shozin", "narki", "pus-crash",
         "mining-fishing", "daily-quests", "event-rewards", "beginner-items"]
BOOK = json.load(open(os.path.join(KOK, "rehber", "web", "book.json"), encoding="utf-8")).get("alt_sayfa", [])
GIZLE = "[class*='chat'],[id*='chat'],[class*='support-widget'],[class*='cookie'],.toast-container{display:none!important}"

hedef = [(b, f"https://sexyko.com/guide/{b}") for b in BOLUM] + [("book_" + a.rsplit("/", 1)[1], "https://sexyko.com" + a) for a in BOOK]
with sync_playwright() as pw:
    br = pw.chromium.launch(); c = br.new_context(user_agent=UA, locale="tr-TR", viewport={"width": 1620, "height": 980}, color_scheme="dark")
    s = c.new_page()
    for ad, url in hedef:
        try:
            s.goto(url, wait_until="load", timeout=60000); s.add_style_tag(content=GIZLE); time.sleep(3.0)
            s.screenshot(path=os.path.join(OUT, f"{ad}_ekran.png"))
            el = s.query_selector("main") or s.query_selector(".sub-wrapper")
            (el or s).screenshot(path=os.path.join(OUT, f"{ad}.png")) if el else s.screenshot(path=os.path.join(OUT, f"{ad}.png"), full_page=True)
            print("✔", ad)
        except Exception as e:
            print("✗", ad, str(e)[:120])
    br.close()
print("bitti:", len(os.listdir(OUT)), "dosya")

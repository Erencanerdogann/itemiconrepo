# -*- coding: utf-8 -*-
# SexyKO OYUN ICI REHBER = https://sexyko.com/guide (oyundaki "Rehber / Guide-Help" penceresi bu siteyi WebView2 ile acar;
# kanit: Game.exe icindeki https://sexyko.com/guide/... dizgeleri + oyunda acilan pencerenin sekmeleri birebir ayni). SADECE OKUMA.
# patron 3 Eki: "premium sekilde oyunu ogren, resimlerin hepsini web sayfasindan mutlaka cek, tam veri istiyorum, EKSIKSIZ"
# Sunucu: Hyper (serverId 12, sitenin varsayilani). Myra (1) cekilmedi.
# Cikti: rehber/web/<bolum>.json (her secim: ad, metin, resimler) · rehber/web/sayfa/<bolum>/<n>.html · rehber/web/resim/* · rehber/web/ozet.json
#   Kullanim: python _guide_cek.py [bolum ...]   (bos = hepsi)
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, time, hashlib, requests

KOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KOK, "rehber", "web")
SAY = os.path.join(OUT, "sayfa"); RES = os.path.join(OUT, "resim")
for d in (OUT, SAY, RES):
    os.makedirs(d, exist_ok=True)
SITE = "https://sexyko.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
S = requests.Session(); S.headers["User-Agent"] = UA
RESIMLER = {}                                     # url -> yerel dosya


def metin(h):
    h = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>|</(p|div|li|tr|h\d|section|article|table|thead|tbody)>", "\n", h)
    h = re.sub(r"</t[dh]>", " | ", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r" *\n[ \n]*", "\n", t)
    return t.strip()


def resimler(h):
    u = re.findall(r'<img[^>]+src="([^"]+)"', h) + re.findall(r'url\([\'"]?(https://cdn\.sexyko\.com/[^\'")]+)', h)
    out = []
    for x in u:
        x = html.unescape(x)
        if x.startswith("/"):
            x = SITE + x
        if x.startswith("http") and "/images/nation/" not in x and "/images/class/" not in x[:60] or "itemicon" in x:
            out.append(x)
    return list(dict.fromkeys(out))


def kaydet(bolum, ad, h):
    d = os.path.join(SAY, bolum); os.makedirs(d, exist_ok=True)
    yol = os.path.join(d, re.sub(r"[^A-Za-z0-9_.-]+", "_", str(ad))[:80] + ".html")
    open(yol, "w", encoding="utf-8").write(h)
    rs = resimler(h)
    for r in rs:
        RESIMLER.setdefault(r, None)
    return {"ad": str(ad), "metin": metin(h), "resimler": rs, "html": os.path.relpath(yol, KOK).replace("\\", "/")}


def yaz(bolum, kayitlar, ek=None):
    json.dump({"bolum": bolum, "kaynak": f"{SITE}/guide/{bolum}", "sunucu": "Hyper (12)", "tarih": time.strftime("%Y-%m-%d %H:%M"),
               "adet": len(kayitlar), **(ek or {}), "kayitlar": kayitlar},
              open(os.path.join(OUT, f"{bolum}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  ✔ {bolum}: {len(kayitlar)} kayit")


# ---------- duz GET sayfalari (book alt sayfalari, monster/quest detaylari)
def get(url):
    for dene in range(4):
        try:
            r = S.get(url, timeout=40)
            if r.status_code == 429:
                time.sleep(5 * (dene + 1)); continue
            return r
        except requests.RequestException:
            time.sleep(3)
    return None


def ana_bolge(t):
    m = re.search(r"<main.*?</main>", t, re.S)
    return m.group(0) if m else t


def book():
    t = get(f"{SITE}/guide/book").text
    alt = sorted(set(re.findall(r'href="(?:https://sexyko\.com)?(/guide/book/[^"#?]+)"', t)))
    kay = [kaydet("book", "index", ana_bolge(t))]
    for a in alt:
        r = get(SITE + a); kay.append(kaydet("book", a.rsplit("/", 1)[1], ana_bolge(r.text))); time.sleep(0.3)
    yaz("book", kay, {"alt_sayfa": alt})


def detaylar(bolum, idler):
    kay = []
    for n, i in enumerate(idler, 1):
        r = get(f"{SITE}/guide/{bolum}/{i}")
        if r is None or r.status_code != 200:
            kay.append({"ad": str(i), "hata": r.status_code if r is not None else "yok"}); continue
        kay.append(kaydet(f"{bolum}_detay", i, ana_bolge(r.text)))
        if n % 50 == 0:
            print(f"    {bolum} detay {n}/{len(idler)}")
        time.sleep(0.25)
    yaz(f"{bolum}_detay", kay)


# ---------- Livewire bilesenleri (dogrudan Livewire 3 istegi; Playwright headless'ta site 500 donuyordu, requests ile 200 — olculdu 3 Eki)
class LW:
    def __init__(self, bolum):
        self.bolum = bolum; self.s = requests.Session(); self.s.headers["User-Agent"] = UA
        t = self.s.get(f"{SITE}/guide/{bolum}", timeout=40).text
        self.csrf = re.search(r'data-csrf="([^"]+)"', t).group(1); self.uri = re.search(r'data-update-uri="([^"]+)"', t).group(1)
        self.snap, self.html, self.lazy = {}, {}, {}
        for m in re.finditer(r'wire:snapshot="([^"]+)"[^>]*?wire:name="([^"]+)"', t):
            self.snap[m.group(2)] = html.unescape(m.group(1))
        for m in re.finditer(r'wire:name="([^"]+)"[^>]*?x-init="\$wire\.__lazyLoad\(&#039;([^&]+)&#039;\)"', t):
            self.lazy[m.group(1)] = m.group(2)
        for m in re.finditer(r"wire:name=\"([^\"]+)\"[^>]*?x-init=\"\$wire\.__lazyLoad\('([^']+)'\)\"", t):
            self.lazy[m.group(1)] = m.group(2)
        for ad in self.snap:
            i = t.find(f'wire:name="{ad}"'); j = t.rfind("<", 0, i)
            self.html[ad] = t[j:j + 400000]

    def istek(self, ad, updates=None, calls=None):
        body = {"_token": self.csrf, "components": [{"snapshot": self.snap[ad], "updates": updates or {}, "calls": calls or []}]}
        hd = {"X-Livewire": "1", "Content-Type": "application/json", "Accept": "application/json", "Referer": f"{SITE}/guide/{self.bolum}", "Origin": SITE}
        for dene in range(4):
            r = self.s.post(self.uri, json=body, headers=hd, timeout=60)
            if r.status_code == 429:
                time.sleep(5 * (dene + 1)); continue
            break
        if r.status_code != 200:
            raise RuntimeError(f"{self.bolum}/{ad} {updates} {calls}: HTTP {r.status_code}")
        c = r.json()["components"][0]; self.snap[ad] = c["snapshot"]
        h = c.get("effects", {}).get("html")
        if h:
            self.html[ad] = h
        time.sleep(0.25)
        return self.html[ad]

    def cagir(self, ad, metod, *arg):
        return self.istek(ad, calls=[{"path": "", "method": metod, "params": list(arg)}])

    def set(self, ad, k, v):
        return self.istek(ad, updates={k: v})

    def yukle(self, ad):
        return self.cagir(ad, "__lazyLoad", self.lazy[ad]) if ad in self.lazy else self.html[ad]


def argumanlar(h, metod):
    out = []
    for m in re.finditer(r'wire:click(?:\.[a-z]+)*="' + metod + r'\(([^)]*)\)"', h):
        out.append(html.unescape(m.group(1)).strip().strip("'\""))
    return list(dict.fromkeys(out))


def _a(x):
    return int(x) if x.lstrip("-").isdigit() else x


def sayfali(bolum, ad, toplam_re):
    lw = LW(bolum); h = lw.html[ad]; m = re.search(toplam_re, metin(h)); n = int(m.group(m.lastindex)) if m else 1
    kay = [kaydet(bolum, 1, h)]; idler = re.findall(rf'/guide/{bolum}/(\d+)', h)
    for i in range(2, n + 1):
        h = lw.set(ad, "page", i); kay.append(kaydet(bolum, i, h)); idler += re.findall(rf'/guide/{bolum}/(\d+)', h)
    idler = list(dict.fromkeys(idler))
    yaz(bolum, kay, {"sayfa": n, "detay_id": idler})
    return idler


def secimli(bolum, ad, metod, alt=None):
    lw = LW(bolum); h0 = lw.yukle(ad); kay = [kaydet(bolum, "baslangic", h0)]
    for a in argumanlar(h0, metod):
        h = lw.cagir(ad, metod, _a(a)); kay.append(kaydet(bolum, f"{metod}_{a}", h))
        if alt:
            for b in argumanlar(h, alt):
                kay.append(kaydet(bolum, f"{metod}_{a}__{alt}_{b}", lw.cagir(ad, alt, _a(b))))
        if len(kay) % 25 == 0:
            print(f"    {bolum} {len(kay)}")
    yaz(bolum, kay, {"metod": metod, "alt_metod": alt})


def upgrade():
    lw = LW("upgrade"); h0 = lw.html["upgrade-rates"]
    ids = list(dict.fromkeys(re.findall(r"selected == '(\d+)'", h0)))
    yaz("upgrade", [kaydet("upgrade", "tum", h0)], {"scroll_id": ids, "not": "tum parsomen panelleri ilk HTML'de (Alpine x-show), secim istegi gerekmez"})


def beginner():
    lw = LW("beginner-items"); h0 = lw.yukle("beginner-items"); kay = [kaydet("beginner-items", "sinif_1", h0)]
    snf = list(dict.fromkeys(re.findall(r"activeClass['\"]?\s*,\s*(\d+)", h0) + re.findall(r"wire:click(?:\.[a-z]+)*=\"(?:setClass|selectClass)\((\d+)\)", h0)))
    for c in snf:
        if c != "1":
            kay.append(kaydet("beginner-items", f"sinif_{c}", lw.set("beginner-items", "activeClass", int(c))))
    yaz("beginner-items", kay, {"siniflar": snf})


def lazy_tek(bolum, ad):
    lw = LW(bolum); yaz(bolum, [kaydet(bolum, "tum", lw.yukle(ad))])


def drops():
    lw = LW("drops"); h = lw.yukle("drop-search"); kay = [kaydet("drops", "mobs_1", h)]
    kay.append(kaydet("drops", "items_1", lw.set("drop-search", "view", "items")))
    yaz("drops", kay, {"not": "Drop Arama = arama ekrani; tam drop verisi monsters_detay.json'da (her canavarin drop listesi + yuzde)"})


def resim_indir():
    os.makedirs(RES, exist_ok=True); ok = 0
    for u in list(RESIMLER):
        ad = re.sub(r"[^A-Za-z0-9_.-]+", "_", u.split("://", 1)[1])[-120:]
        yol = os.path.join(RES, ad)
        if not os.path.exists(yol):
            r = get(u)
            if r is None or r.status_code != 200 or not r.headers.get("content-type", "").startswith("image"):
                RESIMLER[u] = None; continue
            open(yol, "wb").write(r.content); time.sleep(0.05)
        RESIMLER[u] = os.path.relpath(yol, KOK).replace("\\", "/"); ok += 1
    json.dump(RESIMLER, open(os.path.join(OUT, "resimler.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  ✔ resim: {ok}/{len(RESIMLER)}")


if __name__ == "__main__":
    istek = set(sys.argv[1:])
    hepsi = not istek
    if os.path.exists(os.path.join(OUT, "resimler.json")):
        RESIMLER.update(json.load(open(os.path.join(OUT, "resimler.json"), encoding="utf-8")))
    if hepsi or "book" in istek: book()
    if hepsi or "monsters" in istek:
        mi = sayfali("monsters", "monster-database", r"(\d+) monster\s*·\s*sayfa \d+/(\d+)")      # metin() satira boler: '305 monster\n· sayfa 1/7'
        if hepsi or "detay" in istek: detaylar("monsters", mi)
    if hepsi or "quests" in istek:
        qi = sayfali("quests", "quest-database", r"görev\s*·\s*sayfa \d+/(\d+)")
        if hepsi or "detay" in istek: detaylar("quests", qi)
    if hepsi or "upgrade" in istek: upgrade()
    if hepsi or "cross-exchange" in istek: secimli("cross-exchange", "cross-exchanges", "selectGroup")
    if hepsi or "shozin" in istek: secimli("shozin", "mix-exchanges", "selectType", "selectRecipe")
    if hepsi or "narki" in istek: secimli("narki", "narki-crash", "selectPool")
    if hepsi or "pus-crash" in istek: secimli("pus-crash", "pus-crash", "selectGroup")
    if hepsi or "daily-quests" in istek: secimli("daily-quests", "daily-quests", "selectQuest")
    if hepsi or "event-rewards" in istek: secimli("event-rewards", "event-rewards", "selectEvent")
    if hepsi or "fragment" in istek: lazy_tek("fragment", "item-exchanges")
    if hepsi or "mining-fishing" in istek: lazy_tek("mining-fishing", "mining-fishing")
    if hepsi or "beginner-items" in istek: beginner()
    if hepsi or "drops" in istek: drops()
    resim_indir()

# -*- coding: utf-8 -*-
# KENDI KONULARIMIZ EN (13 Eki aksam PATRON "ENG MI BU APTAL") — KB tabanli konular (TeamSpeak, Sezon, Madencilik, Genie, Yayinci, PUS).
# _forum_en.py ile ayni yontem: TR = tek kaynak, ceviri sozlugu <klasor>/ceviri_en.json = {"baslik": EN, "metin": {TR parca: EN parca}, "izin": [...]}
#   parca = (1) uretici bloklari (<klasor>/bloklar.json, KB.kaydet) + resim aciklamalari  (2) gorsel kartlarin HTML yazi dugumleri (<gorsel>.KARTLAR)
# EN resimler: ayni kart HTML'i, yazi dugumleri sozlukten -> <klasor>/resim_en/ (ayni ad). Turkce yazili GIF'ler (GSAYIM / GTAKVIM) EN'de yok (odul pilotu gibi).
# Eksik ceviri / EN'de Turkce harf / kartin disina tasan yazi = ASSERT.
#   python _konu_en.py sablon teamspeak   -> <klasor>/ceviri_tr.txt (numarali)
#   python _konu_en.py birlestir teamspeak -> ceviri_tr.txt + ceviri_en_no.json ({"no": "EN"}) -> ceviri_en.json
#   python _konu_en.py resim teamspeak     -> resim_en/*.jpg
#   python _konu_en.py yaz teamspeak       -> konu_en.json (+ _konu_kit.py EN sayfaya alir)
import os, re, sys, json, html, base64, importlib
import _konu_blok as KB
import _repo_resim

KOK = os.path.dirname(os.path.abspath(__file__))
KONULAR = {"teamspeak": ("teamspeak", "_ts_gorsel"), "sezon": ("sezon", "_sezon_gorsel"), "mining": ("mining", "_mining_gorsel"),
           "genie": ("genie", "_genie_gorsel"), "yayinci": ("yayinci", "_yayinci_gorsel"), "pus": ("pus_kupon", "_pus_gorsel"),
           "yeni": ("yeni_konu", None), "kisa": ("yeni_konu/kisa", None), "skill": ("skill_master", "_skill_gorsel")}   # yeni / kisa / skill: kendi ciziciler (--en)      # yeni: kendi cizicisi (_yeni_konu.py --en) — burada sadece sablon / birlestir; resimleri ekran goruntusu (cizilmez)
TR_GIF = {"GSAYIM", "GTAKVIM"}
TR_HARF = re.compile(r"[ğüşıöçĞÜŞİÖÇ]")
STIL = re.compile(r"(<style.*?</style>|<script.*?</script>)", re.S)


def _yazi(s): return isinstance(s, str) and any(c.isalpha() for c in s) and not s.startswith("http")
def _kl(konu): return os.path.join(KOK, *KONULAR[konu][0].split("/"))


def bloklar(konu):
    J = json.load(open(os.path.join(_kl(konu), "bloklar.json"), encoding="utf-8"))
    B = [tuple(b) for b in J["B"] if not (b[0] in ("afis", "banner", "img") and b[1] in TR_GIF)]
    return J["baslik"], B, {k: tuple(v) for k, v in J["RES"].items() if k not in TR_GIF}


def _atla(b, i):     # resim id / bolum emojisi / rehber yolu
    return (b[0] in ("img", "afis", "banner", "imgs") and i == 1) or (b[0] == "h" and i == 1) or (b[0] == "rlink" and i == 2)


def cevir_bloklar(B, M):
    return [tuple([b[0]] + [x if _atla(b, i) else ([T(s, M) for s in x] if isinstance(x, list) else T(x, M)) for i, x in enumerate(b[1:], 1)]) for b in B]


def _dugumler(h):
    """kart HTML -> yazi dugumleri (style / script haric), html-unescape + strip."""
    L = []
    for parca in STIL.split(h):
        if STIL.fullmatch(parca or ""): continue
        for m in re.finditer(r">([^<]+)<", parca):
            t = html.unescape(m.group(1)).strip()
            if _yazi(t): L.append(t)
    return L


def kartlar(konu):
    return importlib.import_module(KONULAR[konu][1]).KARTLAR if KONULAR[konu][1] else []


def parcalar(konu):
    baslik, B, RES = bloklar(konu)
    L = []
    def ek(s):
        if _yazi(s) and s not in L: L.append(s)
    for b in B:
        for i, x in enumerate(b[1:], 1):
            if _atla(b, i): continue
            for s in (x if isinstance(x, list) else [x]): ek(s)
    for rid, (dosya, acik, url) in RES.items(): ek(acik)
    J = json.load(open(os.path.join(_kl(konu), "bloklar.json"), encoding="utf-8"))
    for a, p in (J.get("REHBER_LINK") or {}).values(): ek(a)          # yeni: "Rehberde ac: <etiket>"
    for ad, f in kartlar(konu):
        for s in _dugumler(f()): ek(s)
    return baslik, L


def sozluk(konu):
    p = os.path.join(_kl(konu), "ceviri_en.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _isaret(tr, en):
    assert tr.count("**") == en.count("**"), ("** sayisi", tr, en)
    assert re.findall(r"\[\[([^|\]]*)\|", tr) == re.findall(r"\[\[([^|\]]*)\|", en), ("link url", tr, en)


def _sayi(s):
    """harfsiz sayi yazisi TR -> EN bicim: 1.970 -> 1,970 · 0,20 -> 0.20 · %0,20 -> 0.20% (url'e dokunmaz). 13 Eki: madencilik kartlari '%0,20' kalmisti."""
    if not isinstance(s, str) or s.startswith("http") or any(c.isalpha() for c in s): return s
    s = re.sub(r"\b\d{1,3}(?:\.\d{3})+\b", lambda m: m.group(0).replace(".", "§"), s)
    s = re.sub(r"\b(\d{1,2}),(\d{1,2})\b", r"\1.\2", s).replace("§", ",")   # ondalik en cok 2+2 hane: koordinat (849,660) bozulmasin (13 Eki S09)
    return re.sub(r"%(\d+(?:\.\d+)?)", r"\1%", s)


def T(s, M):
    if not _yazi(s): return _sayi(s)
    assert M.get(s), ("ceviri yok", s)
    return M[s]


def kart_en(h, M):
    """kart HTML'inin yazi dugumlerini cevir (bosluklar korunur)."""
    def d(m):
        ham = m.group(1); t = html.unescape(ham).strip()
        if not _yazi(t): return ">" + _sayi(ham) + "<"
        b, s = re.match(r"^\s*", ham).group(0), re.search(r"\s*$", ham).group(0)
        return ">" + b + html.escape(T(t, M), quote=False) + s + "<"
    return "".join(p if STIL.fullmatch(p or "") else re.sub(r">([^<]+)<", d, p) for p in STIL.split(h))


# ---------------------------------------------------------------- komutlar
def sablon(konu):
    baslik, L = parcalar(konu)
    open(os.path.join(_kl(konu), "ceviri_tr.txt"), "w", encoding="utf-8").write(f"0\t{baslik}\n" + "".join(f"{i}\t{s}\n" for i, s in enumerate(L, 1)))
    return len(L)


def birlestir(konu):
    _, L = parcalar(konu)
    E = json.load(open(os.path.join(_kl(konu), "ceviri_en_no.json"), encoding="utf-8"))
    eski = sozluk(konu) or {}
    izin = E.pop("izin", eski.get("izin", []))
    assert set(E) == {str(i) for i in range(len(L) + 1)}, ("numara uyusmuyor", len(L) + 1, len(E))
    bos = [n for n, v in E.items() if not v.strip()]; assert not bos, ("bos ceviri", bos)
    M = {s: E[str(i)] for i, s in enumerate(L, 1)}
    for tr, en in M.items(): _isaret(tr, en)
    json.dump({"baslik": E["0"], "metin": M, "izin": izin}, open(os.path.join(_kl(konu), "ceviri_en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.remove(os.path.join(_kl(konu), "ceviri_tr.txt")); os.remove(os.path.join(_kl(konu), "ceviri_en_no.json"))
    return len(M)


def resim(konu):
    from playwright.sync_api import sync_playwright
    M = sozluk(konu)["metin"]; RD = os.path.join(_kl(konu), "resim_en"); os.makedirs(RD, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=1)
        for ad, f in kartlar(konu):
            pg.set_content(kart_en(f(), M), wait_until="load")
            tas = pg.evaluate("(()=>{const k=document.querySelector('#kart'),kr=k.getBoundingClientRect().right;let m=0;k.querySelectorAll('*').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().right)});return [kr,m,k.scrollWidth,k.clientWidth]})()")
            assert tas[1] <= tas[0] + 1 and tas[2] <= tas[3] + 1, (ad, "EN yazi kartin disina tasiyor", tas)
            kalan = pg.evaluate("document.querySelector('#kart').innerText.match(/\\S*[ğüşıöçĞÜŞİÖÇ]\\S*/g)")
            izin = sozluk(konu).get("izin", [])
            kalan = [w for w in (kalan or []) if not any(z in w for z in izin)]
            assert not kalan, (ad, "EN kartta Turkce", kalan[:5])
            pg.locator("#kart").screenshot(path=os.path.join(RD, ad), type="jpeg", quality=90)
            print("  ", ad, os.path.getsize(os.path.join(RD, ad)) // 1024, "KB")
        b.close()


def yaz(konu):
    from PIL import Image
    S = sozluk(konu); M = S["metin"]
    for tr, en in M.items(): _isaret(tr, en)
    baslik, B, RES = bloklar(konu)
    eksik = [s for s in parcalar(konu)[1] if not M.get(s)]; assert not eksik, (konu, len(eksik), eksik[:3])
    Be = cevir_bloklar(B, M)
    RESe = {k: (d, T(a, M), u) for k, (d, a, u) in RES.items()}
    KB.DIL = "en"
    try:
        L, NO = KB.basliklar(Be)
        BB, HT, MD, DZ = KB.bb(Be), KB.onizleme(Be), KB.md(Be), KB.duz(Be, RESe)
        KB.denetle(BB, RESe)
    finally:
        KB.DIL = "tr"
    kl = KONULAR[konu][0]; res = []
    for rid, (dosya, acik, url) in RESe.items():
        d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "SexyKO (EN)"}
        if dosya:
            p = os.path.join(_kl(konu), "resim_en", dosya); assert os.path.exists(p), ("EN resim yok — python _konu_en.py resim " + konu, p)
            raw = open(p, "rb").read()
            with Image.open(p) as im: d["boyut"] = f"{im.width}x{im.height}"
            d.update(dosya=f"FORUM/{kl}/resim_en/{dosya}", data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
        res.append(d)
    _repo_resim.uygula(res)
    tam = re.sub(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", "", BB)
    kalan = [w for w in re.findall(r"\S*[ğüşıöçĞÜŞİÖÇ]\S*", re.sub(r"https?://\S+", "", tam)) if not any(z in w for z in S.get("izin", []))]
    assert not kalan, (konu, "EN'de Turkce harf", kalan[:5])
    assert not TR_HARF.search(S["baslik"]), S["baslik"]
    kontrol = [f"**English version (13 Oct):** same structure as the Turkish topic — every text translated (`FORUM/{kl}/ceviri_en.json`), numbers and links unchanged.",
               f"**{sum(1 for r in res if r['dosya'])} images** redrawn in English (`FORUM/{kl}/resim_en/`, same layout as the Turkish images)."
               + (" The Turkish countdown / calendar GIF is not in the English version." if any(x in json.load(open(os.path.join(_kl(konu), "bloklar.json"), encoding="utf-8"))["RES"] for x in TR_GIF) else "")]
    V = {"baslik": S["baslik"], "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": kontrol,
         "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": f"FORUM/{kl}/ceviri_en.json (= Turkish topic, translated)"}
    json.dump(V, open(os.path.join(_kl(konu), "konu_en.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return len(BB), len(res)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    kom, konu = sys.argv[1], sys.argv[2]
    if kom == "sablon": print(konu, sablon(konu), "parca ->", os.path.join(_kl(konu), "ceviri_tr.txt"))
    elif kom == "birlestir": print(konu, birlestir(konu), "ceviri")
    elif kom == "resim": resim(konu)
    elif kom == "yaz": print(konu, "bbcode / resim:", yaz(konu))

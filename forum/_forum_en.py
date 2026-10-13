# -*- coding: utf-8 -*-
# FORUM KONULARI EN (13 Eki aksam PATRON "ENG MI BU APTAL" — FORUM_KONU_EN.html'de 38 forum konusunun icerigi Turkce kalmisti).
# Ceviri: forum_en/dNNN.json = {"baslik": EN konu basligi, "metin": {TR parca: EN parca}, "izin": [EN'de kalabilecek Turkce harfli ozel ad]}
#   parca = FY.insa bloklarindaki her yazi (h emojisi / resim id / url haric). Isaretler korunur: ** kalin, [[url|metin]] link (ASSERT).
# Yapi TR ile AYNI: once TR bloklar + FK.kartla (kart turu kararlari Turkce basliklara bakar), sonra yazilar sozlukten -> EN bloklar + EN kartlar.
# Eksik ceviri = ASSERT (sessiz Turkce kalmaz) · EN BBCode'da Turkce harf kalirsa ASSERT (url'ler + "izin" haric).
#   python _forum_en.py sablon 12 25   -> forum_en/d012_tr.txt (numarali TR parcalar, cevrilecek liste)
#   python _forum_en.py birlestir 12   -> forum_en/d012_tr.txt + d012_en.json ({"no": "EN"}, "baslik") -> forum_en/d012.json
#   python _forum_en.py kart 12        -> EN kartlari ciz (forum_kart_en/d012/)
#   python _forum_en.py kontrol        -> her konu: parca / cevrili / kart
# _konu_kit.py: VERI_EN.update(_forum_en.hepsi(VERI)) — sadece cevirisi TAM ve kartlari cizili konular (digerleri EN sayfada TR + "TR" etiketi).
import os, re, sys, json, copy
import _forum_yeniden as FY
import _forum_kart as FK
import _konu_blok as KB
import _repo_resim

KOK = os.path.dirname(os.path.abspath(__file__))
ED = os.path.join(KOK, "forum_en")
TR_HARF = re.compile(r"[ğüşıöçĞÜŞİÖÇ]")
ACIKLAMA = {"Konu — bir bakışta": "Topic — at a glance"}
EK = {" — ekran görüntüsü": " — screenshot", " — adımlar": " — steps", " — özet": " — summary"}


def _yazi(s): return isinstance(s, str) and any(c.isalpha() for c in s) and not s.startswith("http")


def _atla(b, i): return (b[0] in ("img", "afis", "banner") and i == 1) or (b[0] == "h" and i == 1)    # resim id / bolum emojisi


def parcalar(Bl):
    L = []
    for b in Bl:
        for i, x in enumerate(b[1:], 1):
            if _atla(b, i): continue
            for s in (x if isinstance(x, list) else [x]):
                if _yazi(s) and s not in L: L.append(s)
    return L


def konular():
    import _forum_sekme as FS
    B = json.load(open(os.path.join(KOK, "forum_bbcode", "bbcode.json"), encoding="utf-8"))
    import _forum_duzeltme as FD                                    # 13 Eki: TR ile ayni kaynak duzeltmesi
    return [FD.uygula(k) for k in B["konular"] if k["id"] not in FS.BIZIM and k["mesajlar"] and "html" in k["mesajlar"][0]]


def _yol(did, ek=".json"): return os.path.join(ED, f"d{did:03d}{ek}")


def sozluk(did):
    p = _yol(did)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _isaret(tr, en):
    """** sayisi + [[url|...]] url'leri ayni olmali (kalin / link bozulmasin)."""
    assert tr.count("**") == en.count("**"), ("** sayisi", tr, en)
    assert re.findall(r"\[\[([^|\]]*)\|", tr) == re.findall(r"\[\[([^|\]]*)\|", en), ("link url", tr, en)


def T(s, M):
    if not _yazi(s): return s
    assert M.get(s), ("ceviri yok", s)
    return M[s]


def _onekli(s, M):
    """'🎮 OYUN AYARLARI' (emoji + bolum basligi) -> '🎮 GAME SETTINGS'."""
    if s in M: return M[s]
    for i, c in enumerate(s):
        if c == " " and s[i + 1:] in M: return s[:i + 1] + M[s[i + 1:]]
    raise AssertionError(("onekli ceviri yok", s))


def cevir_Bl(Bl, M):
    out = []
    for b in Bl:
        y = [b[0]]
        for i, x in enumerate(b[1:], 1):
            if _atla(b, i): y.append(x)
            elif isinstance(x, list): y.append([T(s, M) for s in x])
            else: y.append(T(x, M))
        out.append(tuple(y))
    return out


def cevir_kart(kt, M, ust_en, em):
    e = copy.deepcopy(kt)
    e["konu"], e["konu_alt"] = ust_en[1], ust_en[2]
    e["baslik"] = f"{em} {ust_en[1]}" if kt["tur"] == "kapak" else _onekli(kt["baslik"], M)
    a = kt["aciklama"]
    if a in ACIKLAMA: e["aciklama"] = ACIKLAMA[a]
    else:
        son = next(x for x in EK if a.endswith(x)); e["aciklama"] = T(a[:-len(son)], M) + EK[son]
    if "bolumler" in kt: e["bolumler"] = [(ic, T(t, M)) for ic, t in kt["bolumler"]]
    for f in ("ogeler", "metin"):
        if f in kt: e[f] = [T(s, M) for s in kt[f]]
    e["dosya"] = kt["dosya"].replace("FORUM/forum_kart/", "FORUM/forum_kart_en/")
    return e


def en_yapi(k):
    """k -> (EN bloklar, EN kartlar, R, sozluk). Sozluk eksikse AssertionError."""
    S = sozluk(k["id"]); assert S, ("sozluk yok", k["id"])
    M = S["metin"]
    for tr, en in M.items(): _isaret(tr, en)
    Bl, R, _ = FY.insa(k, set(k.get("kirik_url") or []))
    yeni, KL = FK.kartla(k, Bl, R)
    eksik = [s for s in parcalar(Bl) if not M.get(s)]
    assert not eksik, (k["id"], len(eksik), eksik[:3])
    ust = next(b for b in Bl if b[0] == "baslik")
    ust_en = ("baslik", T(ust[1], M), T(ust[2], M))
    em = FY.emoji_ayir(k["baslik"])[0] or "📘"
    return cevir_Bl(yeni, M), [cevir_kart(kt, M, ust_en, em) for kt in KL], R, S


def veri_en(k, r01=None):
    """_forum_sekme.veri'nin EN esi (ayni anahtarlar) — FORUM_KONU_EN.html V_EN['f<id>']."""
    Bl, KL, R, S = en_yapi(k)
    KB.DIL = "en"
    try:
        BB = KB.bb(Bl)
        kullanilan = set(re.findall(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", BB))
        res = []
        if "R01" in kullanilan:
            assert r01, "R01 logo kaydi yok"; res.append({x: r01[x] for x in r01 if x != "data"} | {"data": None})
        for rid, (_, acik, url) in R.items():
            if rid in kullanilan:
                res.append({"id": rid, "aciklama": "forum image" if acik.startswith("forumdaki") else ("topic banner" if acik == "konu afişi" else acik),
                            "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum"})
        kartlar = []
        for kt in KL:
            assert os.path.exists(os.path.join(KOK, *kt["dosya"][len("FORUM/"):].split("/"))), ("EN kart cizilmemis — python _forum_en.py kart", kt["dosya"])
            kartlar.append({"id": kt["id"], "aciklama": kt["aciklama"], "varsayilan_url": "", "dosya": kt["dosya"], "data": None, "kb": None, "boyut": None, "kaynak": "kart"})
        _repo_resim.uygula(kartlar); res += kartlar
        from PIL import Image
        for r in kartlar:      # itemiconrepo'da yoksa (push oncesi) onizleme yerel kopyadan (HTML/ -> ../FORUM/...); BBCode CDN linkini kullanir
            yl = os.path.join(KOK, *r["dosya"][len("FORUM/"):].split("/")); w, h = Image.open(yl).size
            r["boyut"], r["kb"] = f"{w}x{h}", round(os.path.getsize(yl) / 1024)
            if not os.path.exists(os.path.join(_repo_resim.REPO_KLASOR, "forum", *_repo_resim.surumlu(r["dosya"]).split("/"))):
                r["data"] = "../" + r["dosya"]
        RES = {r["id"]: (None, r["aciklama"], r["varsayilan_url"]) for r in res}
        KB.denetle(BB, RES)
        tam = re.sub(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", lambda m: RES[m.group(1)][2], BB)
        izin = S.get("izin", [])
        kalan = [w for w in re.findall(r"\S*[ğüşıöçĞÜŞİÖÇ]\S*", re.sub(r"https?://\S+", "", tam)) if not any(z in w for z in izin)]
        assert not kalan, (k["id"], "EN'de Turkce harf", kalan[:5])
        HT = KB.onizleme(Bl).replace("<img ", '<img loading="lazy" ')
        kontrol = [f"**English version (13 Oct):** same structure as the Turkish topic — every text translated (forum_en/d{k['id']:03d}.json), images and links unchanged.",
                   f"**{len(KL)} visual cards** in English (itemiconrepo `forum/forum_kart_en/d{k['id']:03d}/`). Screenshots are from the game (Turkish UI).",
                   f"**Source:** forum.sexyko.com/d/{k['id']} — {k['yazar']} · {k['acilis'][:10]}. Old version: **📜 Forum version** tab (Turkish)."]
        return {"baslik": S["baslik"], "bbcode": BB, "html": HT, "markdown": KB.md(Bl), "duz": KB.duz(Bl, RES), "resimler": res, "kontrol": kontrol,
                "bolum": [f"{x[0]} {x[1]}" for x in KB.basliklar(Bl)[0]], "kaynak": k["url"], "orijinal": k["mesajlar"][0]["bbcode"], "kart_sayi": len(KL)}
    finally:
        KB.DIL = "tr"


def hazir(k):
    S = sozluk(k["id"])
    if not S: return False
    try: Bl, KL, _, _ = en_yapi(k)
    except AssertionError: return False
    return all(os.path.exists(os.path.join(KOK, *kt["dosya"][len("FORUM/"):].split("/"))) for kt in KL)


def hepsi(VERI):
    """_konu_kit.py: cevirisi tam + kartlari cizili forum konulari -> {'f<id>': EN veri}."""
    r01 = next((r for v in VERI.values() if isinstance(v, dict) and v.get("resimler") for r in v["resimler"] if r.get("id") == "R01" and r.get("varsayilan_url")), None)
    out = {f"f{k['id']}": veri_en(k, r01) for k in konular() if hazir(k)}
    # EN kartlarin repo listesi (_repo_aktar.py KONULAR "forum_kart_en/konu.json" -> icerik ozetli kopyalar) — TR'deki forum_kart/konu.json gibi
    kart = [r for v in out.values() for r in v["resimler"] if r.get("kaynak") == "kart"]
    json.dump({"resimler": kart}, open(os.path.join(KOK, "forum_kart_en", "konu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


# ---------------------------------------------------------------- komutlar
def sablon(did):
    k = next(x for x in konular() if x["id"] == did)
    Bl, _, _ = FY.insa(k, set(k.get("kirik_url") or []))
    os.makedirs(ED, exist_ok=True)
    L = parcalar(Bl)
    open(_yol(did, "_tr.txt"), "w", encoding="utf-8").write(f"0\t{k['baslik']}\n" + "".join(f"{i}\t{s}\n" for i, s in enumerate(L, 1)))
    return len(L)


def birlestir(did):
    k = next(x for x in konular() if x["id"] == did)
    Bl, _, _ = FY.insa(k, set(k.get("kirik_url") or []))
    L = parcalar(Bl)
    E = json.load(open(_yol(did, "_en.json"), encoding="utf-8"))
    eski = sozluk(did) or {}
    izin = E.pop("izin", eski.get("izin", []))                      # ozel ad (takim adi vb.) EN'de Turkce harfle kalabilir
    assert set(E) =={str(i) for i in range(len(L) + 1)}, ("numara uyusmuyor", len(L) + 1, len(E))
    bos = [n for n, v in E.items() if not v.strip()]; assert not bos, ("bos ceviri", bos)
    M = {s: E[str(i)] for i, s in enumerate(L, 1)}
    for tr, en in M.items(): _isaret(tr, en)
    json.dump({"baslik": E["0"], "metin": M, "izin": izin},open(_yol(did), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.remove(_yol(did, "_tr.txt")); os.remove(_yol(did, "_en.json"))
    return len(M)


def _ss_tr_karttan(dosya_tr):
    """13 Eki: forumdaki ekran goruntusu artik 404 (d/38, d/41) -> 8 Eki cizilmis TR kartindaki ekran goruntusunu kirp.
    Kutu = 2 px #6b5426 cerceve (FK.cizim .ss). Her yarida cerceve rengine EN COK uyan sutun / satir = kenar (esik degil argmax:
    1. deneme sabit esik -> JPEG ust kenari bulandirmis, d/38 K01 bulunamadi; 2. deneme koyu zemin disi -> d/41 K02 kenar bosluklarini katti)."""
    import io, base64
    from PIL import Image
    im = Image.open(os.path.join(KOK, *dosya_tr[len("FORUM/"):].split("/"))).convert("RGB"); W, H = im.size; px = im.load()
    renk = lambda p: abs(p[0] - 107) < 30 and abs(p[1] - 84) < 30 and abs(p[2] - 38) < 30
    Y0 = 110
    sut = {x: sum(renk(px[x, y]) for y in range(Y0, H - 6)) for x in range(6, W - 6)}
    sol = max((x for x in sut if x < W // 2), key=sut.get); sag = max((x for x in sut if x >= W // 2), key=sut.get)
    # ust / alt: oyun arayuzunde de uzun altin cizgiler var (d/41 y=338) -> sol-sag arasinin yarisini kaplayan ILK / SON satir (cerceve resmin disinda)
    yatay = [y for y in range(Y0, H - 6) if sum(renk(px[x, y]) for x in range(sol, sag + 1)) >= (sag - sol) // 2]
    ust, alt = min(yatay), max(yatay)
    kutu = (sol + 3, ust + 3, sag - 2, alt - 2)
    assert kutu[2] - kutu[0] > 100 and kutu[3] - kutu[1] > 60, ("cerceve kucuk", dosya_tr, kutu)
    b = io.BytesIO(); c = im.crop(kutu); c.save(b, "PNG")
    return base64.b64encode(b.getvalue()).decode(), c.width


def kart(sec):
    from playwright.sync_api import sync_playwright
    from urllib.error import HTTPError
    asil_ss = FK._ss
    say, hata = 0, []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=1)
        for k in konular():
            if k["id"] not in sec: continue
            _, KL, _, _ = en_yapi(k)
            os.makedirs(os.path.join(KOK, "forum_kart_en", f"d{k['id']:03d}"), exist_ok=True)
            for kt in KL:
                yol = os.path.join(KOK, *kt["dosya"][len("FORUM/"):].split("/"))
                try:
                    try: h_ = FK.cizim(kt)
                    except HTTPError:                 # kaynak resim 404 -> TR kartindan kirp
                        FK._ss = lambda src, d=kt["dosya"].replace("FORUM/forum_kart_en/", "FORUM/forum_kart/"): _ss_tr_karttan(d)
                        try: h_ = FK.cizim(kt)
                        finally: FK._ss = asil_ss
                        print(f"   d/{k['id']} {kt['id']}: kaynak 404 -> TR kartindan kirpildi")
                    pg.set_content(h_, wait_until="load")
                    tas = pg.evaluate("(()=>{const k=document.querySelector('#kart'),kr=k.getBoundingClientRect().right;let m=0;k.querySelectorAll('*').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().right)});return [kr,m,k.scrollWidth,k.clientWidth]})()")
                    assert tas[1] <= tas[0] + 1 and tas[2] <= tas[3] + 1, ("tasma", tas)
                    pg.locator("#kart").screenshot(path=yol, type="jpeg", quality=88); say += 1
                except Exception as ex:
                    hata.append((k["id"], kt["id"], kt["tur"], str(ex)[:90]))
            print(f"d/{k['id']:<3} {len(KL):>2} EN kart")
        b.close()
    print(f"EN kart cizildi: {say} · hata {len(hata)}")
    for h in hata: print("   HATA", h)
    return not hata


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    kom, ids = sys.argv[1], [int(x) for x in sys.argv[2:] if x.isdigit()]
    if kom == "sablon":
        for d in ids: print(f"d/{d}: {sablon(d)} parca -> {_yol(d, '_tr.txt')}")
    elif kom == "birlestir":
        for d in ids: print(f"d/{d}: {birlestir(d)} ceviri -> {_yol(d)}")
    elif kom == "kart":
        sys.exit(0 if kart(set(ids)) else 1)
    elif kom == "kontrol":
        for k in konular():
            S = sozluk(k["id"]); print(f"d/{k['id']:<3} {'HAZIR' if hazir(k) else ('sozluk var' if S else '-'):<10} {k['baslik'][:50]}")

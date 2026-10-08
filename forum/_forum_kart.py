# -*- coding: utf-8 -*-
# FORUM KONULARINA GORSEL KARTLAR (patron 8 Eki: "gorsel kartlari da yap hepsine go"). Kart stili: _skill_gorsel.kart (Genie / Yayinci kartlari ile ayni).
# Kartlar KONUNUN KENDI icerigiyle (uydurma yok):
#   K00 kapak  — konu basligi + alt baslik + bolum haritasi (bolum basliklari emojileriyle)
#   Knn ekran  — forumdaki her ekran goruntusu bizim cercevede, bolum basligiyla (afis haric)
#   Knn liste  — KISACASI / OZET / AVANTAJ bolumunun maddeleri -> onay kartlari (metinde TEKRAR EDILMEZ — patron 7 Eki "resimde var, yazman lazim miydi")
#   Knn adim   — 1️⃣ 2️⃣ 3️⃣ / "1." adim satirlari (3+) -> adim kartlari (metinde tekrar edilmez)
# kartla(): blok listesini kartli hale getirir (_forum_sekme.veri kullanir) · python _forum_kart.py: butun kartlari cizer -> forum_kart/dNNN/*.jpg
import os, re, io, base64, html
import _forum_yeniden as FY

KOK = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(KOK, "forum_kart")
OZET_BAS = re.compile(r"KISACA|ÖZET|AVANTAJ|SONUÇ|NE KAZANDIRIR|NELER", re.I)
ADIM = re.compile(r"^\s*(?:[0-9]️?⃣|🔟|\*\*[0-9]️?⃣\*\*|\d{1,2}[.)]\s)")
ATLA = {"BAĞLANTILAR"}


def _kisa(s, n=110):
    s = re.sub(r"\[\[[^|\]]*\|([^\]]*)\]\]", r"\1", s).replace("**", "")
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def kartla(k, Bl, RES):
    """Bl (FY.insa ciktisi) -> (yeni Bl, kartlar). kart = {id, tur, dosya, aciklama, baslik, ...cizim verisi}, kartlara tasinan metin 'metin'de."""
    did = k["id"]; ust = next(b for b in Bl if b[0] == "baslik")
    bolumler = [(b[1], b[2]) for b in Bl if b[0] == "h" and b[2] not in ATLA]
    kartlar, yeni, n = [], [], [0]
    def kart(tur, **v):
        kid = f"K{n[0]:02d}"; n[0] += 1
        v.update(id=kid, tur=tur, dosya=f"FORUM/forum_kart/d{did:03d}/{kid}_{tur}.jpg", konu=ust[1], konu_alt=ust[2], d=did)
        kartlar.append(v); return kid
    afis = next((b[1] for b in Bl if b[0] == "afis"), None)
    bolum, ilk_h = None, True
    for b in Bl:
        t = b[0]
        if t == "h":
            bolum = b; yeni.append(b)
            if ilk_h:
                ilk_h = False
                kid = kart("kapak", aciklama="Konu — bir bakışta", baslik=f"{FY.emoji_ayir(k['baslik'])[0] or '📘'} {ust[1]}", bolumler=[x for x in bolumler if x[1] != "BİR BAKIŞTA"])
                yeni.append(("img", kid, ""))
            continue
        if t == "img" and b[1] in RES and b[1] != afis and bolum and bolum[2] not in ATLA:
            kid = kart("ekran", aciklama=f"{bolum[2]} — ekran görüntüsü", baslik=f"{bolum[1]} {bolum[2]}", src=RES[b[1]][2])
            yeni.append(("img", kid, "")); continue
        if t in ("liste", "satirlar") and bolum and bolum[2] not in ATLA:
            ogeler = b[1]
            adimlar = [x for x in ogeler if ADIM.match(x)]
            if len(adimlar) >= 3 and len(adimlar) == len(ogeler) and all(len(x) <= 140 for x in ogeler):
                kid = kart("adim", aciklama=f"{bolum[2]} — adımlar", baslik=f"{bolum[1]} {bolum[2]}", ogeler=ogeler, metin=ogeler)
                yeni.append(("img", kid, "")); continue
            if OZET_BAS.search(bolum[2]) and len(ogeler) >= 3 and all(len(x) <= 120 for x in ogeler):
                kid = kart("liste", aciklama=f"{bolum[2]} — özet", baslik=f"{bolum[1]} {bolum[2]}", ogeler=ogeler, metin=ogeler)
                yeni.append(("img", kid, "")); continue
        yeni.append(b)
    return yeni, kartlar


# ---------------------------------------------------------------- cizim
def _ss(src):
    import urllib.request
    from PIL import Image
    r = urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (SexyKO GM forum kart)"}), timeout=40)
    raw = r.read(); im = Image.open(io.BytesIO(raw)); im.load()
    if getattr(im, "is_animated", False): im.seek(0)
    im = im.convert("RGB"); w = im.width
    b = io.BytesIO(); im.save(b, "PNG")
    return base64.b64encode(b.getvalue()).decode(), w


def cizim(kt):
    import _skill_gorsel as SG
    A, A2 = SG.ALTIN, SG.ALTIN2; e = lambda s: SG.e(s).replace("&#x27;", "’")
    et = "SEXYKO · " + _kisa(re.sub(r"^SEXYKO(?:'DA|’DA)?\s+", "", kt["konu"], flags=re.I), 60)
    css = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.ss{{display:block;margin:0 auto;border-radius:8px;border:2px solid #6b5426;box-shadow:0 6px 20px rgba(0,0,0,.45);max-width:100%}}
.g{{display:grid;gap:12px}} .g .kut{{text-align:center;padding:16px 10px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}}
.g .ic{{font-size:34px;line-height:1}} .g .b{{font-size:16px;font-weight:900;color:{A2};letter-spacing:.3px;line-height:1.3}}
.g .no{{font-size:13px;font-weight:800;color:#a89f91}}
.ls{{display:grid;gap:10px}} .ls .kut{{display:flex;gap:12px;align-items:flex-start;padding:12px 14px}}
.ls .ok{{flex:none;width:30px;height:30px;border-radius:50%;background:{A};color:#1b1400;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:16px}}
.ls .t{{font-size:16px;line-height:1.45;color:#e8dcc8}} .ls .t b{{color:{A2}}}
.ad{{display:grid;gap:12px}} .ad .kut{{text-align:center;padding:16px 10px}}
.ad .no{{width:40px;height:40px;margin:0 auto 8px;border-radius:50%;background:{A};color:#1b1400;font-weight:900;font-size:20px;display:flex;align-items:center;justify-content:center}}
.ad .t{{font-size:16px;line-height:1.45;font-weight:700;color:#e8dcc8}}
.tek{{text-align:center;font-size:17px;color:#e8dcc8;padding:18px}}
"""
    tur = kt["tur"]
    if tur == "kapak":
        L = kt["bolumler"]
        if len(L) >= 2:
            sut = 3 if len(L) in (3, 5, 6, 9) else min(4, len(L))
            g = f'<div class="g" style="grid-template-columns:repeat({sut},1fr)">' + "".join(
                f'<div class="kut"><div class="no">{i:02d}</div><div class="ic">{ic}</div><div class="b">{e(t)}</div></div>' for i, (ic, t) in enumerate(L, 1)) + "</div>"
        else:
            g = f'<div class="kut tek">📄 {e(kt["konu_alt"])}<br><span style="color:#a89f91;font-size:14px">forum.sexyko.com/d/{kt["d"]}</span></div>'
        return SG.kart(g, e(kt["baslik"]), e(kt["konu_alt"]), et, css)
    if tur == "ekran":
        b64, w = _ss(kt["src"])
        gen = 900 if w >= 600 else w
        img = f'<img class="ss" src="data:image/png;base64,{b64}" style="width:{gen}px" alt="">'
        return SG.kart(img, e(kt["baslik"]), e(kt["konu"]), et, css)
    if tur == "liste":
        L = kt["ogeler"]; sut = 2 if len(L) >= 4 else 1
        def ic(s):
            em, r = FY.emoji_ayir(re.sub(r"^\*\*|\*\*$", "", s))
            return (em or "✓"), (r if em else s)
        g = f'<div class="ls" style="grid-template-columns:repeat({sut},1fr)">' + "".join(
            f'<div class="kut"><div class="ok">{ic(x)[0]}</div><div class="t">{_md(e, ic(x)[1].rstrip(" ,;"))}</div></div>' for x in L) + "</div>"
        return SG.kart(g, e(kt["baslik"]), e(kt["konu"]), et, css)
    if tur == "adim":
        L = [FY.NUMARA.sub("", re.sub(r"^\*\*([0-9]️?⃣|🔟)\*\*\s*", "", re.sub(r"^\s*([0-9]️?⃣|🔟)\s*", "", x))) for x in kt["ogeler"]]
        sut = 4 if len(L) in (4, 7, 8) or len(L) > 9 else 3
        g = f'<div class="ad" style="grid-template-columns:repeat({sut},1fr)">' + "".join(
            f'<div class="kut"><div class="no">{i}</div><div class="t">{_md(e, x)}</div></div>' for i, x in enumerate(L, 1)) + "</div>"
        return SG.kart(g, e(kt["baslik"]), e(kt["konu"]), et, css)
    raise ValueError(tur)


def _md(e, s):
    s = re.sub(r"\[\[[^|\]]*\|([^\]]*)\]\]", r"\1", s)
    parca = s.split("**")
    return "".join(e(p) if i % 2 == 0 else f"<b>{e(p)}</b>" for i, p in enumerate(parca))


def hepsi():
    """bbcode.json -> 38 konu -> (konu, kartlar)"""
    import json, _forum_sekme as FS
    B = json.load(open(os.path.join(KOK, "forum_bbcode", "bbcode.json"), encoding="utf-8"))
    for k in B["konular"]:
        if k["id"] in FS.BIZIM or not k["mesajlar"]: continue
        Bl, R, _ = FY.insa(k, set(k.get("kirik_url") or []))
        yield k, kartla(k, Bl, R)[1]


if __name__ == "__main__":
    import sys, json
    sys.stdout.reconfigure(encoding="utf-8")
    from playwright.sync_api import sync_playwright
    sec = {int(x) for x in sys.argv[1:] if x.isdigit()}
    say, hata = 0, []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=1)
        for k, KL in hepsi():
            if sec and k["id"] not in sec: continue
            os.makedirs(os.path.join(KD, f"d{k['id']:03d}"), exist_ok=True)
            for kt in KL:
                yol = os.path.join(KOK, *kt["dosya"][len("FORUM/"):].split("/"))
                try:
                    pg.set_content(cizim(kt), wait_until="load")
                    tas = pg.evaluate("(()=>{const k=document.querySelector('#kart'),kr=k.getBoundingClientRect().right;let m=0;k.querySelectorAll('*').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().right)});return [kr,m,k.scrollWidth,k.clientWidth]})()")
                    assert tas[1] <= tas[0] + 1 and tas[2] <= tas[3] + 1, ("tasma", tas)
                    pg.locator("#kart").screenshot(path=yol, type="jpeg", quality=88); say += 1
                except Exception as ex:
                    hata.append((k["id"], kt["id"], kt["tur"], str(ex)[:90]))
            print(f"d/{k['id']:<3} {len(KL):>2} kart · " + " ".join(f"{x['id']}:{x['tur']}" for x in KL))
        b.close()
    print(f"\nkart cizildi: {say} · hata {len(hata)}")
    for h in hata: print("   HATA", h)
    sys.exit(1 if hata else 0)

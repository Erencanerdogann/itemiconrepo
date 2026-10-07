# -*- coding: utf-8 -*-
# 24 SAATLIK MADENCILIK SONUCLARI GORSELLERI (patron 7 Eki: "amacin forumda bilgi vermek, kurguyu sen yap").
# Veri: _mining_veri.py (canli rehber oranlari + admin assert + Semih'in 24 saat sonucu). Kart stili + buyuk font: _skill_gorsel.py.
# CIKTI: mining/resim/M00..M04 (*.jpg, 960 px) -> _mining_konu.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, io, base64
from PIL import Image
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _mining_veri as V

RD = os.path.join(V.MD, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
GR, NR, PR = "#ffcf4d", "#9aa7b4", "#7fe3ff"          # Golden altin, Normal gumus, Platinum buz mavisi
ET = "SEXYKO · 24 SAATLİK MADENCİLİK"
e = lambda s: SG.e(s).replace("&#x27;", "’")
_IK = {}


def ik(x, px=40):
    u = x["ikon"]
    if u not in _IK:
        with Image.open(V.ikon_yolu(u)) as im:
            im = im.convert("RGBA"); d = im.crop(im.getchannel("A").getbbox())
            b = io.BytesIO(); d.resize((96, 96), Image.LANCZOS).save(b, "PNG")
        _IK[u] = "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
    return f'<img class="ik" src="{_IK[u]}" style="width:{px}px;height:{px}px" alt="">'


def tr(n): return f"{n:,}".replace(",", ".")
def yuzde(o): return f"%{o:.2f}".replace(".", ",")


ORTAK = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}} .go{{color:{GR};font-weight:900}} .no{{color:{NR};font-weight:900}} .pl{{color:{PR};font-weight:900}}
"""


def m00():
    css = ORTAK + f""".ust{{display:flex;align-items:stretch;gap:14px}} .ust .kut{{flex:1;text-align:center;padding:18px 12px}}
.ust .ad{{font-size:19px;font-weight:900;letter-spacing:1px}} .ust .say{{font-size:58px;font-weight:900;line-height:1.05;margin:6px 0 2px}} .ust .bi{{font-size:15px;color:{G}}}
.kat{{flex:none;width:150px;display:flex;flex-direction:column;align-items:center;justify-content:center}} .kat b{{font-size:52px;color:{VU};font-weight:900;line-height:1}}
.kat span{{font-size:14px;color:{G};text-align:center;margin-top:6px}}
.ilk{{display:flex;gap:14px;margin-top:14px}} .ilk .kut{{flex:1}} .ilk h3{{margin:0 0 10px;font-size:16px;letter-spacing:1px}}
.sat{{display:flex;align-items:center;gap:10px;margin:0 0 8px;font-size:16px}} .sat .ik{{border-radius:5px}} .sat b{{margin-left:auto;font-size:19px}}"""
    ust = (f'<div class="ust"><div class="kut" style="border-color:{GR}"><div class="ad go">⛏️ GOLDEN MATTOCK</div><div class="say go">{tr(V.TOPLAM_G)}</div><div class="bi">item · 24 saat · {len(V.G24)} çeşit</div></div>'
           f'<div class="kat"><b>×{V.KAT:.2f}</b><span>Golden, Normal\'in<br>{V.KAT:.2f} katı item</span></div>'.replace(f"×{V.KAT:.2f}", "×" + f"{V.KAT:.2f}".replace(".", ",")).replace(f"<br>{V.KAT:.2f} katı", "<br>" + f"{V.KAT:.2f}".replace(".", ",") + " katı")
           + f'<div class="kut" style="border-color:{NR}"><div class="ad no">⛏️ NORMAL MATTOCK</div><div class="say no">{tr(V.TOPLAM_N)}</div><div class="bi">item · 24 saat · {len(V.N24)} çeşit</div></div></div>')
    ilk = ('<div class="ilk">' + "".join(f'<div class="kut"><h3 class="{c}">EN ÇOK ÇIKAN 3 — {t}</h3>'
           + "".join(f'<div class="sat">{ik(x, 34)}<span>{e(x["ad"])}</span><b class="{c}">{x["adet"]}</b></div>' for x in L[:3]) + "</div>"
           for c, t, L in (("go", "GOLDEN", V.G24), ("no", "NORMAL", V.N24))) + "</div>")
    nt = f'<div class="not">💎 Sadece <b>Golden</b>\'da çıkanlar: <b>{" · ".join(e(x["ad"]) for x in V.SADECE_G)}</b> ({" + ".join(str(x["adet"]) for x in V.SADECE_G)} adet)</div>'
    return SG.kart(ust + ilk + nt, "⛏️ 24 SAATLİK MADENCİLİK SONUÇLARI", "Golden Mattock ile Normal Mattock — aynı süre, gerçek envanter", ET, css)


def liste(L, renk, baslik, alt):
    css = ORTAK + f""".g{{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px}}
.s{{display:flex;align-items:center;gap:10px;background:#1d1712;border:1px solid #3a2e20;border-left:4px solid {renk};border-radius:8px;padding:6px 12px}}
.s .ad{{font-size:16px;font-weight:700;color:#e8dcc8;flex:1}} .s .or{{font-size:13px;color:{G};margin-right:8px}} .s .ad_{{font-size:22px;font-weight:900;color:{renk};min-width:46px;text-align:right}}
.ozet{{display:flex;justify-content:center;gap:26px;margin-top:12px;font-size:16px;color:{G}}} .ozet b{{color:{renk};font-size:20px}}"""
    g = '<div class="g">' + "".join(f'<div class="s">{ik(x, 38)}<span class="ad">{e(x["ad"])}</span><span class="or">{yuzde(x["oran"])}</span><span class="ad_">{x["adet"]}</span></div>' for x in L) + "</div>"
    oz = f'<div class="ozet"><span>Toplam <b>{tr(sum(x["adet"] for x in L))}</b> item</span><span><b>{len(L)}</b> çeşit</span><span>Oran = rehberdeki çıkma oranı</span></div>'
    return SG.kart(g + oz, baslik, alt, ET, css)


def m01(): return liste(V.G24, GR, "⛏️ GOLDEN MATTOCK — 24 SAAT", "Envanterdeki her item: <b>adet</b> (çoktan aza) · rehberdeki çıkma oranı")
def m02(): return liste(V.N24, NR, "⛏️ NORMAL MATTOCK — 24 SAAT", "Envanterdeki her item: <b>adet</b> (çoktan aza) · rehberdeki çıkma oranı")


def m03():
    css = ORTAK + f""".r{{display:flex;align-items:center;gap:10px;margin:0 0 7px}} .r .ad{{width:210px;font-size:15px;font-weight:700;color:#e8dcc8;display:flex;align-items:center;gap:8px}}
.bars{{flex:1}} .bar{{display:flex;align-items:center;gap:8px;height:15px;margin:2px 0}} .bar i{{display:block;height:13px;border-radius:7px}}
.bar span{{font-size:13px;font-weight:900}} .lg{{display:flex;justify-content:center;gap:24px;margin:0 0 12px;font-size:15px}} .lg i{{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:middle;margin-right:6px}}"""
    n = {x["id"]: x for x in V.N24}; mx = max(x["adet"] for x in V.G24)
    sat = "".join(f'<div class="r"><div class="ad">{ik(x, 28)}{e(x["ad"])}</div><div class="bars">'
                  f'<div class="bar"><i style="width:{x["adet"] / mx * 560:.0f}px;background:{GR}"></i><span class="go">{x["adet"]}</span></div>'
                  + (f'<div class="bar"><i style="width:{n[x["id"]]["adet"] / mx * 560:.0f}px;background:{NR}"></i><span class="no">{n[x["id"]]["adet"]}</span></div>' if x["id"] in n
                     else '<div class="bar"><span style="color:#8a7a62;font-weight:700">Normal\'de çıkmaz</span></div>') + "</div></div>" for x in V.G24)
    lg = f'<div class="lg"><span><i style="background:{GR}"></i><b class="go">Golden</b></span><span><i style="background:{NR}"></i><b class="no">Normal</b></span></div>'
    return SG.kart(lg + sat, "📊 ITEM ITEM KARŞILAŞTIRMA", "Aynı item, iki kazma — 24 saatte kaç adet", ET, css)


def m04():
    css = ORTAK + f""".tb{{width:100%;border-collapse:separate;border-spacing:0 5px}} .tb th{{font-size:14px;letter-spacing:1px;padding:4px 8px}}
.tb td{{background:#1d1712;border-top:1px solid #3a2e20;border-bottom:1px solid #3a2e20;padding:5px 10px;font-size:15px;text-align:center}}
.tb td:first-child{{text-align:left;border-left:1px solid #3a2e20;border-radius:6px 0 0 6px}} .tb td:last-child{{border-right:1px solid #3a2e20;border-radius:0 6px 6px 0}}
.tb td:first-child span{{display:inline-flex;align-items:center;gap:8px;font-weight:700;color:#e8dcc8}} .yok{{color:#5c4f3e}}"""
    pool = {}
    for k, L in (("n", V.NORMAL), ("g", V.GOLDEN), ("p", V.PLATIN)):
        for x in L: pool.setdefault(x["ad"], {"x": x})[k] = x["oran"]
    sira = sorted(pool.values(), key=lambda r: (r["x"]["ad"] != "EXP", -(r.get("g") or 0), -(r.get("p") or 0), r["x"]["ad"]))
    hc = lambda v, c: f'<span class="{c}">{yuzde(v)}</span>' if v is not None else '<span class="yok">—</span>'
    sat = "".join(f'<tr><td><span>{"⭐" if r["x"]["ad"] == "EXP" else ik(r["x"], 26)}{e(r["x"]["ad"])}</span></td><td>{hc(r.get("n"), "no")}</td><td>{hc(r.get("g"), "go")}</td><td>{hc(r.get("p"), "pl")}</td></tr>' for r in sira)
    tb = f'<table class="tb"><tr><th style="text-align:left;color:{G}">ITEM</th><th class="no">NORMAL MATTOCK</th><th class="go">GOLDEN MATTOCK</th><th class="pl">PLATINUM AUTO MINING</th></tr>{sat}</table>'
    nt = f'<div class="not">📘 Kaynak: oyun içi rehber <b>sexyko.com/guide/mining-fishing</b> ({e(V.CEKIM)}) · oranlar admin kayıtlarıyla aynı · madencilik alanı <b>{V.ZONE}</b></div>'
    return SG.kart(tb + nt, "📘 RESMÎ ÇIKMA ORANLARI", "Kazma türüne göre her item'ın çıkma oranı", ET, css)


KARTLAR = [("M00_ozet.jpg", m00), ("M01_golden.jpg", m01), ("M02_normal.jpg", m02), ("M03_karsilastirma.jpg", m03), ("M04_oranlar.jpg", m04)]

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=1)
        for ad, f in KARTLAR:
            pg.set_content(f(), wait_until="load")
            tas = pg.evaluate("(()=>{const k=document.querySelector('#kart'),kr=k.getBoundingClientRect().right;let m=0;k.querySelectorAll('*').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().right)});return [kr,m,k.scrollWidth,k.clientWidth]})()")
            assert tas[1] <= tas[0] + 1 and tas[2] <= tas[3] + 1, (ad, "yazi kartin disina tasiyor", tas)
            pg.locator("#kart").screenshot(path=os.path.join(RD, ad), type="jpeg", quality=90)
            print(ad, os.path.getsize(os.path.join(RD, ad)) // 1024, "KB")
        b.close()

# -*- coding: utf-8 -*-
# PUS INDIRIM KODU GORSELLERI (patron 8 Eki: "resimli vs ayni janradan devam"). Veri: _pus_veri.py (forum.sexyko.com/d/51'e assert'li).
# Kart stili: _skill_gorsel.py. Gonderinin KENDI ekran goruntuleri (pus_1..3.png) — U01'de Coupon / Check / sonuc satiri numarali cerceveli.
# CIKTI: pus_kupon/resim/U00..U05 (*.jpg, 960 px) -> _pus_konu.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, io, base64
from PIL import Image
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _pus_veri as V

RD = os.path.join(V.PD, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
YS, KR, SB = "#3ecf8e", "#ff6b6b", "#4fd1ff"        # indirim yesil, yasak kirmizi, SB mavi
ET = "SEXYKO · PUS İNDİRİM KODU"
e = lambda s: SG.e(s).replace("&#x27;", "’")


def ss(n, gen):
    with Image.open(V.RESIM[n]) as im:
        b = io.BytesIO(); im.convert("RGB").save(b, "PNG")
    return f'<img class="ss" src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}" style="width:{gen}px" alt="">'


ORTAK = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}} .ys{{color:{YS};font-weight:900}} .kr{{color:{KR};font-weight:900}} .kod{{font-family:Consolas,monospace;color:{SB};font-weight:700}}
.ss{{display:block;border-radius:8px;border:2px solid #6b5426;box-shadow:0 6px 20px rgba(0,0,0,.45)}}
.ik2{{display:flex;gap:18px;align-items:flex-start}} .ik2 .sag{{flex:1;min-width:0}}
.ad1{{display:flex;gap:12px;align-items:flex-start;margin:0 0 12px}} .ad1 .no{{flex:none;width:34px;height:34px;border-radius:50%;background:{A};color:#1b1400;font-weight:900;font-size:18px;display:flex;align-items:center;justify-content:center}}
.ad1 .t{{font-size:16px;line-height:1.5;color:#e8dcc8}} .ad1 .t b{{color:{A2}}}
.sat{{display:flex;justify-content:space-between;gap:10px;font-size:16px;padding:7px 0;border-bottom:1px solid #3a2e20}} .sat span:first-child{{color:#a89f91}}
"""


def u00():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}} .g .kut{{text-align:center;padding:16px 10px}}
.g .ic{{font-size:40px;line-height:1}} .g .b{{font-size:16px;font-weight:900;color:{A2};letter-spacing:1px;margin:10px 0 6px}} .g .d{{font-size:15px;line-height:1.45}}
.uy{{margin-top:14px;display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:10px;background:#2a1414;border:1px solid #7a2e2e;font-size:16px;color:#f0d6d6}}
.uy b{{color:{KR}}}"""
    k = [("🛒", "TEKLİ ÜRÜN", "uygun tekli PUS ürünlerinde<br>indirim doğrudan uygulanır"), ("🛍️", "BASKET / SEPET", "sepetteki uygun ürünlere<br>toplam yeniden hesaplanır"),
         ("🎥", "SPONSOR YAYINCI", "yayıncının kodunu kullan<br>indirim kazan · destek ol"), ("🔥", "%30'A VARAN", "etkinlik ve kampanya<br>dönemlerinde")]
    g = '<div class="g">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="b">{b}</div><div class="d">{d}</div></div>' for i, b, d in k) + "</div>"
    uy = '<div class="uy">⚠️ Kupon <b>VIP Paketlerde</b> ve <b>Farm Paketlerde</b> kullanılamaz — paketler zaten indirimli.</div>'
    return SG.kart(g + uy, "🎟️ PUS İNDİRİM KODU SİSTEMİ", "Power Up Store'da kuponla indirim — SexyKO &amp; StoneSoft altyapısına özel", ET, css)


def u01():
    k = 900 / 1155
    kutu = [("1", 926, 397, 1032, 427), ("2", 1033, 397, 1093, 427), ("3", 903, 429, 1082, 449)]
    ust = "".join(f'<div class="cr" style="left:{x0*k:.0f}px;top:{y0*k:.0f}px;width:{(x1-x0)*k:.0f}px;height:{(y1-y0)*k:.0f}px"></div>'
                  + (f'<div class="rz" style="left:{(x0 + x1) / 2 * k - 13:.0f}px;top:{y0*k - 30:.0f}px">{n}</div>' if n != "3"        # 1-2: kutunun USTUNE (yaziyi ortmesin)
                     else f'<div class="rz" style="left:{x0*k - 30:.0f}px;top:{y0*k - 4:.0f}px">{n}</div>') for n, x0, y0, x1, y1 in kutu)
    css = ORTAK + f""".rel{{position:relative;width:900px;margin:0 auto}} .cr{{position:absolute;border:3px solid #ff4d4d;border-radius:5px;box-shadow:0 0 0 2px rgba(0,0,0,.6)}}
.rz{{position:absolute;width:26px;height:26px;border-radius:50%;background:#ff4d4d;color:#fff;font-weight:900;font-size:15px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 2px #1b1400}}
.lg{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}} .lg .kut{{display:flex;gap:10px;align-items:flex-start}}
.lg .n{{flex:none;width:28px;height:28px;border-radius:50%;background:#ff4d4d;color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}} .lg .t{{font-size:15px;line-height:1.45}} .lg .t b{{color:{A2}}}"""
    lg = ('<div class="lg"><div class="kut"><div class="n">1</div><div class="t"><b>Kupon</b> alanına indirim kodunu yaz<br><span style="color:#a89f91">resimdeki örnek: <span class="kod">Sexyko10</span></span></div></div>'
          '<div class="kut"><div class="n">2</div><div class="t"><b>CHECK</b> butonuna tıkla</div></div>'
          '<div class="kut"><div class="n">3</div><div class="t">Kod geçerliyse indirim <b class="ys">otomatik</b> aktif<br><span style="color:#a89f91">örnek: Coupon -10%</span></div></div></div>')
    return SG.kart(f'<div class="rel">{ss(1, 900)}{ust}</div>' + lg, "🛒 İNDİRİM KODU NASIL KULLANILIR?", "Power Up Store'un alt bölümündeki <b>Kupon</b> alanı → <b>CHECK</b>", ET, css)


def u02():
    sag = (f'<div class="sag"><div class="kut"><div class="sat"><span>Ürün</span><b>{V.ORNEK_TEKLI[0]}</b></div>'
           f'<div class="sat"><span>Toplam fiyat</span><b><s style="color:#8a7a62">{V.ORNEK_TEKLI[1]}</s> <span class="ys">{V.ORNEK_TEKLI[2]}</span></b></div>'
           f'<div class="sat"><span>İndirim</span><b class="ys">{V.ORNEK_TEKLI[3]}</b></div><div class="sat" style="border:0"><span>Kupon</span><b class="kod">{V.ORNEK_KOD}</b></div></div>'
           '<div class="not">Ürünü satın alırken onay penceresindeki <b>Coupon</b> alanına kodu yaz → <b>Check</b> → <b>Confirm</b>. İndirim doğrudan alışverişe uygulanır.</div>'
           '<div style="font-size:13px;color:#a89f91;margin-top:8px">Rakamlar resimdeki örnek.</div></div>')
    return SG.kart(f'<div class="ik2">{ss(2, 470)}{sag}</div>', "🎁 TEKLİ ITEM ALIMLARINDA KUPON", "Tek bir ürün alırken bile Sponsor Yayıncı indirim kodundan yararlan", ET, ORTAK)


def u03():
    sag = ('<div class="sag"><div class="ad1"><div class="no">1</div><div class="t">Birden fazla ürünü <b>Basket</b>’e ekle</div></div>'
           '<div class="ad1"><div class="no">2</div><div class="t"><b>Coupon</b> alanına kodu yaz → <b>Check</b></div></div>'
           '<div class="ad1"><div class="no">3</div><div class="t">Sepetteki <b>uygun</b> her ürüne indirim uygulanır <span class="ys">(-10%)</span></div></div>'
           '<div class="ad1"><div class="no">4</div><div class="t">Toplam tutar <b>yeniden hesaplanır</b><br><span style="color:#a89f91">örnek: SB <s>2,675</s> <span class="ys">2,408</span> · KC <s>6,120</s> <span class="ys">5,508</span></span></div></div>'
           '<div class="not">Toplu PUS alışverişlerinde de kupon avantajı.</div></div>')
    return SG.kart(f'<div class="ik2">{ss(3, 300)}{sag}</div>', "🛍️ BASKET / SEPET ALIŞVERİŞLERİNDE KUPON", "Sepetteki uygun ürünlere indirim — toplam buna göre yeniden hesaplanır", ET, ORTAK)


def u04():
    css = ORTAK + f""".iki{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .iki .kut{{padding:16px}} .iki h3{{margin:0 0 12px;font-size:18px;letter-spacing:1px}}
.yk{{display:flex;gap:10px;margin-bottom:12px}} .yk div{{flex:1;text-align:center;padding:12px 6px;border-radius:10px;background:#2a1414;border:1px solid #7a2e2e;font-weight:900;font-size:18px;color:#f0d6d6}}
.yk div span{{display:block;font-size:30px}} .ak{{display:flex;flex-direction:column;gap:8px}}
.ak .s{{padding:10px 12px;border-radius:8px;background:linear-gradient(180deg,#2a2018,#1b1511);border:1px solid #6b5426;font-size:16px;font-weight:700;color:#e8dcc8;text-align:center}}
.ak .o{{text-align:center;color:{A};font-size:20px;line-height:1}}"""
    sol = ('<div class="kut" style="border-color:#7a2e2e"><h3 class="kr">⚠️ VIP VE FARM PAKETLERİ</h3><div class="yk"><div><span>👑</span>VIP ✗</div><div><span>🌾</span>FARM ✗</div></div>'
           '<div style="font-size:15px;line-height:1.5">Bu paketler birden fazla ürünün birleşimi ve <b style="color:#ffd27a">zaten indirimli</b> satılıyor →<br><b class="kr">ikinci bir kupon indirimi uygulanmaz.</b></div></div>')
    sag = ('<div class="kut"><h3 style="color:#ffd27a">🎥 SPONSOR YAYINCI KODLARI</h3><div class="ak">'
           + '<div class="o">⬇</div>'.join(f'<div class="s">{e(x)}</div>' for x in V.SPONSOR_AKIS)
           + '</div><div style="font-size:14px;color:#a89f91;margin-top:10px;text-align:center">Oyuncu avantaj kazanır · yayıncı topluluğu desteklenir</div></div>')
    return SG.kart(f'<div class="iki">{sol}{sag}</div>', "⚠️ İSTİSNA &amp; 🎥 SPONSOR KODLARI", "Kupon nerede geçmez — ve kodun kime destek olur", ET, css)


def u05():
    css = ORTAK + f""".ak{{display:flex;align-items:stretch;gap:8px}} .ak .s{{flex:1;padding:14px 8px;border-radius:10px;background:linear-gradient(180deg,#2a2018,#1b1511);border:1px solid #6b5426;text-align:center;font-size:16px;font-weight:800;color:#e8dcc8;display:flex;align-items:center;justify-content:center}}
.ak .s.ck{{background:#2c3a1a;border-color:{YS};color:{YS};font-size:20px;letter-spacing:2px}} .ak .s.son{{background:linear-gradient(180deg,#3a2c14,#241a0e);border:2px solid {A};color:#ffd27a}}
.ak .o{{flex:none;display:flex;align-items:center;color:{A};font-size:22px}}
.yuz{{margin-top:14px;display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;padding:14px 18px;border-radius:12px;background:linear-gradient(90deg,#3a1d0c,#1d1712);border:1px solid #8a4a1a}}
.yuz .b{{font-size:44px;font-weight:900;color:#ff9f43;line-height:1}} .yuz .t{{font-size:16px;line-height:1.5;color:#e8dcc8}} .yuz .t b{{color:#ffd27a}}"""
    adim = V.KISACA
    ak = '<div class="ak">' + '<div class="o">➜</div>'.join(
        f'<div class="s{" ck" if x == "CHECK" else " son" if i == len(adim) - 1 else ""}">{"🎟️ " if i == len(adim) - 1 else ""}{e(x)}</div>' for i, x in enumerate(adim)) + "</div>"
    yuz = ('<div class="yuz"><div class="b">%30</div><div class="t"><b>Etkinlik dönemlerinde</b> Sponsor Yayıncı kuponlarında %30’a varan indirimler aktif edilebilir — kodlar sürekli aktif olmayabilir.<br>'
           'Takip et: <b>Sponsor Yayıncılar</b> · <b>SexyKO Discord</b> · <b>Resmi duyurular</b></div></div>')
    return SG.kart(ak + yuz, "✅ KISACASI", e(V.SLOGAN), ET, css)


KARTLAR = [("U00_ozet.jpg", u00), ("U01_nasil.jpg", u01), ("U02_tekli.jpg", u02), ("U03_sepet.jpg", u03), ("U04_istisna_sponsor.jpg", u04), ("U05_kisaca.jpg", u05)]

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

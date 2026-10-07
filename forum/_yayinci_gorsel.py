# -*- coding: utf-8 -*-
# YAYINCI SISTEMI GORSELLERI (patron 8 Eki: "resimli vs ayni janradan devam"). Veri: _yayinci_veri.py (forum.sexyko.com/d/37'ye assert'li).
# Kart stili: _skill_gorsel.py. Gonderinin KENDI ekran goruntuleri (yy_2..4.png) — onemli yerler numarali cerceveli.
# CIKTI: yayinci/resim/V00..V05 (*.jpg, 960 px) -> _yayinci_konu.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, io, base64
from PIL import Image
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _yayinci_veri as V

RD = os.path.join(V.YD, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
CN = "#ff4d4d"                                     # canli / isaret kirmizisi
ET = "SEXYKO · YAYINCI SİSTEMİ"
e = lambda s: SG.e(s).replace("&#x27;", "’")


def ss(n, gen):
    with Image.open(V.RESIM[n]) as im:
        b = io.BytesIO(); im.convert("RGB").save(b, "PNG")
    return f'<img class="ss" src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}" style="width:{gen}px" alt="">'


def isaret(n, gen, kutular):
    """Ekran goruntusu + numarali kirmizi cerceveler. kutular: [(no, x0, y0, x1, y1)] ORIJINAL piksel."""
    with Image.open(V.RESIM[n]) as im: k = gen / im.width
    ust = "".join(f'<div class="cr" style="left:{x0*k:.0f}px;top:{y0*k:.0f}px;width:{(x1-x0)*k:.0f}px;height:{(y1-y0)*k:.0f}px"></div>'
                  f'<div class="rz" style="left:{max(0, x0*k - 12):.0f}px;top:{max(0, y0*k - 12):.0f}px">{no}</div>' for no, x0, y0, x1, y1 in kutular)
    return f'<div class="rel" style="width:{gen}px">{ss(n, gen)}{ust}</div>'


ORTAK = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}} .cn{{color:{CN};font-weight:900}}
.ss{{display:block;border-radius:8px;border:2px solid #6b5426;box-shadow:0 6px 20px rgba(0,0,0,.45)}}
.rel{{position:relative;margin:0 auto}} .cr{{position:absolute;border:3px solid {CN};border-radius:6px;box-shadow:0 0 0 2px rgba(0,0,0,.55)}}
.rz{{position:absolute;width:26px;height:26px;border-radius:50%;background:{CN};color:#fff;font-weight:900;font-size:15px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 2px #1b1400}}
.lg{{display:grid;gap:12px;margin-top:14px}} .lg .kut{{display:flex;gap:10px;align-items:flex-start;padding:12px 14px}}
.lg .n{{flex:none;width:28px;height:28px;border-radius:50%;background:{CN};color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}}
.lg .t{{font-size:15px;line-height:1.45}} .lg .t b{{color:{A2}}}
"""
lg = lambda sutun, L: f'<div class="lg" style="grid-template-columns:repeat({sutun},1fr)">' + "".join(f'<div class="kut"><div class="n">{n}</div><div class="t">{t}</div></div>' for n, t in L) + "</div>"


def v00():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}} .g .kut{{text-align:center;padding:16px 10px}}
.g .ic{{font-size:40px;line-height:1}} .g .b{{font-size:16px;font-weight:900;color:{A2};letter-spacing:1px;margin:10px 0 6px}} .g .d{{font-size:15px;line-height:1.45}}
.yol{{margin-top:14px;text-align:center;font-size:17px;font-weight:700;color:#e8dcc8}} .yol b{{color:{A2}}}"""
    k = [("🔴", "CANLI TAKİP", "hangi yayıncı şu an<br>yayında, tek ekranda"), ("🎥", "SPONSOR YAYINCILAR", "kanal · platform<br>güncel yayın durumu"),
         ("❤️", "DESTEK OL", "takip et · yayına katıl<br>yayıncıya destek ol"), ("🎙️", "BAŞVUR", "kuralları oku<br>formu doldur · gönder")]
    g = '<div class="g">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="b">{b}</div><div class="d">{d}</div></div>' for i, b, d in k) + "</div>"
    yol = '<div class="not yol">Tüm işlemler tek panelden: <b>www.sexyko.com</b> → <b>YAYINCILAR</b></div>'
    return SG.kart(g + yol, "🎥 SEXYKO YAYINCI SİSTEMİ", "Yayıncıları takip et · canlı yayınları keşfet · destek ol · kendi başvurunu yap", ET, css)


def v01():
    img = isaret(2, 900, [("1", 990, 3, 1137, 47), ("2", 469, 510, 619, 659)])
    L = [("1", "Üst menüde <b>YAYINCILAR</b>"), ("2", "ya da ana sayfadaki <b>YAYINCILAR</b> kısayolu")]
    return SG.kart(img + lg(2, L), "📍 01 — YAYINCILAR BÖLÜMÜNE GİRİŞ", "Hesabına giriş yap → panelden <b>Yayıncılar</b> bölümüne gir", ET, ORTAK)


def v02():
    img = isaret(3, 900, [("1", 70, 95, 366, 262), ("2", 998, 143, 1622, 218), ("3", 390, 345, 694, 610), ("4", 413, 209, 632, 255)])
    L = [("1", "<b class='cn'>Şu an yayında</b> / offline listesi"), ("2", "Sayaçlar: yayında kanal · toplam izleyici · anlaşmalı yayıncı · platform"),
         ("3", "<b>Sponsor Yayıncılar</b> kartı: durum · kanal · platform"), ("4", "<b>Yayıncı Başvurusu Yap</b> → 03. adım")]
    return SG.kart(img + lg(2, L), "🔴 02 — YAYINDA OLANLARI TAKİP ET", "Yayıncılar sayfası: kim yayında, sponsor mu, hangi kanal — tek ekranda", ET, ORTAK)


def v03():
    img = isaret(4, 900, [("1", 132, 225, 732, 568), ("2", 776, 90, 1272, 862), ("3", 143, 578, 725, 618)])
    L = [("1", "<b>Form</b>: " + " · ".join(V.EKRAN_FORM) + f"<br><span style='color:#a89f91'>Kanal: {e(V.EKRAN_KANAL)}</span>"),
         ("2", "Sağda <b>Başvuru Şartları</b> (10 madde) — gönderen kabul etmiş sayılır"), ("3", "<b>Başvuruyu Gönder</b> → yönetim ekibi inceler")]
    return SG.kart(img + lg(3, L), "🎙️ 03 · 04 — BAŞVURU + KURALLAR", "Yayıncı Başvurusu Yap → kuralları oku → formu eksiksiz doldur", ET, ORTAK)


def v04():
    css = ORTAK + f""".ad{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}} .ad .kut{{text-align:center;padding:16px 10px;position:relative}}
.ad .no{{width:40px;height:40px;margin:0 auto 8px;border-radius:50%;background:{A};color:#1b1400;font-weight:900;font-size:20px;display:flex;align-items:center;justify-content:center}}
.ad .t{{font-size:16px;line-height:1.45;font-weight:700;color:#e8dcc8}} .ad .son{{border:2px solid {A};background:linear-gradient(180deg,#3a2c14,#1d1712)}}"""
    ad = '<div class="ad">' + "".join(f'<div class="kut{" son" if i == 6 else ""}"><div class="no">{i + 1}</div><div class="t">{e(x)}</div></div>' for i, x in enumerate(V.NASIL)) + \
         '<div class="kut" style="display:flex;align-items:center;justify-content:center"><div style="font-size:15px;line-height:1.5;color:#a89f91">Yönetim ekibi inceler →<br>uygun bulunursa<br><b style="color:#ffd27a">yayıncı sistemine dahil</b></div></div></div>'
    return SG.kart(ad, "✅ BAŞVURU NASIL YAPILIR?", "7 adımda yayıncı başvurusu", ET, css)


def v05():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}} .g .kut{{text-align:center;padding:14px 8px}}
.g .ic{{font-size:32px;line-height:1}} .g .b{{font-size:14px;font-weight:900;color:{A2};margin:8px 0 6px;line-height:1.3}} .g .d{{font-size:15px;font-weight:800;color:#e8dcc8;line-height:1.35}}
.g .z{{border-color:#7a2e2e;background:#2a1414}} .g .z .d{{color:#ff8a8a}}"""
    g = '<div class="g">' + "".join(f'<div class="kut{" z" if "ZORUNLU" in b else ""}"><div class="ic">{i}</div><div class="b">{e(b)}</div><div class="d">{e(k)}</div></div>' for i, b, m, k in V.SART) + "</div>"
    return SG.kart(g, "🎙️ SPONSOR YAYINCI BAŞVURU ŞARTLARI", "Kanal kalitesi · izleyici kitlesi · yayın geçmişi · aktiflik — sınırlı kontenjan", ET, css)


KARTLAR = [("V00_ozet.jpg", v00), ("V01_giris.jpg", v01), ("V02_takip.jpg", v02), ("V03_basvuru.jpg", v03), ("V04_adimlar.jpg", v04), ("V05_sartlar.jpg", v05)]

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

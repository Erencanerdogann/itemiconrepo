# -*- coding: utf-8 -*-
# GENIE SISTEMI GORSELLERI (patron 8 Eki: "genie sistemi go" — d/16'nin 4 resmi de 404). Veri: _genie_veri.py (forum.sexyko.com/d/16'ya assert'li).
# Kart stili: _skill_gorsel.py. Ekran goruntuleri OYUNUN KENDI Genie penceresi (3 Eki, genie/kaynak_resim/) — onemli yerler numarali cerceveli.
# CIKTI: genie/resim/G00..G07 (*.jpg, 960 px) -> _genie_konu.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, io, base64
from PIL import Image
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _genie_veri as V

RD = os.path.join(V.GD, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
CN = "#ff4d4d"                                     # isaret kirmizisi
ET = "SEXYKO · GENIE SİSTEMİ"
e = lambda s: SG.e(s).replace("&#x27;", "’")


def _ac(ad, kirp):
    im = Image.open(V.RESIM[ad]).convert("RGB")
    return im.crop(kirp) if kirp else im


def ss(ad, gen, kirp=None):
    im = _ac(ad, kirp); b = io.BytesIO(); im.save(b, "PNG")
    return f'<img class="ss" src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}" style="width:{gen}px" alt="">'


def isaret(ad, gen, kutular, kirp=None):
    """Ekran goruntusu (+ istege bagli kirpim) + numarali kirmizi cerceveler. kutular: [(no, x0, y0, x1, y1)] ORIJINAL piksel."""
    ox, oy = (kirp[0], kirp[1]) if kirp else (0, 0)
    k = gen / _ac(ad, kirp).width
    ust = "".join(f'<div class="cr" style="left:{(x0-ox)*k:.0f}px;top:{(y0-oy)*k:.0f}px;width:{(x1-x0)*k:.0f}px;height:{(y1-y0)*k:.0f}px"></div>'
                  + (f'<div class="rz" style="left:{max(0, (x0-ox)*k - 12):.0f}px;top:{max(0, (y0-oy)*k - 12):.0f}px">{no}</div>' if no else "")
                  for no, x0, y0, x1, y1 in kutular)
    return f'<div class="rel" style="width:{gen}px">{ss(ad, gen, kirp)}{ust}</div>'


ORTAK = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}} .cn{{color:{CN};font-weight:900}} .en{{color:#a89f91}}
.ss{{display:block;border-radius:8px;border:2px solid #6b5426;box-shadow:0 6px 20px rgba(0,0,0,.45)}}
.rel{{position:relative;margin:0 auto}} .cr{{position:absolute;border:3px solid {CN};border-radius:6px;box-shadow:0 0 0 2px rgba(0,0,0,.55)}}
.rz{{position:absolute;width:26px;height:26px;border-radius:50%;background:{CN};color:#fff;font-weight:900;font-size:15px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 2px #1b1400}}
.lg{{display:grid;gap:12px;margin-top:14px}} .lg .kut{{display:flex;gap:10px;align-items:flex-start;padding:12px 14px}}
.lg .n{{flex:none;width:28px;height:28px;border-radius:50%;background:{CN};color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}}
.lg .t{{font-size:15px;line-height:1.45}} .lg .t b{{color:{A2}}}
.yan{{display:flex;gap:18px;align-items:flex-start;justify-content:center}} .yan .lg{{margin-top:0;flex:1}}
"""
lg = lambda sutun, L: f'<div class="lg" style="grid-template-columns:repeat({sutun},1fr)">' + "".join(f'<div class="kut"><div class="n">{n}</div><div class="t">{t}</div></div>' for n, t in L) + "</div>"


def g00():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}} .g .kut{{text-align:center;padding:16px 8px}}
.g .ic{{font-size:36px;line-height:1}} .g .b{{font-size:15px;font-weight:900;color:{A2};letter-spacing:.5px;margin:10px 0 6px}} .g .d{{font-size:15px;line-height:1.45}}"""
    k = [("▶️", "TEK TUŞ", "Başlat · Durdur<br>kalan süre üst panelde"), ("⚔️", "8 + 8 + 8 SKILL", "Attack · Self · Party<br>slotlarına diz"),
         ("🧪", "HP / MP POT", "hangi yüzdede<br>basacağını sen seç"), ("🎯", "MOB SEÇ", "sadece listedeki<br>moblara saldırır"), ("📏", "ATTACK RANGE", "farm alanını<br>sen belirle")]
    g = '<div class="g">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="b">{b}</div><div class="d">{d}</div></div>' for i, b, d in k) + "</div>"
    n = '<div class="not">🔒 <b>Genie aktifken normal skill barın kilitlenir</b> — karakter sadece Genie’ye dizdiğin skill ve ayarları kullanır. Durdurunca manuel kullanım geri gelir.</div>'
    return SG.kart(g + n, "⚙️ SEXYKO GENIE SİSTEMİ", e(V.UST), ET, css)


def g01():
    sol = isaret("panel", 300, [("", 82, 0, 280, 61)])
    sag = isaret("panel", 560, [("1", 181, 7, 211, 38), ("2", 212, 7, 243, 38), ("4", 244, 7, 276, 38), ("3", 104, 40, 280, 60)], kirp=(80, 0, 280, 62))
    L = [("1", "<b>▶ BAŞLAT</b> — Genie çalışmaya başlar"), ("2", "<b>■ DURDUR</b> — Genie durur, kontrol sende"),
         ("3", "<b>Kalan Genie süresi</b> — çubukta (örnek: 234d 1h)"), ("4", "<b>⬇ AYARLAR</b> — Genie penceresini açar")]
    return SG.kart(f'<div class="yan">{sol}{sag}</div>' + lg(4, L), "▶️ GENIE HIZLI KONTROL PANELİ", "Oyun ekranının sağ üstü — Genie’ye tek tıkla müdahale", ET, ORTAK)


def g02():
    img = isaret("main", 900, [("1", 488, 107, 1179, 213), ("2", 488, 225, 1179, 331), ("3", 488, 342, 1179, 448), ("4", 50, 277, 469, 488),
                               ("5", 488, 460, 1179, 731), ("6", 50, 502, 469, 676), ("7", 47, 744, 437, 783), ("8", 959, 744, 1179, 783)])
    L = [("1", "<b>Attack Skills</b> — 8 slot"), ("2", "<b>Buff / Self Skills</b> — 8 slot"), ("3", "<b>Party Skills</b> — 8 slot"), ("4", "<b>HP / MP pot</b> yüzdesi"),
         ("5", "<b>Saldırılacak mob</b> listesi"), ("6", "<b>Party / Self heal</b> eşiği · <b>Attack range</b>"), ("7", "<b>Start / Stop</b>"), ("8", "<b>Save Settings</b> — kaydet")]
    n = ('<div class="not">Her satırda <b>Enabled</b> (aç / kapa) ve <b>Clear Row</b> (satırı boşalt) var · skill’i <b>skill penceresinden slota sürükle</b> · '
         'slota <b>sağ tık</b> = boşalt · ikonu <b>pencerenin dışına sürükle</b> = kaldır</div>')
    return SG.kart(img + lg(4, L) + n, "⚔️ GENIE ANA AYARLARI", "Genie penceresi — Main sekmesi", ET, ORTAK)


def g03():
    img = isaret("main", 470, [("1", 58, 312, 462, 391), ("2", 58, 397, 462, 476)], kirp=(50, 277, 469, 488))
    L = [("1", "<b>Use HP Pot</b> ✔ → <b>When HP is … % or below</b><br>can bu yüzdeye inince Genie <b>HP pot</b> basar"),
         ("2", "<b>Use MP Pot</b> ✔ → <b>When MP is … % or below</b><br>mana bu yüzdeye inince Genie <b>MP pot</b> basar")]
    ornek = f'<div class="not" style="text-align:center;font-size:17px">Örnek: <b>HP %60</b> · <b>MP %40</b><br><span class="en" style="font-size:15px">oranı farm bölgesinin zorluğuna göre değiştir</span></div>'
    return SG.kart(f'<div class="yan">{img}<div style="flex:1">{lg(1, L)}{ornek}</div></div>', "❤️ HP / 💙 MP POT AYARLARI", "Smart Auto Use — yüzdeyi sen belirle", ET, ORTAK)


def g04():
    img = isaret("main", 900, [("1", 753, 500, 884, 537), ("2", 503, 548, 1164, 716), ("3", 893, 500, 1024, 537), ("4", 1033, 500, 1165, 537)], kirp=(488, 460, 1179, 731))
    L = [("1", "<b>Add Target</b> = Mob Ekle"), ("2", "Kayıtlı mob isimleri<br><span class='en'>örnek: Satiros Lv 69</span>"), ("3", "<b>Remove</b> = Mob Sil"),
         ("4", "<b>Clear All</b> = listeyi temizle")]
    return SG.kart(img + lg(4, L), "🎯 SALDIRILACAK MOBLARI BELİRLE", "Genie penceresinin sağ altı — Monster List to Attack", ET, ORTAK)


def g05():
    img = isaret("main", 470, [("1", 58, 540, 459, 576), ("2", 58, 582, 459, 618), ("3", 58, 625, 459, 661)], kirp=(50, 502, 469, 676))
    L = [("1", "<b>Party heal below</b> — party üyesinin canı bu yüzdenin altına inince destek skilli"),
         ("2", "<b>Self heal below</b> — kendi canın bu yüzdenin altına inince"),
         ("3", "<b>Attack range</b> — sürgü (metre)<br>düşük = dar alan · yüksek = geniş alan")]
    return SG.kart(f'<div class="yan">{img}{lg(1, L)}</div>', "👥 PARTY HP · ❤️ KENDİ HP · 📏 ATTACK RANGE", "Main sekmesi — Assist Thresholds", ET, ORTAK)


def g06():
    img = isaret("misc", 900, [("1", 488, 107, 1180, 233), ("2", 488, 247, 1180, 373), ("3", 488, 387, 1180, 513)])
    L = [(str(i), f"<b>{e(bas)}</b><br>" + "<br>".join(f"{e(en)} <span class='en'>— {e(tr)}</span>" for en, tr in sec)) for i, (bas, sec) in enumerate(V.EKRAN_MISC, 1)]
    return SG.kart(img + lg(3, L), "🧩 MISC / GELİŞMİŞ AYARLAR", "Genie penceresi — Misc sekmesi", ET, ORTAK)


def g07():
    css = ORTAK + f""".ad{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}} .ad .kut{{text-align:center;padding:16px 10px}}
.ad .no{{width:40px;height:40px;margin:0 auto 8px;border-radius:50%;background:{A};color:#1b1400;font-weight:900;font-size:20px;display:flex;align-items:center;justify-content:center}}
.ad .t{{font-size:16px;line-height:1.45;font-weight:700;color:#e8dcc8}} .ad .son{{border:2px solid {A};background:linear-gradient(180deg,#3a2c14,#1d1712)}}"""
    ad = '<div class="ad">' + "".join(f'<div class="kut{" son" if i == 7 else ""}"><div class="no">{i + 1}</div><div class="t">{e(x)}</div></div>' for i, x in enumerate(V.KURULUM)) + "</div>"
    n = '<div class="not" style="text-align:center">Kalan Genie süren <b>üst panelde</b> · istediğin an <b>▶ Başlat / ■ Durdur</b></div>'
    return SG.kart(ad + n, "🚀 GENIE NASIL KURULUR?", "8 adımda Genie", ET, css)


KARTLAR = [("G00_ozet.jpg", g00), ("G01_panel.jpg", g01), ("G02_ana.jpg", g02), ("G03_pot.jpg", g03), ("G04_mob.jpg", g04),
           ("G05_esik_range.jpg", g05), ("G06_misc.jpg", g06), ("G07_kurulum.jpg", g07)]

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

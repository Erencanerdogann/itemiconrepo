# -*- coding: utf-8 -*-
# UCRETSIZ TEAMSPEAK GORSELLERI (patron 8 Eki: "resimli vs ayni janradan devam"). Veri: _ts_veri.py (forum.sexyko.com/d/55'e assert'li).
# Kart stili + buyuk font: _skill_gorsel.py. Adim kartlarinda gonderinin KENDI ekran goruntuleri (ts_1..3.png) + aciklama.
# CIKTI: teamspeak/resim/Q00..Q04 (*.jpg, 960 px) -> _ts_konu.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, io, base64
from PIL import Image
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _ts_veri as V

RD = os.path.join(V.TD, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
TS = "#4fb3ff"                                   # TeamSpeak mavisi (formdaki renk) — adres / KEY vurgusu
ET = "SEXYKO · ÜCRETSİZ TEAMSPEAK"
e = lambda s: SG.e(s).replace("&#x27;", "’")


def ss(n, gen):
    """Gonderinin ekran goruntusu -> data URI (gen px genislik)."""
    with Image.open(V.RESIM[n]) as im:
        b = io.BytesIO(); im.convert("RGB").save(b, "PNG")
    return f'<img class="ss" src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}" style="width:{gen}px" alt="">'


ORTAK = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}} .ts{{color:{TS};font-weight:900}} .ad{{font-family:Consolas,monospace;color:{TS};font-weight:700}}
.ss{{display:block;border-radius:8px;border:2px solid #6b5426;box-shadow:0 6px 20px rgba(0,0,0,.45)}}
.ik2{{display:flex;gap:18px;align-items:flex-start}} .ik2 .sag{{flex:1;min-width:0}}
.ad1{{display:flex;gap:12px;align-items:flex-start;margin:0 0 12px}} .ad1 .no{{flex:none;width:34px;height:34px;border-radius:50%;background:{A};color:#1b1400;font-weight:900;font-size:18px;display:flex;align-items:center;justify-content:center}}
.ad1 .t{{font-size:16px;line-height:1.5;color:#e8dcc8}} .ad1 .t b{{color:{A2}}}
"""


def q00():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}} .g .kut{{text-align:center;padding:18px 12px}}
.g .ic{{font-size:42px;line-height:1}} .g .b{{font-size:17px;font-weight:900;color:{A2};letter-spacing:1px;margin:10px 0 6px}} .g .d{{font-size:15px;line-height:1.5}}
.yol{{display:flex;align-items:stretch;gap:10px;margin-top:14px}} .yol .s{{flex:1;background:linear-gradient(180deg,#2a2018,#1b1511);border:1px solid #6b5426;border-radius:10px;padding:12px;text-align:center}}
.yol .s .n{{font-size:13px;font-weight:900;color:{A};letter-spacing:2px}} .yol .s .x{{font-size:16px;font-weight:700;color:#e8dcc8;margin-top:4px;line-height:1.4}}
.yol .o{{flex:none;display:flex;align-items:center;font-size:26px;color:{A}}}"""
    g = ('<div class="g">'
         '<div class="kut"><div class="ic">💸</div><div class="b">TAMAMEN ÜCRETSİZ</div><div class="d">ekstra ücret ödemeden<br>kendi TeamSpeak alanın</div></div>'
         '<div class="kut"><div class="ic">📶</div><div class="b">DÜŞÜK PİNG</div><div class="d">hızlı ve stabil<br>clan içi iletişim</div></div>'
         f'<div class="kut"><div class="ic">🛡️</div><div class="b">CLANINA ÖZEL</div><div class="d">kendi adresin<br><span class="ad">clanadi.ts.sexyko.com</span></div></div></div>')
    yol = ('<div class="yol"><div class="s"><div class="n">1. ADIM</div><div class="x">Panel → <span class="ts">TeamSpeak</span></div></div><div class="o">➜</div>'
           '<div class="s"><div class="n">2. ADIM</div><div class="x">Sunucu bilgileri → <b>KEY</b></div></div><div class="o">➜</div>'
           '<div class="s"><div class="n">3. ADIM</div><div class="x">KEY ile ilk giriş → ✅</div></div></div>')
    return SG.kart(g + yol, "🎙️ ÜCRETSİZ TEAMSPEAK SİSTEMİ AKTİF", "Clanına özel, düşük pingli ses sunucusu — 3 adımda kur", ET, css)


def q01():
    css = ORTAK + ".ik2 .sag{padding-top:6px}"
    sag = ('<div class="sag"><div class="ad1"><div class="no">1</div><div class="t"><b>www.sexyko.com</b> hesabına giriş yap</div></div>'
           '<div class="ad1"><div class="no">2</div><div class="t">Üst menüde <span class="ts">TEAMSPEAK</span> bölümüne tıkla<br><span style="color:#a89f91">(resimde kırmızı çerçeveli)</span></div></div>'
           '<div class="not">Açılan ekranda <b>TeamSpeak 3</b> sunucu oluşturma penceresi gelir → 2. adım.</div></div>')
    return SG.kart(f'<div class="ik2">{ss(1, 560)}{sag}</div>', "🔹 1. ADIM — PANELDEN TEAMSPEAK", e(V.ADIM[0][1]), ET, css)


def q02():
    css = ORTAK + """.fl{margin:0 0 10px;background:#1d1712;border:1px solid #3a2e20;border-left:4px solid #4fb3ff;border-radius:8px;padding:9px 12px}
.fl .a{font-size:13px;font-weight:900;letter-spacing:1px;color:#a89f91} .fl .v{font-size:17px;font-weight:700;color:#e8dcc8;margin-top:2px}
.key{margin-top:12px;padding:12px 14px;border-radius:10px;background:linear-gradient(180deg,#3a2c14,#241a0e);border:2px solid #c8a253;text-align:center}
.key .k1{font-size:22px;font-weight:900;color:#ffd27a;letter-spacing:1px} .key .k2{font-size:15px;color:#e8dcc8;margin-top:4px;line-height:1.45}"""
    fl = "".join(f'<div class="fl"><div class="a">{e(a)}</div><div class="v">{("<span class=ad>" + e(v) + "</span>") if "ts.sexyko" in v else e(v)}</div></div>' for a, v in V.FORM)
    sag = (f'<div class="sag">{fl}<div style="font-size:14px;color:#a89f91;margin:-2px 0 6px">Adres: {e(V.FORM_NOT.lower())}</div>'
           f'<div class="not"><b>{e(V.FORM_DUGME)}</b> → hesabınla giriş yapıp sunucunu oluştur.</div>'
           f'<div class="key"><div class="k1">🔑 KEY OLUŞUR</div><div class="k2">Sistem sana özel bir KEY verir.<br><b style="color:#ffd27a">Bu KEY’i mutlaka kaydet</b> — 3. adımda lazım.</div></div></div>')
    return SG.kart(f'<div class="ik2">{ss(2, 380)}{sag}</div>', "🔹 2. ADIM — SUNUCU BİLGİLERİN", "Sunucu adı · kapasite · sana özel adres — formu doldur, sunucunu oluştur", ET, css)


def q03():
    css = ORTAK
    sag = ('<div class="sag"><div class="ad1"><div class="no">1</div><div class="t"><b>TeamSpeak 3</b> ile kendi adresine bağlan<br><span class="ad">clanadi.ts.sexyko.com</span></div></div>'
           '<div class="ad1"><div class="no">2</div><div class="t">İlk girişte <b>KEY</b>’i ilgili alana gir</div></div>'
           '<div class="ad1"><div class="no">✓</div><div class="t"><b>İşlem tamamlandı!</b><br>Kanallarını aç, clanını çağır.</div></div>'
           '<div class="not">Örnek sunucu: Lobi · Klan Toplantısı · PK Odası · Parti 1-2-3 · Sohbet · Müzik · AFK</div></div>')
    return SG.kart(f'<div class="ik2">{ss(3, 520)}{sag}</div>', "🔹 3. ADIM — KEY İLE İLK GİRİŞ", e(V.ADIM[2][1]), ET, css)


def q04():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}} .g .kut{{text-align:center;padding:18px 10px}}
.g .ic{{font-size:42px;line-height:1}} .g .b{{font-size:18px;font-weight:900;color:{A2};letter-spacing:1px;margin-top:10px}}
.sl{{margin-top:14px;text-align:center;font-size:20px;font-weight:900;color:{VU}}} .sl span{{display:block;font-size:16px;color:#e8dcc8;font-weight:700;margin-top:4px}}"""
    alan = [("⚔️", "PK"), ("🌾", "FARM"), ("🎉", "EVENT"), ("🏰", "CASTLE SIEGE WAR")]
    g = '<div class="g">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="b">{b}</div></div>' for i, b in alan) + "</div>"
    sl = f'<div class="sl">🔥 {e(V.SLOGAN[0])}<span>{e(V.SLOGAN[1])} · {e(V.SLOGAN[2])}</span></div>'
    return SG.kart(g + f'<div class="not">{e(V.CLAN)}</div>' + sl, "⚔️ " + e(V.CLAN_BAS), "Takım iletişiminin önemli olduğu her yerde clanınla tek kanalda", ET, css)


KARTLAR = [("Q00_ozet.jpg", q00), ("Q01_adim1.jpg", q01), ("Q02_adim2.jpg", q02), ("Q03_adim3.jpg", q03), ("Q04_clan.jpg", q04)]

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

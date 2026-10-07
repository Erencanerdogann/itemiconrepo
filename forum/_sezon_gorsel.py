# -*- coding: utf-8 -*-
# SEZON SISTEMI (ACADEMY) GORSELLERI (patron 7 Eki: "guzelce yaz, resimle, guzel bir academy rehberi olsun").
# Veri: _sezon_veri.py (tablo + forum d/57'ye assert'li). Kart stili + buyuk font: _skill_gorsel.py (kart, CSS, buyut_css).
# CIKTI: sezon/resim/Z00..Z04 (*.jpg, 960 px) -> _sezon_konu.py konuya koyar.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _sezon_veri as V

RD = os.path.join(V.SZ, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
EXP_R, DROP_R, COIN_R = "#4fd1ff", "#3ecf8e", "#ffb03a"
ET = "SEXYKO · SEZON SİSTEMİ (ACADEMY)"
e = lambda s: SG.e(s).replace("&#x27;", "’")
KISA_AY = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
def gk(d): return f"{d.day} {KISA_AY[d.month - 1]}"                  # '20 Kas'

ORTAK = f"""
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}} .ex{{color:{EXP_R};font-weight:900}} .dr{{color:{DROP_R};font-weight:900}} .co{{color:{COIN_R};font-weight:900}}
"""


def z00():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.g .kut{{text-align:center;padding:16px 12px}} .g .ic{{font-size:40px;line-height:1}} .g .b{{font-size:16px;font-weight:900;color:{A2};letter-spacing:1px;margin:8px 0 6px}}
.g .d{{font-size:15px;line-height:1.5}} .g .d b{{color:{VU}}}"""
    s1, s8 = V.SEZON[0], V.SEZON[-1]
    k = [("📅", "8 SEZON", f"<b>{gk(s1['acilis'])} {s1['acilis'].year}</b> → <b>{gk(s8['birlesim'])} {s8['birlesim'].year}</b><br>28 günde bir yeni sezon"),
         ("🕙", "AÇILIŞ", "Her sezon <b>Cuma 22:00</b><br>(TSİ)"),
         ("📈", "ORANLAR", '<span class="ex">EXP</span> · <span class="dr">DROP</span> · <span class="co">COIN</span><br><b>%100</b> → kademeli → <b>%800</b>'),
         ("🏆", "TURNUVA", 'Kayıtlar: ilk <b style="white-space:nowrap">Pazartesi 12:00</b><br>Duyuru: birleşim günü'),
         ("🔄", "BİRLEŞİM", "Sonraki haftanın <b>Pazartesi 22:00</b><br>gelişimle ana sunucuya"),
         ("💰", "GB ALIMI", "Her sezon ayrı · <b>BursaGB.com</b><br>sezon 1'den 8'e")]
    g = '<div class="g">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="b">{b}</div><div class="d">{d}</div></div>' for i, b, d in k) + "</div>"
    return SG.kart(g, "⚔️ SEZON SİSTEMİ (ACADEMY)", e(V.SLOGAN), ET, css)


def z01():
    css = ORTAK + f""".tb{{width:100%;border-collapse:separate;border-spacing:0 6px}}
.tb th{{font-size:13px;color:{G};letter-spacing:1px;padding:4px 8px;text-align:center}}
.tb td{{background:#1d1712;border-top:1px solid #3a2e20;border-bottom:1px solid #3a2e20;padding:9px 10px;text-align:center;font-size:16px}}
.tb td:first-child{{border-left:4px solid var(--r);border-radius:6px 0 0 6px;text-align:left}} .tb td:last-child{{border-right:1px solid #3a2e20;border-radius:0 6px 6px 0}}
.sn{{font-size:19px;font-weight:900;color:var(--r)}} .tr{{font-weight:800;color:#e8dcc8}} .gn{{font-size:13px;color:{G}}}
.or{{font-size:20px;font-weight:900;color:var(--r)}} .alt3{{text-align:center;color:{G};font-size:14px;margin-top:6px}} .alt3 b{{color:{A2}}}"""
    renk = ["#8fd16a", "#6fd1a0", "#4fd1ff", "#5fa8ff", "#a98bff", "#d07cff", "#ff8ac6", "#ffa94d"]
    sat = "".join(f'<tr style="--r:{renk[i]}"><td><span class="sn">SEZON {z["no"]:02d}</span></td>'
                  f'<td><span class="tr">{V.kisa(z["acilis"])}</span><br><span class="gn">Cuma · 22:00</span></td>'
                  f'<td><span class="tr">{V.kisa(z["turnuva"])}</span><br><span class="gn">Pazartesi · 12:00</span></td>'
                  f'<td><span class="tr">{V.kisa(z["birlesim"])}</span><br><span class="gn">Pazartesi · 22:00</span></td>'
                  f'<td><span class="or">%{z["oran"]}</span><br><span class="gn">EXP · DROP · COIN</span></td></tr>' for i, z in enumerate(V.SEZON))
    tb = f'<table class="tb"><tr><th>SEZON</th><th>🟢 AÇILIŞ</th><th>🏆 TURNUVA KAYDI</th><th>🔄 BİRLEŞİM</th><th>📈 ORAN</th></tr>{sat}</table>'
    alt = f'<div class="alt3">Official <b>{V.OFFICIAL}</b> · saatler <b>TSİ</b> · açılışlar <b>28 günde bir Cuma</b> · birleşim <b>sonraki haftanın Pazartesi</b>si</div>'
    return SG.kart(tb + alt, "📅 2026 – 2027 SEZON TAKVİMİ", "8 sezon — açılış, turnuva kaydı, ana sunucuyla birleşim, oranlar", ET, css)


def z02():
    css = ORTAK + f""".yol{{position:relative;display:flex;justify-content:space-between;margin:26px 10px 8px}}
.yol:before{{content:"";position:absolute;left:60px;right:60px;top:38px;height:4px;background:linear-gradient(90deg,{DROP_R},{EXP_R},{A},{VU});border-radius:2px}}
.ad{{position:relative;width:200px;text-align:center}} .ad .no{{width:78px;height:78px;margin:0 auto;border-radius:50%;background:#1d1712;border:3px solid var(--r);
display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:30px}}
.ad .gn{{font-size:13px;color:{G};font-weight:800;letter-spacing:1px;margin-top:10px}} .ad .t{{font-size:18px;font-weight:900;color:var(--r);margin:4px 0}}
.ad .s{{font-size:16px;font-weight:800;color:#e8dcc8}} .ad .x{{font-size:14px;color:{G};margin-top:6px;line-height:1.4}}"""
    s = V.SEZON[0]
    ad = [(DROP_R, "🟢", "CUMA", "SEZON AÇILIR", "Cuma · 22:00", "Artırılmış EXP · DROP · COIN"),
          (EXP_R, "🏆", "İLK PAZARTESİ", "TURNUVA KAYDI", "Pazartesi · 12:00", "Kayıtlar açılır"),
          (A, "🔄", "SONRAKİ PAZARTESİ", "BİRLEŞİM", "Pazartesi · 22:00", "Gelişimle ana sunucuya · turnuva duyurusu"),
          (VU, "⏭️", "28 GÜN SONRA", "YENİ SEZON", "Cuma · 22:00", "Oranlar bir kademe yükselir")]
    y = '<div class="yol">' + "".join(f'<div class="ad" style="--r:{r}"><div class="no">{i}</div><div class="gn">{g_}</div><div class="t">{t}</div><div class="s">{s_}</div>'
                                      f'<div class="x">{x}</div></div>' for r, i, g_, t, s_, x in ad) + "</div>"
    ornek = (f'<div class="not">📌 Örnek — <b>Sezon 01</b>: açılış <b>{V.kisa(s["acilis"])} Cuma 22:00</b> → turnuva kaydı <b>{V.kisa(s["turnuva"])} Pazartesi 12:00</b> '
             f'→ birleşim <b>{V.kisa(s["birlesim"])} Pazartesi 22:00</b> → <b>Sezon 02</b> {V.kisa(V.SEZON[1]["acilis"])} Cuma 22:00</div>')
    return SG.kart(y + ornek, "🔁 BİR SEZON NASIL İŞLER?", "Açılış → turnuva kaydı → ana sunucuyla birleşim → yeni sezon", ET, css)


def z03():
    css = ORTAK + f""".gr{{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;height:330px;margin:10px 6px 0;padding:0 4px;border-bottom:2px solid #6b5426}}
.st{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}}
.st .y{{font-size:18px;font-weight:900;color:var(--r);margin-bottom:6px}} .st .b{{width:100%;border-radius:8px 8px 0 0;background:linear-gradient(180deg,var(--r),#2a1f12)}}
.etk{{display:flex;justify-content:space-between;gap:10px;margin:8px 6px 0;padding:0 4px}} .etk div{{flex:1;text-align:center;font-size:15px;font-weight:800;color:{A2}}}
.etk span{{display:block;font-size:13px;color:{G};font-weight:600}}"""
    renk = ["#8fd16a", "#6fd1a0", "#4fd1ff", "#5fa8ff", "#a98bff", "#d07cff", "#ff8ac6", "#ffa94d"]
    st = "".join(f'<div class="st" style="--r:{renk[i]}"><div class="y">%{z["oran"]}</div><div class="b" style="height:{int(z["oran"] / 800 * 270)}px"></div></div>' for i, z in enumerate(V.SEZON))
    etk = "".join(f'<div>S{z["no"]:02d}<span>{gk(z["acilis"])}</span></div>' for z in V.SEZON)
    nt = '<div class="not">📈 İlk sezon <b>%100</b> ile başlar · her sezon <b>EXP · DROP · COIN</b> birlikte bir kademe yükselir · <b>Sezon 08</b>\'de <b>%800</b>.</div>'
    return SG.kart(f'<div class="gr">{st}</div><div class="etk">{etk}</div>' + nt, "📈 KADEMELİ ORANLAR",
                   '<span class="ex">EXP</span> · <span class="dr">DROP</span> · <span class="co">COIN</span> — sezon sezon yükselir', ET, css)


def z04():
    css = ORTAK + f""".iki{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .iki .kut{{padding:18px 18px}}
.iki h3{{margin:0 0 12px;font-size:20px;color:{A2};letter-spacing:1px}} .sat{{font-size:16px;line-height:1.6;color:#e8dcc8;margin:0 0 6px}} .sat b{{color:{VU}}}"""
    tv = ('<div class="kut"><h3>🏆 TURNUVA</h3>' + "".join(f'<div class="sat">{i} {e(t).replace("Pazartesi • 12:00", "<b>Pazartesi • 12:00</b>").replace("Birleşim Günü", "<b>Birleşim Günü</b>")}</div>' for i, t in V.TURNUVA)
          + f'<div class="sat" style="color:{G};font-size:14px">{e(V.TURNUVA_NOT)}</div></div>')
    gb = (f'<div class="kut"><h3>💰 GB ALIMI</h3><div class="sat">🛒 <b>BursaGB.com</b> üzerinden</div><div class="sat">📅 Sezon başladığında</div>'
          f'<div class="sat">🔁 <b>Her sezon ayrı</b> — <span style="white-space:nowrap">Sezon 01 → Sezon 08</span></div><div class="sat" style="color:{G};font-size:14px">Serverın durumuna göre değişebilir.</div></div>')
    nt = f'<div class="not">⚔️ <b>{e(V.BULUSMA)}</b> — {" · ".join(e(x) for x in V.MUCADELE)}</div>'
    return SG.kart(f'<div class="iki">{tv}{gb}</div>' + nt, "🏆 TURNUVA & 💰 GB ALIMI", "Her sezonun turnuvası ve GB alımı", ET, css)


KARTLAR = [("Z00_ozet.jpg", z00), ("Z01_takvim.jpg", z01), ("Z02_akis.jpg", z02), ("Z03_oran.jpg", z03), ("Z04_turnuva_gb.jpg", z04)]

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

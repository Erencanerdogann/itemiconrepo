# -*- coding: utf-8 -*-
# HYPER BETA ODULLERI GORSELLERI (patron 7 Eki: "skill ve master gibi ... resimli detayli" + Semih "gorselli yaptin ya guzel oldu").
# Veri: _odul_veri.py (forum.sexyko.com/d/54'e assert'li). Kart stili + buyuk font: _skill_gorsel.py (kart, CSS, buyut_css) — ayni gorunum.
# CIKTI: odul/resim/O00..O05 (*.jpg, 960 px) -> _odul_konu.py konuya koyar.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os
from playwright.sync_api import sync_playwright
import _skill_gorsel as SG
import _odul_veri as V

RD = os.path.join(V.OD, "resim"); os.makedirs(RD, exist_ok=True)
A, A2, G, VU = SG.ALTIN, SG.ALTIN2, SG.GRI, SG.VURGU
TL_R, SB_R = "#3ecf8e", "#4fd1ff"        # nakit yesil, SB mavi (her gorselde ayni anlam)
ET = "SEXYKO · HYPER BETA ÖDÜLLERİ"
e = lambda s: SG.e(s).replace("&#x27;", "’")   # kalin yazida duz kesme isareti nokta gibi gorunuyor -> tipografik

ORTAK = f"""
.tl{{color:{TL_R};font-weight:900;white-space:nowrap}} .sb{{color:{SB_R};font-weight:900;white-space:nowrap}} .hk{{color:{VU};font-weight:900;white-space:nowrap}}
.kut{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 16px}}
.not{{margin-top:14px;padding:12px 16px;border-radius:8px;background:#2a1f12;border:1px solid #6b5426;font-size:15px;line-height:1.5;color:#e8dcc8}}
.not b{{color:{A2}}}
.top{{display:flex;gap:12px;margin-top:14px}} .top .kut{{flex:1;text-align:center}}
.top .t1{{font-size:13px;letter-spacing:1px;color:{G};font-weight:700}} .top .t2{{font-size:24px;margin-top:4px}}
"""


def para(x):
    """'20.000 TL' -> yesil, '20.000 SB' -> mavi, digeri (heykel) turuncu."""
    if x.endswith(" TL"): return f'<span class="tl">💵 {e(x)}</span>'
    if x.endswith(" SB"): return f'<span class="sb">💎 {e(x)}</span>'
    if "Kişi başı" in x: return f'<span class="sb">💎 {e(x)}</span>'
    return f'<span class="hk">🗿 {e(x)}</span>'


def o00():
    css = ORTAK + f""".g{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.g .kut{{text-align:center;padding:16px 12px}} .g .ic{{font-size:40px;line-height:1}} .g .b{{font-size:16px;font-weight:900;color:{A2};letter-spacing:1px;margin:8px 0 6px}}
.g .d{{font-size:15px;line-height:1.5}}"""
    k = [("🏰", "4 BETA CSW", f'<span class="tl">💵 {V.GENEL_TOPLAM[0]}</span><br><span class="sb">💎 {V.GENEL_TOPLAM[1]}</span><br>4 CSW genel toplamı'),
         ("👑", "CLAN SIRALAMASI", f'<span class="sb">💎 {V.CLAN_TOPLAM}</span><br>ilk 3 Clan · genel Clan NP sıralaması'),
         ("⚔️", "JOB SIRALAMASI", f'Her Job 1.\'si: <span class="tl">2.500 TL</span> + <span class="sb">2.500 SB</span><br><span class="hk">🗿 30 cm fiziksel heykel</span>'),
         ("🎁", "100.000+ NP ÇEKİLİŞİ", '<span class="hk">🗿 Job Heykeli</span> + <span class="sb">💎 SB</span><br>100.000 NP ve üzeri kasanlar'),
         ("📅", "CSW TAKVİMİ", "17 · 18 · 20 · 22 Ekim<br>her gün <b>22:00</b> · 10 dk hazırlık + 60 dk savaş"),
         ("🚀", "HYPER OFFICIAL", f'<b>{V.OFFICIAL.title().replace("Ekim", "Ekim")}</b><br>www.sexyko.com')]
    g = '<div class="g">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="b">{b}</div><div class="d">{d}</div></div>' for i, b, d in k) + "</div>"
    return SG.kart(g, "🏆 HYPER BETA ÖDÜLLERİ", f"Beta <b>{V.BETA[0]} · {V.BETA[1]}</b> — rekabet ilk günden başlıyor", ET, css)


def o01():
    css = ORTAK + f""".cs{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.cs .kut{{text-align:center;padding:16px 10px}} .cs .fn{{border:2px solid {A};background:linear-gradient(180deg,#3a2c14,#1d1712)}}
.cs .gn{{font-size:40px;font-weight:900;color:{A2};line-height:1}} .cs .ay{{font-size:15px;color:{G};font-weight:700;letter-spacing:2px}}
.cs .dy{{font-size:16px;color:#e8dcc8;font-weight:700;margin-top:2px}} .cs .ad{{font-size:17px;font-weight:900;color:{A};margin:10px 0 6px}}
.cs .sa{{font-size:22px;font-weight:900;color:{VU}}} .cs .su{{font-size:14px;color:{G};margin-top:4px;line-height:1.4}}
.yol{{display:flex;align-items:center;justify-content:space-between;margin:6px 4px 16px;font-size:14px;color:{G}}}
.yol .n{{text-align:center;flex:none}} .yol .n b{{display:block;color:#e8dcc8;font-size:15px}} .yol .c{{flex:1;height:3px;background:#6b5426;margin:0 8px}}
.yol .bt b{{color:{TL_R}}} .yol .of b{{color:{VU}}}"""
    yol = ('<div class="yol"><div class="n bt"><b>16 Ekim</b>Beta açılış</div><div class="c"></div>'
           + '<div class="c"></div>'.join(f'<div class="n"><b>{t.split()[0]} Ekim</b>{"Final CSW" if "FİNAL" in a else a.split()[0] + " CSW"}</div>' for t, g, a, k in V.CSW)
           + '<div class="c"></div><div class="n of"><b>23 Ekim</b>Official</div></div>')
    kartlar = "".join(f'<div class="kut{" fn" if "FİNAL" in a else ""}"><div class="gn">{t.split()[0]}</div><div class="ay">EKİM 2026</div><div class="dy">{e(g.title().replace("İ", "i") if False else g)}</div>'
                      f'<div class="ad">{"👑" if "FİNAL" in a else "🏰"} {e(a)}</div><div class="sa">🕙 22:00</div><div class="su">⏳ 10 dk hazırlık<br>⚔️ 60 dk savaş</div></div>' for t, g, a, k in V.CSW)
    nt = (f'<div class="not">🕙 <b>22:00</b>\'de CSW hazırlık süreci başlar · ilk <b>10 dakika</b> hazırlık · ardından savaş, en fazla <b>60 dakika</b>.<br>'
          f'👑 <b>Beta Final CSW</b> — Official açılıştan yalnızca 1 gün önce, Beta döneminin son Castle Siege War\'ı.</div>')
    return SG.kart(yol + f'<div class="cs">{kartlar}</div>' + nt, "📅 BETA CSW TAKVİMİ", "4 büyük Castle Siege War · hepsi saat <b>22:00</b>", ET, css)


def o02():
    css = ORTAK + f""".kt{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.kt .kut{{text-align:center;padding:18px 12px}} .kt .ic{{font-size:42px;line-height:1}} .kt .ad{{font-size:18px;font-weight:900;color:{A2};margin:10px 0 12px}}
.kt .m{{font-size:26px;line-height:1.35}}"""
    kt = '<div class="kt">' + "".join(f'<div class="kut"><div class="ic">{i}</div><div class="ad">{e(a)}</div><div class="m">{para(tl)}<br>{para(sb)}</div></div>'
                                      for i, a, tl, sb in V.CSW_ODUL) + "</div>"
    top = (f'<div class="top"><div class="kut"><div class="t1">HER CSW\'DE TOPLAM</div><div class="t2">{para(V.CSW_TOPLAM[0])} · {para(V.CSW_TOPLAM[1])}</div></div>'
           f'<div class="kut" style="border-color:{A}"><div class="t1">4 CSW GENEL TOPLAMI</div><div class="t2">{para(V.GENEL_TOPLAM[0])} · {para(V.GENEL_TOPLAM[1])}</div></div></div>')
    kural = '<div class="not">⚠️ <b>CSW ÖDÜL KURALI</b><br>' + "<br>".join(f"◆ {e(x)}" for x in V.CSW_KURAL) + "</div>"
    return SG.kart(kt + top + kural, "🏰 CSW ÖDÜLLERİ", "4 CSW'nin <b>her birinde</b> aynı ödüller dağıtılır", ET, css)


def o03():
    css = ORTAK + f""".pd{{display:flex;align-items:flex-end;justify-content:center;gap:14px;margin:8px 0 4px}}
.pd .s{{width:250px;text-align:center}} .pd .ic{{font-size:46px;line-height:1}} .pd .ad{{font-size:19px;font-weight:900;color:{A2};margin:6px 0}}
.pd .m{{font-size:26px}} .pd .bl{{margin-top:10px;border-radius:8px 8px 0 0;background:linear-gradient(180deg,#5a4520,#2a1f12);border:1px solid #6b5426;border-bottom:none}}
.pd .s1 .bl{{height:120px;background:linear-gradient(180deg,#8a6a24,#3a2c14);border-color:{A}}} .pd .s2 .bl{{height:84px}} .pd .s3 .bl{{height:56px}}
.pd .bl span{{display:block;padding-top:10px;font-size:34px;font-weight:900;color:#1b1400;text-shadow:0 1px 0 #e6c46a}}"""
    s = {1: V.CLAN[0], 2: V.CLAN[1], 3: V.CLAN[2]}
    pd = '<div class="pd">' + "".join(f'<div class="s s{n}"><div class="ic">{s[n][0]}</div><div class="ad">{e(s[n][1])}</div><div class="m">{para(s[n][2])}</div>'
                                      f'<div class="bl"><span>{n}</span></div></div>' for n in (2, 1, 3)) + "</div>"
    top = f'<div class="top"><div class="kut" style="border-color:{A}"><div class="t1">TOPLAM</div><div class="t2">{para(V.CLAN_TOPLAM)}</div></div></div>'
    nt = '<div class="not">👑 ' + "<br>".join(e(x) for x in V.CLAN_NOT) + "</div>"
    return SG.kart(pd + top + nt, "👑 CLAN SIRALAMA ÖDÜLLERİ", "Beta sonunda <b>genel Clan NP sıralaması</b>", ET, css)


def o04():
    css = ORTAK + f""".jb{{display:flex;justify-content:center;gap:10px;margin:0 0 14px}}
.jb span{{font-size:18px;font-weight:900;padding:6px 16px;border-radius:20px;background:#1d1712;border:2px solid var(--r);color:var(--r)}}
.sr{{display:flex;align-items:center;gap:16px;margin:0 0 10px}} .sr .kut{{display:flex;align-items:center;gap:16px;width:100%}}
.sr .ic{{font-size:40px;flex:none;width:52px;text-align:center}} .sr .ad{{font-size:19px;font-weight:900;color:{A2};width:250px;flex:none}}
.sr .m{{font-size:21px;display:flex;flex-wrap:wrap;gap:6px 18px}} .sr.b1 .kut{{border:2px solid {A};background:linear-gradient(90deg,#3a2c14,#1d1712)}}"""
    jb = '<div class="jb">' + "".join(f'<span style="--r:{SG.JOB_RENK[j]}">{j}</span>' for j in V.JOBLAR) + "</div>"
    sr = "".join(f'<div class="sr{" b1" if i == 0 else ""}"><div class="kut"><div class="ic">{ic}</div><div class="ad">{e(a)}</div><div class="m">'
                 + "".join(f"<span>{para(x)}</span>" for x in od) + "</div></div></div>" for i, (ic, a, od) in enumerate(V.JOB_ODUL))
    nt = f'<div class="not">⚔️ {e(V.JOB_NOT)}<br>🎖️ {e(V.JOB_5_10)}</div>'
    return SG.kart(jb + sr + nt, "⚔️ JOB SIRALAMA ÖDÜLLERİ", "5 job — <b>her job kendi içinde</b> ayrı sıralama", ET, css)


def o05():
    css = ORTAK + f""".sr{{display:flex;align-items:center;gap:16px;margin:0 0 10px}} .sr .kut{{display:flex;align-items:center;gap:16px;width:100%}}
.sr .ic{{font-size:40px;flex:none;width:52px;text-align:center}} .sr .ad{{font-size:19px;font-weight:900;color:{A2};width:250px;flex:none}}
.sr .m{{font-size:21px;display:flex;flex-wrap:wrap;gap:6px 18px}} .sr.b1 .kut{{border:2px solid {A};background:linear-gradient(90deg,#3a2c14,#1d1712)}}
.sart{{text-align:center;font-size:20px;font-weight:800;color:#e8dcc8;margin:0 0 14px}} .sart b{{color:{VU};font-size:24px}}"""
    sart = '<div class="sart">Beta boyunca <b>100.000 NP</b> ve üzeri kas → çekilişe katılma hakkı</div>'
    sr = "".join(f'<div class="sr{" b1" if i == 0 else ""}"><div class="kut"><div class="ic">{ic}</div><div class="ad">{e(a)}</div><div class="m">'
                 + "".join(f"<span>{para(x)}</span>" for x in od) + "</div></div></div>" for i, (ic, a, od) in enumerate(V.NP))
    return SG.kart(sart + sr, "🎁 100.000+ NP BETA ÇEKİLİŞİ", "Özel Beta çekilişi — <b>1.’den 10.’ya</b> ödül", ET, css)


KARTLAR = [("O00_ozet.jpg", o00), ("O01_takvim.jpg", o01), ("O02_csw_odul.jpg", o02), ("O03_clan.jpg", o03), ("O04_job.jpg", o04), ("O05_np_cekilis.jpg", o05)]

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

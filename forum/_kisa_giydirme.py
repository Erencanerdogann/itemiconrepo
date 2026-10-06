# -*- coding: utf-8 -*-
# KISA KONU GIYDIRME — her bolum FORUM_KONU.html'in koyu-altin tasarimiyla GORSEL olarak (patron 4 Eki: "icerik neden cok kotu,
# FORUM_KONU.html gibi olacak ama bizim giydirme olacak"). Sebep: forum editoru beyaz zemin, BBCode renkleri solukti, resimler yoktu.
# Gorselde: numara + baslik + kucuk resim + tek satir. Linkler gorselin ALTINDA BBCode (tiklanir); gorselin kendisi bolumun ilk linkine gider.
# CIKTI: yeni_konu/kisa/giydirme/G00.png (baslik karti) + G01..G24.png + GIYDIRME_bbcode.txt (jeton {{G01}}) + onizleme.html
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, html, base64, json
import _kisa_konu as KK
from playwright.sync_api import sync_playwright

Y = KK.Y
OUT = os.path.join(KK.OUT, "giydirme"); os.makedirs(OUT, exist_ok=True)
A, A2, G, M = Y.ALTIN, Y.ALTIN2, Y.GRI, Y.MAVI
W = 760

CSS = f"""
*{{box-sizing:border-box;margin:0}}
body{{background:transparent;font-family:'Segoe UI',Tahoma,sans-serif;padding:0}}
.k{{width:{W}px;padding:26px 34px 28px;border-radius:16px;text-align:center;color:#ece6da;
   background:radial-gradient(ellipse at 50% 0%,#2a2117 0%,#16120e 55%,#0d0b09 100%);
   border:2px solid {A};box-shadow:inset 0 0 0 1px #000,inset 0 0 38px rgba(200,162,83,.18)}}
.ust{{display:flex;align-items:center;justify-content:center;gap:12px}}
.no{{min-width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:19px;
     color:#1b1400;background:linear-gradient(180deg,#f1d27a,{A});box-shadow:0 0 12px rgba(230,196,106,.45)}}
.t{{font-size:25px;font-weight:800;letter-spacing:.6px;color:{A2};text-shadow:0 2px 0 #000,0 0 14px rgba(230,196,106,.25)}}
.cz{{margin:14px auto 16px;width:72%;height:1px;background:linear-gradient(90deg,transparent,{A},transparent);position:relative}}
.cz:after{{content:"◆";position:absolute;left:50%;top:50%;transform:translate(-50%,-55%);color:{A};font-size:12px;background:#17130e;padding:0 8px}}
.res{{display:inline-block;padding:4px;border:1px solid {A};border-radius:8px;background:#000;box-shadow:0 6px 18px rgba(0,0,0,.6)}}
.res img{{display:block;border-radius:5px;max-width:360px;max-height:240px}}
.m{{margin-top:16px;font-size:18px;line-height:1.5}}
.m b{{color:{A2}}}
.alt{{margin-top:14px;font-size:13px;color:{G};letter-spacing:.5px}}
.bas .t{{font-size:34px}} .bas .m{{font-size:17px;color:{G}}}
"""

def b64(p): return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

def kart(no, emoji, baslik, rid, metin):
    s = f'<div class="k"><div class="ust"><div class="no">{no}</div><div class="t">{emoji} {html.escape(baslik)}</div></div><div class="cz"></div>'
    if rid: s += f'<div class="res"><img src="{b64(os.path.join(KK.RD, "K" + rid + ".jpg"))}"></div>'
    if metin:
        renk = ' style="color:' + A2 + '"'
        s += '<div class="m">' + Y.satir(metin, "html").replace(renk, "") + '</div>'
    s += '<div class="alt">▼ detay için alttaki linke tıkla ▼</div></div>'
    return s

KARTLAR = [("G00", f'<div class="k bas"><div class="t">📘 SEXYKO OYUN REHBERİ</div><div class="cz"></div>'
                   f'<div class="m">24 başlık, kısa kısa — her görselin altındaki linkle detaya git.</div></div>', None)]
for e, no, t, rid, metin, ln in KK.bolumler():
    KARTLAR.append((f"G{no}", kart(no, e, t, rid, metin), ln))

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": W + 40, "height": 900}, device_scale_factor=1)
    for gid, govde, _ in KARTLAR:
        pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{govde}</body></html>")
        pg.wait_for_timeout(150)
        pg.locator(".k").screenshot(path=os.path.join(OUT, gid + ".png"), omit_background=True)
    b.close()

# ---------- forum BBCode: gorsel (ilk linke gider) + altinda tiklanir linkler
o = []
for gid, _, ln in KARTLAR:
    if ln is None:
        o.append(f"[CENTER][IMG]{{{{{gid}}}}}[/IMG][/CENTER]")
        continue
    o.append(f"[CENTER][URL={ln[0][2]}][IMG]{{{{{gid}}}}}[/IMG][/URL]\n[SIZE=4]" +
             " · ".join(f"[URL={u}][B]{i} {a} ↗[/B][/URL]" for i, a, u in ln) + "[/SIZE][/CENTER]")
BB = "\n\n".join(o)
open(os.path.join(OUT, "GIYDIRME_bbcode.txt"), "w", encoding="utf-8").write(BB + "\n")
# yerel onizleme (yukleme oncesi bakmak icin) — gorseller + linkler, beyaz ve koyu zeminde
sat = "".join(f'<div style="margin:18px 0"><a href="{(ln or [(0, 0, "#")])[0][2]}" target="_blank"><img src="{gid}.png" style="max-width:100%"></a>' +
              ("" if ln is None else '<div style="margin-top:6px;font:600 15px Segoe UI">' + " · ".join(f'<a href="{u}" target="_blank" style="color:#2f7fd8">{i} {html.escape(a)} ↗</a>' for i, a, u in ln) + "</div>") + "</div>"
              for gid, _, ln in KARTLAR)
open(os.path.join(OUT, "onizleme.html"), "w", encoding="utf-8").write(
    "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Kısa Konu Giydirme</title></head>"
    "<body style='margin:0;font-family:Segoe UI;display:flex;gap:0;flex-wrap:wrap'>"
    f"<div style='flex:1;min-width:340px;background:#fff;padding:16px;text-align:center'><h3>Beyaz forum zemini</h3>{sat}</div>"
    f"<div style='flex:1;min-width:340px;background:#1e1e1e;color:#ddd;padding:16px;text-align:center'><h3>Koyu forum zemini</h3>{sat}</div></body></html>")
print("giydirme:", len(KARTLAR), "görsel · bbcode", len(BB), "karakter ·", OUT)

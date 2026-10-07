# -*- coding: utf-8 -*-
# SKILL & MASTER GORSELLERI (patron 6 Eki: "once ogren sonra mdle sonra resimlememiz lazim") — veri _skill_veri.py (canli siteye assert'li).
# Her kart HTML olarak kurulur, Playwright ile 960 px genislikte JPG cekilir. Ikon + minimap: site onbellegi rehber/web/resim/ (cdn.sexyko.com).
# CIKTI: skill_master/resim/S01..S07 (*.jpg) -> _skill_konu.py konuya koyar.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, io, re, base64, html
from PIL import Image
from playwright.sync_api import sync_playwright
import _skill_veri as V

RD = os.path.join(V.SM, "resim"); os.makedirs(RD, exist_ok=True)
ALTIN, ALTIN2, GRI, YESIL, KIRMIZI, MAVI, MOR = "#c8a253", "#e6c46a", "#a89f91", "#3ecf8e", "#d14841", "#4fa3ff", "#b07cff"
VURGU = "#ffa94d"   # vurgu (%100, toplam, alt satir) — Rogue yesiliyle karismasin (degerlendirme 6 Eki)
JOB_RENK = {"Warrior": KIRMIZI, "Rogue": YESIL, "Mage": MAVI, "Priest": ALTIN2, "Kurian": MOR, "Porutu": MOR}
BOSS_RENK = ["#ff5c5c", "#ffb03a", "#4fd1ff", "#7dff7a", "#ff7ad9"]
CENTAUR_RENK = "#c77dff"
e = html.escape


def uri(yol):
    tur = "image/webp" if yol.endswith(".webp") else "image/png"
    return f"data:{tur};base64," + base64.b64encode(open(yol, "rb").read()).decode()


_IK = {}


def ik(item_id, px=44):
    """Site ikonu 64x64 tuvalin sol ustunde 45x45 (gerisi seffaf) -> dolu alani kirp, kareyi tam doldursun (patron 6 Eki: 'tam kare icine sok ikonlari')."""
    if item_id not in _IK:
        with Image.open(V.ikon(item_id)) as im:
            im = im.convert("RGBA")
            dolu = im.crop(im.getchannel("A").getbbox())
            b = io.BytesIO(); dolu.resize((96, 96), Image.LANCZOS).save(b, "PNG")
        _IK[item_id] = "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
    return f'<img class="ik" src="{_IK[item_id]}" style="width:{px}px;height:{px}px" alt="">'


def minimap(no):
    return uri(os.path.join(V.WEB, "resim", f"cdn.sexyko.com_minimap_{no}.webp"))


CSS = f"""
*{{box-sizing:border-box}}
body{{margin:0;background:#0d0a08;font-family:"Segoe UI","Segoe UI Emoji",Roboto,Arial,sans-serif;color:#e8dcc8}}
#kart{{width:960px;padding:24px 28px 20px;background:linear-gradient(180deg,#241c15 0%,#16110d 100%);border:2px solid #6b5426;position:relative}}
.etiket{{position:absolute;left:18px;top:12px;font-size:12px;letter-spacing:2px;color:#7d6a4b;font-weight:700}}
h1{{margin:10px 0 4px;text-align:center;font-size:30px;color:{ALTIN};letter-spacing:1px;text-shadow:0 2px 0 #000}}
.alt{{text-align:center;color:{GRI};font-size:15px;margin:0 0 16px}}
.alt b{{color:{ALTIN2}}}
.ik{{display:inline-block;box-sizing:border-box;background:#000;border:1px solid #6b5426;border-radius:4px;vertical-align:middle;flex:none;object-fit:fill;padding:0}}
table{{width:100%;border-collapse:separate;border-spacing:0 6px}}
td,th{{padding:8px 10px;vertical-align:middle}}
th{{color:{GRI};font-size:13px;font-weight:600;text-align:center;letter-spacing:1px}}
tr.sat td{{background:#1d1712;border-top:1px solid #3a2e20;border-bottom:1px solid #3a2e20}}
tr.sat td:first-child{{border-left:4px solid var(--r);border-radius:6px 0 0 6px}}
tr.sat td:last-child{{border-right:1px solid #3a2e20;border-radius:0 6px 6px 0}}
.job{{font-size:20px;font-weight:800;color:var(--r)}}
.irk{{font-size:12px;color:{GRI}}}
.npc{{font-size:16px;font-weight:700;color:{ALTIN2}}}
.yer{{font-size:13px;color:{GRI};margin-top:2px}}
.yer b{{color:#e8dcc8;font-weight:600}}
.it{{display:flex;align-items:center;gap:8px;font-size:13px;line-height:1.25}}
.alt2{{text-align:center;color:{GRI};font-size:13px;margin-top:10px}}
.alt2 b{{color:{VURGU}}}
"""


def buyut_css(s):
    """PATRON 7 Eki: 'yazi fontlarini biraz buyutelim, ozellikle skill master'da' -> resim genisligi ayni (960), yazi buyur (forumda gercekten buyuk gorunsun).
    <=16 px x1,22 (12 -> 14,6 · 13 -> 15,9 · 15 -> 18,3) · 17-24 px x1,1 · buyuk basliklar ayni."""
    def f(m):
        v = float(m.group(1)); k = 1.22 if v <= 16 else 1.1 if v <= 24 else 1.0
        return f"font-size:{round(v * k, 1):g}px"
    return re.sub(r"font-size:(\d+(?:\.\d+)?)px", f, s)


def kart(govde, baslik, alt, etiket="SEXYKO · SKILL & MASTER", ek_css=""):
    return buyut_css(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{ek_css}</style></head><body><div id="kart"><div class="etiket">{etiket}</div>'
                     f'<h1>{baslik}</h1><div class="alt">{alt}</div>{govde}</div></body></html>')


def yer(j):
    s = []
    if j[3]: s.append(f"Karus · Luferson <b>{j[3][0]},{j[3][1]}</b>")
    if j[4]: s.append(f"El Morad · El Morad <b>{j[4][0]},{j[4][1]}</b>")
    return "<br>".join(s)


# ---------- S00 yol haritasi (4 adim)
def s00():
    adim = [("1", "SKILL PUANI", "⌨️", "<b>K</b> ile skill penceresini aç<br>Level 83 = <b>148 puan</b><br>sekme yanındaki <b>▲</b> ile dağıt"),
            ("2", "MASTER GÖREVİ", ik(V.HEART, 40), "Level <b>60+</b><br><b>1 Heart + 2 Essence</b> topla<br>job'unun master NPC'sine götür"),
            ("3", "70 – 80 SKILL", ik(V.SSP, 40), "<b>Spell Stone Powder</b> topla<br>aynı NPC'den görevi al<br>her görev <b>1 skill</b> açar"),
            ("4", "KAYDET", "💾", "<b>Preset</b> → puan dağılımı<br><b>Save Quickslot</b> → 4 skill bar<br>PK · farm · event arası geç")]
    kutu = "".join(f'<div class="a"><div class="no">{n}</div><div class="ic">{ic}</div><div class="t">{t}</div><div class="x">{x}</div></div>' for n, t, ic, x in adim)
    css = f""".gr{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.a{{background:linear-gradient(180deg,#2a2018,#1b1511);border:1px solid #6b5426;border-radius:12px;padding:16px 12px 14px;text-align:center;position:relative}}
.no{{width:42px;height:42px;margin:0 auto 8px;border-radius:50%;background:{ALTIN};color:#1b1400;font-weight:900;font-size:22px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #000,0 0 14px rgba(200,162,83,.5)}}
.ic{{font-size:34px;height:44px;display:flex;align-items:center;justify-content:center}}
.t{{font-size:17px;font-weight:900;color:{ALTIN2};margin:6px 0 8px;letter-spacing:.5px}}
.x{{font-size:13.5px;line-height:1.55;color:#d9cdb8}} .x b{{color:{VURGU}}}"""
    return kart(f'<div class="gr">{kutu}</div><div class="alt2">Master görevi ve 70 – 80 skill görevleri <b>aynı NPC</b>\'den alınır — her job\'un kendi NPC\'si var</div>',
                "🧭 4 ADIMDA SKILL & MASTER", "Warrior · Rogue · Mage · Priest · Kurian · Porutu — hepsi için aynı yol", ek_css=css)


# ---------- S01 master tablosu
def s01():
    sat = ""
    for j in V.JOB:
        its = "".join(f'<td><div class="it">{ik(i)}<span>{e(V.ITEM[i])}</span></div></td>' for i in (V.HEART, j[5], j[6]))
        sat += f'<tr class="sat" style="--r:{JOB_RENK[j[0]]}"><td style="width:120px"><div class="job">{j[0]}</div><div class="irk">{j[1]}</div></td>' \
               f'<td style="width:250px"><div class="npc">{e(j[2])}</div><div class="yer">{yer(j)}</div></td>{its}</tr>'
    g = f'<table><tr><th>JOB</th><th>NPC · YER</th><th colspan="3">GÖTÜRECEĞİN 3 İTEM</th></tr>{sat}</table>' \
        f'<div class="alt2">Görev adı: <b>2nd job change</b> · Level <b>60+</b> · ödül: <b>Job change</b> (Master) · koordinatlar oyun içi x,y</div>'
    return kart(g, "⚔️ MASTER GÖREVİ — 2. JOB", "Herkes <b>1 Unstable Kentaraus' Heart</b> + job'una özel <b>2 Essence</b> götürür")


# ---------- S02 master itemleri
def s02():
    kim = {}
    for j in V.JOB:
        for i in (V.HEART, j[5], j[6]):
            kim.setdefault(i, []).append(j[0])
    kutu = ""
    for i in (V.HEART, V.URK, V.ALK, V.GARU, V.COL, V.TRET):
        d = V.DROP[i]
        lvl = "" if i == V.HEART else f" · Lv {V.lv(d[1][0])}"
        alt = f'<div class="dus">Düşüren: <b>{e(d[0])}</b>{lvl}</div><div class="or">%{d[2][:-1]}</div>' \
              f'<div class="nk">Karus + El Morad haritasında</div>'
        kutu += f'<div class="k">{ik(i, 64)}<div class="ad">{e(V.ITEM[i])}</div>{alt}<div class="kim">{" · ".join(kim[i])}</div></div>'
    css = f""".gr{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.k{{background:#1d1712;border:1px solid #3a2e20;border-radius:10px;padding:14px 12px;text-align:center}}
.k .ad{{font-size:17px;font-weight:800;color:{ALTIN2};margin:8px 0 6px}}
.dus{{font-size:13px;color:{GRI}}} .dus b{{color:#e8dcc8}}
.or{{font-size:34px;font-weight:900;color:{VURGU};line-height:1.2;margin:4px 0 0}} .or.yok{{color:#6b5d4a}}
.nk{{font-size:12px;color:{GRI}}}
.kim{{margin-top:10px;padding-top:8px;border-top:1px solid #3a2e20;font-size:13px;color:{ALTIN}}}"""
    return kart(f'<div class="gr">{kutu}</div><div class="alt2">Alt satır = bu itemi master için isteyen job\'lar</div>',
                "💎 MASTER İTEMLERİ NEREDEN DÜŞER", "Field bosslar <b>%100</b> düşürür · Centaur <b>%50</b>", ek_css=css)


# ---------- S03 / S04 haritalar
HK = 620


def harita(anahtar):
    h = V.HARITA[anahtar]
    px = lambda x, z: (x / 2048 * HK, (1 - z / 2048) * HK)
    isaret, legend = "", ""
    # NPC'ler: 40 birim icindekiler tek numara
    grup = []
    for j in V.JOB:
        xz = j[3] if anahtar == "karus" else j[4]
        if not xz:
            continue
        for g in grup:
            if abs(g["xz"][0] - xz[0]) < 40 and abs(g["xz"][1] - xz[1]) < 40:
                g["j"].append(j); break
        else:
            grup.append({"xz": xz, "j": [j]})
    for n, g in enumerate(grup, 1):
        x, y = px(*g["xz"])
        isaret += f'<div class="npcm" style="left:{x:.1f}px;top:{y:.1f}px">{n}</div>'
        legend += f'<div class="lg"><span class="nm">{n}</span><div>' + "<br>".join(
            f'<b style="color:{JOB_RENK[j[0]]}">{j[0]}</b> · {e(j[2])}' for j in g["j"]) + f'<div class="xz">{g["xz"][0]},{g["xz"][1]}</div></div></div>'
    legend += '<div class="ara"></div>'
    for (cid, it), renk in zip(h["boss"], BOSS_RENK):
        for l, t in V.nokta(cid):
            isaret += f'<div class="bm" style="left:{l / 100 * HK:.1f}px;top:{t / 100 * HK:.1f}px;background:{renk}"></div>'
        legend += f'<div class="lg"><span class="bd" style="background:{renk}"></span>{ik(it, 34)}<div><b>{e(V.CANAVAR[cid]["ad"])}</b> · Lv {V.lv(cid)}' \
                  f'<div class="xz">{e(V.ITEM[it])} %100 · {len(V.nokta(cid))} nokta</div></div></div>'
    for l, t in V.nokta(h["centaur"]):
        isaret += f'<div class="bm" style="left:{l / 100 * HK:.1f}px;top:{t / 100 * HK:.1f}px;background:{CENTAUR_RENK}"></div>'
    legend += f'<div class="lg"><span class="bd" style="background:{CENTAUR_RENK}"></span>{ik(V.HEART, 34)}<div><b>Centaur</b>' \
              f'<div class="xz">Unstable Kentaraus\' Heart %50 · {len(V.nokta(h["centaur"]))} nokta</div></div></div>'
    css = f""".hw{{display:flex;gap:16px;align-items:flex-start}}
.map{{position:relative;width:{HK}px;height:{HK}px;flex:none;background:url({minimap(h["minimap"])}) center/100% 100%;border:2px solid #6b5426;border-radius:6px}}
.npcm{{position:absolute;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:{ALTIN};color:#1b1400;font-weight:900;font-size:16px;
 display:flex;align-items:center;justify-content:center;border:2px solid #fff;box-shadow:0 0 0 2px #000,0 0 12px #000}}
.bm{{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;border:2px solid #000;box-shadow:0 0 6px #000}}
.leg{{flex:1;font-size:14px}}
.lg{{display:flex;gap:8px;align-items:center;margin:0 0 10px}}
.lg b{{color:#e8dcc8}}
.nm{{flex:none;width:26px;height:26px;border-radius:50%;background:{ALTIN};color:#1b1400;font-weight:900;display:flex;align-items:center;justify-content:center}}
.bd{{flex:none;width:14px;height:14px;border-radius:50%;border:2px solid #000}}
.xz{{font-size:12px;color:{GRI}}}
.ara{{height:1px;background:#3a2e20;margin:6px 0 12px}}"""
    alt = f'<b>{h["irk"]}</b> · numaralar master NPC\'leri · renkli noktalar master itemi düşüren moblar'
    return kart(f'<div class="hw"><div class="map">{isaret}</div><div class="leg">{legend}</div></div>'
                f'<div class="alt2">Noktalar oyun içi rehberin (sexyko.com/guide) spawn kayıtlarından · NPC yerleri x,y</div>',
                f"🗺️ {h['irk'].upper()} — {h['ad'].upper()} HARİTASI", alt, ek_css=css)


# ---------- S05 skill gorevleri
def s05():
    sat = ""
    satirlar = V.JOB   # Kurian ve Porutu ayri satir (degerlendirme 6 Eki)
    for j in satirlar:
        ad, npc = j[0], j[2]
        hucre = "".join(f'<td class="c">{ik(V.SSP, 26)} <b>{V.ssp_adet(j[8][l])}</b></td>' if l in j[8] else '<td class="c bos">—</td>' for l in V.SEVIYE)
        sat += f'<tr class="sat" style="--r:{JOB_RENK[j[0]]}"><td style="width:150px"><div class="job">{ad}</div></td><td class="np">{e(npc)}</td>{hucre}' \
               f'<td class="c top">{V.toplam(j)}</td></tr>'
    bas = "".join(f"<th>{l}</th>" for l in V.SEVIYE)
    css = f""".c{{text-align:center;font-size:18px;white-space:nowrap}} .c b{{color:#e8dcc8}} .c .ik{{border-radius:4px}}
.bos{{color:#4d4134}} .top{{font-size:24px;font-weight:900;color:{VURGU}}} .np{{font-size:13px;color:{ALTIN2};font-weight:700;width:150px}}"""
    g = f'<table><tr><th>JOB</th><th>NPC</th>{bas}<th>TOPLAM</th></tr>{sat}</table>' \
        f'<div class="alt2">Görev adı: <b>70Lv skill</b>, <b>72Lv skill</b> … <b>80Lv skill</b> · her görevin ödülü: o seviyenin <b>skill\'i</b> · önce Master ol</div>'
    return kart(g, "📜 70 – 80 SKILL GÖREVLERİ", f"{ik(V.SSP, 22)} <b>Spell Stone Powder</b> adedi · NPC = master NPC'n", ek_css=css)


# ---------- S06 spell stone kaynaklari
def s06():
    satir = ""
    dort = V.SSP_MOB[:4]
    satir += f'<tr class="sat" style="--r:{VURGU}"><td class="m">{" · ".join(e(V.CANAVAR[c]["ad"]) for c in dort)}</td><td class="c">Lv {V.lv(dort[0])}</td>' \
             f'<td class="c or">%{V.ssp_oran(dort[0]):g}</td><td class="y">Ronark Land · her biri 2 nokta</td></tr>'
    for c in V.SSP_MOB[4:]:
        satir += f'<tr class="sat" style="--r:{ALTIN}"><td class="m">{e(V.CANAVAR[c]["ad"])}</td><td class="c">Lv {V.lv(c)}</td>' \
                 f'<td class="c or">%{V.ssp_oran(c):g}</td><td class="y">Ronark Land · {len(V.nokta(c))} nokta</td></tr>'
    for (havuz, adet), no in zip(V.NARKI, (4, 5)):
        ort = format(V.narki_ort(no), ".1f").replace(".", ",")
        satir += f'<tr class="sat" style="--r:{MAVI}"><td class="m">Narki — <b>{havuz}</b> havuzu</td><td class="c">—</td>' \
                 f'<td class="c or">{adet}</td><td class="y">Moradon · {e(V.NARKI_NPC["ad"])}<br>takı ver · ortalama ≈ {ort} adet (Narki kartı)</td></tr>'
    ihtiyac = " · ".join(f'{j[0]} <b>{V.toplam(j)}</b>' for j in V.JOB)
    css = f""".m{{font-size:17px;font-weight:800;color:{ALTIN2}}} .m b{{color:{MAVI}}} .c{{text-align:center;font-size:16px;white-space:nowrap}}
.or{{font-size:24px;font-weight:900;color:{VURGU}}} .y{{font-size:13px;color:{GRI}}}"""
    g = f'<table><tr><th>KAYNAK</th><th>LEVEL</th><th>ORAN / ADET</th><th>YER</th></tr>{satir}</table>' \
        f'<div class="alt2">Toplam ihtiyaç (70→80): {ihtiyac}</div>'
    return kart(g, f"{ik(V.SSP, 40)} SPELL STONE POWDER NEREDEN?", "70 – 80 skill görevlerinin tek malzemesi", ek_css=css)


# ---------- S08 job job NPC karti (patron 6 Eki: "hala skill npcleri yok ... mala anlatir gibi")
def mini(minimap_no, xz, boyut=124, olcek=760):
    """haritadan NPC cevresi kesit: tam harita olcek px'e buyutulur, NPC kesitin ortasina gelir."""
    x, y = xz[0] / 2048 * olcek, (1 - xz[1] / 2048) * olcek
    return f'<div class="mm" style="width:{boyut}px;height:{boyut}px;background:url({minimap(minimap_no)}) {boyut / 2 - x:.1f}px {boyut / 2 - y:.1f}px/{olcek}px {olcek}px no-repeat">' \
           f'<span class="mk"></span></div>'


def s08():
    kart_ = ""
    for j in V.JOB:
        sev = "".join(f'<span class="ch">{l}</span>' for l in j[8])
        yerler = ""
        for irk, harita, xz, no in (("Karus", "Luferson Castle", j[3], "1"), ("El Morad", "El Morad Castle", j[4], "2")):
            if xz:
                yerler += f'<div class="yr">{mini(no, xz)}<div class="yl"><b>{irk}</b><br>{harita}<br><span>{xz[0]},{xz[1]}</span></div></div>'
        kart_ += f'<div class="nk" style="--r:{JOB_RENK[j[0]]}"><div class="jb">{j[0]}</div><div class="nn">{e(j[2])}</div>' \
                 f'<div class="et">MASTER + SKILL NPC\'N</div><div class="vr"><span class="ch m">Master</span>{sev}</div><div class="yrs">{yerler}</div></div>'
    css = f""".gr{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.nk{{background:#1d1712;border:1px solid #3a2e20;border-top:4px solid var(--r);border-radius:10px;padding:12px}}
.jb{{font-size:22px;font-weight:900;color:var(--r)}} .nn{{font-size:16px;font-weight:800;color:{ALTIN2};margin:2px 0 6px}}
.et{{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1px;color:#1b1400;background:{ALTIN};border-radius:4px;padding:2px 7px}}
.vr{{margin:8px 0 10px;display:flex;flex-wrap:wrap;gap:5px}} .ch{{font-size:12.5px;font-weight:800;color:#e8dcc8;background:#2c231a;border:1px solid #6b5426;border-radius:5px;padding:2px 7px}}
.ch.m{{color:#1b1400;background:{ALTIN2};border-color:{ALTIN2}}}
.yrs{{display:flex;flex-direction:column;gap:8px}} .yr{{display:flex;gap:10px;align-items:center}}
.mm{{position:relative;flex:none;border:2px solid #6b5426;border-radius:6px;background-color:#000}}
.mk{{position:absolute;left:50%;top:50%;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;background:var(--r);border:3px solid #fff;box-shadow:0 0 0 2px #000,0 0 12px #000}}
.yl{{font-size:13px;line-height:1.45;color:#d9cdb8}} .yl b{{color:#e8dcc8;font-size:14px}} .yl span{{color:{ALTIN2};font-weight:800;font-size:15px}}"""
    return kart(f'<div class="gr">{kart_}</div><div class="alt2">Ayrı bir skill NPC\'si <b>yok</b> — master görevini de 70 – 80 skill görevlerini de <b>aynı NPC</b> verir · koordinatlar oyun içi x,y</div>',
                "📍 JOB'UNUN NPC'Sİ — MASTER + SKILL", "Kendi job'unu bul → NPC'sinin adı ve <b>haritadaki yeri</b> burada", ek_css=css)


# ---------- S09 Narki (patron 6 Eki: "tam anlat")
def s09():
    MK = 300
    n = V.NARKI_NPC
    dots = "".join(f'<div class="nd" style="left:{x / 1024 * MK:.1f}px;top:{(1 - z / 1024) * MK:.1f}px"></div>' for x, z in n["nokta"])
    adim = ["Moradon'daki <b>[Mysterious] Narki</b>'ye git, konuş",
            "Takını ver (<b>tek adet</b>) — eski takı ya da normal takı",
            "Takı <b>yok olur</b>, karşılığında <b>1 ödül</b> çekilir",
            "Ne çıkacağını takının <b>girdiği havuz</b> belirler ↓"]
    tr = lambda x, f="g": format(x, f).replace(".", ",")
    ornek = {4: ["Old Agate Earring", "Old Amulet of Strength"], 5: ["Warrior Pendant", "Taurus Ring"]}
    havuz = ""
    for no, renk in ((4, "#ffb03a"), (5, "#4fd1ff")):
        h = V.NARKI_VERI["havuz"][str(no)]; ssp, kutu = V.narki_havuz(no)
        assert all(o in h["ornek"] for o in ornek[no]), no
        enb = max([p for _, p in ssp] + [kutu[1]])
        sat = "".join(f'<div class="br"><span class="ba">{a} adet</span><span class="bb"><i style="width:{p / enb * 100:.0f}%;background:{renk}"></i></span>'
                      f'<span class="bp">%{tr(p)}</span></div>' for a, p in ssp)
        sat += f'<div class="br kt"><span class="ba">Kutu</span><span class="bb"><i style="width:{kutu[1] / enb * 100:.0f}%;background:#6b5d4a"></i></span><span class="bp">%{tr(kutu[1])}</span></div>'
        havuz += f'<div class="hv" style="--r:{renk}"><div class="ht">{h["ad"].upper()} HAVUZU</div><div class="hs">{h["esya"]} çeşit takı · ör. {e(", ".join(ornek[no]))} …</div>' \
                 f'{ik(V.SSP, 30)} <b class="sp">Spell Stone Powder</b>{sat}<div class="or">ortalama ≈ <b>{tr(V.narki_ort(no), ".1f")}</b> adet / kırdırma · Kutu = {kutu[0]}</div></div>'
    css = f""".ust{{display:flex;gap:16px;margin-bottom:14px}}
.map{{position:relative;width:{MK}px;height:{MK}px;flex:none;background:url({minimap("3")}) center/100% 100%;border:2px solid #6b5426;border-radius:6px}}
.nd{{position:absolute;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:{ALTIN};border:2px solid #fff;box-shadow:0 0 0 2px #000,0 0 10px #000}}
.ne{{flex:1}} .ne h3{{margin:0 0 6px;color:{ALTIN};font-size:17px;letter-spacing:1px}} .ne .np{{font-size:15px;margin-bottom:12px}} .ne .np b{{color:{ALTIN2}}} .ne .np span{{color:{GRI};font-size:13px}}
.st{{display:flex;gap:10px;align-items:flex-start;margin:0 0 9px;font-size:15px}} .st .no{{flex:none;width:26px;height:26px;border-radius:50%;background:{ALTIN};color:#1b1400;font-weight:900;display:flex;align-items:center;justify-content:center}}
.st b{{color:{ALTIN2}}}
.hg{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.hv{{background:#1d1712;border:1px solid #3a2e20;border-top:3px solid var(--r);border-radius:10px;padding:12px 14px}}
.ht{{font-size:17px;font-weight:900;color:var(--r);letter-spacing:.5px}} .hs{{font-size:12.5px;color:{GRI};margin:2px 0 8px}}
.sp{{color:#e8dcc8;font-size:14px;vertical-align:middle}}
.br{{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:14px}} .ba{{width:58px;color:#e8dcc8}} .bb{{flex:1;height:12px;background:#0d0a08;border-radius:6px;overflow:hidden}}
.bb i{{display:block;height:100%;border-radius:6px}} .bp{{width:58px;text-align:right;color:{ALTIN2};font-weight:800}} .kt .ba,.kt .bp{{color:{GRI};font-weight:600}}
.or{{margin-top:8px;font-size:14px;color:{GRI}}} .or b{{color:{ALTIN2};font-size:18px}}
.ku{{margin-top:12px;font-size:13px;color:{GRI};text-align:center}} .ku b{{color:#ff8a7a}}"""
    nokta = " · ".join(f"{x},{z}" for x, z in n["nokta"])
    g = f'<div class="ust"><div class="map">{dots}</div><div class="ne"><h3>NEREDE</h3><div class="np"><b>Moradon</b> · <b>{e(n["ad"])}</b> — 4 tane, hepsi aynı işi yapar<br><span>{nokta}</span></div>' \
        f'<h3>NASIL</h3>' + "".join(f'<div class="st"><span class="no">{i}</span><span>{a}</span></div>' for i, a in enumerate(adim, 1)) + '</div></div>' \
        f'<div class="hg">{havuz}</div><div class="ku">⚠ Bağlı, kiralık, mühürlü ya da süreli eşya <b>verilemez</b> · kırdırma <b>geri alınamaz</b> · envanterinde <b>boş yer</b> olmalı · takın hangi havuza giriyor: rehber → Narki Kırdırma → ara</div>'
    return kart(g, "♻️ NARKİ İLE SPELL STONE POWDER", "Kullanmadığın takıyı Narki'ye ver → <b>1 – 5 adet Spell Stone Powder</b> çıkar", ek_css=css)


# ---------- S07 Ronark Land
def s07():
    renk = {"8401": "#ff5c5c", "8402": "#ff5c5c", "8403": "#ff5c5c", "8404": "#ff5c5c", "1402": "#ffb03a", "1311": "#4fd1ff"}
    isaret = "".join(f'<div class="bm" style="left:{l / 100 * HK:.1f}px;top:{t / 100 * HK:.1f}px;background:{renk[c]}"></div>'
                     for c in V.SSP_MOB for l, t in V.nokta(c))
    dort = V.SSP_MOB[:4]
    legend = f'<div class="lg"><span class="bd" style="background:#ff5c5c"></span><div><b>{" · ".join(e(V.CANAVAR[c]["ad"]) for c in dort)}</b>' \
             f'<div class="xz">Lv {V.lv(dort[0])} · Spell Stone %{V.ssp_oran(dort[0]):g} · her biri 2 nokta</div></div></div>'
    for c in V.SSP_MOB[4:]:
        legend += f'<div class="lg"><span class="bd" style="background:{renk[c]}"></span><div><b>{e(V.CANAVAR[c]["ad"])}</b>' \
                  f'<div class="xz">Lv {V.lv(c)} · Spell Stone %{V.ssp_oran(c):g} · {len(V.nokta(c))} nokta</div></div></div>'
    css = f""".hw{{display:flex;gap:16px;align-items:flex-start}}
.map{{position:relative;width:{HK}px;height:{HK}px;flex:none;background:url({minimap("11")}) center/100% 100%;border:2px solid #6b5426;border-radius:6px}}
.bm{{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;border:2px solid #000;box-shadow:0 0 6px #000}}
.leg{{flex:1;font-size:14px}} .lg{{display:flex;gap:8px;align-items:center;margin:0 0 12px}} .lg b{{color:#e8dcc8}}
.bd{{flex:none;width:14px;height:14px;border-radius:50%;border:2px solid #000}} .xz{{font-size:12px;color:{GRI}}}"""
    return kart(f'<div class="hw"><div class="map">{isaret}</div><div class="leg">{legend}</div></div>'
                f'<div class="alt2">Noktalar oyun içi rehberin (sexyko.com/guide) spawn kayıtlarından</div>',
                "🗺️ RONARK LAND — SPELL STONE MOBLARI", "Ortadaki halka: <b>Atross · Lyot</b> · iki yandaki tepeler: <b>Hellfire · Enigma · Havoc · Cruel</b>", ek_css=css)


KARTLAR = [("S00_yol_haritasi.jpg", s00), ("S01_master_tablo.jpg", s01), ("S02_master_item.jpg", s02), ("S03_harita_karus.jpg", lambda: harita("karus")),
           ("S04_harita_elmorad.jpg", lambda: harita("elmorad")), ("S05_skill_gorev.jpg", s05), ("S06_spell_stone.jpg", s06),
           ("S07_harita_ronark.jpg", s07), ("S08_npc.jpg", s08), ("S09_narki.jpg", s09)]

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=1)
        for ad, f in KARTLAR:
            pg.set_content(f(), wait_until="load")
            tas = pg.evaluate("(()=>{const k=document.querySelector('#kart'),kr=k.getBoundingClientRect().right;let m=0;k.querySelectorAll('*').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().right)});return [kr,m,k.scrollWidth,k.clientWidth]})()")
            assert tas[1] <= tas[0] + 1 and tas[2] <= tas[3] + 1, (ad, "yazi kartin disina tasiyor", tas)   # 7 Eki: buyuk font -> tasma olmasin
            pg.locator("#kart").screenshot(path=os.path.join(RD, ad), type="jpeg", quality=90)
            print(ad, os.path.getsize(os.path.join(RD, ad)) // 1024, "KB")
        b.close()

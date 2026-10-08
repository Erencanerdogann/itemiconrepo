# -*- coding: utf-8 -*-
# FORUM KONULARINI BIZIM TEMAYLA YENIDEN INSA (patron 8 Eki: "butun forum konularini bizim temamiza gore yeniden insa et, butun hepsini, html'de gorucem").
# Girdi: forum_bbcode/bbcode.json (forum HTML'i). Cikti: _konu_blok blok listesi (banner · baslik · icindekiler · numarali bolumler · ayrac · 18 px yazi · not · son)
# ICERIK KONUNUN KENDISI: her cumle / resim kaynaktan; uydurma yok. Eklenen tek sey yapi (bolum numarasi, icindekiler, baglantilar). Kirik resim cikarilir -> KONTROL.
# Test: insa() her konuda kaynaktaki her satirin yazisi yeni BBCode'da var mi (dogrula()).
import re, html
from html.parser import HTMLParser

EMOJI = re.compile(r"^((?:[\U0001F000-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿〰〽㊗㊙©®‼⁉™ℹⓂ▪-◾]"
                   r"[️‍\U0001F3FB-\U0001F3FF⃣]*)+)\s*")
NUMARA = re.compile(r"^\s*(?:\d{1,2}|[0-9]️?⃣)\s*(?:[—–\-)]|\.(?!\d)|:(?!\d))\s*")   # 8 Eki: "12:00" / "10.000" numara sanilip kesiliyordu       # "01 — ", "1) ", "1️⃣ "
MADDE = re.compile(r"^\s*(?:[•●▪◆◇►▶➤➜→🔸🔹]|-\s|\*\s)\s*")     # ✅ / ✔ / ❌ madde DEGIL — emojisiyle satir kalir (8 Eki d/10)


class Satirlar(HTMLParser):
    """contentHtml -> satir listesi: {'t': 'yazi'|'img'|'hr'|'h', 'md': satir ici (**kalin**, [[url|metin]]), 'duz': yazi, 'kalin': tamami kalin mi, 'px': en buyuk font, 'hn': h seviyesi, 'li': madde mi}"""
    BLOK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "ul", "ol", "tr"}

    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.L = []; s.md = ""; s.duz = ""; s.kalin_harf = 0; s.harf = 0; s.px = 0; s.b = 0; s.a = None; s.hn = 0; s.li = 0; s.pxs = []

    def bitir(s):
        d = re.sub(r"\s+", " ", s.duz).strip()
        if d:
            m = re.sub(r"\s+", " ", s.md).strip()
            m = re.sub(r"\*\*\s*\*\*", "", m)
            s.L.append({"t": "h" if s.hn else "yazi", "md": m, "duz": d, "kalin": s.harf > 0 and s.kalin_harf >= s.harf * 0.9, "px": s.px, "hn": s.hn, "li": bool(s.li)})
        s.md = s.duz = ""; s.kalin_harf = s.harf = 0; s.px = 0

    def handle_starttag(s, t, at):
        at = dict(at)
        if t in s.BLOK or t == "br": s.bitir()
        if t in ("b", "strong"):
            if s.b == 0: s.md += "**"
            s.b += 1
        elif t in ("h1", "h2", "h3", "h4", "h5", "h6"): s.hn = int(t[1])
        elif t == "li": s.li += 1
        elif t == "span":
            m = re.search(r"font-size:\s*(\d+)px", at.get("style", ""))
            s.pxs.append(int(m.group(1)) if m else None)
        elif t == "a": s.a = at.get("href", ""); s.md += "[["
        elif t == "img":
            if "emoji" in at.get("class", ""):
                x = at.get("alt", ""); s.md += x; s.duz += x
            else:
                s.bitir(); s.L.append({"t": "img", "src": at.get("src", ""), "alt": at.get("alt", "")})
        elif t == "hr": s.bitir(); s.L.append({"t": "hr"})

    def handle_endtag(s, t):
        if t in ("b", "strong"):
            s.b = max(0, s.b - 1)
            if s.b == 0: s.md += "**"
        elif t == "a":
            if s.a is not None:
                s.md = s.md.rsplit("[[", 1); metin = s.md[1] if len(s.md) > 1 else ""
                s.md = s.md[0] + (f"[[{s.a}|{metin.strip()}]]" if metin.strip() and metin.strip() != s.a else f"[[{s.a}|{s.a}]]")
            s.a = None
        elif t == "span" and s.pxs: s.pxs.pop()
        if t in s.BLOK: s.bitir()
        if t in ("h1", "h2", "h3", "h4", "h5", "h6"): s.hn = 0
        if t == "li": s.li = max(0, s.li - 1)

    def handle_data(s, x):
        x = x.replace("\n", " ")
        if not x.strip(): s.md += x; s.duz += x; return
        if "**" in x: x = x.replace("**", "∗∗")
        s.md += x; s.duz += x
        n = sum(1 for c in x if c.isalnum())
        s.harf += n
        if s.b: s.kalin_harf += n
        p = [v for v in s.pxs if v]
        if p and n: s.px = max(s.px, p[-1])


def satirlar(h):
    p = Satirlar(); p.feed(h); p.close(); p.bitir()
    return p.L


AYRAC = re.compile(r"^[\s━─═_\-–—=~•·*]{6,}$")


def emoji_ayir(s):
    m = EMOJI.match(s)
    return (m.group(1), s[m.end():].strip()) if m else ("", s.strip())


def buyuk_mu(s):
    h = [c for c in s if c.isalpha()]
    return bool(h) and sum(c.isupper() for c in h) / len(h) >= 0.7


def emojili_kisa(x): return x["t"] == "yazi" and bool(EMOJI.match(x["duz"])) and len(x["duz"]) <= 60


def insa(k, kirik=()):
    """forum konusu (bbcode.json kaydi) -> (B bloklari, RES {id: (dosya, aciklama, url)}, KONTROL notlari)"""
    m0 = k["mesajlar"][0]
    L = satirlar(m0["html"])
    kontrol, RES, B = [], {}, []
    # --- 1) ayrac satirlari (━━━) -> hr (8 Eki: once filtre onlari siliyordu, d/10 bolumsuz kaliyordu); sonra harfsiz bos satirlar atilir
    for x in L:
        if x["t"] == "yazi" and AYRAC.match(x["duz"]): x["t"] = "hr"
    L = [x for x in L if not (x["t"] == "yazi" and not re.sub(r"[\W_]", "", x["duz"]) and not EMOJI.match(x["duz"]))]
    # --- 2) ust baslik + alt baslik = konunun ILK yazi satiri (+ hemen arkasindaki kisa kalin / buyuk satir) — bolum sayilmaz
    idx = [i for i, x in enumerate(L) if x["t"] not in ("img", "hr")]
    kullan, ust, alt = set(), None, ""
    if idx:
        t0 = idx[0]; x = L[t0]
        if len(x["duz"]) <= 90 and not x["li"] and (x["t"] == "h" or x["kalin"] or buyuk_mu(x["duz"]) or x["px"]):
            ust = x; kullan.add(t0)
            t1 = next((i for i in idx if i > t0), None)
            if t1 is not None and t1 - t0 <= 2:
                y = L[t1]
                if len(y["duz"]) <= 90 and not y["li"] and y["hn"] in (0, 3, 4, 5, 6) and (y["kalin"] or buyuk_mu(y["duz"])) and not NUMARA.match(emoji_ayir(y["duz"])[1]):
                    alt = y["md"].replace("**", "").strip(); kullan.add(t1)
    ust_metin = emoji_ayir(ust["duz"])[1] if ust else emoji_ayir(k["baslik"])[1]
    # --- 3) bolum (h) / ara baslik (ara)
    for i, x in enumerate(L):
        if x["t"] == "h": x["t"] = "h" if x["hn"] in (1, 2) else "ara"
    hn_var = any(x.get("hn") in (1, 2) for i, x in enumerate(L) if i not in kullan)
    numarali = {i for i, x in enumerate(L) if i not in kullan and x["t"] in ("yazi", "h", "ara") and not x["li"] and len(x["duz"]) <= 80
                and NUMARA.match(emoji_ayir(x["duz"])[1]) and (x["kalin"] or x["hn"] or buyuk_mu(x["duz"]))}
    pxs = sorted({x["px"] for x in L if x["t"] == "yazi" and x["px"]})
    for i, x in enumerate(L):
        if i in kullan or x["t"] not in ("yazi", "h", "ara") or x["li"] or len(x["duz"]) > 80: continue
        if hn_var:                                                     # once acik markdown basliklari (H1/H2 bolum, H3+ ara) — d/45 "1. Bolum" satirlari bolum sanilmasin
            if x["t"] == "yazi" and x["kalin"] and buyuk_mu(x["duz"]) and len(x["duz"]) <= 60: x["t"] = "ara"
        elif numarali:
            if i in numarali: x["t"] = "h"
            elif x["t"] == "h": x["t"] = "ara"
            elif x["t"] == "yazi" and x["kalin"] and buyuk_mu(x["duz"]): x["t"] = "ara"
        elif x["t"] == "yazi" and EMOJI.match(x["duz"]) and x["duz"].rstrip().endswith(":") and len(x["duz"]) <= 40 and buyuk_mu(x["duz"]):
            x["t"] = "ara"                                                # "⚡ KISACA:" gibi
        elif x["t"] == "yazi":
            once_hr = i == 0 or L[i - 1]["t"] == "hr"
            sonraki = L[i + 1:i + 3]
            liste_akisi = emojili_kisa(x) and len(sonraki) == 2 and all(emojili_kisa(y) for y in sonraki) and not x["kalin"]
            if once_hr and i + 1 < len(L) and (EMOJI.match(x["duz"]) or buyuk_mu(x["duz"])) and not liste_akisi and L[i + 1]["t"] != "hr": x["t"] = "h"
            elif x["kalin"] and (EMOJI.match(x["duz"]) or buyuk_mu(x["duz"])) and len(x["duz"]) <= 60:
                x["t"] = "h" if (x["px"] and pxs and x["px"] >= pxs[-1] - 2 and len(pxs) > 1) else "ara"
    ilk_h = next((i for i, x in enumerate(L) if x["t"] == "h" and i not in kullan), len(L))
    afis = L[0]["src"] if L and L[0]["t"] == "img" and L[0]["src"] not in kirik else None
    # --- 3) son satir (slogan) -> kirmizi kapanis
    son = None
    j = len(L) - 1
    while j >= 0 and L[j]["t"] in ("hr", "img"): j -= 1
    if j > ilk_h and L[j]["t"] in ("yazi", "ara", "h") and len(L[j]["duz"]) <= 80 and not L[j]["li"] and (EMOJI.match(L[j]["duz"]) or L[j]["kalin"] or buyuk_mu(L[j]["duz"])):
        son = L[j]["duz"]; kullan.add(j)
    # --- 4) bloklar
    rn = [0]
    def resim(src, acik=""):
        if src in kirik:
            kontrol.append(f"⚠ **Kırık resim çıkarıldı:** {src} (404) — yeni ekran görüntüsü gerekir."); return None
        rn[0] += 1; rid = f"F{rn[0]:02d}"; RES[rid] = (None, acik or f"forumdaki {rn[0]}. resim", src); return rid
    if afis: kullan.add(0); B.append(("afis", resim(afis, "konu afişi")))
    else: B.append(("banner", "R01"))
    B.append(("baslik", ust_metin, alt or "SexyKO Oyun Rehberi"))
    govde = []          # (tur, ...) — bolum baslıkları dahil
    tampon = []
    def bosalt():
        if not tampon: return
        satir = []
        for y in tampon:
            if satir and not re.search(r"[.!?:…)\]»\"']$|\*\*$", satir[-1]) and y and (y[0].islower() or y[:2] == "**" and y[2:3].islower()):
                satir[-1] += " " + y
            else: satir.append(y)
        govde.append(("p", satir[0]) if len(satir) == 1 else ("satirlar", satir)); tampon.clear()
    liste = []
    def liste_bosalt():
        if liste: govde.append(("liste", list(liste))); liste.clear()
    for i, x in enumerate(L):
        if i in kullan: continue
        t = x["t"]
        if t == "hr": bosalt(); liste_bosalt(); continue
        if t == "img":
            bosalt(); liste_bosalt(); rid = resim(x["src"])
            if rid: govde.append(("img", rid, "")); continue
            continue
        if t == "h":
            bosalt(); liste_bosalt()
            e, m = emoji_ayir(x["duz"]); m = NUMARA.sub("", m).rstrip(":").strip()
            govde.append(("h", e or "🔹", m)); continue
        if t == "ara":
            bosalt(); liste_bosalt(); govde.append(("ara", x["md"].replace("**", "").strip())); continue
        md = x["md"]
        if x["li"] or MADDE.match(x["duz"]):
            bosalt(); liste.append(MADDE.sub("", md.replace("** ", "**", 1) if md.startswith("** ") else md).strip()); continue
        liste_bosalt(); tampon.append(md)
    bosalt(); liste_bosalt()
    # bolumsuz giris -> "BIR BAKISTA"; bos bolum basligi (arkasi hemen yeni baslik) -> ara baslik
    if govde and govde[0][0] != "h": govde.insert(0, ("h", "🔎", "BİR BAKIŞTA"))
    for n in range(len(govde) - 1):
        if govde[n][0] == "h" and govde[n + 1][0] == "h": govde[n] = ("ara", f"{govde[n][1]} {govde[n][2]}")
    if govde and govde[-1][0] == "h": govde[-1] = ("ara", f"{govde[-1][1]} {govde[-1][2]}")
    B.append(("icindekiler",)); B.append(("ayrac",))
    for g in govde:
        if g[0] == "h" and B[-1][0] != "ayrac": B.append(("ayrac",))
        B.append(g)
    B.append(("ayrac",))
    B.append(("h", "🔗", "BAĞLANTILAR"))
    B.append(("liste", ["🌐 Web: [[https://www.sexyko.com|www.sexyko.com]]",
                        f"💬 Discord: [[https://discord.gg/sexyko|discord.gg/sexyko]] · Forum: [[{k['url']}|forum.sexyko.com/d/{k['id']}]]"]))
    B.append(("ayrac",))
    B.append(("son", son or f"🔥 {ust_metin} 🔥"))
    return B, RES, kontrol


def _norm(s): return re.sub(r"[\W_]+", "", s.replace("∗∗", "")).lower()


def dogrula(k, bb, kirik=()):
    """kaynaktaki her yazi satiri yeni BBCode'da var mi (yapi disi kayip yok) + her saglam resim linki var mi -> (eksik satirlar, eksik resimler)"""
    duz = _norm(re.sub(r"\[/?(?:B|I|U|S|CENTER|LIST|QUOTE|CODE|SIZE|COLOR|URL|IMG)(?:=[^\]]*)?\]|\[\*\]", "", bb))   # sadece BBCode etiketi (8 Eki: [10M] / [Teleport] metni de siliniyordu)
    eksik = []
    for x in satirlar(k["mesajlar"][0]["html"]):
        if x["t"] == "img":
            continue
        n = _norm(NUMARA.sub("", emoji_ayir(MADDE.sub("", x["duz"]))[1])) if x["t"] != "hr" else ""
        if n and n not in duz: eksik.append(x["duz"][:70])
    rs = [x["src"] for x in satirlar(k["mesajlar"][0]["html"]) if x["t"] == "img" and x["src"] not in kirik]
    return eksik, [u for u in rs if u not in bb]


if __name__ == "__main__":
    import sys, json, os
    sys.stdout.reconfigure(encoding="utf-8")
    B = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "forum_bbcode", "bbcode.json"), encoding="utf-8"))
    if "--hepsi" in sys.argv:                                              # 38 konu: ozet + butunluk testi
        import _konu_blok as KB, _forum_sekme as FS
        kotu = 0
        for k in B["konular"]:
            if k["id"] in FS.BIZIM: continue
            kir = set(k.get("kirik_url") or [])
            Bl, RES, KN = insa(k, kir)
            bb = re.sub(r"\{\{(F\d+)\}\}", lambda m: RES[m.group(1)][2], KB.bb(Bl))
            ek, er = dogrula(k, bb, kir)
            kotu += bool(ek or er)
            hs = [b[2] for b in Bl if b[0] == "h"]
            print(f"d/{k['id']:<3} bölüm {len(hs):>2} · ara {sum(1 for b in Bl if b[0] == 'ara'):>2} · resim {len(RES):>2} · bb {len(bb):>5} · {'✅' if not (ek or er) else '❌ eksik ' + str(len(ek)) + '/' + str(len(er))} · {' | '.join(hs)[:110]}")
            for e in ek[:3] + er[:2]: print("      eksik:", e)
        print("sorunlu konu:", kotu); sys.exit(1 if kotu else 0)
    for did in [int(x) for x in sys.argv[1:]]:
        k = next(k for k in B["konular"] if k["id"] == did)
        print("=====", did, k["baslik"])
        for x in satirlar(k["mesajlar"][0]["html"]):
            if x["t"] == "img": print("  [IMG]", x["src"][-40:]); continue
            if x["t"] == "hr": print("  ----"); continue
            print(f"  {'H'+str(x['hn']) if x['hn'] else '  '} {'K' if x['kalin'] else ' '} {x['px'] or '':>2} {'•' if x['li'] else ' '} {x['duz'][:90]}")

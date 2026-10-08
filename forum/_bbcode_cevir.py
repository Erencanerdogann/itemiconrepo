# -*- coding: utf-8 -*-
# FORUM HTML -> BBCODE CEVIRICI (patron 8 Eki: "butun konularin bbcode'sini cikart, html'de dursunlar").
# Flarum herkese acik API ham BBCode'u (content) VERMEZ, sadece contentHtml verir (canEdit=false) -> s9e TextFormatter ciktisi geri cevrilir.
# Cikti forumda AYNI gorunur (birebir ayni metin degil): [B] <-> <b>/<strong>, [SIZE=n] <-> font-size:npx, [COLOR] , [CENTER], [IMG], [URL], [LIST], [QUOTE], [CODE], # baslik, ---.
# TEST: python _bbcode_cevir.py  -> bizim yazdigimiz konular (d/54 odul, d/56 skill, d/57 sezon): forum HTML'i -> BBCode == bizim BBCode dosyamiz (yazi + etiket sirasi).
import html, re
from html.parser import HTMLParser

BLOK = {"p", "div", "ul", "ol", "li", "blockquote", "pre", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "table", "details"}
TEK = {"br", "img", "hr"}


class _Dugum:
    def __init__(s, ad, at=None, ust=None):
        s.ad, s.at, s.ust, s.c = ad, dict(at or []), ust, []


class _Agac(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.kok = _Dugum("#kok"); s.su = s.kok

    def handle_starttag(s, t, at):
        d = _Dugum(t, at, s.su); s.su.c.append(d)
        if t not in TEK: s.su = d

    def handle_startendtag(s, t, at):
        s.su.c.append(_Dugum(t, at, s.su))

    def handle_endtag(s, t):
        d = s.su
        while d is not s.kok and d.ad != t: d = d.ust
        if d is not s.kok: s.su = d.ust

    def handle_data(s, x):
        s.su.c.append(x)


def _stil(at):
    return {k.strip(): v.strip() for k, v in (p.split(":", 1) for p in at.get("style", "").split(";") if ":" in p)}


class Cevir:
    def __init__(s): s.bilinmeyen = set()

    def satir_ici(s, n):
        if isinstance(n, str): return n.replace("\r", "").replace("\n", "")
        a = n.ad; ic = lambda: "".join(s.satir_ici(x) for x in n.c)
        if a == "br": return "\n"
        if a in ("b", "strong"): return f"[B]{ic()}[/B]"
        if a in ("i", "em"): return f"[I]{ic()}[/I]"
        if a in ("u", "ins"): return f"[U]{ic()}[/U]"
        if a in ("s", "del", "strike"): return f"[S]{ic()}[/S]"
        if a == "code": return f"`{ic()}`"
        if a == "img":
            if "emoji" in n.at.get("class", ""): return n.at.get("alt", "")
            return f"[IMG]{n.at.get('src', '')}[/IMG]"
        if a == "a":
            h, t = n.at.get("href", ""), ic()
            return f"[URL]{h}[/URL]" if t == h else f"[URL={h}]{t}[/URL]"
        if a == "span":
            st, t = _stil(n.at), ic()
            for k, v in reversed(list(st.items())):                       # stil sirasi = ic ice sira
                if k == "font-size" and v.endswith("px"): t = f"[SIZE={v[:-2]}]{t}[/SIZE]"
                elif k == "color": t = f"[COLOR={v}]{t}[/COLOR]"
                else: s.bilinmeyen.add(f"span {k}")
            return t
        if a in BLOK: return s.blok(n)
        s.bilinmeyen.add(a); return ic()

    def bloklar(s, n):
        """Kapsayicinin cocuklari: bloklar arasi bos satir; bloklar arasindaki satir-ici parcalar birlestirilir."""
        o, satir = [], ""
        for x in n.c:
            if isinstance(x, str) and not x.strip() and not satir: continue
            if not isinstance(x, str) and x.ad in BLOK:
                if satir.strip(): o.append(satir.strip("\n"))
                satir = ""; o.append(s.blok(x))
            else: satir += s.satir_ici(x)
        if satir.strip(): o.append(satir.strip("\n"))
        return "\n\n".join(b for b in o if b != "")

    def blok(s, n):
        a = n.ad
        if a == "p": return "".join(s.satir_ici(x) for x in n.c)
        if a == "div":
            ic = s.bloklar(n)
            return f"[CENTER]{ic}[/CENTER]" if _stil(n.at).get("text-align") == "center" else ic
        if a in ("ul", "ol"):
            li = [s.bloklar(x) for x in n.c if not isinstance(x, str) and x.ad == "li"]
            return ("[LIST=1]" if a == "ol" else "[LIST]") + "".join(f"\n[*]{x}" for x in li) + "\n[/LIST]"
        if a == "li": return s.bloklar(n)
        if a == "blockquote": return f"[QUOTE]{s.bloklar(n)}[/QUOTE]"
        if a == "pre": return "[CODE]" + html.unescape("".join(x if isinstance(x, str) else "".join(y for y in x.c if isinstance(y, str)) for x in n.c)) + "[/CODE]"
        if a in ("h1", "h2", "h3", "h4", "h5", "h6"): return "#" * int(a[1]) + " " + "".join(s.satir_ici(x) for x in n.c)
        if a == "hr": return "---"
        s.bilinmeyen.add(a); return s.bloklar(n)


def cevir(h):
    """contentHtml -> (bbcode, bilinmeyen_etiketler)"""
    ag = _Agac(); ag.feed(h); ag.close()
    c = Cevir(); return c.bloklar(ag.kok), sorted(c.bilinmeyen)


# ---------- karsilastirma (test + rapor)
ETIKET = re.compile(r"\[(?:/?(?:B|I|U|S|CENTER|LIST|QUOTE|CODE)|\*|/SIZE|/COLOR|/URL|/IMG|SIZE=[^\]]+|COLOR=[^\]]+|URL(?:=[^\]]+)?|IMG|LIST=1)\]")


def kanonik(bb):
    """BBCode -> (sadece yazi, bosluksuz) + etiket sirasi. Ayni gorunen iki BBCode'un kanonigi esittir."""
    bb = re.sub(r"(?<![*\w])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![*\w])", r"[I]\1[/I]", bb)       # Markdown *italik* == [I] (forumda ikisi de <em>)
    bb = re.sub(r"\.[0-9a-f]{8}\.(png|jpe?g|gif)\b", r".\1", bb)                          # icerik ozetli resim adi == eski ad (ayni resim, 7 Eki jsDelivr onlemi)
    et = ETIKET.findall(bb)
    yazi = re.sub(r"\s+", "", ETIKET.sub("", bb))
    return yazi, et


if __name__ == "__main__":
    import sys, os, json, urllib.request
    sys.stdout.reconfigure(encoding="utf-8")
    KOK = os.path.dirname(os.path.abspath(__file__))
    TEST = [(54, "odul/ODUL_KONU_bbcode_flarum.txt"), (56, "skill_master/SKILL_KONU_bbcode_flarum.txt"), (57, "sezon/SEZON_KONU_bbcode_flarum.txt"),
            (58, "mining/MINING_KONU_bbcode_flarum.txt"), (16, "genie/GENIE_KONU_bbcode_flarum.txt"), (37, "yayinci/YAYINCI_KONU_bbcode_flarum.txt"),
            (51, "pus_kupon/PUS_KONU_bbcode_flarum.txt"), (55, "teamspeak/TS_KONU_bbcode_flarum.txt")]   # bizim yazip foruma yuklenen 8 konu
    hata = 0
    for no, dosya in TEST:
        r = urllib.request.urlopen(urllib.request.Request(f"https://forum.sexyko.com/api/posts?filter[discussion]={no}&page[limit]=50", headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
        posts = [p for p in json.load(r)["data"] if p["attributes"].get("contentType") == "comment"]
        posts.sort(key=lambda p: p["attributes"]["number"])
        bb_forum = "\n\n".join(cevir(p["attributes"]["contentHtml"])[0] for p in posts[:2])       # konu 1-2 mesaj (ilk yazar mesajlari)
        bizim = open(os.path.join(KOK, *dosya.split("/")), encoding="utf-8").read().split("\n", 2)[2]   # 1. satir baslik + bos satir
        y1, e1 = kanonik(bb_forum); y2, e2 = kanonik(bizim)
        ok = (y1 == y2 and e1 == e2)
        if not ok:
            hata += 1
            i = next((k for k in range(min(len(y1), len(y2))) if y1[k] != y2[k]), min(len(y1), len(y2)))
            j = next((k for k in range(min(len(e1), len(e2))) if e1[k] != e2[k]), min(len(e1), len(e2)))
            print(f"  yazi farki @{i}: forum …{y1[max(0, i-40):i+40]}… | bizim …{y2[max(0, i-40):i+40]}…")
            print(f"  etiket farki @{j}: forum {e1[j:j+4]} | bizim {e2[j:j+4]}")
        print(f"d/{no}: mesaj {len(posts)} · yazi {len(y1)}/{len(y2)} · etiket {len(e1)}/{len(e2)} · {'AYNI ✅' if ok else 'FARKLI ❌'}")
    sys.exit(1 if hata else 0)

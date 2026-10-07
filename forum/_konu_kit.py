# -*- coding: utf-8 -*-
# FORUM KONU KITI (patron 3 Eki: "baska forum sitelerine uyelik alip yeni konular acacagim, taslagi resimleri oldugu gibi kopyalayamayacagim, yardimin lazim")
# KAYNAK: Ko-Yardim tanitim konusu (11734, SexyKO hesabi, 30 Eyl 2026) — SADECE OKUNUR, foruma hicbir sey yazilmaz
#   kaynak/koyardim_11734.html  = misafir HTML (requests) · kaynak/linkler.json = giris yapilmis Chrome'dan cozulen 38 gizli link (sirali)
# CIKTI: SEXYKO_TANITIM_bbcode.txt (XenForo / vBulletin / MyBB) · _markdown.md (Flarum vb.) · _duz.txt · resim/ (5 resim) · ../HTML/FORUM_KONU.html
# Kurallar: Ko-Yardim'in kelimelere otomatik ekledigi kendi linkleri (ko-yardim.com/ ve tanitim forumu .90) atilir, metin kalir ·
#           71 emoji resmi -> emoji karakteri · 5 resim [IMG] olarak Ko-Yardim ek dosyasina bagli (baska forum Referer'i ile 200 olculdu)
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, requests
from html.parser import HTMLParser

KOK = os.path.dirname(os.path.abspath(__file__))
KAY = os.path.join(KOK, "kaynak")
S = open(os.path.join(KAY, "koyardim_11734.html"), encoding="utf-8").read()
LINK = json.load(open(os.path.join(KAY, "linkler.json"), encoding="utf-8"))["linkler"]
KONU_URL = "https://ko-yardim.com/konu/sexyko-beta-16-10-2026-2010dan-beri-16-yillik-efsane-essiz-gercek-v2-64bit-client.11734/"

# --- baslik + ilk mesaj
bas = re.search(r'<h1 class="p-title-value">(.*?)</h1>', S, re.S).group(1)
bas = re.sub(r'<span class="label-append">.*?</span>', "", bas)
bas = re.sub(r'<span class="[^"]*"[^>]*>[^<]*</span>', "", bas, count=1)          # konu etiketi (REKLAM) — forumun kendi etiketi, metne girmez
BASLIK = html.unescape(re.sub(r"<[^>]+>", "", bas)).replace("\xa0", " ").strip()
i = S.find('<div class="bbWrapper">')
j = min(x for x in (S.find('<div class="js-selectToQuote', i), S.find("</article>", i)) if x > 0)
W = re.sub(r"<script.*?</script>", "", S[i:j], flags=re.S)
gizli = re.findall(r'<div class="xgt-GizliLink">.*?</div>', W, re.S)
assert len(gizli) == len(LINK) == 38, (len(gizli), len(LINK))
_it = iter(LINK)
W = re.sub(r'<div class="xgt-GizliLink">.*?</div>', lambda m: (lambda l: f'<a href="{html.escape(l[0])}">{html.escape(l[1])}</a>')(next(_it)), W, flags=re.S)


# --- agac
class N:
    def __init__(s, tag, at=None):
        s.tag, s.at, s.ch = tag, dict(at or {}), []


class P(HTMLParser):
    BOS = {"br", "img", "hr"}

    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.kok = N("kok"); s.st = [s.kok]

    def handle_starttag(s, t, a):
        n = N(t, a); s.st[-1].ch.append(n)
        if t not in s.BOS:
            s.st.append(n)

    def handle_startendtag(s, t, a):
        s.st[-1].ch.append(N(t, a))

    def handle_endtag(s, t):
        for k in range(len(s.st) - 1, 0, -1):
            if s.st[k].tag == t:
                del s.st[k:]; return

    def handle_data(s, d):          # tarayici gibi: metindeki satir sonu / tab / coklu bosluk = tek bosluk (satir sonu sadece <br>)
        s.st[-1].ch.append(re.sub(r"[ \t\r\n]+", " ", d))


p = P(); p.feed(W); KOKN = p.kok.ch[0]          # div.bbWrapper

BOYUT = {9: 1, 10: 2, 12: 3, 15: 4, 18: 5, 22: 6, 26: 7}   # XenForo 2 px -> BBCode 1-7
REKLAM_LINK = re.compile(r"^https://ko-yardim\.com/(forums/knight-online-pvp-server-tanitimi\.90/)?$")
RESIM = []          # [(src, ad, gen, yuk, stil_gen)]


def stil(n):
    d = {}
    for par in (n.at.get("style") or "").split(";"):
        if ":" in par:
            k, v = par.split(":", 1); d[k.strip()] = v.strip()
    return d


def renk(v):
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", v)
    return "#%02x%02x%02x" % tuple(int(x) for x in m.groups()) if m else v


def resim_no(n):
    src = n.at.get("src")
    for k, r in enumerate(RESIM, 1):
        if r[0] == src:
            return k
    RESIM.append((src, n.at.get("alt", ""), n.at.get("width"), n.at.get("height"), stil(n).get("width", "")))
    return len(RESIM)


def kidlar(n, f):
    return "".join(f(c) for c in n.ch)


def bb(n):
    if isinstance(n, str):
        return n.replace("​", "")
    t, c = n.tag, n.at.get("class", "")
    if t == "br":
        return "\n"
    if t == "img":
        if "smilie" in c:
            return n.at.get("alt", "")
        resim_no(n)
        return f"[IMG]{n.at.get('src')}[/IMG]"
    ic = kidlar(n, bb)
    st = stil(n)
    if t == "div":
        return f"[CENTER]{ic}[/CENTER]" if st.get("text-align") == "center" else ic
    if t == "h3":
        return ic
    if t == "span":
        if "font-size" in st:
            px = int(re.sub(r"\D", "", st["font-size"]) or 0)
            ic = f"[SIZE={BOYUT.get(px, 4)}]{ic}[/SIZE]"
        if "color" in st:
            ic = f"[COLOR={renk(st['color'])}]{ic}[/COLOR]"
        return ic
    if t in ("b", "strong"):
        return f"[B]{ic}[/B]"
    if t in ("i", "em"):
        return f"[I]{ic}[/I]"
    if t == "u":
        return f"[U]{ic}[/U]"
    if t == "a":
        h = n.at.get("href", "")
        return ic if REKLAM_LINK.match(h) or not h.startswith("http") else f"[URL={h}]{ic}[/URL]"
    return ic


def hm(n):          # temiz HTML (onizleme + "gorunumu kopyala")
    if isinstance(n, str):
        return html.escape(n.replace("​", ""), quote=False)
    t, c = n.tag, n.at.get("class", "")
    if t == "br":
        return "<br>"
    if t == "img":
        if "smilie" in c:
            return html.escape(n.at.get("alt", ""))
        w = stil(n).get("width") or (n.at.get("width", "") + "px")
        return f'<img src="{html.escape(n.at.get("src"))}" alt="{html.escape(n.at.get("alt", ""))}" style="max-width:100%;width:{w};height:auto">'
    ic = kidlar(n, hm)
    st = stil(n)
    if t == "div":
        return f'<div style="text-align:center">{ic}</div>' if st.get("text-align") == "center" else f"<div>{ic}</div>"
    if t == "h3":
        return f"<div>{ic}</div>"
    if t == "span":
        s_ = ";".join(f"{k}:{renk(v) if k == 'color' else v}" for k, v in st.items() if k in ("font-size", "color"))
        return f'<span style="{s_}">{ic}</span>' if s_ else ic
    if t in ("b", "strong", "i", "em", "u"):
        return f"<{t}>{ic}</{t}>"
    if t == "a":
        h = n.at.get("href", "")
        return ic if REKLAM_LINK.match(h) or not h.startswith("http") else f'<a href="{html.escape(h)}" target="_blank" rel="noopener">{ic}</a>'
    return ic


def md(n):
    if isinstance(n, str):
        return n.replace("​", "").replace("*", r"\*").replace("_", r"\_")
    t, c = n.tag, n.at.get("class", "")
    if t == "br":
        return "\n"
    if t == "img":
        if "smilie" in c:
            return n.at.get("alt", "")
        return f"![{n.at.get('alt', '')}]({n.at.get('src')})"
    ic = kidlar(n, md)
    if t in ("b", "strong", "i", "em"):
        isr = "**" if t in ("b", "strong") else "*"
        sat = []
        for l in ic.split("\n"):
            m = re.match(r"^(\s*)(.*?)(\s*)$", l, re.S)
            sat.append(m.group(1) + isr + m.group(2) + isr + m.group(3) if m.group(2) and not m.group(2).startswith("![") else l)
        return "\n".join(sat)
    if t == "a":
        h = n.at.get("href", "")
        return ic if REKLAM_LINK.match(h) or not h.startswith("http") else f"[{ic}]({h})"
    return ic


def duz(n):
    if isinstance(n, str):
        return n.replace("​", "")
    t, c = n.tag, n.at.get("class", "")
    if t == "br":
        return "\n"
    if t == "img":
        return n.at.get("alt", "") if "smilie" in c else f"[RESİM {resim_no(n)}: {n.at.get('alt', '')}]"
    ic = kidlar(n, duz)
    if t == "a":
        h = n.at.get("href", "")
        if REKLAM_LINK.match(h) or not h.startswith("http"):
            return ic
        return ic if h.rstrip("/").split("://")[-1] == ic.strip().rstrip("/") else f"{ic} ({h})"
    return ic


def temizle_bb(s):
    s = re.sub(r" *\n *", "\n", s)
    for _ in range(6):
        s = re.sub(r"\[(B|I|U)\](\s*)\[/\1\]", r"\2", s)
        s = re.sub(r"\[(SIZE|COLOR)=[^\]]+\](\s*)\[/\1\]", r"\2", s)
        s = re.sub(r"\[CENTER\](\s*)\[/CENTER\]", r"\1", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{4,}", "\n\n\n", s).strip()


def temizle_metin(s):
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


BB_ORIJINAL = temizle_bb(bb(KOKN))
# patron 4 Eki: orijinal icerik + sadece renk/boyut/cerceve (_tanitim_duzen.py — metin/resim/link ayni, assert)
import _tanitim_duzen
BB = _tanitim_duzen.duzenle(BB_ORIJINAL, {r[0]: r[4] for r in RESIM if r[4]})
BB = re.sub(r"\[SIZE=[1-4]\]", "[SIZE=5]", BB)          # 7 Eki PATRON: "abartili buyuk kucuk farklar olmasin, basliklar haric" -> baslik disi tek boy (5)
HT = _tanitim_duzen.onizleme(BB)
MD = temizle_metin(md(KOKN))
DZ = temizle_metin(duz(KOKN))
assert len(RESIM) == 5, len(RESIM)

# --- resimler (ayni adla tekrar indirilmez)
ADLAR = ["1_geri_sayim.gif", "2_logo.png", "3_stonesoft.png", "4_hyper_odul_havuzu.png", "5_takvim.gif"]
RD = os.path.join(KOK, "resim"); os.makedirs(RD, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36", "Referer": "https://ko-yardim.com/"}
RES = []
for (src, alt, gen, yuk, sw), ad in zip(RESIM, ADLAR):
    yol = os.path.join(RD, ad)
    if not os.path.exists(yol):
        r = requests.get(src, headers=H, timeout=120); r.raise_for_status()
        open(yol, "wb").write(r.content)
    RES.append({"no": len(RES) + 1, "dosya": "FORUM/resim/" + ad, "ad": ad, "orijinal_ad": alt, "url": src, "boyut": f"{gen}x{yuk}",
                "konudaki_genislik": sw or "tam", "mb": round(os.path.getsize(yol) / 1048576, 1)})

# --- 7 Eki: Ko-Yardim ek linkleri -> itemiconrepo (baska forumlarda Ko-Yardim eki gorunmeyebilir; tek kaynak repo)
import _repo_resim
for x in RES:
    yeni = _repo_resim.url(x["dosya"]); assert x["url"] in BB, x["url"]
    BB, MD, HT = BB.replace(x["url"], yeni), MD.replace(x["url"], yeni), HT.replace(x["url"], yeni)
    x["koyardim_url"] = x["url"]; x["url"] = yeni; x["repo"] = "forum/" + _repo_resim.rel(x["dosya"])

# --- dosyalar
open(os.path.join(KOK, "SEXYKO_TANITIM_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(KOK, "SEXYKO_TANITIM_bbcode_orijinal.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB_ORIJINAL + "\n")
open(os.path.join(KOK, "SEXYKO_TANITIM_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(KOK, "SEXYKO_TANITIM_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")

# --- forum listesi (REKLAM/DURUM.md: Aktif forumlar + Aktif tanitim siteleri)
RD_ = open(os.path.join(os.path.dirname(KOK), "REKLAM", "DURUM.md"), encoding="utf-8").read()


def tablo(baslik):
    a = RD_.find(baslik); b = RD_.find("\n## ", a)
    out = []
    for l in RD_[a:b].splitlines():
        m = re.match(r"^\| (\d+) \| (.*?) \| (https?://\S+) \| (.*) \|$", l)
        if m:
            out.append({"ad": m.group(2), "link": m.group(3), "not": m.group(4)})
    return out


FORUMLAR = [dict(f, grup="Forum") for f in tablo("### Aktif forumlar")] + [dict(f, grup="Tanıtım sitesi") for f in tablo("### Aktif tanıtım siteleri")]
assert len(FORUMLAR) == 18, len(FORUMLAR)
VERI = {"kaynak": KONU_URL, "baslik": BASLIK, "bbcode": BB, "markdown": MD, "duz": DZ, "html": HT, "resimler": RES, "forumlar": FORUMLAR}
# YENI KONU (Oyun Rehberi, _yeni_konu.py) — sayfada ayri sekme; once python _yeni_konu.py
_yk = os.path.join(KOK, "yeni_konu", "konu.json")
VERI["yeni"] = json.load(open(_yk, encoding="utf-8")) if os.path.exists(_yk) else None
# KISA KONU (uzun konunun ozeti, _kisa_konu.py) — sayfada "Kisa konu" sekmesi; once python _kisa_konu.py
_kk = os.path.join(KOK, "yeni_konu", "kisa", "konu.json")
VERI["kisa"] = json.load(open(_kk, encoding="utf-8")) if os.path.exists(_kk) else None
# SKILL & MASTER KONUSU (_skill_konu.py, 6 Eki) — sayfada "Skill & Master" sekmesi; once python _skill_gorsel.py + _skill_konu.py
_sk = os.path.join(KOK, "skill_master", "konu.json")
VERI["skill"] = json.load(open(_sk, encoding="utf-8")) if os.path.exists(_sk) else None
# HYPER BETA ODULLERI KONUSU (_odul_konu.py, 7 Eki — forum.sexyko.com/d/54) — "Hyper Beta Odulleri" sekmesi; once python _odul_gorsel.py + _odul_konu.py
_od = os.path.join(KOK, "odul", "konu.json")
VERI["odul"] = json.load(open(_od, encoding="utf-8")) if os.path.exists(_od) else None
# SEZON SISTEMI (ACADEMY) KONUSU (_sezon_konu.py, 7 Eki — patron tablosu + forum.sexyko.com/d/57) — once python _sezon_gorsel.py + _sezon_konu.py
_sz = os.path.join(KOK, "sezon", "konu.json")
VERI["sezon"] = json.load(open(_sz, encoding="utf-8")) if os.path.exists(_sz) else None
json.dump(VERI, open(os.path.join(KOK, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# --- 7 Eki: FLARUM (forum.sexyko.com) BBCode dosyalari — [SIZE=n] orada n PIKSEL (s9e {RANGE=8,36}); 1-7 olcegi 8 px'e dusuyordu (d/54, d/56).
# Dogrudan yapistirilir: resim linkleri yerlesik, boyut px (sayfadaki "Forum turu: Flarum" ile birebir). Koyu zemin renkleri.
SIZE_PX = {1: 9, 2: 10, 3: 12, 4: 15, 5: 18, 6: 22, 7: 26}
def flarum(bb, resimler=None):
    if resimler is not None:
        u = {r["id"]: r.get("varsayilan_url") for r in resimler}
        bb = re.sub(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", lambda m: u[m.group(1)] or m.group(0), bb)
    bb = re.sub(r"\[SIZE=([1-7])\]", lambda m: f"[SIZE={SIZE_PX[int(m.group(1))]}]", bb)
    assert "{{" not in bb and not re.search(r"\[SIZE=[1-7]\]", bb)
    return bb
FLARUM = {"SEXYKO_TANITIM_bbcode_flarum.txt": (BASLIK, flarum(BB))}
for k, yol in [("yeni", "yeni_konu/YENI_KONU_bbcode_flarum.txt"), ("kisa", "yeni_konu/kisa/KISA_KONU_bbcode_flarum.txt"), ("skill", "skill_master/SKILL_KONU_bbcode_flarum.txt"),
               ("odul", "odul/ODUL_KONU_bbcode_flarum.txt"), ("sezon", "sezon/SEZON_KONU_bbcode_flarum.txt")]:
    if VERI.get(k): FLARUM[yol] = (VERI[k]["baslik"], flarum(VERI[k]["bbcode"], VERI[k]["resimler"]))
for yol, (bas_, bb_) in FLARUM.items():
    open(os.path.join(KOK, *yol.split("/")), "w", encoding="utf-8").write(bas_ + "\n\n" + bb_ + "\n")
print("flarum bbcode:", len(FLARUM), "dosya ·", ", ".join(f"{y.split('/')[-1]} {len(b)}" for y, (_, b) in FLARUM.items()))

# --- sayfa
sab = open(os.path.join(KOK, "_konu_sablon.html"), encoding="utf-8").read()
gom = json.dumps(VERI, ensure_ascii=False).replace("</", "<\\/")
CIK = os.path.join(os.path.dirname(KOK), "HTML", "FORUM_KONU.html")
open(CIK, "w", encoding="utf-8").write(sab.replace("/*__VERI__*/null", gom))
print("baslik:", BASLIK, f"({len(BASLIK)} karakter)")
print("bbcode", len(BB), "· markdown", len(MD), "· duz", len(DZ), "· resim", len(RES), "· forum", len(FORUMLAR))
print("link [URL]:", BB.count("[URL="), "· [IMG]:", BB.count("[IMG]"), "· ko-yardim.com metinde:", BB.count("ko-yardim.com/konu"), "· yazildi:", CIK)

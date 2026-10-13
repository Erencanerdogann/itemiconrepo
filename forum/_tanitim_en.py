# -*- coding: utf-8 -*-
# TANITIM KONUSU (Ko-Yardim) EN (13 Eki aksam PATRON "ENG MI BU APTAL") — FORUM_KONU_EN.html'in "Promo topic" sekmesi.
# Tanitim BBCode'u serbest (blok yok): [etiket] arasi her yazi parcasi sozlukten -> tanitim_en.json = {"baslik", "metin": {TR: EN}, "izin": []}.
# Onizleme = _tanitim_duzen.onizleme(EN BBCode) (TR ile ayni yol); Markdown / duz metin EN BBCode'dan turetilir.
# Turkce yazili 2 GIF (geri sayim, takvim) EN'de yok; afis (4_hyper_odul_havuzu.png) tasarim resmi — Turkce yazisi resmin icinde, aynen kalir.
#   python _tanitim_en.py sablon / birlestir   (_konu_kit.py'den sonra: BB -> SEXYKO_TANITIM_bbcode.txt)
# _konu_kit.py: VERI_EN["tanitim"] = _tanitim_en.uret(BASLIK, BB, RES, FORUMLAR) — sozluk yoksa / eksikse None (sayfada TR + "TR" etiketi).
import os, re, sys, json
import _tanitim_duzen

KOK = os.path.dirname(os.path.abspath(__file__))
SOZ = os.path.join(KOK, "tanitim_en.json")
GIF = ("1_geri_sayim.gif", "5_takvim.gif")
ETIKET = re.compile(r"(\[[^\]]+\])")


def _yazi(s): return any(c.isalpha() for c in s) and not s.strip().startswith("http")


def parcalar(bb):
    L = []
    for p in ETIKET.split(bb):
        if ETIKET.fullmatch(p or "") or not _yazi(p): continue
        t = p.strip()
        if t not in L: L.append(t)
    return L


def _bb_en(bb, M):
    out = []
    for p in ETIKET.split(bb):
        if ETIKET.fullmatch(p or "") or not _yazi(p): out.append(p); continue
        t = p.strip(); assert M.get(t), ("ceviri yok", t[:60])
        b, s = re.match(r"^\s*", p).group(0), re.search(r"\s*$", p).group(0)
        out.append(b + M[t] + s)
    return "".join(out)


def _gifsiz(bb, RES):
    for r in RES:
        if r["ad"] in GIF:
            bb = re.sub(r"\[IMG[^\]]*\]" + re.escape(r["url"]) + r"\[/IMG\]", "", bb)
    for _ in range(4):
        bb = re.sub(r"\[CENTER\]\s*\[/CENTER\]", "", bb)
    return re.sub(r"\n{4,}", "\n\n\n", bb).strip()


def _md(bb):
    s = re.sub(r"\[IMG[^\]]*\](.*?)\[/IMG\]", r"![](\1)", bb)
    s = re.sub(r"\[URL=([^\]]+)\](.*?)\[/URL\]", r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"\[/?B\]", "**", s)
    s = re.sub(r"\[/?(?:SIZE|COLOR|FONT)(?:=[^\]]*)?\]|\[/?(?:CENTER|LEFT|RIGHT|I|U)\]", "", s)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"\*\*\s*\*\*", "", s)).strip()


def _duz(bb):
    s = re.sub(r"\[IMG[^\]]*\](.*?)\[/IMG\]", r"[IMAGE: \1]", bb)
    s = re.sub(r"\[URL=([^\]]+)\](.*?)\[/URL\]", r"\2 (\1)", s, flags=re.S)
    s = re.sub(r"\[[^\]]+\]", "", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


FORUM_AD = {"FrmTR — Knight Online bölümü": "FrmTR — Knight Online section", "Kocuce — KO PvP Serverlar Tanıtımı (forum)": "Kocuce — KO PvP Server Promotion (forum)",
            "SroTurk — KO PvP Serverler tanıtım forumu": "SroTurk — KO PvP server promo forum"}
FORUM_NOT = [(r"son paylaşım bugün", "last post today"), (r"son paylaşım dün", "last post yesterday"), (r"son paylaşım (\d+) gün önce", r"last post \1 days ago"),
             (r"30 günde (\d+)", r"\1 in 30 days"), (r"Chrome ile ölçüldü", "measured with Chrome"),
             (r"Reklam Alanları / Sponsorluklar \(ana sayfadaki bağlantı\)", "Ad Spaces / Sponsorships (link on the home page)"),
             (r"Üst Sabit Reklam Alanı", "Top Fixed Ad Space"), (r"Reklam Alanları", "Ad Spaces"), (r"Reklam fiyatları / iletişim", "Ad prices / contact"),
             (r"Reklam Paketleri", "Ad Packages"), (r"Reklam / İletişim", "Ads / Contact"), (r"Reklam Ver / Premium Sponsor", "Advertise / Premium Sponsor"),
             (r"Reklam ve İletişim", "Ads and Contact"), (r"💰 Reklam\b", "💰 Ads"), (r"#(\d{1,3}(?:\.\d{3})+)", lambda m: "#" + m.group(1).replace(".", ","))]


def forumlar_en(forumlar):
    """13 Eki: forum listesi (REKLAM/DURUM.md notlari) EN — grup, ad, not. Kalan Turkce harf = ASSERT."""
    out = []
    for f in forumlar:
        n = f["not"]
        for a, b in FORUM_NOT: n = re.sub(a, b, n)
        g = {"Forum": "Forum", "Tanıtım sitesi": "Promo site"}[f["grup"]]
        e = dict(f, grup=g, ad=FORUM_AD.get(f["ad"], f["ad"]), **{"not": n})
        assert not re.search(r"[ğüşıöçĞÜŞİÖÇ]", e["ad"] + e["not"]), (e["ad"], e["not"])
        out.append(e)
    return out


def uret(baslik, bb, RES, forumlar):
    if not os.path.exists(SOZ): return None
    S = json.load(open(SOZ, encoding="utf-8")); M = S["metin"]
    if any(not M.get(t) for t in parcalar(bb)): return None
    BB = _gifsiz(_bb_en(bb, M), RES)
    tam = re.sub(r"https?://\S+", "", BB)
    kalan = [w for w in re.findall(r"\S*[ğüşıöçĞÜŞİÖÇ]\S*", tam) if not any(z in w for z in S.get("izin", []))]
    assert not kalan, ("tanitim EN'de Turkce harf", kalan[:5])
    res = [dict(r) for r in RES if r["ad"] not in GIF]
    return {"baslik": S["baslik"], "bbcode": BB, "html": _tanitim_duzen.onizleme(BB), "markdown": _md(BB), "duz": _duz(BB),
            "resimler": res, "forumlar": forumlar_en(forumlar), "kaynak":"FORUM/tanitim_en.json (= Ko-Yardım promo topic, translated)"}


def _tr_bb():
    t = open(os.path.join(KOK, "SEXYKO_TANITIM_bbcode.txt"), encoding="utf-8").read()
    bas, bb = t.split("\n\n", 1)
    return bas, bb.rstrip("\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    kom = sys.argv[1]; bas, bb = _tr_bb(); L = parcalar(bb)
    if kom == "sablon":
        open(os.path.join(KOK, "tanitim_tr.txt"), "w", encoding="utf-8").write(f"0\t{bas}\n" + "".join(f"{i}\t{s}\n".replace("\n", " ⏎ ", s.count("\n")) for i, s in enumerate(L, 1)))
        print("tanitim", len(L), "parca -> tanitim_tr.txt  (⏎ = parcanin icindeki satir sonu; EN'de de \\n yaz)")
    elif kom == "birlestir":
        E = json.load(open(os.path.join(KOK, "tanitim_en_no.json"), encoding="utf-8"))
        izin = E.pop("izin", [])
        assert set(E) == {str(i) for i in range(len(L) + 1)}, ("numara uyusmuyor", len(L) + 1, len(E))
        assert not [n for n, v in E.items() if not v.strip()], "bos ceviri"
        M = {s: E[str(i)] for i, s in enumerate(L, 1)}
        for tr, en in M.items(): assert tr.count("\n") == en.count("\n"), ("satir sayisi", tr[:40], en[:40])
        json.dump({"baslik": E["0"], "metin": M, "izin": izin}, open(SOZ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.remove(os.path.join(KOK, "tanitim_tr.txt")); os.remove(os.path.join(KOK, "tanitim_en_no.json"))
        print("tanitim", len(M), "ceviri ->", SOZ)

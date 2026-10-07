# -*- coding: utf-8 -*-
# 24 SAATLIK MADENCILIK SONUCLARI — VERI (patron 7 Eki: Semih "Golden Mining / Mattock ... 24 saatlik drop sonuclarinin konusu acilacak" ->
# "go, admin sayfasindan oranlarina vs bakabilirsin, amacin forumda bilgi vermek, kurguyu sen yap" · "forum.html'e atacaksin, ben copy ederim").
# KAYNAK: oranlar = rehber/web/sayfa/mining-fishing/tum.html (sexyko.com/guide/mining-fishing CANLI, 7 Eki 06:18) — admin dokumu (24 Eyl) ile assert.
#         sonuc = mining/sonuc_24saat.json (Semih'in envanter goruntusu: ikon eslemesi + adet; goruntu _HASSAS/ git disi).
#         Platinum Auto Mining (patron 7 Eki 14:59 "automining eklemeyi unutmusuz, ayni sistemde ayni ozenle"): _HASSAS/mining_auto_envanter_2026-10-07.png (git disi)
import os, re, html, json

KOK = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(KOK, "mining")
WEB = os.path.join(KOK, "rehber", "web")
_H = open(os.path.join(WEB, "sayfa", "mining-fishing", "tum.html"), encoding="utf-8").read()
CEKIM = json.load(open(os.path.join(WEB, "mining-fishing.json"), encoding="utf-8")).get("tarih", "")
ADMIN = os.path.join(os.path.dirname(KOK), "ADMIN_PANEL", "VERI", "sexyko_admin_veri_tam.json")

# --- havuzlar (rehber sayfasindaki bolum sirasi)
_kart = list(re.finditer(r'data-id="(\d+)"\s+style="background-image: url\(\'([^\']+)\'\)".*?mining-item-name">([^<]+)<.*?mining-item-rate">([^<]+)<', _H, re.S))
_bas = [(m.start(), m.group(1)) for m in re.finditer(r">\s*(Normal Mattock|Golden Mattock|Platinum Auto Mining)\s*<", _H)]
HAVUZ = {}
for m in _kart:
    b = None
    for p, ad in _bas:
        if p < m.start(): b = ad
    HAVUZ.setdefault(b, []).append({"id": int(m.group(1)), "ikon": m.group(2), "ad": html.unescape(m.group(3)).strip(), "oran": float(m.group(4).strip().rstrip("%"))})
NORMAL, GOLDEN, PLATIN = HAVUZ["Normal Mattock"], HAVUZ["Golden Mattock"], HAVUZ["Platinum Auto Mining"]


def ikon_yolu(url):
    return os.path.join(WEB, "resim", url.replace("https://", "").replace("/", "_"))


# --- 24 saat sonuclari
SONUC = json.load(open(os.path.join(MD, "sonuc_24saat.json"), encoding="utf-8"))["sonuc"]
def _birles(havuz, sonuc):
    o = {x["id"]: x for x in havuz}
    return sorted([{**o[s["id"]], "adet": s["adet"]} for s in sonuc], key=lambda x: (-x["adet"], x["ad"]))
G24 = _birles(GOLDEN, SONUC["Golden Mattock"])           # [{id, ikon, ad, oran, adet}] adete gore
N24 = _birles(NORMAL, SONUC["Normal Mattock"])
TOPLAM_G, TOPLAM_N = sum(x["adet"] for x in G24), sum(x["adet"] for x in N24)
KAT = TOPLAM_G / TOPLAM_N
SADECE_G = [x for x in G24 if x["id"] not in {y["id"] for y in N24}]
P24 = _birles(PLATIN, SONUC["Platinum Auto Mining"])     # Auto Mining (Platinum) — havuzun tamami (21)
TOPLAM_P = sum(x["adet"] for x in P24)
KAT_P = TOPLAM_P / TOPLAM_N                                # Normal'e gore kat
SADECE_P = [x for x in P24 if x["id"] not in {y["id"] for y in G24}]
SURE_P = "24 saat"                                         # VARSAYIM: goruntude sure yazmiyor; patron 'ayni sistemde' dedi -> teyit bekliyor
ZONE = "Moradon Camp 1"

# ---------- dogrulama
assert len(NORMAL) == 19 and len(GOLDEN) == 21 and NORMAL[0]["ad"] == GOLDEN[0]["ad"] == "EXP", (len(NORMAL), len(GOLDEN))
assert len(G24) == 20 and len(N24) == 18                                             # EXP haric havuzun tamami goruntude
assert {x["id"] for x in G24} == {x["id"] for x in GOLDEN if x["ad"] != "EXP"} and {x["id"] for x in N24} == {x["id"] for x in NORMAL if x["ad"] != "EXP"}
assert sorted(x["ad"] for x in SADECE_G) == ["Blue Gem", "Fragment of Sloth"]
assert TOPLAM_G == 1601 and TOPLAM_N == 508
assert len(P24) == 21 and {x["id"] for x in P24} == {x["id"] for x in PLATIN} and TOPLAM_P == 1970        # Auto Mining: havuzun tamami goruntude
assert [x["ad"] for x in SADECE_P] == ["Automatic Mining Gift Box"] and SADECE_P[0]["adet"] == 6
for x in NORMAL + GOLDEN + PLATIN: assert os.path.exists(ikon_yolu(x["ikon"])), x
_a = json.load(open(ADMIN, encoding="utf-8"))["veri"]["ham:item-mining-lists"]   # admin 24 Eyl: sRate 1/100 % (15 = %0,15)
_adm = {r["r"]["Num"]: r["r"] for r in _a if r["r"].get("Status")}
for x in NORMAL[1:]: assert abs(_adm[x["id"]]["sRateNormal"] / 100 - x["oran"]) < 1e-9, ("normal oran", x["ad"])
for x in GOLDEN[1:]: assert abs(_adm[x["id"]]["sRateGolden"] / 100 - x["oran"]) < 1e-9, ("golden oran", x["ad"])
assert {str(r["ZoneID"]) for r in _adm.values()} == {"21"}                       # admin: '21 - Moradon Camp 1'

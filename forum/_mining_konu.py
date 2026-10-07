# -*- coding: utf-8 -*-
# 24 SAATLIK MADENCILIK SONUCLARI FORUM KONUSU (patron 7 Eki: Semih "24 saatlik drop sonuclarinin konusu acilacak" -> "go, admin sayfasindan
# oranlarina vs bakabilirsin, amacin forumda bilgi vermek, kurguyu sen yap" · "forum.html'e atacaksin, ben copy ederim").
# Veri: _mining_veri.py · resimler: _mining_gorsel.py (M00-M04) + R01 logo · cevirici: _konu_blok.py
# CIKTI: mining/ (konu.json, MINING_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py "24 Saat Madencilik" sekmesi.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _mining_veri as V

Y = KB.Y
OUT = V.MD; RD = os.path.join(OUT, "resim")
BASLIK = "⛏️ SEXYKO 24 SAATLİK MADENCİLİK SONUÇLARI | Golden Mattock vs Normal Mattock · Oranlar"
KAT = f"{V.KAT:.2f}".replace(".", ",")
tr = lambda n: f"{n:,}".replace(",", ".")
yz = lambda o: f"%{o:.2f}".replace(".", ",")

RES = {"R01": Y.RESIM["R01"]}
for rid, dosya, acik in [("M00", "M00_ozet.jpg", "24 saat — bir bakışta"), ("M01", "M01_golden.jpg", "Golden Mattock — 24 saat envanter"),
                         ("M02", "M02_normal.jpg", "Normal Mattock — 24 saat envanter"), ("M03", "M03_karsilastirma.jpg", "Item item karşılaştırma"),
                         ("M04", "M04_oranlar.jpg", "Resmî çıkma oranları (Normal / Golden / Platinum)")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

ekle("banner", "R01")
ekle("baslik", "24 SAATLİK MADENCİLİK SONUÇLARI", "Golden Mattock ile Normal Mattock — 24 saatte gerçekten ne çıktı?")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "⛏️", "BİR BAKIŞTA")
ekle("img", "M00", "")
ekle("p", f"Aynı süre — **24 saat** madencilik: **Golden Mattock {tr(V.TOPLAM_G)} item**, **Normal Mattock {tr(V.TOPLAM_N)} item** çıkardı. "
          f"Golden, Normal'in yaklaşık **{KAT} katı** item verdi.")
ekle("ayrac")

ekle("h", "🥇", "GOLDEN MATTOCK — 24 SAAT")
ekle("img", "M01", "")
ekle("liste", [f"**{x['ad']}** — {x['adet']} adet ({yz(x['oran'])})" for x in V.G24])
ekle("ayrac")

ekle("h", "🥈", "NORMAL MATTOCK — 24 SAAT")
ekle("img", "M02", "")
ekle("liste", [f"**{x['ad']}** — {x['adet']} adet ({yz(x['oran'])})" for x in V.N24])
ekle("ayrac")

ekle("h", "📊", "ITEM ITEM KARŞILAŞTIRMA")
ekle("img", "M03", "")
_n = {x["id"]: x for x in V.N24}
_b = V.G24[0]
ekle("p", f"En çok çıkan item iki kazmada farklı: Golden'da **{_b['ad']} ({_b['adet']})**, Normal'de **{V.N24[0]['ad']} ({V.N24[0]['adet']})**.")
ekle("not", f"**Sadece Golden Mattock'ta çıkanlar:** " + " · ".join(f"{x['ad']} ({x['adet']})" for x in V.SADECE_G) + " — Normal Mattock'un listesinde yok.")
ekle("ayrac")

ekle("h", "📘", "RESMÎ ÇIKMA ORANLARI")
ekle("img", "M04", "")
_exp_n = next(x["oran"] for x in V.NORMAL if x["ad"] == "EXP"); _exp_g = next(x["oran"] for x in V.GOLDEN if x["ad"] == "EXP")
ekle("liste", [f"**Normal Mattock:** EXP {yz(_exp_n)} + {len(V.N24)} item (her biri {yz(min(x['oran'] for x in V.N24))} – {yz(max(x['oran'] for x in V.N24))})",
               f"**Golden Mattock:** EXP {yz(_exp_g)} + {len(V.G24)} item (her biri {yz(min(x['oran'] for x in V.G24))} – {yz(max(x['oran'] for x in V.G24))}) — Blue Gem ve Fragment of Sloth sadece burada",
               f"**Platinum Auto Mining:** {len(V.PLATIN)} item — Automatic Mining Gift Box ({yz(next(x['oran'] for x in V.PLATIN if x['ad'] == 'Automatic Mining Gift Box'))}) sadece burada"])
ekle("not", f"Oranlar oyun içi rehberden ({V.CEKIM}) — admin kayıtlarıyla birebir aynı. Madencilik listesi bölgesi: **{V.ZONE}**.")
ekle("ayrac")

ekle("h", "💡", "BİLMEN GEREKENLER")
ekle("liste", [f"Golden Mattock'ta EXP oranı düşük ({yz(_exp_g)}, Normal'de {yz(_exp_n)}) — Golden **item odaklı**, Normal daha çok EXP verir",
               "Bir itemin nereden çıktığını bilmiyorsan: item üstünde **Ctrl + D**",
               "Bütün oranlar: oyunda **Rehber → Madencilik & Balıkçılık** ya da sexyko.com/guide/mining-fishing"])
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["📘 Madencilik & Balıkçılık: [[https://sexyko.com/guide/mining-fishing|sexyko.com/guide/mining-fishing]]",
               "💬 Forum: [[https://forum.sexyko.com|forum.sexyko.com]] · Discord: [[https://discord.gg/sexyko|discord.gg/sexyko]]",
               "🌐 Web: [[https://www.sexyko.com|www.sexyko.com]]"])
ekle("ayrac")
ekle("son", "🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥")

KONTROL = [
    "**Kaynak (sonuç):** Semih'in 24 saatlik envanter görüntüsü (7 Eki, 'Golden Mining' + 'Mattock') — her yuvanın ikonu rehber havuzu ikonlarıyla eşlendi (bire bir atama) ve gözle doğrulandı; adetler görüntüden. Görüntü `_HASSAS/` (git dışı — WhatsApp adı görünüyor).",
    "**Test koşulları bilinmiyor** (kaç karakter, hangi bölge, otomatik mi elle mi, premium var mı) → konuda 'aynı süre: 24 saat' dışında koşul iddiası YOK; ekip eklemek isterse metne.",
    f"**Oranlar:** oyun içi rehber canlı ({V.CEKIM}) = admin dökümü (24 Eyl) — 38 oranın hepsi birebir (`_mining_veri.py` assert). Bölge: admin ZoneID 21 – Moradon Camp 1.",
    f"Kat hesabı: {tr(V.TOPLAM_G)} / {tr(V.TOPLAM_N)} = {KAT}. Golden 20 / Normal 18 çeşit = havuzların EXP hariç tamamı.",
    "Admin'de 'IsPremiumFarmItemDurabilityDrop' (Golden Mattock dayanıklılığı) ayarı var ama döküm 24 Eyl — güncelliği bilinmediği için konuya ALINMADI.",
    "**5 resim (M00–M04)** — hazır linkli (itemiconrepo `forum/mining/resim/`, içerik özetli). R01 logo ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for x in V.G24 + V.N24: assert f"{x['ad']}" in BB, x["ad"]
assert tr(V.TOPLAM_G) in BB and tr(V.TOPLAM_N) in BB and KAT in BB and len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in ["R01", "M00", "M01", "M02", "M03", "M04"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "oyun/rehber"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/mining/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "mining/sonuc_24saat.json (Semih 24 saat) + rehber mining-fishing (canlı) + admin"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "MINING_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "MINING_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "MINING_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("MINING: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

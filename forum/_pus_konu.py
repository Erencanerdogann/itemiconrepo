# -*- coding: utf-8 -*-
# PUS INDIRIM KODU SISTEMI FORUM KONUSU (patron 8 Eki: "yeni forum konulari ... resimli vs ayni janradan devam" · "hepsini tek tek konuya dok guzelce,
# resimleri repoya atmayi unutma, pushlamayi unutma"). Kaynak: forum.sexyko.com/d/51.
# Veri: _pus_veri.py · resimler: _pus_gorsel.py (U00-U05) + R01 logo · cevirici: _konu_blok.py
# CIKTI: pus_kupon/ (konu.json, PUS_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py "PUS Indirim Kodu" sekmesi.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _pus_veri as V

Y = KB.Y
OUT = V.PD; RD = os.path.join(OUT, "resim")
BASLIK = "🎟️ SEXYKO PUS İNDİRİM KODU SİSTEMİ | Kupon Nasıl Kullanılır · Sponsor Yayıncı Kodları · %30'a Varan"

RES = {"R01": Y.RESIM["R01"]}
for rid, dosya, acik in [("U00", "U00_ozet.jpg", "PUS indirim kodu — bir bakışta"), ("U01", "U01_nasil.jpg", "Nasıl kullanılır — Kupon → CHECK"),
                         ("U02", "U02_tekli.jpg", "Tekli item alımında kupon"), ("U03", "U03_sepet.jpg", "Basket / sepette kupon"),
                         ("U04", "U04_istisna_sponsor.jpg", "VIP / Farm istisnası + Sponsor Yayıncı kodları"), ("U05", "U05_kisaca.jpg", "Kısacası + %30'a varan")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

ekle("banner", "R01")
ekle("baslik", "PUS İNDİRİM KODU SİSTEMİ", "Power Up Store'da kuponla indirim — Sponsor Yayıncını destekle")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "🎟️", "BİR BAKIŞTA")
ekle("img", "U00", "")
ekle("p", V.GIRIS[0] + " " + V.GIRIS[1])
ekle("p", f"{V.GIRIS[2]} **{V.GIRIS[3]}**")
ekle("ayrac")

ekle("h", "🛒", V.NASIL_BAS)
ekle("img", "U01", "")
ekle("p", f"{V.NASIL[0]} Ardından **CHECK** butonuna tıklayın.")
ekle("p", f"**{V.NASIL[1]}** {V.NASIL[2]}")
ekle("ayrac")

ekle("h", "🎁", V.TEKLI_BAS)
ekle("img", "U02", "")
ekle("p", " ".join(V.TEKLI[:2]))
ekle("p", f"**{V.TEKLI[2]}**")
ekle("ayrac")

ekle("h", "🛍️", V.SEPET_BAS)
ekle("img", "U03", "")
ekle("p", " ".join(V.SEPET[:2]))
ekle("p", f"**{V.SEPET[2]}**")
ekle("ayrac")

ekle("h", "⚠️", V.PAKET_BAS)
ekle("img", "U04", "")
ekle("liste", [f"**{x}**" for x in V.PAKET])
ekle("p", V.PAKET_NEDEN[0])
ekle("not", f"Bu ürünler hali hazırda paket indirimi içerdiği için **{V.PAKET_NEDEN[1].lower()}**")
ekle("ayrac")

ekle("h", "🎥", V.SPONSOR_BAS)
ekle("p", " ".join(V.SPONSOR[:2]))
ekle("p", "**Oyuncular:** " + " → ".join(V.SPONSOR_AKIS) + ".")
ekle("p", V.SPONSOR[2])
ekle("ayrac")

ekle("h", "🔥", V.ETKINLIK_BAS)
ekle("p", f"{V.ETKINLIK[0]} **🎉 %30'A VARAN İNDİRİMLER** aktif edilebilir. {V.ETKINLIK[1]}")
ekle("p", "Bu nedenle takip etmenizi öneriyoruz:")
ekle("liste", V.TAKIP)
ekle("not", f"**{V.ETKINLIK[2]}**")
ekle("ayrac")

ekle("h", "💎", V.OZEL_BAS)
ekle("p", " ".join(V.OZEL))
ekle("p", "**Sponsor Yayıncı Kupon Sistemi sayesinde:**")
ekle("liste", V.OZEL_L)
ekle("p", V.OZEL_SON)
ekle("ayrac")

ekle("h", "✅", "KISACASI")
ekle("img", "U05", "")                                   # akis resimde (patron 7 Eki: "resimde var, yazman lazim miydi") -> metinde tekrar yok
ekle("p", f"🔥 **SEXYKO PUS KUPON SİSTEMİ** — {V.SLOGAN}")
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["🌐 Web: [[https://www.sexyko.com|www.sexyko.com]]",
               "💬 Discord: [[https://discord.gg/sexyko|discord.gg/sexyko]] · Forum: [[https://forum.sexyko.com|forum.sexyko.com]]"])
ekle("ayrac")
ekle("son", f"🎟️ {V.SON} 🎟️")

KONTROL = [
    "**Kaynak:** forum.sexyko.com/d/51 (Flarum API, 8 Eki) — her cümle kaynakta birebir (`_pus_veri.py` assert).",
    "**Ekran görüntüleri:** gönderinin kendi 3 resmi (PUS penceresi + sepet, tekli alım onayı, sepet) U01–U03'ün içinde; U01'de Coupon / Check / sonuç satırı numaralı çerçeveli.",
    "**Resimdeki örnek:** kod **Sexyko10**, -10%, Switching Premium 950 → 855 SB, sepet SB 2,675 → 2,408 · KC 6,120 → 5,508 — konuda \"örnek\" diye yazıldı; geçerli kod iddiası YOK.",
    "Hangi yayıncının hangi kodu olduğu kaynakta yok → konuya eklenmedi (kodlar yayıncılardan / Discord'dan).",
    "**6 resim (U00–U05)** — hazır linkli (itemiconrepo `forum/pus_kupon/resim/`, içerik özetli). R01 logo ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for s in [V.NASIL[0], *V.TEKLI, *V.SEPET, *V.PAKET, V.PAKET_NEDEN[0], *V.SPONSOR, *V.TAKIP, *V.OZEL, *V.OZEL_L, V.OZEL_SON]: assert s in BB, s
assert len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in ["R01", "U00", "U01", "U02", "U03", "U04", "U05"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum d/51 + oyun içi PUS"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/pus_kupon/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "forum.sexyko.com/d/51 (metin + 3 ekran görüntüsü)"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "PUS_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "PUS_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "PUS_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("PUS: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

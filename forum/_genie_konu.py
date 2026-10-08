# -*- coding: utf-8 -*-
# GENIE SISTEMI FORUM KONUSU (patron 8 Eki: arsivde "cok kotu" d/16 — 4/4 resim kirik — "genie sistemi go"). Kaynak: forum.sexyko.com/d/16.
# Veri: _genie_veri.py · resimler: _genie_gorsel.py (G00-G07, oyunun kendi Genie penceresi) + R01 logo · cevirici: _konu_blok.py
# CIKTI: genie/ (konu.json, GENIE_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py "Genie Sistemi" sekmesi.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _genie_veri as V

Y = KB.Y
OUT = V.GD; RD = os.path.join(OUT, "resim")
BASLIK = "⚙️ SEXYKO GENIE SİSTEMİ | Başlat · Durdur · 8+8+8 Skill · HP/MP Pot · Mob Listesi · Attack Range"

RES = {"R01": Y.RESIM["R01"]}
for rid, dosya, acik in [("G00", "G00_ozet.jpg", "Genie sistemi — bir bakışta"), ("G01", "G01_panel.jpg", "Hızlı kontrol paneli (sağ üst)"),
                         ("G02", "G02_ana.jpg", "Genie penceresi — Main"), ("G03", "G03_pot.jpg", "HP / MP pot yüzdesi"), ("G04", "G04_mob.jpg", "Saldırılacak mob listesi"),
                         ("G05", "G05_esik_range.jpg", "Party / Self heal eşiği + Attack range"), ("G06", "G06_misc.jpg", "Genie penceresi — Misc"),
                         ("G07", "G07_kurulum.jpg", "Genie nasıl kurulur — 8 adım")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

ekle("banner", "R01")
ekle("baslik", "SEXYKO GELİŞMİŞ GENIE SİSTEMİ", V.UST)
ekle("icindekiler")
ekle("ayrac")

ekle("h", "⚙️", "BİR BAKIŞTA")
ekle("img", "G00", "")
ekle("p", V.GIRIS[0])
ekle("p", f"**{V.GIRIS[1]}**")
ekle("ayrac")

ekle("h", "▶️", V.PANEL_BAS)
ekle("img", "G01", "")
ekle("p", V.PANEL_GIRIS)
for i, b, L in V.PANEL:
    ekle("p", f"{i} **{b}** — {' '.join(L)}")
ekle("ayrac")

ekle("h", "⚔️", V.ANA_BAS)
ekle("img", "G02", "")
ekle("p", " ".join(V.ANA))
for i, b, n, L in V.SKILL:
    ekle("p", f"{i} **{b} — {n}** · {' '.join(L)}")
ekle("p", f"📜 **{V.SCROLL[0]}** — {' '.join(V.SCROLL[1])}")
ekle("ayrac")

ekle("h", "❤️", "HP / MP POT AYARLARI")
ekle("img", "G03", "")
ekle("p", f"❤️ **{V.HP[0]}** — {V.HP[1]} {V.HP[2]} Örneğin **{V.HP[3]}** {V.HP[4]} {V.HP[5]}")
ekle("p", f"💙 **{V.MP[0]}** — {V.MP[1]} {V.MP[2]} Örneğin **{V.MP[3]}** {V.MP[4]} {V.MP[5]}")
ekle("ayrac")

ekle("h", "🎯", V.MOB[0])
ekle("img", "G04", "")
ekle("p", f"{V.MOB[1]} {V.MOB[2]}")
ekle("liste", [f"**{a}** — {b}" for a, b in V.MOB_L])
ekle("p", V.MOB_SON[0])
ekle("not", f"**{V.MOB_SON[1]}**")
ekle("ayrac")

ekle("h", "👥", "PARTY HP · KENDİ HP · ATTACK RANGE")       # oyunda Main -> Assist Thresholds (kaynak bunlari Misc altinda anlatiyor -> KONTROL)
ekle("img", "G05", "")
for i, b, L in V.TAKIP:
    ekle("p", f"{i} **{b}** — {' '.join(L)}")
ekle("p", f"📏 **{V.RANGE[0]}** — {V.RANGE[1]}")
ekle("liste", [f"**{a}:** {b}" for a, b in V.RANGE_L])
ekle("p", V.RANGE_SON)
ekle("ayrac")

ekle("h", "🧩", V.MISC[0])
ekle("img", "G06", "")                                   # Misc secenekleri resimde (patron 7 Eki: "resimde var, yazman lazim miydi") -> metinde tekrar yok
ekle("p", f"{V.MISC[1]} {V.MISC[2]}")
ekle("p", f"{V.MINOR[0]} **{V.MINOR[1]}** — {' '.join(V.MINOR[2])}")
ekle("ayrac")

ekle("h", "🔒", V.KILIT[0])
ekle("p", " ".join(V.KILIT[1][:3]))
ekle("not", f"**{V.KILIT[1][3]}**")
ekle("ayrac")

ekle("h", "🚀", V.KURULUM_BAS)
ekle("img", "G07", "")                                   # 8 adim + son not resimde -> metinde tekrar yok
ekle("ayrac")

ekle("h", "✅", "KISACASI")
ekle("liste", [f"**{x}**" for x in V.KISACA])
ekle("p", f"🔥 **{V.SLOGAN}**")
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["🌐 Web: [[https://www.sexyko.com|www.sexyko.com]]",
               "💬 Discord: [[https://discord.gg/sexyko|discord.gg/sexyko]] · Forum: [[https://forum.sexyko.com|forum.sexyko.com]]"])
ekle("ayrac")
ekle("son", f"🚀 {V.SON} 🚀")

KONTROL = [
    "**Kaynak:** forum.sexyko.com/d/16 (Flarum API, 8 Eki) — her cümle kaynakta birebir (`_genie_veri.py` assert).",
    "**Ekran görüntüleri:** gönderinin 4 resmi kaynakta **404** (i.hizliresim.com) → yerine **oyunun kendi Genie penceresi** (3 Eki, Knight Genie Main / Misc + sağ üst Genie çubuğu); önemli yerler numaralı çerçeveli. Ekrandaki değerler (HP %85, MP %44, Party %96, Self %99, 79 m, 234d 1h, Satiros) o karakterin ayarı — örnek.",
    "⚠ **Kaynak kusuru:** \"Bu bölümde üç temel işlem bulunur\" deyip 4 madde sayıyor (Başlat / Durdur / Kalan süre / Ayarlar) → o cümle konuya ALINMADI.",
    "⚠ **Kaynak ↔ oyun farkı 1:** Party HP / Kendi HP takibi kaynakta \"Misc\" altında; oyunda **Main → Assist Thresholds** (Party heal below / Self heal below) → konuda Attack Range ile aynı bölümde (G05).",
    "⚠ **Kaynak ↔ oyun farkı 2:** Misc sekmesindeki 9 seçenek (Combat / Maintenance / Return to town) kaynakta YOK → ekrandan birebir + Türkçesi (G06).",
    "⚠ **Ekip teyidi:** Minor seçeneği ve ayrı \"scroll alanı\" bu ekranda (Knight Genie) görünmüyor — kaynak metni korundu; Rogue'da mı çıkıyor, ekip söylesin.",
    "**⬇ = Ayarlar** — 3 Eki oyunda denendi (`rehber/SEXYKO_REHBER.md` §2.2).",
    "**8 resim (G00–G07)** — hazır linkli (itemiconrepo `forum/genie/resim/`, içerik özetli). R01 logo ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for s in [*V.GIRIS, V.PANEL_GIRIS, *[x for _, _, L_ in V.PANEL for x in L_], *V.ANA, *[x for _, _, _, L_ in V.SKILL for x in L_], *V.SCROLL[1], *V.HP[1:], *V.MP[1:],
          *V.MOB[1:], *[b for _, b in V.MOB_L], *V.MOB_SON, *V.MISC[1:], *[x for _, _, L_ in V.TAKIP for x in L_], *V.MINOR[2], V.RANGE[1], *[b for _, b in V.RANGE_L],
          V.RANGE_SON, *V.KILIT[1], *V.KISACA, V.SLOGAN, V.SON]:
    assert s in BB, s[:60]
assert "üç temel işlem" not in BB and "̇" not in BB and len(BASLIK) <= 100, len(BASLIK)   # kusurlu cumle yok · Turkce harf donusumu bozulmasin (birlesik nokta)
res = []
for rid in ["R01", "G00", "G01", "G02", "G03", "G04", "G05", "G06", "G07"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum d/16 + oyun içi Genie penceresi (3 Eki)"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/genie/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "forum.sexyko.com/d/16 (metin) + oyun içi Genie penceresi (4 resim kaynakta 404)"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "GENIE_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "GENIE_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "GENIE_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("GENIE: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

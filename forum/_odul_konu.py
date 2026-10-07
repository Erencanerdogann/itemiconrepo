# -*- coding: utf-8 -*-
# HYPER BETA ODULLERI FORUM KONUSU (patron 7 Eki: Semih "forum.sexyko.com/d/54 bu konuyu da yapar misin, gorselli yaptin ya guzel oldu" +
# patron "skill ve master gibi yapacagiz, resimli detayli sekilde forum konu html'e ayni sekilde yazacagiz, bbcode vs hepsi olacak, resimleri repoya at linkle").
# Veri: _odul_veri.py (kaynak metne assert'li) · resimler: _odul_gorsel.py (O00-O05) + uzun konunun R01 logo + 2 GIF · cevirici: _konu_blok.py
# CIKTI: odul/ (konu.json, ODUL_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py sayfaya "Hyper Beta Odulleri" sekmesi olarak koyar.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _odul_veri as V

Y = KB.Y
OUT = V.OD; RD = os.path.join(OUT, "resim")
BASLIK = "🏆 SEXYKO HYPER BETA ÖDÜLLERİ | 4 CSW: 200.000 TL + 160.000 SB · Clan & Job Sıralaması · NP Çekilişi"

RES = {"R01": Y.RESIM["R01"], "GSAYIM": Y.RESIM["GSAYIM"], "GTAKVIM": Y.RESIM["GTAKVIM"]}
for rid, dosya, acik in [("O00", "O00_ozet.jpg", "Bir bakışta — 6 ödül başlığı"), ("O01", "O01_takvim.jpg", "Beta CSW takvimi — 17 · 18 · 20 · 22 Ekim, 22:00"),
                         ("O02", "O02_csw_odul.jpg", "Her CSW'de ödüller + toplamlar + ödül kuralı"), ("O03", "O03_clan.jpg", "Clan sıralama ödülleri"),
                         ("O04", "O04_job.jpg", "Job sıralama ödülleri"), ("O05", "O05_np_cekilis.jpg", "100.000+ NP Beta çekilişi")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

bt, bs = V.BETA
ekle("afis", "GSAYIM")
ekle("banner", "R01")
ekle("baslik", "HYPER BETA ÖDÜLLERİ", f"{bt} • {bs} — Clan sıralaması, Job sıralaması, 4 büyük Castle Siege War ve özel NP çekilişi")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "🏆", "BİR BAKIŞTA")
ekle("img", "O00", "")
ekle("p", "SexyKO HYPER Beta sürecinde rekabet **ilk günden** başlayacak. Beta boyunca oyuncularımızı **Clan sıralaması**, **Job sıralaması**, "
          "**4 büyük Castle Siege War** ve özel **NP çekilişi** bekliyor.")
ekle("ayrac")

ekle("h", "📅", "BETA CSW TAKVİMİ")
ekle("img", "O01", "")
KISA_AD = {"1. BETA CSW": "1. Beta CSW", "2. BETA CSW": "2. Beta CSW", "3. BETA CSW": "3. Beta CSW", "BETA FİNAL CSW": "Beta Final CSW"}   # kaynaktaki takvim yazimi
for _a in KISA_AD.values(): assert _a in V.KAYNAK, _a
ekle("liste", [f"**{k} — 22:00** · {'👑' if 'FİNAL' in a else '🏰'} {KISA_AD[a]}" for t, g, a, k in V.CSW])
ekle("p", f"🕙 **CSW başlangıç saati: {V.CSW_SAAT['baslangic']}** · ⏳ **Hazırlık: {V.CSW_SAAT['hazirlik'].lower()}** · ⚔️ **Savaş: {V.CSW_SAAT['savas'].lower()}**")
ekle("p", "Saat 22:00'de CSW hazırlık süreci başlayacaktır. İlk 10 dakika hazırlık süresi olarak geçecek, ardından Castle Siege War başlayacak ve "
          "savaş **maksimum 60 dakika** sürecektir.")
ekle("not", f"**Beta Final CSW (22 Ekim Perşembe):** {V.FINAL_NOT}")
ekle("ayrac")

ekle("h", "🏰", "CSW ÖDÜLLERİ (HER CSW'DE)")
ekle("img", "O02", "")
ekle("liste", [f"{e} **{i}. {a}** → 💵 **{tl}** + 💎 **{sb}**" for i, (e, a, tl, sb) in enumerate(V.CSW_ODUL, 1)])
ekle("p", f"🔥 **Her CSW'de toplam:** 💵 **{V.CSW_TOPLAM[0]} nakit** + 💎 **{V.CSW_TOPLAM[1]}** dağıtılacaktır.")
ekle("p", f"🏆 **4 CSW genel toplamı:** 💵 **{V.GENEL_TOPLAM[0]} nakit ödül** + 💎 **{V.GENEL_TOPLAM[1]}**")
ekle("not", "**CSW ödül kuralı:** " + " ".join(V.CSW_KURAL))
ekle("ayrac")

ekle("h", "👑", "CLAN SIRALAMA ÖDÜLLERİ")
ekle("img", "O03", "")
ekle("liste", [f"{e} **{a}** → 💎 **{sb}**" for e, a, sb in V.CLAN] + [f"**Toplam** → 💎 **{V.CLAN_TOPLAM}**"])
ekle("not", " ".join(V.CLAN_NOT))
ekle("ayrac")

ekle("h", "⚔️", "JOB SIRALAMA ÖDÜLLERİ")
ekle("img", "O04", "")
ekle("p", f"**{' • '.join(V.JOBLAR)}** — {V.JOB_NOT}")
ekle("liste", [f"{e} **{a}** → " + " + ".join(("💵 " if x.endswith(" TL") else "💎 " if "SB" in x else "🗿 ") + f"**{x}**" for x in od) for e, a, od in V.JOB_ODUL])
ekle("not", V.JOB_5_10)
ekle("ayrac")

ekle("h", "🎁", "100.000+ NP BETA ÇEKİLİŞİ")
ekle("img", "O05", "")
ekle("p", V.NP_SART.replace("100.000 NP ve üzeri", "**100.000 NP ve üzeri**"))
ekle("liste", [f"{e} **{a}** → " + " + ".join(("💎 " if "SB" in x else "🗿 ") + f"**{x}**" for x in od) for e, a, od in V.NP])
ekle("ayrac")

ekle("h", "🚀", "23 EKİM 2026 — HYPER OFFICIAL")
ekle("liste", [f"{e} [[{u}|{a}]]" for e, a, u in V.LINK] + [f"📢 Konunun aslı: [[{V.KONU_URL}|forum.sexyko.com/d/54]]"])
ekle("ayrac")
ekle("afis", "GTAKVIM")
ekle("son", "🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥")

KONTROL = [
    f"**Kaynak:** forum.sexyko.com/d/54 (5 Eki 2026, SexyKO) — Flarum açık API ile 7 Eki 05:29'da okundu, düz metni `FORUM/odul/kaynak_d54.txt`. "
    "Konudaki her tarih / tutar / kural cümlesi kaynakta birebir (`_odul_veri.py` import'ta assert); toplamlar tek tek ödüllerle tutarlı (20+10+20 = 50 bin TL …).",
    "**Kaynakta YOK → konuda da yok:** Job sıralamasında **4. sıra** ödülü (kaynak 3.'den 5.–10.'a atlıyor) — ekip sorulsun.",
    "Job listesi kaynaktaki gibi **Priest • Warrior • Rogue • Kurian • Mage** (Rogue tek job; Assassin / Okçu ayrımı kaynakta yok).",
    "Heykel: kaynakta 'Job'a özel 30 cm fiziksel heykel' / 'Job Heykeli' — teslim / kargo bilgisi kaynakta yok.",
    "**6 resim (O00–O05)** yeni çizildi (Skill & Master ile aynı stil, büyük yazı) — **hazır linkli** (itemiconrepo `forum/odul/resim/`, jsDelivr). R01 logo + 2 GIF ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for t, g, a, k in V.CSW: assert k in BB, k
for x in [*V.GENEL_TOPLAM, *V.CSW_TOPLAM, V.CLAN_TOPLAM, "30 cm", "100.000 NP", "22:00", "10 dakika", "60 dakika"]: assert x in BB, x
assert len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in ["R01", "O00", "O01", "O02", "O03", "O04", "O05", "GSAYIM", "GTAKVIM"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "oyun/rehber"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/odul/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
assert len(res) == len(RES)
import _repo_resim; _repo_resim.uygula(res)                       # itemiconrepo linkli
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "forum.sexyko.com/d/54 → FORUM/odul/kaynak_d54.txt + _odul_veri.py"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "ODUL_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "ODUL_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "ODUL_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("ODUL: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

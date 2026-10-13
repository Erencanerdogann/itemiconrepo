# -*- coding: utf-8 -*-
# HYPER BETA ODULLERI FORUM KONUSU (patron 7 Eki: Semih "forum.sexyko.com/d/54 bu konuyu da yapar misin, gorselli yaptin ya guzel oldu" +
# patron "skill ve master gibi yapacagiz, resimli detayli sekilde forum konu html'e ayni sekilde yazacagiz, bbcode vs hepsi olacak, resimleri repoya at linkle").
# Veri: _odul_veri.py (kaynak metne assert'li) · resimler: _odul_gorsel.py (O00-O05) + uzun konunun R01 logo + 2 GIF · cevirici: _konu_blok.py
# CIKTI: odul/ (konu.json, ODUL_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py sayfaya "Hyper Beta Odulleri" sekmesi olarak koyar.
# 13 Eki: `--en` -> Ingilizce (veri _odul_veri_en.py, resim odul/resim_en/, cikti konu_en.json + *_en.*). TR cikti degismez (md5 testi).
#         EN'de 2 GIF (geri sayim / takvim) YOK: icinde Turkce yazi var ("64BIT CLIENT ILE GERI DONUYOR", "16 EKIM BETA"); logo (A NEW WAR!) kalir.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB

EN = "--en" in sys.argv
if EN:
    import _odul_veri_en as V
    KB.DIL = "en"
else:
    import _odul_veri as V
TT = lambda tr, en: en if EN else tr          # her gorunen yazi: TT("turkce", "english")
SON_EK = "_en" if EN else ""

Y = KB.Y
OUT = V.OD; RD = os.path.join(OUT, "resim_en" if EN else "resim")
BASLIK = TT(f"🏆 SEXYKO HYPER BETA ÖDÜLLERİ | 4 CSW: {V.GENEL_TOPLAM[0]} + {V.GENEL_TOPLAM[1]} · Clan & Job Sıralaması · NP Çekilişi",   # 12 Eki: veriden
            f"🏆 SEXYKO HYPER BETA REWARDS | 4 CSW: {V.GENEL_TOPLAM[0]} + {V.GENEL_TOPLAM[1]} · Clan & Job Ranking · NP Raffle")
FIN = V.CSW[-1][2]                              # son CSW = final (dilden bagimsiz)

RES = {"R01": Y.RESIM["R01"]} if EN else {"R01": Y.RESIM["R01"], "GSAYIM": Y.RESIM["GSAYIM"], "GTAKVIM": Y.RESIM["GTAKVIM"]}
for rid, dosya, acik in [("O00", "O00_ozet.jpg", TT("Bir bakışta — 6 ödül başlığı", "At a glance — 6 reward headings")),
                         ("O01", "O01_takvim.jpg", TT("Beta CSW takvimi — 17 · 18 · 20 · 22 Ekim, 22:00", "Beta CSW schedule — 17 · 18 · 20 · 22 October, 22:00")),
                         ("O02", "O02_csw_odul.jpg", TT("Her CSW'de ödüller + toplamlar + ödül kuralı", "Rewards in each CSW + totals + reward rule")),
                         ("O03", "O03_clan.jpg", TT("Clan sıralama ödülleri", "Clan ranking rewards")),
                         ("O04", "O04_job.jpg", TT("Job sıralama ödülleri", "Job ranking rewards")),
                         ("O05", "O05_np_cekilis.jpg", TT("100.000+ NP Beta çekilişi", "100,000+ NP Beta raffle"))]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

bt, bs = V.BETA
if not EN: ekle("afis", "GSAYIM")
ekle("banner", "R01")
ekle("baslik", TT("HYPER BETA ÖDÜLLERİ", "HYPER BETA REWARDS"),
     TT(f"{bt} • {bs} — Clan sıralaması, Job sıralaması, 4 büyük Castle Siege War ve özel NP çekilişi",
        f"{bt} • {bs} — Clan ranking, Job ranking, 4 big Castle Siege Wars and a special NP raffle"))
ekle("icindekiler")
ekle("ayrac")

ekle("h", "🏆", TT("BİR BAKIŞTA", "AT A GLANCE"))
ekle("img", "O00", "")
ekle("p", TT("SexyKO HYPER Beta sürecinde rekabet **ilk günden** başlayacak. Beta boyunca oyuncularımızı **Clan sıralaması**, **Job sıralaması**, "
             "**4 büyük Castle Siege War** ve özel **NP çekilişi** bekliyor.",
             "In the SexyKO HYPER Beta, the competition starts **on day one**. Throughout the Beta, our players can look forward to the **Clan ranking**, "
             "the **Job ranking**, **4 big Castle Siege Wars** and a special **NP raffle**."))
ekle("ayrac")

ekle("h", "📅", TT("BETA CSW TAKVİMİ", "BETA CSW SCHEDULE"))
ekle("img", "O01", "")
if EN:
    KISA_AD = {"1st BETA CSW": "1st Beta CSW", "2nd BETA CSW": "2nd Beta CSW", "3rd BETA CSW": "3rd Beta CSW", "BETA FINAL CSW": "Beta Final CSW"}
else:
    KISA_AD = {"1. BETA CSW": "1. Beta CSW", "2. BETA CSW": "2. Beta CSW", "3. BETA CSW": "3. Beta CSW", "BETA FİNAL CSW": "Beta Final CSW"}   # kaynaktaki takvim yazimi
    for _a in KISA_AD.values(): assert _a in V.KAYNAK, _a
ekle("liste", [f"**{k} — 22:00** · {'👑' if a == FIN else '🏰'} {KISA_AD[a]}" for t, g, a, k in V.CSW])
ekle("p", TT(f"🕙 **CSW başlangıç saati: {V.CSW_SAAT['baslangic']}** · ⏳ **Hazırlık: {V.CSW_SAAT['hazirlik'].lower()}** · ⚔️ **Savaş: {V.CSW_SAAT['savas'].lower()}**",
             f"🕙 **CSW start time: {V.CSW_SAAT['baslangic']}** · ⏳ **Preparation: {V.CSW_SAAT['hazirlik'].lower()}** · ⚔️ **Battle: {V.CSW_SAAT['savas'].lower()}**"))
ekle("p", TT("Saat 22:00'de CSW hazırlık süreci başlayacaktır. İlk 10 dakika hazırlık süresi olarak geçecek, ardından Castle Siege War başlayacak ve "
             "savaş **maksimum 60 dakika** sürecektir.",
             "The CSW preparation phase starts at 22:00. The first 10 minutes are preparation time, then the Castle Siege War begins and "
             "the battle lasts **up to 60 minutes**."))
ekle("not", TT(f"**Beta Final CSW (22 Ekim Perşembe):** {V.FINAL_NOT}", f"**Beta Final CSW (Thursday, 22 October):** {V.FINAL_NOT}"))
ekle("ayrac")

ekle("h", "🏰", TT("CSW ÖDÜLLERİ (HER CSW'DE)", "CSW REWARDS (EACH CSW)"))
ekle("img", "O02", "")
ekle("liste", [f"{e} **{i}{TT('.', '.')} {a}** → " + (f"💵 **{tl}** + " if tl else "") + f"💎 **{sb}**" for i, (e, a, tl, sb) in enumerate(V.CSW_ODUL, 1)])   # 12 Eki: Kill nakit yok
ekle("p", TT(f"🏆 **4 CSW genel toplamı:** 💵 **{V.GENEL_TOPLAM[0]} nakit ödül** + 💎 **{V.GENEL_TOPLAM[1]}**",
             f"🏆 **4 CSW grand total:** 💵 **{V.GENEL_TOPLAM[0]} cash prize** + 💎 **{V.GENEL_TOPLAM[1]}**"))
ekle("not", TT("**CSW ödül kuralı:** ", "**CSW reward rule:** ") + " ".join(V.CSW_KURAL))
ekle("ayrac")

ekle("h", "👑", TT("CLAN SIRALAMA ÖDÜLLERİ", "CLAN RANKING REWARDS"))
ekle("img", "O03", "")
ekle("liste", [f"{e} **{a}** → 💎 **{sb}**" for e, a, sb in V.CLAN] + [TT(f"**Toplam** → 💎 **{V.CLAN_TOPLAM}**", f"**Total** → 💎 **{V.CLAN_TOPLAM}**")])
ekle("not", " ".join(V.CLAN_NOT))
ekle("ayrac")

ekle("h", "⚔️", TT("JOB SIRALAMA ÖDÜLLERİ", "JOB RANKING REWARDS"))
ekle("img", "O04", "")
ekle("p", f"**{' • '.join(V.JOBLAR)}** — {V.JOB_NOT}")
ekle("liste", [f"{e} **{a}** → " + " + ".join(("💵 " if x.endswith(" TL") else "💎 " if "SB" in x else "🗿 ") + f"**{x}**" for x in od) for e, a, od in V.JOB_ODUL])
ekle("ayrac")

ekle("h", "🎁", TT("100.000+ NP BETA ÇEKİLİŞİ", "100,000+ NP BETA RAFFLE"))
ekle("img", "O05", "")
ekle("p", TT(V.NP_SART.replace("100.000 NP ve üzeri", "**100.000 NP ve üzeri**"), V.NP_SART.replace("100,000 NP or more", "**100,000 NP or more**")))
ekle("liste", [f"{e} **{a}** → " + " + ".join(("💎 " if "SB" in x else "🗿 ") + f"**{x}**" for x in od) for e, a, od in V.NP])
ekle("ayrac")

ekle("h", "🚀", TT("23 EKİM 2026 — HYPER OFFICIAL", "23 OCTOBER 2026 — HYPER OFFICIAL"))
ekle("liste", [f"{e} [[{u}|{a}]]" for e, a, u in V.LINK] + [TT(f"📢 Konunun aslı: [[{V.KONU_URL}|forum.sexyko.com/d/54]]", f"📢 Original topic: [[{V.KONU_URL}|forum.sexyko.com/d/54]]")])
ekle("ayrac")
if not EN: ekle("afis", "GTAKVIM")
ekle("son", TT("🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥", "🔥 SEXYKO — WHERE PVP BEGINS 🔥"))

if EN:
    KONTROL = [
        "**Translation of the Turkish topic** (🏆 Hyper Beta Ödülleri, team reward table of 12 Oct). Data: `FORUM/_odul_veri_en.py` — every amount, date and rank is asserted equal to the Turkish data (`_odul_veri.py`).",
        "**Number format:** Turkish `20.000` → English `20,000`. Game terms kept as is: CSW, Clan, NP, SB, TL, Job names.",
        "**Not in the English version:** the 2 animated GIFs (countdown / calendar) — they contain Turkish text. The logo (A NEW WAR!) is English and stays.",
        "**Open points (same as Turkish):** Job 4th place reward not in the source · Job 5th–10th removed in the 12 Oct table · statue delivery info not in the source.",
        "**6 images (O00–O05)** drawn in English (`odul/resim_en/`, same style as Turkish).",
    ]
else:
    KONTROL = [
        "**12 Eki güncelleme (ekibin yeni ödül tablosu, `FORUM/odul/kaynak_tablo_12eki.txt`):** tutarlar bu tablodan, satır satır assert'li. "
        "En Çok Kill Alan Clan → **20.000 SB** (nakit yok) · 2. kategori adı **En Çok Taşı Alan Clan** · 4 CSW toplamı **120.000 TL + 200.000 SB** (4 × 30.000 TL / 4 × 50.000 SB). "
        "Her CSW'de toplam satırı tabloda yok → konudan çıktı.",
        "**Job 5.–10. sıra (kişi başı 250 SB) yeni tabloda YOK → konudan çıkarıldı** — kaldırıldı mı, unutuldu mu ekip teyit etsin (forumda hâlâ var).",
        "**Tablonun hatalı toplamları konuya KONMADI:** 5 Job nakit 22.500 (doğrusu 17.500) · genel nakit 142.500 (doğrusu 137.500) · çekiliş heykel 10 adet (doğrusu 2) · toplam heykel 15 adet (doğrusu 7).",
        f"**Tarih / saat / kural cümleleri:** forum.sexyko.com/d/54 (5 Eki 2026) — 7 Eki 05:29'da okundu, `FORUM/odul/kaynak_d54.txt` (`_odul_veri.py` assert). Beta 16 Ekim · Official 23 Ekim.",
        "**Kaynakta YOK → konuda da yok:** Job sıralamasında **4. sıra** ödülü (tabloda 3.'den sonra yok) — ekip sorulsun.",
        "Job listesi kaynaktaki gibi **Priest • Warrior • Rogue • Kurian • Mage** (Rogue tek job; Assassin / Okçu ayrımı kaynakta yok).",
        "Heykel: kaynakta 'Job'a özel 30 cm fiziksel heykel' / 'Job Heykeli' — teslim / kargo bilgisi kaynakta yok.",
        "**6 resim (O00–O05)** yeni çizildi (Skill & Master ile aynı stil, büyük yazı) — **hazır linkli** (itemiconrepo `forum/odul/resim/`, jsDelivr). R01 logo + 2 GIF ortak.",
    ]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for t, g, a, k in V.CSW: assert k in BB, k
for x in [*V.GENEL_TOPLAM, V.CLAN_TOPLAM, "30 cm", "22:00"] + (["100,000 NP", "10 minutes", "60 minutes"] if EN else ["100.000 NP", "10 dakika", "60 dakika"]): assert x in BB, x
if EN:                                                                        # Ingilizce metinde Turkce harf kalmasin
    import re as _re
    _tr = _re.findall(r"\S*[çğıöşüÇĞİÖŞÜ]\S*", _re.sub(r"\[/?[A-Z]+[^\]]*\]", " ", BB + "\n" + BASLIK))
    assert not _tr, _tr[:8]
assert len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in (["R01", "O00", "O01", "O02", "O03", "O04", "O05"] + ([] if EN else ["GSAYIM", "GTAKVIM"])):
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "oyun/rehber"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya=f"FORUM/odul/{'resim_en' if EN else 'resim'}/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
assert len(res) == len(RES)
import _repo_resim; _repo_resim.uygula(res)                       # itemiconrepo linkli
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": TT("forum.sexyko.com/d/54 → FORUM/odul/kaynak_d54.txt + _odul_veri.py", "FORUM/_odul_veri_en.py (= _odul_veri.py, asserted)")}
json.dump(VERI, open(os.path.join(OUT, f"konu{SON_EK}.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, f"ODUL_KONU_bbcode{SON_EK}.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, f"ODUL_KONU_markdown{SON_EK}.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, f"ODUL_KONU_duz{SON_EK}.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("ODUL" + SON_EK.upper() + ": bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

# -*- coding: utf-8 -*-
# HYPER BETA REWARDS — ENGLISH DATA (patron 13 Eki: "FORUM_KONU.html eng versiyonu lazim, resimler vs dahil").
# Ayni yapi _odul_veri.py ile (TR = tek kaynak). Rakamlar / sayilar / sira TR'den birebir (import'ta assert) — sadece dil degisir.
# Sayi bicimi: TR "20.000" -> EN "20,000". Oyun terimleri (CSW, Clan, NP, SB, TL, Job adlari) aynen kalir.
import re
import _odul_veri as TR

KAYNAK = TR.KAYNAK
OD = TR.OD
KONU_URL = TR.KONU_URL
DIL = "en"

BETA = ("16 October 2026", "22:00")
OFFICIAL = "23 OCTOBER 2026"
CSW_SAAT = {"baslangic": "22:00", "hazirlik": "10 Minutes", "savas": "60 Minutes"}
# (tarih, gun, ad, kisa_tarih) — TR.CSW ile ayni sira
CSW = [("17 OCTOBER 2026", "SATURDAY", "1st BETA CSW", "17 October, Saturday"), ("18 OCTOBER 2026", "SUNDAY", "2nd BETA CSW", "18 October, Sunday"),
       ("20 OCTOBER 2026", "TUESDAY", "3rd BETA CSW", "20 October, Tuesday"), ("22 OCTOBER 2026", "THURSDAY", "BETA FINAL CSW", "22 October, Thursday")]
FINAL_NOT = "Just 1 day before the Official launch, the last Castle Siege War of the Beta period will take place."
CSW_ODUL = [("🏰", "Castle Owner Clan", "20,000 TL", "20,000 SB"), ("👑", "Clan with Most Stone Captures", "10,000 TL", "10,000 SB"),
            ("⚔️", "Clan with Most Kills", None, "20,000 SB")]
GENEL_TOPLAM = ("120,000 TL", "200,000 SB")
CSW_KURAL = ["In each CSW, a Clan can win a reward from only 1 reward category.",
             "Once a Clan wins a reward in any category, it is removed from the other reward categories of the same CSW.",
             "This way, the goal is for different Clans to win rewards in each CSW."]
CLAN = [("🥇", "1st Clan", "30,000 SB"), ("🥈", "2nd Clan", "20,000 SB"), ("🥉", "3rd Clan", "10,000 SB")]
CLAN_TOPLAM = "60,000 SB"
CLAN_NOT = ["The overall Clan NP ranking at the end of the Beta period will be used.", "Only the overall Clan ranking counts, regardless of race."]
JOBLAR = list(TR.JOBLAR)
JOB_NOT = "During the Beta, each Job is ranked separately."
JOB_ODUL = [("🥇", "Each Job's 1st", ["2,500 TL", "2,500 SB", "Job-exclusive 30 cm physical statue"]),
            ("🥈", "Each Job's 2nd", ["1,000 TL", "2,000 SB"]),
            ("🥉", "Each Job's 3rd", ["2,000 SB"])]
NP_SART = "Players who earn 100,000 NP or more during the Beta qualify for the special Beta raffle."
NP = [("🥇", "1st Player", ["Job Statue", "1,000 SB"]), ("🥈", "2nd Player", ["Job Statue"]), ("🥉", "3rd Player", ["1,000 SB"]),
      ("🎖️", "4th Player", ["500 SB"]), ("🎖️", "5th–10th Players", ["250 SB per player"])]
LINK = list(TR.LINK)
KISI_BASI = "per player"          # para(): "Kişi başı" karsiligi (SB rengi)


# ---------- dogrulama: EN yapi + rakamlar TR ile birebir (ceviri sirasinda rakam kaymasin)
def _sayi(s):
    return None if s is None else int(s.split()[0].replace(",", "").replace(".", "")) if s[0].isdigit() else s
def _rakamlar(liste):                                   # metindeki tum sayilar (TR "Kisi basi 250 SB" = EN "250 SB per player")
    return [int(m.replace(",", "").replace(".", "")) for x in liste if x for m in re.findall(r"\d[\d.,]*\d|\d", x)]

assert len(CSW) == len(TR.CSW) and [c[0].split()[0] for c in CSW] == [c[0].split()[0] for c in TR.CSW]           # gunler 17/18/20/22
assert [(e, _sayi(tl), _sayi(sb)) for e, a, tl, sb in CSW_ODUL] == [(e, _sayi(tl), _sayi(sb)) for e, a, tl, sb in TR.CSW_ODUL]
assert [_sayi(x) for x in GENEL_TOPLAM] == [_sayi(x) for x in TR.GENEL_TOPLAM]
assert [(e, _sayi(sb)) for e, a, sb in CLAN] == [(e, _sayi(sb)) for e, a, sb in TR.CLAN] and _sayi(CLAN_TOPLAM) == _sayi(TR.CLAN_TOPLAM)
assert len(CSW_KURAL) == len(TR.CSW_KURAL) and len(CLAN_NOT) == len(TR.CLAN_NOT)
assert [(e, _rakamlar(od)) for e, a, od in JOB_ODUL] == [(e, _rakamlar(od)) for e, a, od in TR.JOB_ODUL]
assert [(e, _rakamlar(od), len(od)) for e, a, od in NP] == [(e, _rakamlar(od), len(od)) for e, a, od in TR.NP]
assert BETA[1] == TR.BETA[1] and BETA[0].split()[0] == TR.BETA[0].split()[0] and OFFICIAL.split()[0] == TR.OFFICIAL.split()[0]
assert CSW_SAAT["baslangic"] == TR.CSW_SAAT["baslangic"]
for s in [*CSW_KURAL, *CLAN_NOT, JOB_NOT, NP_SART, FINAL_NOT]:
    assert not any(ch in s for ch in "çğıöşüÇĞİÖŞÜ"), s                                                  # Turkce harf kalmasin

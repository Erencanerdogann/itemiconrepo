# -*- coding: utf-8 -*-
# HYPER BETA ODULLERI — VERI (patron 7 Eki: Semih'in istegi "forum.sexyko.com/d/54 bu konuyu da yapar misin, gorselli yaptin ya guzel oldu" +
# "skill ve master gibi yapacagiz, resimli detayli, forum konu html'e ayni sekilde, bbcode vs hepsi").
# KAYNAK: odul/kaynak_d54.txt (forum.sexyko.com/d/54, Flarum API, 7 Eki 05:29) — ASAGIDAKI HER METIN KAYNAKTA BIREBIR VAR (import'ta assert).
# Kaynakta olmayan bilgi EKLENMEZ (ornek: Job 4. sirasi kaynakta yok -> konuda da yok, KONTROL'de not).
# 12 Eki PATRON: ekibin yeni odul tablosu (odul/kaynak_tablo_12eki.txt) -> TUTARLAR bu tablodan (assert): Kill Clan 20.000 SB (TL yok),
# 2. kategori "En Cok Tasi Alan Clan", 4 CSW 120.000 TL + 200.000 SB, Job 5.-10. sira tabloda yok -> cikti. Tarih/saat/cumleler eski kaynaktan (tabloda yok).
# Tablonun hatali toplamlari (5 Job nakit 22.500, genel 142.500, heykel 10 / 15) KONUYA KONMAZ.
import os, re

KOK = os.path.dirname(os.path.abspath(__file__))
OD = os.path.join(KOK, "odul")
KAYNAK = open(os.path.join(OD, "kaynak_d54.txt"), encoding="utf-8").read()
TABLO = open(os.path.join(OD, "kaynak_tablo_12eki.txt"), encoding="utf-8").read()   # 12 Eki tutarlar
KONU_URL = "https://forum.sexyko.com/d/54"

BETA = ("16 Ekim 2026", "22:00")
OFFICIAL = "23 EKİM 2026"
CSW_SAAT = {"baslangic": "22:00", "hazirlik": "10 Dakika", "savas": "60 Dakika"}
# (tarih, gun, ad, kisa_tarih) — kisa_tarih takvim bolumundeki yazim
CSW = [("17 EKİM 2026", "CUMARTESİ", "1. BETA CSW", "17 Ekim Cumartesi"), ("18 EKİM 2026", "PAZAR", "2. BETA CSW", "18 Ekim Pazar"),
       ("20 EKİM 2026", "SALI", "3. BETA CSW", "20 Ekim Salı"), ("22 EKİM 2026", "PERŞEMBE", "BETA FİNAL CSW", "22 Ekim Perşembe")]
FINAL_NOT = "Official açılıştan yalnızca 1 gün önce, Beta döneminin son Castle Siege War mücadelesi gerçekleşecek."
# her CSW'de ayni 3 kategori: (emoji, ad, TL, SB)
# 12 Eki tablo: Kill Clan nakit YOK (None) + 20.000 SB · 2. kategori adi "En Cok Tasi Alan Clan"
CSW_ODUL = [("🏰", "Kale Sahibi Clan", "20.000 TL", "20.000 SB"), ("👑", "En Çok Taşı Alan Clan", "10.000 TL", "10.000 SB"),
            ("⚔️", "En Çok Kill Alan Clan", None, "20.000 SB")]
GENEL_TOPLAM = ("120.000 TL", "200.000 SB")      # 4 CSW (tablo "4 CSW Toplamı"); her-CSW toplami tabloda yok -> konuda yok
CSW_KURAL = ["Her CSW'de bir Clan yalnızca 1 ödül kategorisinden ödül kazanabilir.",
             "Bir Clan herhangi bir kategoride ödül kazandığında, aynı CSW içerisindeki diğer ödül kategorilerinden çıkarılır.",
             "Böylece her CSW'de farklı Clanların ödül kazanması hedeflenmektedir."]
CLAN = [("🥇", "1. Clan", "30.000 SB"), ("🥈", "2. Clan", "20.000 SB"), ("🥉", "3. Clan", "10.000 SB")]
CLAN_TOPLAM = "60.000 SB"
CLAN_NOT = ["Beta süreci sonunda genel Clan NP sıralaması esas alınacaktır.", "Irk fark etmeksizin yalnızca genel Clan sıralaması dikkate alınacaktır."]
JOBLAR = ["Priest", "Warrior", "Rogue", "Kurian", "Mage"]
JOB_NOT = "Beta boyunca her Job kendi içerisinde ayrı değerlendirilecektir."
JOB_ODUL = [("🥇", "Her Job 1.'si", ["2.500 TL", "2.500 SB", "Job'a özel 30 cm fiziksel heykel"]),
            ("🥈", "Her Job 2.'si", ["1.000 TL", "2.000 SB"]),
            ("🥉", "Her Job 3.'sü", ["2.000 SB"])]          # 12 Eki tablo: 5.-10. sira (250 SB) yok -> cikti
NP_SART = "Beta boyunca 100.000 NP ve üzeri kasan oyuncular özel Beta çekilişine katılma hakkı kazanacaktır."
NP = [("🥇", "1. Kişi", ["Job Heykeli", "1.000 SB"]), ("🥈", "2. Kişi", ["Job Heykeli"]), ("🥉", "3. Kişi", ["1.000 SB"]),
      ("🎖️", "4. Kişi", ["500 SB"]), ("🎖️", "5.–10. Kişiler", ["Kişi başı 250 SB"])]
LINK = [("🌐", "www.sexyko.com", "https://www.sexyko.com"), ("💬", "discord.gg/sexyko", "https://discord.gg/sexyko")]


# ---------- dogrulama: her metin kaynakta birebir (bosluklar tek)
def _n(s): return re.sub(r"\s+", " ", s).strip()
_K = _n(KAYNAK)
def _var(s):
    assert _n(s) in _K, f"KAYNAKTA YOK: {s!r}"

for s in ["16 Ekim 2026 • 22:00", "🕙 CSW Başlangıç Saati: 22:00", "⏳ Hazırlık Süresi: 10 Dakika", "⚔️ Savaş Süresi: 60 Dakika", FINAL_NOT, OFFICIAL]: _var(s)
for t, g, a, k in CSW:
    _var(f"{t} — {g}"); _var(a); _var(f"{k} — 22:00")
# 12 Eki: tutarlar tablodan (satir birebir)
_T = _n(TABLO)
def _tab(s):
    assert _n(s) in _T, f"TABLODA YOK: {s!r}"
_tab("CSW Kale Sahibi 20.000 20.000 Her CSW için"); _tab("CSW En Çok Taşı Alan Clan 10.000 10.000 Her CSW için")
_tab("CSW En Çok Kill Alan Clan 20.000 Her CSW için"); _tab("4 CSW Toplamı 120.000 200.000")
_tab("CSW Tarihleri: 17 • 18 • 20 • 22 Ekim 2026")
assert [x[2] for x in CSW_ODUL] == ["20.000 TL", "10.000 TL", None] and [x[3] for x in CSW_ODUL] == ["20.000 SB", "10.000 SB", "20.000 SB"]
for i, (sb, ad) in enumerate([("30.000", "1."), ("20.000", "2."), ("10.000", "3.")]):
    _tab(f"Clan Sıralaması {ad} {sb} En Çok NP Basan Clan"); assert CLAN[i][2] == sb + " SB"
_tab("Her Job için 1. 2.500 2.500 Job'a özel 30 cm heykel"); _tab("Her Job için 2. 1.000 2.000"); _tab("Her Job için 3. 2.000 Joblar:")
assert "Her Job 5" not in TABLO and "Her Job için 5" not in TABLO                                  # job 5.-10. tabloda yok
for s in ["1. Job Heykeli + 1.000 SB 1.000", "2. Job Heykeli 1 adet", "3. 1.000 SB 1.000", "4. 500 SB 500", "5.–10. Kişi başı 250 SB 1.500"]: _tab(s)
for s in CSW_KURAL + CLAN_NOT + [JOB_NOT, NP_SART]: _var(s)
for e, a, sb in CLAN: _var(f"{e} {a}")
_var(f"Toplam 💎 {CLAN_TOPLAM}")
_var(" • ".join(JOBLAR))
for e, a, od in JOB_ODUL + NP:
    _var(f"{e} {a}")
    for x in od: _var(x)
for e, a, u in LINK: _var(a)
# toplamlar kaynaktaki tek tek odullerle tutarli mi (yanlis kopyalama yakalansin)
_tl = lambda s: int(s.split()[0].replace(".", ""))
assert 4 * sum(_tl(x[2]) for x in CSW_ODUL if x[2]) == _tl(GENEL_TOPLAM[0]) and 4 * sum(_tl(x[3]) for x in CSW_ODUL) == _tl(GENEL_TOPLAM[1])
assert sum(_tl(x[2]) for x in CLAN) == _tl(CLAN_TOPLAM)
assert "4. Sıra" not in KAYNAK and "Her Job 4." not in KAYNAK                                     # job 4. sirasi kaynakta yok (konuda da yok)

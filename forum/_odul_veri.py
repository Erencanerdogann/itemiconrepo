# -*- coding: utf-8 -*-
# HYPER BETA ODULLERI — VERI (patron 7 Eki: Semih'in istegi "forum.sexyko.com/d/54 bu konuyu da yapar misin, gorselli yaptin ya guzel oldu" +
# "skill ve master gibi yapacagiz, resimli detayli, forum konu html'e ayni sekilde, bbcode vs hepsi").
# KAYNAK: odul/kaynak_d54.txt (forum.sexyko.com/d/54, Flarum API, 7 Eki 05:29) — ASAGIDAKI HER METIN KAYNAKTA BIREBIR VAR (import'ta assert).
# Kaynakta olmayan bilgi EKLENMEZ (ornek: Job 4. sirasi kaynakta yok -> konuda da yok, KONTROL'de not).
import os, re

KOK = os.path.dirname(os.path.abspath(__file__))
OD = os.path.join(KOK, "odul")
KAYNAK = open(os.path.join(OD, "kaynak_d54.txt"), encoding="utf-8").read()
KONU_URL = "https://forum.sexyko.com/d/54"

BETA = ("16 Ekim 2026", "22:00")
OFFICIAL = "23 EKİM 2026"
CSW_SAAT = {"baslangic": "22:00", "hazirlik": "10 Dakika", "savas": "60 Dakika"}
# (tarih, gun, ad, kisa_tarih) — kisa_tarih takvim bolumundeki yazim
CSW = [("17 EKİM 2026", "CUMARTESİ", "1. BETA CSW", "17 Ekim Cumartesi"), ("18 EKİM 2026", "PAZAR", "2. BETA CSW", "18 Ekim Pazar"),
       ("20 EKİM 2026", "SALI", "3. BETA CSW", "20 Ekim Salı"), ("22 EKİM 2026", "PERŞEMBE", "BETA FİNAL CSW", "22 Ekim Perşembe")]
FINAL_NOT = "Official açılıştan yalnızca 1 gün önce, Beta döneminin son Castle Siege War mücadelesi gerçekleşecek."
# her CSW'de ayni 3 kategori: (emoji, ad, TL, SB)
CSW_ODUL = [("🏰", "Kale Sahibi Clan", "20.000 TL", "20.000 SB"), ("👑", "En Çok Kale Alan Clan", "10.000 TL", "10.000 SB"),
            ("⚔️", "En Çok Kill Alan Clan", "20.000 TL", "10.000 SB")]
CSW_TOPLAM = ("50.000 TL", "40.000 SB")          # her CSW
GENEL_TOPLAM = ("200.000 TL", "160.000 SB")      # 4 CSW
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
            ("🥉", "Her Job 3.'sü", ["2.000 SB"]),
            ("🎖️", "Her Job 5.–10. Sıraları", ["Kişi başı 250 SB"])]
JOB_5_10 = "5. • 6. • 7. • 8. • 9. • 10. sıradaki oyuncuların her biri 250 SB kazanacaktır."
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
for e, a, tl, sb in CSW_ODUL:
    _var(f"{a} 💵 {tl} 💎 {sb}")
assert _n(KAYNAK).count("Kale Sahibi Clan 💵 20.000 TL 💎 20.000 SB") == 4                      # 4 CSW'de ayni oduller
_var(f"💵 {CSW_TOPLAM[0]} Nakit"); _var(f"💎 {CSW_TOPLAM[1]}"); _var(f"💵 {GENEL_TOPLAM[0]} Nakit Ödül"); _var(f"💎 {GENEL_TOPLAM[1]}")
for s in CSW_KURAL + CLAN_NOT + [JOB_NOT, JOB_5_10, NP_SART]: _var(s)
for e, a, sb in CLAN: _var(f"{e} {a} 💎 {sb}")
_var(f"Toplam 💎 {CLAN_TOPLAM}")
_var(" • ".join(JOBLAR))
for e, a, od in JOB_ODUL + NP:
    _var(f"{e} {a}")
    for x in od: _var(x)
for e, a, u in LINK: _var(a)
# toplamlar kaynaktaki tek tek odullerle tutarli mi (yanlis kopyalama yakalansin)
_tl = lambda s: int(s.split()[0].replace(".", ""))
assert sum(_tl(x[2]) for x in CSW_ODUL) == _tl(CSW_TOPLAM[0]) and sum(_tl(x[3]) for x in CSW_ODUL) == _tl(CSW_TOPLAM[1])
assert 4 * _tl(CSW_TOPLAM[0]) == _tl(GENEL_TOPLAM[0]) and 4 * _tl(CSW_TOPLAM[1]) == _tl(GENEL_TOPLAM[1])
assert sum(_tl(x[2]) for x in CLAN) == _tl(CLAN_TOPLAM)
assert "4. Sıra" not in KAYNAK and "Her Job 4." not in KAYNAK                                     # job 4. sirasi kaynakta yok (konuda da yok)

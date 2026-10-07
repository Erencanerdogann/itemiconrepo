# -*- coding: utf-8 -*-
# SEZON SISTEMI (ACADEMY) — VERI (patron 7 Eki: tablo resmi "bu da forum-konu sekmesine eklenecek, bunu da guzelce yaz, guzel bir academy rehberi olsun"
# + kararlar: 8 sezon (tablo) · GB alimi "her sezon ayri, 1. sezondan basliyor 8'e kadar" · ad "Sezon Sistemi (Academy)").
# KAYNAK: sezon/kaynak_tablo.md (patron tablosu — tarih, oran, GB, turnuva) + sezon/kaynak_d57.txt (forum.sexyko.com/d/57 — aciklama metinleri).
# Her tarih iki kaynakta birebir + takvim kurali (28 gunde bir Cuma, birlesim +10 gun, turnuva kaydi +3 gun) hesapla dogrulanir (import'ta assert).
import os, re, datetime

KOK = os.path.dirname(os.path.abspath(__file__))
SZ = os.path.join(KOK, "sezon")
TABLO = open(os.path.join(SZ, "kaynak_tablo.md"), encoding="utf-8").read()
FORUM = open(os.path.join(SZ, "kaynak_d57.txt"), encoding="utf-8").read()
KONU_URL = "https://forum.sexyko.com/d/57"
AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUN = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

OFFICIAL = "23 Ekim 2026"
KURAL_SATIR = "Official: 23 Ekim 2026 • Sezon açılışları 28 günde bir Cuma 22:00 • Bitiş/Birleşim sonraki haftanın Pazartesi 22:00"
# (no, acilis, oran %) — birlesim ve turnuva kaydi tarihten hesaplanir, kaynaklarla karsilastirilir
_SEZ = [(1, "20.11.2026", 100), (2, "18.12.2026", 200), (3, "15.01.2027", 300), (4, "12.02.2027", 400),
        (5, "12.03.2027", 500), (6, "09.04.2027", 600), (7, "07.05.2027", 700), (8, "04.06.2027", 800)]


def _t(s): return datetime.datetime.strptime(s, "%d.%m.%Y").date()
def uzun(d): return f"{d.day} {AY[d.month - 1]} {d.year}"          # '20 Kasım 2026'
def kisa(d): return d.strftime("%d.%m.%Y")                           # '20.11.2026'
def gun(d): return GUN[d.weekday()]


SEZON = []
for no, ac, oran in _SEZ:
    a = _t(ac); tk = a + datetime.timedelta(days=3); br = a + datetime.timedelta(days=10)
    SEZON.append({"no": no, "acilis": a, "turnuva": tk, "birlesim": br, "oran": oran})

GB = "Sezon başladığında BursaGB.com üzerinden GB alımı yapılacaktır. (Serverın durumuna göre değişebilir.)"
GB_PATRON = "Her sezon için ayrı — 1. sezondan başlayıp 8. sezona kadar"
TURNUVA_KAYIT = "Sezon Cuma günü açılır. Pazartesi saat 12:00'de turnuva kayıtları başlar."
TURNUVA_ACIK = "Sezon kapandığında, yani birleşim gününde turnuva açıklanır."
# forum d/57 aciklama metinleri (birebir)
GIRIS = ["SexyKO’da rekabeti yıl boyunca canlı tutacak Sezon Sistemi başlıyor.",
         "Her sezon, yeni başlayan oyuncuların ana sunucuya daha hızlı yetişebilmesi için artırılmış EXP • DROP • COIN oranlarıyla açılacak.",
         "Sezon tamamlandığında oyuncular gelişimleriyle birlikte ana SexyKO sunucusuna aktarılacak."]
SLOGAN = "Yeni Mücadele • Hızlandırılmış Gelişim • Ana Sunucuyla Birleşim"
ADIM = [("01", "SEZON AÇILIŞI", "Her yeni sezon Cuma günü saat 22:00’da açılır."),
        ("02", "HIZLANDIRILMIŞ GELİŞİM", "Sezon sunucularında EXP, DROP ve COIN oranları artırılmıştır."),
        ("03", "KADEMELİ ORANLAR", "İlk sezon %100 ile başlar. İlerleyen sezonlarda oranlar kademeli olarak %800’e kadar yükselir."),
        ("04", "TURNUVA KAYITLARI", "Sezon başladıktan sonraki Pazartesi günü saat 12:00’da turnuva kayıtları açılır."),
        ("05", "ANA SUNUCUYLA BİRLEŞİM", "Sezon tamamlandığında oyuncular gelişimleriyle birlikte ana SexyKO sunucusuna aktarılır.")]
TURNUVA = [("📌", "Kayıt Başlangıcı: Pazartesi • 12:00"), ("📌", "Turnuva Duyurusu: Birleşim Günü"), ("📌", "Eşleşmeler: Birleşim sonrası açıklanacaktır.")]
TURNUVA_NOT = "Turnuva sistemiyle ilgili ödüller ve detaylar ayrıca duyurulacaktır."
MUCADELE = ["Yeni oyuncular için daha hızlı gelişim.", "Eski oyuncular için yeni rakipler.", "Her sezon daha yüksek oranlar.", "Her sezon sonunda tek bir sunucu."]
BULUSMA = "HERKES ANA SUNUCUDA BULUŞACAK."
LINK = [("🌐", "www.sexyko.com", "https://www.sexyko.com"), ("💬", "discord.gg/sexyko", "https://discord.gg/sexyko")]


# ---------- dogrulama
def _n(s): return re.sub(r"\s+", " ", s.replace("　", " ")).strip()
_T, _F = _n(TABLO), _n(FORUM)
for s in [KURAL_SATIR, GB, TURNUVA_KAYIT, TURNUVA_ACIK]: assert _n(s) in _T, f"TABLODA YOK: {s!r}"
for s in GIRIS + [SLOGAN, TURNUVA_NOT, BULUSMA] + MUCADELE + [x[2] for x in ADIM] + [x[1] for x in TURNUVA] + [x[1] for x in LINK]:
    assert _n(s) in _F, f"FORUMDA YOK: {s!r}"
for i, z in enumerate(SEZON):
    a, tk, br = z["acilis"], z["turnuva"], z["birlesim"]
    assert gun(a) == "Cuma" and gun(tk) == "Pazartesi" and gun(br) == "Pazartesi", z
    if i: assert (a - SEZON[i - 1]["acilis"]).days == 28, ("28 gun kurali", z)
    # tablo: '| Sezon 1 | 20.11.2026 Cuma · 22:00 | 30.11.2026 Pazartesi · 22:00 | %100 | %100 | %100 |'
    assert _n(f"| Sezon {z['no']} | {kisa(a)} Cuma · 22:00 | {kisa(br)} Pazartesi · 22:00 | %{z['oran']} | %{z['oran']} | %{z['oran']} |") in _T, ("tablo", z["no"])
    # forum: 'SEZON 01 20 Kasım 2026 • Cuma • 22:00 EXP %100 • DROP %100 • COIN %100 🏆 Turnuva Kayıtları 23 Kasım 2026 • Pazartesi • 12:00 🔄 ... 30 Kasım 2026 • Pazartesi • 22:00'
    assert _n(f"SEZON {z['no']:02d} {uzun(a)} • Cuma • 22:00 EXP %{z['oran']} • DROP %{z['oran']} • COIN %{z['oran']} 🏆 Turnuva Kayıtları "
              f"{uzun(tk)} • Pazartesi • 12:00 🔄 Ana Sunucuyla Birleşim {uzun(br)} • Pazartesi • 22:00") in _F, ("forum", z["no"])
assert len(SEZON) == 8 and SEZON[-1]["oran"] == 800

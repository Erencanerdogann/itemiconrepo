# -*- coding: utf-8 -*-
# SEZON SISTEMI (ACADEMY) FORUM KONUSU (patron 7 Eki: tablo resmi "bu da forum-konu sekmesine eklenecek, bunu da guzelce yaz, resimle, guzel bir academy rehberi olsun"
# + kararlar: 8 sezon · GB her sezon ayri (1-8) · ad "Sezon Sistemi (Academy)").
# Veri: _sezon_veri.py (tablo + forum d/57'ye assert'li) · resimler: _sezon_gorsel.py (Z00-Z04) + uzun konunun R01 logo + takvim GIF · cevirici: _konu_blok.py
# CIKTI: sezon/ (konu.json, SEZON_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py "Sezon Sistemi (Academy)" sekmesi.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _sezon_veri as V

Y = KB.Y
OUT = V.SZ; RD = os.path.join(OUT, "resim")
BASLIK = "⚔️ SEXYKO SEZON SİSTEMİ (ACADEMY) | 8 Sezon Takvimi · EXP/DROP/COIN %100 → %800 · Turnuva"

RES = {"R01": Y.RESIM["R01"], "GTAKVIM": Y.RESIM["GTAKVIM"]}
for rid, dosya, acik in [("Z00", "Z00_ozet.jpg", "Sezon Sistemi — bir bakışta"), ("Z01", "Z01_takvim.jpg", "2026 – 2027 sezon takvimi (8 sezon)"),
                         ("Z02", "Z02_akis.jpg", "Bir sezonun akışı"), ("Z03", "Z03_oran.jpg", "Kademeli oranlar %100 → %800"),
                         ("Z04", "Z04_turnuva_gb.jpg", "Turnuva + GB alımı")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

ekle("banner", "R01")
ekle("baslik", "SEZON SİSTEMİ (ACADEMY)", V.SLOGAN)
ekle("icindekiler")
ekle("ayrac")

ekle("h", "⚔️", "SEZON SİSTEMİ NEDİR?")
ekle("img", "Z00", "")
for s in V.GIRIS: ekle("p", s.replace("Sezon Sistemi", "**Sezon Sistemi**").replace("EXP • DROP • COIN", "**EXP • DROP • COIN**").replace("ana SexyKO sunucusuna", "**ana SexyKO sunucusuna**"))
ekle("ayrac")

ekle("h", "📅", "2026 – 2027 SEZON TAKVİMİ")
ekle("img", "Z01", "")
for z in V.SEZON:                                                  # 7 Eki PATRON "burasi cok kotu olmus": tek uzun satir yerine sezon basina 4 kisa satir (d/57 duzeni)
    ekle("satirlar", [f"🟢 **SEZON {z['no']:02d}** — EXP / DROP / COIN **%{z['oran']}**", f"📅 Açılış: **{V.kisa(z['acilis'])} Cuma 22:00**",
                      f"🏆 Turnuva kaydı: {V.kisa(z['turnuva'])} Pazartesi 12:00", f"🔄 Birleşim: **{V.kisa(z['birlesim'])} Pazartesi 22:00**"])
ekle("not", f"Official **{V.OFFICIAL}** · sezon açılışları **28 günde bir Cuma 22:00** · bitiş / birleşim **sonraki haftanın Pazartesi 22:00** · saatler TSİ")
ekle("ayrac")

ekle("h", "🔁", "SEZON NASIL ÇALIŞIR?")
ekle("img", "Z02", "")
ekle("liste", [f"**{no} — {ad}:** {m}" for no, ad, m in V.ADIM])
ekle("ayrac")

ekle("h", "📈", "KADEMELİ ORANLAR")
ekle("img", "Z03", "")
ekle("p", "İlk sezon **%100** ile başlar; her sezon **EXP · DROP · COIN** birlikte bir kademe yükselir: "
          + " → ".join(f"S{z['no']:02d} %{z['oran']}" for z in V.SEZON) + ".")
ekle("ayrac")

ekle("h", "🏆", "TURNUVA SİSTEMİ")
ekle("img", "Z04", "")
ekle("liste", [f"{i} **{t.split(':')[0]}:**{t.split(':', 1)[1]}" for i, t in V.TURNUVA])
ekle("p", f"{V.TURNUVA_KAYIT} {V.TURNUVA_ACIK}")
ekle("not", V.TURNUVA_NOT)
ekle("ayrac")

ekle("h", "💰", "GB ALIMI")
ekle("liste", ["🛒 **BursaGB.com** üzerinden — resmi çözüm ortağı", "📅 **Sezon başladığında** GB alımı yapılır", f"🔁 **{V.GB_PATRON}**",
               "⚠️ Serverın durumuna göre değişebilir."])
ekle("ayrac")

ekle("h", "🔥", "HER SEZON YENİ BİR MÜCADELE")
ekle("liste", V.MUCADELE)
ekle("p", f"⚔️ **{V.BULUSMA}**")
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", [f"{e} [[{u}|{a}]]" for e, a, u in V.LINK] + [f"📢 Forum: [[{V.KONU_URL}|forum.sexyko.com/d/57 — Sezon Sistemi]]"])
ekle("ayrac")
ekle("afis", "GTAKVIM")
ekle("son", "🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥")

KONTROL = [
    "**Kaynak:** patronun tablosu (`FORUM/sezon/kaynak_tablo.md`, 7 Eki) + forum.sexyko.com/d/57 (`kaynak_d57.txt`, açıklama metinleri). 8 sezonun bütün tarihleri iki kaynakta birebir; "
    "takvim kuralı (28 günde bir Cuma · turnuva kaydı +3 gün Pazartesi · birleşim +10 gün Pazartesi) hesapla doğrulandı (`_sezon_veri.py` assert).",
    "**Patron kararları (7 Eki):** 8 sezon (forum d/57'deki Sezon 09 – 10 konuda YOK) · GB alımı her sezon ayrı (1 → 8) · ad 'Sezon Sistemi (Academy)'.",
    "**Çelişki:** GB alımı — tablo 'sezon başladığında … (serverın durumuna göre değişebilir)', forum d/57 'her yeni sezon başlamadan önce' → konuda TABLO yazımı.",
    "**Forum d/57'ye düzeltme:** konunun en sonunda yapay zekâ notu kalmış ('Bu yapıda özellikle “SEZON 01 / tarih / oranlar …” düzeni var. Oyuncu sayfayı aşağı kaydırırken …') → silinmeli. Sezon 09 – 10 da forumda duruyor.",
    "Forum 'turnuva kayıtları her sezonun 3. günü' diyor; konuda gün numarası yerine 'ilk Pazartesi 12:00' (iki kaynakta da aynı) yazıldı.",
    "Academy kutuları (A1 – A10, `HTML/ACADEMY_KUTULARI.html`) bu konuda YOK — duyurulmuş bir bilgi değil.",
    "**5 resim (Z00–Z04)** — hazır linkli (itemiconrepo `forum/sezon/resim/`, jsDelivr). R01 logo + takvim GIF ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for z in V.SEZON:
    for d in (z["acilis"], z["turnuva"], z["birlesim"]): assert V.kisa(d) in BB, V.kisa(d)
assert "SEZON 09" not in BB and "%800" in BB and "BursaGB.com" in BB
assert len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in ["R01", "Z00", "Z01", "Z02", "Z03", "Z04", "GTAKVIM"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "oyun/rehber"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/sezon/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
assert len(res) == len(RES)
import _repo_resim; _repo_resim.uygula(res)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "FORUM/sezon/kaynak_tablo.md (patron) + kaynak_d57.txt (forum.sexyko.com/d/57) + _sezon_veri.py"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "SEZON_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "SEZON_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "SEZON_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("SEZON: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

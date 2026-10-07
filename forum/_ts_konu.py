# -*- coding: utf-8 -*-
# UCRETSIZ TEAMSPEAK FORUM KONUSU (patron 8 Eki: "yeni forum konulari ... resimli vs ayni janradan devam" · "hepsini tek tek konuya dok guzelce,
# resimleri repoya atmayi unutma, pushlamayi unutma"). Kaynak: forum.sexyko.com/d/55.
# Veri: _ts_veri.py · resimler: _ts_gorsel.py (Q00-Q04) + R01 logo · cevirici: _konu_blok.py
# CIKTI: teamspeak/ (konu.json, TS_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py "TeamSpeak" sekmesi.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _ts_veri as V

Y = KB.Y
OUT = V.TD; RD = os.path.join(OUT, "resim")
BASLIK = "🎙️ SEXYKO'DA ÜCRETSİZ TEAMSPEAK DÖNEMİ BAŞLADI! | Clanına Özel Ses Sunucusu · 3 Adımda Kurulum"

RES = {"R01": Y.RESIM["R01"]}
for rid, dosya, acik in [("Q00", "Q00_ozet.jpg", "Ücretsiz TeamSpeak — bir bakışta"), ("Q01", "Q01_adim1.jpg", "1. adım — panelden TeamSpeak"),
                         ("Q02", "Q02_adim2.jpg", "2. adım — sunucu bilgileri + KEY"), ("Q03", "Q03_adim3.jpg", "3. adım — KEY ile ilk giriş"),
                         ("Q04", "Q04_clan.jpg", "Clanını topla — PK · farm · event · CSW")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

ekle("banner", "R01")
ekle("baslik", "ÜCRETSİZ TEAMSPEAK SİSTEMİ AKTİF", "Clanına özel, düşük pingli ses sunucusu — 3 adımda kur")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "🎙️", "BİR BAKIŞTA")
ekle("img", "Q00", "")
ekle("p", V.GIRIS)
ekle("p", f"**{V.GIRIS2}**")
ekle("ayrac")

ekle("h", "🔹", V.ADIM[0][0])
ekle("img", "Q01", "")                                   # adim cumlesi kartin alt basliginda (patron 7 Eki: "resimde var, yazman lazim miydi") -> metinde tekrar yok
ekle("ayrac")

ekle("h", "🔹", V.ADIM[1][0])
ekle("img", "Q02", "")
ekle("p", V.ADIM[1][1])
ekle("liste", V.ADIM2_L)
ekle("p", V.ADIM2_S)
ekle("not", f"🔑 **{V.KEY[0]}** {V.KEY[1]}")
ekle("ayrac")

ekle("h", "🔹", V.ADIM[2][0])
ekle("img", "Q03", "")                                   # adim cumlesi kartin alt basliginda
ekle("p", f"✅ **{V.TAMAM[0]}** {V.TAMAM[1]}")
ekle("ayrac")

ekle("h", "⚔️", V.CLAN_BAS)
ekle("img", "Q04", "")
ekle("p", V.CLAN)
ekle("p", " ".join(V.YATIRIM))
ekle("p", f"🔥 **{V.SLOGAN[0]}** — {V.SLOGAN[1]} {V.SLOGAN[2]}")
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["🌐 Web: [[https://www.sexyko.com|www.sexyko.com]]",
               "💬 Discord: [[https://discord.gg/sexyko|discord.gg/sexyko]] · Forum: [[https://forum.sexyko.com|forum.sexyko.com]]"])
ekle("ayrac")
ekle("son", "🔥 PVP’NİN GEÇMİŞİ DEĞİL, BAŞLANGICI — SEXYKO 🔥")

KONTROL = [
    "**Kaynak:** forum.sexyko.com/d/55 (Flarum API, 8 Eki) — her cümle kaynakta birebir (`_ts_veri.py` assert).",
    "**Ekran görüntüleri:** gönderinin kendi 3 resmi (panel menüsü, oluşturma formu, TeamSpeak 3 istemcisi) Q01–Q03 kartlarının içinde.",
    "**Resimden alınan bilgi (metinde yok):** form alanları — Sunucu adı · Kapasite **64 slot** · Alt alan adı **clanadi.ts.sexyko.com** (küçük harf, rakam, tire) · \"Oluşturmak için giriş yap\"; istemci TeamSpeak 3. Ekip kapasiteyi değiştirirse Q02 güncellenir.",
    "TeamSpeak 3 indirme linki kaynakta yok → konuya eklenmedi.",
    "**5 resim (Q00–Q04)** — hazır linkli (itemiconrepo `forum/teamspeak/resim/`, içerik özetli). R01 logo ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for s in [V.GIRIS, V.ADIM2_S, V.CLAN, V.ADIM[1][1], *V.ADIM2_L, V.KEY[1], V.TAMAM[1]]: assert s in BB, s
assert len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in ["R01", "Q00", "Q01", "Q02", "Q03", "Q04"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum d/55 + SexyKO paneli"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/teamspeak/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "forum.sexyko.com/d/55 (metin + 3 ekran görüntüsü)"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "TS_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "TS_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "TS_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("TEAMSPEAK: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

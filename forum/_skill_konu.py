# -*- coding: utf-8 -*-
# SKILL & MASTER FORUM KONUSU (patron 6 Eki: "Basit Skill Master ve skiller icin detayli bir forum konusu acilacak ... forum konusu nasil yaptik o sekmenin icinde,
# ben sonra onu iceriye yazarim ... butun joblar icin").
# Veri: _skill_veri.py (canli rehbere assert'li) · resimler: _skill_gorsel.py (S01-S07) + yeni konunun R07 skill penceresi.
# Stil + ortak parcalar (satir(), renkler, logo, GIF'ler) uzun konudan: _yeni_konu.py. Celiskili bilgi KONUYA ALINMADI -> KONTROL listesi + skill_master/SKILL_MASTER.md.
# CIKTI: skill_master/ (konu.json, SKILL_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py sayfaya "Skill & Master" sekmesi olarak koyar.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, base64
from PIL import Image
import _yeni_konu as Y   # uzun konuyu da yeniden uretir (ayni cikti) — satir(), renkler, R01 logo, GIF linkleri oradan
import _skill_veri as V

OUT = V.SM; RD = os.path.join(OUT, "resim")
BASLIK = "⚔️ SEXYKO SKILL & MASTER REHBERİ | Tüm Joblar: Master, 70-80 Skill, Gereken İtemler | HYPER 16.10 🔥"
A, A2, G, YE, K, M = Y.ALTIN, Y.ALTIN2, Y.GRI, Y.YESIL, Y.KIRMIZI, Y.MAVI
PX = Y.PX
FORUM = "https://forum.sexyko.com/d/"

RES = {"R01": Y.RESIM["R01"], "GSAYIM": Y.RESIM["GSAYIM"], "GTAKVIM": Y.RESIM["GTAKVIM"],
       "R07": (Y.RESIM["R07"][0], "Skill penceresi (K) — oyun içi", "")}
for rid, dosya, acik in [("S00", "S00_yol_haritasi.jpg", "4 adımda Skill & Master — yol haritası"), ("S01", "S01_master_tablo.jpg", "Master görevi — 6 job: NPC, yer, 3 item"), ("S02", "S02_master_item.jpg", "Master itemleri — kim düşürür, yüzde kaç"),
                         ("S03", "S03_harita_karus.jpg", "Karus — Luferson Castle haritası: master NPC'leri + bosslar + Centaur"),
                         ("S04", "S04_harita_elmorad.jpg", "El Morad — El Morad Castle haritası: master NPC'leri + bosslar + Centaur"),
                         ("S05", "S05_skill_gorev.jpg", "70-80 skill görevleri — job × seviye, Spell Stone Powder adedi"),
                         ("S06", "S06_spell_stone.jpg", "Spell Stone Powder kaynakları"), ("S07", "S07_harita_ronark.jpg", "Ronark Land — Spell Stone mobları"), ("S08", "S08_npc.jpg", "Job job master + skill NPCleri"), ("S09", "S09_narki.jpg", "Narki ile Spell Stone Powder")]:
    RES[rid] = (dosya, acik, "")


def gorev(no): return f"{V.REH}/quests/{no}"
def ad(i): return V.ITEM[i]


# ---------- icerik (bloklar _yeni_konu.py ile ayni turler)
B = []
def ekle(*b): B.append(b)

ekle("afis", "GSAYIM")
ekle("banner", "R01")
ekle("baslik", "SKILL & MASTER REHBERİ", "Hangi job, hangi NPC, hangi item — Master'dan 80 skill'ine kadar adım adım, tüm joblar tek konuda.")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "🧭", "4 ADIMDA YOL HARİTASI")
ekle("img", "S00", "")
ekle("ayrac")

ekle("h", "1️⃣", "1. JOB DEĞİŞİMİ")
_coin = f"{V.ILK_JOB['coin']:,}".replace(",", ".")
ekle("p", f"Karakterin 1. job'unu henüz almadıysa: **Level {V.ILK_JOB['level']}+** → Moradon'daki **{V.ILK_JOB['npc']}** ({V.ILK_JOB['yer'].split()[-1]}) → "
          f"**{_coin} coin** → job change.")
ekle("rlink", "1st job change", f"/quests/{V.ILK_JOB['gorev']}")
ekle("ayrac")

ekle("h", "⌨️", "SKILL PENCERESİ (K)")
ekle("p", "**K** → Skill penceresi. Her job'un **4 sekmesi** var, sonuncusu **Master**. Sekme sayacının yanındaki **▲** ile puan verirsin.")
ekle("liste", ["**Warrior** — Attack · Defence · Passion · Master", "**Rogue** — Archery · Assassinate · Search · Master",
               "**Mage** — Fire · Ice · Lightning · Master", "**Priest** — Heal · Aura · Spirit · Master", "**Kurian** ve **Porutu** — Attack · Defence · Devil · Master"])
ekle("img", "R07", "Örnek Rogue: Assassinate 80 + Search 48 + Master 20 = 148 puan")
ekle("not", "Master sekmesine puan verebilmek için önce **Master görevini** bitir.")
ekle("ayrac")

ekle("h", "📍", "MASTER & SKILL NPC'LERİ — İSİM VE BÖLGE")
ekle("p", "Her job'un **kendi NPC'si** var. Ayrı bir skill NPC'si **yok**: **master görevini de 70 – 80 skill görevlerini de aynı NPC verir.** "
          "NPC'ler kendi ırkının ana haritasında:")
ekle("img", "S08", "")
for irk, harita, i in (("Karus", "Luferson Castle", 3), ("El Morad", "El Morad Castle", 4)):
    ekle("p", f"**{irk}** → **{harita}** haritası:")
    ekle("liste", [f"**{j[0]}** → **{j[2]}** · {j[i][0]},{j[i][1]}" for j in V.JOB if j[i]])
ekle("not", "Warrior, Priest ve Kurian / Porutu NPC'leri **yan yana** durur; Rogue ve Mage NPC'leri haritanın başka yerinde.")
ekle("ayrac")

ekle("h", "⚔️", "MASTER GÖREVİ (2. JOB) — TÜM JOBLAR")
ekle("p", f"**Level 60+** · herkes **1 {ad(V.HEART)}** + job'una özel **2 Essence** toplar, master NPC'sine götürür → **Master** olursun.")
ekle("img", "S01", "")
ekle("p", "**Nasıl yapılır — adım adım:**")
ekle("liste", ["**1 ·** Job'unun NPC'sine git (04. bölüm) → konuş → **master görevini** al — görev adı *2nd job change* (Kurian: *Second* · Porutu: *2nd job*)",
               f"**2 ·** **Centaur** kes → **{ad(V.HEART)}** düşer (%50) — haritada mor noktalar",
               "**3 ·** Job'unun **2 field boss**'unu kes → **2 Essence** düşer (%100) — hangi boss: 06. bölüm",
               "**4 ·** 3 itemle NPC'ye dön → görevi teslim et → **Master** oldun, **K** penceresinde **Master** sekmesi açılır"])
ekle("p", "📘 Rehberde aç: " + " · ".join(f"[[{gorev(j[7])}|{j[0]}]]" for j in V.JOB))
ekle("ayrac")

ekle("h", "💎", "MASTER İTEMLERİ NEREDEN DÜŞER")
ekle("img", "S02", "")
ekle("not", "İsimler oyundaki gibidir: item **Urkthron's** → boss **Urukthrone** · item **Colmicola's** → boss **Kamicollo** · item **Trethonz's** → boss **Trethorns**.")
ekle("p", "Field bosslar ve Centaur'lar **iki ırkın ana haritasında da** var — kendi tarafında kes:")
ekle("img", "S03", "")
ekle("img", "S04", "")
ekle("rlink", "Monster Listesi", "/monsters")
ekle("ayrac")

ekle("h", "📜", "70 – 80 SKILL GÖREVLERİ")
ekle("p", "Master olduktan sonra **aynı master NPC'si** gizli skilleri öğretir. Her görev **Spell Stone Powder** ister, ödülü **o seviyenin skill'i**.")
ekle("img", "S05", "")
ekle("p", "**Nasıl yapılır — adım adım:**")
ekle("liste", ["**1 ·** Önce **Master** ol (05. bölüm)",
               "**2 ·** Job'unun toplamı kadar **Spell Stone Powder** topla — nereden: 08. bölüm",
               "**3 ·** Aynı NPC'ye git → **70Lv skill** görevini al → tozu teslim et → o skill açılır",
               "**4 ·** Sonra job'undaki diğerleri: 72Lv · 74Lv · 75Lv … **80Lv skill** — Level 83'te hepsini aynı gün alabilirsin"])
ekle("ayrac")

ekle("h", "💠", "SPELL STONE POWDER NEREDEN?")
ekle("img", "S06", "")
ekle("img", "S07", "")
_n4, _n5 = (format(V.narki_ort(n), ".1f").replace(".", ",") for n in (4, 5))
ekle("p", "**♻️ Narki ile Spell Stone Powder** — kullanmadığın takıları Spell Stone'a çevir:")
ekle("img", "S09", "")
ekle("liste", [f"**Nerede:** Moradon · **{V.NARKI_NPC['ad']}** (4 tane, hepsi aynı) — " + " · ".join(f"{x},{z}" for x, z in V.NARKI_NPC["nokta"]),
               "**Nasıl:** Narki ile konuş → takını ver (**tek adet**) → takı **yok olur** → karşılığında **1 ödül** çekilir",
               f"**Eski aksesuarlar** havuzu (Old … takılar, 64 çeşit) → 1 – 5 adet Spell Stone, ortalama **≈ {_n4}**",
               f"**Aksesuarlar** havuzu (normal takılar, 926 çeşit) → 1 – 5 adet Spell Stone, ortalama **≈ {_n5}** · %23,17 ihtimalle Forgotten Accessory Box",
               "**Olmaz:** bağlı, kiralık, mühürlü ya da süreli eşya verilemez · kırdırma geri alınamaz · envanterinde boş yer olmalı"])
ekle("rlink", "Narki Kırdırma (takın hangi havuza giriyor, ara)", "/narki")
ekle("ayrac")

ekle("h", "💡", "İPUÇLARI")
ekle("liste", [f"**Skill Preset:** puan dağılımını kaydet, PK / farm / event arasında tek tıkla geç · **Save Quickslot:** 4 ayrı skill bar — 💬 [[{FORUM}42|forum.sexyko.com/d/42]]",
               f"**Job Changer:** iteme sağ tık → job seç, NPC gerekmez · önce üstündeki **tüm itemleri çıkar** — 💬 [[{FORUM}28|forum.sexyko.com/d/28]]",
               "Dikkat: Job Changer ile job değiştirince **skillerin kaybolur, her şey sıfırlanır** — ama **master ve 70 – 80 skill görevlerin sıfırlanmaz**",
               "Bir itemin nereden düştüğünü bilmiyorsan: item üstünde **Ctrl + D**"])
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["📘 Görevler: [[https://sexyko.com/guide/quests|sexyko.com/guide/quests]]", "👹 Monster Listesi: [[https://sexyko.com/guide/monsters|sexyko.com/guide/monsters]]",
               "♻️ Narki: [[https://sexyko.com/guide/narki|sexyko.com/guide/narki]]", "💬 Forum: [[https://forum.sexyko.com|forum.sexyko.com]]",
               "🌐 Web: [[https://sexyko.com|sexyko.com]]"])
ekle("ayrac")
ekle("afis", "GTAKVIM")
ekle("son", "🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥")

KONTROL = [
    "**Patron kararları (6 Eki):** 70+ skill görevi **gerekli** · Heart **var** (Centaur %50) · Colmicola / Trethonz **var** · Job değişince **skiller kaybolur, her şey sıfırlanır** · field bosslar **%100** düşürür.",
    "**Colmicola's Essence (Kamicollo) · Trethonz's Essence (Trethorns) — kaynak: patron + korehberi.** Admin'de bu iki item 2.216 drop tablosunun hiçbirinde yok (Kamicollo #8655/#8661, Trethorns #8658 tabloları boş); rehber sitesinin item sayfası 'bilinen edinme yolu bulunamadı' diyor. Oyuncu rehberde Ctrl + D ile bakarsa göremez → ekip isterse admin drop tablosuna eklesin.",
    "Admin canlı (6 Eki): Centaur #2602 → Heart %50 · Garukonga #8653/#8659 → %100 · Urukthrone #8656/#8662 → %100 · Alkedrada #8657/#8663 → %100 (sitedeki oranlarla aynı). isSkillQuestRequired = 0 — patron: görev gerekli, konu öyle.",
    "Veriler **HYPER** (sexyko.com/guide, 6 Eki canlı): Level 83 + 148 skill puanı, tüm görev / oran / spawn noktaları. Lyot'un Spell Stone oranı 3 Eki'de %1,9 idi, 6 Eki'de %3 → yayından önce rehberde bir daha bak.",
    "Job Changer (patron 6 Eki): skiller kaybolur, her şey sıfırlanır · master ve 70-80 skill görevleri **sıfırlanmaz** (admin pasif duyuru 264 ile aynı).",
    "Skill adları (70 / 72 / 75 / 80'de hangi skill) konuda YOK: rehber sitesi vermiyor (ödül 'Skill ×1'), güvenilir SexyKO kaynağı bulunmadı.",
    "Konuya ALINMADI: 61 Lv scroll görevleri (Scream / Magic Shield / Judgment — Certificate of Victory'nin SexyKO'da kaynağı yok) · 70-80 skill adları (rehber vermiyor) · [Job Change] Biranda NPC'si (admin'de pasif).",
    "Kurian / Porutu: rehber Atlas / Morbor görevlerini 'Warrior' etiketiyle gösteriyor; Warrior'un kendi NPC'si Skaki → bunlar Kurian / Porutu görevi (korehberi + admin katsayı tablosu ile doğrulandı).",
    f"**{sum(1 for r in RES if r.startswith('S'))} resim (S00–S09)** — **hazır linkli** (itemiconrepo `forum/skill_master/resim/`, jsDelivr). R07 (skill penceresi) uzun konuyla aynı dosya. R01 logo + 2 GIF hazır link.",
    "Tüm araştırma, kaynaklar, çelişkiler: `FORUM/skill_master/SKILL_MASTER.md`.",
]

# ---------- cizim (_yeni_konu.py ile ayni gorunum)
BASLIKLAR = [(b[1], b[2]) for b in B if b[0] == "h"]
NO = {x: f"{i:02d}" for i, x in enumerate(BASLIKLAR, 1)}
sat = Y.satir


def bb():
    o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"[CENTER][IMG]{{{{{b[1]}}}}}[/IMG][/CENTER]")
        elif k == "baslik": o.append(f"[CENTER][SIZE=7][B][COLOR={A}]{b[1]}[/COLOR][/B][/SIZE]\n[SIZE=4][COLOR={G}]{b[2]}[/COLOR][/SIZE][/CENTER]")
        elif k == "icindekiler": o.append(f"[CENTER][SIZE=5][B][COLOR={A}]📑 İÇİNDEKİLER[/COLOR][/B][/SIZE]\n[SIZE=4]" + "\n".join(f"[COLOR={A}]{NO[x]}[/COLOR] · {x[0]} {x[1]}" for x in BASLIKLAR) + "[/SIZE][/CENTER]")
        elif k == "ayrac": o.append(f"[CENTER][COLOR={A}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/COLOR][/CENTER]")
        elif k == "h": o.append(f"[CENTER][SIZE=6][B][COLOR={A}]{b[1]} {NO[(b[1], b[2])]} · {b[2]}[/COLOR][/B][/SIZE][/CENTER]")
        elif k == "p": o.append(f"[SIZE=4]{sat(b[1], 'bb')}[/SIZE]")
        elif k == "liste": o.append("[SIZE=4]" + "\n".join(f"[COLOR={A}]◆[/COLOR] {sat(x, 'bb')}" for x in b[1]) + "[/SIZE]")
        elif k == "img": o.append(f"[CENTER][IMG]{{{{{b[1]}}}}}[/IMG]" + (f"\n[SIZE=3][COLOR={G}]▲ {b[2]}[/COLOR][/SIZE]" if b[2] else "") + "[/CENTER]")
        elif k == "not": o.append(f"[SIZE=4][COLOR={YE}]💡 {sat(b[1], 'bb')}[/COLOR][/SIZE]")
        elif k == "rlink": o.append(f"[SIZE=4][URL={V.REH}{b[2]}][B][COLOR={M}]📘 Rehberde aç: {b[1]} ↗[/COLOR][/B][/URL][/SIZE]")
        elif k == "son": o.append(f"[CENTER][SIZE=6][B][COLOR={K}]{b[1]}[/COLOR][/B][/SIZE][/CENTER]")
    return "\n\n".join(o)


def onizleme():
    c = lambda x: f'<div style="text-align:center">{x}</div>'
    sl = lambda x: f'<div style="text-align:left">{x}</div>'   # metin bloklari sola: satirlar ayni kenardan baslar (patron 6 Eki: "satirlarin daginik olmasini istemiyorum")
    o = []
    for b in B:
        k = b[0]
        if k == "banner": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="" style="max-width:100%;width:520px">'))
        elif k == "afis": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="" style="max-width:100%">'))
        elif k == "baslik": o.append(c(f'<span style="font-size:{PX[7]}px;color:{A}"><b>{html.escape(b[1])}</b></span><br><span style="font-size:{PX[4]}px;color:{G}">{html.escape(b[2])}</span>'))
        elif k == "icindekiler": o.append(c(f'<span style="font-size:{PX[5]}px;color:{A}"><b>📑 İÇİNDEKİLER</b></span><br><span style="font-size:{PX[4]}px">'
                                           + "<br>".join(f'<span style="color:{A}">{NO[x]}</span> · {html.escape(x[0])} {html.escape(x[1])}' for x in BASLIKLAR) + "</span>"))
        elif k == "ayrac": o.append(c(f'<span style="color:{A}">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>'))
        elif k == "h": o.append(c(f'<span style="font-size:{PX[6]}px;color:{A}"><b>{b[1]} {NO[(b[1], b[2])]} · {html.escape(b[2])}</b></span>'))
        elif k == "p": o.append(sl(f'<span style="font-size:{PX[4]}px">{sat(b[1], "html")}</span>'))
        elif k == "liste": o.append(sl(f'<span style="font-size:{PX[4]}px">' + "<br>".join(f'<span style="color:{A}">◆</span> {sat(x, "html")}' for x in b[1]) + "</span>"))
        elif k == "img": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="{html.escape(b[2])}" style="max-width:100%">'
                                    + (f'<br><span style="font-size:{PX[3]}px;color:{G}">▲ {html.escape(b[2])}</span>' if b[2] else "")))
        elif k == "not": o.append(sl(f'<span style="font-size:{PX[4]}px;color:{YE}">💡 {sat(b[1], "html")}</span>'))
        elif k == "rlink": o.append(sl(f'<a href="{V.REH}{b[2]}" target="_blank" rel="noopener" style="font-size:{PX[4]}px;color:{M};font-weight:700;text-decoration:none">📘 Rehberde aç: {html.escape(b[1])} ↗</a>'))
        elif k == "son": o.append(c(f'<span style="font-size:{PX[6]}px;color:{K}"><b>{html.escape(b[1])}</b></span>'))
    return "<br>".join(o)


def md():
    o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"![]({{{{{b[1]}}}}})")
        elif k == "baslik": o.append(f"# {b[1]}\n\n*{b[2]}*")
        elif k == "icindekiler": o.append("## 📑 İçindekiler\n\n" + "\n".join(f"{NO[x]} · {x[0]} {x[1]}  " for x in BASLIKLAR))
        elif k == "ayrac": o.append("---")
        elif k == "h": o.append(f"## {b[1]} {NO[(b[1], b[2])]} · {b[2]}")
        elif k in ("p", "not"): o.append(("💡 " if k == "not" else "") + sat(b[1], "md"))
        elif k == "liste": o.append("\n".join(f"- {sat(x, 'md')}" for x in b[1]))
        elif k == "img": o.append(f"![{b[2]}]({{{{{b[1]}}}}})" + (f"\n▲ *{b[2]}*" if b[2] else ""))
        elif k == "rlink": o.append(f"**[📘 Rehberde aç: {b[1]} ↗]({V.REH}{b[2]})**")
        elif k == "son": o.append(f"**{b[1]}**")
    return "\n\n".join(o)


def duz():
    o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"[RESİM {b[1]}]")
        elif k == "img": o.append(f"[RESİM {b[1]}: {b[2] or RES[b[1]][1]}]")
        elif k == "baslik": o.append(f"{b[1]}\n{b[2]}")
        elif k == "icindekiler": o.append("İÇİNDEKİLER\n" + "\n".join(f"{NO[x]} · {x[0]} {x[1]}" for x in BASLIKLAR))
        elif k == "ayrac": o.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        elif k == "h": o.append(f"{b[1]} {NO[(b[1], b[2])]} · {b[2]}")
        elif k == "son": o.append(b[1])
        elif k in ("p", "not"): o.append(("💡 " if k == "not" else "") + sat(b[1], "duz"))
        elif k == "liste": o.append("\n".join(f"◆ {sat(x, 'duz')}" for x in b[1]))
        elif k == "rlink": o.append(f"📘 Rehberde aç: {b[1]} → {V.REH}{b[2]}")
    return "\n\n".join(o)


BB, HT, MD, DZ = bb(), onizleme(), md(), duz()
jeton = set(re.findall(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", BB))
assert jeton == set(RES), (jeton ^ set(RES))
for a, z in [("[B]", "[/B]"), ("[CENTER]", "[/CENTER]"), ("[SIZE=", "[/SIZE]"), ("[COLOR=", "[/COLOR]"), ("[URL=", "[/URL]")]:
    assert BB.count(a) == BB.count(z), a
for j in V.JOB:                                    # her job metinde: ad + NPC + koordinat (item / toplam tablolari S01 / S05 gorselinde — tekrar kaldirildi)
    assert j[0] in BB and j[2] in BB, j[0]
    assert all(f"{xz[0]},{xz[1]}" in BB for xz in (j[3], j[4]) if xz), j[0]
for gerekli in ("S00", "S01", "S02", "S05", "S08", "S09"):     # tabloyu tasiyan gorseller konuda
    assert "{{" + gerekli + "}}" in BB, gerekli
res = []
for rid in ["R01", "S00", "S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "R07", "GSAYIM", "GTAKVIM"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "oyun/rehber"}
    if dosya:
        klasor, rel = (Y.RD, "FORUM/yeni_konu/resim/") if rid == "R07" else (RD, "FORUM/skill_master/resim/")
        p = os.path.join(klasor, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya=rel + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
assert len(res) == len(RES)
import _repo_resim; _repo_resim.uygula(res)                       # 7 Eki: itemiconrepo linkli
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in BASLIKLAR], "kaynak": "FORUM/skill_master/SKILL_MASTER.md + _skill_veri.py (sexyko.com/guide canlı, 6 Eki)"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "SKILL_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "SKILL_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "SKILL_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("SKILL: bölüm", len(BASLIKLAR), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

# -*- coding: utf-8 -*-
# SKILL & MASTER VERISI — tek kaynak (patron 6 Eki: "Basit Skill Master ve skiller icin detayli bir forum konusu ... once ogren sonra mdle sonra resimle, butun joblar icin").
# _skill_gorsel.py (resimler) + _skill_konu.py (forum metni) buradan okur. Aciklama + kaynak + celiskiler: skill_master/SKILL_MASTER.md
# KANIT: her gorev / drop / oran asagida canli site cekimine karsi assert edilir — skill_master/veri/site_gorev.json + site_canavar.json (sexyko.com/guide, 6 Eki)
# NPC koordinatlari: ADMIN_PANEL/VERI list:npc-spawns (25 Eyl, hepsi aktif:1) · harita eslemesi: site noktasi left% = x/2048, top% = 1 - z/2048 (Garukonga 5 noktada birebir)
import os, re, json

KOK = os.path.dirname(os.path.abspath(__file__))
SM = os.path.join(KOK, "skill_master")
WEB = os.path.join(KOK, "rehber", "web")
GOREV = json.load(open(os.path.join(SM, "veri", "site_gorev.json"), encoding="utf-8"))["kayit"]
CANAVAR = json.load(open(os.path.join(SM, "veri", "site_canavar.json"), encoding="utf-8"))["kayit"]
REH = "https://sexyko.com/guide"

HEART, URK, COL, GARU, TRET, ALK, SSP = "810095000", "810090000", "810091000", "810092000", "810093000", "810094000", "810369000"
ITEM = {HEART: "Unstable Kentaraus' Heart", URK: "Urkthron's Essence", COL: "Colmicola's Essence", GARU: "GaruKonga's Essence",
        TRET: "Trethonz's Essence", ALK: "Alkeradeua's Essence", SSP: "Spell Stone Powder"}


def ikon(item_id):
    """Item ikonu: rehber gorev sayfasinda data-id'nin yanindaki itemicon (site ikon onbellegi rehber/web/resim/)."""
    for f in os.listdir(os.path.join(WEB, "sayfa", "quests_detay")):
        s = open(os.path.join(WEB, "sayfa", "quests_detay", f), encoding="utf-8").read()
        m = re.search(r'data-id="' + item_id + r'"[^>]*itemicon/(itemicon_[\d_]+\.png)', s)
        if m:
            p = os.path.join(WEB, "resim", "cdn.sexyko.com_itemicon_" + m.group(1))
            assert os.path.exists(p), p
            return p
    raise KeyError(item_id)


# job: (ad, irk, NPC, Karus x/z, El Morad x/z, 2. item, 3. item, master gorevi, {skill level: gorev no})
JOB = [
    ("Warrior", "Karus · El Morad", "[Warrior Master] Skaki", (387, 1741), (1661, 322), URK, ALK, 408, {70: 336, 75: 510, 80: 511}),
    ("Rogue", "Karus · El Morad", "[Secret Agent] Clarence", (430, 709), (1632, 1331), GARU, TRET, 409, {70: 337, 72: 512, 75: 513, 80: 514}),
    ("Mage", "Karus · El Morad", "[Archmage] Drake", (1696, 806), (372, 1226), COL, GARU, 410, {70: 338, 72: 515, 75: 516, 80: 517}),
    ("Priest", "Karus · El Morad", "[Priest] Minerva", (381, 1744), (1657, 326), COL, TRET, 411, {70: 339, 72: 518, 74: 519, 75: 520, 76: 521, 78: 522, 80: 523}),
    ("Kurian", "Karus", "[Grand Elder] Morbor", (405, 1728), None, URK, ALK, 784, {75: 785, 80: 786}),
    ("Porutu", "El Morad", "[Grand Elder] Atlas", None, (1650, 331), URK, ALK, 781, {75: 782, 80: 783}),
]
SEVIYE = [70, 72, 74, 75, 76, 78, 80]
ILK_JOB = {"gorev": 406, "npc": "[Grand Merchant] Kaishan", "yer": "Moradon 816,703", "coin": 3000, "level": 10}

# master itemi -> (dusuren, [Karus id, El Morad id], oran)
# Heart/Urkthron/Alkeradeua/GaruKonga: site + admin canli drop tablosu (6 Eki) ayni oran.
# Colmicola/Trethonz: KAYNAK PATRON (6 Eki: "3 var ... 5 yuzde yuz duser") + korehberi — admin 2.216 drop tablosunda YOK, site item sayfasi "bilinen edinme yolu bulunamadi"
DROP = {HEART: ("Centaur", ["2602"], "50%"), URK: ("[Field Boss] Urukthrone", ["8656", "8662"], "100%"),
        ALK: ("[Field Boss] Alkedrada", ["8657", "8663"], "100%"), GARU: ("[Field Boss] Garukonga", ["8653", "8659"], "100%"),
        COL: ("[Field Boss] Kamicollo", ["8655", "8661"], "100%"), TRET: ("[Field Boss] Trethorns", ["8658", "8664"], "100%")}
DROP_PATRON = {COL, TRET}
# harita noktalari: site spawn (Centaur spawn'i sitede "Centaur Foal" 2657/2607 adiyla, drop 2602'de — ADM #2602 ayni noktalarda, C-S4)
HARITA = {"karus": {"minimap": "1", "ad": "Luferson Castle", "irk": "Karus", "centaur": "2657",
                    "boss": [("8656", URK), ("8657", ALK), ("8653", GARU), ("8655", COL), ("8658", TRET)]},
          "elmorad": {"minimap": "2", "ad": "El Morad Castle", "irk": "El Morad", "centaur": "2607",
                      "boss": [("8662", URK), ("8663", ALK), ("8659", GARU), ("8661", COL), ("8664", TRET)]}}
# Spell Stone Powder kaynaklari (Ronark Land, canli site oranlari)
SSP_MOB = ["8401", "8402", "8403", "8404", "1402", "1311"]
NARKI = [("Eski aksesuarlar", "1–5 adet"), ("Aksesuarlar", "1–5 adet")]
# Narki (canli site + admin NPC/spawn, 6 Eki) — skill_master/veri/site_narki.json
NARKI_VERI = json.load(open(os.path.join(SM, "veri", "site_narki.json"), encoding="utf-8"))
NARKI_NPC = NARKI_VERI["npc"]          # Moradon, 4 nokta · Moradon haritasi 1024 birim (minimap 3: left% = x/1024)


def narki_havuz(no):
    """havuz -> ([(adet, %)], (kutu adi, %)) — sitedeki metinden ayristirilir."""
    t = NARKI_VERI["havuz"][str(no)]["odul"]
    ssp = sorted((int(a), float(p.replace(",", "."))) for a, p in re.findall(r"Spell Stone Powder (\d) adet %([\d,]+)", t))
    kutu = re.search(r"Forgotten Accessory Box 1 adet %([\d,]+)", t)
    return ssp, ("Forgotten Accessory Box", float(kutu.group(1).replace(",", ".")))


def narki_ort(no):
    return sum(a * p for a, p in narki_havuz(no)[0]) / 100


def nokta(cid):
    return CANAVAR[cid]["nokta"]          # [(left%, top%)]


def ssp_oran(cid):
    return float(re.search(r"Spell Stone Powder ([\d.]+)%", CANAVAR[cid]["metin"]).group(1))


def ssp_adet(gno):
    return int(re.search(r"Spell Stone Powder topla (\d+)×", GOREV[str(gno)]["metin"]).group(1))


def toplam(j):
    return sum(ssp_adet(g) for g in j[8].values())


def lv(cid):
    return CANAVAR[cid]["level"]


# ---------- kanit (canli siteye karsi)
for ad, irk, npc, kx, ex, i2, i3, mg, sk in JOB:
    g = GOREV[str(mg)]
    assert npc in g["metin"], (ad, npc)
    assert {HEART, i2, i3} <= set(g["item_id"]), (ad, g["item_id"])
    assert "Job change" in g["metin"], ad
    for lvl, no in sk.items():
        s = GOREV[str(no)]
        assert s["metin"].startswith(f"Level {lvl}–100"), (ad, lvl, s["metin"][:20])
        assert npc in s["metin"] and SSP in s["item_id"] and "Ödüller Skill 1×" in s["metin"], (ad, lvl)
assert GOREV["406"]["metin"].count(ILK_JOB["npc"]) >= 2 and "Coin topla 3000×" in GOREV["406"]["metin"] and "Level 10–100" in GOREV["406"]["metin"]
assert [toplam(j) for j in JOB] == [30, 37, 37, 69, 25, 25]
for it, d in DROP.items():
    for cid in d[1]:
        if it in DROP_PATRON:                            # site bu bosslarda drop gostermiyor (C-S1) — bilgi patrondan
            assert "drop kaydı yok" in CANAVAR[cid]["metin"] and d[0] == CANAVAR[cid]["ad"], cid
        else:
            assert f"{ITEM[it]} {d[2]}" in CANAVAR[cid]["metin"].replace("&#039;", "'"), (it, cid)
for h in HARITA.values():
    for cid, _ in h["boss"]:
        assert CANAVAR[cid]["minimap"] == [h["minimap"]] and h["irk"] in CANAVAR[cid]["metin"], cid
    assert CANAVAR[h["centaur"]]["minimap"] == [h["minimap"]] and len(nokta(h["centaur"])) == 7
assert [ssp_oran(c) for c in SSP_MOB] == [10.0, 10.0, 10.0, 10.0, 3.0, 3.0]
_nk = open(os.path.join(KOK, "rehber", "veri", "narki.md"), encoding="utf-8").read()
for havuz, _ in NARKI:
    blok = _nk[_nk.find(havuz + " /"):][:200000].split("\n## ")[0]
    assert "Spell Stone Powder / 1 adet" in blok and "Spell Stone Powder / 5 adet" in blok, havuz

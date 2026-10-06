# -*- coding: utf-8 -*-
# KISA FORUM KONUSU — "SexyKO Oyun Rehberi (kisa)" (patron 4 Eki: "bunun bir yan sekmeye kisasini yap, konular degismeden,
# en ufak resimlilerini, yonlendirmeli cogu olacak sekilde").
# Bolumler _yeni_konu.py'nin 24 bolumunun AYNISI (assert). Her bolum: kucuk resim (360x240 kutuya sigdirilmis) + 1 satir + rehber/forum linki.
# Bilgi uzun konudan alindi, yeni bilgi yok. Forum linki forum.sexyko.com/d/<id> (d/53 200 olculdu 4 Eki), rehber linkleri _yeni_konu REHBER_LINK ile ayni.
# CIKTI: yeni_konu/kisa/ (konu.json, KISA_KONU_bbcode.txt / _markdown.md / _duz.txt, resim/K*.jpg) -> _konu_kit.py sayfaya "Kisa konu" sekmesi olarak koyar.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, base64
from PIL import Image
import _yeni_konu as Y   # uzun konuyu da yeniden uretir (ayni cikti) — basliklar, resimler, renkler oradan

OUT = os.path.join(Y.KOK, "yeni_konu", "kisa"); RD = os.path.join(OUT, "resim")
os.makedirs(RD, exist_ok=True)
KUTU = (360, 240)
BASLIK = "📘 SEXYKO OYUN REHBERİ (KISA) | 24 Sistem Tek Bakışta, Detayı Rehberde | HYPER 16.10 BETA 🔥"
FORUM = "https://forum.sexyko.com/d/"
REH = "https://sexyko.com"

def r(ad, yol): return ("📘", ad, REH + yol)
def f(ad, no): return ("💬", ad, FORUM + str(no))

# bolum basligi -> (resim, kisa metin, linkler). Resme tiklayinca ilk linke gider.
K = {
    "OYUNUN İÇİNDEKİ REHBER": ("R02", "Sol üstteki **📖 kitap** → oyunun içinde rehber: **305 monster**, **998 görev**, upgrade oranları, drop arama.",
                               [r("Rehberin tamamı", "/guide/book"), f("Rehber Sistemi", 22)]),
    "KISAYOLLAR VE ARAYÜZ": ("R19", "**F10** ayarlar · **K** skill · **U** karakter · **H** komutlar · **I** envanter · **Ctrl + D** drop kaynağı.",
                             [r("Rehber", "/guide/book")]),
    "BAŞLANGIÇ PAKETİ": ("F53_4", "**Level 83** · **1.000.000.000 coin** · 3 günlük EXP Premium, Valkyrie Set, Pathos, Kanat, Magic Bag, War Tattoo · **24 saat Genie**.",
                         [r("Başlangıç Eşyaları", "/guide/beginner-items"), f("Başlangıç Paketi", 53)]),
    "GELİŞMİŞ GENIE": ("R03", "**8 Attack + 8 Buff + 8 Party** skill slotu · yüzdeyle HP/MP · sadece listedeki moblara vurur.", [f("Genie Sistemi", 16)]),
    "F10 AYARLAR — 11 SEKME": ("R05", "Grafik, efekt, **loot filtresi**, font ve **2. şifre** — 11 sekme.", [f("F10 Oyun Ayarları", 12)]),
    "SKILL PRESET & QUICK SLOT": ("R07", "**K** → **4 ayrı Quick Slot** — PK, farm, party, event düzenleri arasında hızlı geç.", [f("Skill Preset & Quick Slot", 42)]),
    "PARTY AYARLARI": ("F11_2", "Party üyelerinin **HP · MP · Buff · Damage** bilgisini ayrı ayrı aç / kapat.", [f("Party Sistemi", 11)]),
    "SAĞ TIK DEVRİ — NPC'YE GİTMEYE SON": ("F10_5", "KC, Gem, Fragment, Chest: **sağ tıkla kırdır** · Tag Name, Make Over, Nick, Job Changer da sağ tıkla.",
                                           [f("Kırdırma", 10), f("Chaotic Generator", 43), f("Tag Name", 30), f("Make Over", 31), f("Nick", 32), f("Job Changer", 28)]),
    "SOLO PELERİN": ("F44_2", "Clana girmeden pelerin: **15 gün · 250 HP · 250 MP · 25 DEF · %3 AP** · takım pelerinleri.",
                     [f("Solo Pelerin", 44), f("Solo Cape", 29)]),
    "GEM & FRAGMENT · NARKİ · PUS KIRDIRMA": ("R21", "Neyi kırdırırsan **ne çıkar, yüzde kaç** — hepsi rehberde.",
                                              [r("Gem & Fragment", "/guide/fragment"), r("Narki", "/guide/narki"), r("PUS Kırdırma", "/guide/pus-crash")]),
    "DROP INFO · DROP SEARCH": ("F34_2", "Moba tıkla → **drop yüzdeleri** · item üstünde **Ctrl + D** → hangi mobdan düşer.",
                                [f("Drop Info", 34), f("Drop Search", 50), r("Monster Listesi", "/guide/monsters")]),
    "SLOT TELEPORT": ("F52_2", "**[Teleport] Portal** → mobu seç → **250.000 coin** ile slotuna ışınlan.", [f("Slot Teleport", 52)]),
    "GRIND TRACKER": ("R08", "Sol üst **⏱** → farm süresi, **saatlik coin** ve **saatlik item** — slot verimini karşılaştır.", [f("Farm Grind Tracker", 14)]),
    "AUTO MINING — MINING INN": ("F24_2", "Auto Mining ürünleri **Mining Inn**'de birikir · depo tek yönlü: sadece çekilir.", [f("Auto Mining — Mining Inn", 24)]),
    "POWER UP STORE + KUPON": ("R09", "**Basket** ile toplu alışveriş · sponsor yayıncı kodu ile **%30'a varan** indirim.",
                               [f("Power Up Store", 27), f("PUS İndirim Kodu", 51)]),
    "ÇARKIFELEK": ("R10", "**350 KC** ile çevir ya da **2 saat online** kal, **1 ücretsiz** hak.", [f("Çarkıfelek", 41)]),
    "GÜNLÜK GÖREVLER": ("R20", "Sol alt **Daily Quest** → görev seç → **Accept** → süre dolmadan bitir, ödül otomatik.",
                        [r("Günlük Görevler", "/guide/daily-quests"), f("Daily Quest", 33)]),
    "ETKİNLİK TAKVİMİ": ("R11", "Sağ üst **kum saati** → takvim · **Bildirim kur** → etkinlikten 5 dakika önce uyarı.", [f("Kum Saati", 38)]),
    "ETKİNLİK KURALLARI": ("R12", "Knight Chaos, Border Defense War, Juraid, Forgotten Temple, Castle Siege, Knight Royale, Under the Castle — kurallar ve ödüller.",
                           [r("Knight Chaos", "/guide/book/chaos"), r("Etkinlik Ödülleri", "/guide/event-rewards")]),
    "DRAKI'S TOWER": ("R24", "**5 bölüm** · günde **3 giriş** · sıfırlama **18:00** · aylık sıralama.", [r("Draki's Tower", "/guide/book/draki"), f("Draki's Tower", 45)]),
    "UPGRADE ORANLARI": ("R13", "Oranlar rehberde ve **Anvil'de canlı** · en yüksek **+8** · **Trina's Piece** oranı artırır.",
                         [r("Upgrade Oranları", "/guide/upgrade"), f("Upgrade Oranları", 26)]),
    "REBIRTH": ("F49_1", "**83 Lv + %100 EXP + 100.000.000 coin + 10.000 NP** → Rebirth · her seviye **+2 stat**.", [f("Karakter Rebirth", 49)]),
    "EQUIPMENT VIEW": ("F46_2", "Karaktere **sağ tık → Equipment View**: ekipman, upgrade, stat, resistance, buff listesi.", [f("Equipment View", 46)]),
    "BAĞLANTILAR": (None, "", [("🌐", "sexyko.com", REH), ("📘", "Rehber", REH + "/guide/book"), ("💬", "Forum", "https://forum.sexyko.com"),
                               ("📥", "Client", REH + "/download")]),
}
assert [t for _, t in Y.BASLIKLAR] == list(K), "bolumler uzun konuyla ayni olmali"
for t, (rid, _, ln) in K.items():
    assert rid is None or rid in Y.RESIM, rid
    assert ln, t
assert "/d/25" not in json.dumps(K)   # d/25 etkinlik saatleri oyun ici takvimle celisiyor (uzun konu KONTROL) — link verilmez

# ---------- kucuk resimler
RES = {"R01": Y.RESIM["R01"], "GSAYIM": Y.RESIM["GSAYIM"], "GTAKVIM": Y.RESIM["GTAKVIM"]}   # GIF'ler: patron 4 Eki "kisa versiyona da koyman lazim"
for t, (rid, _, _) in K.items():
    if not rid:
        continue
    with Image.open(os.path.join(Y.RD, Y.RESIM[rid][0])) as im:
        im = im.convert("RGB"); im.thumbnail(KUTU, Image.LANCZOS)
        im.save(os.path.join(RD, f"K{rid}.jpg"), quality=88, optimize=True)
    RES["K" + rid] = (f"K{rid}.jpg", Y.RESIM[rid][1] + " (küçük)", "")

# ---------- cizim
A, A2, G, M = Y.ALTIN, Y.ALTIN2, Y.GRI, Y.MAVI
AYRAC = "━━━━━━━━━━━━━━━━━━━━━━━━"

def bolumler():
    for e, t in Y.BASLIKLAR:
        rid, metin, ln = K[t]
        yield e, Y.NO[(e, t)], t, rid, metin, ln

def bb():
    o = ["[CENTER][IMG]{{GSAYIM}}[/IMG][/CENTER]", f"[CENTER][IMG]{{{{R01}}}}[/IMG]\n[SIZE=7][B][COLOR={A}]SEXYKO OYUN REHBERİ[/COLOR][/B][/SIZE]\n"
         f"[SIZE=4][COLOR={G}]24 başlık, kısa kısa — detay için başlığın altındaki linke tıkla.[/COLOR][/SIZE][/CENTER]", f"[CENTER][COLOR={A}]{AYRAC}[/COLOR][/CENTER]"]
    for e, no, t, rid, metin, ln in bolumler():
        s = f"[CENTER][SIZE=5][B][COLOR={A}]{e} {no} · {t}[/COLOR][/B][/SIZE]"
        if rid: s += f"\n[URL={ln[0][2]}][IMG]{{{{K{rid}}}}}[/IMG][/URL]"
        if metin: s += f"\n[SIZE=4]{Y.satir(metin, 'bb')}[/SIZE]"
        s += "\n[SIZE=4]" + " · ".join(f"[URL={u}][B][COLOR={M}]{i} {a} ↗[/COLOR][/B][/URL]" for i, a, u in ln) + "[/SIZE][/CENTER]"
        o += [s, f"[CENTER][COLOR={A}]{AYRAC}[/COLOR][/CENTER]"]
    o.append("[CENTER][IMG]{{GTAKVIM}}[/IMG][/CENTER]")
    o.append(f"[CENTER][SIZE=6][B][COLOR={Y.KIRMIZI}]🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥[/COLOR][/B][/SIZE][/CENTER]")
    return "\n\n".join(o)

def onizleme():
    PX = Y.PX
    c = lambda x: f'<div style="text-align:center">{x}</div>'
    lk = lambda i, a, u: f'<a href="{u}" target="_blank" rel="noopener" style="color:{M};font-weight:700;text-decoration:none">{i} {html.escape(a)} ↗</a>'
    ay = c(f'<span style="color:{A}">{AYRAC}</span>')
    o = [c('<img src="{{GSAYIM}}" alt="" style="max-width:100%">'), c(f'<img src="{{{{R01}}}}" alt="" style="max-width:100%;width:420px"><br><span style="font-size:{PX[7]}px;color:{A}"><b>SEXYKO OYUN REHBERİ</b></span><br>'
           f'<span style="font-size:{PX[4]}px;color:{G}">24 başlık, kısa kısa — detay için başlığın altındaki linke tıkla.</span>'), ay]
    for e, no, t, rid, metin, ln in bolumler():
        s = f'<span style="font-size:{PX[5]}px;color:{A}"><b>{e} {no} · {html.escape(t)}</b></span>'
        if rid: s += f'<br><a href="{ln[0][2]}" target="_blank" rel="noopener"><img src="{{{{K{rid}}}}}" alt="{html.escape(t)}" style="max-width:100%"></a>'
        if metin: s += f'<br><span style="font-size:{PX[4]}px">{Y.satir(metin, "html")}</span>'
        s += f'<br><span style="font-size:{PX[4]}px">' + " · ".join(lk(*x) for x in ln) + "</span>"
        o += [c(s), ay]
    o.append(c('<img src="{{GTAKVIM}}" alt="" style="max-width:100%">'))
    o.append(c(f'<span style="font-size:{PX[6]}px;color:{Y.KIRMIZI}"><b>🔥 SEXYKO — PVP\'NİN BAŞLADIĞI YER 🔥</b></span>'))
    return "\n".join(o)

def md():
    o = ["![]({{GSAYIM}})", "![]({{R01}})", "## SEXYKO OYUN REHBERİ", "*24 başlık, kısa kısa — detay için başlığın altındaki linke tıkla.*", "---"]
    for e, no, t, rid, metin, ln in bolumler():
        s = f"### {e} {no} · {t}"
        if rid: s += f"\n[![{t}]({{{{K{rid}}}}})]({ln[0][2]})"
        if metin: s += "\n" + Y.satir(metin, "md")
        s += "\n" + " · ".join(f"**[{i} {a} ↗]({u})**" for i, a, u in ln)
        o += [s, "---"]
    o.append("![]({{GTAKVIM}})")
    o.append("**🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥**")
    return "\n\n".join(o)

def duz():
    o = ["[RESİM GSAYIM]", "[RESİM R01]", "SEXYKO OYUN REHBERİ\n24 başlık, kısa kısa — detay için başlığın altındaki linke tıkla.", AYRAC]
    for e, no, t, rid, metin, ln in bolumler():
        s = f"{e} {no} · {t}"
        if rid: s += f"\n[RESİM K{rid}]"
        if metin: s += "\n" + Y.satir(metin, "duz")
        s += "\n" + "\n".join(f"{i} {a} → {u}" for i, a, u in ln)
        o += [s, AYRAC]
    o.append("[RESİM GTAKVIM]")
    o.append("🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥")
    return "\n\n".join(o)

BB, HT, MD, DZ = bb(), onizleme(), md(), duz()
jeton = set(re.findall(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", BB))
assert jeton == set(RES), (jeton ^ set(RES))
for a, z in [("[B]", "[/B]"), ("[CENTER]", "[/CENTER]"), ("[SIZE=", "[/SIZE]"), ("[COLOR=", "[/COLOR]"), ("[URL=", "[/URL]")]:
    assert BB.count(a) == BB.count(z), a
res = []
for rid in sorted(RES, key=lambda x: (x != "R01", [int(n) for n in re.findall(r"\d+", x)] if x[1] == "R" else [99] + [int(n) for n in re.findall(r"\d+", x)])):
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "oyun/rehber" if rid[:2] != "KF" else "forum (küçük)"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya=f"FORUM/yeni_konu/kisa/resim/{dosya}", data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)                       # 7 Eki: itemiconrepo linkli
LINK = sum(len(v[2]) for v in K.values())
KONTROL = [
    "Kısa sürüm = uzun konunun özeti: **24 bölüm aynı**, bilgi uzun konudan, yeni bilgi yok.",
    f"**{len(res) - 1} küçük resim** (360x240 kutusuna sığdırıldı) — **hazır linkli** (itemiconrepo `forum/yeni_konu/kisa/resim/`, jsDelivr).",
    f"**{LINK} yönlendirme linki** (rehber + forum.sexyko.com konuları). Resme tıklayınca bölümün ilk linki açılır.",
    "Forum d/25 (etkinlik listesi) linki **konmadı**: saatleri oyun içi takvimle çelişiyor (uzun konu ⚠ Kontrol).",
]
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{no} · {e} {t}" for e, no, t, *_ in bolumler()], "kaynak": "FORUM/_yeni_konu.py (uzun konu) özeti"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "KISA_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "KISA_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "KISA_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("KISA: bölüm", len(K), "· resim", len(res), "· link", LINK, "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

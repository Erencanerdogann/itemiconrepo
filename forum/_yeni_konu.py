# -*- coding: utf-8 -*-
# YENI FORUM KONUSU — "SexyKO Oyun Rehberi" v2 (patron 4 Eki: "forumlarda yazabilecegimiz gibi olsun, ogrendigin rehberi yeni tasarimla yeni resimlerle goster",
# "cektigin fotolari ve konularini koymayi unutma, resimli olacak, detayli rehber, oyun/forum disi bilgi ve yanlis fazla bilgi yok",
# "baslangic paketi fotolari yok", "genel fotograflandirma eksik", "yazilarin boyutu, duzeni net degil, yazi stili kotu").
# Kaynak: rehber/SEXYKO_REHBER.md (beyin) — oyun ici rehber (sexyko.com/guide), forum.sexyko.com rehber konulari, oyun ici ekranlar. Celiskili bilgi KONUYA ALINMADI (kontrol listesi).
# Stil: numarali bolumler + icindekiler, hepsi ortali, govde SIZE=4, maddeler altin ◆, vurgu altin kalin, resim alti 📷 aciklama (forumun kendi alt yazilari).
# Resim jetonu {{ID}}: R.. = oyun ici / rehber cekimlerimiz (yuklenip link yapistirilacak) · F.. = forum.sexyko.com'un kendi resmi (hizliresim linki, dogrudan acilir — olculdu 4 Eki)
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, base64
from PIL import Image

KOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KOK, "yeni_konu"); RD = os.path.join(OUT, "resim")
ALTIN, ALTIN2, GRI, YESIL, KIRMIZI = "#c8a253", "#e6c46a", "#a89f91", "#3ecf8e", "#d14841"
PX = {1: 9, 2: 10, 3: 12, 4: 15, 5: 18, 6: 22, 7: 26}
BASLIK = "📘 SEXYKO OYUN REHBERİ | Tüm Sistemler, Kısayollar ve Etkinlikler Tek Konuda | HYPER 16.10 BETA 🔥"

# ---------- resimler
RESIM = {"R01": (None, "SexyKO logo", "https://ko-yardim.com/attachments/logo_big-png.20989/")}
# Ko-Yardim tanitim konusunun GIF'leri (patron 4 Eki: "gifleri koymamissin, uzun versiyona da kisa versiyona da koyman lazim, kesinlikle")
# hazir link: baska forum Referer'i ile de 200 image/gif olculdu (4 Eki) · 1138x140, 61/71 kare, ~7 MB — gomulmez, onizleme linkten acar
RESIM["GSAYIM"] = (None, "Geri sayım GIF — Hazır Ol! (Ko-Yardım konusundan)",
                   "https://ko-yardim.com/attachments/hazir-ol-sexyko-icin-geri-sayim-basladi-_-16-ekim-beta-23-ekim-official-gif.21037/")
RESIM["GTAKVIM"] = (None, "Takvim GIF — 16 Ekim Beta · 23 Ekim Official (Ko-Yardım konusundan)",
                    "https://ko-yardim.com/attachments/takvimleri-isaretle-_-16-ekim-beta-o-23-ekim-official-gif.21039/")
for rid, dosya, acik in [
    ("R02", "R02_rehber.jpg", "Oyun içi Rehber penceresi"), ("R03", "R03_genie_main.jpg", "Knight Genie — Main"),
    ("R04", "R04_genie_misc.jpg", "Knight Genie — Misc"), ("R05", "R05_f10_1.jpg", "F10 — Oyun · Ses · Ekran · Grafik"),
    ("R06", "R06_f10_guvenlik.jpg", "F10 — Güvenlik (2. şifre)"), ("R07", "R07_skill.jpg", "Skill penceresi (K)"),
    ("R08", "R08_grind_tracker.jpg", "Grind Tracker penceresi"), ("R09", "R09_pus.jpg", "Power Up Store"),
    ("R10", "R10_cark.jpg", "Çarkıfelek (Lucky Wheel)"), ("R11", "R11_takvim.jpg", "Etkinlik Takvimi"),
    ("R12", "R12_rehber_chaos.jpg", "Rehber — Knight Chaos"), ("R13", "R13_rehber_upgrade.jpg", "Rehber — Upgrade Oranları"),
    ("R14", "R14_rehber_monster.jpg", "Rehber — Monster Listesi"), ("R15", "R15_karakter.jpg", "Character Info (U)"),
    ("R16", "R16_komut_H.jpg", "Komut listesi (H)"), ("R17", "R17_f10_2.jpg", "F10 — Gelişmiş Grafik · Efekt · Kontroller · Loot"),
    ("R18", "R18_f10_3.jpg", "F10 — Bildirimler · Font"), ("R19", "R19_envanter.jpg", "Envanter (I)"),
    ("R20", "R20_rehber_gunluk.jpg", "Rehber — Günlük Görevler"), ("R21", "R21_rehber_fragment.jpg", "Rehber — Gem & Fragment"),
    ("R22", "R22_rehber_narki.jpg", "Rehber — Narki Kırdırma"), ("R23", "R23_rehber_pus_kirdirma.jpg", "Rehber — PUS Kırdırma"),
    ("R24", "R24_rehber_draki.jpg", "Rehber — Draki's Tower"), ("R25", "R25_rehber_etkinlik_odul.jpg", "Rehber — Etkinlik Ödülleri")]:
    RESIM[rid] = (dosya, acik, "")
FORUM_URL = {}
for f in os.listdir(os.path.join(KOK, "rehber", "forum", "ham")):
    if not f[:-5].isdigit():
        continue
    d = json.load(open(os.path.join(KOK, "rehber", "forum", "ham", f), encoding="utf-8"))
    p = sorted([x for x in d.get("included", []) if x["type"] == "posts" and x["attributes"].get("contentType") == "comment"], key=lambda x: x["attributes"]["number"])
    if p:
        for n, src in enumerate(re.findall(r'<img [^>]*src="([^"]+)"', p[0]["attributes"]["contentHtml"]), 1):
            FORUM_URL[f"{f[:-5]}_{n}"] = src
for fid, acik in [
    ("10_1", "Sağ tık kırdırma (forum)"), ("10_5", "KC itemine sağ tık → direkt kırdır"), ("11_2", "Party Settings — HP · MP · Buff · Damage"),
    ("14_2", "Farm Grind Tracker açılışı"), ("24_2", "Mining Inn giriş"), ("24_3", "Mining Inn depo"), ("27_2", "Power Up Store — Basket"),
    ("30_2", "Tag Name ayar penceresi"), ("30_3", "Tag Name karakter üstünde"), ("33_2", "Daily Quest giriş (sol alt)"),
    ("34_2", "Drop Info — mob görünümü"), ("34_3", "Drop Info — item arama"), ("34_4", "Blocked drop listesi"),
    ("38_2", "Kum saati — bilgi penceresi"), ("38_3", "Kum saati — event penceresi"), ("43_1", "Chaotic Generator — tek / toplu kırdırma"),
    ("44_2", "Solo Pelerin seçim ekranı"), ("44_3", "Solo Pelerin bonusları"), ("44_4", "Beşiktaş pelerini"), ("44_5", "Galatasaray pelerini"),
    ("44_6", "Fenerbahçe pelerini"), ("44_7", "Trabzonspor pelerini"), ("46_1", "Equipment View açılışı"), ("46_2", "Equipment / Ability penceresi"),
    ("49_1", "Rebirth gereksinimleri"), ("49_2", "Rebirth işlemi"), ("50_1", "Drop Search — Ctrl + D"), ("51_1", "PUS indirim kodu (kupon)"),
    ("52_1", "[Teleport] Portal"), ("52_2", "Slot Teleport — mob seçimi"), ("53_1", "Rogue başlangıç ekipmanı"), ("53_2", "Mage başlangıç ekipmanı"),
    ("53_3", "Priest başlangıç ekipmanı"), ("53_4", "Warrior başlangıç ekipmanı"), ("53_5", "Kurian başlangıç ekipmanı")]:
    RESIM["F" + fid] = (f"F{fid}.jpg", acik, FORUM_URL[fid])

# rehber gorselleri -> rehberdeki asil sayfa (patron 4 Eki: "Rehber — Upgrade Oranlari link olmasi lazim"; hepsi 200 olculdu)
REHBER_LINK = {"R02": ("Rehberin tamamı", "/guide/book"), "R12": ("Knight Chaos", "/guide/book/chaos"), "R13": ("Upgrade Oranları", "/guide/upgrade"),
               "R14": ("Monster Listesi", "/guide/monsters"), "R20": ("Günlük Görevler", "/guide/daily-quests"), "R21": ("Gem & Fragment", "/guide/fragment"),
               "R22": ("Narki Kırdırma", "/guide/narki"), "R23": ("PUS Kırdırma", "/guide/pus-crash"), "R24": ("Draki's Tower", "/guide/book/draki"),
               "R25": ("Etkinlik Ödülleri", "/guide/event-rewards")}
MAVI = "#4fa3ff"


def rl(rid):
    a, p = REHBER_LINK[rid]
    return a, "https://sexyko.com" + p


# ---------- icerik
B = []
def ekle(*b): B.append(b)

ekle("afis", "GSAYIM")
ekle("banner", "R01")
ekle("baslik", "SEXYKO OYUN REHBERİ", "Yeni başlayan da, 16 yıllık emektar da — bilmen gereken her şey tek konuda, oyun içi görüntülerle.")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "📖", "OYUNUN İÇİNDEKİ REHBER")
ekle("p", "Sol üstteki **📖 kitap** simgesine tıkla, rehber oyunun içinde açılır. Upgrade oranları, dönüşüm ve madencilik sayfaları **sunucudan canlı** beslenir. Aynı rehber web'de de açık: [[https://sexyko.com/guide/book|sexyko.com/guide]]")
ekle("img", "R02", "Oyun içi Rehber — 14 sekme: Oyun Rehberi, Monster Listesi, Görevler, Upgrade, Drop Arama, Gem & Fragment, Çapraz Takas, Shozin, Narki, PUS Kırdırma, Madencilik, Günlük Görevler, Etkinlik Ödülleri")
ekle("liste", ["**305 monster** — spawn noktası + yüzdeli drop listesi", "**998 görev** — NPC, şart ve ödül", "**380 Shozin tarifi** — malzeme + çıkma oranı",
               "**139 çapraz takas** · **45 PUS paketi** · Narki'ye verilebilen **1.893 eşya**", "**Ctrl + K** ile rehberde ara — Türkçe karakter yazmana gerek yok"])
ekle("ayrac")

ekle("h", "⌨️", "KISAYOLLAR VE ARAYÜZ")
ekle("liste", ["**F10** — Ayarlar (11 sekme)", "**K** — Skill · Preset · Save Quickslot", "**U** — Character Info · Perks · Rebirth · Stat Preset",
               "**H** — Komutlar · Solo Pelerin · Yayıncı", "**I** — Envanter", "**Ctrl + D** (item üstünde) — item hangi moblardan, yüzde kaçla düşüyor",
               "**Shift + C** — arayüzü gizle", "**⏳ Kum saati** (sağ üst) — etkinlik takvimi · **⏱** (sol üst) — Grind Tracker",
               "**🛒** (sol alt) — Power Up Store · **🎡** (sol alt) — Çarkıfelek", "**Genie çubuğu** (sağ üst) — ▶ başlat · ■ durdur · ⬇ ayarlar · kalan süre"])
ekle("imgs", ["R16", "R19"], "H — Komut listesi · I — Envanter")
ekle("ayrac")

ekle("h", "🎁", "BAŞLANGIÇ PAKETİ")
ekle("p", "Karakterini oluşturduğunda **seçtiğin job'a uygun başlangıç ekipmanı** hazır gelir.")
ekle("liste", ["3 günlük **EXP Premium** · 3 günlük **Valkyrie Set** · 3 günlük **Pathos (2x)**", "3 günlük **Kanat** · 3 günlük **Magic Bag** · 3 günlük **War Tattoo**",
               "**5.000 HP + 5.000 MP** pot · **24 saatlik Genie**"])
ekle("img", "F53_4", "Warrior başlangıç ekipmanı")
ekle("img", "F53_1", "Rogue başlangıç ekipmanı")
ekle("img", "F53_2", "Mage başlangıç ekipmanı")
ekle("img", "F53_3", "Priest başlangıç ekipmanı")
ekle("img", "F53_5", "Kurian başlangıç ekipmanı")
# rehber /guide/beginner-items, sinif sinif (patron 4 Eki: "baslangic paketleri hala yok"; veri rehber/web/beginner_items_sinif.json, ITEM 18/21/20/19/18 olculdu)
ekle("h2", "📋 Her job'un başlangıç değerleri")
ekle("liste", ["**Level 83** · **1.000.000.000 coin** · **1.000 NP**", "**302 bonus stat** · **148 serbest skill puanı**"])
ekle("liste", ["**Warrior** — STR 65 · STA 65 · DEX 60 · INT 50 · CHA 50", "Thigh Bone · Warrior Earring ×2 · Warrior Pendant · Mercenary Ring ×2 · Body Belt"])
ekle("liste", ["**Rogue** — STR 60 · STA 60 · DEX 70 · INT 50 · CHA 50", "Skeleton Rib ×2 · Clarence's Training Bow · 500 Arrow · Assassin Earring ×2 · Warrior Pendant · Assassin Ring ×2 · Body Belt"])
ekle("liste", ["**Mage** — STR 50 · STA 60 · DEX 60 · INT 70 · CHA 50", "Eerie Skull Cane ×3 · Priest Earring ×2 · Cleric Pendant · Priest Ring ×2 · Body Belt"])
ekle("liste", ["**Priest** — STR 50 · STA 60 · DEX 60 · INT 70 · CHA 50", "Bone Breaker · Wolf Slayer Shield · Priest Earring ×2 · Cleric Pendant · Priest Ring ×2 · Body Belt"])
ekle("liste", ["**Kurian** — STR 65 · STA 65 · DEX 60 · INT 50 · CHA 50", "Thigh Bone · Warrior Earring ×2 · Warrior Pendant · Mercenary Ring ×2 · Body Belt"])
ekle("liste", ["**Her job'a:** War Helmet · War Pauldron · War Pad · War Gauntlet · War Boots",
               "**Çantada:** 1.000 Holy Water of Grace · 1.000 Spirit Potion · 30 Scroll of 1500HP Up · 30 Scroll of Armor 300 · 30 Scroll of Attack · Speed Up Rice Cake (Priest 30, diğerleri 3)"])
ekle("rlink", "Başlangıç Eşyaları", "/guide/beginner-items")
ekle("ayrac")

ekle("h", "🧞", "GELİŞMİŞ GENIE")
ekle("liste", ["**8 Attack + 8 Buff/Self + 8 Party** skill slotu — her satır ayrı açılır / kapanır", "HP ve MP potunu **yüzdeyle** ayarla (Smart Auto Use)",
               "Party heal ve self heal eşikleri · **Attack range** kaydırıcısı", "**Monster List to Attack** — Add Target / Remove / Clear All: Genie sadece listedeki moblara vurur"])
ekle("img", "R03", "Knight Genie — Main sekmesi")
ekle("liste", ["**Combat:** R ile saldır · hedefe git · avlanma merkezine dön", "**Maintenance:** çekiçle tamir · premium flash bonusunu koru · pet besle",
               "**Return to town:** party dağılınca · party ölünce · ok bitince"])
ekle("img", "R04", "Knight Genie — Misc sekmesi")
ekle("not", "Genie açıkken skill bar kilitlenir; durdurunca elle kullanıma dönersin.")
ekle("ayrac")

ekle("h", "⚙️", "F10 AYARLAR — 11 SEKME")
ekle("p", "**Oyun · Ses · Ekran · Grafik · Gelişmiş Grafik · Efekt · Kontroller · Loot · Bildirimler · Font · Güvenlik**")
ekle("liste", ["**Oyun:** kamera · görev takip penceresi · hava durumu ve günün saati", "**Ses:** müzik, çevre, karakter & NPC, öldürme anonsları ayrı ayrı",
               "**Ekran:** pencere modu · çözünürlük · FPS sınırı · **arayüz ölçeği 1x / 1.25x / 1.5x / 2x** · HP/MP çubuğu", "**Grafik:** gölge, arazi, HDR, Bloom, ACES, MSAA / SMAA, AMD FSR 1"])
ekle("img", "R05", "F10 — Oyun · Ses · Ekran · Grafik")
ekle("liste", ["**Gelişmiş Grafik:** kontrast, doygunluk, sıcaklık, ton + hazır renk profilleri", "**Efekt:** CZ'de diğer oyuncuların skillerini, hasar yazılarını kapat",
               "**Kontroller:** gamepad + hareket tuşları — değişiklik anında kaydedilir", "**Loot:** değer (Magic / Rare / Craft / Unique / Upgrade), upgrade, tür ve coin değerine göre filtre"])
ekle("img", "R17", "F10 — Gelişmiş Grafik · Efekt · Kontroller · Loot")
ekle("liste", ["**Bildirimler:** sistem önerileri · slave pazar satışı · kritik kaynak · repair · death notice", "**Font:** chat, sistem, nick, klan, tag ve eşya adet yazı boyutları"])
ekle("img", "R18", "F10 — Bildirimler · Font")
ekle("h2", "🔐 Güvenlik — 2. Şifre (Desen)")
ekle("p", "Desen etkinken her girişte sorulur. **F10 → Güvenlik → Deseni Değiştir**.")
ekle("img", "R06", "F10 — Güvenlik")
ekle("ayrac")

ekle("h", "⚔️", "SKILL PRESET & QUICK SLOT")
ekle("p", "**K** ile aç. **Preset** skill puanı dağılımını, **Save Quickslot** skill bar dizilimini kaydeder — **4 ayrı Quick Slot**, istediğin ismi ver. PK, farm, party ve event düzenleri arasında hızlıca geç.")
ekle("img", "R07", "Skill penceresi (K)")
ekle("ayrac")

ekle("h", "👥", "PARTY AYARLARI")
ekle("p", "Party panelindeki ayarlardan party üyelerinin **HP · MP · Buff · Damage** bilgisini ayrı ayrı aç / kapat — party ekranını kendi oyun tarzına göre düzenle.")
ekle("img", "F11_2", "Party Settings — HP · MP · Buff · Damage")
ekle("ayrac")

ekle("h", "🖱️", "SAĞ TIK DEVRİ — NPC'YE GİTMEYE SON")
ekle("img", "F10_1", "Sağ tık kırdırma")
ekle("liste", ["**KC · Dragon Wing · Gem · Fragment · Chest:** iteme sağ tıkla, NPC'ye gitmeden kırdır", "Gem / Fragment / Chest kırınca: **Direkt Sat** ya da **Inventory'ne Al**"])
ekle("img", "F10_5", "KC itemine sağ tık → direkt kırdır")
ekle("h2", "♻️ Chaotic Generator — Tek / Toplu Kırdırma")
ekle("liste", ["**Exchange One** — tek tek · **Exchange All** — envanterdeki boş slot kadar toplu", "Gelen ödüllerden istemediğini **sağ tıkla karart** → **Sell** (sat) · **Storage** (bankaya) · **Trash** (sil, coin vermez)"])
ekle("img", "F43_1", "Chaotic Generator penceresi")
ekle("h2", "🏷️ Tag Name — Make Over — Nick — Job Changer")
ekle("liste", ["**Tag Name:** sağ tık → ismini yaz → **RGB** ile rengini seç", "**Make Over Coupon:** sağ tık → saç ve yüz", "**Scroll of Identity:** sağ tık → yeni nick",
               "**Job Changer:** önce üstündeki tüm itemleri çıkar, sonra sağ tık → job seç"])
ekle("imgs", ["F30_2", "F30_3"], "Tag Name ayar penceresi · karakter üstünde")
ekle("ayrac")

ekle("h", "🦸", "SOLO PELERİN")
ekle("liste", ["Clana girmeden pelerin — PUS'tan al → sağ tık → desen seç → **Purchase** → **Confirm**", "**15 gün** · **250 HP · 250 MP · 25 DEF · %3 AP**",
               "Takım pelerinleri: **Beşiktaş · Galatasaray · Fenerbahçe · Trabzonspor**", "Sonradan değiştir: **H → Solo Pelerin** sekmesi · pelerin efekti **500 KC**"])
ekle("imgs", ["F44_2", "F44_3"], "Solo Pelerin seçim ekranı · bonuslar")
ekle("imgs", ["F44_4", "F44_5"], "Beşiktaş · Galatasaray pelerinleri")
ekle("imgs", ["F44_6", "F44_7"], "Fenerbahçe · Trabzonspor pelerinleri")
ekle("ayrac")

ekle("h", "💎", "GEM & FRAGMENT · NARKİ · PUS KIRDIRMA")
ekle("p", "Neyi kırdırırsan **ne çıkar, yüzde kaç** — hepsi rehberde.")
ekle("img", "R21", "Rehber — Gem & Fragment: sandık, gem ve fragmentlerden çıkanlar")
ekle("liste", ["**Narki:** verdiğin eşya yok olur, karşılığında **tek ödül** çekilir; havuzu verdiğin eşya belirler",
               "4 havuz: **Özel silahlar · Silah ve zırhlar · Eski aksesuarlar · Aksesuarlar** — 1.893 eşya kabul edilir",
               "Bağlı, kiralık, mühürlü veya süreli eşya verilemez · kırdırma geri alınamaz"])
ekle("img", "R22", "Rehber — Narki havuzları ve çıkma oranları")
ekle("p", "**PUS Kırdırma:** 45 paketin içinden çıkanların tamamı — ör. **VIP Package** → 20 eşyanın hepsi birden.")
ekle("img", "R23", "Rehber — PUS Kırdırma")
ekle("ayrac")

ekle("h", "🎯", "DROP INFO · DROP SEARCH")
ekle("liste", ["Moba tıkla → alttaki **Drop Info** kutusu: düşen itemler ve yüzdeleri", "Üstteki aramaya **item adını** yaz → hangi moblardan, yüzde kaçla düştüğü"])
ekle("imgs", ["F34_2", "F34_3"], "Drop Info — mob görünümü · item arama")
ekle("liste", ["Listede item'a **sağ tık** → kararır → **Auto Loot toplamaz**", "Yanlış engellediysen **Blocked** listesinden kaldır", "Item üstünde açıklamanın altında **CTRL + D** yazıyorsa → bas, drop kaynağını gör"])
ekle("imgs", ["F34_4", "F50_1"], "Blocked listesi · Drop Search (Ctrl + D)")
ekle("img", "R14", "Rehber — Monster Listesi")
ekle("ayrac")

ekle("h", "🌀", "SLOT TELEPORT")
ekle("p", "**[Teleport] Portal** NPC'sine git → mobu seç → **250.000 coin** ile direkt slotuna ışınlan. **Luferson · El Morad Castle · Eslant**.")
ekle("imgs", ["F52_1", "F52_2"], "[Teleport] Portal · mob seçimi")
ekle("ayrac")

ekle("h", "📊", "GRIND TRACKER")
ekle("p", "Sol üstteki **⏱** simgesi: farm süresi, toplanan coin, **saatlik ortalama coin**, düşen itemler ve **saatlik item adedi** — slotların verimini oyun içinden karşılaştır.")
ekle("img", "F14_2", "Farm Grind Tracker açılışı")
ekle("img", "R08", "Grind Tracker penceresi")
ekle("ayrac")

ekle("h", "⛏️", "AUTO MINING — MINING INN")
ekle("liste", ["Auto Mining ürünleri **Mining Inn**'de birikir — işaretli kutuya tıkla", "Mining Inn deposu **tek yönlü**: item **çekebilirsin**, item **bırakamazsın**"])
ekle("imgs", ["F24_2", "F24_3"], "Mining Inn giriş · depo")
ekle("ayrac")

ekle("h", "🛒", "POWER UP STORE + KUPON")
ekle("liste", ["**Basket** ile toplu alışveriş · **Knight Cash** ve **SexyBalance** bakiyesi ayrı görünür", "**Kupon alanı → CHECK:** sponsor yayıncı indirim kodu — kampanya dönemlerinde %30'a varan",
               "Kupon tekli üründe de, Basket'te de geçer · **VIP** ve **Farm** paketlerinde geçmez"])
ekle("img", "R09", "Power Up Store (oyun içi)")
ekle("imgs", ["F27_2", "F51_1"], "Basket · indirim kodu")
ekle("ayrac")

ekle("h", "🎡", "ÇARKIFELEK")
ekle("p", "**350 KC** ile sınırsız çevir ya da **2 saat online** kal, **1 ücretsiz** çevirme hakkı kazan.")
ekle("img", "R10", "Çarkıfelek (Lucky Wheel)")
ekle("ayrac")

ekle("h", "📅", "GÜNLÜK GÖREVLER")
ekle("liste", ["Sol alttaki **Daily Quest** bölümüne tıkla → görevi seç → **Detail** → **Accept**", "Accept'e basınca süre başlar — süre dolmadan tamamla, **ödül otomatik** gelir",
               "Rehberde **23 günlük görev** (Ronark Land) — ör. **Atross & Riote:** 10 Atross + 10 Lyot → **500 Knight Cash**"])
ekle("img", "F33_2", "Daily Quest giriş (sol alt)")
ekle("img", "R20", "Rehber — Günlük Görevler")
ekle("ayrac")

ekle("h", "⏳", "ETKİNLİK TAKVİMİ")
ekle("p", "Sağ üstteki **kum saati**: üzerine gel = anlık bilgi · tıkla = takvim · **Bildirim kur** → etkinlikten 5 dakika önce uyarı.")
ekle("imgs", ["F38_2", "F38_3"], "Kum saati — bilgi penceresi · event penceresi")
ekle("img", "R11", "Etkinlik Takvimi (oyun içi)")
ekle("liste", ["**Chaos Dungeon** — her gün 00:00", "**Border Defense War** — her gün 01:00 · 15:30 · 19:30", "**Juraid Mountain** — her gün 02:00 · 18:00",
               "**Chaos Stone War** — her gün 18:30", "**Rank War** — her gün 21:30", "**Draki's Tower** — Pazar 00:00", "**Castle Siege War** — Pazar 22:00"])
ekle("ayrac")

ekle("h", "🏆", "ETKİNLİK KURALLARI")
ekle("liste", ["**Knight Chaos:** 18 kişi, ücretsiz, 20 dakika — herkes aynı karakter, 10.000 HP; en çok öldüren, en az ölen öne geçer",
               "**Border Defense War:** 8v8, 30 dakika — altarı üsse taşı 80 puan, kill 2 puan; 600 puana ilk ulaşan kazanır",
               "**Juraid Mountain:** 8v8 PvPvE, 50 dakika, Lv 70+ — Devabird'ü öldüren ırk kazanır",
               "**Forgotten Temple:** 80 kişi, 100.000 Noah — [Priest] Iris (Moradon 815,921), dalga dalga gelen canavarlar",
               "**Castle Siege War:** Delos kalesi için klan savaşı, 60 dakika — kayıt 100.000.000 Noah",
               "**Knight Royale:** 80 kişilik battle royale, herkes 1. seviyeden başlar",
               "**Under the Castle:** Lv 75+, 4 boss — ölünce ekipman yanar, **Life Crystal** taşı"])
ekle("img", "R12", "Rehber — Knight Chaos kuralları ve ödülleri")
ekle("img", "R25", "Rehber — Etkinlik Ödülleri (17 etkinlik)")
ekle("ayrac")

ekle("h", "🐉", "DRAKI'S TOWER")
ekle("liste", ["Giriş: El Morad'lar **El Morad Castle**, Karus'lar **Luferson Castle** — **Draki Rift**", "**5 bölüm**, her bölümde katlar ve bosslar · son boss **Draki El Rasaga**",
               "Günde **3 giriş** · sıfırlama her gün **18:00** · zamana karşı yarış, **aylık sıralama**",
               "1-3. bölüm sonlarında **[Sundries] Ghost** (tamir + iksir) ve **[Monster Strategist]** (AP · DEF · 1.000 HP takviyesi)"])
ekle("img", "R24", "Rehber — Draki's Tower")
ekle("ayrac")

ekle("h", "🔨", "UPGRADE ORANLARI")
ekle("p", "Oranlar rehberde ve **Anvil'de canlı** görünür; en yüksek kademe **+8**. Örnek — **Blessed Upgrade Scroll (High Class):**")
ekle("liste", ["+1 → +2 **%100** · +2 → +3 **%100** · +3 → +4 **%95** · +4 → +5 **%75**", "+5 → +6 **%50** · +6 → +7 **%25** · +7 → +8 **%4**",
               "**Trina's Piece** ile oran artar · ücret 120.000 – 360.000 coin"])
ekle("img", "R13", "Rehber — Upgrade Oranları")
ekle("ayrac")

ekle("h", "⭐", "REBIRTH")
ekle("p", "**83 Level + %100 EXP + 100.000.000 coin + 10.000 NP** → Rebirth. Her Rebirth seviyesi **+2 stat puanı**. Durumunu **U → Rebirth** sekmesinden gör.")
ekle("imgs", ["F49_1", "F49_2"], "Rebirth gereksinimleri · Rebirth işlemi")
ekle("img", "R15", "Character Info (U)")
ekle("ayrac")

ekle("h", "👁️", "EQUIPMENT VIEW")
ekle("liste", ["Karaktere **sağ tık → Equipment View**", "Takılı ekipmanlar ve **upgrade seviyeleri** · inventory", "**Level · HP · MP · SP · STR · DEX · INT** · Attack · Defence",
               "**6 resistance** (Fire · Ice · Lightning · Magic · Curse · Poison) · aktif **Buff List**"])
ekle("img", "F46_1", "Equipment View açılışı")
ekle("img", "F46_2", "Equipment / Ability penceresi")
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["🌐 Web: [[https://sexyko.com|sexyko.com]]", "📘 Rehber: [[https://sexyko.com/guide/book|sexyko.com/guide]]", "💬 Forum: [[https://forum.sexyko.com|forum.sexyko.com]]",
               "📥 Client: [[https://sexyko.com/download|sexyko.com/download]]"])
ekle("ayrac")
ekle("afis", "GTAKVIM")
ekle("son", "🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥")

KONTROL = [
    "Etkinlik saatleri **oyun içi takvimden** (3 Eki 23:40, istemcinin bağlı olduğu sunucu — büyük ihtimalle Myra). Forum d/25 farklı saat yazıyor (BDW 02:00/13:00/18:00/23:00, JR 07:40/22:40, Chaos 00:00/12:00/19:00) → HYPER saatleri yayından önce teyit.",
    "Rehber sayıları (305 monster, 998 görev, 380 tarif, 139 takas, 45 paket, 1.893 eşya) sexyko.com/guide **Hyper** sunucusundan (3-4 Eki).",
    "Konuya ALINMADI (kaynaklar çelişiyor): Royal NP bağışları (d/36 ≠ d/39) · Old takı dönüşümü (forum Shozin ≠ oyun duyurusu Juel %30) · başlangıç level'ı (Ko-Yardım 1 Lv ≠ web 83 Lv) · Solo pelerin desen sayısı (21 ≠ 20) · Draki min level (80 ≠ 70).",
    "**F** ile başlayan 35 resim forum.sexyko.com'un kendi görseli — linkleri **hizliresim.com**'da, 4 Eki'de hepsi açıldı (başka forum Referer'ı ile 200). Ama hizliresim'de forumun 50 resmi zaten öldü → bunlar da ölebilir; yedek olarak indir + kendi yükleyicine at.",
    "**Bütün resimler hazır linkli** (7 Eki): GitHub `itemiconrepo/forum/` → jsDelivr CDN. Yükle-yapıştır yok; istersen kendi linkini kutuya girersin.",
    "Upgrade örneği sitedeki Hyper tablosundan: Blessed Upgrade Scroll / High Class. +8 → +9 ve üstü 'şu anda kapalı'.",
]

# ---------- cizim
BASLIKLAR = [(b[1], b[2]) for b in B if b[0] == "h"]
NO = {}
for i, (e, t) in enumerate(BASLIKLAR, 1):
    NO[(e, t)] = f"{i:02d}"


# PATRON 7 Eki: "genel olarak yazi fontlarini biraz buyutelim, ozellikle skill master'da" -> sonra: "butun forum bbcode'larina duzen getir,
# abartili buyuk kucuk farklar olmasin, basliklar haric" -> basliklar DISINDAKI her yazi (govde, liste, not, resim alti) TEK BOY: SIZE 5 (18 px).
# Basliklar (5-7) ayni. Tek gecis. Butun uretilen konular (yeni / kisa / skill / odul / sezon); tanitim _konu_kit.py'de ayni kural.
FONT_ADIM = {3: 5, 4: 5}


def buyut_bb(s):
    return re.sub(r"\[SIZE=([34])\]", lambda m: f"[SIZE={FONT_ADIM[int(m.group(1))]}]", s)


def buyut_ht(s):
    return re.sub(r"font-size:(12|15)px", lambda m: f"font-size:{PX[FONT_ADIM[{12: 3, 15: 4}[int(m.group(1))]]]}px", s)


def satir(t, f):
    def link(m):
        u, x = m.group(1), m.group(2)
        return {"bb": f"[URL={u}]{x}[/URL]", "html": f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(x)}</a>',
                "md": f"[{x}]({u})", "duz": f"{x} ({u})"}[f]
    out = ""
    for p in re.split(r"(\[\[[^|\]]+\|[^\]]+\]\])", t):
        m = re.match(r"\[\[([^|\]]+)\|([^\]]+)\]\]", p)
        if m:
            out += link(m); continue
        if f == "html":
            p = html.escape(p)
        p = re.sub(r"\*\*(.+?)\*\*", {"bb": rf"[B][COLOR={ALTIN2}]\1[/COLOR][/B]", "html": rf'<b style="color:{ALTIN2}">\1</b>', "md": r"**\1**", "duz": r"\1"}[f], p)
        out += p
    return out


def bb():
    o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"[CENTER][IMG]{{{{{b[1]}}}}}[/IMG][/CENTER]")
        elif k == "baslik": o.append(f"[CENTER][SIZE=7][B][COLOR={ALTIN}]{b[1]}[/COLOR][/B][/SIZE]\n[SIZE=4][COLOR={GRI}]{b[2]}[/COLOR][/SIZE][/CENTER]")
        elif k == "icindekiler": o.append(f"[CENTER][SIZE=5][B][COLOR={ALTIN}]📑 İÇİNDEKİLER[/COLOR][/B][/SIZE]\n[SIZE=4]"
                                          + "\n".join(f"[COLOR={ALTIN}]{NO[x]}[/COLOR] · {x[0]} {x[1].title() if False else x[1]}" for x in BASLIKLAR) + "[/SIZE][/CENTER]")
        elif k == "ayrac": o.append(f"[CENTER][COLOR={ALTIN}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/COLOR][/CENTER]")
        elif k == "h": o.append(f"[CENTER][SIZE=6][B][COLOR={ALTIN}]{b[1]} {NO[(b[1], b[2])]} · {b[2]}[/COLOR][/B][/SIZE][/CENTER]")
        elif k == "h2": o.append(f"[CENTER][SIZE=5][B][COLOR={ALTIN2}]{b[1]}[/COLOR][/B][/SIZE][/CENTER]")
        elif k == "p": o.append(f"[CENTER][SIZE=4]{satir(b[1], 'bb')}[/SIZE][/CENTER]")
        elif k == "liste": o.append("[CENTER][SIZE=4]" + "\n".join(f"[COLOR={ALTIN}]◆[/COLOR] {satir(x, 'bb')}" for x in b[1]) + "[/SIZE][/CENTER]")
        elif k == "img" and b[1] in REHBER_LINK:
            a, u = rl(b[1]); alt = "" if b[2].startswith("Rehber —") else f"[SIZE=3][COLOR={GRI}]▲ {b[2]}[/COLOR][/SIZE]\n"
            o.append(f"[CENTER][URL={u}][IMG]{{{{{b[1]}}}}}[/IMG][/URL]\n{alt}[SIZE=4][URL={u}][B][COLOR={MAVI}]📘 Rehberde aç: {a} ↗[/COLOR][/B][/URL][/SIZE][/CENTER]")
        elif k == "img": o.append(f"[CENTER][IMG]{{{{{b[1]}}}}}[/IMG]\n[SIZE=3][COLOR={GRI}]▲ {b[2]}[/COLOR][/SIZE][/CENTER]")
        elif k == "imgs": o.append("[CENTER]" + " ".join(f"[IMG]{{{{{x}}}}}[/IMG]" for x in b[1]) + f"\n[SIZE=3][COLOR={GRI}]▲ {b[2]}[/COLOR][/SIZE][/CENTER]")
        elif k == "not": o.append(f"[CENTER][SIZE=4][COLOR={YESIL}]💡 {satir(b[1], 'bb')}[/COLOR][/SIZE][/CENTER]")
        elif k == "rlink": o.append(f"[CENTER][SIZE=4][URL=https://sexyko.com{b[2]}][B][COLOR={MAVI}]📘 Rehberde aç: {b[1]} ↗[/COLOR][/B][/URL][/SIZE][/CENTER]")
        elif k == "son": o.append(f"[CENTER][SIZE=6][B][COLOR={KIRMIZI}]{b[1]}[/COLOR][/B][/SIZE][/CENTER]")
    return "\n\n".join(o)


def onizleme():
    c = lambda x: f'<div style="text-align:center">{x}</div>'
    cap = lambda t: f'<span style="font-size:{PX[3]}px;color:{GRI}">▲ {html.escape(t)}</span>'
    o = []
    for b in B:
        k = b[0]
        if k == "banner": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="" style="max-width:100%;width:520px">'))
        elif k == "afis": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="" style="max-width:100%">'))
        elif k == "baslik": o.append(c(f'<span style="font-size:{PX[7]}px;color:{ALTIN}"><b>{html.escape(b[1])}</b></span><br><span style="font-size:{PX[4]}px;color:{GRI}">{html.escape(b[2])}</span>'))
        elif k == "icindekiler": o.append(c(f'<span style="font-size:{PX[5]}px;color:{ALTIN}"><b>📑 İÇİNDEKİLER</b></span><br><span style="font-size:{PX[4]}px">'
                                           + "<br>".join(f'<span style="color:{ALTIN}">{NO[x]}</span> · {html.escape(x[0])} {html.escape(x[1])}' for x in BASLIKLAR) + "</span>"))
        elif k == "ayrac": o.append(c(f'<span style="color:{ALTIN}">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>'))
        elif k == "h": o.append(c(f'<span style="font-size:{PX[6]}px;color:{ALTIN}"><b>{b[1]} {NO[(b[1], b[2])]} · {html.escape(b[2])}</b></span>'))
        elif k == "h2": o.append(c(f'<span style="font-size:{PX[5]}px;color:{ALTIN2}"><b>{html.escape(b[1])}</b></span>'))
        elif k == "p": o.append(c(f'<span style="font-size:{PX[4]}px">{satir(b[1], "html")}</span>'))
        elif k == "liste": o.append(c(f'<span style="font-size:{PX[4]}px">' + "<br>".join(f'<span style="color:{ALTIN}">◆</span> {satir(x, "html")}' for x in b[1]) + "</span>"))
        elif k == "img" and b[1] in REHBER_LINK:
            a, u = rl(b[1]); alt = "" if b[2].startswith("Rehber —") else cap(b[2]) + "<br>"
            o.append(c(f'<a href="{u}" target="_blank" rel="noopener"><img src="{{{{{b[1]}}}}}" alt="{html.escape(b[2])}" style="max-width:100%"></a><br>{alt}'
                       f'<a href="{u}" target="_blank" rel="noopener" style="font-size:{PX[4]}px;color:{MAVI};font-weight:700;text-decoration:none">📘 Rehberde aç: {html.escape(a)} ↗</a>'))
        elif k == "img": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="{html.escape(b[2])}" style="max-width:100%"><br>{cap(b[2])}'))
        elif k == "imgs": o.append(c(" ".join(f'<img src="{{{{{x}}}}}" alt="" style="max-width:{96 // len(b[1])}%;vertical-align:middle">' for x in b[1]) + f"<br>{cap(b[2])}"))
        elif k == "not": o.append(c(f'<span style="font-size:{PX[4]}px;color:{YESIL}">💡 {satir(b[1], "html")}</span>'))
        elif k == "rlink": o.append(c(f'<a href="https://sexyko.com{b[2]}" target="_blank" rel="noopener" style="font-size:{PX[4]}px;color:{MAVI};font-weight:700;text-decoration:none">📘 Rehberde aç: {html.escape(b[1])} ↗</a>'))
        elif k == "son": o.append(c(f'<span style="font-size:{PX[6]}px;color:{KIRMIZI}"><b>{html.escape(b[1])}</b></span>'))
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
        elif k == "h2": o.append(f"### {b[1]}")
        elif k in ("p", "not"): o.append(("💡 " if k == "not" else "") + satir(b[1], "md"))
        elif k == "liste": o.append("\n".join(f"- {satir(x, 'md')}" for x in b[1]))
        elif k == "img" and b[1] in REHBER_LINK:
            a, u = rl(b[1]); o.append(f"[![{b[2]}]({{{{{b[1]}}}}})]({u})\n" + ("" if b[2].startswith("Rehber —") else f"▲ *{b[2]}*  \n") + f"**[📘 Rehberde aç: {a} ↗]({u})**")
        elif k == "img": o.append(f"![{b[2]}]({{{{{b[1]}}}}})\n▲ *{b[2]}*")
        elif k == "imgs": o.append(" ".join(f"![]({{{{{x}}}}})" for x in b[1]) + f"\n▲ *{b[2]}*")
        elif k == "rlink": o.append(f"**[📘 Rehberde aç: {b[1]} ↗](https://sexyko.com{b[2]})**")
        elif k == "son": o.append(f"**{b[1]}**")
    return "\n\n".join(o)


def duz():
    o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"[RESİM {b[1]}]")
        elif k == "img" and b[1] in REHBER_LINK: o.append(f"[RESİM {b[1]}: {b[2]}]\n📘 Rehberde aç: {rl(b[1])[0]} → {rl(b[1])[1]}")
        elif k == "img": o.append(f"[RESİM {b[1]}: {b[2]}]")
        elif k == "imgs": o.append(f"[RESİM {' + '.join(b[1])}: {b[2]}]")
        elif k == "baslik": o.append(f"{b[1]}\n{b[2]}")
        elif k == "icindekiler": o.append("İÇİNDEKİLER\n" + "\n".join(f"{NO[x]} · {x[0]} {x[1]}" for x in BASLIKLAR))
        elif k == "ayrac": o.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        elif k == "h": o.append(f"{b[1]} {NO[(b[1], b[2])]} · {b[2]}")
        elif k in ("h2", "son"): o.append(b[1])
        elif k in ("p", "not"): o.append(("💡 " if k == "not" else "") + satir(b[1], "duz"))
        elif k == "liste": o.append("\n".join(f"◆ {satir(x, 'duz')}" for x in b[1]))
        elif k == "rlink": o.append(f"📘 Rehberde aç: {b[1]} → https://sexyko.com{b[2]}")
    return "\n\n".join(o)


BB, HT, MD, DZ = bb(), onizleme(), md(), duz()
BB, HT = buyut_bb(BB), buyut_ht(HT)
jeton = set(re.findall(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", BB))
kullanilmayan = set(RESIM) - jeton
assert jeton <= set(RESIM), jeton - set(RESIM)
assert not kullanilmayan, kullanilmayan
for a, z in [("[B]", "[/B]"), ("[CENTER]", "[/CENTER]"), ("[I]", "[/I]")]:
    assert BB.count(a) == BB.count(z), a
for a, z in [("[SIZE=", "[/SIZE]"), ("[COLOR=", "[/COLOR]"), ("[URL=", "[/URL]")]:
    assert BB.count(a) == BB.count(z), a
res = []
for rid in sorted(RESIM, key=lambda x: (x[0] != "R", x[0] == "F", [int(n) for n in re.findall(r"\d+", x)])):
    dosya, acik, url = RESIM[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum" if rid.startswith("F") else "oyun/rehber"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya=f"FORUM/yeni_konu/resim/{dosya}", data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)                       # 7 Eki: butun resimler itemiconrepo linkli (yukle-yapistir yok)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL, "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in BASLIKLAR],
        "kaynak": "FORUM/rehber/SEXYKO_REHBER.md (beyin, 3-4 Eki)"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "YENI_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "YENI_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "YENI_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("bölüm", len(BASLIKLAR), "· blok", len(B), "· resim", len(res), f"(oyun/rehber {sum(1 for r in res if r['kaynak'] != 'forum')} · forum {sum(1 for r in res if r['kaynak'] == 'forum')})",
      "· [IMG]", BB.count("[IMG]"), "· bbcode", len(BB), "· gömülü", sum(r["kb"] or 0 for r in res), "KB")

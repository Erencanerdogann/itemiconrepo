# SexyKO — Skill & Master (araştırma beyni)

6 Ekim 2026 · DOKTOR · patron emri: "Basit Skill Master ve skiller için detaylı bir forum konusu — önce öğren, sonra MD, sonra resimle, bütün joblar için".
Kaynak sırası (patron): **rehber → site → admin → genel KO rehberi**. Her satırın kaynağı yanında. Forum konusu: `HTML/FORUM_KONU.html` → **⚔️ Skill & Master** sekmesi (`FORUM/_skill_konu.py`).

| Kısaltma | Kaynak | Tarih |
|---|---|---|
| **SİTE** | sexyko.com/guide (oyun içi Rehber penceresinin kaynağı, sunucu Hyper) · canlı çekim `veri/site_gorev.json` + `veri/site_canavar.json` | 6 Eki 2026 |
| **REH** | `FORUM/rehber/` (forum.sexyko.com konuları + oyun ekranları + sitenin 3 Eki kopyası) | 3–4 Eki |
| **ADM** | `ADMIN_PANEL/VERI/sexyko_admin_veri_tam.json` (sexyko.com/admin, salt okuma) | 25 Eyl |
| **KOR** | korehberi.com (wiki 2nd job change + Kurian/Porutu sayfaları) · Steam KO master rehberi | genel KO |
| **TAN** | SexyKO'nun Ko-Yardım tanıtım konusu (11734) — `FORUM/SEXYKO_TANITIM_*.txt` | 30 Eyl |

---

## 1. Skill penceresi (K)

- **K** → Skill penceresi: Preset · Save Quickslot · Skill Point sekmeleri (REH `oyun/pencere/skill_K.png`, forum d/42).
- Her job'un 4 skill sekmesi (SİTE beginner-items, `rehber/web/beginner_items_sinif.json`):

| Job | Sekmeler |
|---|---|
| Warrior | Attack · Defence · Passion · Master |
| Rogue | Archery · Assassinate · Explore · Master (oyun penceresinde 3. sekme **Search** yazıyor → konuda "Search") |
| Mage | Fire · Ice · Lightning · Master |
| Priest | Heal · Aura · Spirit · Master |
| Kurian | Attack · Defence · Devil · Master |

- Hyper başlangıç: **Level 83 · 148 serbest skill puanı** (SİTE beginner-items). Kanıt 2: oyun görüntüsündeki Rogue → Archery 0 + Assassinate 80 + Search 48 + Master 20 = **148** (`skill_K.png`).
- **Master** sekmesi = 2. job (master) görevinden sonra açılan sekme (KOR: "2nd job change quest … unlock master skills").
- Skill Preset (puan dağılımı kaydet) + 4 Quick Slot → forum d/42 (konuya link olarak girdi).

## 2. 1. job değişimi

| Görev | Level | NPC | Yer | İstek | Ödül | Kaynak |
|---|---|---|---|---|---|---|
| 1st job change (#406) | 10+ | [Grand Merchant] Kaishan | Moradon **816,703** (ADM spawn, aktif) | 3.000 coin | Job change | SİTE /guide/quests/406 |

## 3. Master — 2. job değişimi (Level 60+)

Her job: **1 Unstable Kentaraus' Heart + job'a özel 2 Essence** → NPC'ye götür → Job change (SİTE /guide/quests/408-411, 781, 784; KOR + Steam aynı).

| Job | NPC | Karus (Luferson Castle haritası) | El Morad (El Morad Castle haritası) | 2. item | 3. item | Görev |
|---|---|---|---|---|---|---|
| Warrior | [Warrior Master] Skaki | 387,1741 | 1661,322 | Urkthron's Essence | Alkeradeua's Essence | 408 |
| Rogue | [Secret Agent] Clarence | 430,709 | 1632,1331 | GaruKonga's Essence | Trethonz's Essence | 409 |
| Mage | [Archmage] Drake | 1696,806 | 372,1226 | Colmicola's Essence | GaruKonga's Essence | 410 |
| Priest | [Priest] Minerva | 381,1744 | 1657,326 | Colmicola's Essence | Trethonz's Essence | 411 |
| Kurian (Karus) | [Grand Elder] Morbor | 405,1728 | — | Urkthron's Essence | Alkeradeua's Essence | 784 |
| Porutu (El Morad) | [Grand Elder] Atlas | — | 1650,331 | Urkthron's Essence | Alkeradeua's Essence | 781 |

- NPC koordinatları: ADM `list:npc-spawns` (Luferson Camp 1 / Elmorad Camp 1, hepsi `aktif:1`).
- **Kurian kanıtı:** SİTE Atlas/Morbor görevlerini "Warrior" etiketiyle gösteriyor (sitede 998 görevde **hiç "Kurian" etiketi yok**) ama Warrior'un kendi görevi Skaki'de (408). KOR: "Kurian'ın master NPC'si [Grand Elder] Morbor (Luferson Castle), Porutu'nun [Grand Elder] Atlas (El Morad Castle)". ADM: Morbor = Karus, Atlas = El Morad; katsayı tablosunda "Kurian (Master)" 115 / "Porutu (Master)" 215 var → **781/784 = Kurian/Porutu**.
- Item ID: Heart 810095000 · Urkthron 810090000 · Colmicola 810091000 · GaruKonga 810092000 · Trethonz 810093000 · Alkeradeua 810094000.

## 4. Master itemleri nereden düşer

| Item | Kim düşürür | Oran | Yer | Kaynak |
|---|---|---|---|---|
| Unstable Kentaraus' Heart | Centaur (Lv76) | **%50** | Karus: Luferson haritası sağ alt köşe (~1840-1926, 382-432) · El Morad: El Morad haritası sol üst (~111-244, 1628-1690) | SİTE /guide/monsters/2602 (drop) + 2657/2607 (spawn, "Centaur Foal") + ADM #2602 spawn aynı noktalar |
| Urkthron's Essence | [Field Boss] Urukthrone (Lv70) | **%100** | Karus 5 nokta · El Morad 5 nokta | SİTE 8656 / 8662 |
| Alkeradeua's Essence | [Field Boss] Alkedrada (Lv70) | **%100** | Karus 6 · El Morad 6 | SİTE 8657 / 8663 |
| GaruKonga's Essence | [Field Boss] Garukonga (Lv70) | **%100** | Karus 5 · El Morad 5 | SİTE 8653 / 8659 |
| Colmicola's Essence | ⚠ SexyKO'da drop kaydı YOK | — | KOR: [Field Boss] Kamicollo — SİTE 8655/8661 "Bu monsterın drop kaydı yok" (spawn var: Karus 5 · El Morad 5) | ⚠ Ç-S1 |
| Trethonz's Essence | ⚠ SexyKO'da drop kaydı YOK | — | KOR: [Field Boss] Trethorns — SİTE 8658/8664 "drop kaydı yok" (spawn var: Karus 5 · El Morad 5, Lv73) | ⚠ Ç-S1 |

- Spawn noktaları sitedeki harita yüzdesinden: oyun koordinatı = `x = left% × 20,48`, `z = (100 − top%) × 20,48` (Garukonga Karus 1130,1819 ve El Morad 4 noktası ADM ile birebir → eşleme doğrulandı).
- ADM drop tablolarında (`drops:detay`) bu görev itemleri **hiç yok** (boss tabloları "hiçbir yuva düşmüyor"); Centaur #2602'de sadece Potion of Wisdom %30 + Water of Grace %30 — SİTE aynı %30'ları + Heart %50'yi gösteriyor → site görev droplarını ayrıca ekliyor. Oyuncunun gördüğü = SİTE.

## 5. 70–80 skill görevleri (Master sekmesi)

Hepsi **Spell Stone Powder** ister, ödül **Skill ×1** (o seviyenin skill'i açılır). NPC = master NPC'si. (SİTE canlı 6 Eki, 23 görev)

| Job | NPC | 70 | 72 | 74 | 75 | 76 | 78 | 80 | **Toplam** |
|---|---|---|---|---|---|---|---|---|---|
| Warrior | Skaki | 5 | — | — | 10 | — | — | 15 | **30** |
| Rogue | Clarence | 5 | 7 | — | 10 | — | — | 15 | **37** |
| Mage | Drake | 5 | 7 | — | 10 | — | — | 15 | **37** |
| Priest | Minerva | 5 | 7 | 9 | 10 | 11 | 12 | 15 | **69** |
| Kurian / Porutu | Morbor / Atlas | — | — | — | 10 | — | — | 15 | **25** |

Görev no: W 336/510/511 · R 337/512/513/514 · M 338/515/516/517 · P 339/518/519/520/521/522/523 · K 785/786 (Morbor) · 782/783 (Atlas).

- TAN (SexyKO ekibinin resmi tanıtımı): "**Master kapalı, +70 Lv Skiller kapalı**" → master ve 70+ skiller görevle açılır.
- ⚠ ADM `game-settings → isSkillQuestRequired = 0` ("Skilleri açmak için görev yapılıp yapılmayacağını gösterir") → TAN ile çelişiyor (Ç-S2).

## 6. Spell Stone Powder (810369000) nereden

| Kaynak | Oran / adet | Yer | Kaynak |
|---|---|---|---|
| Hellfire · Enigma · Havoc · Cruel (Lv95) | **%10** (her biri) | Ronark Land, her biri 2 nokta | SİTE 8401-8404 (canlı 6 Eki) |
| Atross (Lv85) | %3 | Ronark Land 8 nokta | SİTE 1402 |
| Lyot (Lv78) | %3 | Ronark Land 8 nokta | SİTE 1311 (3 Eki'de %1,9'du → güncellenmiş) |
| Narki — **Eski aksesuarlar** havuzu | 1–5 adet (2 adet %40,4 · 1 %20,2 · 3 %20,2 · 4 %14,14 · 5 %4,04 · Forgotten Accessory Box %1,01) | Narki NPC'si | SİTE /guide/narki + ADM `ozel:narki-kirdirma` pool 4 (aynı) |
| Narki — **Aksesuarlar** havuzu | 1–5 adet (1 adet %33,2 · 2 %19,69 · 3 %11,2 · 4 %8,88 · 5 %3,8 · Forgotten Accessory Box %23,17) | Narki NPC'si | SİTE + ADM pool 5 (aynı) |

- Shozin'de bir tarif 20 Spell Stone Powder'ı malzeme olarak harcıyor (ADM `ozel:shozin-karisimi`) — konuya alınmadı.
- Rampage Orc (ADM #8809, Spell Stone %10) → ADM'de spawn kaydı yok, sitede yok → alınmadı.

## 7. Konuya ALINMAYANLAR (sebepli)

| Konu | Neden |
|---|---|
| 61 Lv skill scroll'ları: Warrior **Scream** (Skaki) · Rogue **Magic Shield** (Clarence) · Priest **Judgment** (Minerva) — 7 Certificate of Victory (900017000) | Görev metni: "National Defence Combat (Kalluga Valley üst kısmı) 7 zafer". Certificate'ın SexyKO'da kaynağı yok (SİTE etkinlik ödülleri + ADM hiçbir tabloda yok) → Ç-S3 |
| Nostrum of Magic / Stamp of Magic Power (SİTE #20, #21) | NPC/level/şart yok, sadece eski açıklama metni; gerçek 70-80 görevleri sadece Spell Stone istiyor |
| 70-80 skill adları | SİTE vermiyor (ödül "Skill ×1"); KOR sınıf sayfası eksik/tutarsız → uydurmadım |
| Master's teaching (810249000, PUS 732 KC, günlük ödül 18. gün) | Ne işe yaradığı hiçbir kaynakta yok |
| [Job Change] Biranda (Moradon 811,707) + PUS "Job Change Application Form" 250 SB | ADM spawn `aktif:0` → oyunda yok |
| GmrGame "Spell Stone +70 Skill Açma Rehberi" (25M coin) | Rakip sunucu (AGENTLAR/CURSOR/CALISMA) — SexyKO değil |

## 8. İpuçları (konuya girdi)

- **Job Changer** (forum d/28): iteme sağ tık → job seç, NPC gerekmez; önce üstündeki tüm itemleri çıkar.
- ADM duyuru 264/273 (SexyKO ekibi metni, şu an pasif): "Job Change değişiminde **skilleriniz sıfırlanır**, quest görevleri sıfırlanmaz."
- ADM `State_SkillReset = 1` (skill reset butonu açık) · `IsFreeRedistribute = 0` (skill/stat sıfırlama ücretli) — ücret bilinmiyor → konuya sadece "ücretli" diye bile girmedi.
- Ctrl + D (item üstünde) → item hangi moblardan düşüyor (forum d/50) → Colmicola/Trethonz için oyuncuya bu yol gösterildi.

## 9. Çelişkiler / açık sorular (patron · ekip)

| No | Konu | A | B | Konuda ne yaptım |
|---|---|---|---|---|
| **Ç-S1** | Colmicola's + Trethonz's Essence kaynağı | KOR: Kamicollo / Trethorns bossları düşürür | SİTE canlı: iki boss da "drop kaydı yok" · ADM: hiçbir tabloda yok | Konuda drop yeri yazmadım → "item üstünde Ctrl + D". **Rogue, Mage, Priest master'ı bu iki iteme bağlı** — ekip teyit etsin / drop eklesin |
| **Ç-S2** | 70+ skill görevi gerekli mi | TAN: "Master kapalı, +70 Lv Skiller kapalı" · SİTE: 23 skill görevi | ADM `isSkillQuestRequired = 0` (25 Eyl) | Konu TAN + SİTE'ye göre (görev gerekli). Ayar 0 kalırsa görevsiz açılır → ekip teyit |
| **Ç-S3** | 61 Lv scroll (Certificate of Victory) | SİTE görev var | Certificate kaynağı yok | Konuya almadım |
| Ç-S4 | Centaur spawn/drop ayrı ID | SİTE: drop #2602 (spawn yok), spawn #2607/#2657 "Centaur Foal" (drop yok) | ADM: #2602 aynı noktalarda spawn | Konuda "Centaur — %50" + harita noktası (iki ID aynı yer) |
| Ç-S5 | Başlangıç level'ı | SİTE Hyper: Level 83 | TAN/ADM: Level 1 | Konuda "Level 83'te 148 puan" (Hyper) + 1. job Lv10 adımı her ihtimale karşı |

### 9a. Denetim + patron kararları (6 Eki öğleden sonra)

Denetim (salt okuma): site 15:09'da yeniden çekildi → 29 görev + 19 canavar **fark 0** · NPC koordinatları sitenin görev haritası işaretleriyle ±4 · Spell Stone **oyunda doğrulandı** (Noisee `tur_kill`/OLAY: Enigma 42/300, Havoc 35/280, Cruel 38/328 = %11-14) · admin canlı: `isSkillQuestRequired = 0`, duyuru 264/273 pasif, başlangıç **5 job Level 83 / 302 stat** (25 Eyl'de Level 1'di → tanıtımdaki "1 Level" eskimiş) · admin canlı drop: **#2602 Centaur → Heart %50**, **#8653/#8659 Garukonga → GaruKonga's Essence %100** (25 Eyl'de ikisi de boştu).

Patron (6 Eki): "**1 gerekiyor 2 var 3 var** sexykoadmin panelinden bak rehberde sorun değil db de olmayabilir ama **4 kaybolur her şey sıfırlanır 5 yüzde yüz düşer**" + "her jobun kendi master skill açtığı NPC var, isimlerini bölgelerini yazarak".

| No | Karar | Konuya etkisi |
|---|---|---|
| Ç-S2 | 70+ skill görevi **gerekli** (admin ayarı 0 olsa da) | 70-80 bölümü kalır |
| Ç-S4 | Heart **var** (Centaur %50) | Centaur + harita kalır; kaynak admin canlı #2602 |
| Ç-S1 | Colmicola / Trethonz **var**, admin'den bakılacak | admin drop taraması → bulunan kaynak konuya |
| İpucu 4 | Job değişince **skillerin kaybolur, her şey sıfırlanır** (patron) | "görevler sıfırlanmaz" kısmı kaldırıldı |
| 5 | Field bosslar **%100** düşürür | S02 alt başlığı doğru |
| NPC | Her job'un master + skill NPC'si isim + bölge | yeni bölüm "📍 Master & Skill NPC'leri" |

## 10. Görseller (`skill_master/resim/`)

| ID | Dosya | Ne |
|---|---|---|
| S01 | S01_master_tablo.jpg | 6 job kartı: NPC + 3 item ikonu |
| S02 | S02_master_item.jpg | 6 master itemi: kim düşürür, oran |
| S03 | S03_harita_karus.jpg | Luferson Castle haritası: master NPC'leri + field bosslar + Centaur |
| S04 | S04_harita_elmorad.jpg | El Morad Castle haritası: aynısı |
| S05 | S05_skill_gorev.jpg | 70-80 skill görevleri × job, Spell Stone adedi + toplam |
| S06 | S06_spell_stone.jpg | Spell Stone Powder kaynakları (mob % + Narki) |
| S07 | S07_harita_ronark.jpg | Ronark Land: Spell Stone mobları |
| R07 | (yeni_konu R07) skill_K.png | Oyun içi Skill penceresi (K) |

Üretim: `python FORUM/_skill_gorsel.py` (Playwright, site ikonları + minimap'ler `rehber/web/resim/`) → `python FORUM/_skill_konu.py` → `python FORUM/_konu_kit.py`.
Veri tek yerde: `FORUM/_skill_veri.py` — import edilince tüm sayılar `veri/site_gorev.json` + `veri/site_canavar.json` (6 Eki canlı çekim) ile assert edilir; site değişirse önce bu iki dosyayı yeniden çek.

## 11. Konu çıktısı (6 Eki)

| Ne | Değer |
|---|---|
| Sekme | `HTML/FORUM_KONU.html` → **⚔️ Skill & Master** (önek `s`, linkler `localStorage skill_konu_url_v1`) |
| Başlık | 100 karakter |
| Bölüm | 9: yol haritası · K penceresi · 1. job · master (6 job) · master itemleri + 2 harita · 70-80 skill · Spell Stone + Ronark haritası · ipuçları · bağlantılar |
| BBCode | 12.613 karakter → 2 mesaj (7.991 + 4.620) · 11 [IMG] (8 yüklenecek: S01-S07 + R07 · 3 hazır: logo + 2 GIF) · 16 link |
| Dosyalar | `skill_master/SKILL_KONU_bbcode.txt` · `_markdown.md` · `_duz.txt` · `SKILL_KONU_uzun.jpg` (1038×9865) + `_parca_1-2.jpg` (≤7800 px) |
| Test | Playwright (scratchpad `test_skill.py`): JS hata 0 · 4 sekme açılıyor (eski 3 sağlam) · 11 resim yüklendi · beyaz zemin renk dönüşümü · S01 link yapıştır → BBCode'a girdi |

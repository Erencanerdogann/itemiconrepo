# -*- coding: utf-8 -*-
# FORUM_KONU.html ARAYUZ SOZLUGU TR -> EN (patron 13 Eki: "tr tiklicam eng tiklicam degisecek").
# Sadece ARAYUZ (butonlar, menu, aciklama satirlari, konu adlari). Konu ICERIGI (BBCode, onizleme, resim, kontrol) -> <konu>/konu_en.json.
# Kaynak: sayfadaki gorunen metin Playwright ile toplandi (13 Eki, 291 + 383 dugum; .onz / textarea / resim satiri / kontrol listesi HARIC).
# Kullanim: _dil.py bunu sayfaya gomer; tarayicida EN secilince: BLOK (ic HTML birebir) -> KURAL (kalip) -> METIN (metin dugumu) -> BASLIK (konu adi).

# --- 1) BLOK: guvenli blogun ic HTML'i (bosluklar tek) -> EN ic HTML (etiketler ayni)
BLOK = {
    '🔥 SexyKO Forum Kiti<small>49 konu · alanlara göre</small>': '🔥 SexyKO Forum Kit<small>49 topics · by area</small>',
    '<b>🖼 Resimler hazır linkli</b> — hepsi GitHub <code>itemiconrepo/forum/</code> deposunda, jsDelivr CDN\'den açılır; yükle-yapıştır yok. İstersen bir resmin kutusuna kendi linkini girersin (hazır linkin yerine geçer).':
        '<b>🖼 Images have ready links</b> — all in the GitHub <code>itemiconrepo/forum/</code> repo, served from the jsDelivr CDN; no upload-and-paste needed. If you want, enter your own link in an image box (it replaces the ready link).',
    '<b>BBCode kopyala</b> → forumda BBCode moduna yapıştır. Forum uzun mesajı kabul etmezse <b>1. mesaj</b> + <b>2. mesaj</b> olarak böl (bölüm çizgisinden ikiye ayrılır).':
        '<b>Copy BBCode</b> → paste in the forum\'s BBCode mode. If the forum rejects a long post, split it into <b>Post 1</b> + <b>Post 2</b> (split at a section line).',
    'forum.sexyko.com (Flarum) → üstte <b>Forum türü: Flarum</b> seç → <b>BBCode kopyala</b> (renkli, doğru boyut) · istersen <b>Markdown kopyala</b> (renksiz).':
        'forum.sexyko.com (Flarum) → at the top select <b>Forum type: Flarum</b> → <b>Copy BBCode</b> (colored, correct size) · or <b>Copy Markdown</b> (no colors).',
    'İçerik: <b>sadece oyunun ve forumun bilgisi</b> (oyun içi rehber = sexyko.com/guide, forum.sexyko.com rehber konuları, oyun içi ekranlar · 4 Eki). Kaynakların çeliştiği bilgiler konuya alınmadı → <b>⚠ Kontrol</b>.':
        'Contents: <b>only information from the game and the forum</b> (in-game guide = sexyko.com/guide, forum.sexyko.com guide topics, in-game screens · 4 Oct). Information where sources conflict was left out → <b>⚠ Check</b>.',
    'Uzun konunun <b>24 bölümü aynen</b>; her bölümde <b>küçük bir resim</b>, tek satır ve <b>rehber / forum linkleri</b>. Resme tıklayınca bölümün ilk linki açılır.':
        'The <b>same 24 sections</b> as the long topic; each section has <b>a small image</b>, one line and <b>guide / forum links</b>. Clicking the image opens the section\'s first link.',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/yeni_konu/kisa/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/yeni_konu/kisa/resim/</code>, jsDelivr) — no upload needed.',
    '<b>BBCode kopyala</b> → forumda BBCode moduna yapıştır; uzun gelirse <b>1. mesaj</b> + <b>2. mesaj</b>. forum.sexyko.com (Flarum) → üstte <b>Forum türü: Flarum</b> seç → <b>BBCode kopyala</b> (renkli, doğru boyut) · istersen <b>Markdown kopyala</b> (renksiz).':
        '<b>Copy BBCode</b> → paste in the forum\'s BBCode mode; if too long, use <b>Post 1</b> + <b>Post 2</b>. forum.sexyko.com (Flarum) → at the top select <b>Forum type: Flarum</b> → <b>Copy BBCode</b> (colored, correct size) · or <b>Copy Markdown</b> (no colors).',
    'Job job master + skill NPC\'leri (isim, bölge, harita), master görevi ve itemleri, 70 – 80 skill görevleri, Spell Stone Powder + Narki — <b>6 job</b> (Warrior, Rogue, Mage, Priest, Kurian, Porutu).':
        'Master + skill NPCs per job (name, zone, map), master quest and items, 70 – 80 skill quests, Spell Stone Powder + Narki — <b>6 jobs</b> (Warrior, Rogue, Mage, Priest, Kurian, Porutu).',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/skill_master/resim/</code>, jsDelivr) — yükleme yok. R07 uzun konudaki skill penceresiyle aynı.':
        '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/skill_master/resim/</code>, jsDelivr) — no upload needed. R07 is the same as the skill window in the long topic.',
    'Bilgi: oyun içi rehber (sexyko.com/guide, <b>6 Eki canlı</b>) + admin + korehberi. Patron kararları (6 Eki) işlendi → <b>⚠ Kontrol</b> (ekip notu: Colmicola / Trethonz drop\'u admin drop tablosunda tanımlı değil, konuda patron bilgisiyle %100).':
        'Info: in-game guide (sexyko.com/guide, <b>live on 6 Oct</b>) + admin + korehberi. Owner decisions (6 Oct) applied → <b>⚠ Check</b> (team note: the Colmicola / Trethonz drop is not defined in the admin drop table; the topic says 100% per the owner).',
    '4 Beta CSW (takvim, saat, ödüller, ödül kuralı) · Clan sıralaması · Job sıralaması (30 cm heykel) · 100.000+ NP çekilişi · 23 Ekim Official — <b>resimli</b> (6 görsel).':
        '4 Beta CSWs (schedule, time, rewards, reward rule) · Clan ranking · Job ranking (30 cm statue) · 100,000+ NP raffle · 23 October Official — <b>with images</b> (6 visuals).',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/odul/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/odul/resim_en/</code>, jsDelivr) — no upload needed.',
    'Bilgi: <b>forum.sexyko.com/d/54</b> (SexyKO, 5 Eki) — her tarih / tutar birebir, kaynakta olmayan bilgi yok → <b>⚠ Kontrol</b> (Job 4. sırası kaynakta yok).':
        'Info: <b>forum.sexyko.com/d/54</b> (SexyKO, 5 Oct) + team reward table (12 Oct) — every date / amount identical, nothing added that is not in the source → <b>⚠ Check</b> (Job 4th place not in the source).',
    'Sezon nedir · 2026 – 2027 takvimi (8 sezon: açılış, turnuva kaydı, birleşim, oran) · bir sezonun akışı · kademeli oranlar %100 → %800 · turnuva · GB alımı — <b>resimli</b> (5 görsel).':
        'What a season is · 2026 – 2027 schedule (8 seasons: opening, tournament registration, merge, rate) · how a season flows · tiered rates 100% → 800% · tournament · GB purchase — <b>with images</b> (5 visuals).',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/sezon/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/sezon/resim/</code>, jsDelivr) — no upload needed.',
    '<b>BBCode kopyala</b> → forumda BBCode moduna yapıştır; uzun gelirse <b>1. mesaj</b> + <b>2. mesaj</b>. forum.sexyko.com (Flarum) → üstte <b>Forum türü: Flarum</b> seç → <b>BBCode kopyala</b>.':
        '<b>Copy BBCode</b> → paste in the forum\'s BBCode mode; if too long, use <b>Post 1</b> + <b>Post 2</b>. forum.sexyko.com (Flarum) → at the top select <b>Forum type: Flarum</b> → <b>Copy BBCode</b>.',
    'Bilgi: <b>patronun sezon tablosu</b> (8 sezon) + <b>forum.sexyko.com/d/57</b> açıklamaları — tarihler iki kaynakta birebir → <b>⚠ Kontrol</b> (GB alımı zamanı çelişkisi, d/57\'de kalan yapay zekâ notu).':
        'Info: <b>the owner\'s season table</b> (8 seasons) + <b>forum.sexyko.com/d/57</b> descriptions — dates identical in both sources → <b>⚠ Check</b> (conflict on GB purchase timing, an AI note left in d/57).',
    '24 saatte ne çıktı (Golden 1.601 / Normal 508 item) · iki envanter item item · karşılaştırma grafiği · resmî oranlar (Normal / Golden / Platinum) — <b>resimli</b> (5 görsel).':
        'What dropped in 24 hours (Golden 1,601 / Normal 508 items) · both inventories item by item · comparison chart · official rates (Normal / Golden / Platinum) — <b>with images</b> (5 visuals).',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/mining/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/mining/resim/</code>, jsDelivr) — no upload needed.',
    'forum.sexyko.com (Flarum) → üstte <b>Forum türü: Flarum</b> (varsayılan) → <b>BBCode kopyala</b> → yeni konuya yapıştır.':
        'forum.sexyko.com (Flarum) → at the top <b>Forum type: Flarum</b> (default) → <b>Copy BBCode</b> → paste into a new topic.',
    'Bilgi: <b>Semih\'in 24 saatlik envanter görüntüsü</b> (ikonlar eşlendi, gözle doğrulandı) + oyun içi rehber oranları (7 Eki canlı = admin) → <b>⚠ Kontrol</b> (test koşulları bilinmiyor).':
        'Info: <b>Semih\'s 24-hour inventory screenshot</b> (icons matched, checked by eye) + in-game guide rates (live on 7 Oct = admin) → <b>⚠ Check</b> (test conditions unknown).',
    'Hızlı panel (Başlat / Durdur / kalan süre / Ayarlar) · Main: 8+8+8 skill, HP/MP pot, mob listesi, Party/Self heal, Attack range · Misc · skill bar kilidi · 8 adımda kurulum — <b>resimli</b> (8 görsel, oyunun kendi Genie penceresi).':
        'Quick panel (Start / Stop / time left / Settings) · Main: 8+8+8 skills, HP/MP potions, mob list, Party/Self heal, Attack range · Misc · skill bar lock · setup in 8 steps — <b>with images</b> (8 visuals, the game\'s own Genie window).',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/genie/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/genie/resim/</code>, jsDelivr) — no upload needed.',
    'Bilgi: <b>forum.sexyko.com/d/16</b> (SexyKO) — her cümle kaynakta birebir; gönderinin 4 resmi 404 → oyun ekranı (3 Eki) → <b>⚠ Kontrol</b>.':
        'Info: <b>forum.sexyko.com/d/16</b> (SexyKO) — every sentence identical to the source; the post\'s 4 images were 404 → game screen (3 Oct) → <b>⚠ Check</b>.',
    'Yayıncılar bölümü · canlı yayıncı takibi · destek · başvuru (kurallar + form + 7 adım) · Sponsor Yayıncı şartları — <b>resimli</b>.':
        'Streamers section · live streamer tracking · support · application (rules + form + 7 steps) · Sponsor Streamer requirements — <b>with images</b>.',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/yayinci/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/yayinci/resim/</code>, jsDelivr) — no upload needed.',
    'Bilgi: <b>forum.sexyko.com/d/37</b> (SexyKO) — her cümle / şart kaynakta birebir → <b>⚠ Kontrol</b>.': 'Info: <b>forum.sexyko.com/d/37</b> (SexyKO) — every sentence / requirement identical to the source → <b>⚠ Check</b>.',
    'Kupon nedir · nasıl kullanılır (Kupon → CHECK) · tekli item · Basket · VIP / Farm paketi istisnası · Sponsor Yayıncı kodları · etkinlikte %30\'a varan — <b>resimli</b>.':
        'What a coupon is · how to use it (Coupon → CHECK) · single item · Basket · VIP / Farm package exception · Sponsor Streamer codes · up to 30% during events — <b>with images</b>.',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/pus_kupon/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/pus_kupon/resim/</code>, jsDelivr) — no upload needed.',
    'Bilgi: <b>forum.sexyko.com/d/51</b> (SexyKO) — her cümle kaynakta birebir → <b>⚠ Kontrol</b>.': 'Info: <b>forum.sexyko.com/d/51</b> (SexyKO) — every sentence identical to the source → <b>⚠ Check</b>.',
    'Ücretsiz TeamSpeak — bir bakışta · 3 adım (panel → sunucu bilgileri + KEY → KEY ile ilk giriş) · clanını topla — <b>resimli</b> (5 görsel, gönderinin kendi ekran görüntüleriyle).':
        'Free TeamSpeak — at a glance · 3 steps (panel → server details + KEY → first login with KEY) · gather your clan — <b>with images</b> (5 visuals, with the post\'s own screenshots).',
    '<b>🖼 Resimler hazır linkli</b> (itemiconrepo <code>forum/teamspeak/resim/</code>, jsDelivr) — yükleme yok.': '<b>🖼 Images have ready links</b> (itemiconrepo <code>forum/teamspeak/resim/</code>, jsDelivr) — no upload needed.',
    'Bilgi: <b>forum.sexyko.com/d/55</b> (SexyKO, 5 Eki) — her cümle kaynakta birebir; form alanları (64 slot, clanadi.ts.sexyko.com) ekran görüntüsünden → <b>⚠ Kontrol</b>.':
        'Info: <b>forum.sexyko.com/d/55</b> (SexyKO, 5 Oct) — every sentence identical to the source; form fields (64 slots, clanname.ts.sexyko.com) from the screenshot → <b>⚠ Check</b>.',
    '✏️ <b>Burada düzenleyebilirsin</b> — otomatik kaydedilir; BBCode kopyala / mesaj parçaları / önizleme / görünüm düzenlenmiş hali kullanır.':
        '✏️ <b>You can edit it here</b> — saved automatically; Copy BBCode / post parts / preview / rendered view use the edited version.',
    'Forumda <b>Yeni konu</b> aç → aşağıdaki <b>Başlığı kopyala</b>.':'On the forum, open a <b>New topic</b> → <b>Copy title</b> below.',
    '<b>XenForo / vBulletin / MyBB</b> (Kocuce, Ko-Yardım, FrmTR, Turkmmo, vSRO …): editörde <b>BBCode moduna</b> geç (genelde <code>[ ]</code> veya "Kaynak" düğmesi) → <b>BBCode kopyala</b> → yapıştır. Editör BBCode moduna geçmiyorsa → <b>Görünümü kopyala</b> → normal editöre yapıştır.':
        '<b>XenForo / vBulletin / MyBB</b> (Kocuce, Ko-Yardım, FrmTR, Turkmmo, vSRO …): switch the editor to <b>BBCode mode</b> (usually the <code>[ ]</code> or "Source" button) → <b>Copy BBCode</b> → paste. If the editor has no BBCode mode → <b>Copy rendered view</b> → paste into the normal editor.',
    'Resimler BBCode\'da <b>link olarak</b> geliyor (GitHub itemiconrepo → jsDelivr CDN; her forumda açılır). Bir forum dış resmi engellerse → <b>Resimler</b> sekmesinden indir → forumun kendi "resim yükle" düğmesiyle aynı yere koy.':
        'Images come in the BBCode <b>as links</b> (GitHub itemiconrepo → jsDelivr CDN; they open on every forum). If a forum blocks external images → download them from the <b>Images</b> tab → upload them in the same place with the forum\'s own "upload image" button.',
    'Konuyu açınca <b>Forumlar</b> sekmesinde o forumu ✔ işaretle (bu tarayıcıda hatırlanır).': 'After posting, tick ✔ that forum in the <b>Forums</b> tab (remembered in this browser).',
    'Linkler hazır: GitHub <code>itemiconrepo/forum/resim/</code> → jsDelivr · bilgisayarda <code>C:\\temp\\Sexyko\\FORUM\\resim\\</code> · ⚠ 7 MB\'lık GIF\'ler bazı forumların yükleme sınırını aşabilir — o forumda GIF\'i link olarak bırak.':
        'Links ready: GitHub <code>itemiconrepo/forum/resim/</code> → jsDelivr · on this PC <code>C:\\temp\\Sexyko\\FORUM\\resim\\</code> · ⚠ the 7 MB GIFs may exceed some forums\' upload limit — leave the GIF as a link on that forum.',
}

# --- 2) KURAL: kalipli metin (38 forum konusu satirlari, sayaclar). (regex, js-yerine-koyma) — hem blok ic HTML'ine hem metin dugumune uygulanir.
KURAL = [
    (r"^<b>🖼 Resimler</b> forumdaki linkleriyle \((\d+)\)(.*)$", "<b>🖼 Images</b> with their forum links ($1)$2"),
    (r"— <b>⚠ (\d+) kırık resim çıkarıldı</b>\.$", "— <b>⚠ $1 broken image(s) removed</b>."),
    (r"^forum\.sexyko\.com/d/(\d+) → <b>Düzenle</b> → <b>BBCode kopyala</b> → yapıştır\. Eski hali: <b>📜 Forumdaki hali</b>\.$",
     "forum.sexyko.com/d/$1 → <b>Edit</b> → <b>Copy BBCode</b> → paste. Original version: <b>📜 Forum original</b>."),
    (r"^Bilgi: <b>forum\.sexyko\.com/d/(\d+)</b> · (.+?) · açılış (\S+) · (\d+) mesaj → <b>⚠ Kontrol</b>\.$",
     "Info: <b>forum.sexyko.com/d/$1</b> · $2 · opened $3 · $4 post(s) → <b>⚠ Check</b>."),
    (r"^BBCode <b>([\d.]+)</b> karakter · (\d+) mesaja bölünür \(her biri ≤ ([\d.]+)\) · yüklemen gereken resim linki (<span class=\"say\">.*?</span>)( · forum resimleri hazır link)?$",
     "BBCode <b>$1</b> characters · split into $2 post(s) (each ≤ $3) · image links you need to upload $4$5"),
    (r" · forum resimleri hazır link$", " · forum images: ready links"),
    (r"^<b>Bizim temayla yeniden inşa</b> — <b>(\d+) görsel kart</b> · (\d+) bölüm \((.*)\) · metin ve resimler konunun kendisi\.$",
     "<b>Rebuilt with our theme</b> — <b>$1 visual card(s)</b> · $2 sections · text and images are from the topic itself."),   # 13 Eki: ($3) TR bolum listesi EN'de cikti
    (r"^(\d+)\. mesaj( \(([\d.]+)\))?$", "Post $1$2"),
    (r"^(\d+) karakter$", "$1 characters"),
    (r"^✔ kopyalandı: (.*)$", "✔ copied: $1"),
    (r"^kopyalanamadı — metin kutusundan Ctrl\+A, Ctrl\+C$", "could not copy — use Ctrl+A, Ctrl+C in the text box"),
    (r"^kopyalanamadı$", "could not copy"),
    (r"^(\d+) görsel kart$", "$1 visual card(s)"),
    (r"^\((\d+)/(\d+) link\)$", "($1/$2 links)"),
    (r"^📜 (.+) — forum\.sexyko\.com/d/(\d+)$", "📜 {T:$1} — forum.sexyko.com/d/$2"),       # {T:...} = BASLIK tablosundan
]

# --- 3) METIN: tek metin dugumu / attribute (trim'li birebir)
METIN = {
    "🌙 Koyu": "🌙 Dark", "☀️ Beyaz": "☀️ Light", "Forum zemini:": "Forum background:", "Forum türü:": "Forum type:", "Varsayılan": "Default",
    "Yapıştıracağın forumun mesaj zemini hangisiyse onu seç — BBCode renkleri ve önizleme ona göre değişir.":
        "Pick the post background of the forum you will paste into — BBCode colors and the preview adapt to it.",
    "(forum.sexyko.com). Flarum'da BBCode yazı boyutu": "(forum.sexyko.com). On Flarum the BBCode text size is in",
    "piksel": "pixels",
    "— XenForo / vBulletin forumuna yapıştıracaksan önce onu seç (yoksa yazılar dev gelir). Seçim bütün sekmelerin BBCode'una uygulanır.":
        "— if you will paste into a XenForo / vBulletin forum, select it first (otherwise the text comes out huge). The choice applies to the BBCode of every tab.",
    "Flarum — forum.sexyko.com": "Flarum — forum.sexyko.com",
    "📜 Forumdaki konular — bizim temayla yeniden (38 konu · ⚠ = eski halinde küçük yazı / kırık resim vardı)":
        "📜 Forum topics — rebuilt with our theme (38 topics · ⚠ = the original had tiny text / broken images)",
    "☰ Konular": "☰ Topics", "◀ Önceki": "◀ Previous", "Sonraki ▶": "Next ▶",
    "Başlık": "Title", "Başlığı kopyala": "Copy title", "BBCode kopyala": "Copy BBCode", "Görünümü kopyala": "Copy rendered view",
    "Görünümü kopyala (editöre yapıştır)": "Copy rendered view (paste into editor)", "Markdown kopyala": "Copy Markdown", "Düz metin kopyala": "Copy plain text",
    "Düz metin": "Plain text", "Düzenle": "Edit", "👁 Önizleme": "👁 Preview", "🖼 Resimler": "🖼 Images", "Resimler": "Images", "⚠ Kontrol": "⚠ Check",
    "↺ Orijinale dön": "↺ Back to original", "📜 Forumdaki hali": "📜 Forum original", "İndir": "Download", "Link": "Link", "Yer": "Place",
    "Not (REKLAM listesinden)": "Note (from the ad list)", "Tanıtım sitesi": "Promo site", "Forum": "Forum", "Forumlar": "Forums", "📋 Forumlar": "📋 Forums",
    "Nasıl kullanılır": "How to use", "İçerik:": "Contents:", "Bilgi:": "Info:", "✔ hazır link": "✔ ready link", "büyük dosya": "large file",
    "Burada düzenleyebilirsin": "You can edit it here", "Bilgi uzun konudan alındı, yeni bilgi yok. ⚠ Kontrol sekmesinde notlar.":
        "Information taken from the long topic, nothing new. ⚠ Notes in the Check tab.",
    "Ko-Yardım tanıtım konusu": "Ko-Yardım promo topic", "· aynı konuyu başka forumlarda açmak için hazır metin + resimler": "· ready text + images to open the same topic on other forums",
    "📋 Kısa konu: SexyKO Oyun Rehberi (özet)": "📋 Short topic: SexyKO Game Guide (summary)", "📝 Yeni konu: SexyKO Oyun Rehberi": "📝 New topic: SexyKO Game Guide",
    "⚔️ Skill & Master konusu (tüm joblar)": "⚔️ Skill & Master topic (all jobs)",
    "🏆 Hyper Beta Ödülleri konusu (forum.sexyko.com/d/54)": "🏆 Hyper Beta Rewards topic (forum.sexyko.com/d/54)",
    "⚔️ Sezon Sistemi (Academy) konusu — 8 sezon": "⚔️ Season System (Academy) topic — 8 seasons",
    "⛏️ 24 Saatlik Madencilik Sonuçları — Golden Mattock vs Normal Mattock": "⛏️ 24-Hour Mining Results — Golden Mattock vs Normal Mattock",
    "⚙️ Genie Sistemi konusu (forum.sexyko.com/d/16 — yeniden, resimler oyundan)": "⚙️ Genie System topic (forum.sexyko.com/d/16 — remade, images from the game)",
    "🎥 Yayıncı Sistemi & Sponsor Yayıncı Başvurusu konusu (forum.sexyko.com/d/37)": "🎥 Streamer System & Sponsor Streamer Application topic (forum.sexyko.com/d/37)",
    "🎟️ PUS İndirim Kodu Sistemi konusu (forum.sexyko.com/d/51)": "🎟️ PUS Discount Code System topic (forum.sexyko.com/d/51)",
    "🎙️ Ücretsiz TeamSpeak konusu (forum.sexyko.com/d/55)": "🎙️ Free TeamSpeak topic (forum.sexyko.com/d/55)",
    "isteğe bağlı: kendi yüklediğin link (hazır linkin yerine geçer)": "optional: your own uploaded link (replaces the ready link)",
    "yüklediğin resmin linkini yapıştır (…jpg / …png)": "paste the link of your uploaded image (…jpg / …png)",
    "🔍 Konu ara (başlık veya içerik)…": "🔍 Search topics (title or content)…",
    "(renksiz).": "(no colors).", "link olarak": "as a link", "resimli": "with images",
    # alanlar (sol menu)
    "📣 Tanıtım konuları": "📣 Promo topics", "📣 Tanıtım konuları ›": "📣 Promo topics ›", "🔥 Yeni Sunucu HYPER": "🔥 New Server HYPER",
    "🎮 Oyun Rehberi · Oyun Sistemleri": "🎮 Game Guide · Game Systems", "⚔️ Oyun Rehberi · Karakter & Skill": "⚔️ Game Guide · Character & Skill",
    "🛡️ Oyun Rehberi · Item & Upgrade": "🛡️ Game Guide · Item & Upgrade", "🛒 Oyun Rehberi · Mağaza & Destek": "🛒 Game Guide · Store & Support",
    "📢 Duyurular": "📢 Announcements", "🛠️ Destek & Client": "🛠️ Support & Client", "💬 Genel / Topluluk": "💬 General / Community",
    "🔥 SexyKO — Forum Konu Kiti": "🔥 SexyKO — Forum Topic Kit",
    "forumda aç ↗": "open on forum ↗",
}
for _k in [k for k in METIN if k.startswith(("📣", "🔥", "🎮", "⚔️", "🛡️", "🛒", "📢", "🛠️", "💬")) and not k.endswith("›")]:     # ust yol satiri: "<alan> ›"
    METIN.setdefault(_k + " ›", METIN[_k] + " ›")

# --- 4) BASLIK: konu adi (menu / sekme / h2). Emoji on-eki ve sondaki " ⚠" korunur; BUYUK harfli forum basliklari da (BUYUK alani).
BASLIK = {
    "Yeni konu: Oyun Rehberi": "New topic: Game Guide", "Kısa konu: Rehber özeti": "Short topic: Guide summary", "Tanıtım konusu (Ko-Yardım)": "Promo topic (Ko-Yardım)",
    "Hyper Beta Ödülleri": "Hyper Beta Rewards", "Sezon Sistemi (Academy)": "Season System (Academy)", "Başlangıç Paketi İçeriği": "Starter Pack Contents",
    "Genie Sistemi": "Genie System", "F10 Oyun Ayarları": "F10 Game Settings", "Rehber Sistemi": "Guide System", "Kum Saati Sistemi": "Hourglass System",
    "Slot Teleport Sistemi": "Slot Teleport System", "Auto Mining — Mining Inn Sistemi": "Auto Mining — Mining Inn System", "Party Sistemi Yenilendi!": "Party System Renewed!",
    "Daily Quest Sistemi": "Daily Quest System", "Çarkıfelek Sistemi": "Wheel of Fortune System", "Draki's Tower Sistemi": "Draki's Tower System",
    "Clan Grade Sistemi": "Clan Grade System", "Skill Preset & Quick Slot Sistemi": "Skill Preset & Quick Slot System", "Karakter Rebirth Sistemi": "Character Rebirth System",
    "Job Changer Kullanımı": "Using the Job Changer", "Equipment View Sistemi": "Equipment View System", "NCS — Nick Değiştirme Sistemi": "NCS — Nickname Change System",
    "Make Over Coupon Sistemi": "Make Over Coupon System", "Tag Name Sistemi": "Tag Name System", "Upgrade Oranları Sistemi": "Upgrade Rates System",
    "Kırdırma Sistemi Detayları": "Item Exchange System Details", "Chaotic Generator & Toplu Kırdırma Sistemi": "Chaotic Generator & Bulk Exchange System",
    "Old Takı Dönüşüm Sistemi": "Old Accessory Conversion System", "Solo Cape Sistemi": "Solo Cape System", "Solo Pelerin Sistemi": "Solo Cloak System",
    "Royal Pelerin Bonusları": "Royal Cape Bonuses", "Drop Info Sistemi": "Drop Info System", "Drop Search Sistemi": "Drop Search System",
    "Destek Talebi Sistemi": "Support Ticket System", "Yeni Client Yayınlandı!": "New Client Released!", "Ücretsiz TeamSpeak": "Free TeamSpeak",
    "24 Saat Madencilik": "24-Hour Mining", "Aktif Etkinlik Listesi": "Active Event List", "Sponsor Yayıncı Materyalleri": "Sponsor Streamer Materials",
    "Yayıncı Sistemi": "Streamer System", "PUS İndirim Kodu": "PUS Discount Code", "64-Bit Client | Hata & Bug Bildirim Konusu": "64-Bit Client | Error & Bug Report Topic",
    "Kendini/Clanını Tanıt": "Introduce Yourself / Your Clan", "Küfür ediyorlar. Bunun bir cezası yok mu.": "People are swearing. Is there no penalty for this?",
}
# forumdaki BUYUK harfli orijinal basliklar (h2 "📜 ... — forum.sexyko.com/d/N")
BUYUK = {
    "64-BIT CLIENT | HATA & BUG BİLDİRİM KONUSU": "64-BIT CLIENT | ERROR & BUG REPORT TOPIC", "🔥 SEXYKO'DA KIRDIRMA SİSTEMİ DETAYLARI": "🔥 SEXYKO ITEM EXCHANGE SYSTEM DETAILS",
    "🔥 SEXYKO PARTY SİSTEMİ YENİLENDİ!": "🔥 SEXYKO PARTY SYSTEM RENEWED!", "⚙️ SEXYKO F10 OYUN AYARLARI": "⚙️ SEXYKO F10 GAME SETTINGS",
    "🎫 SEXYKO DESTEK TALEBİ SİSTEMİ": "🎫 SEXYKO SUPPORT TICKET SYSTEM", "📽️SEXYKO SPONSOR YAYINCI MATERYALLERİ": "📽️SEXYKO SPONSOR STREAMER MATERIALS",
    "📘 SEXYKO REHBER SİSTEMİ": "📘 SEXYKO GUIDE SYSTEM", "⛏️ SEXYKO AUTO MINING — MINING INN SİSTEMİ": "⛏️ SEXYKO AUTO MINING — MINING INN SYSTEM",
    "🎮 SEXYKO AKTİF ETKİNLİK LİSTESİ": "🎮 SEXYKO ACTIVE EVENT LIST", "🔨 SEXYKO UPGRADE ORANLARI SİSTEMİ": "🔨 SEXYKO UPGRADE RATES SYSTEM",
    "🔄 SEXYKO JOB CHANGER KULLANIMI": "🔄 USING THE SEXYKO JOB CHANGER", "🦸 SEXYKO SOLO CAPE SİSTEMİ": "🦸 SEXYKO SOLO CAPE SYSTEM",
    "🏷️ SEXYKO TAG NAME SİSTEMİ": "🏷️ SEXYKO TAG NAME SYSTEM", "💇 SEXYKO MAKE OVER COUPON SİSTEMİ": "💇 SEXYKO MAKE OVER COUPON SYSTEM",
    "🪪 SEXYKO NCS — NICK DEĞİŞTİRME SİSTEMİ": "🪪 SEXYKO NCS — NICKNAME CHANGE SYSTEM", "📅 SEXYKO DAILY QUEST SİSTEMİ": "📅 SEXYKO DAILY QUEST SYSTEM",
    "🎯 SEXYKO DROP INFO SİSTEMİ": "🎯 SEXYKO DROP INFO SYSTEM", "💬 KENDINI/CLANINI TANIT": "💬 INTRODUCE YOURSELF / YOUR CLAN",
    "⚔️ SEXYKO CLAN GRADE SİSTEMİ": "⚔️ SEXYKO CLAN GRADE SYSTEM", "⏳ SEXYKO KUM SAATİ SİSTEMİ": "⏳ SEXYKO HOURGLASS SYSTEM",
    "👑 SEXYKO ROYAL PELERİN BONUSLARI": "👑 SEXYKO ROYAL CAPE BONUSES", "💍 SEXYKO OLD TAKI DÖNÜŞÜM SİSTEMİ": "💍 SEXYKO OLD ACCESSORY CONVERSION SYSTEM",
    "🎡 SEXYKO ÇARKIFELEK SİSTEMİ": "🎡 SEXYKO WHEEL OF FORTUNE SYSTEM", "⚔️ SEXYKO SKILL PRESET & QUICK SLOT SİSTEMİ": "⚔️ SEXYKO SKILL PRESET & QUICK SLOT SYSTEM",
    "♻️ SEXYKO CHAOTIC GENERATOR & TOPLU KIRDIRMA SİSTEMİ": "♻️ SEXYKO CHAOTIC GENERATOR & BULK EXCHANGE SYSTEM", "🦸 SEXYKO SOLO PELERİN SİSTEMİ": "🦸 SEXYKO SOLO CLOAK SYSTEM",
    "🐉 SEXYKO DRAKI'S TOWER SİSTEMİ": "🐉 SEXYKO DRAKI'S TOWER SYSTEM", "👁️ SEXYKO EQUIPMENT VIEW SİSTEMİ": "👁️ SEXYKO EQUIPMENT VIEW SYSTEM",
    "⭐ SEXYKO KARAKTER REBIRTH SİSTEMİ": "⭐ SEXYKO CHARACTER REBIRTH SYSTEM", "🔎 SEXYKO DROP SEARCH SİSTEMİ": "🔎 SEXYKO DROP SEARCH SYSTEM",
    "🌀 SEXYKO SLOT TELEPORT SİSTEMİ": "🌀 SEXYKO SLOT TELEPORT SYSTEM", "🎁 BAŞLANGIÇ PAKETİ İÇERİĞİ": "🎁 STARTER PACK CONTENTS",
    "🛒 SEXYKO POWER UP STORE": "🛒 SEXYKO POWER UP STORE", "⚔️ FARM GRIND TRACKER": "⚔️ FARM GRIND TRACKER", "Küfür ediyorlar. Bunun bir cezası yok mu.": "People are swearing. Is there no penalty for this?",
    "Yeni Client Yayınlandı!": "New Client Released!",
}
UI_EN = {"cevrilmedi": "🇹🇷 This topic is not translated yet — the Turkish content is shown.", "dil_tr": "TR", "dil_en": "EN", "title": "Forum Topic Kit"}

if __name__ == "__main__":
    import re
    for k, v in {**BLOK, **METIN, **BASLIK, **BUYUK}.items():
        assert not re.search(r"[çğıöşüÇĞİÖŞÜ]", re.sub(r"Ko-Yardım|Kaynak|clanname", "", v)), (k, v)     # EN tarafinda Turkce harf (ozel adlar haric) yok
    print("sozluk OK · blok", len(BLOK), "· kural", len(KURAL), "· metin", len(METIN), "· baslik", len(BASLIK), "· buyuk", len(BUYUK))

# -*- coding: utf-8 -*-
# TANITIM KONUSU — DUZENLI BBCode (patron 4 Eki: "en bastaki haline donuyoruz, hic degismemis halini, sadece duzen getir, bir sey ekleme cikartma",
# "color ayarla, basliklari yazi metinlerini boyutlandir, cervevele"). Kaynak = Ko-Yardim 11734 ilk mesaj (_konu_kit.py BB, canli ile birebir olculdu 4 Eki).
# Sadece: renk + boyut + cerceve ([TABLE] — Ko-Yardim BB yardim sayfasinda var, kenarlikli). Metin / resim / link AYNI: kodlar silinince harfi harfine esit (assert).
import re, html

# renkler = KOYU set (yeni/kisa konu ile ortak). Beyaz zeminli forum icin FORUM_KONU.html "Forum zemini: Beyaz" dugmesi
# ayni renkleri beyaz karsiliklarina cevirir (patron 4 Eki secenek A) — kontrast olculdu: koyu set koyu zeminde >=4.0, beyaz set beyazda >=4.4
ALTIN, KIRMIZI, VURGU, LINK, CIZGI_RENK = "#c8a253", "#d14841", "#e6c46a", "#4fa3ff", "#d4a017"
ALT_CIZGI = "━━━━━━━━━━━━━━━━━━━━"
PX = {1: 9, 2: 10, 3: 12, 4: 15, 5: 18, 6: 22, 7: 26}
CIZGI = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


def duzenle(bb, genislik=None):
    # genislik: {resim url: '520px'} — orijinal konudaki gosterim genisligi (kit RESIM sw), ayni kalsin
    genislik = genislik or {}
    imgs = re.findall(r"\[IMG\](.*?)\[/IMG\]", bb)
    urls = re.findall(r"\[URL=([^\]]+)\]", bb)
    def I(p):
        x = [u for u in imgs if p in u]; assert len(x) == 1, (p, x)
        w = genislik.get(x[0])
        return (f'[IMG width="{w}"]' if w else "[IMG]") + f"{x[0]}[/IMG]"
    def U(p, metin, kalin=True):
        x = sorted({u for u in urls if u.endswith(p) or p in u}, key=len); assert x, p
        t = f"[B][COLOR={LINK}]{metin}[/COLOR][/B]" if kalin else f"[COLOR={LINK}]{metin}[/COLOR]"
        return f"[URL={x[0]}]{t}[/URL]"
    bas = lambda t, r=ALTIN, s=6: f"[SIZE={s}][B][COLOR={r}]{t}[/COLOR][/B][/SIZE]"
    alt = lambda t: f"[SIZE=5][B][COLOR={ALTIN}]{t}[/COLOR][/B][/SIZE]"
    govde = lambda *s: "[SIZE=4]" + "\n".join(s) + "[/SIZE]"
    # kutu: baslik + altinda renkli kisa cizgi + icerik
    cerceve = lambda bs, *s: ("[TABLE][TR][TD][CENTER]\n" + bs + f"\n[COLOR={CIZGI_RENK}]{ALT_CIZGI}[/COLOR]\n\n" + "\n\n".join(s)
                              + "\n[/CENTER][/TD][/TR][/TABLE]")
    cizgi = f"[CENTER][SIZE=5][COLOR={CIZGI_RENK}]{CIZGI}[/COLOR][/SIZE][/CENTER]"
    # govde + kalin kelimeler vurgu renginde (link olmayan satirlar)
    gv = lambda *s: govde(*[re.sub(r"\[B\](.*?)\[/B\]", lambda m: f"[B][COLOR={VURGU}]{m.group(1)}[/COLOR][/B]", x) for x in s])
    sis = lambda e, ad, d: f"{e} [B]{ad}[/B] ➜ " + U(f"/d/{d}", "Detaylı Bilgi")

    o = [
        "[CENTER]\n" + I("hazir-ol") + "\n\n" + I("logo_big") + "\n\n" + bas("2010'DAN BERİ 16 YILLIK EFSANE!", s=5) + "\n\n" +
        f"[SIZE=6][B][I][U][COLOR={ALTIN}]Eşsiz ve Gerçek v2 64-Bit Client[/COLOR][/U][/I][/B][/SIZE]" + "\n\n" +
        I("stonesoft") + "\n[SIZE=4][B]StoneSoft\nAltyapı ve Anti-Cheat Koruması[/B][/SIZE]\n[/CENTER]",
        cizgi,
        cerceve(bas("🔥 ALIŞILMIŞIN DIŞINDA BİR DENEYİME HAZIR OLUN!"), I("sexyko-hyper"),
                gv("Bildiğiniz tüm [B]64-Bit Clientleri[/B],", "[B]Light Farm DB'leri[/B] ve klasikleşmiş [B]Event sistemlerini[/B] bir kenara bırakın!", "",
                      "Çünkü bu kez sıradan bir başlangıç yapmıyoruz.", "",
                      "Ezberleri bozuyor, sınırları yeniden çiziyor ve [B]Knight Online deneyimini yepyeni bir boyuta[/B] taşıyoruz!", "",
                      "Bu sadece yeni bir server değil…", "",
                      "Bu, yılların tecrübesiyle şekillenen, teknolojinin gücüyle yeniden doğan ve rekabetin merkezine yerleşmeye hazırlanan [B]yeni bir dönem![/B]"),
                bas("🔥 SEXYKO GERİ DÖNÜYOR!", KIRMIZI)),
        cizgi,
        cerceve(bas("📌 SUNUCU BİLGİLERİ"),
                gv("[B]⚔️ Sürüm:[/B] [I]v.2 Light Farm[/I]", "[B]⚔️ Level Cap:[/B] [I]83 / Rebirth 5[/I]",
                      "[B]⚔️ Multiclient:[/B] [I]2 | IP Limiti: 8[/I]", "[B]⚔️ Upgrade:[/B] [I]+8 | Takı: +1[/I]"),
                bas("BAŞLANGIÇ", KIRMIZI),
                govde("[B]⚔️ 1 Level,", "⚔️ Master kapalı,", "⚔️ +70 Lv Skiller kapalı,", "⚔️ Chitin Armor, Chitin Shell",
                      "⚔️ High Class Weapons, Exp Weapons, Unique Weapons", "⚔️ Karakter Rebirth 5[/B]")),
        cizgi,
        cerceve(bas("🎁 BAŞLANGIÇ PAKETİ BİZDEN!"),
                govde("Karakterinizi oluşturduğunuzda seçtiğiniz Job'a uygun başlangıç ekipmanı hazır olarak gelir.",
                      "Oyuna hızla adapte olun, ilk günden gelişiminize başlayın.", "",
                      "[B]Paket İçeriği ve Başlangıç İtemleri: ➜[/B] " + U("/d/53", "Detaylı Bilgi"))),
        cizgi,
        cerceve(bas("🏆 ÖDÜL HAVUZU"), govde("Beta ödül tablosu ve ödül havuzunun tüm detayları resmi forumumuzda yayınlanmıştır:"),
                "[SIZE=5]" + U("hyper-sunucusu-d-l-havuzu", "HYPER Sunucusu Ödül Havuzu") + "[/SIZE]"),
        cizgi,
        "[CENTER]" + I("takvimleri") + "[/CENTER]",
        cerceve(bas("🔥 NEDEN SEXYKO?"),
                gv("✅ [B]16 yıllık tecrübe:[/B] 2010'dan beri kesintisiz hizmet",
                      "✅ [B]Eşsiz Gerçek v2 64-Bit Client:[/B] Daha hızlı, daha stabil oyun deneyimi",
                      "✅ [B]Hilesiz oyun:[/B] StoneSoft Anti-Cheat System ile korumalı altyapı",
                      "✅ [B]Hazır başlangıç:[/B] Job'una özel ekipman, premium, pot ve 24 saatlik Genie",
                      "✅ [B]NPC'ye son:[/B] Kırdırma, nick/job/ırk değişimi, make over ve daha fazlası sağ tıkla yapılır",
                      "✅ [B]Gelişmiş Genie:[/B] 8 attack + 8 self + 8 party skill slotu, pot yüzdesi, mob listesi",
                      "✅ [B]Oyun içi rehber, drop arama ve upgrade oranları:[/B] Şeffaf sistem, sürpriz yok",
                      "✅ [B]Rebirth, Draki's Tower, günlük görevler:[/B] 83'ten sonra da gelişim devam eder",
                      "✅ [B]Solo pelerin:[/B] Clansız da pelerin bonusu, 20+ seçenek ve efekt",
                      "✅ [B]Sponsor yayıncı indirim kodları:[/B] PUS alışverişinde %30'a varan kampanyalar")),
        cizgi,
        cerceve(bas("📅 ETKİNLİKLER"), gv("Oyun içi [B]Kum Saati[/B] sistemi ile etkinlikleri takip edebilir, 5 dakika kala bildirim kurabilirsiniz.")),
        cizgi,
        cerceve(bas("🎮 OYUN SİSTEMLERİ"),
                gv("SexyKO'nun oyuncuya zaman kazandıran sistemlerini aşağıdan inceleyebilirsiniz.",
                      "Merak ettiğiniz sistemin yanındaki [B]Detaylı Bilgi[/B] bağlantısına tıklayın, resimli anlatımıyla doğrudan konuya gidin.")),
        cerceve(alt("📘 REHBER & ARAYÜZ"),
                govde(*[sis(*x) for x in [("📘", "Rehber Sistemi", 22), ("⚙️", "F10 Oyun Ayarları", 12), ("⏳", "Kum Saati Sistemi", 38),
                                          ("🎯", "Drop Info Sistemi", 34), ("🔎", "Drop Search Sistemi", 50), ("👁️", "Equipment View Sistemi", 46),
                                          ("👥", "Party Sistemi", 11), ("📊", "Farm Grind Tracker", 14), ("⚔️", "Skill Preset & Quick Slot Sistemi", 42)]])),
        cerceve(alt("🤖 FARM & OTOMASYON"),
                govde(*[sis(*x) for x in [("🤖", "Gelişmiş Genie Sistemi", 16), ("🌀", "Slot Teleport Sistemi", 52), ("⛏️", "Auto Mining & Mining Inn Sistemi", 24),
                                          ("🖱️", "Sağ Tık ile Kırdırma Sistemi", 10), ("♻️", "Chaotic Generator & Toplu Kırdırma Sistemi", 43),
                                          ("📅", "Daily Quest Sistemi", 33), ("⭐", "Karakter Rebirth Sistemi", 49), ("🐉", "Draki's Tower Sistemi", 45),
                                          ("🔨", "Upgrade Oranları Sistemi", 26), ("💍", "Old Takı Dönüşüm Sistemi", 40)]])),
        cerceve(alt("👑 CLAN Sistemi"),
                govde(*[sis(*x) for x in [("⚔️", "Clan Grade Sistemi", 36), ("👑", "Royal Pelerin Bonusları", 39)]])),
        cerceve(alt("🛒 Power Up Store ve Yeni Ürünler"),
                govde(*[sis(*x) for x in [("🛒", "Power Up Store", 27), ("🎟️", "PUS İndirim Kodu Sistemi", 51), ("🦸", "Solo Pelerin Sistemi", 44),
                                          ("🦸", "Solo Cape Sistemi", 29), ("🏷️", "Tag Name Sistemi", 30), ("💇", "Make Over Coupon Sistemi", 31),
                                          ("🪪", "NCS — Nick Değiştirme Sistemi", 32), ("🔄", "Job Changer Kullanımı", 28), ("🎡", "Çarkıfelek Sistemi", 41)]])),
        cerceve(alt("🎫 DESTEK Sistemi"), govde(sis("🎫", "Destek Talebi Sistemi", 13))),
        cizgi,
        cerceve(alt("Sistem Gereksinimleri:"),
                gv("[B]Minimum:[/B] Intel Core i3-4130 / Ryzen 3 1200 • GTX 750 Ti • 4 GB RAM • Windows 10 (64-bit)",
                      "[B]Önerilen:[/B] Core i5-8400 / Ryzen 5 2600 • GTX 1060 6 GB • 8 GB+ RAM • SSD • Windows 11 (64-bit)")),
        cizgi,
        cerceve(bas("🔗 BAĞLANTILAR"),
                govde("🌐 Web Sitesi: " + U("https://sexyko.com", "sexyko.com"), "💬 Forum: " + U("https://forum.sexyko.com", "forum.sexyko.com"),
                      "📥 Client İndir: " + U("/download", "sexyko.com/download"),
                      "📘 Oyun Rehberi: " + U("/t/sexyko-oyun-rehberi", "forum.sexyko.com/t/sexyko-oyun-rehberi"), "",
                      "[B]📢 Tüm sistemlerin listesi:[/B] " + U("/t/sexyko-oyun-rehberi", "SexyKO Oyun Rehberi"))),
        "[CENTER][SIZE=5][B]Discord ve Sosyal Medya hesaplarımızı takip etmeyi unutma![/B][/SIZE]\n\n" + bas("🔥 SEXYKO — PVP'NİN BAŞLADIĞI YER 🔥", KIRMIZI) + "[/CENTER]",
    ]
    yeni = "\n\n".join(o)
    dogrula(bb, yeni)
    return yeni


def duz_metin(s):
    s = re.sub(r"\[/?(?:B|I|U|CENTER|LEFT|RIGHT|TABLE|TR|TD|SIZE|COLOR|URL|IMG)(?:[= ][^\]]*)?\]", "", s, flags=re.I)
    return re.sub(r"[\s━]+", "", s)   # ━ = sus cizgisi (bicim), metin sayilmaz


def dogrula(eski, yeni):
    a, b = duz_metin(eski), duz_metin(yeni)
    if a != b:
        i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
        raise AssertionError(f"METIN FARKLI @ {i}: eski …{a[max(0, i - 40):i + 40]}… / yeni …{b[max(0, i - 40):i + 40]}…")
    for t in ("IMG", "URL"):
        rx = r"\[IMG[^\]]*\](.*?)\[/IMG\]" if t == "IMG" else r"\[URL=([^\]]+)\]"
        assert re.findall(rx, eski) == re.findall(rx, yeni), f"{t} listesi farkli"
    for a1, z1 in [("[B]", "[/B]"), ("[I]", "[/I]"), ("[U]", "[/U]"), ("[CENTER]", "[/CENTER]"), ("[SIZE=", "[/SIZE]"), ("[COLOR=", "[/COLOR]"),
                   ("[URL=", "[/URL]"), ("[TABLE]", "[/TABLE]"), ("[TD]", "[/TD]")]:
        assert yeni.count(a1) == yeni.count(z1), a1


def onizleme(bb):
    """Ko-Yardim (XenForo) gorunumune yakin HTML — sadece bu dosyanin kullandigi kodlar."""
    h = html.escape(bb, quote=False)
    h = re.sub(r'\[IMG(?: width="([^"]+)")?\](.*?)\[/IMG\]', lambda m: f'<img src="{m.group(2)}" alt="" style="max-width:100%;width:{m.group(1) or "auto"}">', h)
    h = re.sub(r"\[URL=([^\]]+)\]", r'<a href="\1" target="_blank" rel="noopener">', h).replace("[/URL]", "</a>")
    h = re.sub(r"\[SIZE=(\d)\]", lambda m: f'<span style="font-size:{PX[int(m.group(1))]}px">', h).replace("[/SIZE]", "</span>")
    h = re.sub(r"\[COLOR=([^\]]+)\]", r'<span style="color:\1">', h).replace("[/COLOR]", "</span>")
    for k, t in [("B", "b"), ("I", "i"), ("U", "u")]:
        h = h.replace(f"[{k}]", f"<{t}>").replace(f"[/{k}]", f"</{t}>")
    h = h.replace("[TABLE][TR][TD]", '<table style="width:100%;border-collapse:collapse;margin:6px 0"><tr><td style="border:1px solid #d8d8d8;padding:3px">')
    h = h.replace("[/TD][/TR][/TABLE]", "</td></tr></table>")
    h = h.replace("[CENTER]", '<div style="text-align:center">').replace("[/CENTER]", "</div>")
    h = re.sub(r"\n?(<table|</table>|<div[^>]*>|</div>)\n?", r"\1", h)
    # zemin rengi sayfadaki secimden gelir (body.zemin-beyaz) — burada sabit zemin yok
    return ('<div style="padding:14px;font-family:Inter,\'Segoe UI\',Arial,sans-serif;font-size:15px;line-height:1.55">'
            + h.replace("\n", "<br>") + "</div>")

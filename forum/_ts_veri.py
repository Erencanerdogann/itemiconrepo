# -*- coding: utf-8 -*-
# UCRETSIZ TEAMSPEAK KONUSU — VERI (patron 8 Eki: "yeni forum konulari geliyor, yeniden yapacagiz resimli vs ayni janradan devam" ·
# "hepsini tek tek konuya dok guzelce, resimleri repoya atmayi unutma, pushlamayi unutma").
# KAYNAK: teamspeak/kaynak_d55.txt (forum.sexyko.com/d/55, Flarum API, 8 Eki) — ASAGIDAKI HER METIN KAYNAKTA BIREBIR VAR (import'ta assert).
# Ekran goruntuleri: ayni gonderinin 3 resmi (teamspeak/kaynak_resim/ts_1..3.png). FORM alanlari METINDE YOK, ts_2.png'de gorunuyor (kaynak: resim).
import os

KOK = os.path.dirname(os.path.abspath(__file__))
TD = os.path.join(KOK, "teamspeak")
KAYNAK = open(os.path.join(TD, "kaynak_d55.txt"), encoding="utf-8").read()
KONU_URL = "https://forum.sexyko.com/d/55"
RESIM = {n: os.path.join(TD, "kaynak_resim", f"ts_{n}.png") for n in (1, 2, 3)}   # 1 panel menusu · 2 olusturma formu · 3 TeamSpeak 3 istemcisi

GIRIS = "SexyKO olarak oyuncularımızın clan içi iletişimini daha hızlı, stabil ve kolay hale getirmek için Ücretsiz TeamSpeak sistemini aktif ettik."
GIRIS2 = "Artık ekstra ücret ödemeden, düşük pingli kendi TeamSpeak alanınızı oluşturabilir ve clanınızla birlikte kullanmaya başlayabilirsiniz."
ADIM = [("1. ADIM — PANELDEN TEAMSPEAK BÖLÜMÜNE GİRİN", "SexyKO panelinize giriş yaptıktan sonra üst menüde bulunan TeamSpeak bölümüne tıklayın."),
        ("2. ADIM — SUNUCU BİLGİLERİNİZİ OLUŞTURUN", "Açılan ekranda sizden istenen bilgileri doldurun."),
        ("3. ADIM — KEY İLE İLK GİRİŞİNİZİ TAMAMLAYIN", "Oluşturulan KEY’i TeamSpeak sunucunuza ilk giriş yaptığınızda ilgili alana girmeniz yeterlidir.")]
ADIM2_L = ["Sunucu adınızı belirleyin.", "Size özel TeamSpeak adresinizi oluşturun.", "Gerekli bilgileri eksiksiz şekilde doldurun."]
ADIM2_S = "Bilgileri tamamladıktan sonra TeamSpeak sunucunuzu oluşturabilirsiniz."
KEY = ["İşlem tamamlandığında sistem tarafından size özel bir KEY oluşturulacaktır.", "Bu KEY’i mutlaka kaydedin."]
TAMAM = ["İşlem tamamlandı!", "Artık clanınızla birlikte düşük pingli TeamSpeak hizmetinizi tamamen ücretsiz şekilde kullanmaya başlayabilirsiniz."]
CLAN_BAS = "CLANINI TOPLA, İLETİŞİMİNİ KUR!"
CLAN = "PK, farm, event ve Castle Siege War gibi takım iletişiminin önemli olduğu tüm alanlarda clanınızla çok daha hızlı ve düzenli organize olun."
CLAN_ALAN = ["PK", "farm", "event", "Castle Siege War"]
YATIRIM = ["SexyKO olarak yalnızca oyun içi sistemlere değil, oyuncularımızın ihtiyaç duyduğu tüm alanlara yatırım yapmaya devam ediyoruz.", "İhtiyaç duyulan sistemleri hayata geçiriyoruz."]
SLOGAN = ["İlklerin Sunucusu SexyKO", "Daha kaliteli oyun.", "Daha güçlü topluluk."]
SON = "PVP’nin Geçmişi Değil, Başlangıcı."
LINK = ["www.sexyko.com", "discord.gg/sexyko"]

# --- ts_2.png (olusturma formu) ve ts_3.png'de GORUNEN bilgiler (metinde yok — resimden; KONTROL'de not)
SURUM = "TeamSpeak 3"
FORM = [("SUNUCU ADI", "Örn. SexyKO Clan Sunucusu"), ("KAPASİTE (SLOT SAYISI)", "64 slot"), ("ALT ALAN ADI (TSDNS)", "clanadi.ts.sexyko.com")]
FORM_NOT = "Küçük harf, rakam ve tire kullanılabilir."
FORM_DUGME = "OLUŞTURMAK İÇİN GİRİŞ YAP"

# ---------- dogrulama: her metin kaynakta birebir
for s in [GIRIS, GIRIS2, ADIM2_S, CLAN, SON, *[a for _, a in ADIM], *[b for b, _ in ADIM], *ADIM2_L, *KEY, *TAMAM, *YATIRIM, *SLOGAN, *LINK, CLAN_BAS]:
    assert s in KAYNAK, s
for p in RESIM.values(): assert os.path.exists(p), p

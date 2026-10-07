# -*- coding: utf-8 -*-
# YAYINCI SISTEMI & SPONSOR YAYINCI BASVURUSU KONUSU — VERI (patron 8 Eki: "yeni forum konulari ... resimli vs ayni janradan devam" ·
# "hepsini tek tek konuya dok guzelce, resimleri repoya atmayi unutma, pushlamayi unutma"). Kaynak: forum.sexyko.com/d/37.
# KAYNAK: yayinci/kaynak_d37.txt (Flarum API, 8 Eki) — ASAGIDAKI HER METIN KAYNAKTA BIREBIR VAR (import'ta assert).
# Ekran goruntuleri: gonderinin 4 resminden 3'u (yy_2..4.png); 1. resim (SPONSOR.png bannerı) kaynakta da 404 -> kullanilmadi.
# KAYNAK KUSURLARI (KONTROL'de): Mikrofon maddesinin son cumlesi yarim ("...etkilesim saglam") -> konuya ALINMADI; SexyKO Icerigi maddesinde nokta eksik -> sadece noktalama.
import os

KOK = os.path.dirname(os.path.abspath(__file__))
YD = os.path.join(KOK, "yayinci")
KAYNAK = open(os.path.join(YD, "kaynak_d37.txt"), encoding="utf-8").read()
KONU_URL = "https://forum.sexyko.com/d/37"
RESIM = {n: os.path.join(YD, "kaynak_resim", f"yy_{n}.png") for n in (2, 3, 4)}   # 2 menu · 3 Yayincilar sayfasi · 4 basvuru formu + sartlar

GIRIS = ["SexyKO web panelinde bulunan Yayıncılar Sistemi sayesinde aktif yayıncıları takip edebilir, hangi sponsor yayıncının yayında olduğunu görebilir, yayıncılara destek olabilir ve aynı bölüm üzerinden yayıncı başvurusu yapabilirsiniz.",
         "Tüm işlemler tek panel üzerinden kolayca yönetilir."]
B01 = ("01 — YAYINCILAR BÖLÜMÜNE GİRİŞ", "SexyKO hesabınıza giriş yaptıktan sonra panel üzerinden Yayıncılar bölümüne giriş yapın.", "Bu bölüm, SexyKO yayıncı sisteminin ana merkezidir.")
B01_L = ["aktif yayıncıları görebilir,", "sponsor yayıncıları takip edebilir,", "yayın durumlarını kontrol edebilir,", "yayıncı başvuru ekranına ulaşabilirsiniz."]
B02 = ("02 — YAYINDA OLAN YAYINCILARI TAKİP EDİN", "Yayıncılar sayfasında SexyKO içerikleri üreten yayıncıları tek ekranda görüntüleyebilirsiniz.",
       "Yayında olan yayıncıların yayınlarına doğrudan ulaşabilir ve SexyKO yayıncılarına destek olabilirsiniz.")
B02_L = ["yayında olduğunu,", "sponsor yayıncı olup olmadığını,", "yayın kanalını,", "güncel yayın durumunu"]
DESTEK = ("YAYINCILARA DESTEK OLUN", ["SexyKO yayıncı sistemi yalnızca yayıncıları listelemek için değil, topluluğun yayıncılarla daha kolay buluşabilmesi için hazırlanmıştır.",
                                     "Beğendiğiniz yayıncıyı takip edebilir, yayınına katılabilir ve yayıncıya destek olabilirsiniz.",
                                     "Bu sayede hem SexyKO topluluğunun büyümesine hem de içerik üreticilerimizin daha fazla oyuncuya ulaşmasına katkı sağlayabilirsiniz."])
B03 = ("03 — YAYINCI BAŞVURUSU YAPIN", "Siz de SexyKO için yayın yapmak ve yayıncı sistemine dahil olmak istiyorsanız aynı panel üzerinden Yayıncı Başvurusu yapabilirsiniz.")
B04 = ("04 — BAŞVURU KURALLARINI OKUYUN", ["Başvuru ekranını açtığınızda sağ tarafta Yayıncı Başvuru Kuralları yer almaktadır.",
                                          "Başvurunuzu göndermeden önce bu kuralları dikkatlice okumanız önemlidir.",
                                          "Kurallar; yayıncı programına katılım şartlarını, yayın düzenini ve yayıncıların uyması gereken temel koşulları açıklar.",
                                          "Başvuru gönderen oyuncular kuralları kabul etmiş sayılır."])
FORM = ("BAŞVURU FORMUNU DOLDURUN", "Başvuru sırasında sizden istenen bilgileri eksiksiz ve doğru şekilde doldurun.", "Yayın kanalınızın aktif ve erişilebilir olduğundan emin olun.")
FORM_L = ["Karakter / Nick bilgisi", "E-posta adresi", "Discord ID", "Yayın kanalınızın linki", "Takipçi / izleyici bilgileri", "Kendiniz ve yayınlarınız hakkında kısa açıklama"]
NASIL = ["SexyKO hesabınıza giriş yapın.", "Panelden Yayıncılar bölümüne girin.", "Aktif ve sponsor yayıncıları inceleyin.", "Yayıncı Başvurusu Yap seçeneğine tıklayın.",
         "Sağ taraftaki başvuru kurallarını okuyun.", "Başvuru formunu eksiksiz doldurun.", "Başvurunuzu gönderin."]
NASIL_SON = "Başvurunuz yönetim ekibi tarafından incelendikten sonra uygun bulunması halinde yayıncı sistemine dahil edilirsiniz."
DIKKAT = ("BAŞVURU YAPARKEN DİKKAT", "Başvuru formunda verdiğiniz bilgilerin doğru olması değerlendirme sürecini kolaylaştırır.",
          "Bu nedenle başvurunuzu göndermeden önce bilgilerinizi mutlaka kontrol edin.")
DIKKAT_L = ["yanlış kanal bağlantısı,", "eksik Discord bilgisi,", "ulaşılamayan yayın hesabı,", "eksik başvuru bilgileri"]
# --- Sponsor Yayinci Basvuru Sartlari: (emoji, baslik, metin, kart_ozeti) — metin kaynakta birebir (kusurlu 2 madde asagida duzeltilir)
SART = [
 ("🎙️", "SexyKO Sponsor Yayıncı Programı", "SexyKO Sponsor Yayıncı Programı; düzenli, kaliteli ve aktif yayın yapan yayıncılarla uzun vadeli iş birliği oluşturmak amacıyla hazırlanmıştır. Başvurular kanal kalitesi, izleyici kitlesi, yayın geçmişi ve aktiflik durumuna göre değerlendirilir. Sınırlı kontenjan uygulanmaktadır.", "sınırlı kontenjan"),
 ("📊", "Takipçi ve İzlenme", "Başvuru yapacak yayıncının Youtube veya Kick platformunda en az 250 takipçisi bulunmalıdır. Bunun yanında düzenli yayın geçmişi ve gerçek izleyici kitlesi aranır. Takipçi sayısının yanı sıra ortalama izleyici, yayın etkileşimi ve kanal aktifliği de değerlendirmeye alınır.", "en az 250 takipçi"),
 ("⚔️", "SexyKO İçeriği", "Yayınların ana odağı SexyKO olmalıdır. Sponsor yayıncıların düzenli olarak SexyKO üzerinde yayın yapması, sunucunun oyun yapısını ve sistemlerini izleyicilerine aktarması beklenmektedir Yayınlarda PK, farm, etkinlikler, rekabet, karakter gelişimi, item geliştirme ve SexyKO'ya özel sistemler.", "ana odak SexyKO"),
 ("🛡️", "Temiz Yayın Geçmişi", "Başvuru sahibinin yayın geçmişinde platform yasağı, hile kullanımı, dolandırıcılık, ciddi topluluk ihlalleri veya sunucu kurallarını kötüye kullanma gibi durumlar bulunmamalıdır. SexyKO yönetimi gerekli gördüğü durumlarda geçmiş yayınları ve kanal geçmişini inceleme hakkına sahiptir.", "yasak / hile / ihlal yok"),
 ("📢", "Yayında SexyKO Tanıtımı", "Sponsor yayıncıların yayın başlığında SexyKO'ya yer vermesi ve yayın sırasında sunucunun tanıtımını aktif şekilde yapması beklenir. Yayın açıklaması/panel alanlarında SexyKO bağlantılarının kullanılması ve gerekli görülen sponsor görsellerinin yayın içerisinde bulundurulması zorunludur.", "başlıkta SexyKO · bağlantı"),
 ("🎤", "Mikrofon Kullanımı — ZORUNLU", "Sponsor yayıncı programına kabul edilen tüm yayıncıların yayın sırasında aktif mikrofon kullanması zorunludur. Mikrofonsuz yayın yapan kanallar sponsor yayıncı programına kabul edilmez.", "mikrofon zorunlu"),
 ("💰", "Kameralı / Kamerasız Yayıncı", "Sponsor yayıncı ödemeleri yayın formatına ve performansa göre farklılık gösterebilir. Kameralı ve kamerasız yayıncılar için farklı ödeme paketleri uygulanacaktır. Kamera kullanımı, yayın kalitesi, aktiflik ve performans kriterleri ödeme değerlendirmesinde dikkate alınır.", "farklı ödeme paketi"),
 ("🎁", "Sponsor Yayıncı VIP Destek Paketi", "Sponsor yayıncılarımıza yayın başlangıcında 7 günlük VIP Destek Paketi hediye edilir ve sponsorluğun devam ettiği her hafta yenilenir. Partner yayıncılarımıza ise 30 günlük VIP Destek Paketi tanımlanır. Paketler Orjin VIP'ye göre daha kısıtlı olup yalnızca oyun içi destek amacıyla verilir.", "7 gün VIP · partner 30 gün"),
 ("⏱️", "Haftalık Yayın Süresi", "Sponsor yayıncıların haftalık en az 20 saat yayın yapması zorunludur. Yayın süreleri düzenli olarak kontrol edilir ve belirlenen sürenin altında kalan yayıncıların sponsorluğu ve VIP yenilemesi değerlendirmeye alınır.", "haftada en az 20 saat"),
 ("💬", "Aktif Yayın ve Etkileşim", "Yayıncıların yayın boyunca aktif olması, izleyicileriyle iletişim kurması ve SexyKO hakkında bilgi vermesi beklenir. AFK, sessiz veya izleyici etkileşimi olmayan yayınlar sponsor kapsamında değerlendirilmez.", "AFK / sessiz yayın yok"),
]
SART_BAS = "Sponsor Yayıncı Başvuru Şartları"
SLOGAN = "Yayıncıları takip et • Canlı yayınları keşfet • Destek ol • Kendi başvurunu yap"
SON = "SexyKO içerik üreticileriyle topluluğun buluştuğu tek merkez."
# --- ekran goruntusunden (metinde yok): form alanlari + kanal notu
EKRAN_FORM = ["Nick", "E-mail", "Discord ID", "Takipçi sayısı", "Yayın kanalı linki", "Kısa tanıtım / özet"]
EKRAN_KANAL = "Twitch, Kick veya YouTube kanalının tam adresi."

# ---------- dogrulama
for s in [*GIRIS, *B01, *B01_L, *B02, *B02_L, DESTEK[0], *DESTEK[1], *B03, B04[0], *B04[1], *FORM, *FORM_L, *NASIL, NASIL_SON, *DIKKAT, *DIKKAT_L,
          SART_BAS, SLOGAN, SON, *[b for _, b, _, _ in SART]]:
    assert s in KAYNAK, s
for _, b, m, _ in SART: assert m in KAYNAK, b                      # mikrofon: kaynaktaki metnin TAM cumleleri (yarim son cumle haric) -> alt dizi
assert "etkileşim sağlam\n" in KAYNAK                               # kusur hala kaynakta (ekip duzeltirse burasi patlar -> metni guncelle)
SART = [(i, b, m.replace("beklenmektedir Yayınlarda PK", "beklenmektedir. Yayınlarda: PK"), k) for i, b, m, k in SART]   # sadece noktalama
for p in RESIM.values(): assert os.path.exists(p), p

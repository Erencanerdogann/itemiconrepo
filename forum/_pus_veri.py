# -*- coding: utf-8 -*-
# PUS INDIRIM KODU SISTEMI KONUSU — VERI (patron 8 Eki: "yeni forum konulari ... resimli vs ayni janradan devam" ·
# "hepsini tek tek konuya dok guzelce, resimleri repoya atmayi unutma, pushlamayi unutma"). Kaynak: forum.sexyko.com/d/51.
# KAYNAK: pus_kupon/kaynak_d51.txt (Flarum API, 8 Eki) — ASAGIDAKI HER METIN KAYNAKTA BIREBIR VAR (import'ta assert).
# Ekran goruntuleri: ayni gonderinin 3 resmi (pus_kupon/kaynak_resim/pus_1..3.png). ORNEK rakamlar (Sexyko10, -10%, 950 -> 855 SB) RESIMDEN — ornek, kod iddiasi yok.
import os

KOK = os.path.dirname(os.path.abspath(__file__))
PD = os.path.join(KOK, "pus_kupon")
KAYNAK = open(os.path.join(PD, "kaynak_d51.txt"), encoding="utf-8").read()
KONU_URL = "https://forum.sexyko.com/d/51"
RESIM = {n: os.path.join(PD, "kaynak_resim", f"pus_{n}.png") for n in (1, 2, 3)}   # 1 PUS penceresi + sepet + kupon · 2 tekli alim onayi · 3 sepet

GIRIS = ["SexyKO olarak Power Up Store sistemine çok özel ve farklı bir özellik ekledik:",
         "Bu sistem sayesinde artık PUS alışverişlerinizde Sponsor Yayıncıların indirim kodlarını kullanabilir ve alışverişlerinizi daha avantajlı şekilde tamamlayabilirsiniz.",
         "Bu özellik, SexyKO ve StoneSoft altyapısında PUS sistemine doğrudan entegre edilmiş özel bir yapıdır.",
         "Oyuncular hem alışverişlerinde indirim kazanır, hem de desteklediği Sponsor Yayıncıya katkı sağlar."]
NASIL_BAS = "İNDİRİM KODU NASIL KULLANILIR?"
NASIL = ["Power Up Store'un alt bölümünde bulunan Kupon alanına kullanmak istediğiniz indirim kodunu yazmanız yeterlidir.",
         "Kod geçerliyse indirim otomatik olarak aktif edilir.", "Böylece alışverişinizi indirimli fiyat üzerinden tamamlayabilirsiniz."]
TEKLI_BAS = "TEKLİ ITEM ALIMLARINDA KUPON"
TEKLI = ["İndirim kodları yalnızca sepet alışverişlerinde değil, uygun olan tekli PUS ürünlerinde de kullanılabilir.",
         "Ürünü satın alırken geçerli bir kupon kodunuz varsa indirim doğrudan alışverişe uygulanır.",
         "Yani tek bir ürün alırken bile Sponsor Yayıncı indirim kodundan yararlanabilirsiniz."]
SEPET_BAS = "BASKET / SEPET ALIŞVERİŞLERİNDE KUPON"
SEPET = ["PUS üzerinde birden fazla ürünü Basket içerisine eklediğinizde de kupon sistemini kullanabilirsiniz.",
         "Sepette bulunan uygun ürünlere indirim uygulanır ve toplam alışveriş tutarınız buna göre yeniden hesaplanır.",
         "Bu sayede toplu PUS alışverişlerinde de kupon avantajından faydalanabilirsiniz."]
PAKET_BAS = "ÖNEMLİ — VIP VE FARM PAKETLERİ"
PAKET = ["VIP Paketlerde kullanılamaz", "Farm Paketlerde kullanılamaz"]
PAKET_NEDEN = ["Bunun nedeni bu paketlerin zaten birden fazla ürünün bir araya getirilmesiyle oluşturulması ve normal toplam fiyatlarının altında avantajlı şekilde satışa sunulmasıdır.",
               "İkinci bir kupon indirimi uygulanmaz."]
SPONSOR_BAS = "SPONSOR YAYINCI KODLARI"
SPONSOR = ["Kupon sisteminin önemli amaçlarından biri de SexyKO Sponsor Yayıncılarını desteklemektir.", "Sponsor Yayıncılara özel indirim kodları tanımlanabilir.",
           "Böylece hem oyuncu avantaj kazanır hem de SexyKO yayıncı topluluğu desteklenmiş olur."]
SPONSOR_AKIS = ["Sponsor Yayıncının kodunu kullanır", "PUS alışverişinde indirim kazanır", "Sponsor Yayıncıya destek olur"]
ETKINLIK_BAS = "ETKİNLİK DÖNEMLERİNDE %30'A VARAN İNDİRİM"
ETKINLIK = ["Özel etkinlik ve kampanya dönemlerinde Sponsor Yayıncı kuponlarında:", "Bu özel kodlar sürekli aktif olmayabilir.", "Özel kampanya kodlarını kaçırmayın!"]
TAKIP = ["Sponsor Yayıncıları", "SexyKO Discord kanalını", "Resmi duyuruları"]
OZEL_BAS = "SEXYKO & STONESOFT'A ÖZEL BİR SİSTEM"
OZEL = ["SexyKO'da oyuncuya yalnızca klasik bir Power Up Store sunmak istemiyoruz.", "PUS sistemini daha kullanışlı, daha avantajlı ve toplulukla daha bağlantılı hale getiriyoruz."]
OZEL_L = ["Tekli PUS alışverişlerinde indirim kullanabilirsiniz", "Basket alışverişlerinde kupon kullanabilirsiniz", "Sponsor Yayıncılara destek olabilirsiniz",
          "Etkinlik dönemlerinde yüksek indirimlerden yararlanabilirsiniz", "Kuponunuzu doğrudan oyun içerisindeki PUS ekranından kullanabilirsiniz"]
OZEL_SON = "Bu sistem SexyKO ve StoneSoft altyapısına özel olarak geliştirilen PUS özelliklerinden biridir."
KISACA = ["PUS'a gir", "Ürününü veya Basket'ini hazırla", "Kupon kodunu gir", "CHECK", "İNDİRİMİNİ KAZAN!"]
SLOGAN = "Sponsorunu destekle • Kuponunu kullan • Daha avantajlı alışveriş yap"
SON = "SEXYKO'DA PUS ALIŞVERİŞİ ARTIK DAHA AVANTAJLI!"

# --- resimdeki ORNEK (pus_1..3.png) — metinde yok
ORNEK_KOD = "Sexyko10"
ORNEK_TEKLI = ("Switching Premium", "950", "855 SB", "-10% (-95 SB)")
ORNEK_SEPET = "Coupon -10%: -282 SB, -210 KC"

for s in [*GIRIS, NASIL_BAS, *NASIL, TEKLI_BAS, *TEKLI, SEPET_BAS, *SEPET, PAKET_BAS, *PAKET, *PAKET_NEDEN, SPONSOR_BAS, *SPONSOR, ETKINLIK_BAS, *ETKINLIK,
          *TAKIP, OZEL_BAS, *OZEL, *OZEL_L, OZEL_SON, *KISACA, SLOGAN, SON, " → ".join(SPONSOR_AKIS)]:
    assert s in KAYNAK, s
for p in RESIM.values(): assert os.path.exists(p), p

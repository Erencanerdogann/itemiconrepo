# -*- coding: utf-8 -*-
# GENIE SISTEMI KONUSU — VERI (patron 8 Eki: forum arsivinde "cok kotu olan" d/16 — 4/4 resim kirik — "genie sistemi go").
# KAYNAK: genie/kaynak_d16.txt (forum.sexyko.com/d/16, Flarum API, 8 Eki) — ASAGIDAKI HER METIN KAYNAKTA BIREBIR VAR (import'ta assert).
# Ekran goruntuleri: gonderinin 4 resmi kaynakta 404 (i.hizliresim.com) -> yerine OYUNUN KENDI ekrani (3 Eki, rehber/oyun/: Knight Genie Main / Misc + sag ust Genie cubugu).
# KAYNAK <-> EKRAN FARKLARI (KONTROL'de): "uc temel islem" denip 4 madde var -> o cumle alinmadi · Party/Self HP esikleri ekranda Main -> Assist Thresholds'ta ·
#   Misc sekmesindeki secenekler (Combat / Maintenance / Return to town) kaynakta yok -> ekrandan birebir · Minor ve ayri "scroll alani" bu ekranda gorunmuyor.
import os

KOK = os.path.dirname(os.path.abspath(__file__))
GD = os.path.join(KOK, "genie")
KAYNAK = open(os.path.join(GD, "kaynak_d16.txt"), encoding="utf-8").read()
KONU_URL = "https://forum.sexyko.com/d/16"
RESIM = {"main": os.path.join(GD, "kaynak_resim", "genie_main.png"),     # Knight Genie — Main sekmesi (1228x815)
         "misc": os.path.join(GD, "kaynak_resim", "genie_misc.png"),     # Knight Genie — Misc sekmesi (1229x815)
         "panel": os.path.join(GD, "kaynak_resim", "genie_panel.png")}   # sag ust Genie cubugu (280x250, 1920x1200 ekrandan)

UST = "Başlat • Durdur • Kalan Süreni Gör • Ayarlarını Tek Panelden Yönet"
GIRIS = ["SexyKO Genie sistemi, karakterinizin belirlediğiniz kurallara göre otomatik şekilde saldırmasını, skill kullanmasını, HP/MP kontrolü yapmasını ve farm sürecini yönetmesini sağlayan gelişmiş bir otomasyon sistemidir.",
         "Yeni Genie arayüzüyle birlikte sistemi kullanmak ve kontrol etmek çok daha pratik hale getirildi."]
PANEL_BAS = "GENIE HIZLI KONTROL PANELİ"
PANEL_GIRIS = "Oyun ekranında bulunan Genie kontrol paneli üzerinden sisteme hızlıca müdahale edebilirsiniz."
PANEL = [("▶️", "BAŞLAT", ["Genie sistemini aktif eder.", "Daha önce oluşturduğunuz skill, pot, mob ve diğer ayarlarınız doğrultusunda karakteriniz otomatik olarak çalışmaya başlar."]),
         ("⏹️", "DURDUR", ["Aktif olan Genie sistemini durdurur.", "Farm işlemini sonlandırmak veya karakterinizi manuel olarak kontrol etmek istediğinizde bu seçeneği kullanabilirsiniz."]),
         ("⏳", "KALAN GENIE SÜRESİ", ["Panel üzerinden mevcut Genie kullanım sürenizi anlık olarak takip edebilirsiniz.",
                                     "Böylece Genie'nizin ne kadar süresi kaldığını görmek için farklı bir pencereye girmenize gerek kalmaz."]),
         ("⚙️", "AYARLAR", ["Ayarlar butonuna tıklayarak Genie'nin detaylı kontrol panelini açabilirsiniz.", "Skill sıralaması, pot kullanımı, saldırılacak moblar ve diğer otomasyon ayarları buradan yapılır."])]
ANA_BAS = "GENIE ANA AYARLARI"
ANA = ["Genie ayarlarını açtığınızda karakterinizin farm sırasında nasıl hareket edeceğini belirleyebileceğiniz ana panel karşınıza çıkar.",
       "Burada skill kullanımından pot yüzdelerine kadar birçok detay tamamen sizin kontrolünüzdedir."]
SKILL = [("⚔️", "ATTACK SKILLS", "8 ADET ATTACK SKILL SLOTU", ["Karakterinizin saldırı sırasında kullanacağı skillleri bu alana yerleştirirsiniz.",
                                                            "Genie, bu alana yerleştirdiğiniz skillleri belirlediğiniz düzene göre kullanır.",
                                                            "Bu sayede her job için farklı bir farm skill dizilimi oluşturabilirsiniz."]),
         ("🟢", "SELF SKILLS", "8 ADET SELF SKILL SLOTU", ["Karakterinizin kendi üzerinde kullanacağı skillleri bu alana yerleştirebilirsiniz.",
                                                        "Buff, karaktere özel destek skilleri ve kendi üzerinizde kullanılması gereken yetenekler buradan yönetilebilir."]),
         ("👥", "PARTY SKILLS", "8 ADET PARTY SKILL SLOTU", ["Party üyeleri üzerinde kullanılacak destek skillleri için hazırlanmıştır.",
                                                          "Özellikle Priest gibi party desteği sağlayan karakterlerde oldukça kullanışlıdır."])]
SCROLL = ("SKILL & SCROLL ALANLARI", ["Genie içerisinde skill kullanımının yanında yardımcı scroll alanları da bulunmaktadır.",
                                     "Farm sırasında kullanılmasını istediğiniz uygun scroll ve yardımcı öğeleri Genie sistemine tanımlayabilirsiniz.",
                                     "Böylece farm düzeniniz yalnızca saldırı skilllerinden ibaret kalmaz."])
HP = ("HP POT AYARLARI", "Genie karakterinizin HP değerini otomatik olarak takip edebilir.", "Potun hangi HP yüzdesinde kullanılacağını siz belirlersiniz.", "HP %60",
      "olarak ayarlanırsa karakterinizin canı belirlenen seviyeye geldiğinde Genie otomatik olarak HP pot kullanır.", "Farm yaptığınız bölgenin zorluğuna göre bu oranı değiştirebilirsiniz.")
MP = ("MP POT AYARLARI", "MP pot sistemi de aynı şekilde çalışır.", "Mana seviyesinin hangi yüzdeye geldiğinde pot kullanılacağını belirleyebilirsiniz.", "MP %40",
      "olarak ayarlanırsa mana belirlenen seviyeye düştüğünde Genie otomatik olarak MP pot basar.", "Özellikle sürekli skill kullanan karakterlerde oldukça önemlidir.")
MOB = ("SALDIRILACAK MOBLARI BELİRLE", "Genie ekranının sağ alt tarafında karakterinizin saldıracağı mobları belirleyebileceğiniz özel bir hedef listesi bulunur.",
       "Bu sistem sayesinde Genie'nin çevredeki her moba saldırmasını engelleyebilirsiniz.")
MOB_L = [("Mob Ekle", "Farm yapmak istediğiniz mobu listeye ekleyebilirsiniz."), ("Mob İsmini Kaydet", "Seçtiğiniz mobların isimleri hedef listenizde kayıtlı olarak görüntülenir."),
         ("Mob Sil", "Artık saldırmak istemediğiniz mobu listeden kaldırabilirsiniz.")]
MOB_SON = ["Bu özellik özellikle aynı slotta birden fazla yaratık bulunan bölgelerde büyük avantaj sağlar.", "Sadece istediğiniz mobu seçin, Genie yalnızca o hedeflere yönelsin."]
MISC = ("MISC / GELİŞMİŞ AYARLAR", "Genie içerisinde bulunan Misc bölümü, otomatik farm sistemini daha detaylı şekilde kişiselleştirmenizi sağlar.",
        "Bu bölüm özellikle Priest ve Rogue gibi karakterlerde oldukça kullanışlı ek seçenekler içerir.")
TAKIP = [("👥", "PARTY HP TAKİBİ", ["Genie, party içerisindeki oyuncuların HP durumunu takip edebilir.", "Party üyelerinin can seviyelerine göre belirlediğiniz destek skilllerinin kullanılması sağlanabilir.",
                                  "Özellikle Priest karakterlerde party desteğini otomatik hale getirmek için kullanışlıdır."]),
         ("❤️", "KENDİ HP'Nİ TAKİP ET", ["Karakterinizin kendi can durumunu sürekli takip etmesini sağlar.", "HP seviyesine göre Genie içerisinde belirlediğiniz işlemler otomatik olarak gerçekleştirilebilir."])]
MINOR = ("🩹", "MINOR KULLANIMI", ["Rogue / Assassin karakterler için Minor Healing kullanımını Genie üzerinden kontrol edebilirsiniz.",
                                  "Karakterinizin HP durumuna göre Minor kullanımı otomatik hale getirilebilir.",
                                  "Bu sayede farm sırasında HP Pot + Minor düzenini daha kontrollü kullanabilirsiniz."])
RANGE = ("ATTACK RANGE", "Attack Range ayarı Genie'nin karakterinizden ne kadar uzaklıktaki moblara saldıracağını belirler.")
RANGE_L = [("Düşük Range", "Karakteriniz daha dar bir farm alanında kalır."), ("Yüksek Range", "Daha geniş bir alandaki mobları hedefleyebilir.")]
RANGE_SON = "Sabit bir slotta farm yapıyorsanız karakterinizin gereksiz yere uzaklaşmasını önlemek için Attack Range değerini farm alanınıza göre ayarlamanız önemlidir."
KILIT = ("GENIE AKTİFKEN SKILL BAR KİLİTLENİR", ["Genie aktif edildiğinde normal skill barınız kilitlenir.", "Bu süre içerisinde manuel olarak skill kullanamazsınız.",
                                               "Karakteriniz yalnızca Genie içerisine yerleştirdiğiniz skill ve otomasyon ayarlarını kullanır.",
                                               "Genie'yi durdurduğunuzda tekrar manuel kullanıma geçebilirsiniz."])
KURULUM_BAS = "GENIE NASIL KURULUR?"
KURULUM = ["Genie Ayarlar bölümünü açın.", "Attack Skill'lerinizi yerleştirin.", "Self ve Party Skill'lerinizi ayarlayın.", "HP / MP pot yüzdelerinizi belirleyin.",
           "Saldırılmasını istediğiniz mobları listeye ekleyin.", "Misc bölümünden ek otomasyonları düzenleyin.", "Attack Range değerini farm alanınıza göre ayarlayın.",
           "Ayarlarınızı tamamlayıp Genie'yi başlatın."]
KURULUM_SON = "Bundan sonra kalan Genie sürenizi üst panelden takip edebilir, istediğiniz zaman sistemi Başlat / Durdur seçenekleriyle kontrol edebilirsiniz."
KISACA = ["Genie'yi tek tuşla başlatıp durdurabilirsiniz.", "Kalan kullanım sürenizi görebilirsiniz.", "8 adet Attack Skill kullanabilirsiniz.", "8 adet Self Skill ayarlayabilirsiniz.",
          "8 adet Party Skill ayarlayabilirsiniz.", "HP ve MP pot yüzdelerini belirleyebilirsiniz.", "Saldırılacak mobları seçebilirsiniz.",
          "Party HP ve kendi HP'nizi takip ettirebilirsiniz.", "Minor kullanımını otomatikleştirebilirsiniz.", "Attack Range değerini kendiniz ayarlayabilirsiniz."]
SLOGAN = "Skilllerini ayarla • Pot oranını belirle • Mobunu seç • Range'ini düzenle"
SON = "BAŞLAT VE GERİSİNİ GENIE'YE BIRAK!"

# --- EKRANDAN (kaynak metinde yok — oyunun Genie penceresi, 3 Eki): etiketler birebir, Turkcesi yaninda
EKRAN_MISC = [("Combat", [("Use R attacks", "R vuruşu kullan"), ("Go to the target", "hedefe git"), ("Return to the hunting centre", "av merkezine geri dön")]),
              ("Maintenance", [("Repair with a hammer", "çekiçle tamir et"), ("Keep the premium flash bonus up", "premium flash bonusunu açık tut"), ("Feed the pet", "pet'i besle")]),
              ("Return to town when", [("the party breaks up", "party dağılınca"), ("the party is wiped", "party tamamen ölünce"), ("the arrows run out", "oklar bitince")])]
EKRAN_IPUCU = ("Drag a skill from the skill window onto a slot", "Right-click a slot to empty it", "drag an icon out of the window to drop it")   # Misc ekranindaki ipucu satiri

# ---------- dogrulama
for s in [UST, *GIRIS, PANEL_BAS, PANEL_GIRIS, *[x for _, b, L in PANEL for x in (b, *L)], ANA_BAS, *ANA, *[x for _, b, n, L in SKILL for x in (b, n, *L)],
          SCROLL[0], *SCROLL[1], *HP, *MP, *MOB, *[x for a, b in MOB_L for x in (a, b)], *MOB_SON, *MISC, *[x for _, b, L in TAKIP for x in (b, *L)],
          MINOR[1], *MINOR[2], *RANGE, *[x for a, b in RANGE_L for x in (a, b)], RANGE_SON, KILIT[0], *KILIT[1], KURULUM_BAS, *KURULUM, KURULUM_SON, *KISACA, SLOGAN, SON]:
    assert s in KAYNAK, s
assert "Bu bölümde üç temel işlem bulunur:" in KAYNAK and len(PANEL) == 4          # kaynak "uc" diyor, 4 madde sayiyor -> o cumle konuya alinmadi
assert KAYNAK.count("[RESIM: https://i.hizliresim.com/") == 4                        # gonderinin 4 resmi (hepsi 404, 8 Eki arsivi)
for p in RESIM.values(): assert os.path.exists(p), p

# -*- coding: utf-8 -*-
# YAYINCI SISTEMI & SPONSOR YAYINCI BASVURUSU FORUM KONUSU (patron 8 Eki: "yeni forum konulari ... resimli vs ayni janradan devam" ·
# "hepsini tek tek konuya dok guzelce, resimleri repoya atmayi unutma, pushlamayi unutma"). Kaynak: forum.sexyko.com/d/37.
# Veri: _yayinci_veri.py · resimler: _yayinci_gorsel.py (V00-V05) + R01 logo · cevirici: _konu_blok.py
# CIKTI: yayinci/ (konu.json, YAYINCI_KONU_bbcode.txt / _markdown.md / _duz.txt) -> _konu_kit.py "Yayinci Sistemi" sekmesi.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, base64
from PIL import Image
import _konu_blok as KB
import _yayinci_veri as V

Y = KB.Y
OUT = V.YD; RD = os.path.join(OUT, "resim")
BASLIK = "🎥 SEXYKO YAYINCI SİSTEMİ & SPONSOR YAYINCI BAŞVURUSU | Canlı Takip · Başvuru · Şartlar"

RES = {"R01": Y.RESIM["R01"]}
for rid, dosya, acik in [("V00", "V00_ozet.jpg", "Yayıncı sistemi — bir bakışta"), ("V01", "V01_giris.jpg", "01 — Yayıncılar bölümüne giriş"),
                         ("V02", "V02_takip.jpg", "02 — Yayında olanları takip"), ("V03", "V03_basvuru.jpg", "03 · 04 — Başvuru formu + kurallar"),
                         ("V04", "V04_adimlar.jpg", "Başvuru — 7 adım"), ("V05", "V05_sartlar.jpg", "Sponsor Yayıncı başvuru şartları (10 madde)")]:
    RES[rid] = (dosya, acik, "")

B = []
def ekle(*b): B.append(b)

ekle("banner", "R01")
ekle("baslik", "SEXYKO YAYINCI SİSTEMİ & YAYINCI BAŞVURUSU", "Yayıncıları takip et · canlı yayınları keşfet · destek ol · kendi başvurunu yap")
ekle("icindekiler")
ekle("ayrac")

ekle("h", "🎥", "BİR BAKIŞTA")
ekle("img", "V00", "")
ekle("p", V.GIRIS[0])
ekle("p", f"**{V.GIRIS[1]}**")
ekle("ayrac")

ekle("h", "📍", V.B01[0])
ekle("img", "V01", "")
ekle("p", f"{V.B01[1]} {V.B01[2]}")
ekle("p", "**Buradan:**")
ekle("liste", V.B01_L)
ekle("ayrac")

ekle("h", "🔴", V.B02[0])
ekle("img", "V02", "")
ekle("p", V.B02[1] + " Bu bölüm sayesinde hangi yayıncının:")
ekle("liste", V.B02_L)
ekle("p", f"kolayca takip edebilirsiniz. **{V.B02[2]}**")
ekle("ayrac")

ekle("h", "❤️", V.DESTEK[0])
ekle("p", V.DESTEK[1][0])
ekle("p", f"**{V.DESTEK[1][1]}** {V.DESTEK[1][2]}")
ekle("ayrac")

ekle("h", "🎙️", V.B03[0])
ekle("p", f"{V.B03[1]} Yayıncılar bölümünde bulunan **Yayıncı Başvurusu Yap** seçeneğine tıklayarak başvuru ekranına geçebilirsiniz.")
ekle("ayrac")

ekle("h", "📋", V.B04[0])
ekle("img", "V03", "")
ekle("p", " ".join(V.B04[1][:3]))
ekle("not", f"**{V.B04[1][3]}**")
ekle("ayrac")

ekle("h", "✍️", V.FORM[0])
ekle("p", V.FORM[1] + " Başvuruda genel olarak:")
ekle("liste", V.FORM_L)
ekle("p", f"gibi bilgiler talep edilebilir. **{V.FORM[2]}**")
ekle("ayrac")

ekle("h", "✅", "BAŞVURU NASIL YAPILIR?")
ekle("img", "V04", "")                                   # 7 adim resimde (patron 7 Eki: "resimde var, yazman lazim miydi") -> metinde tekrar yok
ekle("p", f"**{V.NASIL_SON}**")
ekle("ayrac")

ekle("h", "⚠️", V.DIKKAT[0])
ekle("p", V.DIKKAT[1] + " Özellikle:")
ekle("liste", V.DIKKAT_L)
ekle("p", f"başvurunun değerlendirilmesini zorlaştırabilir. **{V.DIKKAT[2]}**")
ekle("ayrac")

ekle("h", "🎙️", "SPONSOR YAYINCI BAŞVURU ŞARTLARI")
ekle("img", "V05", "")
for i, b, m, k in V.SART:
    ekle("p", f"{i} **{b}** — {m}")
ekle("ayrac")

ekle("h", "🔗", "BAĞLANTILAR")
ekle("liste", ["🌐 Web: [[https://www.sexyko.com|www.sexyko.com]] → **YAYINCILAR**",
               "💬 Discord: [[https://discord.gg/sexyko|discord.gg/sexyko]] · Forum: [[https://forum.sexyko.com|forum.sexyko.com]]"])
ekle("ayrac")
ekle("son", f"🔥 {V.SON.rstrip('.').replace('i', 'İ').replace('ı', 'I').upper()} 🔥")   # Turkce buyuk harf (Python upper 'i' -> 'I' yapiyordu)

KONTROL = [
    "**Kaynak:** forum.sexyko.com/d/37 (Flarum API, 8 Eki) — her cümle / şart kaynakta birebir (`_yayinci_veri.py` assert).",
    "**Ekran görüntüleri:** gönderinin 3 resmi (menü, Yayıncılar sayfası, başvuru formu + şartlar) V01–V03'ün içinde, önemli yerler numaralı çerçeveli. **1. resim (SPONSOR.png bannerı) kaynakta da 404** → kullanılmadı.",
    "⚠ **Kaynak kusuru 1:** \"Mikrofon Kullanımı\" maddesinin son cümlesi yarım (\"…yayın boyunca etkileşim **sağlam**\" — sitedeki şartlarda da yarım) → yarım cümle konuya ALINMADI; ekip tamamlarsa eklenir.",
    "⚠ **Kaynak kusuru 2:** \"SexyKO İçeriği\" maddesinde \"beklenmektedir Yayınlarda\" → sadece noktalama düzeltildi (\"beklenmektedir. Yayınlarda: …\").",
    "Takipçi şartı kaynakta **Youtube veya Kick** (250); formdaki kanal notu **Twitch, Kick veya YouTube** diyor — çelişki gibi görünüyor, ekip teyit etsin.",
    "**6 resim (V00–V05)** — hazır linkli (itemiconrepo `forum/yayinci/resim/`, içerik özetli). R01 logo ortak.",
]

L, NO = KB.basliklar(B)
BB, HT, MD, DZ = KB.bb(B), KB.onizleme(B), KB.md(B), KB.duz(B, RES)
KB.denetle(BB, RES)
for s in [V.GIRIS[0], V.B01[1], *V.B01_L, *V.B02_L, *V.DESTEK[1], *V.FORM_L, V.NASIL_SON, *V.DIKKAT_L, *[m for _, _, m, _ in V.SART]]: assert s in BB, s[:60]
assert "sağlam" not in BB and "İÇERİK ÜRETİCİLERİYLE" in BB and len(BASLIK) <= 100, len(BASLIK)
res = []
for rid in ["R01", "V00", "V01", "V02", "V03", "V04", "V05"]:
    dosya, acik, url = RES[rid]
    d = {"id": rid, "aciklama": acik, "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum d/37 + SexyKO paneli"}
    if dosya:
        p = os.path.join(RD, dosya); raw = open(p, "rb").read()
        with Image.open(p) as im:
            d["boyut"] = f"{im.width}x{im.height}"
        d.update(dosya="FORUM/yayinci/resim/" + dosya, data="data:image/jpeg;base64," + base64.b64encode(raw).decode(), kb=len(raw) // 1024)
    res.append(d)
import _repo_resim; _repo_resim.uygula(res)
VERI = {"baslik": BASLIK, "bbcode": BB, "html": HT, "markdown": MD, "duz": DZ, "resimler": res, "kontrol": KONTROL,
        "bolum": [f"{NO[x]} · {x[0]} {x[1]}" for x in L], "kaynak": "forum.sexyko.com/d/37 (metin + 3 ekran görüntüsü)"}
json.dump(VERI, open(os.path.join(OUT, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(OUT, "YAYINCI_KONU_bbcode.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + BB + "\n")
open(os.path.join(OUT, "YAYINCI_KONU_markdown.md"), "w", encoding="utf-8").write("# " + BASLIK + "\n\n" + MD + "\n")
open(os.path.join(OUT, "YAYINCI_KONU_duz.txt"), "w", encoding="utf-8").write(BASLIK + "\n\n" + DZ + "\n")
print("YAYINCI: bölüm", len(L), "· blok", len(B), "· resim", len(res), "· [IMG]", BB.count("[IMG]"), "· [URL]", BB.count("[URL="),
      "· bbcode", len(BB), "· başlık", len(BASLIK), "karakter · gömülü", sum(x["kb"] or 0 for x in res), "KB")

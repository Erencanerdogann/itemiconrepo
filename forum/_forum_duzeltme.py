# -*- coding: utf-8 -*-
# FORUM KONULARINA RESMI KAYNAK DUZELTMELERI (13 Eki aksam PATRON "duzelt" — yayin oncesi kontrolde forum metni resmi rehberle celisti).
# Kaynak: sexyko.com/guide (Hyper, canli; yerel kopya rehber/web/sayfa/book/*.html, 3 Eki). Sadece rehberin ACIKCA yazdigi bilgi duzeltilir;
# kaniti olmayan celiskiler (baslangic level, Draki level, pelerin sayisi, Royal NP, etkinlik saatleri, odul listeleri) PATRON kararinda — burada YOK.
# Uygulama: kaynak konunun HTML'i (m0["html"]) — FY.insa + FY.dogrula ayni metni gorur. "📜 Forumdaki hali" (m0["bbcode"]) DEGISMEZ (forumun bugunku hali).
# Her duzeltme (eski, yeni, kanit) — eski metin bulunamazsa ASSERT (forum degisirse sessizce kaymaz).
import copy

DUZELT = {
    25: [
        ("<strong>Kontenjan:</strong> İlk 82 Oyuncu", "<strong>Kontenjan:</strong> İlk 80 Oyuncu",
         "book/forgotten-temple: 'Kapasite 80 oyuncu' · 'Yalnızca ilk 80 kişi girebilir'"),
        ("<strong>Giriş:</strong> Premium bulunmayan oyuncular için <strong>100 Ladder NP</strong>", "<strong>Giriş:</strong> Ücretsiz",
         "book/chaos: 'Katılım Ücretsiz' · 'Bu etkinliğe ücretsiz şekilde katılabilirsiniz'"),
        ("BORDER DEFENSE WAR — BDW</h2>\n\n<p><strong>Level Sınırı:</strong> 20 — 83", "BORDER DEFENSE WAR — BDW</h2>\n\n<p><strong>Level Sınırı:</strong> 20 — 80",
         "book/bdw: 'Seviye 20 - 80'"),
        ("<h3>☠️ 30 Kill Kuralını Unutmayın</h3>", "<h3>☠️ 600 Puan Kuralını Unutmayın</h3>", "book/bdw: 'Kazanma Kuralları 600 puana ilk ulaşan takım'"),
        ("<p>Anıt alınamasa bile:</p>", "<p>Kazanma şartı:</p>", "book/bdw (30 kill kurali rehberde yok)"),
        ("<strong>30 Kill sayısına ilk ulaşan taraf etkinliği doğrudan kazanır.</strong>",
         "<strong>600 puana ilk ulaşan taraf kazanır — her kill 2 puan, altarı üsse teslim etmek 80 puan.</strong>",
         "book/bdw: 'Düşman öldürmek 2 puan' · 'Altar'ı üssünüze teslim etmek 80 puan' · '600 puana ilk ulaşan takım ... kazanılır'"),
        # hizli ozet: forumda markdown tablo duz metin kalmisti ("| a | b |") -> okunur satir; BDW seviyesi rehberle ayni
        ("<p>| Etkinlik | Level | Ana Ödül |</p>", "<p>Etkinlik · Level · Ana Ödül</p>", "gorunum"),
        ("| ⚔️ BDW | 20 — 83 | Red Chest + EXP |", "⚔️ BDW · Lv 20 — 80 · Red Chest + EXP", "book/bdw: 'Seviye 20 - 80'"),
        ("| 🌀 Chaos | 70 — 83 | Treasure Chest |", "🌀 Chaos · Lv 70 — 83 · Treasure Chest", "gorunum"),
        ("| 🛡️ JR | 70 — 83 | Silvery / Black Gem |", "🛡️ JR · Lv 70 — 83 · Silvery / Black Gem", "gorunum"),
        ("| 🔥 FT | 60 — 83 | Chest + FT Coin |", "🔥 FT · Lv 60 — 83 · Chest + FT Coin", "gorunum"),
        ("| 🏰 UTC | 75 — 83 | UTC Item &amp; Materyal |", "🏰 UTC · Lv 75 — 83 · UTC Item &amp; Materyal", "gorunum"),
        ("| 💎 Bifrost | 70 — 83 | Günah Taşları |", "💎 Bifrost · Lv 70 — 83 · Günah Taşları", "gorunum"),
        ("| 🗡️ Draki | 70 — 83 | Badge + Superior Box |", "🗡️ Draki · Lv 70 — 83 · Badge + Superior Box", "gorunum"),
    ],
}


def uygula(k):
    """bbcode.json konu kaydi -> duzeltilmis kopya (sadece m0 html). Duzeltmesi olmayan konu aynen doner."""
    d = DUZELT.get(k["id"])
    if not d: return k
    k = copy.deepcopy(k); h = k["mesajlar"][0]["html"]
    for eski, yeni, _ in d:
        assert h.count(eski) == 1, (k["id"], "duzeltme kaynagi bulunamadi / birden cok", eski[:60], h.count(eski))
        h = h.replace(eski, yeni)
    k["mesajlar"][0]["html"] = h
    return k

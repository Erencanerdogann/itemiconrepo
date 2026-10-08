# -*- coding: utf-8 -*-
# Forum kitine YENI KONU SEKMESI ekler (8 Eki — TeamSpeak / PUS kupon / Yayinci konulari ayni kaliptan).
# Kalip = "24 Saat Madencilik" sekmesi (k_mining, onek m). Yapilanlar (her biri tek sefer, tekrar calistirmak zararsiz):
#   _konu_sablon.html: buton + sekme blogu (id onekleri degisir) + KONU haritasi · _konu_kit.py: VERI + Flarum dosyasi · _repo_aktar.py: KONULAR
# Kullanim: python _sekme_ekle.py <onek> <anahtar> <klasor> <dosya_on>   (ornek: q teamspeak teamspeak TS)  — metinler SEKMELER sozlugunden
import sys, os, re
sys.stdout.reconfigure(encoding="utf-8")
KOK = os.path.dirname(os.path.abspath(__file__))

SEKMELER = {
    "teamspeak": dict(buton="🎙️ Ücretsiz TeamSpeak",
                      h2="🎙️ Ücretsiz TeamSpeak konusu (forum.sexyko.com/d/55)",
                      adim1="Ücretsiz TeamSpeak — bir bakışta · 3 adım (panel → sunucu bilgileri + KEY → KEY ile ilk giriş) · clanını topla — <b>resimli</b> (5 görsel, gönderinin kendi ekran görüntüleriyle).",
                      alt="Bilgi: <b>forum.sexyko.com/d/55</b> (SexyKO, 5 Eki) — her cümle kaynakta birebir; form alanları (64 slot, clanadi.ts.sexyko.com) ekran görüntüsünden → <b>⚠ Kontrol</b>."),
    "pus": dict(buton="🎟️ PUS İndirim Kodu",
                h2="🎟️ PUS İndirim Kodu Sistemi konusu (forum.sexyko.com/d/51)",
                adim1="Kupon nedir · nasıl kullanılır (Kupon → CHECK) · tekli item · Basket · VIP / Farm paketi istisnası · Sponsor Yayıncı kodları · etkinlikte %30'a varan — <b>resimli</b>.",
                alt="Bilgi: <b>forum.sexyko.com/d/51</b> (SexyKO) — her cümle kaynakta birebir → <b>⚠ Kontrol</b>."),
    "yayinci": dict(buton="🎥 Yayıncı Sistemi",
                    h2="🎥 Yayıncı Sistemi &amp; Sponsor Yayıncı Başvurusu konusu (forum.sexyko.com/d/37)",
                    adim1="Yayıncılar bölümü · canlı yayıncı takibi · destek · başvuru (kurallar + form + 7 adım) · Sponsor Yayıncı şartları — <b>resimli</b>.",
                    alt="Bilgi: <b>forum.sexyko.com/d/37</b> (SexyKO) — her cümle / şart kaynakta birebir → <b>⚠ Kontrol</b>."),
    "genie": dict(buton="⚙️ Genie Sistemi",
                  h2="⚙️ Genie Sistemi konusu (forum.sexyko.com/d/16 — yeniden, resimler oyundan)",
                  adim1="Hızlı panel (Başlat / Durdur / kalan süre / Ayarlar) · Main: 8+8+8 skill, HP/MP pot, mob listesi, Party/Self heal, Attack range · Misc · skill bar kilidi · 8 adımda kurulum — <b>resimli</b> (8 görsel, oyunun kendi Genie penceresi).",
                  alt="Bilgi: <b>forum.sexyko.com/d/16</b> (SexyKO) — her cümle kaynakta birebir; gönderinin 4 resmi 404 → oyun ekranı (3 Eki) → <b>⚠ Kontrol</b>."),
}


def ekle(onek, anahtar, klasor, dosya_on):
    s = SEKMELER[anahtar]
    # ---------- sablon
    p = os.path.join(KOK, "_konu_sablon.html"); t = open(p, encoding="utf-8").read()
    if f'id="k_{anahtar}"' not in t:
        i = t.index('<div id="k_mining" class="konu">')
        # 8 Eki: blok sonu aramasi girintiye bagliydi -> girintisiz eklenen TeamSpeak blogu PUS'a KOPYALANDI (cift k_teamspeak). Artik girintiden bagimsiz.
        j = re.compile(r'\n[ \t]*<div id="k_[a-z]+" class="konu').search(t, i + 10).start() + 1
        blok = t[i:j]
        assert not re.search(rf'id="{onek}[a-z]', t), f"onek {onek} kullanimda"
        blok = blok.replace('id="k_mining"', f'id="k_{anahtar}"').replace('id="m', f'id="{onek}').replace('data-p="m', f'data-p="{onek}')
        h2 = re.search(r"<h2>.*?</h2>", blok).group(0); blok = blok.replace(h2, f"<h2>{s['h2']}</h2>", 1)
        li = re.search(r"<ol class=\"adim\">\s*<li>.*?</li>", blok, re.S).group(0)
        blok = blok.replace(li, li[:li.index("<li>")] + f"<li>{s['adim1']}</li>", 1)
        blok = blok.replace("forum/mining/resim/", f"forum/{klasor}/resim/")
        alt = re.search(r'<div class="alt">Bilgi:.*?</div>', blok).group(0); blok = blok.replace(alt, f'<div class="alt">{s["alt"]}</div>', 1)
        blok = blok.rstrip(" \t")                                    # sonraki blogun girintisi bloga girmesin
        t = t[:j] + "  " + blok + t[j:]                               # yeni blok da 2 bosluk girintili
        assert t.count(f'id="k_{anahtar}"') == 1 and t.count(f'id="{onek}onzic"') == 1, "cift blok"
        b0 = '    <button type="button" data-konu="k_mining">⛏️ 24 Saat Madencilik</button>\n'
        assert t.count(b0) == 1
        # yeni butonlar madencilikten sonra, SIRAYLA (ts -> pus -> yayinci): son eklenen butonun arkasina
        son = max((t.index(f'data-konu="k_{k}"') for k in SEKMELER if f'data-konu="k_{k}"' in t), default=-1)
        yer = t.index("\n", son) + 1 if son > t.index(b0) else t.index(b0) + len(b0)
        t = t[:yer] + f'    <button type="button" data-konu="k_{anahtar}">{s["buton"]}</button>\n' + t[yer:]
        km = 'k_mining:kur("m",V.mining,"mining_konu_url_v1")'
        assert t.count(km) == 1
        t = t.replace(km, km + f',k_{anahtar}:kur("{onek}",V.{anahtar},"{anahtar}_konu_url_v1")')
        open(p, "w", encoding="utf-8").write(t); print("sablon: sekme eklendi", anahtar)
    # ---------- kit
    p = os.path.join(KOK, "_konu_kit.py"); t = open(p, encoding="utf-8").read()
    if f'VERI["{anahtar}"]' not in t:
        a = 'json.dump(VERI, open(os.path.join(KOK, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)'
        assert t.count(a) == 1
        t = t.replace(a, f'# {s["buton"]} KONUSU (8 Eki) — once python _{dosya_on.lower()}_gorsel.py + _{dosya_on.lower()}_konu.py\n'
                         f'_k{onek} = os.path.join(KOK, "{klasor}", "konu.json")\nVERI["{anahtar}"] = json.load(open(_k{onek}, encoding="utf-8")) if os.path.exists(_k{onek}) else None\n' + a)
        b = '("mining", "mining/MINING_KONU_bbcode_flarum.txt")'
        assert t.count(b) == 1
        t = t.replace(b, b + f', ("{anahtar}", "{klasor}/{dosya_on}_KONU_bbcode_flarum.txt")')
        open(p, "w", encoding="utf-8").write(t); print("kit: eklendi", anahtar)
    # ---------- repo aktar
    p = os.path.join(KOK, "_repo_aktar.py"); t = open(p, encoding="utf-8").read()
    if f'"{klasor}/konu.json"' not in t:
        a = '"mining/konu.json"'
        assert t.count(a) == 1
        t = t.replace(a, a + f', "{klasor}/konu.json"'); open(p, "w", encoding="utf-8").write(t); print("repo: eklendi", klasor)


if __name__ == "__main__":
    ekle(*sys.argv[1:5])

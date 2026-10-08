# -*- coding: utf-8 -*-
# FORUMDAKI KONULAR -> FORUM_KONU.html SEKMELERI (patron 8 Eki: "file:///C:/temp/Sexyko/HTML/FORUM_KONU.html ayni bunlarin gibi yapacaksin").
# Veri: forum_bbcode/bbcode.json (_forum_bbcode.py — forumdaki butun konular, BBCode forum HTML'inden geri cevrilmis, testli).
# Her konu = diger sekmelerle AYNI blok (Baslik kopyala · BBCode kopyala · Gorunum / Markdown / Duz · Onizleme · Resimler · Kontrol) — blok k_mining'den kopyalanir.
# Bizim zaten sekmesi olan konular (forumdakiyle birebir ayni) tekrar eklenmez. _konu_kit.py sayfayi yazmadan once cagirir: sab = ekle(sab, VERI).
import os, re, json, html
import _forum_arsiv as FA
import _forum_yeniden as FY
import _konu_blok as KB

KOK = os.path.dirname(os.path.abspath(__file__))
BIZIM = {16: "genie", 37: "yayinci", 51: "pus", 54: "odul", 55: "teamspeak", 56: "skill", 57: "sezon", 58: "mining"}   # kendi sekmesi var
KORU = {"F10", "NCS", "PUS", "VIP", "GM", "KO", "CR", "HP", "MP", "NP", "PK", "PVP", "EXP", "FPS"}
# Ingilizce kelimeler: buyuk 'I' = i (Turkce kelimede I = ı). 8 Eki ilk deneme 'Clıent / Mınıng / Skıll' yapmisti.
INGILIZCE = {"CLIENT", "GRIND", "MINING", "INN", "NICK", "SKILL", "QUICK", "REBIRTH", "EQUIPMENT", "VIEW", "BIT", "DRAKI'S", "CHAOTIC", "INFO", "DAILY",
             "IMASSAKA", "ITEM", "LIST", "SPIN", "BINGO", "TIME", "KING", "WING", "PING", "LIMIT"}
OZEL = {"KENDINI/CLANINI": "Kendini/Clanını"}                          # kaynak basligi noktasiz I ile yazilmis


def tr_kucuk(s): return s.replace("I", "ı").replace("İ", "i").lower()


def _kucuk(w):
    """kelimeyi kucult: Ingilizce (veya Turkce harfi olmayan bilinen Ingilizce) -> standart, degilse Turkce."""
    cekirdek = re.sub(r"[^A-Za-zÇĞİÖŞÜçğıöşü']", "", w)
    return w.lower() if cekirdek.upper() in INGILIZCE else tr_kucuk(w)


def tr_baslik(s):
    """'🔥 SEXYKO'DA KIRDIRMA SİSTEMİ DETAYLARI' -> '🔥 Kırdırma Sistemi Detayları' (sadece cogu buyuk harfli basliklar)."""
    harf = [c for c in s if c.isalpha()]
    if not harf or sum(c.isupper() for c in harf) / len(harf) < 0.7: return s.strip()
    s = re.sub(r"\bSEXYKO(?:'DA|’DA)?\s+", "", s).strip()
    def parca(w):
        if w in OZEL: return OZEL[w]
        if w.upper() in KORU or not any(c.isalpha() for c in w): return w
        k = _kucuk(w); i = next((j for j, c in enumerate(k) if c.isalpha()), None)
        if i is None: return k
        b = {"i": "İ", "ı": "I"}.get(k[i], k[i].upper()) if w[i] != "I" or k[i] != "i" else "I"
        return k[:i] + b + k[i + 1:]
    def kel(w):
        if w in OZEL: return OZEL[w]
        return "-".join(parca(x) for x in w.split("-"))                # 64-BIT -> 64-Bit
    return " ".join(kel(w) for w in s.split(" "))


def duz(h):
    t = re.sub(r"<br\s*/?>", "\n", h); t = re.sub(r"</(p|div|li|h[1-6]|blockquote)>", "\n\n", t); t = re.sub(r"<li[^>]*>", "• ", t)
    t = re.sub(r'<img[^>]*\bsrc="([^"]+)"[^>]*>', lambda m: f"[RESİM: {html.unescape(m.group(1))}]", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+\n", "\n", t)).strip()


def veri(k, r01=None):
    """8 Eki PATRON "butun forum konularini bizim temamiza gore yeniden insa et": _forum_yeniden.insa -> bizim blok temasi (metin + resim konunun kendisi).
    Butunluk ASSERT: kaynaktaki her satirin yazisi + her saglam resim yeni BBCode'da (FY.dogrula)."""
    m0 = k["mesajlar"][0]; kirik = set(k.get("kirik_url") or [])
    Bl, R, KN = FY.insa(k, kirik)
    BB = KB.bb(Bl)
    kullanilan = set(re.findall(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", BB))
    res = []
    if "R01" in kullanilan:
        assert r01, "R01 logo kaydi yok"; res.append({x: r01[x] for x in r01 if x != "data"} | {"data": None})
    for rid, (_, acik, url) in R.items():
        res.append({"id": rid, "aciklama": acik + (" — ⚠ KIRIK (404)" if url in kirik else ""), "varsayilan_url": url, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum"})
    RES = {r["id"]: (None, r["aciklama"], r["varsayilan_url"]) for r in res}
    KB.denetle(BB, RES)
    tam = re.sub(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", lambda m: RES[m.group(1)][2], BB)
    ek, er = FY.dogrula(k, tam, kirik)
    assert not ek and not er, (k["id"], ek[:3], er[:2])
    q = k["kalite"]
    kontrol = [f"**Yeniden inşa (8 Eki, bizim tema):** metin ve resimler forumdaki konunun kendisi — eklenen sadece yapı (başlık, içindekiler, bölüm numarası, ayraç, bağlantılar). "
               "Test: kaynaktaki her satır + her sağlam resim yeni BBCode'da ✅.",
               f"**Kaynak:** forum.sexyko.com/d/{k['id']} — yazar {k['yazar']} · açılış {k['acilis']}" + (f" · son düzenleme {m0['duzenleme']}" if m0.get("duzenleme") else "") + ". Eski hali: **📜 Forumdaki hali** sekmesi."]
    if q["kucuk"]: kontrol.append(f"Eski halinde küçük yazı vardı (en küçük {q['min_px']} px) → yeni halde bütün yazılar tek boy (18 px).")
    kontrol += KN
    if k["mesaj_sayisi"] > 1: kontrol.append(f"Konuda {k['mesaj_sayisi'] - 1} cevap daha var (forumda) — burada sadece konu mesajı.")
    HT = KB.onizleme(Bl).replace("<img ", '<img loading="lazy" ')   # 38 konunun resimleri acilista yuklenmesin (3,0 sn olculdu)
    return {"baslik": k["baslik"], "bbcode": BB, "html": HT, "markdown": KB.md(Bl), "duz": KB.duz(Bl, RES), "resimler": res, "kontrol": kontrol,
            "bolum": [f"{x[0]} {x[1]}" for x in KB.basliklar(Bl)[0]], "kaynak": k["url"], "orijinal": m0["bbcode"]}


def ekle(sab, VERI):
    """sab (FORUM_KONU sablonu) + VERI -> forum konusu sekmeleri eklenmis sablon. VERI['f<id>'] doldurulur."""
    yol = os.path.join(KOK, "forum_bbcode", "bbcode.json")
    if not os.path.exists(yol): return sab
    B = json.load(open(yol, encoding="utf-8"))
    konular = [k for k in B["konular"] if k["id"] not in BIZIM and k["mesajlar"] and "html" in k["mesajlar"][0]]
    i = sab.index('<div id="k_mining" class="konu">')
    j = re.compile(r'\n[ \t]*<div id="k_[a-z]+" class="konu').search(sab, i + 10).start() + 1
    kalip = sab[i:j].rstrip(" \t")
    bloklar, butonlar, kur = [], [], []
    r01 = next((r for v in VERI.values() if isinstance(v, dict) and v.get("resimler") for r in v["resimler"] if r.get("id") == "R01" and r.get("varsayilan_url")), None)   # ortak logo
    for k in konular:
        P = f"f{k['id']}"; Y = veri(k, r01); VERI[P] = Y
        b = kalip.replace('id="k_mining"', f'id="k_{P}"').replace('id="m', f'id="{P}').replace('data-p="m', f'data-p="{P}')
        b = re.sub(r"<h2>.*?</h2>", f"<h2>📜 {html.escape(k['baslik'])} — forum.sexyko.com/d/{k['id']}</h2>", b, count=1)
        kr = k.get("kirik_resim")
        adim = (f"<li><b>Bizim temayla yeniden inşa</b> — {len(Y['bolum'])} bölüm (" + html.escape(" · ".join(Y["bolum"][:-1])[:160]) + ") · metin ve resimler konunun kendisi.</li>"
                + f"<li><b>🖼 Resimler</b> forumdaki linkleriyle ({len([r for r in Y['resimler'] if r['id'] != 'R01'])})" + (f" — <b>⚠ {kr[0]} kırık resim çıkarıldı</b>" if kr and kr[0] else "") + ".</li>"
                + f"<li>forum.sexyko.com/d/{k['id']} → <b>Düzenle</b> → <b>BBCode kopyala</b> → yapıştır. Eski hali: <b>📜 Forumdaki hali</b>.</li>")
        b = re.sub(r'(<ol class="adim">).*?(</ol>)', lambda m: m.group(1) + adim + m.group(2), b, count=1, flags=re.S)
        b = re.sub(r'<div class="alt">Bilgi:.*?</div>', f'<div class="alt">Bilgi: <b>forum.sexyko.com/d/{k["id"]}</b> · {html.escape(k["yazar"])} · açılış {k["acilis"][:10]} · '
                   f'{k["mesaj_sayisi"]} mesaj → <b>⚠ Kontrol</b>.</div>', b, count=1)
        # 📜 Forumdaki hali paneli (eski BBCode) — Kontrol'un yanina
        kb_ = f'<button data-p="{P}kt">⚠ Kontrol</button>'; kp_ = f'<div class="ypan" id="{P}kt"><ul id="{P}kl"></ul></div>'
        assert b.count(kb_) == 1 and b.count(kp_) == 1, P
        b = b.replace(kb_, kb_ + f'\n      <button data-p="{P}org">📜 Forumdaki hali</button>')
        b = b.replace(kp_, kp_ + f'\n    <div class="ypan" id="{P}org"><textarea readonly>{html.escape(Y["orijinal"])}</textarea></div>')
        assert b.count(f'id="k_{P}"') == 1 and f'id="{P}onzic"' in b and 'id="m' not in b, P
        bloklar.append("  " + b)
        rozet = (" ⚠" if (k["kalite"]["kucuk"] or (kr and kr[0])) else "")
        butonlar.append(f'    <button type="button" class="fk" data-konu="k_{P}" title="forum.sexyko.com/d/{k["id"]}">{html.escape(tr_baslik(k["baslik"]))}{rozet}</button>\n')
        kur.append(f'k_{P}:kur("{P}",V.{P},"forum_d{k["id"]}_url_v1")')
    # sekme blokları: k_mining'in onune
    sab = sab[:i] + "".join(bloklar) + sab[i:]
    # dugmeler: ksec'in sonuna, ayri baslikla
    son = '<button type="button" data-konu="k_tanitim">'
    a = sab.index(son); a = sab.index("\n", a) + 1
    etiket = (f'    <div class="fkb">📜 Forumdaki konular — bizim temayla yeniden ({len(konular)} konu · ⚠ = eski halinde küçük yazı / kırık resim vardı)</div>\n')
    sab = sab[:a] + etiket + "".join(butonlar) + sab[a:]
    # stil
    css = ".ksec .fkb{flex-basis:100%;margin:12px 0 0;font-weight:700;font-size:15px;color:var(--ana)}.ksec button.fk{font-size:13px;padding:6px 11px}[id^=\"k_f\"] .onz img{max-width:100%;height:auto}\n"
    sab = sab.replace("</style>", css + "</style>", 1)
    # Resimler listesi lazy (38 konunun resimleri gizli panelde de acilista yukleniyordu: acilis 3,4 sn -> 14 sn olculdu)
    eski = "<img src=\"'+(r.data||r.varsayilan_url)+'\" alt=\"'+r.id+'\">"
    assert sab.count(eski) == 1, "rsl img kalibi"
    sab = sab.replace(eski, "<img loading=\"lazy\" src=\"'+(r.data||r.varsayilan_url)+'\" alt=\"'+r.id+'\">")
    # KONU haritasi
    m = re.search(r"var KONU=\{.*?\};", sab)
    assert m, "KONU haritasi yok"
    sab = sab[:m.end() - 2] + "," + ",".join(kur) + sab[m.end() - 2:]
    print(f"forum sekmeleri: {len(konular)} konu eklendi (bizim sekmesi olan {len(BIZIM)} hariç)")
    return sab

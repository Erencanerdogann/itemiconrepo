# -*- coding: utf-8 -*-
# FORUMDAKI KONULAR -> FORUM_KONU.html SEKMELERI (patron 8 Eki: "file:///C:/temp/Sexyko/HTML/FORUM_KONU.html ayni bunlarin gibi yapacaksin").
# Veri: forum_bbcode/bbcode.json (_forum_bbcode.py — forumdaki butun konular, BBCode forum HTML'inden geri cevrilmis, testli).
# Her konu = diger sekmelerle AYNI blok (Baslik kopyala · BBCode kopyala · Gorunum / Markdown / Duz · Onizleme · Resimler · Kontrol) — blok k_mining'den kopyalanir.
# Bizim zaten sekmesi olan konular (forumdakiyle birebir ayni) tekrar eklenmez. _konu_kit.py sayfayi yazmadan once cagirir: sab = ekle(sab, VERI).
import os, re, json, html
import _forum_arsiv as FA

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


def veri(k):
    m0 = k["mesajlar"][0]; h = m0["html"]; kirik = set(k.get("kirik_url") or [])
    srcs = re.findall(r"\[IMG\](.*?)\[/IMG\]", m0["bbcode"])
    res = []
    for i, u in enumerate(srcs, 1):
        res.append({"id": f"F{i:02d}", "aciklama": f"forumdaki {i}. resim" + (" — ⚠ KIRIK (404), yeni resim gerekir" if u in kirik else ""),
                    "varsayilan_url": u, "dosya": None, "data": None, "kb": None, "boyut": None, "kaynak": "forum"})
    q = k["kalite"]; kr = k.get("kirik_resim")
    kontrol = [f"**Kaynak:** forum.sexyko.com/d/{k['id']} — yazar {k['yazar']} · açılış {k['acilis']}" + (f" · son düzenleme {m0['duzenleme']}" if m0.get("duzenleme") else "") + ".",
               "**BBCode forumdaki konunun kendisi** — forum ham BBCode'u herkese vermediği için forum görünümünden geri çevrildi: yapıştırınca forumda aynı görünür "
               "(çevirici testi: bizim yüklediğimiz 8 konuda yazı + etiket birebir). Yazım birebir olmayabilir (Markdown **kalın** → [B])."]
    if q["kucuk"]: kontrol.append(f"⚠ **Küçük yazı:** en küçük {q['min_px']} px, {q['kucuk']} yerde 13 px altı (Flarum'da [SIZE=n] = n piksel).")
    if kr and kr[0]: kontrol.append(f"⚠ **Kırık resim:** {kr[0]}/{kr[1]} (404) — yeni resim gerekir (Resimler sekmesinde işaretli).")
    if not q["renkli"] and not q["ortali"]: kontrol.append("Sade: renk / ortalama yok (eski tarz).")
    if not m0["butunluk"]: kontrol.append("⚠ **Çeviri kontrolü tutmadı** — forumdaki ile karşılaştır.")
    if k["mesaj_sayisi"] > 1: kontrol.append(f"Konuda {k['mesaj_sayisi'] - 1} cevap daha var (forumda) — burada sadece konu mesajı.")
    md = FA.md(h, {u: {"dosya": u} for u in srcs})
    onz = h.replace("<img ", '<img loading="lazy" ')               # 8 Eki: 38 konunun 100+ forum resmi acilista yukleniyordu, olu linkler sayfayi 30 sn+ bekletti
    return {"baslik": k["baslik"], "bbcode": m0["bbcode"], "html": onz, "markdown": md, "duz": duz(h), "resimler": res, "kontrol": kontrol,
            "bolum": [], "kaynak": k["url"]}


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
    for k in konular:
        P = f"f{k['id']}"; Y = veri(k); VERI[P] = Y
        b = kalip.replace('id="k_mining"', f'id="k_{P}"').replace('id="m', f'id="{P}').replace('data-p="m', f'data-p="{P}')
        b = re.sub(r"<h2>.*?</h2>", f"<h2>📜 {html.escape(k['baslik'])} — forum.sexyko.com/d/{k['id']}</h2>", b, count=1)
        kr = k.get("kirik_resim")
        adim = (f"<li>Forumdaki konunun <b>kendi BBCode'u</b> ({k['mesajlar'][0]['uzunluk']:,} karakter) — yapıştırınca forumda aynı görünür.</li>".replace(",", ".")
                + f"<li><b>🖼 Resimler</b> forumdaki linkleriyle ({len(Y['resimler'])})" + (f" — <b>⚠ {kr[0]} kırık (404)</b>" if kr and kr[0] else "") + ".</li>"
                + f"<li>forum.sexyko.com/d/{k['id']} → <b>Düzenle</b> → <b>BBCode kopyala</b> → yapıştır.</li>")
        b = re.sub(r'(<ol class="adim">).*?(</ol>)', lambda m: m.group(1) + adim + m.group(2), b, count=1, flags=re.S)
        b = re.sub(r'<div class="alt">Bilgi:.*?</div>', f'<div class="alt">Bilgi: <b>forum.sexyko.com/d/{k["id"]}</b> · {html.escape(k["yazar"])} · açılış {k["acilis"][:10]} · '
                   f'{k["mesaj_sayisi"]} mesaj → <b>⚠ Kontrol</b>.</div>', b, count=1)
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
    etiket = (f'    <div class="fkb">📜 Forumdaki konular — forum.sexyko.com ({len(konular)} konu · BBCode forumdan · ⚠ = küçük yazı / kırık resim)</div>\n')
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

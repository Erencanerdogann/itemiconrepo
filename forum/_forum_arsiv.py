# -*- coding: utf-8 -*-
# FORUM ARSIVI — forum.sexyko.com'da bir ETIKETIN butun konulari -> FORUM/rehber/forum_<etiket>/ (her konu: ham API, okunur Markdown, HTML, resimler)
# PATRON 8 Eki: "forum.sexyko.com/t/sexyko-oyun-rehberi bu sekmeye gir, butun icerigi sexyko rehberine klasorumuze kaydet, bilgili olalim,
#   resimleri vs her seyi cek, mutlaka repoya al. hem GM'lik yapiyoruz hem materyal toplamis oluyoruz. full butun sekmelere gir cik"
#   + "en son bbcode kotu olanlari not al, hangisini yapalimin listesi de ciksin".
# Kaynak: Flarum herkese acik API (salt okuma). Ham BBCode anonim API'de YOK -> kalite contentHtml'den olculur.
# Kullanim: python _forum_arsiv.py [etiket-slug]   (varsayilan sexyko-oyun-rehberi)
import sys, os, re, json, html, hashlib, time, io, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

KOK = os.path.dirname(os.path.abspath(__file__))
API = "https://forum.sexyko.com/api"
ETIKET = next((a for a in sys.argv[1:] if not a.startswith("--")), "sexyko-oyun-rehberi")
OUT = os.path.join(KOK, "rehber", "forum_oyun_rehberi" if ETIKET == "sexyko-oyun-rehberi" else "forum_" + ETIKET)
UA = {"User-Agent": "Mozilla/5.0 (SexyKO GM forum arsivi)"}
BIZIM = {56: "Skill & Master (6 Eki, bizim janr)"}            # bizim yeniden yaptigimiz (bu etiket icinde)
TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def al(url, deneme=3):
    for i in range(deneme):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40)
            return r.status, r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            return e.code, "", b""
        except Exception as e:
            if i == deneme - 1: return -1, repr(e)[:80], b""
            time.sleep(2 * (i + 1))


def jget(yol):
    s, _, b = al(API + yol); assert s == 200, (yol, s)
    return json.loads(b.decode("utf-8"))


def sayfali(yol):
    """Flarum sayfalama (links.next) -> data + included birlesik."""
    data, inc, url = [], [], API + yol
    while url:
        s, _, b = al(url); assert s == 200, (url, s); j = json.loads(b.decode("utf-8"))
        data += j.get("data", []); inc += j.get("included", []); url = (j.get("links") or {}).get("next")
    return data, inc


def guvenli(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9-]", "-", s.translate(TR).lower())).strip("-")[:60]


def md(h, resim):
    """contentHtml -> okunur Markdown (resimler yerel dosyaya)."""
    def img(m):
        src = html.unescape(m.group(1)); alt = html.unescape((re.search(r'alt="([^"]*)"', m.group(0)) or [None, ""])[1])
        r = resim.get(src)
        return f"\n\n![{alt}]({r['dosya']})\n" if r and r.get("dosya") else f"\n\n![{alt} — KIRIK ({r['durum'] if r else '?'})]({src})\n"
    t = re.sub(r'<img[^>]*\bsrc="([^"]+)"[^>]*>', img, h)
    t = re.sub(r'<iframe[^>]*\bsrc="([^"]+)"[^>]*>.*?</iframe>', lambda m: f"\n[video]({html.unescape(m.group(1))})\n", t, flags=re.S)
    for n in range(6, 0, -1): t = re.sub(rf"<h{n}[^>]*>(.*?)</h{n}>", lambda m, n=n: f"\n\n{'#' * n} {m.group(1)}\n\n", t, flags=re.S)
    t = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", t, flags=re.S); t = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", t, flags=re.S)
    t = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f"[{m.group(2)}]({html.unescape(m.group(1))})", t, flags=re.S)
    t = re.sub(r"<li[^>]*>", "\n- ", t); t = re.sub(r"<hr\s*/?>", "\n\n---\n\n", t); t = re.sub(r"<br\s*/?>", "  \n", t)
    t = re.sub(r"<blockquote[^>]*>", "\n> ", t); t = re.sub(r"</(p|div|ul|ol|blockquote)>", "\n\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+\n", "\n", t)).strip()


def kalite(h, resim_listesi):
    """contentHtml olcumu -> metrik + sorun bayraklari (patron: 'bbcode kotu olanlari not al')."""
    duz = html.unescape(re.sub(r"<[^>]+>", " ", h))
    fs = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", h)]
    ham_bb = re.findall(r"\[/?(?:b|i|u|s|size|color|center|right|left|url|img|list|quote|code|spoiler)(?:=[^\]]*)?\]", duz, re.I)
    md_k = len(re.findall(r"\*\*|__", duz))
    kirik = [r for r in resim_listesi if not r.get("dosya")]
    m = {"karakter": len(re.sub(r"\s+", " ", duz).strip()), "resim": len(resim_listesi), "kirik_resim": len(kirik),
         "baslik": len(re.findall(r"<h[1-4]", h)), "font_px_min": min(fs) if fs else None, "font_px_kucuk": sum(1 for x in fs if x < 13),
         "renk": len(re.findall(r"color:", h)), "ham_bbcode": len(ham_bb), "ham_ornek": ham_bb[:5], "md_kalinti": md_k, "hizali": len(re.findall(r"text-align:\s*center", h))}
    s = []
    if m["font_px_min"] is not None and m["font_px_min"] < 12: s.append(f"KÜÇÜK YAZI (min {m['font_px_min']:g} px, {m['font_px_kucuk']} alan <13 px — Flarum SIZE=piksel)")
    if kirik: s.append(f"KIRIK RESİM {len(kirik)}/{len(resim_listesi)}")
    if m["ham_bbcode"]: s.append(f"HAM BBCODE GÖRÜNÜYOR ({m['ham_bbcode']}: {', '.join(ham_bb[:3])})")
    if md_k: s.append(f"MARKDOWN KALINTISI ({md_k} '**'/'__')")
    if not resim_listesi and m["karakter"] > 1200: s.append("RESİMSİZ UZUN METİN")
    if m["baslik"] == 0 and m["karakter"] > 800: s.append("BAŞLIKSIZ (bölüm yok)")
    if not m["renk"] and not m["hizali"]: s.append("SADE (renk / ortalama yok — eski janr)")
    return m, s


def main():
    os.makedirs(OUT, exist_ok=True)
    disk, inc = sayfali(f"/discussions?filter%5Btag%5D={urllib.parse.quote(ETIKET)}&page%5Blimit%5D=50&include=tags,user")
    etiket = {x["id"]: x["attributes"]["name"] for x in inc if x["type"] == "tags"}
    kisi = {x["id"]: x["attributes"].get("displayName") or x["attributes"].get("username") for x in inc if x["type"] == "users"}
    ozet = []
    for d in sorted(disk, key=lambda x: int(x["id"])):
        did = int(d["id"]); a = d["attributes"]; rel = d.get("relationships", {})
        klasor = os.path.join(OUT, f"d{did:03d}-{guvenli(a['slug'])}"); os.makedirs(os.path.join(klasor, "resim"), exist_ok=True)
        posts, pinc = sayfali(f"/posts?filter%5Bdiscussion%5D={did}&page%5Blimit%5D=50&include=user")
        pk = {x["id"]: x["attributes"].get("displayName") or x["attributes"].get("username") for x in pinc if x["type"] == "users"}
        posts = sorted([p for p in posts if p["attributes"].get("contentType") == "comment"], key=lambda p: p["attributes"]["number"])
        resim = {}; parcalar = []; olc = []
        for p in posts:
            h = p["attributes"].get("contentHtml") or ""
            srcs = [html.unescape(s) for s in re.findall(r'<img[^>]*\bsrc="([^"]+)"', h)]
            for src in srcs:
                if src in resim: continue
                s, ct, b = al(src); kayit = {"url": src, "durum": s}
                if s == 200 and b:
                    try:
                        with Image.open(io.BytesIO(b)) as im: kayit["boyut"] = f"{im.width}x{im.height}"; fmt = (im.format or "png").lower()
                        ext = {"jpeg": "jpg"}.get(fmt, fmt); ad = f"{len(resim) + 1:02d}_{hashlib.md5(b).hexdigest()[:8]}.{ext}"
                        open(os.path.join(klasor, "resim", ad), "wb").write(b); kayit.update(dosya=f"resim/{ad}", bayt=len(b))
                    except Exception as e: kayit["durum"] = f"resim değil ({repr(e)[:40]})"
                resim[src] = kayit
            plist = [resim[s] for s in dict.fromkeys(srcs)]
            m, sorun = kalite(h, plist); olc.append((m, sorun))
            yazar = pk.get(((p.get("relationships") or {}).get("user") or {}).get("data", {}).get("id")) or "?"
            parcalar.append(f"## Mesaj {p['attributes']['number']} — {yazar} — {p['attributes']['createdAt'][:16].replace('T', ' ')}"
                            + (f" (düzenleme {p['attributes']['editedAt'][:10]})" if p['attributes'].get('editedAt') else "") + "\n\n" + md(h, resim))
        ets = [etiket.get(t["id"], t["id"]) for t in (rel.get("tags") or {}).get("data", [])]
        bas = (f"# {a['title']}\n\n- Forum: https://forum.sexyko.com/d/{did}\n- Etiket: {', '.join(ets)}\n- Açılış: {a['createdAt'][:10]} · "
               f"yazar {kisi.get(((rel.get('user') or {}).get('data') or {}).get('id'), '?')} · mesaj {len(posts)} · görüntülenme {a.get('viewCount', '?')}\n"
               f"- Arşiv: 8 Eki 2026 (Flarum API) · resim {sum(1 for r in resim.values() if r.get('dosya'))}/{len(resim)}\n\n")
        open(os.path.join(klasor, "konu.md"), "w", encoding="utf-8").write(bas + "\n\n".join(parcalar) + "\n")
        open(os.path.join(klasor, "icerik.html"), "w", encoding="utf-8").write("\n<hr>\n".join(p["attributes"].get("contentHtml") or "" for p in posts))
        json.dump({"discussion": d, "posts": posts, "resim": list(resim.values())}, open(os.path.join(klasor, "ham.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        m0, s0 = olc[0] if olc else ({}, [])
        ozet.append({"id": did, "baslik": a["title"], "klasor": os.path.basename(klasor), "tarih": a["createdAt"][:10], "mesaj": len(posts), "goruntulenme": a.get("viewCount"),
                     "resim": len(resim), "kirik": sum(1 for r in resim.values() if not r.get("dosya")), "metrik": m0, "sorun": s0, "bizim": BIZIM.get(did)})
        print(f"d{did:>3} {a['title'][:52]:52} resim {ozet[-1]['resim'] - ozet[-1]['kirik']}/{ozet[-1]['resim']}  {'; '.join(s0)[:90]}")
    json.dump(ozet, open(os.path.join(OUT, "ozet.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("KONU", len(ozet), "· resim", sum(x["resim"] for x in ozet), "· kirik", sum(x["kirik"] for x in ozet))


# --- yeniden yapma onceligi (patron 8 Eki: "hangisini yapalimin listesi de ciksin") — sira + sebep (olcum + sistemin onemi)
ONCELIK = [(12, "Yazılar 8 px (Flarum SIZE hatası, 17 alan <13 px) — okunmuyor; 11 resim sağlam → hemen yeniden yapılabilir"),
           (16, "4/4 resim kırık (hizliresim 404) — yeni oyun ekran görüntüsü gerekir (Genie penceresi; Noisee GM ile çekilebilir)"),
           (10, "Temel sistem (kırdırma) — başlıksız tek blok; resimler sağlam"),
           (26, "Upgrade oranları — oyuncunun en çok baktığı veri; admin verisiyle tablo / görsel yapılabilir"),
           (36, "Clan Grade — 2.168 karakter başlıksız tek blok"),
           (11, "Party sistemi — başlıksız; resimler sağlam"),
           (27, "Power Up Store — yeni PUS İndirim Kodu konusuyla aynı görsel dil"),
           (24, "Auto Mining / Mining Inn — madencilik verimiz hazır (24 saat + Auto Mining)")]


def index_yaz(ozet):
    o = {x["id"]: x for x in ozet}
    sat = "\n".join(f"| [d/{x['id']}](https://forum.sexyko.com/d/{x['id']}) | [{x['baslik']}]({x['klasor']}/konu.md) | {x['tarih']} | {x['resim'] - x['kirik']}/{x['resim']} | "
                    f"{(x['metrik'].get('font_px_min') or '—')} | {x['bizim'] or ('; '.join(x['sorun']) or '—')} |" for x in ozet)
    kotu = [x for x in ozet if any(s.startswith(("KÜÇÜK", "KIRIK", "HAM BBCODE", "MARKDOWN")) for s in x["sorun"])]
    duzensiz = [x for x in ozet if not x["bizim"] and any(s.startswith("BAŞLIKSIZ") for s in x["sorun"])]
    sade = [x for x in ozet if not x["bizim"] and x not in kotu and x not in duzensiz]
    t = (f"# Forum arşivi — SexyKO Oyun Rehberi (forum.sexyko.com/t/sexyko-oyun-rehberi)\n\n"
         f"> 8 Eki 2026, Flarum herkese açık API. Patron: \"bütün içeriği rehber klasörümüze kaydet, bilgili olalım, resimleri çek, repoya al\" + \"bbcode kötü olanları not al, hangisini yapalımın listesi çıksın\".\n"
         f"> Üretici: `FORUM/_forum_arsiv.py` (tekrar çalıştırınca günceller) · her konu klasöründe `konu.md` (okunur) · `icerik.html` · `ham.json` · `resim/`.\n\n"
         f"**{len(ozet)} konu · {sum(x['resim'] for x in ozet)} resim ({sum(x['kirik'] for x in ozet)} kırık)**\n\n"
         "## Konular\n\n| Forum | Başlık | Açılış | Resim | min px | Durum |\n|---|---|---|---|---|---|\n" + sat + "\n\n"
         "## 🔴 BBCode / görünüm KÖTÜ olanlar\n\n" + "\n".join(f"- **d/{x['id']} {x['baslik']}** — {'; '.join(s for s in x['sorun'] if s.startswith(('KÜÇÜK', 'KIRIK', 'HAM', 'MARKDOWN')))}" for x in kotu) +
         "\n\n## 🟠 Düzensiz (başlıksız tek blok)\n\n" + "\n".join(f"- d/{x['id']} {x['baslik']} — {x['metrik']['karakter']:,} karakter".replace(",", ".") for x in duzensiz) +
         f"\n\n## 🟡 Sade (okunur ama eski janr — renk / görsel kart yok): {len(sade)} konu\n\n" + " · ".join(f"d/{x['id']}" for x in sade) +
         "\n\n## ✅ Hangisini yeniden yapalım (öneri sırası)\n\n| Sıra | Konu | Sebep |\n|---|---|---|\n" +
         "\n".join(f"| {i} | d/{d} {o[d]['baslik']} | {s} |" for i, (d, s) in enumerate(ONCELIK, 1) if d in o) +
         f"\n\nSonra: kalan {len(sade) - sum(1 for d, _ in ONCELIK if d in {x['id'] for x in sade})} sade konu aynı kalıpla (`_<konu>_veri/_gorsel/_konu.py` + `_sekme_ekle.py`).\n"
         "Zaten bizim janrda: d/56 Skill & Master (bu etikette) · etiket dışı: d/54 Ödüller, d/55 TeamSpeak, d/57 Sezon, d/51 PUS kupon, d/37 Yayıncı.\n")
    open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8").write(t)
    print("INDEX.md:", len(ozet), "konu ·", len(kotu), "kötü ·", len(duzensiz), "düzensiz ·", len(sade), "sade")


if __name__ == "__main__":
    if "--index" in sys.argv: index_yaz(json.load(open(os.path.join(OUT, "ozet.json"), encoding="utf-8")))
    else:
        main(); index_yaz(json.load(open(os.path.join(OUT, "ozet.json"), encoding="utf-8")))

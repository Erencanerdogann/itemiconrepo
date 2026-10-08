# -*- coding: utf-8 -*-
# FORUM BBCODE ARSIVI (patron 8 Eki: "kanka sen butun konularin bbcode'sini cikart. html'de dursunlar.")
# forum.sexyko.com'daki BUTUN konular (herkese acik, tum etiketler) -> her mesajin BBCode'u (_bbcode_cevir: forum HTML'i -> BBCode, testli).
# CIKTI: FORUM/forum_bbcode/ (konu basina dNNN-slug.txt + bbcode.json) · HTML/FORUM_BBCODE.html (arama, etiket suzgeci, kopyala dugmesi)
# Her mesajda butunluk: yazi (bosluksuz) + resim sayisi + link sayisi forum HTML'i ile ayni mi -> sayfada / ciktida.
# Calistir: python _forum_bbcode.py   (tekrar calistirmak = guncelle)
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, datetime, urllib.request, urllib.error
import _forum_arsiv as FA
import _bbcode_cevir as BC

KOK = FA.KOK
OUT = os.path.join(KOK, "forum_bbcode")
SAYFA = os.path.join(os.path.dirname(KOK), "HTML", "FORUM_BBCODE.html")
os.makedirs(OUT, exist_ok=True)


def tarih(s): return (s or "")[:16].replace("T", " ")


def butunluk(h, bb):
    """forum HTML'i ile BBCode ayni icerigi mi tasiyor: (yazi, resim, link) esit mi."""
    hy = re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<img[^>]*?alt=\"([^\"]*)\"[^>]*class=\"[^\"]*emoji[^\"]*\"[^>]*>|<img[^>]*class=\"[^\"]*emoji[^\"]*\"[^>]*alt=\"([^\"]*)\"[^>]*>",
                                                                                        lambda m: m.group(1) or m.group(2) or "", h))))
    b = re.sub(r"\[IMG\].*?\[/IMG\]", "", bb, flags=re.S)
    b = re.sub(r"^#{1,6} |^---$|\[\*\]|`", "", b, flags=re.M)
    by = BC.kanonik(b)[0]
    r_html = len(re.findall(r"<img(?![^>]*emoji)", h)); r_bb = bb.count("[IMG]")
    l_html = len(re.findall(r"<a\s", h)); l_bb = len(re.findall(r"\[URL[\]=]", bb))
    return hy == by and r_html == r_bb and l_html == l_bb, {"yazi": [len(hy), len(by)], "resim": [r_html, r_bb], "link": [l_html, l_bb]}


def kalite(h):
    px = [int(x) for x in re.findall(r"font-size:\s*(\d+)px", h)]
    kucuk = sum(1 for x in px if x < 13)
    return {"min_px": min(px) if px else None, "kucuk": kucuk, "renkli": "color:" in h, "ortali": "text-align:center" in h}


def main():
    ds, inc = FA.sayfali("/discussions?include=tags,user&page[limit]=50&sort=createdAt")
    etiket = {x["id"]: x["attributes"] for x in inc if x["type"] == "tags"}
    kisi = {x["id"]: x["attributes"].get("displayName") or x["attributes"].get("username") for x in inc if x["type"] == "users"}
    # kirik resim CANLI yoklanir (8 Eki: arsivdeki bilgi bayatliyordu — d/16 yeniden yuklenmisti)
    durum = {}
    def resim_var(u):
        if u not in durum:
            s = -1
            for yontem in ("HEAD", "GET"):
                try:
                    s = urllib.request.urlopen(urllib.request.Request(u, headers=FA.UA, method=yontem), timeout=30).status
                except urllib.error.HTTPError as e: s = e.code
                except Exception: s = -1
                if s == 200 or s == 404: break
            durum[u] = s
        return durum[u] == 200
    konular, bilinmeyen, bozuk = [], set(), []
    for d in ds:
        a = d["attributes"]; did = int(d["id"])
        et = [etiket[t["id"]]["name"] for t in (d.get("relationships", {}).get("tags", {}).get("data") or []) if t["id"] in etiket]
        ps, pinc = FA.sayfali(f"/posts?filter[discussion]={did}&page[limit]=50&include=user")
        pk = {x["id"]: x["attributes"].get("displayName") or x["attributes"].get("username") for x in pinc if x["type"] == "users"}
        ps = sorted([p for p in ps if p["attributes"].get("contentType") == "comment" and p["attributes"].get("contentHtml") is not None], key=lambda p: p["attributes"]["number"])
        mesajlar, kal = [], {"min_px": None, "kucuk": 0, "renkli": False, "ortali": False}
        for p in ps:
            pa = p["attributes"]; h = pa["contentHtml"]
            bb, bil = BC.cevir(h); bilinmeyen |= set(bil)
            ok, olc = butunluk(h, bb)
            if not ok: bozuk.append((did, pa["number"], olc))
            k = kalite(h)
            kal["min_px"] = k["min_px"] if kal["min_px"] is None else (min(kal["min_px"], k["min_px"]) if k["min_px"] is not None else kal["min_px"])
            kal["kucuk"] += k["kucuk"]; kal["renkli"] |= k["renkli"]; kal["ortali"] |= k["ortali"]
            uid = ((p.get("relationships", {}).get("user") or {}).get("data") or {}).get("id")
            mesajlar.append({"no": pa["number"], "yazar": pk.get(uid, "?"), "tarih": tarih(pa.get("createdAt")), "duzenleme": tarih(pa.get("editedAt")),
                             "bbcode": bb, "uzunluk": len(bb), "butunluk": ok, "olcum": olc, "html": h})   # html: FORUM_KONU.html onizlemesi (_forum_sekme.py)
        uid = ((d.get("relationships", {}).get("user") or {}).get("data") or {}).get("id")
        srcs = [u for m in mesajlar for u in re.findall(r"\[IMG\](.*?)\[/IMG\]", m["bbcode"])]
        kr = (sum(1 for u in srcs if not resim_var(u)), len(srcs)) if srcs else None
        konular.append({"id": did, "baslik": a["title"], "slug": a.get("slug", ""), "url": f"https://forum.sexyko.com/d/{did}", "etiketler": et,
                        "acilis": tarih(a.get("createdAt")), "yazar": kisi.get(uid, "?"), "mesaj_sayisi": len(mesajlar), "mesajlar": mesajlar,
                        "kalite": kal, "kirik_resim": list(kr) if kr else None, "kirik_url": [u for u in srcs if not resim_var(u)]})
        dosya = f"d{did:03d}-{FA.guvenli(a.get('slug') or a['title'])[:60]}.txt"
        nl = chr(10)
        govde = (nl + nl).join((f"===== MESAJ #{m['no']} — {m['yazar']} — {m['tarih']} =====" + nl + nl if len(mesajlar) > 1 else "") + m["bbcode"] for m in mesajlar)
        open(os.path.join(OUT, dosya), "w", encoding="utf-8").write(a["title"] + nl + nl + govde + nl)
        print(f"d/{did:<3} {len(mesajlar)} mesaj · {sum(m['uzunluk'] for m in mesajlar):>6} karakter · {'✅' if all(m['butunluk'] for m in mesajlar) else '❌'} · {a['title'][:50]}")
    zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    VERI = {"zaman": zaman, "konu": len(konular), "mesaj": sum(k["mesaj_sayisi"] for k in konular), "konular": konular,
            "bilinmeyen_etiket": sorted(bilinmeyen), "bozuk": len(bozuk)}
    json.dump(VERI, open(os.path.join(OUT, "bbcode.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sablon = open(os.path.join(KOK, "_forum_bbcode_sablon.html"), encoding="utf-8").read()
    SAYFA_V = dict(VERI, konular=[dict(k, mesajlar=[{x: y for x, y in m.items() if x != "html"} for m in k["mesajlar"]]) for k in konular])   # bu sayfada html gerekmez
    veri_js = json.dumps(SAYFA_V, ensure_ascii=False).replace("</", "<\\/")
    assert sablon.count("/*VERI*/null") == 1
    open(SAYFA, "w", encoding="utf-8").write(sablon.replace("/*VERI*/null", veri_js))
    print(f"\nkonu {VERI['konu']} · mesaj {VERI['mesaj']} · butunluk bozuk {len(bozuk)} · bilinmeyen etiket {sorted(bilinmeyen) or 'yok'} · sayfa {os.path.getsize(SAYFA) // 1024} KB")
    for b in bozuk[:8]: print("   bozuk:", b)
    return 1 if bozuk else 0


if __name__ == "__main__":
    sys.exit(main())

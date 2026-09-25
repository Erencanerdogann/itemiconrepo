# -*- coding: utf-8 -*-
"""SexyKO ikon seti: admin ItemIcon numarasi -> repoda yoksa sexyko.com herkese acik rehber ikonu indirilir.
Formul (olculdu 25 Eyl): ItemIcon 38901700 -> /assets/itemicon/itemicon_3_8901_70_0.png (1|4|2|1 hane).
Sirali, yavas (0,4 sn), her dosya PIL ile dogrulanir; bulunamayanlar eksik.json'a. Tekrar calistirilirsa inenleri atlar."""
import os, json, time, io, urllib.request
from PIL import Image
KOK = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(KOK)
ADMIN = r"C:\temp\Sexyko\ADMIN_PANEL\VERI\sexyko_admin_veri_tam.json"
IKON = os.path.join(KOK, "ikon"); os.makedirs(IKON, exist_ok=True)

def url(n): return f"https://sexyko.com/assets/itemicon/itemicon_{n[0]}_{n[1:5]}_{n[5:7]}_{n[7]}.png"

def main():
    repo = {f[:-4] for f in os.listdir(os.path.join(REPO, "itemicon")) if f.endswith(".jpg")}
    V = json.load(open(ADMIN, encoding="utf-8"))["veri"]
    tum = set()
    for k, v in V.items():
        if k.startswith("items:c"):
            for pg in v:
                for r in pg["rows"]:
                    i = str(r["c"].get("ItemIcon") or "")
                    if len(i) == 8 and i.isdigit(): tum.add(i)
    eks = sorted(tum - repo); inen, yok = 0, []
    print(f"toplam ikon {len(tum)} | repoda {len(tum & repo)} | indirilecek {len(eks)}", flush=True)
    for j, n in enumerate(eks, 1):
        yol = os.path.join(IKON, n + ".png")
        if os.path.exists(yol): inen += 1; continue
        try:
            r = urllib.request.urlopen(urllib.request.Request(url(n), headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
            b = r.read(); Image.open(io.BytesIO(b)).verify()          # 404 HTML'i ikon sanma
            open(yol, "wb").write(b); inen += 1
        except Exception as e:
            yok.append({"ikon": n, "url": url(n), "hata": str(e)[:80]})
        if j % 25 == 0: print(f"{j}/{len(eks)} indi {inen} yok {len(yok)}", flush=True)
        time.sleep(0.4)
    json.dump(yok, open(os.path.join(KOK, "eksik.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"BITTI: indi {inen} / {len(eks)}, sitede de yok {len(yok)}", flush=True)

if __name__ == "__main__": main()

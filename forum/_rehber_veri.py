# -*- coding: utf-8 -*-
# Rehber ham JSON (rehber/web/*.json) -> okunur veri MD'leri (rehber/veri/<bolum>.md) + rehber/veri/INDEX.md
# Kural: her kaydin metninden footer ("Bizi Takip Et" sonrasi) ve bolum icinde kayitlarin yarisindan fazlasinda tekrar eden satirlar (liste/menu) atilir.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, json, glob, collections, re

KOK = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(KOK, "rehber", "web"); OUT = os.path.join(KOK, "rehber", "veri")
os.makedirs(OUT, exist_ok=True)
RES = json.load(open(os.path.join(WEB, "resimler.json"), encoding="utf-8")) if os.path.exists(os.path.join(WEB, "resimler.json")) else {}
AD = {"book": "Rehber (kitap) sayfaları", "monsters": "Monster listesi", "monsters_detay": "Monster detayları (spawn + drop %)",
      "quests": "Görev listesi", "quests_detay": "Görev detayları (NPC, şart, ödül)", "upgrade": "Upgrade oranları",
      "drops": "Drop arama", "fragment": "Gem & Fragment kırdırma", "cross-exchange": "Çapraz takas", "shozin": "Shozin karışımı",
      "narki": "Narki kırdırma", "pus-crash": "PUS kırdırma", "mining-fishing": "Madencilik & balıkçılık",
      "daily-quests": "Günlük görevler", "event-rewards": "Etkinlik ödülleri", "beginner-items": "Başlangıç eşyaları"}


def temiz(t):
    i = t.find("Bizi Takip Et")
    return t[:i] if i > 0 else t


ozet = []
for f in sorted(glob.glob(os.path.join(WEB, "*.json"))):
    b = os.path.basename(f)[:-5]
    if b in ("resimler",):
        continue
    d = json.load(open(f, encoding="utf-8")); K = d.get("kayitlar", [])
    if not K:
        continue
    # ortak ONEK: tum kayitlarin basinda birebir ayni olan satirlar (sol liste / menu) -> bir kez yazilir, kayitlardan atilir.
    # (eski kural 'yarisindan fazlasinda gecen satiri at' secimli bolumlerde detay basligini da siliyordu — 3 Eki duzeltildi)
    satlar = [[l.strip() for l in temiz(k.get("metin", "")).splitlines() if l.strip()] for k in K if "hata" not in k]

    def onek_bul(ss):
        n = 0
        if len(ss) >= 2:
            while all(len(s) > n for s in ss) and len({s[n] for s in ss}) == 1:
                n += 1
        return n
    onek = onek_bul(satlar)
    # alt secimli bolum (shozin: tur -> tarif): ayni turun kayitlari kendi listesini tasir -> grup ici onek de atilir
    grup = collections.defaultdict(list)
    for k in K:
        if "hata" not in k and "__" in k["ad"]:
            grup[k["ad"].split("__")[0]].append(k)
    grup_onek = {}
    for g, ks in grup.items():
        ss = [[l.strip() for l in temiz(x["metin"]).splitlines() if l.strip()][onek:] for x in ks]
        grup_onek[g] = onek_bul(ss) if len(ss) >= 2 else 0
    sat = [f"# {AD.get(b, b)}", "", f"Kaynak: {d.get('kaynak')} · sunucu: {d.get('sunucu')} · çekildi: {d.get('tarih')} · {len(K)} kayıt", ""]
    if onek:
        sat += ["## Ortak liste / menü (her kaydın başında aynı)", "", " · ".join(satlar[0][:onek])[:20000], ""]
    toplam_resim = set()
    for k in K:
        if "hata" in k:
            sat += [f"## {k['ad']}", "", f"HATA: {k['hata']}", ""]; continue
        satirlar = [l.strip() for l in temiz(k["metin"]).splitlines() if l.strip()][onek:]
        if "__" in k["ad"]:
            satirlar = satirlar[grup_onek.get(k["ad"].split("__")[0], 0):]
        rs = [RES.get(r) for r in k.get("resimler", []) if RES.get(r)]
        toplam_resim.update(rs)
        sat += [f"## {k['ad']}", "", " / ".join(satirlar), ""]
        if rs:
            sat += ["Resimler: " + " ".join(f"`{r}`" for r in rs[:60]) + (f" … (+{len(rs) - 60})" if len(rs) > 60 else ""), ""]
    open(os.path.join(OUT, f"{b}.md"), "w", encoding="utf-8").write("\n".join(sat))
    ozet.append((b, len(K), len(toplam_resim), os.path.getsize(os.path.join(OUT, f"{b}.md"))))
    print(f"{b:16s} {len(K):5d} kayıt · {len(toplam_resim):4d} resim · {os.path.getsize(os.path.join(OUT, f'{b}.md')) // 1024} KB")

idx = ["# Rehber verisi — INDEX", "", "sexyko.com/guide (oyundaki Rehber penceresinin kaynağı) · sunucu Hyper (12) · `python FORUM/_guide_cek.py` + `python FORUM/_rehber_veri.py`", "",
       "| Bölüm | Dosya | Kayıt | Resim | Boyut |", "|---|---|---|---|---|"]
for b, n, r, s in ozet:
    idx.append(f"| {AD.get(b, b)} | [{b}.md]({b}.md) | {n} | {r} | {s // 1024} KB |")
open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
print("INDEX yazildi")

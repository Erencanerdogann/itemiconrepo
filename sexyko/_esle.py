# -*- coding: utf-8 -*-
"""SexyKO item kodu -> ikon eslemesi (item_ikon.json). Kaynak: SexyKO admin paneli item listesi (ItemIcon alani).
Cikti: {"ikon": {ItemIcon: dosya_yolu_ya_da_null}, "item": {Num: [ad, tip, ItemIcon]}, "ozet": {...}}"""
import os, json, time
KOK = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(KOK)
ADMIN = r"C:\temp\Sexyko\ADMIN_PANEL\VERI\sexyko_admin_veri_tam.json"

def main():
    V = json.load(open(ADMIN, encoding="utf-8"))["veri"]
    item = {}
    for k, v in V.items():
        if k.startswith("items:c"):
            for pg in v:
                for r in pg["rows"]:
                    c = r["c"]; item[str(c["Num"])] = [c.get("strName"), c.get("ItemType"), str(c.get("ItemIcon") or "")]
    ikon = {}
    for _, _, n in item.values():
        if not n or n in ikon: continue
        if os.path.exists(os.path.join(REPO, "itemicon", n + ".jpg")): ikon[n] = f"itemicon/{n}.jpg"
        elif os.path.exists(os.path.join(KOK, "ikon", n + ".png")): ikon[n] = f"sexyko/ikon/{n}.png"
        else: ikon[n] = None
    kap = sum(1 for _, _, n in item.values() if ikon.get(n))
    ozet = {"tarih": time.strftime("%Y-%m-%d %H:%M"), "item": len(item), "ikon_numarasi": len(ikon),
            "ikon_var": sum(1 for x in ikon.values() if x), "ikonu_olan_item": kap, "kapsama_yuzde": round(100 * kap / max(1, len(item)), 2)}
    json.dump({"ozet": ozet, "ikon": ikon, "item": item}, open(os.path.join(KOK, "item_ikon.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(json.dumps(ozet, ensure_ascii=False))

if __name__ == "__main__": main()

# SexyKO ikon seti

SexyKO item kodları bizimkinden farklı, ama **ikon numaraları ortak**: SexyKO admin panelindeki her item kaydında
`ItemIcon` alanı var (örnek: Stiletto(+9) → `11051000`) ve bu numara bu repodaki `itemicon/<numara>.jpg` ile aynı.

| Dosya | İçerik |
|---|---|
| `item_ikon.json` | `item`: SexyKO item kodu → [ad, tip, ikon numarası] · `ikon`: ikon numarası → dosya yolu (`itemicon/…jpg`, `sexyko/ikon/…png` ya da `null`) · `ozet` |
| `ikon/<numara>.png` | Repoda olmayan ikonlar — sexyko.com herkese açık rehberinden indirildi |
| `eksik.json` | Sitede de bulunamayan ikon numaraları |
| `_indir.py` / `_esle.py` | Eksik ikonları indirir / eşlemeyi yeniden üretir |

**Site ikon adresi (ölçüldü 25 Eyl 2026):** `ItemIcon 38901700` → `https://sexyko.com/assets/itemicon/itemicon_3_8901_70_0.png`
(numara 1 | 4 | 2 | 1 hane bölünür).

Kullanım (Noisee GM): panel `/itemikon/<numara>` → önce `itemicon/<n>.jpg`, yoksa `sexyko/ikon/<n>.png`.
Yeniden üretmek: `python sexyko/_indir.py` (sadece eksikleri indirir) → `python sexyko/_esle.py`.

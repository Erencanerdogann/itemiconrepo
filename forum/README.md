# SexyKO — Forum konu kiti + resimler

Forum sitelerine açılan SexyKO konularının **tamamı**: konu kiti sayfası, BBCode / Markdown / düz metinler ve **bütün resimler**.
Resimler buradan (GitHub → jsDelivr CDN) çekilir. Her forumda aynı link açılır, resmi tek tek yüklemeye gerek kalmaz.

## Resim linki

```
https://cdn.jsdelivr.net/gh/Erencanerdogann/itemiconrepo@main/forum/<yol>
örnek: https://cdn.jsdelivr.net/gh/Erencanerdogann/itemiconrepo@main/forum/yeni_konu/resim/R02_rehber.jpg
```

Yedek (GitHub'ın kendi linki): `https://raw.githubusercontent.com/Erencanerdogann/itemiconrepo/main/forum/<yol>`

Aynı adla güncellenen resim jsDelivr'de 12 saate kadar eski görünebilir. Hemen yenilemek için şu adresi açın:
`https://purge.jsdelivr.net/gh/Erencanerdogann/itemiconrepo@main/forum/<yol>`

## İçerik

| Yol | Ne |
|---|---|
| `FORUM_KONU.html` | Konu kiti: sekmeler (Tanıtım · Uzun rehber · Kısa rehber · ⚔️ Skill & Master), BBCode / Markdown / Görünüm kopyala; resim linkleri hazır |
| `SEXYKO_TANITIM_*` | Tanıtım konusu (BBCode, Markdown, düz; `_orijinal` = Ko-Yardım'daki ilk hal) |
| `resim/` | Tanıtım resimleri (geri sayım GIF, logo, StoneSoft, Hyper ödül havuzu, takvim GIF) |
| `yeni_konu/` | Uzun "SexyKO Oyun Rehberi" konusu: metinler, `resim/` (R.. oyun içi + F.. forum.sexyko.com görselleri), parça / uzun JPG |
| `yeni_konu/kisa/` | Kısa sürüm: metinler, `resim/` (küçük resimler), giydirme |
| `skill_master/` | ⚔️ Skill & Master konusu: metinler, `resim/` (S00–S09), `SKILL_MASTER.md` (kaynak / doğrulama notları), `veri/` |
| `_*.py`, `_konu_sablon.html` | Üretici kit (kaynak: `C:\temp\Sexyko\FORUM\`) |
| `FORUM_LINKLERI.md` | Konu açtığımız forumlar |

## Güncelleme (kaynak: `C:\temp\Sexyko\FORUM\`)

```bash
cd /c/temp/Sexyko/FORUM
python _yeni_konu.py && python _kisa_konu.py && python _skill_konu.py && python _konu_kit.py   # FORUM_KONU.html
python _repo_aktar.py      # -> C:\temp\itemiconrepo\forum\ (doğrulama + gizli bilgi taraması; hata varsa çıkış 1)
cd /c/temp/itemiconrepo && git add forum && git commit -m "..." && git push
```

Bu repo **herkese açık**. Şunlar bilerek dışarıda bırakılır: ham site kopyası (`rehber/`), forumlardan çekilmiş sayfa HTML'leri (`kaynak/`), iç ajan talimatı, admin betikleri ve admin durum dosyası.

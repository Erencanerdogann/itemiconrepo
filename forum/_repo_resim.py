# FORUM RESIMLERI -> itemiconrepo (patron 7 Eki: "FORUM_KONU.html'i C:\temp\itemiconrepo'ya koyalim, repoyu push edelim,
# forum resimleri buradan ceksin — butun sitelerdeki resim sorunumuz kalkar").
# Her resmin varsayilan_url'si = repodaki kopyasi (jsDelivr CDN, GitHub herkese acik repo). Yerel yol "FORUM/<x>" -> repo "forum/<x>".
# Dosyasi olmayan (eskiden Ko-Yardim ek linki) resimler yerel kopyaya baglanir (FORUM/resim/ — _konu_kit.py indirir).
# Resim degisirse: ayni ad -> jsDelivr @main 12 saate kadar eskiyi gosterebilir -> https://purge.jsdelivr.net/gh/<REPO>@main/forum/<yol>
import os, hashlib
from urllib.parse import quote

REPO = "Erencanerdogann/itemiconrepo"
DAL = "main"
TABAN = f"https://cdn.jsdelivr.net/gh/{REPO}@{DAL}/forum/"
REPO_KLASOR = r"C:\temp\itemiconrepo"
KOK = os.path.dirname(os.path.abspath(__file__))          # C:\temp\Sexyko\FORUM
DOSYASIZ = {"GSAYIM": "FORUM/resim/1_geri_sayim.gif", "GTAKVIM": "FORUM/resim/5_takvim.gif", "R01": "FORUM/resim/2_logo.png"}


def rel(dosya):
    """'FORUM/yeni_konu/resim/R02.jpg' -> 'yeni_konu/resim/R02.jpg' (repoda forum/ altindaki yol)."""
    assert dosya.startswith("FORUM/"), dosya
    return dosya[len("FORUM/"):]


def surumlu(dosya):
    """7 Eki: 'skill_master/resim/S00_yol_haritasi.jpg' -> 'skill_master/resim/S00_yol_haritasi.c8f2a003.jpg' (icerik md5 ilk 8).
    jsDelivr @main ayni adli dosyayi gunlerce eski gosterdi (S00 / S06: 2 purge + ?v= ise yaramadi) -> icerik degisince LINK degisir, bayat kalamaz."""
    r = rel(dosya); b, e = os.path.splitext(r)
    return f"{b}.{hashlib.md5(open(yerel(dosya), 'rb').read()).hexdigest()[:8]}{e}"


def url(dosya):
    return TABAN + "/".join(quote(p) for p in surumlu(dosya).split("/"))


def yerel(dosya):
    return os.path.join(KOK, *rel(dosya).split("/"))


def uygula(res):
    """Uretici resim listesi (her biri {id, varsayilan_url, dosya, ...}) -> varsayilan_url = repo linki. Eski link 'eski_url'de kalir."""
    for d in res:
        dosya = d.get("dosya") or DOSYASIZ.get(d["id"])
        if not dosya:
            continue
        assert os.path.exists(yerel(dosya)), yerel(dosya)
        d["eski_url"] = d.get("varsayilan_url") or ""
        d["varsayilan_url"] = url(dosya)
        d["repo"] = "forum/" + surumlu(dosya); d["repo_kaynak"] = dosya          # _repo_aktar.py ozetli kopyayi buradan yazar
    return res

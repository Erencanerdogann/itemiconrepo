# FORUM -> C:\temp\itemiconrepo\forum\ (HERKESE ACIK GitHub repo — patron 7 Eki: "forum repoyu olustur, her sey olsun icinde").
# Forum kiti + FORUM_KONU.html + butun resimler + metinler. Disarida: ham site kopyasi (rehber/ 649 MB), cekilmis sayfa HTML'leri
# (kaynak/ — oturum token'i tasiyabilir), ic ajan talimati, admin betikleri / durum dosyasi, gecici dosya.
# SILME YOK: hedefte kaynakta olmayan dosya kalir (rapor edilir). Calistir: python _repo_aktar.py  (once uretici zinciri)
import os, re, json, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _repo_resim as RR

KOK = RR.KOK
HEDEF = os.path.join(RR.REPO_KLASOR, "forum")
HTML = os.path.join(os.path.dirname(KOK), "HTML", "FORUM_KONU.html")
DISLA_KLASOR = {"rehber", "kaynak", "__pycache__"}
# .gitignore: Sexyko'nunku /resim/'i disliyor -> repoda resimler commit disi kaliyordu (7 Eki)
DISLA_DOSYA = {".gitignore", "AJAN_KOYARDIM_GOREV.md", "_skill_rehber_admin.py", "_skill_rehber_taslak.py", "_renk_aday.png",
               "skill_master/admin_state.json", "skill_master/REHBER_SAYFA_TASLAK.md"}
GIZLI = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|xf_session|xf_csrf|_xfToken|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[=:]|"
                   r"password\s*[=:]\s*\S|parola\s*[=:]\s*\S|@gmail\.com|@hotmail\.com|sa_password", re.I)

kopya = []
for d, alt, dosyalar in os.walk(KOK):
    r = os.path.relpath(d, KOK).replace(os.sep, "/")
    # 8 Eki PATRON "forum oyun rehberi arsivini repoya mutlaka al": rehber/ icinden SADECE forum_oyun_rehberi/ (ham site kopyasi 649 MB yine disarida)
    alt[:] = [a for a in alt if not (r == "." and a in DISLA_KLASOR and a != "rehber") and not (r == "rehber" and a != "forum_oyun_rehberi") and a != "__pycache__"]
    if r == "rehber": dosyalar = []                                   # rehber/ kok dosyalari (rehber beyni, cekilmis sayfalar) repoya gitmez
    for f in dosyalar:
        rel = f if r == "." else f"{r}/{f}"
        if rel in DISLA_DOSYA or f.endswith(".pyc"): continue
        kopya.append((os.path.join(d, f), os.path.join(HEDEF, *rel.split("/")), rel))
kopya.append((HTML, os.path.join(HEDEF, "FORUM_KONU.html"), "FORUM_KONU.html"))
# 7 Eki: konularin kullandigi her resmin ICERIK OZETLI kopyasi (link bu ada gider; eski adli dosya da kalir, eski forum linkleri bozulmaz)
KONULAR = ["konu.json", "yeni_konu/konu.json", "yeni_konu/kisa/konu.json", "skill_master/konu.json", "odul/konu.json", "sezon/konu.json", "mining/konu.json", "genie/konu.json", "yayinci/konu.json", "pus_kupon/konu.json", "teamspeak/konu.json"]
_ozet = {}
for k in KONULAR:
    for x in json.load(open(os.path.join(KOK, *k.split("/")), encoding="utf-8"))["resimler"]:
        if x.get("repo") and x.get("repo_kaynak"): _ozet[x["repo"][len("forum/"):]] = RR.yerel(x["repo_kaynak"])
for rel_, kay_ in sorted(_ozet.items()):
    kopya.append((kay_, os.path.join(HEDEF, *rel_.split("/")), rel_))

boyut = 0
for kay, hed, rel in kopya:
    os.makedirs(os.path.dirname(hed), exist_ok=True)
    if not os.path.exists(hed) or os.path.getsize(hed) != os.path.getsize(kay) or open(hed, "rb").read() != open(kay, "rb").read():
        shutil.copy2(kay, hed)
    boyut += os.path.getsize(kay)

# dogrulama: ad + boyut birebir; uretici zincirinin kullandigi BUTUN resimler hedefte
hata = [rel for kay, hed, rel in kopya if not os.path.exists(hed) or os.path.getsize(hed) != os.path.getsize(kay)]
kullanilan = set()
for k in KONULAR:
    for x in json.load(open(os.path.join(KOK, *k.split("/")), encoding="utf-8"))["resimler"]:
        if x.get("repo"): kullanilan.add(x["repo"])
eksik = [x for x in kullanilan if not os.path.exists(os.path.join(RR.REPO_KLASOR, *x.split("/")))]
import subprocess                                                     # kullanilan resim repoda git'ce yok sayiliyorsa push'a girmez -> hata
yok_sayilan = subprocess.run(["git", "check-ignore", "--stdin"], input=chr(10).join(sorted(kullanilan)), capture_output=True, text=True,
                             cwd=RR.REPO_KLASOR).stdout.split()
eksik += [f"git yok sayiyor: {x}" for x in yok_sayilan]
sizinti = [x for x in DISLA_DOSYA | DISLA_KLASOR if os.path.exists(os.path.join(HEDEF, *x.split("/")))   # dislanan hedefe sizdiysa HATA
           and not (x == "rehber" and set(os.listdir(os.path.join(HEDEF, "rehber"))) <= {"forum_oyun_rehberi"})]   # 8 Eki: rehber/'den yalniz forum arsivi serbest
eksik += [f"dislanan hedefte: {x}" for x in sizinti]
gizli = []
for kay, hed, rel in kopya:
    if rel.lower().endswith((".py", ".md", ".txt", ".json", ".html")) and rel != "_repo_aktar.py":   # tarayicinin kendi kalibi haric
        t = open(hed, encoding="utf-8", errors="replace").read()
        if rel == "FORUM_KONU.html": t = re.sub(r"data:image/[^\"']+", "", t)
        m = GIZLI.search(t)
        if m: gizli.append((rel, m.group(0)[:40]))
fazla = []
for d, alt, dosyalar in os.walk(HEDEF):
    for f in dosyalar:
        rel = os.path.relpath(os.path.join(d, f), HEDEF).replace(os.sep, "/")
        if rel != "README.md" and rel not in {k[2] for k in kopya}: fazla.append(rel)
print(f"dosya {len(kopya)} · {boyut / 1048576:.1f} MB · ad+boyut hatasi {len(hata)} · kullanilan resim {len(kullanilan)} eksik {len(eksik)} · "
      f"gizli bilgi {len(gizli)} · hedefte fazla (silinmedi) {len(fazla)}")
for x in hata[:5] + eksik[:5] + gizli[:5] + fazla[:5]: print("  ", x)
sys.exit(1 if hata or eksik or gizli else 0)

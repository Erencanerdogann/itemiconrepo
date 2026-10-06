# -*- coding: utf-8 -*-
# SexyKO FORUM REHBERI CEK (patron 3 Eki: "oyunu ogren ... hepsini md'ye yaz") — SADECE OKUMA (Flarum public API)
# Kaynak: forum.sexyko.com etiket "sexyko-oyun-rehberi" + Ko-Yardim konusundaki 34 forum linki (kaynak/linkler.json)
# Cikti: rehber/forum/ham/<id>.json (API ham) · rehber/forum/<id>.md (metin) · rehber/forum/resim/<id>_<n>.<uzanti> · rehber/forum/liste.json
import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, re, json, html, time, requests

KOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KOK, "rehber", "forum")
for d in ("ham", "resim"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
API = "https://forum.sexyko.com/api"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36", "Accept": "application/vnd.api+json"}
HR = {"User-Agent": H["User-Agent"]}


def al(url, **kw):
    for dene in range(4):
        r = requests.get(url, headers=H, timeout=40, **kw)
        if r.status_code == 429:
            time.sleep(5 * (dene + 1)); continue
        r.raise_for_status(); return r.json()
    raise RuntimeError("429: " + url)


# 1) etiket listesi + Ko-Yardim linkleri
ids, etiket = [], {}
url = f"{API}/discussions?page[limit]=50&sort=createdAt"          # patron "tam veri": forumdaki TUM konular (etiket filtresi yok)
while url:
    d = al(url)
    for x in d["data"]:
        ids.append(int(x["id"]))
    url = d.get("links", {}).get("next")
LINK = json.load(open(os.path.join(KOK, "kaynak", "linkler.json"), encoding="utf-8"))["linkler"]
ky = []
for u, t in LINK:
    m = re.search(r"forum\.sexyko\.com/d/(\d+)", u)
    if m:
        ky.append(int(m.group(1)))
print("etiket:", len(ids), "· Ko-Yardim linki:", len(ky), "· etikette olmayan:", sorted(set(ky) - set(ids)))
tum = list(dict.fromkeys(ids + ky))


def md_cevir(h):
    s = h
    s = re.sub(r"<img [^>]*src=\"([^\"]+)\"[^>]*alt=\"([^\"]*)\"[^>]*>", lambda m: f"\n![{m.group(2)}]({m.group(1)})\n", s)
    s = re.sub(r"<img [^>]*src=\"([^\"]+)\"[^>]*>", lambda m: f"\n![]({m.group(1)})\n", s)
    s = re.sub(r"<h(\d)[^>]*>(.*?)</h\1>", lambda m: "\n" + "#" * (int(m.group(1)) + 1) + " " + m.group(2) + "\n", s, flags=re.S)
    s = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", s, flags=re.S)
    s = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", s, flags=re.S)
    s = re.sub(r"<a [^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<li>", "- ", s)
    s = re.sub(r"<hr\s*/?>", "\n---\n", s)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</(p|li|ul|ol|tr|blockquote|div)>", "\n", s)
    s = re.sub(r"<t[dh][^>]*>", " | ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


liste = []
for did in tum:
    d = al(f"{API}/discussions/{did}?include=posts,tags,user")
    json.dump(d, open(os.path.join(OUT, "ham", f"{did}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    a = d["data"]["attributes"]
    inc = {(x["type"], x["id"]): x for x in d.get("included", [])}
    posts = [x for x in d.get("included", []) if x["type"] == "posts" and x["attributes"].get("contentType") == "comment"]
    posts.sort(key=lambda x: x["attributes"]["number"])
    tags = [inc[("tags", t["id"])]["attributes"]["name"] for t in d["data"]["relationships"].get("tags", {}).get("data", []) if ("tags", t["id"]) in inc]
    ilk = posts[0]["attributes"]["contentHtml"] if posts else ""
    resimler = []
    for n, src in enumerate(re.findall(r"<img [^>]*src=\"([^\"]+)\"", ilk), 1):
        uz = (os.path.splitext(src.split("?")[0])[1] or ".png")[:5]
        yol = os.path.join(OUT, "resim", f"{did}_{n}{uz}")
        if not os.path.exists(yol):
            try:
                r = requests.get(src, headers=HR, timeout=60); r.raise_for_status()
                open(yol, "wb").write(r.content)
            except Exception as e:
                print("  resim indirilemedi:", did, n, src, e); yol = None
        resimler.append({"n": n, "url": src, "dosya": os.path.relpath(yol, KOK).replace("\\", "/") if yol else None})
    metin = md_cevir(ilk)
    for r_ in resimler:
        if r_["dosya"]:
            metin = metin.replace(f"]({r_['url']})", f"]({os.path.relpath(os.path.join(KOK, r_['dosya']), OUT).replace(chr(92), '/')})", 1)
    baslik = a["title"]
    open(os.path.join(OUT, f"{did}.md"), "w", encoding="utf-8").write(
        f"# {baslik}\n\nKaynak: https://forum.sexyko.com/d/{did} · etiket: {', '.join(tags)} · açılış {a['createdAt'][:10]} · yorum {a['commentCount']}\n\n{metin}\n")
    liste.append({"id": did, "baslik": baslik, "slug": a.get("slug"), "tarih": a["createdAt"][:10], "etiket": tags, "yorum": a["commentCount"],
                  "resim": len(resimler), "resim_ok": sum(1 for r_ in resimler if r_["dosya"]), "karakter": len(metin), "ko_yardim_linki": did in ky})
    print(f"{did:4d} {baslik[:60]:60s} resim {len(resimler)} · {len(metin)} kr")
    time.sleep(0.4)
json.dump(liste, open(os.path.join(OUT, "liste.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("toplam konu:", len(liste), "· resim:", sum(x["resim"] for x in liste), "· indirilen:", sum(x["resim_ok"] for x in liste))

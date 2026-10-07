# -*- coding: utf-8 -*-
# FORUM KONU BLOK CEVIRICI (7 Eki — Hyper Beta Odulleri konusu icin; _skill_konu.py ile ayni gorunum, ayni blok turleri).
# Blok listesi B -> BBCode / onizleme HTML / Markdown / duz metin. Renkler + satir() (kalin + [[url|metin]] link) + PX + font buyutme: _yeni_konu.py.
# Blok turleri: afis(id) · banner(id) · baslik(ust, alt) · icindekiler · ayrac · h(emoji, metin) · p(metin) · liste([metin]) · img(id, aciklama) ·
#               not(metin) · link(etiket, url) · son(metin) · satirlar([metin]) — maddesiz kisa satirlar (7 Eki: uzun liste satiri forumda kirilip karisiyordu)
import html, re
import _yeni_konu as Y

A, A2, G, YE, K, M = Y.ALTIN, Y.ALTIN2, Y.GRI, Y.YESIL, Y.KIRMIZI, Y.MAVI
PX = Y.PX
CIZGI = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sat = Y.satir


def basliklar(B):
    L = [(b[1], b[2]) for b in B if b[0] == "h"]
    return L, {x: f"{i:02d}" for i, x in enumerate(L, 1)}


def bb(B):
    L, NO = basliklar(B); o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"[CENTER][IMG]{{{{{b[1]}}}}}[/IMG][/CENTER]")
        elif k == "baslik": o.append(f"[CENTER][SIZE=7][B][COLOR={A}]{b[1]}[/COLOR][/B][/SIZE]\n[SIZE=4][COLOR={G}]{b[2]}[/COLOR][/SIZE][/CENTER]")
        elif k == "icindekiler": o.append(f"[CENTER][SIZE=5][B][COLOR={A}]📑 İÇİNDEKİLER[/COLOR][/B][/SIZE]\n[SIZE=4]" + "\n".join(f"[COLOR={A}]{NO[x]}[/COLOR] · {x[0]} {x[1]}" for x in L) + "[/SIZE][/CENTER]")
        elif k == "ayrac": o.append(f"[CENTER][COLOR={A}]{CIZGI}[/COLOR][/CENTER]")
        elif k == "h": o.append(f"[CENTER][SIZE=6][B][COLOR={A}]{b[1]} {NO[(b[1], b[2])]} · {b[2]}[/COLOR][/B][/SIZE][/CENTER]")
        elif k == "p": o.append(f"[SIZE=4]{sat(b[1], 'bb')}[/SIZE]")
        elif k == "liste": o.append("[SIZE=4]" + "\n".join(f"[COLOR={A}]◆[/COLOR] {sat(x, 'bb')}" for x in b[1]) + "[/SIZE]")
        elif k == "satirlar": o.append("[SIZE=4]" + "\n".join(sat(x, "bb") for x in b[1]) + "[/SIZE]")
        elif k == "img": o.append(f"[CENTER][IMG]{{{{{b[1]}}}}}[/IMG]" + (f"\n[SIZE=3][COLOR={G}]▲ {b[2]}[/COLOR][/SIZE]" if b[2] else "") + "[/CENTER]")
        elif k == "not": o.append(f"[SIZE=4][COLOR={YE}]💡 {sat(b[1], 'bb')}[/COLOR][/SIZE]")
        elif k == "link": o.append(f"[SIZE=4][URL={b[2]}][B][COLOR={M}]{b[1]} ↗[/COLOR][/B][/URL][/SIZE]")
        elif k == "son": o.append(f"[CENTER][SIZE=6][B][COLOR={K}]{b[1]}[/COLOR][/B][/SIZE][/CENTER]")
        else: raise ValueError(k)
    return Y.buyut_bb("\n\n".join(o))


def onizleme(B):
    L, NO = basliklar(B)
    c = lambda x: f'<div style="text-align:center">{x}</div>'
    sl = lambda x: f'<div style="text-align:left">{x}</div>'
    o = []
    for b in B:
        k = b[0]
        if k == "banner": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="" style="max-width:100%;width:520px">'))
        elif k == "afis": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="" style="max-width:100%">'))
        elif k == "baslik": o.append(c(f'<span style="font-size:{PX[7]}px;color:{A}"><b>{html.escape(b[1])}</b></span><br><span style="font-size:{PX[4]}px;color:{G}">{html.escape(b[2])}</span>'))
        elif k == "icindekiler": o.append(c(f'<span style="font-size:{PX[5]}px;color:{A}"><b>📑 İÇİNDEKİLER</b></span><br><span style="font-size:{PX[4]}px">'
                                           + "<br>".join(f'<span style="color:{A}">{NO[x]}</span> · {html.escape(x[0])} {html.escape(x[1])}' for x in L) + "</span>"))
        elif k == "ayrac": o.append(c(f'<span style="color:{A}">{CIZGI}</span>'))
        elif k == "h": o.append(c(f'<span style="font-size:{PX[6]}px;color:{A}"><b>{b[1]} {NO[(b[1], b[2])]} · {html.escape(b[2])}</b></span>'))
        elif k == "p": o.append(sl(f'<span style="font-size:{PX[4]}px">{sat(b[1], "html")}</span>'))
        elif k == "liste": o.append(sl(f'<span style="font-size:{PX[4]}px">' + "<br>".join(f'<span style="color:{A}">◆</span> {sat(x, "html")}' for x in b[1]) + "</span>"))
        elif k == "satirlar": o.append(sl(f'<span style="font-size:{PX[4]}px">' + "<br>".join(sat(x, "html") for x in b[1]) + "</span>"))
        elif k == "img": o.append(c(f'<img src="{{{{{b[1]}}}}}" alt="{html.escape(b[2])}" style="max-width:100%">'
                                    + (f'<br><span style="font-size:{PX[3]}px;color:{G}">▲ {html.escape(b[2])}</span>' if b[2] else "")))
        elif k == "not": o.append(sl(f'<span style="font-size:{PX[4]}px;color:{YE}">💡 {sat(b[1], "html")}</span>'))
        elif k == "link": o.append(sl(f'<a href="{html.escape(b[2])}" target="_blank" rel="noopener" style="font-size:{PX[4]}px;color:{M};font-weight:700;text-decoration:none">{html.escape(b[1])} ↗</a>'))
        elif k == "son": o.append(c(f'<span style="font-size:{PX[6]}px;color:{K}"><b>{html.escape(b[1])}</b></span>'))
    return Y.buyut_ht("<br>".join(o))


def md(B):
    L, NO = basliklar(B); o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"![]({{{{{b[1]}}}}})")
        elif k == "baslik": o.append(f"# {b[1]}\n\n*{b[2]}*")
        elif k == "icindekiler": o.append("## 📑 İçindekiler\n\n" + "\n".join(f"{NO[x]} · {x[0]} {x[1]}  " for x in L))
        elif k == "ayrac": o.append("---")
        elif k == "h": o.append(f"## {b[1]} {NO[(b[1], b[2])]} · {b[2]}")
        elif k in ("p", "not"): o.append(("💡 " if k == "not" else "") + sat(b[1], "md"))
        elif k == "liste": o.append("\n".join(f"- {sat(x, 'md')}" for x in b[1]))
        elif k == "satirlar": o.append("  \n".join(sat(x, "md") for x in b[1]))
        elif k == "img": o.append(f"![{b[2]}]({{{{{b[1]}}}}})" + (f"\n▲ *{b[2]}*" if b[2] else ""))
        elif k == "link": o.append(f"**[{b[1]} ↗]({b[2]})**")
        elif k == "son": o.append(f"**{b[1]}**")
    return "\n\n".join(o)


def duz(B, RES):
    L, NO = basliklar(B); o = []
    for b in B:
        k = b[0]
        if k in ("banner", "afis"): o.append(f"[RESİM {b[1]}]")
        elif k == "img": o.append(f"[RESİM {b[1]}: {b[2] or RES[b[1]][1]}]")
        elif k == "baslik": o.append(f"{b[1]}\n{b[2]}")
        elif k == "icindekiler": o.append("İÇİNDEKİLER\n" + "\n".join(f"{NO[x]} · {x[0]} {x[1]}" for x in L))
        elif k == "ayrac": o.append(CIZGI)
        elif k == "h": o.append(f"{b[1]} {NO[(b[1], b[2])]} · {b[2]}")
        elif k == "son": o.append(b[1])
        elif k in ("p", "not"): o.append(("💡 " if k == "not" else "") + sat(b[1], "duz"))
        elif k == "liste": o.append("\n".join(f"◆ {sat(x, 'duz')}" for x in b[1]))
        elif k == "satirlar": o.append("\n".join(sat(x, "duz") for x in b[1]))
        elif k == "link": o.append(f"{b[1]} → {b[2]}")
    return "\n\n".join(o)


def denetle(BB, RES):
    """Jeton = resim listesi; BBCode etiketleri dengeli."""
    jeton = set(re.findall(r"\{\{([A-Z][A-Za-z0-9_]*)\}\}", BB))
    assert jeton == set(RES), (jeton ^ set(RES))
    for a, z in [("[B]", "[/B]"), ("[CENTER]", "[/CENTER]"), ("[SIZE=", "[/SIZE]"), ("[COLOR=", "[/COLOR]"), ("[URL=", "[/URL]")]:
        assert BB.count(a) == BB.count(z), a

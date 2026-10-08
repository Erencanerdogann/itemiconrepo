# -*- coding: utf-8 -*-
# FORUM_KONU.html PREMIUM DUZEN (patron 8 Eki: "sekmeleri de kendi alanlarina gore html'i yeniden duzenle, premium bir sayfa olsun —
# hem rahat goreyim gezeyim hem de rahat rahat copy yapip edit yapayim").
# _konu_kit.py sayfayi yazmadan once cagirir: sab = uygula(sab). Eski sekme makinesi (kur / #ksec / .konu) AYNEN calisir; ustune:
#   sol menu (alanlara gore gruplu + arama + son acilan konu) · ustte yapiskan konu cubugu (alan > konu, onceki / sonraki) · yapiskan kopyala cubugu ·
#   BBCode sayfada DUZENLENIR (otomatik kayit localStorage, canli onizleme, "Orijinale don") — kopyala / gorunum / mesaj bolme duzenlenmis hali kullanir · telefonda acilir menu.
import re, json, html
import _forum_sekme as FS

# alanlar (forum etiketleri + Oyun Rehberi icin konu alani). Sayi = forum d/N; bizim sekmeler FS.BIZIM ile eslenir.
ALANLAR = [
    ("📣", "Tanıtım konuları", ["k_yeni", "k_kisa", "k_tanitim"]),
    ("🔥", "Yeni Sunucu HYPER", [54, 57, 53]),
    ("🎮", "Oyun Rehberi · Oyun Sistemleri", [16, 12, 14, 22, 38, 52, 24, 11, 33, 41, 45, 36]),
    ("⚔️", "Oyun Rehberi · Karakter & Skill", [56, 42, 49, 28, 46, 32, 31, 30]),
    ("🛡️", "Oyun Rehberi · Item & Upgrade", [26, 10, 43, 40, 29, 44, 39, 34, 50]),
    ("🛒", "Oyun Rehberi · Mağaza & Destek", [27, 13]),
    ("📢", "Duyurular", [3, 55, 58, 25, 15, 37, 51]),
    ("🛠️", "Destek & Client", [5, 9]),
    ("💬", "Genel / Topluluk", [35, 4, 48]),
]

CSS = r"""
/* ===== PREMIUM DUZEN (8 Eki) — sol menu + yapiskan cubuklar + duzenleme ===== */
body.premium{--yan:300px}
body.premium #ksec{display:none}
#yan{position:fixed;left:0;top:0;bottom:0;width:var(--yan);background:linear-gradient(180deg,#0f1634,#090d1d);border-right:1px solid var(--bor);display:flex;flex-direction:column;z-index:60}
#yan .marka{padding:16px 16px 6px;font-weight:800;font-size:17px;letter-spacing:.3px;color:var(--ana)}
#yan .marka small{display:block;font-weight:500;font-size:12px;color:var(--sol);letter-spacing:0;margin-top:2px}
#yan .ara{padding:8px 14px 10px}
#yan .ara input{width:100%;background:var(--kod);color:var(--txt);border:1px solid var(--bor);border-radius:10px;padding:9px 12px;font-size:14px;outline:none}
#yan .ara input:focus{border-color:var(--ana)}
#yan nav{overflow-y:auto;flex:1;padding:2px 8px 24px}
#yan details{margin:2px 0}
#yan summary{cursor:pointer;list-style:none;padding:9px 10px 5px;font-weight:700;font-size:12px;letter-spacing:.4px;color:var(--sol);display:flex;gap:6px;align-items:center;user-select:none}
#yan summary::-webkit-details-marker{display:none}
#yan summary::after{content:"▾";margin-left:auto;transition:transform .15s}
#yan details:not([open]) summary::after{transform:rotate(-90deg)}
#yan summary .s{background:var(--card2);color:var(--sol);border-radius:10px;padding:0 7px;font-size:11px;font-weight:600}
#yan .og{display:flex;gap:8px;align-items:center;width:100%;text-align:left;background:transparent;border:1px solid transparent;border-radius:9px;padding:7px 10px;margin:1px 0;font-size:14px;line-height:1.3;color:var(--txt)}
#yan .og:hover{background:var(--card2);border-color:var(--bor)}
#yan .og.on{background:var(--ana);color:#1b1400;font-weight:700;border-color:var(--ana)}
#yan .og .e{flex:none;width:20px;text-align:center}
#yan .og .a{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#yan .og .d{flex:none;font-size:11px;color:var(--sol)}
#yan .og.on .d{color:#4a3700}
#yan .og .k{display:none;flex:none;font-size:12px}
#yan .og.duz .k{display:inline}
#yan .bos{padding:16px;color:var(--sol);font-size:13px}
body.premium .kap{margin-left:var(--yan);max-width:none;padding:0 32px 70px}
body.premium .kap>*{max-width:1120px}
.ustc{position:sticky;top:0;z-index:40;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 0;margin:0 0 6px;background:var(--bg);border-bottom:1px solid var(--bor)}
.ustc .yol{flex:1;min-width:200px;font-size:14px;color:var(--sol);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ustc .yol b{color:var(--txt);font-size:16px}
.ustc button{padding:7px 12px;font-size:13px}
#yanac{display:none}
.konu .dug{position:sticky;top:58px;z-index:30;background:var(--card);padding:8px 0;margin:-6px 0 10px;border-bottom:1px solid var(--bor)}
.duzbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 8px;padding:8px 12px;border:1px dashed var(--bor);border-radius:8px;font-size:13px;color:var(--sol)}
.duzbar b{color:var(--txt)} .duzbar .dd{margin-left:auto;font-weight:700} .duzbar .dd.var{color:var(--ana)}
.duzbar button{padding:6px 10px;font-size:13px}
.duzbar button.emin{background:#c0392b;border-color:#c0392b;color:#fff}
.konu.duzenli .onz{outline:2px solid var(--ana);outline-offset:-2px}
.konu:not(#k_tanitim) .sek button[data-p$="bb"]::after{content:" ✏️"}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]) #yan{background:linear-gradient(180deg,#ffffff,#f3f4fa)}}
@media (max-width:900px){
  #yan{transform:translateX(-102%);transition:transform .2s;width:86vw;max-width:340px;box-shadow:0 0 40px rgba(0,0,0,.5)}
  body.yan-acik #yan{transform:none}
  body.premium .kap{margin-left:0;padding:0 12px 60px}
  #yanac{display:inline-flex}
  .ustc .yol{order:3;flex-basis:100%}
  .konu .dug{top:98px}
}
"""

JS_GLOBAL = r"""
// ===== DUZENLEME (8 Eki): BBCode sayfada duzenlenir, localStorage'a kaydedilir — kur() bb() once buraya bakar
var DUZ={k:"forum_duzen_v1",hepsi:function(){try{return JSON.parse(localStorage.getItem(this.k)||"{}");}catch(e){return {};}},
  oku:function(P){var h=this.hepsi();return Object.prototype.hasOwnProperty.call(h,P)?h[P]:null;},
  yaz:function(P,v){var h=this.hepsi();if(v==null)delete h[P];else h[P]=v;try{localStorage.setItem(this.k,JSON.stringify(h));}catch(e){}}};
function bb2html(s){
  var h=String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  var R=[[/\[B\]([\s\S]*?)\[\/B\]/gi,"<b>$1</b>"],[/\[I\]([\s\S]*?)\[\/I\]/gi,"<i>$1</i>"],[/\[U\]([\s\S]*?)\[\/U\]/gi,"<u>$1</u>"],[/\[S\]([\s\S]*?)\[\/S\]/gi,"<s>$1</s>"],
    [/\[SIZE=(\d+)\]([\s\S]*?)\[\/SIZE\]/gi,function(m,n,t){n=+n;return '<span style="font-size:'+(n<=7?SIZE_PX[n]:Math.min(Math.max(n,8),36))+'px">'+t+'</span>';}],
    [/\[COLOR=(#?[0-9a-zA-Z]+)\]([\s\S]*?)\[\/COLOR\]/gi,'<span style="color:$1">$2</span>'],
    [/\[CENTER\]([\s\S]*?)\[\/CENTER\]/gi,'<div style="text-align:center">$1</div>'],
    [/\[IMG\]([\s\S]*?)\[\/IMG\]/gi,'<img src="$1" alt="" loading="lazy" style="max-width:100%">'],
    [/\[URL=([^\]]+)\]([\s\S]*?)\[\/URL\]/gi,'<a href="$1" target="_blank" rel="noopener">$2</a>'],
    [/\[URL\]([\s\S]*?)\[\/URL\]/gi,'<a href="$1" target="_blank" rel="noopener">$1</a>'],
    [/\[QUOTE\]([\s\S]*?)\[\/QUOTE\]/gi,'<blockquote>$1</blockquote>'],[/\[CODE\]([\s\S]*?)\[\/CODE\]/gi,'<pre>$1</pre>'],
    [/\[LIST(=1)?\]([\s\S]*?)\[\/LIST\]/gi,function(m,o,t){var it=t.split(/\[\*\]/).slice(1).map(function(x){return "<li>"+x.trim()+"</li>";}).join("");return o?"<ol>"+it+"</ol>":"<ul>"+it+"</ul>";}]];
  for(var g=0;g<8;g++){var o=h;R.forEach(function(r){h=h.replace(r[0],r[1]);});if(o===h)break;}
  return h.replace(/\n/g,"<br>");
}
"""

JS_NAV = r"""
// ===== PREMIUM MENU (8 Eki) — alanlara gore gruplu sol menu, arama, son acilan konu, onceki / sonraki, telefonda acilir menu
(function(){
  var NAV=/*__NAV__*/null, SIRA=[], YER={};
  NAV.forEach(function(g){g.ogeler.forEach(function(o){YER[o.konu]={g:g,o:o};SIRA.push(o.konu);});});
  var yan=document.createElement("aside");yan.id="yan";
  yan.innerHTML='<div class="marka">🔥 SexyKO Forum Kiti<small>'+SIRA.length+' konu · alanlara göre</small></div><div class="ara"><input type="search" id="yanara" placeholder="🔍 Konu ara (başlık veya içerik)…" autocomplete="off"></div><nav id="yannav"></nav>';
  document.body.insertBefore(yan,document.body.firstChild);document.body.classList.add("premium");
  var es=function(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");};
  function metin(k){var K=KONU[k];if(K&&K.Y)return (K.Y.baslik+" "+K.Y.bbcode).toLocaleLowerCase("tr-TR");if(k==="k_tanitim")return (V.baslik+" "+V.bbcode).toLocaleLowerCase("tr-TR");return "";}
  function ciz(){var q=document.getElementById("yanara").value.trim().toLocaleLowerCase("tr-TR"),h="",n=0,ak=aktif();
    NAV.forEach(function(g){var L=g.ogeler.filter(function(o){return !q||o.ad.toLocaleLowerCase("tr-TR").indexOf(q)>=0||("d/"+o.d)===q||metin(o.konu).indexOf(q)>=0;});
      if(!L.length)return;n+=L.length;
      h+='<details open><summary>'+g.ikon+' '+es(g.ad)+' <span class="s">'+L.length+'</span></summary>'+L.map(function(o){
        return '<button type="button" class="og'+(o.konu===ak?" on":"")+(KONU[o.konu]&&KONU[o.konu].duzenli&&KONU[o.konu].duzenli()?" duz":"")+'" data-k="'+o.konu+'" title="'+es(o.tam)+'"><span class="e">'+o.ikon+'</span><span class="a">'+es(o.ad)+'</span><span class="k">✏️</span>'+(o.d?'<span class="d">d/'+o.d+'</span>':'')+'</button>';}).join("")+'</details>';});
    document.getElementById("yannav").innerHTML=h||'<div class="bos">Eşleşen konu yok.</div>';}
  function aktif(){var b=document.querySelector("#ksec button.on");return b?b.dataset.konu:SIRA[0];}
  var ust=document.createElement("div");ust.className="ustc";
  ust.innerHTML='<button type="button" id="yanac">☰ Konular</button><div class="yol" id="ustyol"></div><button type="button" id="onceki">◀ Önceki</button><button type="button" id="sonraki">Sonraki ▶</button>';
  var ks=document.getElementById("ksec");ks.parentNode.insertBefore(ust,ks.nextSibling);
  function ustCiz(){var k=aktif(),y=YER[k];if(!y)return;document.getElementById("ustyol").innerHTML=y.g.ikon+' '+es(y.g.ad)+' › <b>'+y.o.ikon+' '+es(y.o.ad)+'</b>'+(y.o.d?' <a href="https://forum.sexyko.com/d/'+y.o.d+'" target="_blank" rel="noopener" style="color:var(--info);font-size:13px">forumda aç ↗</a>':'');}
  window.konuAc=function(k,kaydir){var b=document.querySelector('#ksec button[data-konu="'+k+'"]');if(!b)return;b.click();
    try{localStorage.setItem("forum_son_konu_v1",k);}catch(e){}
    ciz();ustCiz();document.body.classList.remove("yan-acik");if(kaydir!==false)window.scrollTo({top:0});
    var on=document.querySelector('#yan .og.on');if(on&&on.scrollIntoView)on.scrollIntoView({block:"nearest"});};
  yan.addEventListener("click",function(e){var b=e.target.closest(".og");if(b)konuAc(b.dataset.k);});
  document.getElementById("yanara").addEventListener("input",ciz);
  document.getElementById("yanac").addEventListener("click",function(e){e.stopPropagation();document.body.classList.toggle("yan-acik");});
  document.addEventListener("click",function(e){if(document.body.classList.contains("yan-acik")&&!e.target.closest("#yan")&&!e.target.closest("#yanac"))document.body.classList.remove("yan-acik");});
  function git(d){var i=SIRA.indexOf(aktif());konuAc(SIRA[(i+d+SIRA.length)%SIRA.length]);}
  document.getElementById("onceki").addEventListener("click",function(){git(-1);});
  document.getElementById("sonraki").addEventListener("click",function(){git(1);});
  window.duzRozet=function(){ciz();Object.keys(KONU).forEach(function(k){var K=KONU[k],el=document.getElementById(k);if(!K||!el||!K.duzenli)return;var d=K.duzenli();el.classList.toggle("duzenli",d);
    var s=document.getElementById(K.P+"duz");if(s){s.textContent=d?"✏️ düzenlendi (kayıtlı)":"orijinal";s.classList.toggle("var",d);}});};
  document.addEventListener("click",function(e){var b=e.target.closest("[data-duz]");if(!b)return;var K=KONU[b.closest(".konu").id];if(!K)return;
    if(!b.classList.contains("emin")){b.classList.add("emin");b.dataset.eski=b.textContent;b.textContent="Emin misin? tekrar tıkla";setTimeout(function(){if(b.classList.contains("emin")){b.classList.remove("emin");b.textContent=b.dataset.eski;}},3000);return;}
    b.classList.remove("emin");b.textContent=b.dataset.eski;K.sifirla();duzRozet();toast("↺ orijinale döndü");});
  var son=null;try{son=localStorage.getItem("forum_son_konu_v1");}catch(e){}
  konuAc(son&&YER[son]?son:SIRA[0],false);duzRozet();
})();
"""


def uygula(sab):
    # --- menu verisi: sekme dugmeleri (ad) + alan listesi
    dug = dict(re.findall(r'<button type="button"(?: class="[^"]*")? data-konu="(k_\w+)"[^>]*>(.*?)</button>', sab))
    ad_temiz = lambda s: html.unescape(re.sub(r"\s*⚠\s*$", "", s)).strip()
    NAV, goruldu = [], set()
    for ikon, ad, L in ALANLAR:
        og = []
        for x in L:
            if isinstance(x, int): k = "k_" + FS.BIZIM[x] if x in FS.BIZIM else f"k_f{x}"; d = x
            else: k = x; d = None
            assert k in dug, f"sekme yok: {k}"
            assert k not in goruldu, f"iki alanda: {k}"; goruldu.add(k)
            tam = ad_temiz(dug[k]); e, a = FS_emoji(tam)
            og.append({"konu": k, "ad": a, "ikon": e or "📄", "d": d, "tam": tam})
        NAV.append({"ikon": ikon, "ad": ad, "ogeler": og})
    eksik = set(dug) - goruldu
    assert not eksik, f"menude olmayan sekme: {sorted(eksik)}"
    # --- kur(): duzenleme destegi (bb once DUZ'e bakar; onizleme / gorunum duzenlenmis BBCode'dan)
    R = [
        ('  function bb(){return renk(yjeton(Y.bbcode,url));}',
         '  function bbOrj(){return renk(yjeton(Y.bbcode,url));}\n  function bb(){var d=DUZ.oku(P);return d!=null?d:bbOrj();}\n'
         '  function onzCiz(){E("onzic").innerHTML=DUZ.oku(P)!=null?bb2html(bb()):htm(true);}'),
        ('  function guncel(){E("tbb").value=bb();', '  function guncel(){if(document.activeElement!==E("tbb"))E("tbb").value=bb();'),
        ('  E("onzic").innerHTML=htm(true);\n  E("rsl")', '  onzCiz();\n  E("rsl")'),
        ('function yenile(){E("onzic").innerHTML=htm(true);guncel();}', 'function yenile(){onzCiz();guncel();}'),
        ('function htmlKop(){var h=htm(false);', 'function htmlKop(){var h=DUZ.oku(P)!=null?bb2html(bb()):htm(false);'),
        ('  return {Y:Y,bb:bb,md:md,duz:duz,bol:bol,htmlKop:htmlKop,yenile:yenile};',
         '  (function(){var ta=E("tbb");if(!ta)return;ta.readOnly=false;ta.spellcheck=false;\n'
         '    ta.addEventListener("input",function(){DUZ.yaz(P,ta.value===bbOrj()?null:ta.value);onzCiz();guncel();if(window.duzRozet)duzRozet();});})();\n'
         '  return {Y:Y,P:P,bb:bb,md:md,duz:duz,bol:bol,htmlKop:htmlKop,yenile:yenile,duzenli:function(){return DUZ.oku(P)!=null;},sifirla:function(){DUZ.yaz(P,null);E("tbb").value=bbOrj();yenile();}};'),
        ('function kur(P,Y,LS){', JS_GLOBAL + 'function kur(P,Y,LS){'),
    ]
    for a, b in R:
        assert sab.count(a) == 1, "kalip: " + a[:60]
        sab = sab.replace(a, b)
    # --- BBCode panelleri: duzenleme cubugu + readonly kalkar (tanitim sekmesi haric — onun makinesi ayri)
    n = 0
    def bar(m):
        nonlocal n; n += 1; P = m.group(1)
        return (f'<div class="ypan" id="{P}bb"><div class="duzbar"><span>✏️ <b>Burada düzenleyebilirsin</b> — otomatik kaydedilir; BBCode kopyala / mesaj parçaları / önizleme / görünüm düzenlenmiş hali kullanır.</span>'
                f'<span class="dd" id="{P}duz">orijinal</span><button type="button" data-duz="sifirla">↺ Orijinale dön</button></div><textarea id="{P}tbb"></textarea></div>')
    sab = re.sub(r'<div class="ypan" id="(\w+)bb"><textarea id="\1tbb" readonly></textarea></div>', bar, sab)
    assert n == len(dug) - 1, (n, len(dug))                              # tanitim haric hepsi
    # --- CSS + menu JS
    sab = sab.replace("</style>", CSS + "</style>", 1)
    i = sab.rindex("</script>")
    sab = sab[:i] + JS_NAV.replace("/*__NAV__*/null", json.dumps(NAV, ensure_ascii=False)) + sab[i:]
    print(f"premium: {len(NAV)} alan · {sum(len(g['ogeler']) for g in NAV)} konu · düzenlenebilir BBCode paneli {n}")
    return sab


def FS_emoji(s):
    import _forum_yeniden as FY
    e, a = FY.emoji_ayir(s)
    return e, a

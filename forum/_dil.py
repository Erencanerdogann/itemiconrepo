# -*- coding: utf-8 -*-
# FORUM_KONU TR / EN — 13 Eki aksam PATRON: "ayri html yap gitsin" -> iki dosya: HTML/FORUM_KONU.html (TR) + HTML/FORUM_KONU_EN.html (EN).
#   (ilk hali 13 Eki gece: ayni sayfa + localStorage + reload dugmesi — patron "calismiyor" dedi -> kaldirildi; kosedeki TR / EN = obur dosyaya duz link)
# _konu_kit.py: _dil.uygula(sab, "tr" | "en") (premium'dan sonra) + "/*__VERI_EN__*/null" -> EN konu verisi (konu_en.json'lar).
# EN dosyasinda:
#   1) V[k] = V_EN[k] (cevrilmis konular) — kur() konuyu EN veriyle kurar; cevrilmemisler TR kalir + ust notu + menude "TR" etiketi
#   2) arayuz: _dil_en.py sozlugu (BLOK ic HTML -> KURAL kalip -> METIN dugum -> BASLIK konu adi); sonradan eklenen yazi (toast, menu) MutationObserver ile
#   3) localStorage: konuya bagli anahtarlar (duzenleme, kendi resim linki) EN'de "en:" on-ekli -> TR / EN duzenlemeleri karismaz
# TR modunda sayfa eskisi gibi (cevirici calismaz, V degismez).
import json, re
import _dil_en as D

ORTAK_ANAHTAR = ["forum_tur_v1", "forum_zemin_v1", "forum_son_konu_v1", "forum_konu_acildi_v1", "forum_dil_v1"]   # iki dilde ortak (gorunum / secim)
ICERIK = "textarea,script,style,.onz,pre,.rs,[id$=\"rsl\"],ul[id$=\"kl\"],#ftb,#dilsec"

CSS = """
#dilsec{position:fixed;top:10px;right:14px;z-index:9999;display:flex;gap:0;border:1px solid #6b5426;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.5)}
#dilsec a{background:#1d1712;color:#c9bca6;border:0;padding:6px 12px;font-weight:800;font-size:13px;cursor:pointer;letter-spacing:1px;text-decoration:none}
#dilsec a.on{background:#c8a253;color:#1b1400}
.cevrilmedi{margin:0 0 10px;padding:8px 12px;border-radius:8px;background:#2a1f12;border:1px dashed #c8a253;color:#e6c46a;font-size:13px}
html[lang=en] .tr-only::after{content:" · TR";font-size:10px;color:#c8a253;font-weight:800;margin-left:4px}
"""

ON_JS = """
var DIL=__DIL__;
var V_EN=/*__VERI_EN__*/null;
(function(){ if(DIL!=="en")return; document.documentElement.lang="en";
  var ORTAK=__ORTAK__, S=Storage.prototype, g=S.getItem, s=S.setItem, r=S.removeItem;
  function k(x){return ORTAK.indexOf(x)>=0?x:"en:"+x}
  S.getItem=function(x){return g.call(this,k(x))}; S.setItem=function(x,v){return s.call(this,k(x),v)}; S.removeItem=function(x){return r.call(this,k(x))};
})();
function DIL_V(T){ if(DIL!=="en"||!T||!V_EN) return T; for(var x in V_EN){ if(V_EN[x]){ T[x]=V_EN[x]; T[x]._en=1; } }
  if(V_EN.tanitim){ ["baslik","bbcode","html","markdown","duz","resimler"].forEach(function(f){ T[f]=V_EN.tanitim[f]; }); }   // 13 Eki: tanitim verisi sayfanin kokunde
  return T; }
"""

SON_JS = """
(function(){
  var kutu=document.createElement("div"); kutu.id="dilsec";
  kutu.innerHTML='<a href="FORUM_KONU.html" data-dil="tr">TR</a><a href="FORUM_KONU_EN.html" data-dil="en">EN</a>';
  document.body.appendChild(kutu);
  kutu.querySelectorAll("a").forEach(function(b){ if(b.getAttribute("data-dil")===DIL) b.classList.add("on"); });
  if(DIL!=="en") return;
  var BLOK=__BLOK__, METIN=__METIN__, BASLIK=__BASLIK__, BUYUK=__BUYUK__, UI=__UI__;
  var KURAL=__KURAL__.map(function(k){return [new RegExp(k[0]),k[1]]});
  var ICERIK='__ICERIK__';
  function norm(s){return s.replace(/\\s+/g," ").trim()}
  var EMO=/^((?:\\p{Extended_Pictographic}|\\uFE0F|\\u200D|\\s)*)(.*?)((?:\\s*⚠)?)$/u;
  function baslik(t){ if(BUYUK[t]) return BUYUK[t]; var m=t.match(EMO); if(!m) return null; var c=m[2];
    var e=BASLIK[c]||BUYUK[c]; return e?(m[1]+e+m[3]):null; }
  function kural(t){ for(var i=0;i<KURAL.length;i++){ var k=KURAL[i]; if(k[0].test(t)){
      return t.replace(k[0],k[1]).replace(/\\{T:([^}]*)\\}/g,function(_,x){return baslik(x)||x}); } } return null; }
  function cevir(t){ if(!t) return null; return METIN[t]||kural(t)||baslik(t)||null; }
  var SATIR={B:1,I:1,CODE:1,SPAN:1,BR:1,SMALL:1,EM:1,STRONG:1,U:1};
  function guvenli(e){ var a=e.querySelectorAll("*"); for(var i=0;i<a.length;i++){ var c=a[i]; if(!SATIR[c.tagName]) return false;
      for(var j=0;j<c.attributes.length;j++){ var n=c.attributes[j].name; if(n.indexOf("data-")===0||n==="id"||n.indexOf("on")===0) return false; } } return true; }
  function blok(kok){ var el=(kok.nodeType===1?[kok]:[]).concat([].slice.call((kok.querySelectorAll?kok:document).querySelectorAll("li,div,p,span,small,summary,h1,h2,h3,td,label")));
    el.forEach(function(e){ if(!e.firstElementChild||e.closest(ICERIK)||!guvenli(e)) return; var h=norm(e.innerHTML);
      var y=BLOK[h]; if(!y){ var kk=kural(h); if(kk&&kk!==h) y=kk; } if(y) e.innerHTML=y; }); }
  function metin(kok){ var w=document.createTreeWalker(kok,NodeFilter.SHOW_TEXT), n, L=[]; while(n=w.nextNode()) L.push(n);
    L.forEach(function(n){ var p=n.parentElement; if(!p||p.closest(ICERIK)) return; var v=n.nodeValue, t=norm(v); var y=cevir(t);
      if(y&&y!==t){ var b=v.match(/^\\s*/)[0], s=v.match(/\\s*$/)[0]; n.nodeValue=b+y+s; } });
    (kok.querySelectorAll?kok:document).querySelectorAll("[placeholder],[title]").forEach(function(e){ ["placeholder","title"].forEach(function(a){
      var v=e.getAttribute(a); var y=v&&cevir(norm(v)); if(y) e.setAttribute(a,y); }); }); }
  function hepsi(kok){ blok(kok); metin(kok); }
  // cevrilmemis konular: panel ustune not + menude TR etiketi
  document.querySelectorAll(".konu[id^='k_']").forEach(function(p){ var x=p.id.slice(2); if(V_EN&&V_EN[x]) return;
    var d=document.createElement("div"); d.className="cevrilmedi"; d.textContent=UI.cevrilmedi; p.insertBefore(d,p.firstChild);
    document.querySelectorAll('[data-konu="'+p.id+'"]').forEach(function(b){ b.classList.add("tr-only"); }); });
  document.title=UI.title;
  hepsi(document.body);
  var bekle=false, kuyruk=[];
  new MutationObserver(function(ms){ ms.forEach(function(m){ if(m.type==="characterData") kuyruk.push(m.target.parentNode); else m.addedNodes.forEach(function(n){ kuyruk.push(n.nodeType===3?n.parentNode:n); }); });
    if(!bekle){ bekle=true; requestAnimationFrame(function(){ var q=kuyruk; kuyruk=[]; bekle=false; q.forEach(function(k){ if(k&&k.nodeType===1&&document.body.contains(k)) hepsi(k); }); }); } })
    .observe(document.body,{childList:true,subtree:true,characterData:true});
})();
"""


def _js(o): return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")


def uygula(sab, dil):
    assert dil in ("tr", "en"), dil
    a = "var V=/*__VERI__*/null;"
    assert sab.count(a) == 1, "kalip: var V"
    i = sab.find(a); j = sab.rfind("<script", 0, i); assert j > 0
    on = "<script>" + ON_JS.replace("__ORTAK__", _js(ORTAK_ANAHTAR)).replace("__DIL__", _js(dil)) + "</script>\n"
    sab = sab[:j] + on + sab[j:]
    sab = sab.replace(a, "var V=DIL_V(/*__VERI__*/null);", 1)
    kural = [[re.sub(r"\(\?P<", "(?<", k), v] for k, v in D.KURAL]          # python regex -> JS (ayni sozdizimi)
    son = (SON_JS.replace("__BLOK__", _js(D.BLOK)).replace("__METIN__", _js(D.METIN)).replace("__BASLIK__", _js(D.BASLIK)).replace("__BUYUK__", _js(D.BUYUK))
           .replace("__UI__", _js(D.UI_EN)).replace("__KURAL__", _js(kural)).replace("__ICERIK__", ICERIK.replace("'", "\\'")))
    assert sab.count("</body>") == 1
    sab = sab.replace("</body>", "<script>" + son + "</script>\n</body>", 1).replace("</head>", "<style>" + CSS + "</style>\n</head>", 1)
    assert "/*__VERI_EN__*/null" in sab and "DIL_V(/*__VERI__*/null)" in sab
    return sab

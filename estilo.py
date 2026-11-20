# Estilo de marca de El Profe Trader (copiado de carruseles/semana1.py)
INK, PAPER, OCHRE, OCHRE_DARK, POS, NEG = "#1C2230", "#F2F3F0", "#C9861F", "#8F5A0E", "#2F7D5B", "#B5473A"

def logo(bowl):
    return f'''<svg width="64" height="64" viewBox="0 0 100 100">
      <rect x="31" y="6" width="3" height="16" fill="{OCHRE}"/>
      <rect x="25" y="22" width="15" height="58" rx="1.5" fill="{OCHRE}"/>
      <rect x="31" y="80" width="3" height="16" fill="{OCHRE}"/>
      <path d="M44 22 H58 A18 18 0 0 1 58 58 H44 V47 H58 A7 7 0 0 0 58 33 H44 Z" fill="{bowl}"/>
    </svg>'''

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=block');
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px}}
.s{{width:1080px;height:1350px;padding:88px 96px;display:flex;flex-direction:column;position:relative;overflow:hidden}}
.ink{{background:{INK};color:{PAPER}}} .paper{{background:{PAPER};color:{INK}}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.kick{{font:500 30px 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:{OCHRE}}}
.paper .kick{{color:{OCHRE_DARK}}}
.rule{{width:72px;height:4px;background:{OCHRE};margin-top:22px}}
.mid{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px}}
.bot{{display:flex;justify-content:space-between;align-items:center;font:500 28px 'IBM Plex Mono',monospace;opacity:.8}}
h1{{font:800 118px/1.02 'Archivo',sans-serif;letter-spacing:-.02em}}
h2{{font:800 84px/1.06 'Archivo',sans-serif;letter-spacing:-.015em}}
h1 em,h2 em{{font-style:normal;color:{OCHRE}}}
.paper h2 em{{color:{OCHRE_DARK}}}
.sub{{font:500 44px/1.35 'Inter',sans-serif;opacity:.85}}
p.b{{font:400 46px/1.4 'Inter',sans-serif}}
p.b b{{font-weight:600}}
ul{{list-style:none;display:flex;flex-direction:column;gap:30px}}
li{{font:400 44px/1.35 'Inter',sans-serif;display:grid;grid-template-columns:56px 1fr;align-items:start}}
li .m{{font:500 34px/1.45 'IBM Plex Mono',monospace;color:{OCHRE}}}
.paper li .m{{color:{OCHRE_DARK}}}
li .x{{color:{NEG}}}
.ink li .x{{color:#E07A6C}}
li b{{font-weight:600}}
.note{{font:500 28px/1.4 'IBM Plex Mono',monospace;opacity:.7}}
table{{border-collapse:collapse;width:100%;font:400 40px 'Inter',sans-serif}}
td,th{{padding:22px 10px;border-bottom:2px solid rgba(28,34,48,.15);text-align:left}}
th{{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;opacity:.6}}
td.k{{font:800 40px 'Archivo',sans-serif}}
td.v{{font:500 34px 'IBM Plex Mono',monospace;color:{OCHRE_DARK};white-space:nowrap}}
.box{{border:3px solid {OCHRE};border-radius:6px;padding:36px 40px;display:flex;flex-direction:column;gap:18px}}
.paper .box{{border-color:{OCHRE_DARK}}}
.cta{{font:800 76px/1.08 'Archivo',sans-serif}}
.cta em{{font-style:normal;color:{OCHRE}}}
.handle{{font:500 38px 'IBM Plex Mono',monospace;color:{OCHRE}}}
.legal{{font:400 26px/1.4 'Inter',sans-serif;opacity:.55}}
.swipe{{color:{OCHRE};opacity:1}}
.candles{{position:absolute;left:0;right:0;bottom:140px;height:200px;opacity:.22}}
.cover .mid{{padding-bottom:230px;justify-content:flex-end}}
"""

def candles():
    hs=[(60,110),(90,150),(70,120),(120,190),(100,150),(140,210),(110,170),(150,230),(130,180),(170,240),(150,200),(190,250),(160,215),(200,255)]
    out=[]; w=1080/len(hs)
    for i,(lo,hi) in enumerate(hs):
        x=i*w+w*0.3; bw=w*0.4; up = i%3!=2
        top=260-hi; bot=260-lo
        col = OCHRE if up else PAPER
        out.append(f'<rect x="{x+bw/2-2}" y="{top-18}" width="4" height="{bot-top+36}" fill="{col}"/><rect x="{x}" y="{top}" width="{bw}" height="{bot-top}" fill="{col}"/>')
    return '<svg class="candles" viewBox="0 0 1080 260" preserveAspectRatio="none">'+''.join(out)+'</svg>'

def slide(kind, bg, kicker, n, total, body):
    bowl = PAPER if bg == "ink" else INK
    right = '<span class="swipe">Deslizá →</span>' if kind == "cover" else f"{n:02d} / {total:02d}"
    deco = candles() if kind == 'cover' else ''
    return f'''<div class="s {bg} {kind}">{deco}
      <div class="top"><div><div class="kick">{kicker}</div><div class="rule"></div></div>{logo(bowl)}</div>
      <div class="mid">{body}</div>
      <div class="bot"><span>@elprofetrader</span><span>{right}</span></div>
    </div>'''

LEGAL = '<p class="legal">Contenido educativo. No es recomendación de inversión.</p>'

def ul(items, mark="—", cls="m"):
    return "<ul>" + "".join(f'<li><span class="{cls}">{mark}</span><span>{i}</span></li>' for i in items) + "</ul>"

def nums(items):
    return "<ul>" + "".join(f'<li><span class="m">{k+1:02d}</span><span>{i}</span></li>' for k, i in enumerate(items)) + "</ul>"


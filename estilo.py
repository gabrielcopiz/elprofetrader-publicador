# Estilo de marca de El Profe Trader: un color y un dibujo de portada por troncal.
# Lo usan semana1.py, semana2.py y (copiado como estilo.py) el publicador.
INK, PAPER, OCHRE, OCHRE_DARK, POS, NEG = "#1C2230", "#F2F3F0", "#C9861F", "#8F5A0E", "#2F7D5B", "#B5473A"

# (fondo fuerte, fondo claro, acento sobre fuerte, acento sobre claro, texto sobre claro, texto sobre fuerte)
# Criterios (20/11): 1) distinguir troncales en la grilla; 2) nada de verde "ganancia" ni rojo "pérdida"
# como color de troncal; 3) apoyarse en la historia del profe (pizarrón, conos, aula). Contraste medido 4,4 a 15,9.
TEMAS = {
    "base":    ("#1C2230", "#F2F3F0", "#C9861F", "#8F5A0E", "#1C2230", "#FFFFFF"),  # Presentación: tinta + ocre (logo)
    "cabeza":  ("#2B1E4F", "#F0EBFA", "#B9A2FF", "#5B3DB8", "#22183F", "#FFFFFF"),  # Cabeza: violeta, neutro en trading
    "tactica": ("#0E3B33", "#E9F1EC", "#F3E6A6", "#0E5A4A", "#1C2230", "#FFFFFF"),  # Táctica: pizarrón + tiza
    "pasos":   ("#8ECDF3", "#EEF7FD", "#1E3A8A", "#1E4FA0", "#1C2230", "#1C2230"),  # Primeros pasos: celeste del aula
    "entreno": ("#EA580C", "#FCEEE5", "#FFFFFF", "#B45309", "#1C2230", "#1C2230"),  # Entrenamiento: naranja cono
}

def tema(kicker):
    k = kicker.lower()
    if k.startswith("cabeza"): return "cabeza"
    if k.startswith("táctica") or k.startswith("tactica"): return "tactica"
    if k.startswith("primeros"): return "pasos"
    if k.startswith("entrenamiento"): return "entreno"
    return "base"

def logo():
    return '''<svg class="logo" width="64" height="64" viewBox="0 0 100 100">
      <rect class="lc" x="31" y="6" width="3" height="16"/>
      <rect class="lc" x="25" y="22" width="15" height="58" rx="1.5"/>
      <rect class="lc" x="31" y="80" width="3" height="16"/>
      <path class="lb" d="M44 22 H58 A18 18 0 0 1 58 58 H44 V47 H58 A7 7 0 0 0 58 33 H44 Z"/>
    </svg>'''

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=block');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
.s{width:1080px;height:1350px;padding:88px 96px;display:flex;flex-direction:column;position:relative;overflow:hidden}
.ink{background:var(--d);color:var(--td);--ac:var(--a)}
.paper{background:var(--l);color:var(--tx);--ac:var(--al)}
.lc{fill:var(--ac)} .ink .lb{fill:var(--td)} .paper .lb{fill:var(--tx)}
.top{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1}
.kick{font:500 30px 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ac)}
.rule{width:72px;height:4px;background:var(--ac);margin-top:22px}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;position:relative;z-index:1}
.bot{display:flex;justify-content:space-between;align-items:center;font:500 28px 'IBM Plex Mono',monospace;opacity:.85;position:relative;z-index:1}
h1{font:800 118px/1.02 'Archivo',sans-serif;letter-spacing:-.02em}
h2{font:800 84px/1.06 'Archivo',sans-serif;letter-spacing:-.015em}
h1 em,h2 em{font-style:normal;color:var(--ac)}
.sub{font:500 44px/1.35 'Inter',sans-serif;opacity:.9}
p.b{font:400 46px/1.4 'Inter',sans-serif}
p.b b{font-weight:600}
ul{list-style:none;display:flex;flex-direction:column;gap:30px}
li{font:400 44px/1.35 'Inter',sans-serif;display:grid;grid-template-columns:56px 1fr;align-items:start}
li .m{font:500 34px/1.45 'IBM Plex Mono',monospace;color:var(--ac)}
li .x{color:#B5473A}
.ink li .x{color:#FFB4A8}
li b{font-weight:600}
.note{font:500 28px/1.4 'IBM Plex Mono',monospace;opacity:.75}
table{border-collapse:collapse;width:100%;font:400 40px 'Inter',sans-serif}
td,th{padding:22px 10px;border-bottom:2px solid color-mix(in srgb,currentColor 18%,transparent);text-align:left}
th{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;opacity:.65}
td.k{font:800 40px 'Archivo',sans-serif}
td.v{font:500 34px 'IBM Plex Mono',monospace;color:var(--ac);white-space:nowrap}
.box{border:3px solid var(--ac);border-radius:6px;padding:36px 40px;display:flex;flex-direction:column;gap:18px;background:color-mix(in srgb,var(--ac) 10%,transparent)}
.cta{font:800 76px/1.08 'Archivo',sans-serif}
.cta em{font-style:normal;color:var(--ac)}
.handle{font:500 38px 'IBM Plex Mono',monospace;color:var(--ac)}
.legal{font:400 26px/1.4 'Inter',sans-serif;opacity:.65}
.swipe{color:var(--ac);opacity:1}
.motivo{position:absolute;left:0;right:0;bottom:140px;height:260px;opacity:.38}
.m-pasos{opacity:.9}
.m-tactica{opacity:.7}
.m-entreno{opacity:.5}
.ok{color:var(--tx)!important}
.cover .mid{padding-bottom:260px;justify-content:flex-end}
"""

def motivo(t):
    """Dibujo de portada propio de cada troncal."""
    W = 1080
    svg = f'<svg class="motivo m-{t}" viewBox="0 0 1080 260" preserveAspectRatio="none">'
    if t == "cabeza":  # ondas que se van calmando
        out = []
        for k in range(6):
            amp = 70 - k * 11; y0 = 50 + k * 34
            d = f"M0 {y0} " + " ".join(f"Q {x+45} {y0-amp if (x//90)%2==0 else y0+amp} {x+90} {y0}" for x in range(0, W, 90))
            out.append(f'<path d="{d}" fill="none" stroke="var(--a)" stroke-width="5"/>')
        return svg + "".join(out) + "</svg>"
    if t == "tactica":  # precio con niveles de target, entrada y stop
        pts = [(0,190),(90,165),(170,200),(260,135),(340,155),(430,110),(520,145),(610,85),(700,115),(790,70),(880,100),(970,50),(1080,75)]
        line = " ".join(f"{x},{y}" for x, y in pts)
        lv = "".join(f'<line x1="0" x2="1080" y1="{y}" y2="{y}" stroke="var(--a)" stroke-width="3" stroke-dasharray="{da}"/>' for y, da in [(30,"16 10"),(160,"4 8"),(235,"16 10")])
        return svg + lv + f'<polyline points="{line}" fill="none" stroke="var(--td)" stroke-width="6" stroke-linejoin="round"/></svg>'
    if t == "pasos":  # escalera
        n = 8; w = W / n
        return svg + "".join(f'<rect x="{i*w+4:.0f}" y="{260-(30+i*28)}" width="{w-8:.0f}" height="{30+i*28}" fill="{'var(--a)' if i == n-1 else '#fff'}" opacity="{1 if i == n-1 else 0.12+0.05*i:.2f}"/>' for i in range(n)) + "</svg>"
    if t == "entreno":  # casillas de la planilla con tildes
        out = ['<svg class="motivo m-entreno" viewBox="0 0 1080 260">']
        for r in range(3):
            for c in range(9):
                x = 40 + c * 115; y = 20 + r * 80
                out.append(f'<rect x="{x}" y="{y}" width="64" height="64" rx="6" fill="none" stroke="var(--td)" stroke-width="4"/>')
                if (r * 9 + c) % 4 != 3:
                    out.append(f'<path d="M{x+14} {y+34} l14 14 l24 -30" fill="none" stroke="var(--a)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
        return "".join(out) + "</svg>"
    hs = [(60,110),(90,150),(70,120),(120,190),(100,150),(140,210),(110,170),(150,230),(130,180),(170,240),(150,200),(190,250),(160,215),(200,255)]
    out = []; w = W / len(hs)
    for i, (lo, hi) in enumerate(hs):
        x = i*w + w*0.3; bw = w*0.4; col = "var(--a)" if i % 3 != 2 else "var(--td)"
        top = 260 - hi; bot = 260 - lo
        out.append(f'<rect x="{x+bw/2-2:.1f}" y="{top-18}" width="4" height="{bot-top+36}" fill="{col}"/><rect x="{x:.1f}" y="{top}" width="{bw:.1f}" height="{bot-top}" fill="{col}"/>')
    return svg + "".join(out) + "</svg>"

def slide(kind, bg, kicker, n, total, body):
    d, l, a, al, tx, td = TEMAS[tema(kicker)]
    right = '<span class="swipe">Deslizá →</span>' if kind == "cover" else f"{n:02d} / {total:02d}"
    deco = motivo(tema(kicker)) if kind == "cover" else ""
    return f'''<div class="s {bg} {kind}" style="--d:{d};--l:{l};--a:{a};--al:{al};--tx:{tx};--td:{td}">{deco}
      <div class="top"><div><div class="kick">{kicker}</div><div class="rule"></div></div>{logo()}</div>
      <div class="mid">{body}</div>
      <div class="bot"><span>@elprofetrader</span><span>{right}</span></div>
    </div>'''

LEGAL = '<p class="legal">Contenido educativo. No es recomendación de inversión.</p>'

def ul(items, mark="—", cls="m"):
    return "<ul>" + "".join(f'<li><span class="{cls}">{mark}</span><span>{i}</span></li>' for i in items) + "</ul>"

def nums(items):
    return "<ul>" + "".join(f'<li><span class="m">{k+1:02d}</span><span>{i}</span></li>' for k, i in enumerate(items)) + "</ul>"

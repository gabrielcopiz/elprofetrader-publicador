"""Planilla del viernes: lee los trades reales del Diario de Futuros y arma el carrusel con la nota de la semana.
Uso: python planilla.py [AAAA-MM-DD]   (por defecto, hoy en hora Argentina; tiene que ser viernes)
Escribe publicaciones/planillas/planilla-AAAA-MM-DD-NN.jpg + caption y suma la fecha a agenda.json.
Lo publica publicar.py, igual que cualquier carrusel. Si el diario no responde, no hace nada."""
import json, os, sys, datetime, asyncio, urllib.request
from estilo import CSS, slide, ul, nums, LEGAL, NEG

AQUI = os.path.dirname(os.path.abspath(__file__))
API = "https://diario-futuros.netlify.app/api/p/pmviaje0g7bd2vp/all"
MULT = {"ES": 50, "MES": 5, "NQ": 20, "MNQ": 2}
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie"]
MOTIVO = {"senal": "no apareció mi setup", "rojo": "check-in en rojo", "noticias": "noticias o feriado",
          "ausente": "no pude operar", "otro": "no operé"}

def bajar():
    if os.environ.get("DIARIO_JSON"):
        return json.load(open(os.environ["DIARIO_JSON"], encoding="utf-8"))
    req = urllib.request.Request(API, headers={"x-team-key": os.environ["DIARIO_KEY"]})
    return json.load(urllib.request.urlopen(req, timeout=60))

def puntos(t):
    s = 1 if t.get("side") == "long" else -1
    return (float(t["exit"]) - float(t["entry"])) * s

def es_be(t):
    neto = puntos(t) * MULT.get(t.get("inst"), 0) * float(t.get("qty") or 0)
    riesgo = float(t.get("risk") or 0) * MULT.get(t.get("inst"), 0) * float(t.get("qty") or 0)
    return abs(neto) <= (0.15 * riesgo if riesgo else 25)

def calcular(d, viernes):
    lunes = viernes - datetime.timedelta(days=4)
    fechas = [(lunes + datetime.timedelta(days=i)).isoformat() for i in range(5)]
    trades = sorted([t for t in d["trades"].values() if t.get("date") in fechas], key=lambda t: (t["date"], t.get("time") or ""))
    cfg = d.get("settings", {})
    setups = {s["name"] for s in cfg.get("strategies", [])}
    maxt = int(cfg.get("maxt") or 1)
    movio = [t for t in trades if any("stop" in e.lower() and "mov" in e.lower() for e in (t.get("psy", {}).get("exec") or []))
             or any("stop" in str(e).lower() for e in (t.get("err") or []))]
    fuera = [t for t in trades if not t.get("plan") or t.get("setup") not in setups]
    pasado = [f for f in fechas if sum(1 for t in trades if t["date"] == f and not es_be(t)) > maxt]
    incompletos = [t for t in trades if t.get("incomplete") or not t.get("time") or not (t.get("psy") or {}).get("after")]
    preg = [("¿Respeté el stop en todos los trades?", not movio, "Moví el stop en un trade. Aunque fuera para cubrirme, no estaba escrito en el plan." if len(movio) == 1 else f"Moví el stop en {len(movio)} trades. No estaba escrito en el plan."),
            ("¿Entré solo con mi setup?", not fuera, "Entré fuera de mi setup. Eso no se negocia."),
            ("¿Respeté mi límite del día?", not pasado, "Pasé mi límite de trades en un día."),
            ("¿Anoté todo?", not incompletos, "Dejé un trade sin anotar completo. Lo que no se anota no se puede corregir.")]
    filas = []
    for i, f in enumerate(fechas):
        del_dia = [t for t in trades if t["date"] == f]
        if del_dia:
            for t in del_dia:
                r = puntos(t) / float(t["risk"]) if float(t.get("risk") or 0) else 0
                res = "BE" if es_be(t) else f"{r:+.1f}R".replace(".", ",")
                filas.append((DIAS[i], f"{t.get('setup','')} · {t.get('inst','')}", res))
        else:
            skip = (d.get("days", {}).get(f) or {}).get("skip")
            filas.append((DIAS[i], "No operé" + (f": {MOTIVO.get(skip.get('reason'), 'no operé')}" if skip else ""), "—"))
    total_r = sum(puntos(t) / float(t["risk"]) for t in trades if float(t.get("risk") or 0) and not es_be(t))
    return dict(fechas=fechas, trades=trades, preg=preg, nota=sum(1 for p in preg if p[1]), filas=filas, total_r=total_r)

def dm(iso):
    y, m, dd = iso.split("-"); return f"{int(dd)}/{int(m)}"

def laminas(c):
    rango = f"Del {dm(c['fechas'][0])} al {dm(c['fechas'][-1])}"
    k = "Entrenamiento · Planilla"
    tot = f"{c['total_r']:+.1f}R".replace(".", ",")
    tabla = '<table><tr><th>Día</th><th>Qué hice</th><th>Resultado</th></tr>' + "".join(
        f'<tr><td class="k">{a}</td><td>{b}</td><td class="v">{r}</td></tr>' for a, b, r in c["filas"][:8]) + "</table>"
    marcas = "<ul>" + "".join(
        f'<li><span class="m"{"" if ok else f" style=color:{NEG}"}>{"✓" if ok else "✕"}</span><span>{q}</span></li>' for q, ok, _ in c["preg"]) + "</ul>"
    fallas = [txt for _, ok, txt in c["preg"] if not ok]
    if not c["trades"]:
        lleva = '<h2>Esta semana <em>no operé</em>.</h2><p class="b">No apareció lo que espero. No entrar también es parte del plan.</p>'
    elif fallas:
        lleva = '<h2>Lo que <em>me llevo</em></h2>' + ul(fallas) + '<p class="sub">Es lo que voy a corregir la semana que viene.</p>'
    else:
        lleva = '<h2>Lo que <em>me llevo</em></h2><p class="b">Hice lo que dije que iba a hacer. <b>Es lo único que controlo.</b></p>' + ('<p class="sub">Los días sin operar también cuentan: no entrar es parte del plan.</p>' if len(c["trades"]) < 5 else '<p class="sub">La semana que viene, lo mismo.</p>')
    return [
        ("ink", f'<h1>Mi planilla de la semana: <em>{c["nota"]} de 4</em>.</h1><p class="sub">{rango}. Con todos los trades, no solo los lindos.</p>'),
        ("paper", '<h2>Los trades</h2>' + tabla + f'<p class="b">Resultado de la semana: <b>{tot}</b>.</p><p class="note">R = cuánto gané o perdí, medido en veces mi riesgo.</p>'),
        ("paper", f'<h2>Las 4 preguntas: <em>{c["nota"]}/4</em></h2>' + marcas + '<p class="b">El resultado <b>no entra en la nota</b>.</p>'),
        ("ink", lleva),
        ("ink", '<p class="cta">¿Qué nota te pusiste <em>vos</em>?</p><p class="sub">Usá las 4 preguntas de la lámina 3 y contame en comentarios.</p><p class="handle">Seguí a @elprofetrader</p>' + LEGAL),
    ]

def caption(c):
    tot = f"{c['total_r']:+.1f}R".replace(".", ",")
    return (f"Planilla del viernes, semana del {dm(c['fechas'][0])} al {dm(c['fechas'][-1])}: {c['nota']} de 4.\n\n"
            f"Resultado de la semana: {tot}. No entra en la nota: la nota mide si hice lo que dije que iba a hacer.\n\n"
            "Hacé la tuya con las 4 preguntas y contame qué te pusiste.\n\n"
            "#psicotrading #trading #futuros #disciplina #tradingargentina")

async def render(slides, base, chrome=None):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(**({"executable_path": chrome} if chrome else {}))
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, (bg, body) in enumerate(slides, 1):
            doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{slide('cover' if i == 1 else 'inner', bg, 'Entrenamiento · Planilla', i, len(slides), body)}</body></html>"
            await pg.set_content(doc, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            if await pg.evaluate("(()=>{const m=document.querySelector('.mid');return m.scrollHeight>m.clientHeight+2})()"):
                raise SystemExit(f"La lámina {i} se desborda: no se publica")
            await pg.screenshot(path=f"{base}-{i:02d}.jpg", type="jpeg", quality=92)
        await b.close()

def main():
    hoy = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - datetime.timedelta(hours=3)).date()
    viernes = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else hoy
    if viernes.weekday() != 4:
        print("Hoy no es viernes: no hay planilla"); return
    pid = f"planilla-{viernes.isoformat()}"
    agenda_p = os.path.join(AQUI, "agenda.json")
    agenda = json.load(open(agenda_p, encoding="utf-8"))
    if (not os.environ.get("PRUEBA") and viernes < datetime.date(2026, 12, 4)) or any(a["fecha"] == viernes.isoformat() for a in agenda):
        print("Ese viernes ya tiene publicación (o es antes del 4/12): no hay planilla"); return
    try:
        d = bajar()
    except Exception as e:
        print("No pude leer el diario, no hay planilla esta semana:", e); return
    c = calcular(d, viernes)
    carpeta = os.path.join(AQUI, "publicaciones", "planillas"); os.makedirs(carpeta, exist_ok=True)
    sl = laminas(c)
    asyncio.run(render(sl, os.path.join(carpeta, pid), os.environ.get("CHROME")))
    open(os.path.join(carpeta, f"{pid}-caption.txt"), "w", encoding="utf-8").write(caption(c))
    agenda.append({"fecha": viernes.isoformat(), "carpeta": "planillas", "id": pid, "laminas": len(sl)})
    agenda.sort(key=lambda a: a["fecha"])
    open(agenda_p, "w", encoding="utf-8").write("[\n" + ",\n".join("  " + json.dumps(a, ensure_ascii=False) for a in agenda) + "\n]\n")
    print("Planilla armada:", pid, "nota", c["nota"], "de 4")

if __name__ == "__main__":
    main()

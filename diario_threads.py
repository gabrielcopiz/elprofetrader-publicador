"""Operativa del día en Threads: lee los trades REALES del Diario de Futuros y agenda el resumen del día.
Uso: python diario_threads.py            -> si es día hábil y ya son las 19:00 ART, agrega "op-AAAA-MM-DD" a threads/posteos.json
     python diario_threads.py --prueba AAAA-MM-DD -> muestra el texto de ese día, sin agendar nada
Reglas del fundador (25/11): sin el nombre del setup; después del cierre, nunca en vivo; plata permitida; sin número de cuenta ni firma;
los días sin trade también (solo si él anotó el motivo); cierre "Mi diario, no una recomendación".
Si el diario no responde o el día no tiene nada cargado, no hace nada (cero invento)."""
import json, os, sys, datetime
from planilla import bajar, puntos, es_be, MULT, MOTIVO

AQUI = os.path.dirname(os.path.abspath(__file__))
POSTEOS = os.path.join(AQUI, "threads", "posteos.json")
ART = datetime.timezone(datetime.timedelta(hours=-3))
NOMBRE = {"ES": "S&P 500 (ES)", "MES": "micro S&P 500 (MES)", "NQ": "Nasdaq (NQ)", "MNQ": "micro Nasdaq (MNQ)"}
CIERRE = "Mi diario, no una recomendación.\n\n¿Vos cómo cerraste el día?"

def coma(x, dec=1):
    return f"{x:+.{dec}f}".replace(".", ",")

def neto(t):
    bruto = float(t["grossOverride"]) if t.get("grossOverride") not in (None, "") else puntos(t) * MULT.get(t.get("inst"), 0) * float(t.get("qty") or 1)
    return bruto - float(t.get("comm") or 0)

def linea(t, n=None):
    lado = "largo" if t.get("side") == "long" else "corto"
    r = puntos(t) / float(t["risk"]) if float(t.get("risk") or 0) else None
    res = "break-even" if es_be(t) else (f"{coma(r)}R" if r is not None else "")
    usd = neto(t)
    plata = f"{'+' if usd >= 0 else '-'}USD {abs(usd):,.0f}".replace(",", ".")
    antes = (t.get("psy") or {}).get("before")
    partes = [f"{'Trade ' + str(n) + ': ' if n else ''}{NOMBRE.get(t.get('inst'), t.get('inst', ''))} en {lado}"
              + ".",  # el nombre del setup NO se publica (pedido del fundador 25/11)
              f"Resultado: {res} · {plata} netos de comisión." if res else f"Resultado: {plata} netos de comisión.",
              ("Antes de entrar: " + (", ".join(antes) if isinstance(antes, list) else str(antes)).lower() + "." if antes else ""),
              "Seguí el plan: " + ("sí." if t.get("plan") else "no.")]
    return "\n".join(p for p in partes if p)

def texto(d, fecha):
    dm = f"{int(fecha[8:])}/{int(fecha[5:7])}"
    trades = sorted([t for t in d["trades"].values() if t.get("date") == fecha], key=lambda t: t.get("time") or "")
    if trades:
        if len(trades) == 1:
            cuerpo = linea(trades[0])
        else:
            cuerpo = "\n\n".join(linea(t, i) for i, t in enumerate(trades, 1))
            cuerpo += f"\n\nEl día: {'+' if sum(map(neto, trades)) >= 0 else '-'}USD {abs(sum(map(neto, trades))):,.0f} netos.".replace(",", ".")
        return f"Mi operativa de hoy, {dm}. Con el resultado que sea.\n\n{cuerpo}\n\n{CIERRE}"
    skip = (d.get("days", {}).get(fecha) or {}).get("skip")
    if skip:
        motivo = MOTIVO.get(skip.get("reason"), "no operé")
        return (f"Hoy, {dm}, no operé: {motivo}.\n\nTambién lo anoto en el diario. No entrar es parte del plan: "
                f"somos traders, no apostadores.\n\n{CIERRE}")
    return None  # nada cargado todavía: no se inventa

def recortar(t):
    if len(t) <= 500: return t
    return t[:497].rsplit("\n", 1)[0] + "\n…"

def agendar():
    ahora = datetime.datetime.now(ART)
    if ahora.weekday() > 4 or ahora.hour < 19:
        print("Operativa: todavía no (días hábiles desde las 19:00 ART)"); return
    fecha = ahora.date().isoformat()
    base = json.load(open(POSTEOS, encoding="utf-8"))
    pid = f"op-{fecha}"
    if any(p["id"] == pid for p in base["posteos"]):
        print("Operativa de hoy ya agendada"); return
    try:
        d = bajar()
    except Exception as e:
        print(f"El diario no respondió ({e}); se reintenta en la próxima corrida"); return
    t = texto(d, fecha)
    if not t:
        print("Hoy no hay nada cargado en el diario todavía; se reintenta en la próxima corrida"); return
    base["posteos"].append({"id": pid, "fecha": fecha, "hora": "19:00", "tema": "Trading", "partes": [recortar(t)],
                            "fuente": "Diario de Futuros (trades reales del día, leídos por el robot)",
                            "por_que_trae_gente": "Prueba diaria y transparente (resultado real, también los días malos o sin trade) + pregunta de cierre."})
    json.dump(base, open(POSTEOS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Operativa agendada: {pid}\n{t}")

if __name__ == "__main__":
    if "--prueba" in sys.argv:
        f = sys.argv[sys.argv.index("--prueba") + 1]
        print(texto(bajar(), f) or "(ese día no hay nada cargado)")
    else:
        agendar()

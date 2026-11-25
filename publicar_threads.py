"""Publica en Threads (@elprofetrader) los posteos de threads/posteos.json cuando llega su hora (Argentina).
Uso: python publicar_threads.py --auto      -> publica UNO por corrida: el más viejo que ya debía salir y no salió
     python publicar_threads.py --prueba ID -> muestra cómo saldría ese posteo, sin publicar
     python publicar_threads.py --renovar   -> renueva la llave (dura 60 días); se corre una vez por semana
La llave viaja cifrada en threads/llave.enc (clave en el secreto THREADS_CLAVE) para poder renovarla sola."""
import json, os, sys, time, subprocess, urllib.request, urllib.parse, datetime

API = "https://graph.threads.net/v1.0"
AQUI = os.path.dirname(os.path.abspath(__file__))
POSTEOS = os.path.join(AQUI, "threads", "posteos.json")
REGISTRO = os.path.join(AQUI, "threads", "publicado.json")
LLAVE = os.path.join(AQUI, "threads", "llave.enc")
ART = datetime.timezone(datetime.timedelta(hours=-3))

def openssl(args, entrada):
    r = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-a", "-A", *args,
                        "-pass", "env:THREADS_CLAVE"], input=entrada, capture_output=True, text=True)
    if r.returncode: raise SystemExit("No se pudo usar la llave cifrada: " + r.stderr[:200])
    return r.stdout.strip()

def leer_token():
    if os.environ.get("THREADS_TOKEN"): return os.environ["THREADS_TOKEN"].strip()
    return openssl(["-d"], open(LLAVE).read().strip() + "\n")

def llamar(metodo, ruta, datos, token):
    cuerpo = urllib.parse.urlencode(dict(datos, access_token=token))
    req = (urllib.request.Request(f"{API}/{ruta}?{cuerpo}") if metodo == "GET"
           else urllib.request.Request(f"{API}/{ruta}", data=cuerpo.encode(), method="POST"))
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Error de Threads en {ruta}: {e.read().decode()[:500]}")

def publicar_parte(texto, token, tema=None, responde_a=None):
    datos = {"media_type": "TEXT", "text": texto}
    if tema: datos["topic_tag"] = tema
    if responde_a: datos["reply_to_id"] = responde_a
    cid = llamar("POST", "me/threads", datos, token)["id"]
    time.sleep(30)  # Meta recomienda esperar antes de publicar el contenedor
    return llamar("POST", "me/threads_publish", {"creation_id": cid}, token)["id"]

def publicar(p, token):
    primero = previo = publicar_parte(p["partes"][0], token, p.get("tema"))
    for parte in p["partes"][1:]:  # hilo: cada parte responde a la anterior
        previo = publicar_parte(parte, token, None, previo)
    link = llamar("GET", primero, {"fields": "permalink"}, token).get("permalink", "")
    return primero, link

def auto():
    token = leer_token()
    ahora = datetime.datetime.now(ART)
    reg = json.load(open(REGISTRO, encoding="utf-8")) if os.path.exists(REGISTRO) else {}
    posteos = json.load(open(POSTEOS, encoding="utf-8"))["posteos"]
    vencidos = sorted((p for p in posteos if p["id"] not in reg and not p.get("retenido")
                       and datetime.datetime.fromisoformat(f"{p['fecha']}T{p['hora']}").replace(tzinfo=ART) <= ahora),
                      key=lambda p: (p["fecha"], p["hora"]))
    if not vencidos:
        print("Nada para publicar en Threads ahora"); return
    p = vencidos[0]
    pid, link = publicar(p, token)
    reg[p["id"]] = f"{ahora:%Y-%m-%d %H:%M} ART, robot, id {pid}, {link}"
    json.dump(reg, open(REGISTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Publicado en Threads: {p['id']} -> {link}")

def renovar():
    token = leer_token()
    q = urllib.parse.urlencode({"grant_type": "th_refresh_token", "access_token": token})
    nuevo = json.load(urllib.request.urlopen(f"https://graph.threads.net/refresh_access_token?{q}", timeout=60))
    open(LLAVE, "w").write(openssl([], nuevo["access_token"] + "\n") + "\n")
    print(f"Llave de Threads renovada: vence en {nuevo.get('expires_in', 0) // 86400} días")

if __name__ == "__main__":
    if "--auto" in sys.argv: auto()
    elif "--renovar" in sys.argv: renovar()
    elif "--prueba" in sys.argv:
        i = sys.argv[sys.argv.index("--prueba") + 1]
        p = next(x for x in json.load(open(POSTEOS, encoding="utf-8"))["posteos"] if x["id"] == i)
        print(f"[{p['fecha']} {p['hora']} · tema {p.get('tema')}]")
        for n, parte in enumerate(p["partes"], 1): print(f"--- parte {n} ({len(parte)} letras)\n{parte}")
    else: print(__doc__)

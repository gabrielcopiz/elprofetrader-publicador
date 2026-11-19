"""Publica en Instagram (@elprofetrader) el carrusel agendado para hoy (hora Argentina).
Uso: python publicar.py            -> publica lo de hoy si no se publicó
     python publicar.py --prueba ID -> arma el carrusel de ID sin publicarlo (control)"""
import json, os, sys, time, urllib.request, urllib.parse, datetime

IG_USER = "17841433283485002"
API = "https://graph.facebook.com/v23.0"
RAW = "https://raw.githubusercontent.com/gabrielcopiz/elprofetrader-publicador/main/publicaciones"
TOKEN = os.environ["IG_TOKEN"]
AQUI = os.path.dirname(os.path.abspath(__file__))

def llamar(metodo, ruta, datos=None):
    datos = dict(datos or {}, access_token=TOKEN)
    cuerpo = urllib.parse.urlencode(datos).encode()
    if metodo == "GET":
        req = urllib.request.Request(f"{API}/{ruta}?{cuerpo.decode()}")
    else:
        req = urllib.request.Request(f"{API}/{ruta}", data=cuerpo, method="POST")
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Error de Instagram en {ruta}: {e.read().decode()[:500]}")

def esperar(cid):
    for _ in range(30):
        st = llamar("GET", cid, {"fields": "status_code"})["status_code"]
        if st == "FINISHED": return
        if st in ("ERROR", "EXPIRED"): raise SystemExit(f"Contenedor {cid} con estado {st}")
        time.sleep(5)
    raise SystemExit(f"Contenedor {cid} no terminó a tiempo")

def armar(item):
    base = f"{RAW}/{item['carpeta']}/{item['id']}"
    hijos = []
    for i in range(1, item["laminas"] + 1):
        r = llamar("POST", f"{IG_USER}/media", {"image_url": f"{base}-{i:02d}.jpg", "is_carousel_item": "true"})
        hijos.append(r["id"])
    for h in hijos: esperar(h)
    texto = open(os.path.join(AQUI, "publicaciones", item["carpeta"], f"{item['id']}-caption.txt"), encoding="utf-8").read()
    car = llamar("POST", f"{IG_USER}/media", {"media_type": "CAROUSEL", "children": ",".join(hijos), "caption": texto})["id"]
    esperar(car)
    return car

def main():
    agenda = json.load(open(os.path.join(AQUI, "agenda.json"), encoding="utf-8"))
    if len(sys.argv) > 2 and sys.argv[1] == "--prueba":
        item = next(a for a in agenda if a["id"] == sys.argv[2])
        print("Prueba OK, carrusel armado y listo (sin publicar):", armar(item)); return
    hoy = (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).date().isoformat()
    hecho_p = os.path.join(AQUI, "publicado.json")
    hecho = json.load(open(hecho_p, encoding="utf-8"))
    pend = [a for a in agenda if a["fecha"] <= hoy and a["id"] not in hecho]
    if not pend:
        print("Nada para publicar hoy", hoy); return
    item = pend[0]  # uno por día como máximo
    car = armar(item)
    post = llamar("POST", f"{IG_USER}/media_publish", {"creation_id": car})["id"]
    link = llamar("GET", post, {"fields": "permalink"}).get("permalink")
    hecho[item["id"]] = {"fecha": hoy, "post": post, "link": link}
    json.dump(hecho, open(hecho_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Publicado:", item["id"], link)

if __name__ == "__main__":
    main()

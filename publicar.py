"""Publica en Instagram (@elprofetrader) el carrusel agendado para hoy (hora Argentina).
Uso: python publicar.py [--tipo carrusel|reel]  -> publica lo de hoy de ese tipo si no se publicó (por defecto carrusel)
     python publicar.py --prueba ID             -> arma la publicación de ID sin publicarla (control)
Un carrusel y un reel por día como máximo, cada uno en su horario."""
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

def esperar(cid, vueltas=30):
    for _ in range(vueltas):
        st = llamar("GET", cid, {"fields": "status_code"})["status_code"]
        if st == "FINISHED": return
        if st in ("ERROR", "EXPIRED"): raise SystemExit(f"Contenedor {cid} con estado {st}")
        time.sleep(5)
    raise SystemExit(f"Contenedor {cid} no terminó a tiempo")

def armar_reel(item):
    url = f"{RAW}/{item['carpeta']}/{item['id']}.mp4"
    texto = open(os.path.join(AQUI, "publicaciones", item["carpeta"], f"{item['id']}-caption.txt"), encoding="utf-8").read()
    datos = {"media_type": "REELS", "video_url": url, "caption": texto, "share_to_feed": "true"}
    if item.get("portada"):
        datos["cover_url"] = f"{RAW}/{item['carpeta']}/{item['id']}-portada.jpg"
    cid = llamar("POST", f"{IG_USER}/media", datos)["id"]
    esperar(cid, 60)  # hasta 5 minutos de procesamiento
    return cid

def armar(item):
    if item.get("tipo") == "reel":
        return armar_reel(item)
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
    tipo = sys.argv[sys.argv.index("--tipo") + 1] if "--tipo" in sys.argv else "carrusel"
    hoy = (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).date().isoformat()
    hecho_p = os.path.join(AQUI, "publicado.json")
    hecho = json.load(open(hecho_p, encoding="utf-8"))
    pend = [a for a in agenda if a["fecha"] <= hoy and a["id"] not in hecho and a.get("tipo", "carrusel") == tipo]
    if not pend:
        print("Nada para publicar hoy", tipo, hoy); return
    item = pend[0]  # uno por día como máximo
    car = armar(item)
    post = llamar("POST", f"{IG_USER}/media_publish", {"creation_id": car})["id"]
    link = llamar("GET", post, {"fields": "permalink"}).get("permalink")
    hecho[item["id"]] = {"fecha": hoy, "post": post, "link": link}
    json.dump(hecho, open(hecho_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Publicado:", item["id"], link)

if __name__ == "__main__":
    main()

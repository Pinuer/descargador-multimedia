# Descarga de imagenes: una imagen directa por URL, o todas las de una pagina.
import os
import re
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

# user-agent de chrome comun, sin esto algunos sitios devuelven 403
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}


def _nombre_archivo_valido(nombre):
    return re.sub(r'[<>:"/\\|?*]', "_", nombre)


def descargar_imagen(url: str, carpeta_salida: str = "descargas") -> str:
    os.makedirs(carpeta_salida, exist_ok=True)

    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    nombre = os.path.basename(urlparse(url).path) or "imagen.jpg"
    nombre = _nombre_archivo_valido(nombre)
    ruta = os.path.join(carpeta_salida, nombre)

    with open(ruta, "wb") as f:
        f.write(resp.content)

    return ruta


def descargar_imagenes_de_pagina(url_pagina: str, carpeta_salida: str = "descargas") -> list:
    """Busca todos los <img> de una pagina y baja lo que encuentre.

    Ojo: esto es un scraping bastante basico, solo lee el HTML crudo.
    En paginas que cargan las imagenes con JS (ej. scroll infinito, lazy
    load raro) probablemente no va a encontrar todo.
    """
    os.makedirs(carpeta_salida, exist_ok=True)

    resp = requests.get(url_pagina, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    urls_imagenes = []
    for tag in soup.find_all("img"):
        src = tag.get("src") or tag.get("data-src")
        if src:
            urls_imagenes.append(urljoin(url_pagina, src))

    rutas_descargadas = []
    for i, url_img in enumerate(urls_imagenes, start=1):
        try:
            resp_img = requests.get(url_img, headers=HEADERS, timeout=30)
            resp_img.raise_for_status()
            nombre = os.path.basename(urlparse(url_img).path) or f"imagen_{i}.jpg"
            nombre = _nombre_archivo_valido(nombre)
            ruta = os.path.join(carpeta_salida, nombre)
            with open(ruta, "wb") as f:
                f.write(resp_img.content)
            rutas_descargadas.append(ruta)
        except requests.RequestException:
            # si una imagen falla seguimos con las demas, no vale la pena
            # frenar todo el lote por un link roto
            continue

    return rutas_descargadas

# TODO: filtrar imagenes muy chicas (iconos, sprites, pixel de tracking)
# capaz por tamaño de archivo o dimensiones antes de guardarlas

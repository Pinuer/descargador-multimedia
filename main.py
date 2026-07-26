import argparse
import sys

from descargador.video import descargar_video, descargar_audio
from descargador.imagen import descargar_imagen, descargar_imagenes_de_pagina


def menu_interactivo():
    print("=== Descargador de Videos/Imagenes ===\n")

    url = input("Pega el link: ").strip()
    if not url:
        print("Error: no ingresaste ningun link", file=sys.stderr)
        sys.exit(1)

    print("\nQue queres descargar?")
    print("  1) Video")
    print("  2) Audio (mp3)")
    print("  3) Imagen (link directo)")
    print("  4) Galeria (todas las imagenes de una pagina)")

    opcion = input("\nOpcion [1-4]: ").strip()
    salida = input("Carpeta de salida (Enter = 'descargas'): ").strip() or "descargas"

    try:
        if opcion == "1":
            calidad = input("Calidad (Enter = 'best', o ej. 720p, 1080p): ").strip() or "best"
            ruta = descargar_video(url, salida, calidad)
            print(f"\nListo, video descargado: {ruta}")

        elif opcion == "2":
            ruta = descargar_audio(url, salida)
            print(f"\nListo, audio descargado: {ruta}")

        elif opcion == "3":
            ruta = descargar_imagen(url, salida)
            print(f"\nListo, imagen descargada: {ruta}")

        elif opcion == "4":
            rutas = descargar_imagenes_de_pagina(url, salida)
            print(f"\n{len(rutas)} imagenes descargadas en '{salida}'")
            for r in rutas:
                print(f"  - {r}")

        else:
            print("Opcion invalida", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        # yt-dlp y requests tiran excepciones bastante distintas entre si,
        # por ahora las mando todas para stderr y listo
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) == 1:
        menu_interactivo()
        return

    parser = argparse.ArgumentParser(description="Descargador de videos/imagenes desde la web")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    p_video = subparsers.add_parser("video", help="Descargar un video")
    p_video.add_argument("url")
    p_video.add_argument("--calidad", default="best")
    p_video.add_argument("--salida", default="descargas")

    p_audio = subparsers.add_parser("audio", help="Descargar solo el audio (mp3)")
    p_audio.add_argument("url")
    p_audio.add_argument("--salida", default="descargas")

    p_imagen = subparsers.add_parser("imagen", help="Descargar una imagen directa")
    p_imagen.add_argument("url")
    p_imagen.add_argument("--salida", default="descargas")

    p_galeria = subparsers.add_parser("galeria", help="Descargar todas las imagenes de una pagina")
    p_galeria.add_argument("url")
    p_galeria.add_argument("--salida", default="descargas")

    args = parser.parse_args()

    try:
        if args.comando == "video":
            ruta = descargar_video(args.url, args.salida, args.calidad)
            print(f"Video descargado: {ruta}")

        elif args.comando == "audio":
            ruta = descargar_audio(args.url, args.salida)
            print(f"Audio descargado: {ruta}")

        elif args.comando == "imagen":
            ruta = descargar_imagen(args.url, args.salida)
            print(f"Imagen descargada: {ruta}")

        elif args.comando == "galeria":
            rutas = descargar_imagenes_de_pagina(args.url, args.salida)
            print(f"{len(rutas)} imagenes descargadas en '{args.salida}'")
            for r in rutas:
                print(f"  - {r}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Descarga de videos usando yt-dlp.
# Anda con YouTube, Twitter/X, Instagram, TikTok, Facebook, etc, en general
# cualquier sitio que soporte yt-dlp (son un monton, ver su wiki).
#
# ojo: necesita ffmpeg instalado en el sistema para el merge de video+audio
# y para pasar a mp3. Si no esta instalado, yt-dlp tira error.

import os
import yt_dlp


def descargar_video(url: str, carpeta_salida: str = "descargas", calidad: str = "best") -> str:
    os.makedirs(carpeta_salida, exist_ok=True)

    # si piden algo tipo "720p" armamos el formato manualmente, sino
    # dejamos que yt-dlp use best/worst directo
    formato = calidad
    if calidad not in ("best", "worst"):
        altura = calidad.replace("p", "")
        formato = f"bestvideo[height<={altura}]+bestaudio/best"

    ydl_opts = {
        "format": formato,
        "outtmpl": os.path.join(carpeta_salida, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ruta = ydl.prepare_filename(info)

        # a veces prepare_filename devuelve la extension original (webm, etc)
        # aunque haya habido merge a mp4, entonces chequeamos si existe la version mp4
        if not ruta.endswith(".mp4"):
            base, _ = os.path.splitext(ruta)
            posible = f"{base}.mp4"
            if os.path.exists(posible):
                ruta = posible

        return ruta


def descargar_audio(url: str, carpeta_salida: str = "descargas") -> str:
    """Baja solo el audio y lo convierte a mp3 (requiere ffmpeg)."""
    os.makedirs(carpeta_salida, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(carpeta_salida, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ruta = ydl.prepare_filename(info)
        base, _ = os.path.splitext(ruta)
        return base + ".mp3"

# TODO: agregar soporte para pasar cookies (--cookies-from-browser) para
# poder bajar contenido privado/con restriccion de edad

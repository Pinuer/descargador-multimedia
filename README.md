# descargador-multimedia

CLI en Python para bajar videos, audio e imagenes desde internet. Lo hice
porque me cansé de instalar 3 extensiones distintas del navegador cada vez
que quería guardar un video.

- **Video**: usa `yt-dlp` por debajo (YouTube, Twitter/X, Instagram, TikTok, Facebook, etc.)
- **Audio**: extrae mp3 de cualquier video soportado por yt-dlp
- **Imagenes**: descarga directa por URL, o en lote leyendo los `<img>` de una pagina

## Instalación

```bash
git clone https://github.com/Pinuer/descargador-multimedia.git
cd descargador-multimedia
pip install -r requirements.txt
```

También hace falta `ffmpeg` instalado en el sistema (lo usa yt-dlp para el merge de video+audio y para convertir a mp3):

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

```

## Uso

### Modo interactivo

Se ejecuta sin argumentos y te va preguntando todo:

```bash
python main.py
```

### Modo por comandos

```bash
# video en mejor calidad
python main.py video "https://youtube.com/watch?v=XXXX"

# video en calidad especifica
python main.py video "https://youtube.com/watch?v=XXXX" --calidad 720p

# solo audio (mp3)
python main.py audio "https://youtube.com/watch?v=XXXX"

# una imagen directa
python main.py imagen "https://ejemplo.com/foto.jpg"

# todas las imagenes de una pagina
python main.py galeria "https://ejemplo.com/galeria"
```

Todos los comandos aceptan `--salida <carpeta>` (por defecto guarda en `descargas/`).


## Notas / pendientes

- No maneja login ni cookies todavía, así que contenido privado o con
  restricción de edad no se puede bajar por ahora.
- El modo `galeria` solo lee el HTML crudo de la página, si el sitio carga
  las imágenes con JS puede no encontrarlas todas.
- Usalo para tu propio contenido o donde tengas permiso — respetá los
  términos de servicio de cada plataforma y los derechos de autor.



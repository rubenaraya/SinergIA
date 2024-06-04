# pysinergia\exportadores\convertidor_audio.py

from pathlib import Path
import math, os
# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)
from pysinergia.adaptadores import I_ConectorDisco as _I_Disco

RUTA_FFMPEG = Path(f'{_Constantes.DIR_LIB_FFMPEG}').resolve()
os.environ["PATH"] = str(RUTA_FFMPEG) + os.pathsep + os.getenv("PATH")
from pydub import AudioSegment

class FORMATO:
    WAV = 'wav'
    MP3 = 'mp3'
    MP4 = 'mp4'
    M4A = 'm4a'
    OGG = 'ogg'
    OPUS = 'opus'
    WMA = 'wma'
    WEBA = 'weba'
    WEBM = 'webm'

class BITRATE:
    _64KBPS = '64'
    _96KBPS = '96'
    _128KBPS = '128'
    _192KBPS = '192'
    _256KBPS = '256'

# --------------------------------------------------
# Clase: ConvertidorAudio
# --------------------------------------------------
class ConvertidorAudio:
    def __init__(mi, disco:_I_Disco):
        mi.disco:_I_Disco = disco
        AudioSegment.converter = f'{RUTA_FFMPEG.as_posix()}/ffmpeg'
        mi.opciones = {
            'tiempo_maximo': 30 * _Constantes.TIEMPO.MIN,
            'peso_maximo': 24 * _Constantes.PESO.MB,
            'canales': 1,
            'formato': FORMATO.MP3,
            'bitrate': BITRATE._64KBPS,
        }

    # --------------------------------------------------
    # Métodos públicos

    def convertir(mi, ruta_audio:str, dir_destino:str, opciones:dict=None) -> list[str]:
        try:
            if not opciones:
                opciones = mi.opciones
            ruta_destino = mi.disco.crear_carpeta(nombre=dir_destino, antecesores=True)
            ruta_origen = mi.disco.comprobar_ruta(ruta_audio)
            resultado:list = []
            if ruta_origen and ruta_destino and opciones:
                ruta_origen_path = Path(ruta_origen)
                nombre_base = ruta_origen_path.stem
                formato = opciones.get('formato')
                peso_maximo = opciones.get('peso_maximo')
                tiempo_maximo = opciones.get('tiempo_maximo')
                bitrate = opciones.get('bitrate')
                canales = opciones.get('canales')
                audio = AudioSegment.from_file(ruta_origen)
                audio = audio.set_channels(canales)
                duracion = round(audio.duration_seconds, None) + 1
                cantidad = math.ceil(duracion * 1000 / tiempo_maximo)
                for i in range(0, cantidad):
                    inicio = (i * tiempo_maximo)
                    final = inicio + (tiempo_maximo)
                    seleccion = audio[inicio:final]
                    if cantidad > 1:
                        ruta_final = f"{ruta_destino}/{nombre_base}-{str(i + 1)}.{formato}"
                    else:
                        ruta_final = f"{ruta_destino}/{nombre_base}.{formato}"
                    seleccion.export(ruta_final, format=formato, bitrate=bitrate)
                    if Path(ruta_final).stat().st_size > peso_maximo:
                        break
                    else:
                        resultado.append(ruta_final)
            return resultado
        except Exception as e:
            print(e)
            return []


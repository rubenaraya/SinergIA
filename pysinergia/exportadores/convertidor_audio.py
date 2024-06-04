# pysinergia\exportadores\convertidor_audio.py

import math, os
from pathlib import Path

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import Constantes as _Constantes
from pysinergia.adaptadores import I_ConectorDisco as _I_Disco

# --------------------------------------------------
# Configuracion de FFMPEG
RUTA_FFMPEG = Path(f'{_Constantes.DIR_LIB_FFMPEG}').resolve()
os.environ["PATH"] = str(RUTA_FFMPEG) + os.pathsep + os.getenv("PATH")
from pydub import AudioSegment

# --------------------------------------------------
# Clases de Constantes

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
                audio:AudioSegment = AudioSegment.from_file(ruta_origen)
                if canales == 1:
                    audio = audio.split_to_mono()[0]
                audio = audio.set_channels(canales)
                cantidad = math.ceil(len(audio) / tiempo_maximo)
                for i in range(0, cantidad):
                    inicio = (i * tiempo_maximo)
                    final = inicio + (tiempo_maximo)
                    seleccion = audio[inicio:final]
                    if cantidad > 1:
                        ruta_guardar = f"{ruta_destino}/{nombre_base}-{str(i + 1)}.{formato}"
                    else:
                        ruta_guardar = f"{ruta_destino}/{nombre_base}.{formato}"
                    seleccion.export(ruta_guardar, format=formato, bitrate=bitrate)
                    if Path(ruta_guardar).stat().st_size > peso_maximo:
                        break
                    else:
                        resultado.append(ruta_guardar)
            return resultado
        except Exception as e:
            print(e)
            return []


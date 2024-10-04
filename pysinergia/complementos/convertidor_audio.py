# --------------------------------------------------
# pysinergia\complementos\convertidor_audio.py
# --------------------------------------------------

import os, math
from pathlib import Path
from pydub import AudioSegment

# Importaciones de PySinergIA
from pysinergia.globales import Constantes
from pysinergia.complementos.exportador import ErrorExportador

# --------------------------------------------------
# Clase: ConvertidorAudio
class ConvertidorAudio:
    def __init__(mi, ruta_base:str):
        mi.ruta_base:str = ruta_base
        mi.opciones = {
            'tiempo_maximo': 30 * Constantes.TIEMPO.MIN,
            'peso_maximo': 24 * Constantes.PESO.MB,
            'canales': 1,
            'formato': Constantes.AUDIO.MP3,
            'bitrate': Constantes.BITRATE._64KBPS,
        }

    def convertir(mi, ruta_audio:str, dir_destino:str, opciones:dict=None) -> list[str]:
        resultado:list = []
        try:
            if not opciones:
                opciones = mi.opciones
            path_origen = Path(f'{mi.ruta_base}/{ruta_audio}')
            if not path_origen.is_file():
                return resultado
            path_destino = Path(f'{mi.ruta_base}/{dir_destino}')
            path_destino.mkdir(parents=True, exist_ok=True)
            nombre_base = path_origen.stem
            formato = opciones.get('formato')
            peso_maximo = opciones.get('peso_maximo')
            tiempo_maximo = opciones.get('tiempo_maximo')
            bitrate = opciones.get('bitrate')
            canales = opciones.get('canales')
            ruta_lib_ffmpeg = os.getenv('RUTA_LIB_FFMPEG')
            AudioSegment.converter = f'{ruta_lib_ffmpeg}/ffmpeg'
            audio:AudioSegment = AudioSegment.from_file(path_origen)
            if canales == 1:
                audio = audio.split_to_mono()[0]
            audio = audio.set_channels(canales)
            cantidad = math.ceil(len(audio) / tiempo_maximo)
            for i in range(0, cantidad):
                inicio = (i * tiempo_maximo)
                final = inicio + (tiempo_maximo)
                seleccion = audio[inicio:final]
                if cantidad > 1:
                    ruta_guardar = f"{path_destino.as_posix()}/{nombre_base}-{str(i + 1)}.{formato}"
                else:
                    ruta_guardar = f"{path_destino.as_posix()}/{nombre_base}.{formato}"
                seleccion.export(ruta_guardar, format=formato, bitrate=bitrate)
                if Path(ruta_guardar).stat().st_size > peso_maximo:
                    break
                else:
                    resultado.append(ruta_guardar)
        except Exception as e:
            raise ErrorExportador(
                mensaje='Error-en-exportador-Audio',
                codigo=Constantes.ESTADO._500_ERROR,
                tipo=type(e).__name__,
                recurso=ruta_audio,
            )
        return resultado


# backend\pysinergia\globales.py

import uuid, os, json
from typing import Dict

# --------------------------------------------------
# Valores globales
UUID = uuid.UUID


# --------------------------------------------------
# Clase estática: Constantes
# --------------------------------------------------
class Constantes:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    RUTA_CONECTORES = 'backend.pysinergia.conectores'
    DIR_LIB_SQLEAN = './_lib/sqlean'
    DIR_LIB_FFMPEG = './_lib/ffmpeg'

    class MODO:
        PRODUCCION = 'PRODUCCION'
        DESARROLLO = 'DESARROLLO'
        PRUEBAS = 'PRUEBAS'
        LOCAL = 'LOCAL'

    class CONECTOR:
        AlmacenChroma = 'AlmacenChroma'
        AlmacenFaiss = 'AlmacenFaiss'
        BasedatosMysql = 'BasedatosMysql'
        BasedatosSqlite = 'BasedatosSqlite'
        DiscoLocal = 'DiscoLocal'
        LlmOpenai = 'LlmOpenai'


# --------------------------------------------------
# Clase estática: Json
# --------------------------------------------------
class Json:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def leer(archivo:str):
        data = None
        try:
            if archivo and os.path.isfile(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
        except:
            pass
        return data

    @staticmethod
    def guardar(datos, archivo:str) -> bool:
        try:
            if archivo and datos:
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, ensure_ascii=False, indent=2)
                return True
        except:
            pass
        return False

    @staticmethod
    def codificar(objeto) -> str:
        return json.dumps(dict(objeto), ensure_ascii=False)

    @staticmethod
    def decodificar(texto:str):
        return json.loads(texto)


# --------------------------------------------------
# Clase estática: Funciones
# --------------------------------------------------
class Funciones:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def _() -> str:
        return os.sep

    @staticmethod
    def fecha_hora(zona_horaria:str) -> Dict:
        import pytz
        from datetime import datetime
        fechahora = {}
        if not zona_horaria:
            zona_horaria = 'Etc/GMT'
        ist = pytz.timezone(zona_horaria)
        local = ist.localize(datetime.now())
        fechahora['hoy_fecha'] = local.strftime( "%d/%m/%Y" )
        fechahora['hoy_hora'] = local.strftime( "%H:%M" )
        fechahora['hoy_amd'] = local.strftime( "%Y-%m-%d" )
        fechahora['hoy_dma'] = local.strftime( "%d-%m-%Y" )
        fechahora['hoy_mda'] = local.strftime( "%m-%d-%Y" )
        fechahora['hoy_md'] = local.strftime( "%m-%d" )
        fechahora['hoy_dia'] = local.strftime( "%d" )
        fechahora['hoy_mes'] = local.strftime( "%m" )
        fechahora['hoy_año'] = local.strftime( "%Y" )
        fechahora['ahora'] = local.strftime( "%Y%m%d%H%M%S" )
        fechahora['periodo'] = local.strftime( "%Y%m%d" )
        return fechahora

    @staticmethod
    def obtener_ruta_env(nombre_modulo:str, nombre_archivo:str='.config.env'):
        parts = nombre_modulo.split('.')[:-1]
        path = os.path.join(*parts)
        return os.path.join(path, nombre_archivo)


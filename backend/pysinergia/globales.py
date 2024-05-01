# backend\pysinergia\globales.py

import uuid, os, json, logging
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

    class NIVEL:
        INFO = 'INFO'
        DEBUG = 'DEBUG'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        CRITICAL = 'CRITICAL'

    class SALIDA:
        EXITO = "EXITO"
        AVISO = "AVISO"
        ALERTA = "ALERTA"
        ERROR = "ERROR"

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
    def obtener_ruta_env(nombre_modulo:str, modo:str):
        nombre_archivo = '.config.env'
        if modo:
            nombre_archivo = f".{modo.lower()}.env"
        parts = nombre_modulo.split('.')[:-1]
        path = os.path.join(*parts)
        return os.path.join(path, nombre_archivo)


# --------------------------------------------------
# Clase estática: RegistradorLogs
# --------------------------------------------------
class RegistradorLogs():

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def crear(nombre:str, nivel:str, archivo:str):
        logging.basicConfig(
            level=nivel,
            encoding='utf-8',
            filename=archivo,
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s',
            datefmt="%d/%m/%Y %H:%M:%S"
        )
        return logging.getLogger(nombre)


# --------------------------------------------------
# Clase: ErrorPersonalizado
# --------------------------------------------------
class ErrorPersonalizado(Exception):
    def __init__(mi, mensaje:str, tipo:str='ERROR', codigo:int=500, detalles:list=[]):
        mi.codigo = codigo
        mi.tipo = tipo
        mi.mensaje = mensaje
        mi.detalles = detalles
        super().__init__(mi.mensaje)

    def __str__(mi):
        return f'{mi.mensaje}'

    def __repr__(mi):
        return f'{mi.tipo} {mi.codigo}: {mi.mensaje}. {mi.detalles.__str__()}'


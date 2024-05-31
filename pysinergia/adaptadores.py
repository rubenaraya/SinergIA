# pysinergia\adaptadores.py

from abc import (ABCMeta, abstractmethod)
from typing import (Dict, List, BinaryIO, TextIO)
from functools import lru_cache
from pathlib import Path

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Adaptadores)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
)
from pysinergia.dominio import (
    CargaArchivo as _CargaArchivo,
    Archivo as _Archivo,
)

# --------------------------------------------------
# Interface: I_ConectorAlmacen
# --------------------------------------------------
class I_ConectorAlmacen(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura por los conectores

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorBasedatos
# --------------------------------------------------
class I_ConectorBasedatos(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura por los conectores

    # --------------------------------------------------
    # Constantes

    class ESTRUCTURA:
        DICCIONARIO = 1
        TUPLA = 2

    class INSTRUCCION:
        INSERT = "INSERT"
        UPDATE = "UPDATE"
        DELETE = "DELETE"
        SELECT = "SELECT"

    class FILTRO:
        CONTIENE = "CONTIENE"
        COINCIDE = "COINCIDE"
        PALABRAS = "PALABRAS"
        FRASE = "FRASE"
        INCLUYE = "INCLUYE"
        FECHA = "FECHA"
        RANGO_FECHAS = "RANGO_FECHAS"
        RANGO_NUMEROS = "RANGO_NUMEROS"
        PERIODO = "PERIODO"
        LISTA_DATOS = "LISTA_DATOS"
        NUMERO = "NUMERO"

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...

    @abstractmethod
    def desconectar(mi):
        ...

    @abstractmethod
    def insertar(mi, instruccion:str, parametros:list) -> int:
        ...

    @abstractmethod
    def actualizar(mi, instruccion:str, parametros:list) -> int:
        ...

    @abstractmethod
    def eliminar(mi, instruccion:str, parametros:list) -> int:
        ...

    @abstractmethod
    def leer(mi, instruccion:str, parametros:list, contenido:int) -> tuple:
        ...

    @abstractmethod
    def obtener(mi, instruccion:str, parametros:list, pagina:int, maximo:int, contenido:int) -> tuple:
        ...

    @abstractmethod
    def crear_filtro(mi, filtro:str) -> str:
        ...


# --------------------------------------------------
# Interface: I_ConectorLlm
# --------------------------------------------------
class I_ConectorLlm(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura por los conectores

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorSpi
# --------------------------------------------------
class I_ConectorSpi(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura por los conectores

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorDisco
# --------------------------------------------------
class I_ConectorDisco(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def normalizar_nombre(mi, nombre:str, extension:str=None, largo:int=100, auto:bool=False) -> str:
        ...

    @abstractmethod
    def generar_nombre(mi, nombre:str, unico:bool=True) -> str:
        ...

    @abstractmethod
    def escribir(mi, contenido: BinaryIO | TextIO, nombre:str, modo:str='') -> str:
        ...

    @abstractmethod
    def abrir(mi, nombre:str, modo:str='') -> BinaryIO | TextIO:
        ...

    @abstractmethod
    def eliminar(mi, nombre:str) -> bool:
        ...

    @abstractmethod
    def crear_carpeta(mi, nombre:str, antecesores:bool=False) -> str:
        ...

    @abstractmethod
    def eliminar_carpeta(mi, nombre:str) ->bool:
        ...

    @abstractmethod
    def comprobar_ruta(mi, nombre:str, tipo:str='') -> bool:
        ...

    @abstractmethod
    def listar_archivos(mi, nombre:str, extension:str='*') -> List[_Archivo]:
        ...


# --------------------------------------------------
# Interface: I_Comunicador
# --------------------------------------------------
class I_Comunicador(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura web

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        ...

    @abstractmethod
    def determinar_formato(mi, formato:str=None) -> str:
        ...

    @abstractmethod
    def cargar_archivo(mi, portador:_CargaArchivo, unico:bool=False) -> _CargaArchivo:
        ...
    
    @abstractmethod
    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='.') -> str:
        ...

    @abstractmethod
    def exportar_contenido(mi, formato:str, info:dict={}, guardar:bool=False):
        ...

    @abstractmethod
    def obtener_nombre_archivo(mi, info:dict, extension:str='', largo:int=250, auto:bool=False) -> str:
        ...

    @abstractmethod
    def comprobar_plantilla(mi, opciones:dict, tipo:str='') -> tuple:
        ...

    @abstractmethod
    def generar_encabezados(mi, tipo_mime:str, charset:str='', disposicion:str='inline', nombre_archivo:str='') -> dict:
        ...

    @abstractmethod
    def transferir_contexto(mi) -> dict:
        ...


# --------------------------------------------------
# ClaseModelo: Configuracion
# --------------------------------------------------
class Configuracion(BaseSettings):
    aplicacion: str = ''
    servicio: str = ''
    zona_horaria: str = ''
    dominio: str = ''
    dir_locales: str = ''
    ruta_temp: str = ''
    idiomas_disponibles: list = []
    api_keys: dict = {}
    secret_key: str = ''
    algoritmo_jwt: str = ''
    ruta_servicio: str = ''
    nivel_registro: str = ''
    raiz_api: str = ''
    app_web: str = ''
    frontend: str = ''
    basedatos_fuente: str = ''
    basedatos_clase: str = ''
    basedatos_nombre: str = ''
    basedatos_ruta: str = ''
    basedatos_url: str = ''
    basedatos_usuario: str = ''
    basedatos_password: str = ''
    almacen_fuente: str = ''
    almacen_clase: str = ''
    almacen_nombre: str = ''
    almacen_ruta: str = ''
    almacen_apikey: str = ''
    almacen_url: str = ''
    almacen_usuario: str = ''
    almacen_password: str = ''
    disco_fuente: str = ''
    disco_clase: str = ''
    disco_nombre: str = ''
    disco_ruta: str = ''
    disco_id: str = ''
    disco_location: str = ''
    disco_key: str = ''
    disco_secret: str = ''
    llm_fuente: str = ''
    llm_clase: str = ''
    llm_nombre: str = ''
    llm_ruta: str = ''
    llm_apikey: str = ''
    llm_url: str = ''
    spi_fuente: str = ''
    spi_clase: str = ''
    spi_nombre: str = ''
    spi_ruta: str = ''
    spi_apikey: str = ''
    spi_url: str = ''
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='',
        extra='ignore',
    )
    def basedatos(mi) -> Dict:
        return dict({
            'fuente': mi.basedatos_fuente,
            'clase': mi.basedatos_clase,
            'nombre': mi.basedatos_nombre,
            'ruta': mi.basedatos_ruta,
            'url': mi.basedatos_url,
            'usuario': mi.basedatos_usuario,
            'password': mi.basedatos_password
        })
    def disco(mi) -> Dict:
        return dict({
            'fuente': mi.disco_fuente,
            'clase': mi.disco_clase,
            'nombre': mi.disco_nombre,
            'ruta': mi.disco_ruta,
            'id': mi.disco_id,
            'location': mi.disco_location,
            'key': mi.disco_key,
            'secret': mi.disco_secret
        })
    def almacen(mi) -> Dict:
        return dict({
            'fuente': mi.almacen_fuente,
            'clase': mi.almacen_clase,
            'nombre': mi.almacen_nombre,
            'ruta': mi.almacen_ruta,
            'url': mi.almacen_url,
            'apikey': mi.almacen_apikey,
            'usuario': mi.almacen_usuario,
            'password': mi.almacen_password
        })
    def llm(mi) -> Dict:
        return dict({
            'fuente': mi.llm_fuente,
            'clase': mi.llm_clase,
            'nombre': mi.llm_nombre,
            'ruta': mi.llm_ruta,
            'url': mi.llm_url,
            'apikey': mi.llm_apikey,
        })
    def spi(mi) -> Dict:
        return dict({
            'fuente': mi.spi_fuente,
            'clase': mi.spi_clase,
            'nombre': mi.spi_nombre,
            'ruta': mi.spi_ruta,
            'url': mi.spi_url,
            'apikey': mi.spi_apikey,
        })
    def iniciar(mi, ruta_archivo:str, aplicacion:str):
        import os
        mi.ruta_servicio = Path(ruta_archivo).parent.as_posix()
        if mi.ruta_servicio:
            ruta = Path(mi.ruta_servicio)
            mi.servicio = ruta.name if ruta.parts else ''
            mi.aplicacion = aplicacion
            mi.app_web = os.getenv('APP_WEB', '')
            mi.raiz_api = os.getenv('RAIZ_API', '')
            mi.frontend = os.getenv('ALIAS_FRONTEND', '')
    def web(mi) -> Dict:
        return {
            'aplicacion': mi.aplicacion,
            'servicio': mi.servicio,
            'dominio': mi.dominio,
            'dir_locales': mi.dir_locales,
            'ruta_temp': mi.ruta_temp,
            'ruta_servicio': mi.ruta_servicio,
            'zona_horaria': mi.zona_horaria,
            'idiomas_disponibles': mi.idiomas_disponibles,
            'app_web': mi.app_web,
            'raiz_api': mi.raiz_api,
            'frontend': mi.frontend,
        }
    def autenticacion(mi) -> Dict:
        return dict({
            'algoritmo_jwt': mi.algoritmo_jwt,
            'secret_key': mi.secret_key,
            'api_keys': mi.api_keys,
            'ruta_temp': mi.ruta_temp,
        })
    def traductor(mi) -> Dict:
        return dict({
            'dominio': mi.dominio,
            'dir_locales': mi.dir_locales,
            'idiomas_disponibles': mi.idiomas_disponibles,
            'zona_horaria': mi.zona_horaria,
        })


# --------------------------------------------------
# Clase: Exportador
# --------------------------------------------------
class Exportador:
    def __init__(mi, config_web:dict):
        mi.config_web:dict = config_web or {}

    def obtener_ruta(mi):
        ruta_temp = mi.config_web.get('ruta_temp', '')
        ruta = Path(ruta_temp) / 'archivos'
        ruta = ruta.resolve()
        if not ruta.exists():
            return ''
        return ruta.as_posix()

    def generar(mi, contenido:str='', opciones:dict={}):
        raise NotImplementedError()


# --------------------------------------------------
# Clase: Operador
# --------------------------------------------------
class Operador:
    def __init__(mi, configuracion:Configuracion):
        mi.configuracion:Configuracion = configuracion
        mi.inyectar_conectores(mi.configuracion)

    # --------------------------------------------------
    # Métodos privados

    def _importar_conector(mi, config:dict):
        import importlib
        try:
            modulo = getattr(
                importlib.import_module(f"{_Constantes.RUTA_CONECTORES}.{config.get('fuente')}"),
                config.get('clase'))
            if modulo:
                return modulo
            return None
        except Exception as e:
            print(e)
            return None

    # --------------------------------------------------
    # Métodos públicos

    def inyectar_conectores(mi, configuracion:Configuracion):
        try:
            if configuracion.basedatos_clase:
                conector_basedatos = mi._importar_conector(mi.configuracion.basedatos())
                if conector_basedatos:
                    mi.basedatos:I_ConectorBasedatos = conector_basedatos()
            if configuracion.almacen_clase:
                conector_almacen = mi._importar_conector(mi.configuracion.almacen())
                if conector_almacen:
                    mi.almacen:I_ConectorAlmacen = conector_almacen()
            if configuracion.disco_clase:
                conector_disco = mi._importar_conector(mi.configuracion.disco())
                if conector_disco:
                    mi.disco:I_ConectorDisco = conector_disco(mi.configuracion.disco())
            if configuracion.llm_clase:
                conector_llm = mi._importar_conector(mi.configuracion.llm())
                if conector_llm:
                    mi.llm:I_ConectorLlm = conector_llm()
            if configuracion.spi_clase:
                conector_spi = mi._importar_conector(mi.configuracion.spi())
                if conector_spi:
                    mi.spi:I_ConectorSpi = conector_spi()
        except Exception as e:
            print(e)


# --------------------------------------------------
# Clase: Controlador
# --------------------------------------------------
class Controlador:
    def __init__(mi, configuracion:Configuracion, comunicador:I_Comunicador):
        mi.configuracion:Configuracion = configuracion
        mi.comunicador:I_Comunicador = comunicador
        contexto = mi.comunicador.transferir_contexto()
        sesion = contexto.get('sesion')
        mi.sesion:dict = sesion or {}


# --------------------------------------------------
# Funcion: cargar_configuracion
# --------------------------------------------------
@lru_cache
def cargar_configuracion(modelo:Configuracion, paquete:str, aplicacion:str, entorno:str=None):
    archivo_env = _Funciones.obtener_ruta_env(paquete, entorno)
    configuracion:Configuracion = modelo(_env_file=archivo_env)
    configuracion.iniciar(archivo_env, aplicacion)
    return configuracion


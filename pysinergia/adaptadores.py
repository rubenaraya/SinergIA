# pysinergia\adaptadores.py

from abc import (ABC, ABCMeta, abstractmethod)
from typing import (
    List, Dict
)
import json

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Adaptadores)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import Field, field_validator

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import (
    ArchivoCargado as ArchivoCargado,
)

# --------------------------------------------------
# Interface: I_Traductor
# --------------------------------------------------
class I_Traductor(metaclass=ABCMeta):

    @abstractmethod
    def asignar_idioma(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None, dominio_idioma:str=None, ruta_locales:str=None) -> str:
        ...

    @abstractmethod
    def abrir_traduccion(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None, dominio_idioma:str=None, ruta_locales:str=None):
        ...

    @abstractmethod
    def traducir_textos(mi, info:dict={}, claves:list=[]) -> dict:
        ...

    @abstractmethod
    def _(mi, texto:str='') -> str:
        ...

    @abstractmethod
    def idioma_actual(mi) -> str:
        ...

    @abstractmethod
    def fecha_hora(mi, fecha_hora:str=None, zona_horaria:str=None, formato_fecha:str=None) -> dict:
        ...


# --------------------------------------------------
# Interface: I_Comunicador
# --------------------------------------------------
class I_Comunicador(metaclass=ABCMeta):

    @abstractmethod
    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        ...

    @abstractmethod
    def elegir_conversion(mi, conversion:str=None) -> str:
        ...

    @abstractmethod
    def cargar_archivo(mi, portador:ArchivoCargado, unico:bool=False) -> ArchivoCargado:
        ...
    
    @abstractmethod
    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='.') -> str:
        ...

    @abstractmethod
    def exportar_contenido(mi, conversion:str, info:dict={}, guardar:bool=False):
        ...

    @abstractmethod
    def obtener_nombre_descarga(mi, info:dict, extension:str='', largo:int=250, auto:bool=False) -> str:
        ...

    @abstractmethod
    def generar_encabezados(mi, tipo_mime:str, charset:str='', disposicion:str='inline', nombre_descarga:str='') -> dict:
        ...

    @abstractmethod
    def transferir_contexto(mi, datos:dict=None) -> dict:
        ...

    @abstractmethod
    def traspasar_traductor(mi) -> I_Traductor:
        ...


# --------------------------------------------------
# ClaseModelo: Configuracion
# --------------------------------------------------
class Configuracion(BaseSettings):
    # Aplicacion Global
    APP_GLOBAL: str = Field(default='')
    RAIZ_GLOBAL: str = Field(default='')
    RUTA_RAIZ: str = Field(default='')
    RUTA_LOGS: str = Field(default='')
    IDIOMAS_DISPONIBLES: List[str] = Field(default=[])
    ARCHIVO_LOGS: str = Field(default='')
    ALIAS_FRONTEND: str = Field(default='')
    DOMINIO_IDIOMA: str = Field(default='')
    RUTA_LOCALES: str = Field(default='')
    NIVEL_REGISTRO: str = Field(default='')
    # Aplicacion Personalizada
    APLICACION: str = Field(default='')
    NOMBRE_PWA: str = ''
    TITULO_PWA: str = ''
    DESCRIPCION_PWA: str = ''
    API_KEYS: Dict[str,str] = Field(default={})
    SECRET_KEY: str = ''
    ALGORITMO_JWT: str = ''
    ZONA_HORARIA: str = ''
    FORMATO_FECHA: str = ''
    RUTA_TEMP: str = ''
    # Microservicio especifico
    MICROSERVICIO: str = Field(default='')
    RUTA_MICROSERVICIO: str = Field(default='')
    BASEDATOS_FUENTE: str = ''
    BASEDATOS_CLASE: str = ''
    BASEDATOS_NOMBRE: str = ''
    BASEDATOS_RUTA: str = ''
    BASEDATOS_USUARIO: str = ''
    BASEDATOS_PASSWORD: str = ''
    ALMACEN_FUENTE: str = ''
    ALMACEN_CLASE: str = ''
    ALMACEN_NOMBRE: str = ''
    ALMACEN_RUTA: str = ''
    ALMACEN_APIKEY: str = ''
    ALMACEN_URL: str = ''
    ALMACEN_USUARIO: str = ''
    ALMACEN_PASSWORD: str = ''
    DISCO_FUENTE: str = ''
    DISCO_CLASE: str = ''
    DISCO_NOMBRE: str = ''
    DISCO_RUTA: str = ''
    DISCO_ID: str = ''
    DISCO_LOCATION: str = ''
    DISCO_KEY: str = ''
    DISCO_SECRET: str = ''
    LLM_FUENTE: str = ''
    LLM_CLASE: str = ''
    LLM_NOMBRE: str = ''
    LLM_RUTA: str = ''
    LLM_APIKEY: str = ''
    LLM_URL: str = ''
    SPI_FUENTE: str = ''
    SPI_CLASE: str = ''
    SPI_NOMBRE: str = ''
    SPI_RUTA: str = ''
    SPI_APIKEY: str = ''
    SPI_URL: str = ''
    model_config = SettingsConfigDict(
        env_prefix='',
        extra='ignore',
        case_sensitive=True,
        validate_assignment=True,
        validate_default=True,
    )

    @field_validator('IDIOMAS_DISPONIBLES', mode='before')
    @classmethod
    def parse_json_list(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                pass
        return v or []

    @field_validator('API_KEYS', mode='before')
    @classmethod
    def parse_json_dict(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                pass
        return v or {}

    def basedatos(mi) -> dict:
        return dict({
            'fuente': mi.BASEDATOS_FUENTE,
            'clase': mi.BASEDATOS_CLASE,
            'nombre': mi.BASEDATOS_NOMBRE,
            'ruta': mi.BASEDATOS_RUTA,
            'usuario': mi.BASEDATOS_USUARIO,
            'password': mi.BASEDATOS_PASSWORD,
        })
    def disco(mi) -> dict:
        return dict({
            'fuente': mi.DISCO_FUENTE,
            'clase': mi.DISCO_CLASE,
            'nombre': mi.DISCO_NOMBRE,
            'ruta': mi.DISCO_RUTA,
            'id': mi.DISCO_ID,
            'location': mi.DISCO_LOCATION,
            'key': mi.DISCO_KEY,
            'secret': mi.DISCO_SECRET,
        })
    def almacen(mi) -> dict:
        return dict({
            'fuente': mi.ALMACEN_FUENTE,
            'clase': mi.ALMACEN_CLASE,
            'nombre': mi.ALMACEN_NOMBRE,
            'ruta': mi.ALMACEN_RUTA,
            'url': mi.ALMACEN_URL,
            'apikey': mi.ALMACEN_APIKEY,
            'usuario': mi.ALMACEN_USUARIO,
            'password': mi.ALMACEN_PASSWORD,
        })
    def llm(mi) -> dict:
        return dict({
            'fuente': mi.LLM_FUENTE,
            'clase': mi.LLM_CLASE,
            'nombre': mi.LLM_NOMBRE,
            'ruta': mi.LLM_RUTA,
            'url': mi.LLM_URL,
            'apikey': mi.LLM_APIKEY,
        })
    def spi(mi) -> dict:
        return dict({
            'fuente': mi.SPI_FUENTE,
            'clase': mi.SPI_CLASE,
            'nombre': mi.SPI_NOMBRE,
            'ruta': mi.SPI_RUTA,
            'url': mi.SPI_URL,
            'apikey': mi.SPI_APIKEY,
        })
    def web(mi) -> dict:
        return {
            'APLICACION': mi.APLICACION,
            'MICROSERVICIO': mi.MICROSERVICIO,
            'RUTA_MICROSERVICIO': mi.RUTA_MICROSERVICIO,
            'RUTA_RAIZ': mi.RUTA_RAIZ,
            'RUTA_TEMP': mi.RUTA_TEMP,
            'APP_GLOBAL': mi.APP_GLOBAL,
            'RAIZ_GLOBAL': mi.RAIZ_GLOBAL,
            'ALIAS_FRONTEND': mi.ALIAS_FRONTEND,
            'IDIOMAS_DISPONIBLES': mi.IDIOMAS_DISPONIBLES,
            'ARCHIVO_LOGS': mi.ARCHIVO_LOGS,
            'ZONA_HORARIA': mi.ZONA_HORARIA,
            'FORMATO_FECHA': mi.FORMATO_FECHA,
            'NOMBRE_PWA': mi.NOMBRE_PWA,
            'TITULO_PWA': mi.TITULO_PWA,
            'DESCRIPCION_PWA': mi.DESCRIPCION_PWA,
        }
    def autenticacion(mi) -> dict:
        return dict({
            'ALGORITMO_JWT': mi.ALGORITMO_JWT,
            'SECRET_KEY': mi.SECRET_KEY,
            'API_KEYS': mi.API_KEYS,
            'RUTA_TEMP': mi.RUTA_TEMP,
        })
    def traductor(mi) -> dict:
        return dict({
            'DOMINIO_IDIOMA': mi.DOMINIO_IDIOMA,
            'RUTA_LOCALES': mi.RUTA_LOCALES,
            'IDIOMAS_DISPONIBLES': mi.IDIOMAS_DISPONIBLES,
            'ZONA_HORARIA': mi.ZONA_HORARIA,
            'FORMATO_FECHA': mi.FORMATO_FECHA,
        })


# --------------------------------------------------
# Clase: Repositorio
# --------------------------------------------------
class Repositorio(ABC):
    def __init__(mi, configuracion:Configuracion):
        mi.configuracion:Configuracion = configuracion
        mi.inyectar_conectores(mi.configuracion)

    # --------------------------------------------------
    # Métodos privados

    def _importar_conector(mi, config:dict):
        import importlib
        try:
            fuente = config.get('fuente')
            clase = config.get('clase')
            modulo = getattr(importlib.import_module(f"pysinergia.conectores.{fuente}"), clase)
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
            if configuracion.BASEDATOS_CLASE:
                from pysinergia.conectores.basedatos import Basedatos
                conector_basedatos = mi._importar_conector(mi.configuracion.basedatos())
                if conector_basedatos:
                    mi.basedatos:Basedatos = conector_basedatos()
            if configuracion.ALMACEN_CLASE:
                from pysinergia.conectores.almacen import Almacen
                conector_almacen = mi._importar_conector(mi.configuracion.almacen())
                if conector_almacen:
                    mi.almacen:Almacen = conector_almacen()
            if configuracion.DISCO_CLASE:
                from pysinergia.conectores.disco import Disco
                conector_disco = mi._importar_conector(mi.configuracion.disco())
                if conector_disco:
                    mi.disco:Disco = conector_disco(mi.configuracion.disco())
            if configuracion.LLM_CLASE:
                from pysinergia.conectores.llm import Llm
                conector_llm = mi._importar_conector(mi.configuracion.llm())
                if conector_llm:
                    mi.llm:Llm = conector_llm()
            if configuracion.SPI_CLASE:
                from pysinergia.conectores.spi import Spi
                conector_spi = mi._importar_conector(mi.configuracion.spi())
                if conector_spi:
                    mi.spi:Spi = conector_spi()
        except Exception as e:
            print(e)


# --------------------------------------------------
# Clase: Controlador
# --------------------------------------------------
class Controlador(ABC):
    def __init__(mi, configuracion:Configuracion, comunicador:I_Comunicador):
        mi.configuracion:Configuracion = configuracion
        mi.comunicador:I_Comunicador = comunicador
        contexto = mi.comunicador.transferir_contexto()
        sesion = contexto.get('sesion')
        mi.sesion:dict = sesion or {}


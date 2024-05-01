# pysinergia\adaptadores.py

from abc import (ABCMeta, abstractmethod)
from typing import Dict

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Adaptadores)
from pydantic_settings import (BaseSettings, SettingsConfigDict)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import Constantes as _Constantes

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

    class FORMATO:
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
# Interface: I_ConectorDisco
# --------------------------------------------------
class I_ConectorDisco(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura por los conectores

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
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
# ClaseModelo: Configuracion
# --------------------------------------------------
class Configuracion(BaseSettings):
    aplicacion: str = ''
    servicio: str = ''
    nivel_registro: str = ''
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
    disco_apikey: str = ''
    disco_url: str = ''
    disco_usuario: str = ''
    disco_password: str = ''
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
    def disco(mi) -> Dict:
        return dict({
            'fuente': mi.disco_fuente,
            'clase': mi.disco_clase,
            'nombre': mi.disco_nombre,
            'ruta': mi.disco_ruta,
            'url': mi.disco_url,
            'apikey': mi.disco_apikey,
            'usuario': mi.disco_usuario,
            'password': mi.disco_password
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
    def identificar(mi, aplicacion:str, servicio:str):
        mi.aplicacion = aplicacion
        mi.servicio = servicio


# --------------------------------------------------
# Clase: Operador
# --------------------------------------------------
class Operador():
    def __init__(mi, config:Configuracion):
        mi.config:Configuracion = config
        mi.inyectar_conectores(mi.config)

    # --------------------------------------------------
    # Métodos privados

    def _importar_modulo(mi, config:dict):
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

    def inyectar_conectores(mi, config:Configuracion):
        try:
            if config.basedatos_clase:
                conector_basedatos = mi._importar_modulo(config=mi.config.basedatos())
                if conector_basedatos:
                    mi.basedatos:I_ConectorBasedatos = conector_basedatos()
            if config.disco_clase:
                conector_disco = mi._importar_modulo(mi.config.disco())
                if conector_disco:
                    mi.disco:I_ConectorDisco = conector_disco()
            if config.almacen_clase:
                conector_almacen = mi._importar_modulo(mi.config.almacen())
                if conector_almacen:
                    mi.almacen:I_ConectorAlmacen = conector_almacen()
            if config.llm_clase:
                conector_llm = mi._importar_modulo(mi.config.llm())
                if conector_llm:
                    mi.llm:I_ConectorLlm = conector_llm()
            if config.spi_clase:
                conector_spi = mi._importar_modulo(mi.config.spi())
                if conector_spi:
                    mi.spi:I_ConectorSpi = conector_spi()
        except Exception as e:
            print(e)


# --------------------------------------------------
# Interface: I_Emisor
# --------------------------------------------------
class I_Emisor(metaclass=ABCMeta):
    # Implementada en la capa web por EmisorWeb

    # --------------------------------------------------
    # Métodos obligatorios

    @abstractmethod
    def entregar_respuesta(mi, resultado:dict):
        ...


# --------------------------------------------------
# Interface: I_Exportador
# --------------------------------------------------
class I_Exportador(metaclass=ABCMeta):
    # Implementada en la capa de infraestructura por los exportadores
    ...


# --------------------------------------------------
# Clase: Controlador
# --------------------------------------------------
class Controlador():
    def __init__(mi, config:Configuracion, emisor:I_Emisor):
        mi.emisor:I_Emisor = emisor
        mi.config:Configuracion = config


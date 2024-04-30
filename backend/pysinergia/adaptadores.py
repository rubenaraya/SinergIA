# backend\pysinergia\adaptadores.py

from abc import (ABCMeta, abstractmethod)

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Adaptadores)
from pydantic_settings import BaseSettings, SettingsConfigDict

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia.globales import Constantes
from backend.pysinergia.servicio import I_Operador

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
    def insertar(mi, sql:str, parametros:list) -> int:
        ...
    @abstractmethod
    def actualizar(mi, sql:str, parametros:list) -> int:
        ...
    @abstractmethod
    def eliminar(mi, sql:str, parametros:list) -> int:
        ...
    @abstractmethod
    def leer(mi, sql:str, parametros:list, contenido:int) -> tuple:
        ...
    @abstractmethod
    def obtener(mi, sql:str, parametros:list, pagina:int, maximo:int, contenido:int) -> tuple:
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
# Clase: Operador
# --------------------------------------------------
class Operador(I_Operador):

    # --------------------------------------------------
    # Métodos privados

    def _importar_modulo(mi, config:dict):
        import importlib
        try:
            modulo = getattr(
                importlib.import_module(f"{Constantes.RUTA_CONECTORES}.{config.get('modulo')}"),
                config.get('clase'))
            if modulo:
                return modulo
            return None
        except Exception as e:
            print(e)
            return None

    # --------------------------------------------------
    # Métodos públicos

    def inyectar_conectores(mi, basedatos:dict=None, almacen:dict=None, disco:dict=None, llm:dict=None, spi:dict=None):
        try:
            if basedatos:
                conector_basedatos = mi._importar_modulo(basedatos)
                if conector_basedatos:
                    mi.basedatos:I_ConectorBasedatos = conector_basedatos()
            if disco:
                conector_disco = mi._importar_modulo(disco)
                if conector_disco:
                    mi.disco:I_ConectorDisco = conector_disco()
            if almacen:
                conector_almacen = mi._importar_modulo(almacen)
                if conector_almacen:
                    mi.almacen:I_ConectorAlmacen = conector_almacen()
            if llm:
                conector_llm = mi._importar_modulo(llm)
                if conector_llm:
                    mi.llm:I_ConectorLlm = conector_llm()
            if spi:
                conector_spi = mi._importar_modulo(spi)
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
    def __init__(mi, emisor:I_Emisor):
        mi.emisor:I_Emisor = emisor


# --------------------------------------------------
# ClaseModelo: Configuracion
# --------------------------------------------------
class Configuracion(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='',
        extra='ignore',
    )
    ruta_logs: str = ''
    nivel_registro: str = ''
    ruta_repositorios: str = ''
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


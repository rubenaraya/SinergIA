# backend\pysinergia\adaptadores.py

from abc import (ABCMeta, abstractmethod)

from backend.pysinergia.servicio import I_Operador
from backend.pysinergia.globales import Constantes

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

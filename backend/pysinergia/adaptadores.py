# backend\pysinergia\adaptadores.py

from abc import (ABCMeta, abstractmethod)

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
    # Métodos públicos

    def inyectar_conectores(mi, basedatos:str=None, almacen:str=None, disco:str=None, llm:str=None, spi:str=None):
        import importlib
        ruta_conectores = 'backend.pysinergia.conectores'
        try:
            if basedatos:
                conector_basedatos = getattr(importlib.import_module(ruta_conectores), basedatos)
                if conector_basedatos:
                    mi.basedatos:I_ConectorBasedatos = conector_basedatos()
            if disco:
                conector_disco = getattr(importlib.import_module(ruta_conectores), disco)
                if conector_disco:
                    mi.disco:I_ConectorDisco = conector_disco()
            if almacen:
                conector_almacen = getattr(importlib.import_module(ruta_conectores), almacen)
                if conector_almacen:
                    mi.almacen:I_ConectorAlmacen = conector_almacen()
            if llm:
                conector_llm = getattr(importlib.import_module(ruta_conectores), llm)
                if conector_llm:
                    mi.llm:I_ConectorLlm = conector_llm()
            if spi:
                conector_spi = getattr(importlib.import_module(ruta_conectores), spi)
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

# backend\pysinergia\adaptadores.py

from abc import (ABCMeta, abstractmethod)

from backend.pysinergia.servicio import I_Operador

# --------------------------------------------------
# Interface: I_ConectorAlmacen
# --------------------------------------------------
class I_ConectorAlmacen(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorBasedatos
# --------------------------------------------------
class I_ConectorBasedatos(metaclass=ABCMeta):

    class CONTENIDO:
        DICCIONARIO = 1
        TUPLA = 2

    class CLASE:
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
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorLlm
# --------------------------------------------------
class I_ConectorLlm(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorSpi
# --------------------------------------------------
class I_ConectorSpi(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Clase: Operador
# --------------------------------------------------
class Operador(I_Operador):
    ...


# --------------------------------------------------
# Interface: I_Emisor
# --------------------------------------------------
class I_Emisor(metaclass=ABCMeta):
    @abstractmethod
    def entregar_respuesta(mi, resultado:dict):
        ...


# --------------------------------------------------
# Interface: I_Exportador
# --------------------------------------------------
class I_Exportador(metaclass=ABCMeta):
    ...


# --------------------------------------------------
# Clase: Controlador
# --------------------------------------------------
class Controlador():
    def __init__(mi, emisor:I_Emisor):
        mi.emisor:I_Emisor = emisor

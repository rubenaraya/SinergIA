# backend\pysinergia\servicio.py

from abc import (ABCMeta, abstractmethod)

from backend.pysinergia.dominio import ModeloPeticion, ModeloRespuesta

# --------------------------------------------------
# Interface: I_Operador
# --------------------------------------------------
class I_Operador(metaclass=ABCMeta):

    basedatos = None
    almacen = None
    llm = None
    disco = None
    spi = None

    @abstractmethod
    def inyectar_conectores(mi, basedatos:str=None, almacen:str=None, disco:str=None, llm:str=None, spi:str=None):
        ...


# --------------------------------------------------
# Interface: I_Servicio
# --------------------------------------------------
class I_Servicio(metaclass=ABCMeta):
    @abstractmethod
    def solicitar_accion(mi, accion:int, peticion:ModeloPeticion):
        ...


# --------------------------------------------------
# Clase: Servicio
# --------------------------------------------------
class Servicio(I_Servicio):
    ...

# --------------------------------------------------
# Clase: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(ModeloRespuesta):
    codigo: int | None = 200
    tipo: str | None = 'EXITO'
    mensaje: str | None = ''
    resultado: dict | None = {}

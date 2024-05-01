# pysinergia\servicio.py

from abc import (ABCMeta, abstractmethod)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import (
    ModeloPeticion,
    ModeloRespuesta,
)

# --------------------------------------------------
# Interface: I_Operador
# --------------------------------------------------
class I_Operador(metaclass=ABCMeta):

    """
    basedatos = None
    almacen = None
    llm = None
    disco = None
    spi = None
    """

    @abstractmethod
    def inyectar_conectores(mi, config):
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
# ClaseModelo: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(ModeloRespuesta):
    codigo: int | None = 200
    tipo: str | None = 'EXITO'
    mensaje: str | None = ''
    resultado: dict | None = {}
    esquemas: dict | None = {}


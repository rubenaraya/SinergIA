# backend\pysinergia\infra_interfaz.py

from abc import (ABCMeta, abstractmethod)

# --------------------------------------------------
# Interface: I_Exportador
# --------------------------------------------------
class I_Exportador(metaclass=ABCMeta):
    @abstractmethod
    def generar(mi, opciones:dict) -> str:
        ...

# --------------------------------------------------
# Interface: I_ReceptorPeticion
# --------------------------------------------------
class I_ReceptorPeticion(metaclass=ABCMeta):
    @abstractmethod
    def recibir_peticion(mi) -> dict:
        ...

# --------------------------------------------------
# Interface: I_EmisorRespuesta
# --------------------------------------------------
class I_EmisorRespuesta(metaclass=ABCMeta):
    @abstractmethod
    def crear_respuesta(mi) -> str:
        ...


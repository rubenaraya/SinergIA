# backend\pysinergia\servicio.py

from abc import (ABCMeta, abstractmethod)

# --------------------------------------------------
# Interface: I_Operador
# --------------------------------------------------
class I_Operador(metaclass=ABCMeta):
    ...


# --------------------------------------------------
# Interface: I_Servicio
# --------------------------------------------------
class I_Servicio(metaclass=ABCMeta):
    @abstractmethod
    def solicitar_accion(mi, accion:int, peticion:dict):
        ...


# --------------------------------------------------
# Clase: Servicio
# --------------------------------------------------
class Servicio(I_Servicio):
    ...

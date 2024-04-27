# --------------------------------------------------
# Extensible: Servicio
# --------------------------------------------------

from abc import (ABCMeta, abstractmethod)

class I_Operador(metaclass=ABCMeta):
    ...

class I_Servicio(metaclass=ABCMeta):
    @abstractmethod
    def solicitar_accion(mi, accion, peticion):
        ...

class Servicio(I_Servicio):
    ...

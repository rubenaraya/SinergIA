# backend\pysinergia\__init__.py

# --------------------------------------------------
# Componentes de PySinergIA
# --------------------------------------------------

from backend.pysinergia.dominio import Entidad
from backend.pysinergia.servicio import Servicio
from backend.pysinergia.adaptadores import (
    Controlador, 
    Operador, 
    I_ConectorBasedatos, 
    I_ConectorAlmacen, 
    I_ConectorDisco, 
    I_ConectorLlm, 
    I_ConectorSpi, 
    I_Exportador
)
from backend.pysinergia.web import (EmisorWeb, ServidorApi)

__all__ = [
    'Operador',
    'Controlador',
    'Entidad',
    'Servicio',
    'EmisorWeb',
    'ServidorApi',
    'I_ConectorBasedatos',
    'I_ConectorAlmacen',
    'I_ConectorDisco',
    'I_ConectorLlm',
    'I_ConectorSpi',
    'I_Exportador'
]

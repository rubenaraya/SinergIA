# backend\pysinergia\__init__.py

# --------------------------------------------------
# Componentes públicos de PySinergIA
# --------------------------------------------------

from backend.pysinergia.globales import (
    Constantes,
    Funciones,
    Json,
)
from backend.pysinergia.dominio import (
    Entidad,
    ModeloPeticion,
    ModeloRespuesta,
)
from backend.pysinergia.servicio import (
    Servicio,
    RespuestaResultado,
    I_Operador,
)
from backend.pysinergia.adaptadores import (
    Controlador, 
    Operador, 
    I_ConectorBasedatos, 
    I_ConectorAlmacen, 
    I_ConectorDisco, 
    I_ConectorLlm, 
    I_ConectorSpi, 
    I_Exportador,
)
from backend.pysinergia.web import (
    EmisorWeb,
    RegistradorLogs,
    ServidorApi,
)

__all__ = [
    'Constantes',
    'Funciones',
    'Json',
    'Entidad',
    'ModeloPeticion',
    'ModeloRespuesta',
    'Servicio',
    'RespuestaResultado',
    'I_Operador',
    'Controlador',
    'Operador',
    'I_ConectorBasedatos',
    'I_ConectorAlmacen',
    'I_ConectorDisco',
    'I_ConectorLlm',
    'I_ConectorSpi',
    'I_Exportador',
    'EmisorWeb',
    'RegistradorLogs',
    'ServidorApi',
]

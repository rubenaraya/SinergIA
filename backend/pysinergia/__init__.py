# backend\pysinergia\__init__.py

# --------------------------------------------------
# Componentes de PySinergIA
# --------------------------------------------------

from backend.pysinergia.globales import ( GestorEstado, NotificadorEventos, Constantes, Funciones )
from backend.pysinergia.adaptadores import ( Operador, ValidadorDatos )
from backend.pysinergia.adaptadores import ( ComunicadorWeb, TraductorIdiomas, PresentadorContenidos )
from backend.pysinergia.nucleo import ( Coordinador, ControladorAcceso, PortadorInformacion, ManejadorErrores, RegistradorErrores, ErrorPersonalizado, ProcesadorEsquemas )
from backend.pysinergia.infraestructura import ( ServidorApi, Enrutador, ReceptorPeticion, EmisorRespuesta )

__all__ = [
    'Operador', 'ValidadorDatos', 
    'GestorEstado', 'NotificadorEventos', 'Constantes', 'Funciones',
    'ServidorApi', 'Enrutador', 'ReceptorPeticion', 'EmisorRespuesta', 'ComunicadorWeb', 'TraductorIdiomas', 'PresentadorContenidos',
    'Coordinador', 'ControladorAcceso', 'PortadorInformacion', 'ManejadorErrores', 'RegistradorErrores', 'ErrorPersonalizado', 'ProcesadorEsquemas'
]

__version__ = '0.0.1'

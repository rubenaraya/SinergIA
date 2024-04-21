# backend\pysinergia\__init__.py

# --------------------------------------------------
# Componentes de PySinergIA
# --------------------------------------------------

from backend.pysinergia.datos import ( Operador, ValidadorDatos )
from backend.pysinergia.globales import ( GestorEstados, NotificadorEventos, Constantes, Funciones )
from backend.pysinergia.interfaz import ( ServidorApi, Enrutador, ReceptorPeticion, EmisorRespuesta, ComunicadorWeb, TraductorIdiomas, PresentadorContenidos )
from backend.pysinergia.nucleo import ( Coordinador, ControladorAcceso, PortadorInformacion, ManejadorErrores, RegistradorErrores, ErrorPersonalizado, ProcesadorEsquemas )

__all__ = [
    'Operador', 'ValidadorDatos', 
    'GestorEstados', 'NotificadorEventos', 'Constantes', 'Funciones',
    'ServidorApi', 'Enrutador', 'ReceptorPeticion', 'EmisorRespuesta', 'ComunicadorWeb', 'TraductorIdiomas', 'PresentadorContenidos',
    'Coordinador', 'ControladorAcceso', 'PortadorInformacion', 'ManejadorErrores', 'RegistradorErrores', 'ErrorPersonalizado', 'ProcesadorEsquemas'
]

__version__ = '0.0.1'

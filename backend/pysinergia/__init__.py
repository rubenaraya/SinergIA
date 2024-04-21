# backend\pysinergia\__init__.py

# --------------------------------------------------
# Componentes de PySinergIA
# --------------------------------------------------

from backend.pysinergia.datos import Operador, ValidadorDatos
from backend.pysinergia.entorno import GestorEstados, GestorEstados, Constantes, Funciones
from backend.pysinergia.interfaz import ServidorApi, Enrutador, ReceptorPeticion, EmisorRespuesta, ComunicadorWeb, TraductorIdiomas, PresentadorContenidos
from backend.pysinergia.nucleo import Coordinador, ControladorAcceso, PortadorInformacion, ManejadorErrores, RegistradorErrores, ErrorPersonalizado, ProcesadorEsquemas
from backend.pysinergia.adaptadores import I_ConectorAlmacen, I_ConectorBasedatos, I_ConectorDisco, I_ConectorLlm, I_ConectorSpi, I_Exportador

__all__ = [
    'Operador', 'ValidadorDatos', 
    'GestorEstados', 'GestorEstados', 'Constantes', 'Funciones',
    'ServidorApi', 'Enrutador', 'ReceptorPeticion', 'EmisorRespuesta', 'ComunicadorWeb', 'TraductorIdiomas', 'PresentadorContenidos',
    'Coordinador', 'ControladorAcceso', 'PortadorInformacion', 'ManejadorErrores', 'RegistradorErrores', 'ErrorPersonalizado', 'ProcesadorEsquemas',
    'I_ConectorAlmacen', 'I_ConectorBasedatos', 'I_ConectorDisco', 'I_ConectorLlm', 'I_ConectorSpi', 'I_Exportador'
]

__version__ = '0.0.1'

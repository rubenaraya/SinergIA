# --------------------------------------------------
# backend\documentos\servicio.py
# --------------------------------------------------

from abc import (ABCMeta, abstractmethod)

# Importaciones de PySinergIA
from pysinergia.servicio import CasosDeUso

# --------------------------------------------------
# Interface: I_RepositorioDocumentos
class I_RepositorioDocumentos(metaclass=ABCMeta):

    @abstractmethod
    def recuperar_lista_documentos(mi, solicitud:dict, roles_sesion:str='') -> dict:
        ...

# --------------------------------------------------
# Clase: CasosDeUsoDocumentos
class CasosDeUsoDocumentos(CasosDeUso):
    def __init__(mi, repositorio:I_RepositorioDocumentos, sesion:dict=None):
        mi.repositorio:I_RepositorioDocumentos = repositorio
        mi.sesion:dict = sesion

    # Clases de constantes

    class ACCIONES:
        BUSCAR = 1
        AGREGAR = 2
        VER = 3

    class PERMISOS:
        BUSCAR = '*'
        AGREGAR = '*'
        VER = '*'

    # Métodos

    def solicitar_accion(mi, accion:ACCIONES, solicitud:dict) -> dict:
        realizar = {
            mi.ACCIONES.BUSCAR: mi._buscar_documentos,
            mi.ACCIONES.AGREGAR: mi._agregar_documento,
            mi.ACCIONES.VER: mi._ver_documento,
        }
        return realizar.get(accion)(solicitud)

    def _buscar_documentos(mi, solicitud:dict):
        entrega:dict = solicitud.get('_dto_contexto', {})
        if mi.autorizar_accion(permisos=mi.PERMISOS.BUSCAR, rechazar=True):
            resultado = mi.repositorio.recuperar_lista_documentos(solicitud, roles_sesion=mi.sesion.get('roles'))
            entrega['descripcion'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}'
            entrega['resultado'] = resultado
        return entrega

    def _agregar_documento(mi, solicitud:dict):
        ...
    
    def _ver_documento(mi, solicitud:dict):
        ...


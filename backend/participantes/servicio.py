# backend\participantes\servicio.py

from pysinergia._dependencias import CasosDeUso
from abc import (ABCMeta, abstractmethod)
from typing import S

# --------------------------------------------------
# Importaciones del Microservicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    PeticionActualizarParticipante,
    PeticionAgregarParticipante,
    ProcedimientoAgregarParticipante,
    ProcedimientoActualizarParticipante,
    ProcedimientoEliminarParticipante,
)

# --------------------------------------------------
# Interface: I_RepositorioParticipantes
# --------------------------------------------------
class I_RepositorioParticipantes(metaclass=ABCMeta):
    # Implementada en la capa de adaptadores por RepositorioParticipantes

    @abstractmethod
    def recuperar_lista_participantes_todos(mi, solicitud:dict, roles_sesion:str='') -> dict:
        ...

    @abstractmethod
    def recuperar_lista_participantes_filtrados(mi, solicitud:dict) -> dict:
        ...

    @abstractmethod
    def recuperar_participante_por_id(mi, solicitud:dict) -> dict:
        ...

    @abstractmethod
    def insertar_nuevo_participante(mi, solicitud:dict) -> dict:
        ...

    @abstractmethod
    def actualizar_participante_por_id(mi, solicitud:dict) -> dict:
        ...

    @abstractmethod
    def eliminar_participante_por_id(mi, solicitud:dict) -> dict:
        ...


# --------------------------------------------------
# Clase: CasosDeUsoParticipantes
# --------------------------------------------------
class CasosDeUsoParticipantes(CasosDeUso):
    def __init__(mi, repositorio:I_RepositorioParticipantes, sesion:dict=None):
        mi.repositorio:I_RepositorioParticipantes = repositorio
        mi.sesion:dict = sesion

    # --------------------------------------------------
    # Clase de constantes: ACCIONES

    class ACCIONES:
        BUSCAR = 1
        AGREGAR = 2
        VER = 3
        ACTUALIZAR = 4
        ELIMINAR = 5

    class PERMISOS:
        BUSCAR = '*'
        AGREGAR = 'Admin'
        VER = '*'
        ACTUALIZAR = 'Admin,Ejecutivo'
        ELIMINAR = 'Admin'

    # --------------------------------------------------
    # Métodos públicos

    def solicitar_accion(mi, accion:ACCIONES, solicitud:dict) -> dict:
        realizar = {
            mi.ACCIONES.BUSCAR: mi._buscar_participantes,
            mi.ACCIONES.AGREGAR: mi._agregar_participante,
            mi.ACCIONES.ACTUALIZAR: mi._actualizar_participante,
            mi.ACCIONES.ELIMINAR: mi._eliminar_participante,
            mi.ACCIONES.VER: mi._ver_participante
        }
        return realizar.get(accion)(solicitud)

    # --------------------------------------------------
    # Métodos privados

    def _buscar_participantes(mi, solicitud:dict):
        entrega:dict = solicitud.get('_dto_contexto', {})
        if mi.autorizar_accion(permisos=mi.PERMISOS.BUSCAR, rechazar=True):
            resultado = mi.repositorio.recuperar_lista_participantes_todos(solicitud, roles_sesion=mi.sesion.get('roles'))
            metadatos = mi.agregar_metadatos({
                'nombre_descarga': 'documento de prueba',
                'titulo': 'Listado de Pruebas',
                'carpeta_guardar': 'creados'
            })
            entrega['descripcion'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}'
            entrega['resultado'] = resultado
            entrega['metadatos'] = metadatos
        return entrega

    def _agregar_participante(mi, solicitud:dict):
        mi.repositorio.insertar_nuevo_participante(solicitud)
        return {"solicitud": solicitud}

    def _actualizar_participante(mi, solicitud:dict):
        mi.repositorio.actualizar_participante_por_id(solicitud)
        return {"solicitud": solicitud}

    def _eliminar_participante(mi, solicitud:dict):
        mi.repositorio.eliminar_participante_por_id(solicitud)
        return {"solicitud": solicitud}

    def _ver_participante(mi, solicitud:dict):
        mi.repositorio.recuperar_participante_por_id(solicitud)
        return {"solicitud": solicitud}


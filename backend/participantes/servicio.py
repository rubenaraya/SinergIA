# backend\participantes\servicio.py

from pysinergia._dependencias import CasosDeUso
from abc import (ABCMeta, abstractmethod)

# --------------------------------------------------
# Importaciones del Microservicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)

# --------------------------------------------------
# Interface: I_RepositorioParticipantes
# --------------------------------------------------
class I_RepositorioParticipantes(metaclass=ABCMeta):
    # Implementada en la capa de adaptadores por RepositorioParticipantes

    @abstractmethod
    def recuperar_lista_participantes_todos(mi, peticion:dict) -> dict:
        ...

    @abstractmethod
    def recuperar_lista_participantes_filtrados(mi, peticion:dict) -> dict:
        ...

    @abstractmethod
    def recuperar_participante_por_id(mi, peticion:dict) -> dict:
        ...

    @abstractmethod
    def insertar_nuevo_participante(mi, peticion:dict) -> dict:
        ...

    @abstractmethod
    def actualizar_participante_por_id(mi, peticion:dict) -> dict:
        ...

    @abstractmethod
    def eliminar_participante_por_id(mi, peticion:dict) -> dict:
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
        BUSCAR_PARTICIPANTES = 1
        AGREGAR_PARTICIPANTE = 2
        VER_PARTICIPANTE = 3
        ACTUALIZAR_PARTICIPANTE = 4
        ELIMINAR_PARTICIPANTE = 5

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de adaptadores)

    def solicitar_accion(mi, accion:ACCIONES, peticion:dict) -> dict:
        realizar = {
            mi.ACCIONES.BUSCAR_PARTICIPANTES: mi._buscar_participantes,
            mi.ACCIONES.AGREGAR_PARTICIPANTE: mi._agregar_participante,
            mi.ACCIONES.ACTUALIZAR_PARTICIPANTE: mi._actualizar_participante,
            mi.ACCIONES.ELIMINAR_PARTICIPANTE: mi._eliminar_participante,
            mi.ACCIONES.VER_PARTICIPANTE: mi._ver_participante
        }
        return realizar.get(accion)(peticion)

    # --------------------------------------------------
    # Métodos privados

    def _buscar_participantes(mi, peticion:dict):
        mi.autorizar_roles('Ejecutivo,Usuario', rechazar=True)
        resultado = mi.repositorio.recuperar_lista_participantes_todos(peticion)
        metadatos = mi.agregar_metadatos({
            'nombre_descarga': 'documento de prueba',
            'titulo': 'Listado de Pruebas',
            'carpeta_guardar': 'creados'
        })
        return {
            "accion": "_buscar_participantes",
            "operacion": "recuperar_lista_participantes_todos",
            "modelo": "PeticionBuscarParticipantes",
            "resultado": resultado,
            "metadatos": metadatos
        }

    def _agregar_participante(mi, peticion:dict):
        mi.repositorio.insertar_nuevo_participante(peticion)
        return {"accion": "_agregar_participante", "operacion": "insertar_nuevo_participante", "modelo": "ModeloNuevoParticipante", "peticion": peticion.diccionario()}

    def _actualizar_participante(mi, peticion:dict):
        mi.repositorio.actualizar_participante_por_id(peticion)
        return {"accion": "_actualizar_participante", "operacion": "actualizar_participante_por_id", "modelo": "ModeloEditarParticipante", "peticion": peticion.diccionario()}

    def _eliminar_participante(mi, peticion:dict):
        mi.repositorio.eliminar_participante_por_id(peticion)
        return {"accion": "_eliminar_participante", "operacion": "eliminar_participante_por_id", "modelo": "PeticionParticipante", "peticion": peticion.diccionario()}

    def _ver_participante(mi, peticion:dict):
        mi.repositorio.recuperar_participante_por_id(peticion)
        return {"accion": "_ver_participante", "operacion": "recuperar_participante_por_id", "modelo": "PeticionParticipante", "peticion": peticion.diccionario()}


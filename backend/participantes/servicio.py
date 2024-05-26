# backend\participantes\servicio.py

from pysinergia._dependencias.servicio import *

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)

# --------------------------------------------------
# Constantes: ACCION
# --------------------------------------------------
class ACCION:
    BUSCAR_PARTICIPANTES = 1
    AGREGAR_PARTICIPANTE = 2
    VER_PARTICIPANTE = 3
    ACTUALIZAR_PARTICIPANTE = 4
    ELIMINAR_PARTICIPANTE = 5


# --------------------------------------------------
# Interface: I_OperadorParticipantes
# --------------------------------------------------
class I_OperadorParticipantes(metaclass=ABCMeta):
    # Implementada en la capa de adaptadores por OperadorParticipantes
    @abstractmethod
    def recuperar_lista_participantes_todos(mi) -> Dict:
        ...
    @abstractmethod
    def recuperar_lista_participantes_filtrados(mi) -> Dict:
        ...
    @abstractmethod
    def recuperar_participante_por_id(mi) -> Dict:
        ...
    @abstractmethod
    def insertar_nuevo_participante(mi) -> Dict:
        ...
    @abstractmethod
    def actualizar_participante_por_id(mi) -> Dict:
        ...
    @abstractmethod
    def eliminar_participante_por_id(mi) -> Dict:
        ...


# --------------------------------------------------
# Clase: ServicioParticipantes
# --------------------------------------------------
"""
Falta convertir los Modelos de peticiones en Modelos de instrucciones para traspasar al Operador (procesar: validar y completar)
Falta entregar un estado interno del resultado (exito / error) ¿y un mensaje?
"""
class ServicioParticipantes(Servicio):

    def __init__(mi, operador:I_OperadorParticipantes, sesion:dict=None):
        mi.operador:I_OperadorParticipantes = operador
        mi.sesion:dict = sesion

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de adaptadores)

    def solicitar_accion(mi, accion:ACCION, peticion:dict) -> dict:
        realizar = {
            ACCION.BUSCAR_PARTICIPANTES: mi._buscar_participantes,
            ACCION.AGREGAR_PARTICIPANTE: mi._agregar_participante,
            ACCION.ACTUALIZAR_PARTICIPANTE: mi._actualizar_participante,
            ACCION.ELIMINAR_PARTICIPANTE: mi._eliminar_participante,
            ACCION.VER_PARTICIPANTE: mi._ver_participante
        }
        return realizar.get(accion)(peticion)

    # --------------------------------------------------
    # Métodos privados

    def _buscar_participantes(mi, peticion:dict):
        mi.autorizar_roles('Ejecutivo,Usuario', rechazar=True)
        resultado = mi.operador.recuperar_lista_participantes_todos()
        opciones = mi.establecer_opciones({
            'nombre_archivo': 'documento de prueba',
            'titulo': 'Listado de Pruebas',
            'carpeta_guardar': 'creados'
        })
        return {
            "accion": "_buscar_participantes",
            "operacion": "recuperar_lista_participantes_todos",
            "modelo": "PeticionBuscarParticipantes",
            "peticion": peticion,
            "resultado": resultado,
            "opciones": opciones
        }

    def _agregar_participante(mi, peticion:dict):
        mi.operador.insertar_nuevo_participante()
        return {"accion": "_agregar_participante", "operacion": "insertar_nuevo_participante", "modelo": "ModeloNuevoParticipante", "peticion": peticion.diccionario()}

    def _actualizar_participante(mi, peticion:dict):
        mi.operador.actualizar_participante_por_id()
        return {"accion": "_actualizar_participante", "operacion": "actualizar_participante_por_id", "modelo": "ModeloEditarParticipante", "peticion": peticion.diccionario()}

    def _eliminar_participante(mi, peticion:dict):
        mi.operador.eliminar_participante_por_id()
        return {"accion": "_eliminar_participante", "operacion": "eliminar_participante_por_id", "modelo": "PeticionParticipante", "peticion": peticion.diccionario()}

    def _ver_participante(mi, peticion:dict):
        mi.operador.recuperar_participante_por_id()
        return {"accion": "_ver_participante", "operacion": "recuperar_participante_por_id", "modelo": "PeticionParticipante", "peticion": peticion.diccionario()}


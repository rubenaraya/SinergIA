# backend\prueba\participantes\servicio.py

from abc import (ABCMeta, abstractmethod)

from backend.pysinergia import Servicio

from .dominio import (
    EntidadParticipante,
    ModeloPeticion,
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
    @abstractmethod
    def recuperar_lista_participantes_todos(mi):
        ...
    @abstractmethod
    def recuperar_lista_participantes_filtrados(mi):
        ...
    @abstractmethod
    def recuperar_participante_por_id(mi):
        ...
    @abstractmethod
    def insertar_nuevo_participante(mi):
        ...
    @abstractmethod
    def actualizar_participante_por_id(mi):
        ...
    @abstractmethod
    def eliminar_participante_por_id(mi):
        ...

# --------------------------------------------------
# Clase: ServicioParticipantes
# --------------------------------------------------
class ServicioParticipantes(Servicio):

    def __init__(mi, operador:I_OperadorParticipantes):
        mi.operador:I_OperadorParticipantes = operador

    def solicitar_accion(mi, accion:ACCION, peticion:ModeloPeticion):
        realizar = {
            ACCION.BUSCAR_PARTICIPANTES: mi._buscar_participantes,
            ACCION.AGREGAR_PARTICIPANTE: mi._agregar_participante,
            ACCION.ACTUALIZAR_PARTICIPANTE: mi._actualizar_participante,
            ACCION.ELIMINAR_PARTICIPANTE: mi._eliminar_participante,
            ACCION.VER_PARTICIPANTE: mi._ver_participante
        }
        return realizar.get(accion)(peticion)

    def _buscar_participantes(mi, peticion:PeticionBuscarParticipantes):
        resultado = mi.operador.recuperar_lista_participantes_todos()
        return {"accion": "_buscar_participantes", "operacion": "recuperar_lista_participantes_todos", "modelo": "PeticionBuscarParticipantes", "peticion": peticion.diccionario(), "resultado": resultado}

    def _agregar_participante(mi, peticion:ModeloNuevoParticipante):
        mi.operador.insertar_nuevo_participante()
        return {"accion": "_agregar_participante", "operacion": "insertar_nuevo_participante", "modelo": "ModeloNuevoParticipante", "peticion": peticion.diccionario()}

    def _actualizar_participante(mi, peticion:ModeloEditarParticipante):
        mi.operador.actualizar_participante_por_id()
        return {"accion": "_actualizar_participante", "operacion": "actualizar_participante_por_id", "modelo": "ModeloEditarParticipante", "peticion": peticion.diccionario()}

    def _eliminar_participante(mi, peticion:PeticionParticipante):
        mi.operador.eliminar_participante_por_id()
        return {"accion": "_eliminar_participante", "operacion": "eliminar_participante_por_id", "modelo": "PeticionParticipante", "peticion": peticion.diccionario()}

    def _ver_participante(mi, peticion:PeticionParticipante):
        mi.operador.recuperar_participante_por_id()
        return {"accion": "_ver_participante", "operacion": "recuperar_participante_por_id", "modelo": "PeticionParticipante", "peticion": peticion.diccionario()}


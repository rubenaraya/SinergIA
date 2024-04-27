from backend.pysinergia import Servicio
from backend.prueba.participantes.dominio import EntidadParticipante
from backend.prueba.participantes.operador import OperadorParticipantes

class ACCION:
    BUSCAR_PARTICIPANTES = 1
    AGREGAR_PARTICIPANTE = 2
    VER_PARTICIPANTE = 3
    ACTUALIZAR_PARTICIPANTE = 4
    ELIMINAR_PARTICIPANTE = 5

class ServicioParticipantes(Servicio):

    def __init__(mi):
        mi.operador = OperadorParticipantes()
        mi.entidad = EntidadParticipante()

    def solicitar_accion(mi, accion:ACCION, peticion):
        realizar = {
            ACCION.BUSCAR_PARTICIPANTES: mi._buscar_participantes,
            ACCION.AGREGAR_PARTICIPANTE: mi._agregar_participante,
            ACCION.ACTUALIZAR_PARTICIPANTE: mi._actualizar_participante,
            ACCION.ELIMINAR_PARTICIPANTE: mi._eliminar_participante,
            ACCION.VER_PARTICIPANTE: mi._ver_participante
        }
        return realizar.get(accion)(peticion)

    def _buscar_participantes(mi, peticion):
        return {"accion": "_buscar_participantes", "peticion": peticion}

    def _agregar_participante(mi, peticion):
        return {"accion": "_agregar_participante", "peticion": peticion}

    def _actualizar_participante(mi, peticion):
        return {"accion": "_actualizar_participante", "peticion": peticion}

    def _eliminar_participante(mi, peticion):
        return {"accion": "_eliminar_participante", "peticion": peticion}

    def _ver_participante(mi, peticion):
        return {"accion": "_ver_participante", "peticion": peticion}


from backend.pysinergia.adaptadores import Controlador
from backend.prueba.participantes.servicio import ServicioParticipantes as Servicio, ACCION

class ControladorParticipantes(Controlador):

    def buscar_participantes(mi, peticion):
        resultado = Servicio().solicitar_accion(ACCION.BUSCAR_PARTICIPANTES, peticion)
        return mi.emisor.entregar_respuesta(resultado)
    
    def agregar_participante(mi, peticion):
        resultado = Servicio().solicitar_accion(ACCION.AGREGAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def ver_participante(mi, peticion):
        resultado = Servicio().solicitar_accion(ACCION.VER_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def actualizar_participante(mi, peticion):
        resultado = Servicio().solicitar_accion(ACCION.ACTUALIZAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def eliminar_participante(mi, peticion):
        resultado = Servicio().solicitar_accion(ACCION.ELIMINAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

from backend.pysinergia import Controlador, Operador
from backend.prueba.participantes.servicio import (
    ServicioParticipantes as Servicio, 
    ACCION,
    I_Operador
)
from backend.pysinergia import (
    I_ConectorBasedatos, 
    I_ConectorAlmacen, 
    I_ConectorDisco, 
    I_ConectorLlm, 
    I_ConectorSpi, 
)

class ControladorParticipantes(Controlador):

    def buscar_participantes(mi, peticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.BUSCAR_PARTICIPANTES, peticion)
        return mi.emisor.entregar_respuesta(resultado)
    
    def agregar_participante(mi, peticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def ver_participante(mi, peticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def actualizar_participante(mi, peticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def eliminar_participante(mi, peticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

class OperadorParticipantes(Operador, I_Operador):
    def __init__(mi):
        # inyectar
        from backend.pysinergia.conectores import BasedatosSqlite
        mi.basedatos:I_ConectorBasedatos = BasedatosSqlite()
        mi.basedatos.conectar(config={})


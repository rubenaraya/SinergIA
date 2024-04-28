# backend\prueba\participantes\adaptadores.py

from backend.pysinergia import Controlador, Operador
from backend.pysinergia import (
    I_ConectorBasedatos, 
    I_ConectorAlmacen, 
    I_ConectorDisco, 
    I_ConectorLlm, 
    I_ConectorSpi, 
)

from .servicio import (
    ACCION,
    ServicioParticipantes as Servicio, 
    I_OperadorParticipantes
)
from .dominio import ModeloPeticion

class Config():
    ...

class ControladorParticipantes(Controlador):

    """
    Falta autorizar_acceso según roles
    Falta convertir codigos de estado para respuesta del emisor
    """
    def buscar_participantes(mi, peticion:ModeloPeticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.BUSCAR_PARTICIPANTES, peticion)
        return mi.emisor.entregar_respuesta(resultado)
    
    def agregar_participante(mi, peticion:ModeloPeticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def ver_participante(mi, peticion:ModeloPeticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def actualizar_participante(mi, peticion:ModeloPeticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def eliminar_participante(mi, peticion:ModeloPeticion):
        resultado = Servicio(OperadorParticipantes()).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

class OperadorParticipantes(Operador, I_OperadorParticipantes):

    """
    Falta usar config para inyectar dependencias
    """
    def __init__(mi):
        # inyectar
        from backend.pysinergia.conectores import BasedatosSqlite
        mi.basedatos:I_ConectorBasedatos = BasedatosSqlite()
        mi.basedatos.conectar(config={})


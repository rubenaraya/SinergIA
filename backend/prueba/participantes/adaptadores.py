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

# --------------------------------------------------
# Clase: Config
# --------------------------------------------------
class Config():
    ...

# --------------------------------------------------
# Clase: ControladorParticipantes
# --------------------------------------------------
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

# --------------------------------------------------
# Clase: OperadorParticipantes
# --------------------------------------------------
class OperadorParticipantes(Operador, I_OperadorParticipantes):

    """
    Falta usar config para inyectar dependencias y configuraciones
    """
    def __init__(mi):
        # inyectar
        from backend.pysinergia.conectores import BasedatosSqlite
        mi.basedatos:I_ConectorBasedatos = BasedatosSqlite()
        mi.basedatos.conectar(config={})

    def recuperar_lista_participantes_filtrados(mi):
        ...

    def recuperar_participante_por_id(mi):
        ...

    def insertar_nuevo_participante(mi):
        ...

    def actualizar_participante_por_id(mi):
        ...

    def eliminar_participante_por_id(mi):
        ...


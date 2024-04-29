# backend\prueba\participantes\adaptadores.py

from backend.pysinergia import Controlador, Operador

from .servicio import (
    ACCION,
    ServicioParticipantes, 
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
    Falta formatear la respuesta
    """
    # --------------------------------------------------
    # Métodos públicos (usados en la capa web)

    def buscar_participantes(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes()).solicitar_accion(
            ACCION.BUSCAR_PARTICIPANTES, peticion)
        return mi.emisor.entregar_respuesta(resultado)
    
    def agregar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes()).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def ver_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes()).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def actualizar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes()).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def eliminar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes()).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

# --------------------------------------------------
# Clase: OperadorParticipantes
# --------------------------------------------------
class OperadorParticipantes(Operador, I_OperadorParticipantes):

    """
    Falta usar config para inyectar dependencias y cargar configuraciones
    """
    def __init__(mi):
        ...

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de servicio)

    def recuperar_lista_participantes_todos(mi) -> dict:

        mi.inyectar_conectores(basedatos='BasedatosSqlite')
        mi.basedatos.conectar(config={
            "basedatos": "prueba",
            "ruta": "repositorios/prueba/basedatos"
        })
        sql = "SELECT * FROM participantes WHERE 1 ORDER BY id DESC"
        datos, total = mi.basedatos.obtener(sql=sql, parametros=[])
        mi.basedatos.desconectar()
        return dict(datos)

    def recuperar_lista_participantes_filtrados(mi) -> dict:
        ...

    def recuperar_participante_por_id(mi) -> dict:
        ...

    def insertar_nuevo_participante(mi) -> dict:
        ...

    def actualizar_participante_por_id(mi) -> dict:
        ...

    def eliminar_participante_por_id(mi) -> dict:
        ...


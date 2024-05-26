# backend\participantes\adaptadores.py

from pysinergia._dependencias.adaptadores import *

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .servicio import (
    ACCION,
    ServicioParticipantes, 
    I_OperadorParticipantes
)

# --------------------------------------------------
# ClaseModelo: ConfigParticipantes
# --------------------------------------------------
class ConfigParticipantes(Configuracion):
    ...


# --------------------------------------------------
# Clase: ControladorParticipantes
# --------------------------------------------------
class ControladorParticipantes(Controlador):

    # --------------------------------------------------
    # Métodos públicos (usados en la capa web)

    def buscar_participantes(mi, peticion:ModeloPeticion, formato:str='JSON', guardar:bool=False) -> tuple:
        servicio = ServicioParticipantes(OperadorParticipantes(mi.configuracion), mi.sesion)
        resultado = servicio.solicitar_accion(ACCION.BUSCAR_PARTICIPANTES, peticion.diccionario())
        respuesta = RespuestaResultado(**resultado).diccionario()
        respuesta.update(mi.comunicador.traspasar_contexto())
        entrega = Funciones.atributos_entrega(formato)
        nombre_archivo = mi.comunicador.obtener_nombre_archivo(respuesta, entrega.extension)
        encabezados = mi.comunicador.generar_encabezados(tipo_mime=entrega.tipo_mime, nombre_archivo=nombre_archivo)
        contenido = mi.comunicador.exportar_contenido(formato=entrega.exportar, info=respuesta, guardar=guardar)
        return (contenido, encabezados)

    def agregar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion.diccionario())
        return resultado

    def ver_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion.diccionario())
        return resultado

    def actualizar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion.diccionario())
        return resultado

    def eliminar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion.diccionario())
        return resultado


# --------------------------------------------------
# Clase: OperadorParticipantes
# --------------------------------------------------
"""
Falta recibir la petición procesada
Falta crear generar_instruccion y generar_consulta en I_ConectorBasedatos y BasedatosSqlite) -> ¿Debería usar Entidad?
Falta probar Modelos iniciales para insertar y actualizar participantes
"""
class OperadorParticipantes(Operador, I_OperadorParticipantes):

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de servicio)

    def recuperar_lista_participantes_todos(mi) -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())

        instruccion = "SELECT * FROM participantes WHERE 1 ORDER BY id DESC"

        datos, total = mi.basedatos.obtener(instruccion, parametros=[])
        mi.basedatos.desconectar()
        return datos

    def recuperar_lista_participantes_filtrados(mi) -> Dict:
        ...

    def recuperar_participante_por_id(mi) -> Dict:
        ...

    def insertar_nuevo_participante(mi) -> Dict:
        ...

    def actualizar_participante_por_id(mi) -> Dict:
        ...

    def eliminar_participante_por_id(mi) -> Dict:
        ...


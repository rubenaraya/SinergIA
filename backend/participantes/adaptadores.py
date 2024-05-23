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

    def buscar_participantes(mi, peticion:ModeloPeticion) -> dict:
        servicio = ServicioParticipantes(OperadorParticipantes(mi.config), mi.sesion)
        resultado = servicio.solicitar_accion(ACCION.BUSCAR_PARTICIPANTES, peticion)
        respuesta = RespuestaResultado(**resultado).diccionario()
        respuesta['opciones'] = {
            'plantilla': f'{mi.config.ruta_servicio}/plantillas/tabla.html',
            'hoja_estilos': f'{mi.config.ruta_servicio}/plantillas/tabla.css',
            'ruta_destino': f'./repositorios/{mi.config.aplicacion}/disco',
            'nombre_archivo': 'documento de prueba',
            'titulo': 'Listado de Pruebas',
            'descripcion': '',
            'etiquetas': '',
            'hoja_datos': 'participantes',
        }
        return respuesta

    def agregar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config), mi.sesion).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion)
        return resultado

    def ver_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config), mi.sesion).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion)
        return resultado

    def actualizar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config), mi.sesion).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion)
        return resultado

    def eliminar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config), mi.sesion).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion)
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
        mi.basedatos.conectar(mi.config.basedatos())

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


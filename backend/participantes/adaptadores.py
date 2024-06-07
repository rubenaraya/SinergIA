# backend\participantes\adaptadores.py

from pysinergia._dependencias.adaptadores import *

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .servicio import (
    ACCION,
    CasosDeUsoParticipantes, 
    I_RepositorioParticipantes
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

    def buscar_participantes(mi, peticion:ModeloPeticion, formato:str=None, guardar:bool=False) -> tuple:
        servicio = CasosDeUsoParticipantes(RepositorioParticipantes(mi.configuracion), mi.sesion)
        resultado = servicio.solicitar_accion(ACCION.BUSCAR_PARTICIPANTES, peticion.exportar())
        resultado.update(mi.comunicador.transferir_contexto())
        respuesta = RespuestaResultado(**resultado,
            titulo='{titulo}',
            descripcion='Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}',
            T=mi.comunicador.traspasar_traductor()
        ).diccionario()
        recurso = Recurso(formato=mi.comunicador.elegir_formato(formato))
        nombre_descarga = mi.comunicador.obtener_nombre_descarga(respuesta, recurso.extension)
        encabezados = mi.comunicador.generar_encabezados(tipo_mime=recurso.tipo_mime, nombre_descarga=nombre_descarga, charset='utf-8')
        contenido = mi.comunicador.exportar_contenido(formato=recurso.formato, info=respuesta, guardar=guardar)
        return (contenido, encabezados)

    def cargar_archivo(mi, peticion:CargaArchivo) -> dict:
        resultado = mi.comunicador.cargar_archivo(peticion)
        if resultado.es_valido:
            contenido = ModeloRespuesta(
                mensaje='Archivo-cargado-con-exito',
                resultado={'nombre': resultado.nombre},
                T=mi.comunicador.traspasar_traductor()
            ).diccionario()
        else:
            contenido = ModeloRespuesta(
                codigo=resultado.codigo,
                tipo=resultado.resultado,
                mensaje=resultado.mensaje_error,
                resultado={'nombre': resultado.nombre},
                T=mi.comunicador.traspasar_traductor()
            ).diccionario()
        return contenido

    def agregar_participante(mi, peticion:ModeloPeticion):
        resultado = CasosDeUsoParticipantes(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion.diccionario())
        return resultado

    def ver_participante(mi, peticion:ModeloPeticion):
        resultado = CasosDeUsoParticipantes(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion.diccionario())
        return resultado

    def actualizar_participante(mi, peticion:ModeloPeticion):
        resultado = CasosDeUsoParticipantes(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion.diccionario())
        return resultado

    def eliminar_participante(mi, peticion:ModeloPeticion):
        resultado = CasosDeUsoParticipantes(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion.diccionario())
        return resultado


# --------------------------------------------------
# Clase: RepositorioParticipantes
# --------------------------------------------------
class RepositorioParticipantes(Repositorio, I_RepositorioParticipantes):

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de servicio)

    def recuperar_lista_participantes_todos(mi, peticion:dict) -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
            modelo=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
            peticion=peticion
        )
        datos, total = mi.basedatos.ver_lista(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def recuperar_lista_participantes_filtrados(mi, peticion:dict) -> Dict:
        ...

    def recuperar_participante_por_id(mi, peticion:dict) -> Dict:
        ...

    def insertar_nuevo_participante(mi, peticion:dict) -> Dict:
        ...

    def actualizar_participante_por_id(mi, peticion:dict) -> Dict:
        ...

    def eliminar_participante_por_id(mi, peticion:dict) -> Dict:
        ...


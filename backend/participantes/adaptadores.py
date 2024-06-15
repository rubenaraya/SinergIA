# backend\participantes\adaptadores.py

from pysinergia.componentes import (
    Configuracion,
    Controlador,
    Repositorio,
    Peticion,
    ArchivoCargado,
    Respuesta,
    Recurso,
)

# --------------------------------------------------
# Importaciones del Microservicio personalizado
from .servicio import (
    CasosDeUsoParticipantes as CasosDeUso, 
    I_RepositorioParticipantes,
)
from .dominio import ProcedimientoBuscarParticipantes

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

    def buscar_participantes(mi, peticion:Peticion, conversion:str=None, guardar:bool=False) -> tuple:
        casosdeuso = CasosDeUso(RepositorioParticipantes(mi.configuracion), mi.sesion)
        peticion.agregar_contexto(mi.comunicador.transferir_contexto())
        resultado = casosdeuso.solicitar_accion(CasosDeUso.ACCIONES.BUSCAR, peticion.serializar())
        respuesta = Respuesta(**resultado, T=mi.comunicador.traspasar_traductor()).diccionario()
        recurso = Recurso(conversion=mi.comunicador.elegir_conversion(conversion))
        nombre_descarga = mi.comunicador.generar_nombre_descarga(respuesta, recurso.extension)
        encabezados = mi.comunicador.generar_encabezados(tipo_mime=recurso.tipo_mime, nombre_descarga=nombre_descarga, charset='utf-8')
        cuerpo = mi.comunicador.exportar_informacion(conversion=recurso.conversion, info=respuesta, guardar=guardar)
        return (cuerpo, encabezados)

    def cargar_archivo(mi, peticion:ArchivoCargado) -> dict:
        resultado = mi.comunicador.cargar_archivo(peticion)
        if resultado.es_valido:
            contenido = Respuesta(
                mensaje='Archivo-cargado-con-exito',
                resultado={'recurso': resultado.nombre},
                T=mi.comunicador.traspasar_traductor()
            ).diccionario()
        else:
            contenido = Respuesta(
                codigo=resultado.codigo,
                conclusion=resultado.conclusion,
                mensaje=resultado.mensaje_error,
                resultado={'recurso': resultado.nombre},
                T=mi.comunicador.traspasar_traductor()
            ).diccionario()
        return contenido

    def agregar_participante(mi, peticion:Peticion):
        resultado = CasosDeUso(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            CasosDeUso.ACCIONES.AGREGAR, peticion.serializar())
        return resultado

    def ver_participante(mi, peticion:Peticion):
        resultado = CasosDeUso(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            CasosDeUso.ACCIONES.VER, peticion.serializar())
        return resultado

    def actualizar_participante(mi, peticion:Peticion):
        resultado = CasosDeUso(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            CasosDeUso.ACCIONES.ACTUALIZAR, peticion.serializar())
        return resultado

    def eliminar_participante(mi, peticion:Peticion):
        resultado = CasosDeUso(RepositorioParticipantes(mi.configuracion), mi.sesion).solicitar_accion(
            CasosDeUso.ACCIONES.ELIMINAR, peticion.serializar())
        return resultado


# --------------------------------------------------
# Clase: RepositorioParticipantes
# --------------------------------------------------
class RepositorioParticipantes(Repositorio, I_RepositorioParticipantes):

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de servicio)

    def recuperar_lista_participantes_todos(mi, solicitud:dict, roles_sesion:str='') -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        procedimiento = ProcedimientoBuscarParticipantes(dto_solicitud_datos=solicitud, dto_roles_sesion=roles_sesion).serializar()
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
            plantilla=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
            procedimiento=procedimiento
        )
        datos, total = mi.basedatos.ver_lista(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def recuperar_lista_participantes_filtrados(mi, solicitud:dict) -> dict:
        ...

    def recuperar_participante_por_id(mi, solicitud:dict) -> dict:
        ...

    def insertar_nuevo_participante(mi, solicitud:dict) -> dict:
        ...

    def actualizar_participante_por_id(mi, solicitud:dict) -> dict:
        ...

    def eliminar_participante_por_id(mi, solicitud:dict) -> dict:
        ...


# --------------------------------------------------
# backend\documentos\operaciones.py
# --------------------------------------------------

# Importaciones de PySinergIA
from pysinergia.modelos import (
    Peticion,
    Respuesta,
)
from pysinergia.operaciones import (
    Controlador,
    Repositorio,
    CasosDeUso,
)

# Importaciones del Microservicio
from .modelos import (
    OperacionConsultarDocumentos,
    OperacionVerDocumento,
    OperacionInsertarDocumento,
)

# --------------------------------------------------
# Clase: ControladorDocumentos
class ControladorDocumentos(Controlador):

    def buscar_documentos(mi, peticion:Peticion):
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        casosdeuso = CasosDeUsoDocumentos(RepositorioDocumentos(mi.configuracion), mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.BUSCAR, peticion.serializar())
        return Respuesta(**resultado, T=mi.comunicador.traspasar_traductor()).diccionario()

    def ver_documento(mi, peticion:Peticion):
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        casosdeuso = CasosDeUsoDocumentos(RepositorioDocumentos(mi.configuracion), mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.VER, peticion.serializar())
        return Respuesta(**resultado, T=mi.comunicador.traspasar_traductor()).diccionario()

    def agregar_documento(mi, peticion:Peticion):
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        casosdeuso = CasosDeUsoDocumentos(RepositorioDocumentos(mi.configuracion), mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.AGREGAR, peticion.serializar())
        return Respuesta(**resultado, T=mi.comunicador.traspasar_traductor()).diccionario()

# --------------------------------------------------
# Clase: RepositorioDocumentos
class RepositorioDocumentos(Repositorio):

    def recuperar_lista_documentos(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        operacion = OperacionConsultarDocumentos(dto_solicitud_datos=solicitud, dto_roles_sesion=roles_sesion).serializar()
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
            plantilla=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
            operacion=operacion
        )
        datos = mi.basedatos.ver_lista(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def recuperar_documento(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        operacion = OperacionVerDocumento(dto_solicitud_datos=solicitud, dto_roles_sesion=roles_sesion).serializar()
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
            plantilla=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
            operacion=operacion
        )
        datos = mi.basedatos.ver_caso(instruccion, [])
        mi.basedatos.desconectar()
        return datos


    #TODO: Pendiente
    def insertar_nuevo_documento(mi, solicitud:dict) -> dict:
        ...

# --------------------------------------------------
# Clase: CasosDeUsoDocumentos
class CasosDeUsoDocumentos(CasosDeUso):
    def __init__(mi, repositorio:RepositorioDocumentos, sesion:dict=None):
        mi.repositorio:RepositorioDocumentos = repositorio
        mi.sesion:dict = sesion

    # Clases de constantes

    class ACCIONES:
        BUSCAR = 1
        AGREGAR = 2
        VER = 3

    class PERMISOS:
        BUSCAR = ''
        AGREGAR = ''
        VER = ''

    # Métodos

    def solicitar_accion(mi, accion:ACCIONES, solicitud:dict) -> dict:
        realizar = {
            mi.ACCIONES.BUSCAR: mi._buscar_documentos,
            mi.ACCIONES.AGREGAR: mi._agregar_documento,
            mi.ACCIONES.VER: mi._ver_documento,
        }
        return realizar.get(accion)(solicitud)

    def _buscar_documentos(mi, solicitud:dict):
        entrega:dict = solicitud.get('_dto_contexto', {})
        if mi.autorizar_accion(permisos=mi.PERMISOS.BUSCAR, rechazar=True):
            resultado = mi.repositorio.recuperar_lista_documentos(solicitud, roles_sesion=mi.sesion.get('roles'))
            entrega['resultado'] = resultado
            entrega['descripcion'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}' if resultado.get('total', 0) > 0 else 'No-hay-casos'
        return entrega

    def _ver_documento(mi, solicitud:dict):
        entrega:dict = solicitud.get('_dto_contexto', {})
        if mi.autorizar_accion(permisos=mi.PERMISOS.VER, rechazar=True):
            resultado = mi.repositorio.recuperar_documento(solicitud, roles_sesion=mi.sesion.get('roles'))
            entrega['resultado'] = resultado
            if len(resultado) == 0:
                entrega['mensaje'] = 'Recurso-no-encontrado'
        return entrega


    #TODO: Pendiente
    def _agregar_documento(mi, solicitud:dict):
        ...

ACCIONES = CasosDeUsoDocumentos.ACCIONES

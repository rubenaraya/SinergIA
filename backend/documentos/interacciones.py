# --------------------------------------------------
# backend\documentos\interacciones.py
# --------------------------------------------------

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as C,
)
from pysinergia.modelos import (
    Peticion,
    Respuesta,
)
from pysinergia.interacciones import (
    Controlador,
    Repositorio,
    CasosDeUso,
)

# Importaciones del Microservicio
from .modelos import (
    OperacionListaDocumentos,
    OperacionAbrirDocumento,
    OperacionInsertarDocumento,
    OperacionActualizarDocumento,
)

# --------------------------------------------------
# Clase: ControladorDocumentos
class ControladorDocumentos(Controlador):

    def buscar_documentos(mi, peticion:Peticion) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.BUSCAR, peticion.convertir())
        respuesta = Respuesta(**resultado, T=mi.comunicador.traductor).extraer()
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
        return (respuesta, codigo)

    def ver_documento(mi, peticion:Peticion) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.VER, peticion.convertir())
        respuesta = Respuesta(**resultado, T=mi.comunicador.traductor).extraer()
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
        return (respuesta, codigo)

    def agregar_documento(mi, peticion:Peticion) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.AGREGAR, peticion.convertir())
        respuesta = Respuesta(**resultado, T=mi.comunicador.traductor).extraer()
        codigo = respuesta.get('codigo', C.ESTADO._201_CREADO)
        return (respuesta, codigo)

    #TODO: Pendiente
    def actualizar_documento(mi, peticion:Peticion) -> tuple:
        ...

    #TODO: Pendiente
    def eliminar_documento(mi, peticion:Peticion) -> tuple:
        ...

# --------------------------------------------------
# Clase: RepositorioDocumentos
class RepositorioDocumentos(Repositorio):

    def recuperar_lista_documentos(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        operacion = OperacionListaDocumentos(
                dto_solicitud_datos=solicitud,
                dto_roles_sesion=roles_sesion
            ).preparar()
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
                plantilla=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
                operacion=operacion
            )
        datos = mi.basedatos.lista_casos(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def ver_documento(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        operacion = OperacionAbrirDocumento(
                dto_solicitud_datos=solicitud,
                dto_roles_sesion=roles_sesion
            ).preparar()
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
                plantilla=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
                operacion=operacion
            )
        datos = mi.basedatos.abrir_caso(instruccion, [])
        mi.basedatos.desconectar()
        return datos

    #TODO: Pendiente
    def agregar_documento(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        ...

    #TODO: Pendiente
    def actualizar_documento(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        ...

    #TODO: Pendiente
    def eliminar_documento(mi, solicitud:dict, roles_sesion:str=None) -> dict:
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
            resultado = mi.repositorio.recuperar_lista_documentos(
                    solicitud,
                    roles_sesion=mi.sesion.get('roles')
                )
            entrega['resultado'] = resultado
            entrega['descripcion'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}' if resultado.get('total', 0) > 0 else 'No-hay-casos'
        return entrega

    def _ver_documento(mi, solicitud:dict):
        entrega:dict = solicitud.get('_dto_contexto', {})
        if mi.autorizar_accion(permisos=mi.PERMISOS.VER, rechazar=True):
            resultado = mi.repositorio.ver_documento(
                    solicitud,
                    roles_sesion=mi.sesion.get('roles')
                )
            entrega['resultado'] = resultado
            if len(resultado) == 0:
                entrega['mensaje'] = 'Recurso-no-encontrado'
        return entrega

    #TODO: Pendiente
    def _agregar_documento(mi, solicitud:dict):
        ...

    #TODO: Pendiente
    def _actualizar_documento(mi, solicitud:dict):
        ...

    #TODO: Pendiente
    def _eliminar_documento(mi, solicitud:dict):
        ...

ACCIONES = CasosDeUsoDocumentos.ACCIONES

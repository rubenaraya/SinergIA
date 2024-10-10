# --------------------------------------------------
# backend\documentos\interacciones.py
# --------------------------------------------------

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as C,
)
from pysinergia.modelos import (
    Validador,
    Presentador,
)
from pysinergia.sql import GeneradorSQL
from pysinergia.interacciones import (
    Controlador,
    Repositorio,
    CasosDeUso,
)

# Importaciones del Microservicio
from .modelos import (
    ConstructorListarDocumentos,
    ConstructorAbrirDocumento,
    ConstructorAgregarDocumento,
    ConstructorActualizarDocumento,
)

# --------------------------------------------------
# Clase: ControladorDocumentos
class ControladorDocumentos(Controlador):

    def buscar_documentos(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.BUSCAR, peticion.convertir())
        respuesta = Presentador(**resultado, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
        return (respuesta, codigo)

    def ver_documento(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.VER, peticion.convertir())
        respuesta = Presentador(**resultado, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
        return (respuesta, codigo)

    def agregar_documento(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        resultado = casosdeuso.solicitar_accion(ACCIONES.AGREGAR, peticion.convertir())
        respuesta = Presentador(**resultado, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._201_CREADO)
        return (respuesta, codigo)

    #TODO: Pendiente
    def actualizar_documento(mi, peticion:Validador) -> tuple:
        ...

    #TODO: Pendiente
    def eliminar_documento(mi, peticion:Validador) -> tuple:
        ...

# --------------------------------------------------
# Clase: RepositorioDocumentos
class RepositorioDocumentos(Repositorio):

    def consultar_lista_documentos(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = GeneradorSQL(mi.configuracion.BASEDATOS_MARCA)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorListarDocumentos(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, pagina, maximo = sql.generar_consulta(sql.CONSULTA.SELECT_FILTRADO, constructor)
        datos = mi.basedatos.lista_casos(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def consultar_documento_seleccionado(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = GeneradorSQL(mi.configuracion.BASEDATOS_MARCA)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorAbrirDocumento(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, pagina, maximo = sql.generar_consulta(sql.CONSULTA.SELECT_FILTRADO, constructor)
        datos = mi.basedatos.abrir_caso(instruccion, [])
        mi.basedatos.desconectar()
        return datos

    #TODO: Pendiente
    def agregar_documento_nuevo(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        ...

    #TODO: Pendiente
    def actualizar_documento_seleccionado(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        ...

    #TODO: Pendiente
    def eliminar_documento_seleccionado(mi, solicitud:dict, roles_sesion:str=None) -> dict:
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
        ACTUALIZAR = 4
        ELIMINAR = 5

    class PERMISOS:
        BUSCAR = ''
        AGREGAR = ''
        VER = ''
        ACTUALIZAR = ''
        ELIMINAR = ''

    # Métodos

    def solicitar_accion(mi, accion:ACCIONES, solicitud:dict) -> dict:
        realizar = {
            mi.ACCIONES.BUSCAR: mi._buscar,
            mi.ACCIONES.AGREGAR: mi._agregar,
            mi.ACCIONES.VER: mi._ver,
            mi.ACCIONES.ACTUALIZAR: mi._actualizar,
            mi.ACCIONES.ELIMINAR: mi._eliminar,
        }
        return realizar.get(accion)(solicitud)

    def _buscar(mi, solicitud:dict):
        entrega = mi.preparar_entrega(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.BUSCAR, rechazar=True):
            resultado = mi.repositorio.consultar_lista_documentos(solicitud, mi.sesion.get('roles'))
            entrega['resultado'] = resultado
            entrega['descripcion'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}' if resultado.get('total', 0) > 0 else 'No-hay-casos'
        return entrega

    def _ver(mi, solicitud:dict):
        entrega = mi.preparar_entrega(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.VER, rechazar=True):
            resultado = mi.repositorio.consultar_documento_seleccionado(solicitud, mi.sesion.get('roles'))
            entrega['resultado'] = resultado
            if len(resultado) == 0:
                entrega['mensaje'] = 'Recurso-no-encontrado'
        return entrega

    #TODO: Pendiente
    def _agregar(mi, solicitud:dict):
        ...

    #TODO: Pendiente
    def _actualizar(mi, solicitud:dict):
        ...

    #TODO: Pendiente
    def _eliminar(mi, solicitud:dict):
        ...

ACCIONES = CasosDeUsoDocumentos.ACCIONES

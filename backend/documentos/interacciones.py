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
from pysinergia.sql import InstructorSQL
from pysinergia.interacciones import (
    Controlador,
    Repositorio,
    CasosDeUso,
    preparar_datos,
)

# Importaciones del Microservicio
from .modelos import (
    DocumentoBase,
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
        """
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        datos = casosdeuso.solicitar_accion(ACCIONES.BUSCAR, peticion.convertir())
        """
        solicitud = peticion.convertir()
        datos = preparar_datos(solicitud)
        resultado = repositorio.consultar_lista_documentos(solicitud, mi.sesion.get('roles'))
        datos['resultado'] = resultado
        datos['mensaje'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}' if resultado.get('total', 0) > 0 else 'No-hay-casos'

        respuesta = Presentador(**datos, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
        return (respuesta, codigo)

    def ver_documento(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        """
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        datos = casosdeuso.solicitar_accion(ACCIONES.VER, peticion.convertir())
        """
        solicitud = peticion.convertir()
        datos = preparar_datos(solicitud)
        resultado = repositorio.consultar_documento_seleccionado(solicitud, mi.sesion.get('roles'))
        datos['resultado'] = resultado
        if resultado.get('total', 0) <= 0:
            datos['mensaje'] = 'Recurso-no-encontrado'

        respuesta = Presentador(**datos, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
        return (respuesta, codigo)

    def agregar_documento(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        datos = casosdeuso.solicitar_accion(ACCIONES.AGREGAR, peticion.convertir())
        respuesta = Presentador(**datos, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._201_CREADO)
        return (respuesta, codigo)

    def actualizar_documento(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        datos = casosdeuso.solicitar_accion(ACCIONES.ACTUALIZAR, peticion.convertir())
        respuesta = Presentador(**datos, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._204_VACIO)
        return (respuesta, codigo)

    def eliminar_documento(mi, peticion:Validador) -> tuple:
        peticion.adjuntar_contexto(mi.comunicador.contexto)
        repositorio = RepositorioDocumentos(mi.configuracion)
        casosdeuso = CasosDeUsoDocumentos(repositorio, mi.sesion)
        datos = casosdeuso.solicitar_accion(ACCIONES.ELIMINAR, peticion.convertir())
        respuesta = Presentador(**datos, T=mi.comunicador.traductor).componer()
        codigo = respuesta.get('codigo', C.ESTADO._204_VACIO)
        return (respuesta, codigo)

    def crear_tabla(mi) -> tuple:
        repositorio = RepositorioDocumentos(mi.configuracion)
        repositorio.basedatos.conectar(repositorio.configuracion.basedatos())
        constructor = DocumentoBase().definiciones()
        datos = {'resultado': repositorio.basedatos.crear_tabla('catalogo', constructor)}
        repositorio.basedatos.desconectar()
        respuesta = Presentador(**datos, T=mi.comunicador.traductor).componer()
        return (respuesta, C.ESTADO._200_EXITO)

    # TODO: Pendiente
    def exportar_documentos(mi, peticion:Validador) -> tuple:
        ...

# --------------------------------------------------
# Clase: RepositorioDocumentos
class RepositorioDocumentos(Repositorio):

    def consultar_lista_documentos(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = InstructorSQL(mi.configuracion.BASEDATOS_CLASE)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorListarDocumentos(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, pagina, maximo = sql.generar_consulta(sql.CONSULTA.SELECT_FILTRADO, constructor)
        datos = mi.basedatos.lista_casos(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def consultar_documento_seleccionado(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = InstructorSQL(mi.configuracion.BASEDATOS_CLASE)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorAbrirDocumento(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, pagina, maximo = sql.generar_consulta(sql.CONSULTA.SELECT_FILTRADO, constructor)
        datos = mi.basedatos.abrir_caso(instruccion, [])
        mi.basedatos.desconectar()
        return datos

    def agregar_documento_nuevo(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = InstructorSQL(mi.configuracion.BASEDATOS_CLASE)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorAgregarDocumento(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, parametros = sql.generar_comando(sql.COMANDO.INSERT_FILA, constructor, 'uid')
        datos = mi.basedatos.agregar_caso(instruccion, parametros)
        mi.basedatos.desconectar()
        return datos

    def actualizar_documento_seleccionado(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = InstructorSQL(mi.configuracion.BASEDATOS_CLASE)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorActualizarDocumento(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, parametros = sql.generar_comando(sql.COMANDO.UPDATE_POR_UID, constructor, 'uid')
        datos = mi.basedatos.actualizar_caso(instruccion, parametros)
        mi.basedatos.desconectar()
        return datos

    def eliminar_documento_seleccionado(mi, solicitud:dict, roles_sesion:str=None) -> dict:
        sql = InstructorSQL(mi.configuracion.BASEDATOS_CLASE)
        mi.basedatos.conectar(mi.configuracion.basedatos())
        constructor = ConstructorAbrirDocumento(dto_solicitud=solicitud, dto_roles=roles_sesion).organizar()
        instruccion, parametros = sql.generar_comando(sql.COMANDO.DELETE_POR_UID, constructor, 'uid')
        datos = mi.basedatos.eliminar_caso(instruccion, parametros)
        mi.basedatos.desconectar()
        return datos

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
        datos = preparar_datos(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.BUSCAR, rechazar=True):
            resultado = mi.repositorio.consultar_lista_documentos(solicitud, mi.sesion.get('roles'))
            datos['resultado'] = resultado
            datos['mensaje'] = 'Hay-{total}-casos.-Lista-del-{primero}-al-{ultimo}' if resultado.get('total', 0) > 0 else 'No-hay-casos'
        return datos

    def _ver(mi, solicitud:dict):
        datos = preparar_datos(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.VER, rechazar=True):
            resultado = mi.repositorio.consultar_documento_seleccionado(solicitud, mi.sesion.get('roles'))
            datos['resultado'] = resultado
            if resultado.get('total', 0) <= 0:
                datos['mensaje'] = 'Recurso-no-encontrado'
        return datos

    def _agregar(mi, solicitud:dict):
        datos = preparar_datos(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.AGREGAR, rechazar=True):
            resultado = mi.repositorio.agregar_documento_nuevo(solicitud, mi.sesion.get('roles'))
            datos['resultado'] = resultado
            if resultado.get('total', 0) <= 0:
                datos['mensaje'] = 'Recurso-no-agregado'
        return datos

    def _actualizar(mi, solicitud:dict):
        datos = preparar_datos(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.ACTUALIZAR, rechazar=True):
            resultado = mi.repositorio.actualizar_documento_seleccionado(solicitud, mi.sesion.get('roles'))
            datos['resultado'] = resultado
            if resultado.get('total', 0) <= 0:
                datos['mensaje'] = 'Recurso-no-actualizado'
        return datos

    def _eliminar(mi, solicitud:dict):
        datos = preparar_datos(solicitud)
        if mi.autorizar_accion(permisos=mi.PERMISOS.ELIMINAR, rechazar=True):
            resultado = mi.repositorio.eliminar_documento_seleccionado(solicitud, mi.sesion.get('roles'))
            datos['resultado'] = resultado
            if resultado.get('total', 0) <= 0:
                datos['mensaje'] = 'Recurso-no-eliminado'
        return datos

ACCIONES = CasosDeUsoDocumentos.ACCIONES

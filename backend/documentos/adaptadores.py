# --------------------------------------------------
# backend\documentos\adaptadores.py
# --------------------------------------------------

# Importaciones de PySinergIA
from pysinergia.dominio import (
    Peticion,
    Respuesta,
)
from pysinergia.adaptadores import (
    Controlador,
    Repositorio,
    Configuracion,
)

# Importaciones del Microservicio personalizado
from .servicio import (
    CasosDeUsoDocumentos, 
    I_RepositorioDocumentos,
)
from .dominio import (
    ProcedimientoBuscarDocumentos,
)

# --------------------------------------------------
# Modelo: ConfigDocumentos
class ConfigDocumentos(Configuracion):
    ...

# --------------------------------------------------
# Clase: ControladorDocumentos
class ControladorDocumentos(Controlador):

    def buscar_documentos(mi, peticion:Peticion, conversion:str=None, guardar:bool=False) -> tuple:
        casosdeuso = CasosDeUsoDocumentos(RepositorioDocumentos(mi.configuracion), mi.sesion)
        peticion.agregar_contexto(mi.comunicador.transferir_contexto())
        resultado = casosdeuso.solicitar_accion(CasosDeUsoDocumentos.ACCIONES.BUSCAR, peticion.serializar())
        respuesta = Respuesta(**resultado, T=mi.comunicador.traspasar_traductor()).diccionario()
        return respuesta

    def agregar_documento(mi, peticion:Peticion):
        resultado = CasosDeUsoDocumentos(RepositorioDocumentos(mi.configuracion), mi.sesion).solicitar_accion(
            CasosDeUsoDocumentos.ACCIONES.AGREGAR, peticion.serializar())
        return resultado

    def ver_documento(mi, peticion:Peticion):
        resultado = CasosDeUsoDocumentos(RepositorioDocumentos(mi.configuracion), mi.sesion).solicitar_accion(
            CasosDeUsoDocumentos.ACCIONES.VER, peticion.serializar())
        return resultado

# --------------------------------------------------
# Clase: RepositorioDocumentos
class RepositorioDocumentos(Repositorio, I_RepositorioDocumentos):

    def recuperar_lista_documentos(mi, solicitud:dict, roles_sesion:str='') -> dict:
        mi.basedatos.conectar(mi.configuracion.basedatos())
        procedimiento = ProcedimientoBuscarDocumentos(dto_solicitud_datos=solicitud, dto_roles_sesion=roles_sesion).serializar()
        instruccion, pagina, maximo = mi.basedatos.generar_consulta(
            plantilla=mi.basedatos.INSTRUCCION.SELECT_CON_FILTROS,
            procedimiento=procedimiento
        )
        datos, total = mi.basedatos.ver_lista(instruccion, [], pagina, maximo)
        mi.basedatos.desconectar()
        return datos

    def recuperar_documento_por_id(mi, solicitud:dict) -> dict:
        ...

    def insertar_nuevo_documento(mi, solicitud:dict) -> dict:
        ...


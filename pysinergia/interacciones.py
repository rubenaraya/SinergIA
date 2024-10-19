# --------------------------------------------------
# pysinergia\interacciones.py
# --------------------------------------------------

from abc import (ABC, ABCMeta, abstractmethod)

# Importaciones de PySinergIA
from pysinergia.globales import *
from pysinergia.config import Configuracion

# --------------------------------------------------
# Funcion: preparar_datos
def preparar_datos(solicitud:dict=None) -> dict:
    datos:dict = {}
    if isinstance(solicitud, dict):
        datos = solicitud.get('_dto_contexto', {})
    return datos

# --------------------------------------------------
# Interface: I_ArchivoCargado
class I_ArchivoCargado(metaclass=ABCMeta):

    nombre:str
    extension:str
    carpeta:str
    mensaje_error:str
    codigo:str
    conclusion:str
    ruta:str
    tipo_mime:str
    es_valido:bool
    RENOMBRAR:str
    RECHAZAR:str
    SOBREESCRIBIR:str

# --------------------------------------------------
# Interface: I_Comunicador
class I_Comunicador(metaclass=ABCMeta):

    contexto = dict()
    traductor = None

    @abstractmethod
    def procesar_solicitud(mi, idiomas_aceptados:str=None, sesion:dict=None):
        ...

    @abstractmethod
    def elegir_conversion(mi, conversion:str=None) -> str:
        ...

    @abstractmethod
    def cargar_archivo(mi, portador, unico:bool=False):
        ...
    
    @abstractmethod
    def transformar_contenido(mi, info:dict, plantilla:str, ruta_plantillas:str='.') -> str:
        ...

    @abstractmethod
    def exportar_informacion(mi, conversion:str, info:dict={}, guardar:bool=False):
        ...

    @abstractmethod
    def generar_nombre_descarga(mi, info:dict, extension:str='', largo:int=250, auto:bool=False) -> str:
        ...

    @abstractmethod
    def crear_encabezados(mi, tipo_mime:str, charset:str='', disposicion:str='inline', nombre_descarga:str='') -> dict:
        ...

    @abstractmethod
    def asignar_cookie(mi, respuesta, nombre:str, valor:str, duracion:int=None):
        ...

    @abstractmethod
    def agregar_contexto(mi, datos:dict=None) -> dict:
        ...

# --------------------------------------------------
# Clase: Repositorio
class Repositorio(ABC):
    def __init__(mi, configuracion:Configuracion):
        mi.configuracion:Configuracion = configuracion
        mi.inyectar_conectores(mi.configuracion)

    def _importar_conector(mi, dic_config:dict):
        import importlib
        try:
            fuente = dic_config.get('fuente')
            clase = dic_config.get('clase')
            modulo = getattr(importlib.import_module(f"pysinergia.conectores.{fuente}"), clase)
            if modulo:
                return modulo
            return None
        except Exception:
            ErrorPersonalizado(mensaje='No-se-pudo-importar-el-conector', codigo=Constantes.ESTADO._500_ERROR, nivel_evento=Constantes.REGISTRO.WARNING, recurso=clase).registrar()
            return None

    def inyectar_conectores(mi, configuracion:Configuracion):
        try:
            if configuracion.BASEDATOS_CLASE:
                from pysinergia.conectores.basedatos import Basedatos
                conector_basedatos = mi._importar_conector(mi.configuracion.basedatos())
                if conector_basedatos:
                    mi.basedatos:Basedatos = conector_basedatos()
            if configuracion.DISCO_CLASE:
                from pysinergia.conectores.disco import Disco
                conector_disco = mi._importar_conector(mi.configuracion.disco())
                if conector_disco:
                    mi.disco:Disco = conector_disco(mi.configuracion.disco())
        except Exception as e:
            ErrorPersonalizado(mensaje='No-se-pudieron-inyectar-los-conectores', codigo=Constantes.ESTADO._500_ERROR, nivel_evento=Constantes.REGISTRO.WARNING).registrar()

# --------------------------------------------------
# Clase: Controlador
class Controlador(ABC):
    def __init__(mi, configuracion:Configuracion, comunicador:I_Comunicador):
        mi.configuracion:Configuracion = configuracion
        mi.comunicador:I_Comunicador = comunicador
        contexto = mi.comunicador.contexto
        mi.sesion:dict = contexto.get('sesion', {})

# --------------------------------------------------
# Clase: CasosDeUso
class CasosDeUso(ABC):

    sesion:dict

    # Clases de constantes

    class ACCIONES:
        ...

    class PERMISOS:
        ...

    # Métodos públicos

    @abstractmethod
    def solicitar_accion(mi, accion:ACCIONES, solicitud:dict) -> dict:
        ...

    def autorizar_accion(mi, permisos:PERMISOS, rechazar:bool=False) -> bool:
        roles:str = mi.sesion.get('roles')
        autorizacion = autorizar_acceso(permisos=permisos, roles=roles)
        if not autorizacion and rechazar:
            raise ErrorPersonalizado(
                mensaje='No-autorizado-para-acceder',
                codigo=Constantes.ESTADO._403_NO_AUTORIZADO,
            )
        return autorizacion

    def agregar_metadatos(mi, agregados:dict, anteriores:dict=None) -> dict:
        requeridos = {
            'plantilla': 'tabla.html',
            'hoja_estilos': 'tabla.css',
            'tabla_datos': 'Hoja1',
            'ruta_plantillas': '',
            'carpeta_guardar': '',
            'nombre_descarga': '',
            'titulo': '',
        }
        if anteriores is None:
            anteriores = {}
        for clave, valor in requeridos.items():
            if clave not in anteriores:
                anteriores[clave] = valor
        if agregados is not None:
            for clave, valor in agregados.items():
                anteriores[clave] = valor
        return anteriores

__all__ = ['Repositorio', 'Controlador', 'CasosDeUso', 'preparar_datos']

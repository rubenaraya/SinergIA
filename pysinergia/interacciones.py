# --------------------------------------------------
# pysinergia\interacciones.py
# --------------------------------------------------

from abc import (ABC, ABCMeta, abstractmethod)

# Importaciones de PySinergIA
from pysinergia.globales import (
    ErrorPersonalizado,
    Constantes,
    autorizar_acceso,
)
from pysinergia.config import Configuracion
from pysinergia.archivos import (
    ArchivoCargado as ArchivoCargado,
)

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
    def cargar_archivo(mi, portador:ArchivoCargado, unico:bool=False) -> ArchivoCargado:
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
        sesion = contexto.get('sesion')
        mi.sesion:dict = sesion or {}

# --------------------------------------------------
# Clase: CasosDeUso
class CasosDeUso(ABC):

    # Clases de constantes

    class ACCIONES:
        ...

    class PERMISOS:
        ...

    def __init__(mi, repositorio, sesion:dict=None):
        mi.repositorio = repositorio
        mi.sesion:dict = sesion

    # Métodos públicos

    def solicitar_accion(mi, accion:ACCIONES, solicitud:dict) -> dict:
        raise NotImplementedError()

    def autorizar_accion(mi, permisos:PERMISOS, rechazar:bool=False) -> bool:
        roles:str = mi.sesion.get('roles')
        autorizacion = autorizar_acceso(permisos=permisos, roles=roles)
        if not autorizacion and rechazar:
            raise ErrorPersonalizado(
                mensaje='No-autorizado-para-acceder',
                codigo=Constantes.ESTADO._403_NO_AUTORIZADO,
            )
        return autorizacion

    def agregar_metadatos(mi, agregados:dict, metadatos:dict=None) -> dict:
        requeridos = {
            'plantilla': 'tabla.html',
            'hoja_estilos': 'tabla.css',
            'tabla_datos': 'Hoja1',
            'ruta_plantillas': '',
            'carpeta_guardar': '',
            'nombre_descarga': '',
            'titulo': '',
            'autor': '',
            'descripcion': '',
            'etiquetas': '',
        }
        if metadatos is None:
            metadatos = {}
        for clave, valor in requeridos.items():
            if clave not in metadatos:
                metadatos[clave] = valor
        if agregados is not None:
            for clave, valor in agregados.items():
                metadatos[clave] = valor
        return metadatos


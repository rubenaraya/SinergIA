# --------------------------------------------------
# pysinergia\adaptadores.py
# --------------------------------------------------

import json
from abc import (ABC, ABCMeta, abstractmethod)
from typing import (List, Dict)

# Importaciones de Pydantic
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import Field, field_validator

# Importaciones de PySinergIA
from pysinergia.globales import (
    ErrorPersonalizado,
    Constantes,
    autorizar_acceso,
)
from pysinergia.dominio import (
    ArchivoCargado as ArchivoCargado,
)

# --------------------------------------------------
# Interface: I_Comunicador
class I_Comunicador(metaclass=ABCMeta):

    @abstractmethod
    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
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
    def generar_encabezados(mi, tipo_mime:str, charset:str='', disposicion:str='inline', nombre_descarga:str='') -> dict:
        ...

    @abstractmethod
    def transferir_contexto(mi, datos:dict=None) -> dict:
        ...

    @abstractmethod
    def traspasar_traductor(mi):
        ...

    @abstractmethod
    def asignar_cookie(mi, respuesta, nombre:str, valor:str, duracion:int=None):
        ...

# --------------------------------------------------
# Modelo: Configuracion
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class Configuracion(ABC, BaseSettings):
    # Aplicacion Global
    APP_GLOBAL: str = Field(default='')
    RAIZ_GLOBAL: str = Field(default='')
    RUTA_RAIZ: str = Field(default='')
    RUTA_PLANTILLAS: str = Field(default='')
    RUTA_LOGS: str = Field(default='')
    IDIOMAS_DISPONIBLES: List[str] = Field(default=[])
    ARCHIVO_LOGS: str = Field(default='')
    ALIAS_FRONTEND: str = Field(default='')
    DOMINIO_IDIOMA: str = Field(default='')
    RUTA_LOCALES: str = Field(default='')
    NIVEL_REGISTRO: str = Field(default='')
    # Aplicacion PWA
    APP_PWA: str = Field(default='')
    NOMBRE_PWA: str = ''
    TITULO_PWA: str = ''
    DESCRIPCION_PWA: str = ''
    API_KEYS: Dict[str,str] = Field(default={})
    SECRET_KEY: str = ''
    ALGORITMO_JWT: str = ''
    DURACION_TOKEN: int = 5
    ZONA_HORARIA: str = ''
    FORMATO_FECHA: str = ''
    RUTA_TEMP: str = ''
    # Microservicio especifico
    MICROSERVICIO: str = Field(default='')
    RUTA_MICROSERVICIO: str = Field(default='')
    URL_MICROSERVICIO: str = ''
    PREFIJO_MICROSERVICIO: str = ''
    BASEDATOS_FUENTE: str = ''
    BASEDATOS_CLASE: str = ''
    BASEDATOS_NOMBRE: str = ''
    BASEDATOS_RUTA: str = ''
    BASEDATOS_USUARIO: str = ''
    BASEDATOS_PASSWORD: str = ''
    DISCO_FUENTE: str = ''
    DISCO_CLASE: str = ''
    DISCO_NOMBRE: str = ''
    DISCO_RUTA: str = ''
    model_config = SettingsConfigDict(
        env_prefix='',
        extra='ignore',
        case_sensitive=True,
        validate_assignment=True,
        validate_default=True,
    )

    @field_validator('IDIOMAS_DISPONIBLES', mode='before')
    @classmethod
    def parse_json_list(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                pass
        return v or []

    @field_validator('API_KEYS', mode='before')
    @classmethod
    def parse_json_dict(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                pass
        return v or {}

    def basedatos(mi) -> dict:
        return dict({
            'fuente': mi.BASEDATOS_FUENTE,
            'clase': mi.BASEDATOS_CLASE,
            'nombre': mi.BASEDATOS_NOMBRE,
            'ruta': mi.BASEDATOS_RUTA,
            'usuario': mi.BASEDATOS_USUARIO,
            'password': mi.BASEDATOS_PASSWORD,
        })
    def disco(mi) -> dict:
        return dict({
            'fuente': mi.DISCO_FUENTE,
            'clase': mi.DISCO_CLASE,
            'nombre': mi.DISCO_NOMBRE,
            'ruta': mi.DISCO_RUTA,
        })
    def web(mi) -> dict:
        return {
            'APP_PWA': mi.APP_PWA,
            'MICROSERVICIO': mi.MICROSERVICIO,
            'RUTA_MICROSERVICIO': mi.RUTA_MICROSERVICIO,
            'URL_MICROSERVICIO': mi.URL_MICROSERVICIO,
            'PREFIJO_MICROSERVICIO': mi.PREFIJO_MICROSERVICIO,
            'RUTA_RAIZ': mi.RUTA_RAIZ,
            'RUTA_TEMP': mi.RUTA_TEMP,
            'RUTA_PLANTILLAS': mi.RUTA_PLANTILLAS,
            'APP_GLOBAL': mi.APP_GLOBAL,
            'RAIZ_GLOBAL': mi.RAIZ_GLOBAL,
            'ALIAS_FRONTEND': mi.ALIAS_FRONTEND,
            'IDIOMAS_DISPONIBLES': mi.IDIOMAS_DISPONIBLES,
            'ARCHIVO_LOGS': mi.ARCHIVO_LOGS,
            'ZONA_HORARIA': mi.ZONA_HORARIA,
            'FORMATO_FECHA': mi.FORMATO_FECHA,
            'NOMBRE_PWA': mi.NOMBRE_PWA,
            'TITULO_PWA': mi.TITULO_PWA,
            'DESCRIPCION_PWA': mi.DESCRIPCION_PWA,
            'DURACION_TOKEN': mi.DURACION_TOKEN,
        }

# --------------------------------------------------
# Clase: Repositorio
"""
PROPOSITO:
RESPONSABILIDADES:
"""
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
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class Controlador(ABC):
    def __init__(mi, configuracion:Configuracion, comunicador:I_Comunicador):
        mi.configuracion:Configuracion = configuracion
        mi.comunicador:I_Comunicador = comunicador
        contexto = mi.comunicador.transferir_contexto()
        sesion = contexto.get('sesion')
        mi.sesion:dict = sesion or {}

# --------------------------------------------------
# Clase: CasosDeUso
"""
PROPOSITO:
RESPONSABILIDADES:
"""
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
        autorizacion = autorizar_acceso(roles=roles, permisos=permisos)
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


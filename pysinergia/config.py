# --------------------------------------------------
# pysinergia\config.py
# --------------------------------------------------

import os
import json
from abc import ABC
from pathlib import Path
from typing import (List, Dict)
from dotenv import dotenv_values
from functools import lru_cache

# Importaciones de Pydantic
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import Field, field_validator

# --------------------------------------------------
# Modelo: Configuracion
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
    BASEDATOS_PUERTO: int = 0
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
            'puerto': mi.BASEDATOS_PUERTO,
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
# Funcion: configurar_microservicio
@lru_cache
def configurar_microservicio(modelo_base:Configuracion, ruta_origen:str, env_aplicacion:str=None, entorno:str=None) -> Configuracion:
    prefijo_entorno = f'{entorno.lower()}' if entorno else 'config'
    ruta_microservicio_path = Path(ruta_origen).parent
    lista_env:list[Path] = [(ruta_microservicio_path / f'.{prefijo_entorno}.env')]
    if env_aplicacion:
        lista_env.append((ruta_microservicio_path.parent / f'_config/.{prefijo_entorno}.{env_aplicacion}.env'))
    valores_configuracion = {
        'RUTA_MICROSERVICIO': ruta_microservicio_path.as_posix(),
        'MICROSERVICIO': ruta_microservicio_path.name,
    }
    for archivo in lista_env:
        if archivo.exists():
            valores_configuracion.update(dotenv_values(archivo))
    configuracion:Configuracion = modelo_base(**valores_configuracion)
    configuracion.URL_MICROSERVICIO = f'/{configuracion.APP_GLOBAL}/{configuracion.APP_PWA}'
    configuracion.PREFIJO_MICROSERVICIO = f'{configuracion.RAIZ_GLOBAL}/{configuracion.APP_PWA}'
    return configuracion

# --------------------------------------------------
# Funcion: configurar_servidor_api
def configurar_servidor_api(ruta_origen:str, archivo_env:str='.config.env'):
    try:
        archivo_env_path = Path(archivo_env)
        claves = dotenv_values(archivo_env_path)
        for clave, valor in claves.items():
            os.environ[clave] = valor
        ruta_lib_ffmpeg = Path(os.getenv('RUTA_LIB_FFMPEG','')).resolve()
        if ruta_lib_ffmpeg.is_dir():
            os.environ['PATH'] = str(ruta_lib_ffmpeg) + os.pathsep + os.getenv('PATH')
        if os.getenv('FRAMEWORK') == 'flask':
            from pysinergia.interfaces.flask import ServidorApi
        elif os.getenv('FRAMEWORK') == 'fastapi':
            from pysinergia.interfaces.fastapi import ServidorApi
        return ServidorApi(ruta_origen)
    except Exception as e:
        raise


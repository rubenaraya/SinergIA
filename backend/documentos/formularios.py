# --------------------------------------------------
# backend\documentos\formularios.py
# --------------------------------------------------

from typing import Optional

# Importaciones de Pydantic
from pydantic import (Field)

# Importaciones de PySinergIA
from pysinergia.modelos import (Formulario, Diccionario, VALIDACION, VISTA)

# --------------------------------------------------
# Modelo: DiccionarioDocumento
class DiccionarioDocumentos(Diccionario):
    nivcomplejidad:dict = {
        'alto': {'valor':'Alto', 'etiqueta':'Etiqueta-Alto'},
        'medio': {'valor':'Medio', 'etiqueta':'Etiqueta-Medio'},
        'bajo': {'valor':'Bajo', 'etiqueta':'Etiqueta-Bajo'},
    }
    coleccion:dict = {
        'ninguna': {'valor':'', 'etiqueta':''},
        'leykarin': {'valor':'LeyKarin', 'etiqueta':'Coleccion-Ley-Karin'}
    }

# --------------------------------------------------
# Modelo: FormActualizarDocumento
class FormActualizarDocumento(Formulario):
    dto_titulo:str = 'Form-Editar-documento'
    dto_icono:str = 'pencil-square'
    dto_grupos:dict = {'basicos': {'etiqueta':'Datos-basicos'}, 'avanzados': {'etiqueta':'Datos-avanzados'}}
    dto_acciones:dict = {'enviar': {'etiqueta':'Actualizar-documento', 'icono':'check-square', 'estilo':'primary'}}
    D:object = DiccionarioDocumentos

    uid: Optional[str] = Field(
        default=None,
        validation_alias='uid',
        title='UID',
        description='',
        json_schema_extra={'permisos':'', 'grupo':'basicos', 'requerido':True, 'minimo':16, 'maximo':16, 'vista': VISTA.HIDDEN, 'validacion': VALIDACION.NOVALIDAR, 'error': ''}
    )
    titulo: Optional[str] = Field(
        default=None,
        validation_alias='titulo',
        title='Etiqueta-Titulo',
        description='Marcador-Titulo',
        json_schema_extra={'permisos':'', 'grupo':'basicos', 'requerido':True, 'minimo':5, 'maximo':250, 'vista': VISTA.TEXT, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-tener-entre-(minimo)-y-(maximo)-caracteres', 'patron':''}
    )
    autores: Optional[str] = Field(
        default=None,
        validation_alias='autores',
        title='Etiqueta-Autores',
        description='Marcador-Autores',
        json_schema_extra={'permisos':'', 'grupo':'basicos', 'requerido':True, 'minimo':5, 'maximo':100, 'vista': VISTA.TEXT, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-tener-entre-(minimo)-y-(maximo)-caracteres', 'patron':''}
    )
    editor: Optional[str] = Field(
        default=None,
        validation_alias='editor',
        title='Etiqueta-Editor',
        description='Marcador-Editor',
        json_schema_extra={'permisos':'', 'grupo':'basicos', 'requerido':True, 'minimo':5, 'maximo':100, 'vista': VISTA.TEXT, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-tener-entre-(minimo)-y-(maximo)-caracteres', 'patron':''}
    )
    fechapub: Optional[str] = Field(
        default=None,
        validation_alias='fechapub',
        title='Etiqueta-Fecha-publicacion',
        description='Marcador-Fecha-publicacion',
        json_schema_extra={'permisos':'', 'grupo':'basicos', 'requerido':False, 'minimo':0, 'maximo':30, 'vista': VISTA.TEXT, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-ser-una-fecha-valida', 'patron':''}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        validation_alias='etiquetas',
        title='Etiqueta-Etiquetas',
        description='Marcador-Etiquetas',
        json_schema_extra={'permisos':'', 'grupo':'avanzados', 'requerido':False, 'minimo':0, 'maximo':250, 'vista': VISTA.TEXTAREA, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-tener-maximo-(maximo)-caracteres', 'patron':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        validation_alias='palabras',
        title='Etiqueta-Palabras-clave',
        description='Marcador-Palabras-clave',
        json_schema_extra={'permisos':'', 'grupo':'avanzados', 'requerido':False, 'minimo':0, 'maximo':250, 'vista': VISTA.TEXTAREA, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-tener-maximo-(maximo)-caracteres', 'patron':''}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        validation_alias='tipodoc',
        title='Etiqueta-Tipo',
        description='Marcador-Tipo',
        json_schema_extra={'permisos':'', 'grupo':'avanzados', 'requerido':False, 'minimo':0, 'maximo':30, 'vista': VISTA.TEXT, 'validacion': VALIDACION.TEXTO, 'error': '(etiqueta)-debe-tener-maximo-(maximo)-caracteres', 'patron':''}
    )
    nivcomplejidad: Optional[str] = Field(
        default=None,
        validation_alias='nivcomplejidad',
        title='Etiqueta-Nivel-complejidad',
        description='Marcador-Nivel-complejidad',
        json_schema_extra={'permisos':'', 'grupo':'avanzados', 'requerido':False, 'minimo':0, 'maximo':10, 'vista': VISTA.SELECT, 'validacion': VALIDACION.OPCIONES, 'error': '(etiqueta)-debe-ser-un-elemento-de-la-lista', 'diccionario':'nivcomplejidad'}
    )
    coleccion: Optional[str] = Field(
        default=None,
        validation_alias='coleccion',
        title='Etiqueta-Coleccion',
        description='Marcador-Coleccion',
        json_schema_extra={'permisos':'', 'grupo':'avanzados', 'requerido':False, 'minimo':0, 'maximo':30, 'vista': VISTA.SELECT, 'validacion': VALIDACION.OPCIONES, 'error': '(etiqueta)-debe-ser-un-elemento-de-la-lista', 'diccionario':'coleccion'}
    )

__all__ = ['FormActualizarDocumento']

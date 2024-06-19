# backend\participantes\dominio.py

from typing import Optional
from pydantic import Field

from pysinergia.base import (
    C,
    Peticion,
    Procedimiento,
    Formulario,
    Diccionario,
    Informe,
)

# --------------------------------------------------
# ClaseModelo: PeticionBuscarParticipantes
# --------------------------------------------------
class PeticionBuscarParticipantes(Peticion):
    id: Optional[int] = Field(
        default=None,
        serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'orden':'DESC', 'entidad':''}
    )
    alias: Optional[str] = Field(
        default=None,
        title='Alias',
        description='Nombre del participante',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    email: Optional[str] = Field(
        default=None,
        title='E-Mail',
        description='Correo-e del participante',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    estado: Optional[str] = Field(
        default=None,
        title='Estado',
        description='Estado del participante',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'COINCIDE', 'orden':'', 'entidad':''}
    )
    maximo: Optional[int] = Field(serialization_alias='maximo', default=0)
    pagina: Optional[int] = Field(serialization_alias='pagina', default=0)

# --------------------------------------------------
# ClaseModelo: ProcedimientoBuscarParticipantes
# --------------------------------------------------
class ProcedimientoBuscarParticipantes(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'entidad':''}
    )
    alias: Optional[str] = Field(
        default=None,
        title='Alias',
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'entidad':''}
    )
    email: Optional[str] = Field(
        default=None,
        title='E-Mail',
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'entidad':''}
    )
    estado: Optional[str] = Field(
        default=None,
        title='Estado',
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: PeticionParticipante
# --------------------------------------------------
class PeticionParticipante(Peticion):
    id: Optional[int] = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: PeticionAgregarParticipante
# --------------------------------------------------
class PeticionAgregarParticipante(Peticion):
    alias: Optional[str] = Field(
        default=None,
        title='Alias',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    email: Optional[str] = Field(
        default=None,
        title='E-Mail',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    estado: Optional[str] = Field(
        default=None,
        title='Estado',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoActualizarParticipante
# --------------------------------------------------
class ProcedimientoActualizarParticipante(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] = Field(
        default=None,
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'formato':'integer', 'permisos':''}
    )
    alias: Optional[str] = Field(
        default=None,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    email: Optional[str] = Field(
        default=None,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    estado: Optional[str] = Field(
        default=None,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

# --------------------------------------------------
# ClaseModelo: DiccionarioParticipantes
# --------------------------------------------------
class DiccionarioParticipantes(Diccionario):
    estado:dict = {
        'activo': {'valor':'Activo', 'etiqueta':'Estado-Activo', 'estilo':'success'},
        'inactivo': {'valor':'Inactivo', 'etiqueta':'Estado-Inactivo', 'estilo':'warning'},
        'archivado': {'valor':'Archivado', 'etiqueta':'Estado-Archivado', 'estilo':'secondary'},
    }

# --------------------------------------------------
# ClaseModelo: FormActualizarParticipante
# --------------------------------------------------
class FormActualizarParticipante(Formulario):
    dto_titulo:str = 'Form-Editar-participante'
    dto_icono:str = 'pencil-square'
    dto_grupos:dict = {'general': {'etiqueta':'Datos-basicos'}, 'perfil': {'etiqueta':'Perfil-participante'}}
    dto_acciones:dict = {'enviar': {'etiqueta':'Actualizar-participante', 'icono':'check-square', 'estilo':'primary'}}
    D:object = DiccionarioParticipantes 

    id:int = Field(
        default=None,
        validation_alias='id',
    )
    alias:str = Field(
        default=None,
        validation_alias='nombre',
        serialization_alias='alias',
        title='Nombre-participante',
        description='Alias-del-participante',
        max_length=25,
        json_schema_extra={'grupo':'general', 'vista': C.CAMPO.TEXT, 'requerido':True, 'validacion': C.VALIDACION.TEXTO, 'error':'Nombre-debe-tener-entre-(minimo)-y-(maximo)-caracteres', 'minimo':5, 'maximo':25}
    )
    email:str = Field(
        default=None,
        validation_alias='email',
        title='Correo-e-participante',
        description='Correo-electronico-del-participante',
        max_length=50,
        json_schema_extra={'grupo':'general', 'vista': C.CAMPO.TEXT, 'requerido':True, 'validacion': C.VALIDACION.TEXTO, 'error':'Debe-ingresar-un-correo-electronico-valido', 'minimo':7, 'maximo':50, 'patron':'[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})'}
    )
    estado:str = Field(
        default=None,
        validation_alias='estado',
        title='Estado-participante',
        description='Estado-del-participante',
        json_schema_extra={'grupo':'perfil', 'vista': C.CAMPO.SELECT, 'validacion': C.VALIDACION.TEXTO, 'error':'Debe-elegir-un-estado', 'minimo':1, 'maximo':10, 'diccionario':'estado'}
    )

# --------------------------------------------------
# ClaseModelo: FormLogin
# --------------------------------------------------
class FormLogin(Formulario):
    dto_titulo:str = 'Form-Autenticacion'
    dto_icono:str = 'person-exclamation'
    dto_grupos:dict = {'general': {'etiqueta':'Datos-para-iniciar-sesion'}}
    dto_acciones:dict = {'enviar': {'etiqueta':'Iniciar-sesion', 'icono':'box-arrow-in-right', 'estilo':'primary'}}

    username: Optional[str] = Field(
        default=None,
        validation_alias='username',
        serialization_alias='email',
        title='Nombre-usuario',
        description='Nombre-de-usuario',
        max_length=50,
        json_schema_extra={'grupo':'general', 'vista': C.CAMPO.EMAIL, 'requerido':True, 'validacion': C.VALIDACION.TEXTO, 'error':'Debe-ingresar-su-nombre-de-usuario', 'minimo':7, 'maximo':50, 'autocompletar':'username', 'patron':'[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})'}
    )
    password: Optional[str] = Field(
        default=None,
        validation_alias='password',
        serialization_alias='clave',
        title='Contraseña-usuario',
        description='Contraseña-del-usuario',
        max_length=50,
        json_schema_extra={'grupo':'general', 'vista': C.CAMPO.PASSWORD, 'requerido':True, 'validacion': C.VALIDACION.TEXTO, 'error':'Debe-ingresar-su-contraseña', 'minimo':5, 'maximo':15, 'autocompletar':'current-password', 'patron':'[A-Za-z0-9.,_-]+'}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoAgregarParticipante
# --------------------------------------------------
class ProcedimientoAgregarParticipante(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    alias: Optional[str] = Field(
        default=None,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    email: Optional[str] = Field(
        default=None,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    estado: Optional[str] = Field(
        default=None,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoEliminarParticipante
# --------------------------------------------------
class ProcedimientoEliminarParticipante(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] = Field(
        default=None,
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'formato':'integer', 'permisos':''}
    )


# pysinergia\servicio.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import (
    ModeloRespuesta as _ModeloRespuesta,
    ModeloPeticion as _ModeloPeticion,
)
from pysinergia.globales import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: Servicio
# --------------------------------------------------
class Servicio:

    def __init__(mi, operador, sesion:dict=None):
        mi.operador = operador
        mi.sesion:dict = sesion

    def solicitar_accion(mi, accion:int, peticion):
        return NotImplementedError

    def autorizar_roles(mi, roles:str, rechazar:bool=False) -> bool:
        if roles == '':
            return True
        credenciales:str = mi.sesion.get('roles')
        if roles and credenciales:
            if roles == '*':
                return True
            eval_roles = set(roles.split(','))
            eval_credenciales = set(credenciales.split(','))
            if bool(eval_roles & eval_credenciales):
                return True
        if rechazar:
            raise _ErrorPersonalizado(
                mensaje='No tiene permisos para realizar esta acción.',
                tipo=_Constantes.SALIDA.ALERTA,
                codigo=_Constantes.ESTADO.HTTP_403_NO_AUTORIZADO,
            )
        return False


# --------------------------------------------------
# ClaseModelo: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(_ModeloRespuesta):
    codigo: int | None = _Constantes.ESTADO.HTTP_200_EXITO
    tipo: str | None = _Constantes.SALIDA.EXITO
    mensaje: str | None = ''
    resultado: dict | None = {}
    esquemas: dict | None = {}

    def asignar_contexto(mi, estado:int, mensaje:str=''):
        mi.codigo = estado
        mi.tipo = _Funciones.tipo_salida(estado)
        if mensaje:
            mi.mensaje = mensaje


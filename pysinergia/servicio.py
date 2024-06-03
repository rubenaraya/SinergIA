# pysinergia\servicio.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: Servicio
# --------------------------------------------------
class Servicio:

    def __init__(mi, operador, sesion:dict=None):
        mi.operador = operador
        mi.sesion:dict = sesion

    def solicitar_accion(mi, accion:int, peticion:dict) -> dict:
        raise NotImplementedError()

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
                mensaje='No-autorizado-para-acceder',
                tipo=_Constantes.SALIDA.ALERTA,
                codigo=_Constantes.ESTADO._403_NO_AUTORIZADO,
            )
        return False

    def adjuntar_opciones(mi, opciones:dict, info:dict=None) -> dict:
        requeridas = {
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
        if info is None:
            info = {}
        for clave, valor in requeridas.items():
            if clave not in info:
                info[clave] = valor
        if opciones is not None:
            for clave, valor in opciones.items():
                info[clave] = valor
        return info


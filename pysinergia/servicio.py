# pysinergia\servicio.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes,
    ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: CasosDeUso
# --------------------------------------------------
class CasosDeUso:

    class ACCIONES:
        ...

    def __init__(mi, repositorio, sesion:dict=None):
        mi.repositorio = repositorio
        mi.sesion:dict = sesion

    def solicitar_accion(mi, accion:ACCIONES, peticion:dict) -> dict:
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
            raise ErrorPersonalizado(
                mensaje='No-autorizado-para-acceder',
                conclusion=Constantes.CONCLUSION.ALERTA,
                codigo=Constantes.ESTADO._403_NO_AUTORIZADO,
            )
        return False

    def agregar_metadatos(mi, metadatos:dict, info:dict=None) -> dict:
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
        if info is None:
            info = {}
        for clave, valor in requeridos.items():
            if clave not in info:
                info[clave] = valor
        if metadatos is not None:
            for clave, valor in metadatos.items():
                info[clave] = valor
        return info


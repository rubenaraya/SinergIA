# --------------------------------------------------
# pysinergia\servicio.py
# --------------------------------------------------

from abc import (ABC)

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes,
    ErrorPersonalizado,
)
from pysinergia.dominio import autorizar_acceso

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


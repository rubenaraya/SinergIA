# pysinergia\dominio.py

from typing import Dict

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from pydantic import BaseModel

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
)

# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad:
    ...


# --------------------------------------------------
# ClaseModelo: ModeloPeticion
# --------------------------------------------------
class ModeloPeticion(BaseModel):

    def diccionario(mi) -> Dict:
        return mi.model_dump()

    def json(mi) -> str:
        return mi.model_dump_json()


# --------------------------------------------------
# ClaseModelo: ModeloRespuesta
# --------------------------------------------------
class ModeloRespuesta(BaseModel):

    def diccionario(mi) -> Dict:
        return mi.model_dump()

    def json(mi) -> str:
        return mi.model_dump_json()


# --------------------------------------------------
# ClaseModelo: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(ModeloRespuesta):
    codigo: int | None = _Constantes.ESTADO.HTTP_200_EXITO
    tipo: str | None = _Constantes.SALIDA.EXITO
    mensaje: str | None = ''
    resultado: dict | None = {}
    esquemas: dict | None = {}
    opciones: dict | None = {}

    def asignar_contexto(mi, estado:int, mensaje:str=''):
        mi.codigo = estado
        mi.tipo = _Funciones.tipo_salida(estado)
        if mensaje:
            mi.mensaje = mensaje


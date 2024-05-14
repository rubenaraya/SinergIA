# pysinergia\servicio.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import ModeloRespuesta as _ModeloRespuesta
from pysinergia.globales import (
    Constantes as _Constantes,
    Funciones as _Funciones,
)

# --------------------------------------------------
# Clase: Servicio
# --------------------------------------------------
class Servicio:
    ...


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

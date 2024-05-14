# pysinergia\servicio.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import ModeloRespuesta as _ModeloRespuesta
from pysinergia.globales import Constantes as _Constantes

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


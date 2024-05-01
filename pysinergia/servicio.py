# pysinergia\servicio.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import ModeloRespuesta as _ModeloRespuesta

# --------------------------------------------------
# Clase: Servicio
# --------------------------------------------------
class Servicio:
    ...


# --------------------------------------------------
# ClaseModelo: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(_ModeloRespuesta):
    codigo: int | None = 200
    tipo: str | None = 'EXITO'
    mensaje: str | None = ''
    resultado: dict | None = {}
    esquemas: dict | None = {}


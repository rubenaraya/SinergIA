# pysinergia\dependencias\web_flask.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from flask import (
    Response,
    Blueprint,
    request,
    make_response
)
from flask_cors import cross_origin
from functools import lru_cache
import os

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Funciones as F,
    Constantes as C,
    Json,
    ErrorPersonalizado,
)
from pysinergia.servicio import RespuestaResultado

from pysinergia.web_flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

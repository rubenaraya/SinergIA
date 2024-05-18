# pysinergia\dependencias\web_flask.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from flask import (
    Response,
    Blueprint,
    request,
    redirect,
    make_response,
    send_file,
)
from flask_cors import cross_origin
from flask_pydantic import validate
import os, gettext

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Funciones as F,
    Constantes as C,
    Json,
    ErrorPersonalizado,
)
from pysinergia.adaptadores import obtener_config
from pysinergia.web_flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

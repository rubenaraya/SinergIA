# pysinergia\_dependencias\web_flask.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from flask import (
    Response,
    Blueprint,
    request,
    redirect,
    make_response,
    send_file,
    jsonify
)
from flask_cors import cross_origin
from flask_pydantic import validate
import os, filetype

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Funciones as F,
    Constantes as C,
    Json,
    ErrorPersonalizado,
)
from pysinergia.dominio import (
    CargaAudio,
    CargaDocumento,
    CargaImagen,
    CargaVideo,
    CargaArchivo,
)
from pysinergia.adaptadores import (
    cargar_configuracion,
)
from pysinergia.interfaces.web_flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

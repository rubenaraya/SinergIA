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

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as C,
    ErrorPersonalizado,
)
from pysinergia.dominio import (
    CargaAudio,
    CargaDocumento,
    CargaImagen,
    CargaVideo,
    ModeloRespuesta,
)
from pysinergia.adaptadores import (
    cargar_configuracion,
)
from pysinergia.web import Traductor
from pysinergia.interfaces.web_flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

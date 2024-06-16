# pysinergia\base\flask.py

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
from pysinergia.web.flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

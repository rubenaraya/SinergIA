# pysinergia\dependencias\web_fastapi.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    APIRouter,
    Request,
    status,
    Depends,
    Body,
    Header,
)
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse,
    Response
)
from functools import lru_cache
import os

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Funciones,
    Constantes,
    ErrorPersonalizado,
)
from pysinergia.servicio import RespuestaResultado

from pysinergia.web_fastapi import (
    ComunicadorWeb,
    AutenticadorWeb,
)

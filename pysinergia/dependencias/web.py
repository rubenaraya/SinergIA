# pysinergia\dependencias\web.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    APIRouter,
    status,
    Depends,
    Body,
)
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse,
)
from functools import lru_cache

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Funciones,
    Constantes,
    ErrorPersonalizado,
)
from pysinergia.servicio import RespuestaResultado
from pysinergia.web import (
    ComunicadorWeb,
    AutenticadorJWT,
)

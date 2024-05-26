# pysinergia\_dependencias\web_fastapi.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    APIRouter,
    Request,
    Depends,
    Body,
    Header,
    UploadFile,
)
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse,
    Response,
)
import os

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Funciones as F,
    Constantes as C,
    ErrorPersonalizado,
)
from pysinergia.adaptadores import (
    cargar_configuracion,
)
from pysinergia.interfaces.web_fastapi import (
    ComunicadorWeb,
    AutenticadorWeb,
)

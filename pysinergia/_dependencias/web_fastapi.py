# pysinergia\_dependencias\web_fastapi.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    APIRouter,
    Request,
    Depends,
    Body,
    Header,
    File,
    Form,
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

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Funciones as F,
    Constantes as C,
    ErrorPersonalizado,
)
from pysinergia.dominio import (
    CargaAudio,
    CargaDocumento,
    CargaImagen,
    CargaVideo,
)
from pysinergia.adaptadores import (
    cargar_configuracion,
)
from pysinergia.interfaces.web_fastapi import (
    ComunicadorWeb,
    AutenticadorWeb,
)

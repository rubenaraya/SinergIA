# pysinergia\base\fastapi.py

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
from pysinergia.web.fastapi import (
    ComunicadorWeb,
    AutenticadorWeb,
)

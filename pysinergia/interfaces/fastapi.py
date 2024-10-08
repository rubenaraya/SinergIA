# --------------------------------------------------
# pysinergia\interfaces\fastapi.py
# --------------------------------------------------

import os
from pathlib import Path

# Importaciones de FastAPI
from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import (
    JSONResponse,
    RedirectResponse,
    FileResponse,
    Response,
)

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as C,
    ErrorPersonalizado,
)
from pysinergia.modelos import Respuesta
from pysinergia.interfaces.web import (
    Comunicador,
    Autenticador,
    ErrorAutenticacion,
    Traductor,
)

# --------------------------------------------------
# Clase: ServidorApi
class ServidorApi:
    def __init__(mi, ruta_script:str):
        ruta_script_path = Path(ruta_script)
        os.environ['RUTA_RAIZ'] = ruta_script_path.parent.as_posix()
        mi.nombre_script = ruta_script_path.stem

    # Métodos privados

    def _configurar_encabezados(mi, api:FastAPI):
        
        @api.middleware("http")
        async def configurar_encabezados_(request:Request, call_next):
            if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO:
                content_type = str(request.headers.get('Content-Type', ''))
                if content_type:
                    print(f'peticion: {content_type}')
            respuesta:Response = await call_next(request)
            respuesta.headers["X-API-Motor"] = 'PySinergIA'
            if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO and respuesta.status_code >= 200:
                content_type = str(respuesta.headers.get('Content-Type', ''))
                print(f'respuesta: {content_type} | {str(respuesta.status_code)}')
            return respuesta

    def _configurar_endpoints(mi, api:FastAPI):

        @api.get('/', include_in_schema=False)
        def entrypoint():
            return {'api-entrypoint': 'PySinergIA'}

        @api.get('/favicon.ico', include_in_schema=False)
        def favicon():
            ruta_favicon = Path(mi.dir_frontend) / 'favicon.ico'
            return FileResponse(str(ruta_favicon))

    def _configurar_cors(mi, api:FastAPI):
        from fastapi.middleware.cors import CORSMiddleware
        api.add_middleware(
            CORSMiddleware,
            allow_origins = os.getenv('ORIGENES_CORS'),
            allow_credentials = True,
            allow_methods = ['*'],
            allow_headers = ['*'],
        )

    def _obtener_url(mi, request:Request) -> str:
        url = f'{request.url.path}?{request.query_params}' if request.query_params else request.url.path
        return f'{request.method} {url}'

    def _crear_respuesta_error(mi, request:Request, err:ErrorPersonalizado):
        registrar_detalles = bool(os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO)
        if (err.codigo >= 500) or registrar_detalles:
            err.registrar(texto_pre=mi._obtener_url(request), exc_info=registrar_detalles)
        traductor = Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
        traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'), dominio_idioma=err.dominio_idioma)
        respuesta = Respuesta(**err.exportar(), T=traductor).diccionario()
        return JSONResponse(content=respuesta, status_code=err.codigo)

    def _manejar_errores(mi, api:FastAPI):
        from fastapi.exceptions import (
            RequestValidationError,
            HTTPException,
        )
        from pydantic import ValidationError

        @api.exception_handler(ErrorAutenticacion)
        async def _error_autenticacion(request:Request, err:ErrorAutenticacion):
            if err.url_login:
                return RedirectResponse(url=err.url_login)
            return mi._crear_respuesta_error(request, err)

        @api.exception_handler(ErrorPersonalizado)
        async def _error_personalizado(request:Request, err:ErrorPersonalizado):
            return mi._crear_respuesta_error(request, err)

        @api.exception_handler(RequestValidationError)
        async def _error_procesar_solicitud(request:Request, err:RequestValidationError):
            error = ErrorPersonalizado(mensaje='Los-datos-recibidos-no-se-procesaron', codigo=C.ESTADO._422_NO_PROCESABLE, nivel_evento=C.REGISTRO.INFO, detalles=err.errors())
            return mi._crear_respuesta_error(request, error)

        @api.exception_handler(ValidationError)
        async def _error_validacion(request:Request, err:ValidationError):
            error = ErrorPersonalizado(mensaje='Los-datos-recibidos-son-invalidos', codigo=C.ESTADO._422_NO_PROCESABLE, nivel_evento=C.REGISTRO.INFO, detalles=err.errors())
            return mi._crear_respuesta_error(request, error)

        @api.exception_handler(HTTPException)
        async def _error_http(request:Request, err:HTTPException):
            error = ErrorPersonalizado(mensaje=err.detail, codigo=err.status_code, nivel_evento=C.REGISTRO.DEBUG if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO else C.REGISTRO.ERROR)
            return mi._crear_respuesta_error(request, error)

        @api.exception_handler(Exception)
        async def _error_nomanejado(request:Request, err:Exception):
            error = ErrorPersonalizado(mensaje='Error-no-manejado', codigo=C.ESTADO._500_ERROR, nivel_evento=C.REGISTRO.ERROR)
            return mi._crear_respuesta_error(request, error)

    # Métodos públicos

    def crear_api(mi) -> FastAPI:
        from fastapi.staticfiles import StaticFiles
        mi.dir_frontend = ( Path('.') / str(os.getenv('DIR_FRONTEND',''))).resolve()
        docs_url = '/docs' if os.getenv('DOCS') else None
        redoc_url = '/redoc' if os.getenv('DOCS') else None
        api = FastAPI(
            docs_url=docs_url,
            redoc_url=redoc_url,
        )
        api.mount(f"{str(os.getenv('RAIZ_GLOBAL',''))}/{str(os.getenv('ALIAS_FRONTEND',''))}", StaticFiles(directory=f'{mi.dir_frontend.as_posix()}'), name='frontend')
        mi._configurar_cors(api)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        mi._manejar_errores(api)
        return api

    def mapear_microservicios(mi, api:FastAPI):
        import importlib
        ruta_backend = Path(os.getenv('DIR_BACKEND'))
        modulo_base = 'web_fastapi'
        directorios = [d for d in ruta_backend.iterdir() if d.is_dir()]
        for directorio in directorios:
            try:
                if (directorio / f'{modulo_base}.py').is_file():
                    dir_backend = os.getenv('DIR_BACKEND')
                    modulo = f'{dir_backend}.{directorio.name}.{modulo_base}'
                    enrutador = importlib.import_module(modulo)
                    api.include_router(getattr(enrutador, 'enrutador'))
            except Exception:
                ErrorPersonalizado(mensaje='No-se-pudo-registrar-el-microservicio', codigo=C.ESTADO._500_ERROR, nivel_evento=C.REGISTRO.WARNING, recurso=str(directorio)).registrar()
                continue

    def iniciar_servicio_web(mi, app:str, puerto:int, host:str=None):
        if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO or os.getenv('ENTORNO') == C.ENTORNO.LOCAL:
            import uvicorn
            if not host:
                host = os.getenv('HOST_LOCAL')
            uvicorn.run(
                app,
                host=host,
                port=int(puerto),
                ssl_keyfile=os.getenv('SSL_KEY',''),
                ssl_certfile=os.getenv('SSL_CERT',''),
                reload=os.getenv('MODO_DEBUG')
            )

# --------------------------------------------------
# Clase: ComunicadorWeb
class ComunicadorWeb(Comunicador):

    # Métodos privados

    async def _recibir_peticion(mi, request:Request) -> dict:
        peticion = {}
        try:
            form_data = await request.form()
            for key, value in form_data.multi_items():
                if hasattr(value, 'file'):
                    continue
                if key in peticion:
                    peticion[key].append(value)
                else:
                    peticion[key] = form_data.getlist(key) if len(form_data.getlist(key)) > 1 else value
            try:
                json_data = await request.json()
                for key, value in json_data.items():
                    if key in peticion:
                        if not isinstance(peticion[key], list):
                            peticion[key] = [peticion[key]]
                        peticion[key].append(value)
                    else:
                        peticion[key] = value
            except Exception:
                pass
            for key, value in request.query_params.multi_items():
                if key in peticion:
                    if not isinstance(peticion[key], list):
                        peticion[key] = [peticion[key]]
                    peticion[key].append(value)
                else:
                    peticion[key] = request.query_params.getlist(key) if len(request.query_params.getlist(key)) > 1 else value
        except Exception as e:
            pass
        return peticion

    # Métodos públicos

    async def procesar_solicitud(mi, request:Request, idiomas_aceptados:str=None, sesion:dict=None):
        super().procesar_solicitud(idiomas_aceptados, sesion)
        from urllib.parse import urlparse
        alias_frontend = mi.config_web.get('ALIAS_FRONTEND')
        url_analizada = urlparse(str(request.url))
        servidor = f'{url_analizada.scheme}://{url_analizada.netloc}'
        partes = url_analizada.path.lstrip('/').split('/')
        raiz_global = '/' + partes[0] if len(partes) > 0 else ''
        app_pwa = '/' + partes[1] if len(partes) > 1 else ''
        recurso = '/' + '/'.join(partes[2:]) if len(partes) > 2 else '/'
        mi.contexto['url'] = {
            'servidor': servidor,
            'absoluta': f'{servidor}{url_analizada.path}',
            'relativa': url_analizada.path,
            'puntoentrada': f'{servidor}{raiz_global}',
            'puntofinal': f'{app_pwa}{recurso}',
            'app': f'{raiz_global}{app_pwa}',
            'recurso': recurso,
            'frontend': f'{raiz_global}/{alias_frontend}',
            'frontapp': f'{raiz_global}/{alias_frontend}{app_pwa}',
        }
        mi.contexto['web']['API_MARCO'] = 'FastAPI'
        mi.contexto['web']['DOMINIO'] = url_analizada.hostname
        mi.contexto['web']['ACEPTA'] = request.headers.get('accept', '')
        mi.contexto['peticion'] = await mi._recibir_peticion(request)
        mi.contexto['cookies'] = {}
        if request.cookies:
            for nombre, valor in request.cookies.items():
                mi.contexto['cookies'][nombre] = valor

    def asignar_cookie(mi, respuesta:Response, nombre:str, valor:str, duracion:int=None):
        alcance = mi.contexto['url'].get('app') if mi.contexto.get('url') else '/'
        duracion = mi.config_web.get('DURACION_TOKEN') if not duracion else duracion
        respuesta.set_cookie(
            key=nombre,
            value=valor,
            max_age=duracion,
            path=alcance,
            secure=True,
            httponly=False
        )
        return respuesta

# --------------------------------------------------
# Clase: AutenticadorWeb
class AutenticadorWeb(Autenticador):

    async def validar_apikey(mi, request:Request) -> str:
        if 'Authorization' in request.headers:
            api_key_header = request.headers.get('Authorization').replace('Bearer ', '')
            if mi.api_keys and api_key_header and api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
        mensaje = 'API-key-invalida'
        raise ErrorAutenticacion(
            mensaje=mensaje,
            codigo=C.ESTADO._403_NO_AUTORIZADO,
        )

    async def validar_token(mi, request:Request) -> str:
        mensaje = 'Encabezado-de-autorizacion-invalido'
        if 'X-Token' in request.headers:
            sesion_token_header = request.headers.get('X-Token')
            if sesion_token_header:
                mi.token = sesion_token_header
                if not mi._verificar_jwt():
                    mensaje = 'Token-invalido'
                else:
                    return mi.token
        raise ErrorAutenticacion(
            mensaje=mensaje,
            codigo=C.ESTADO._401_NO_AUTENTICADO,
            url_login=mi.url_login
        )

    async def validar_todo(mi, request:Request):
        await mi.validar_apikey(request)
        await mi.validar_token(request)


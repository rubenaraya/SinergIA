# pysinergia\interfaces\web_fastapi.py

import os
from pathlib import Path

# --------------------------------------------------
# Importaciones de Infraestructura Web
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
from fastapi.encoders import jsonable_encoder

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _C,
    Funciones as _F,
    ErrorPersonalizado as _ErrorPersonalizado,
    ErrorAutenticacion as _ErrorAutenticacion,
    ErrorDisco as _ErrorDisco,
    RegistradorLogs as _RegistradorLogs,
    Traductor as _Traductor,
)
from pysinergia.dominio import ModeloRespuesta
from pysinergia.web import (
    Comunicador as _Comunicador,
    Autenticador as _Autenticador,
)
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi:
    def __init__(mi, app_web:str, raiz_api:str=''):
        os.environ['RAIZ_API'] = raiz_api
        os.environ['APP_WEB'] = app_web
        mi.entorno:str = None

    # --------------------------------------------------
    # Métodos privados

    def _configurar_encabezados(mi, api:FastAPI):
        @api.middleware("http")
        async def configurar_encabezados_(request:Request, call_next):
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                content_type = str(request.headers.get('Content-Type', ''))
                if content_type:
                    print(f'peticion: {content_type}')
            respuesta:Response = await call_next(request)
            respuesta.headers["X-API-Motor"] = api_motor
            if mi.entorno == _C.ENTORNO.DESARROLLO and respuesta.status_code >= 200:
                content_type = str(respuesta.headers.get('Content-Type', ''))
                print(f'respuesta: {content_type} | {str(respuesta.status_code)}')
            return respuesta

    def _configurar_endpoints(mi, api:FastAPI):

        @api.get('/', include_in_schema=False)
        def entrypoint():
            return {'api-entrypoint': f'{api_motor}'}

        @api.get('/favicon.ico', include_in_schema=False)
        def favicon():
            ruta_favicon = Path(mi.dir_frontend) / 'favicon.ico'
            return FileResponse(str(ruta_favicon))

    def _configurar_cors(mi, api:FastAPI, origenes_cors:list):
        from fastapi.middleware.cors import CORSMiddleware
        api.add_middleware(
            CORSMiddleware,
            allow_origins = origenes_cors,
            allow_credentials = True,
            allow_methods = ['*'],
            allow_headers = ['*'],
        )

    def _obtener_url(mi, request:Request) -> str:
        url = f'{request.url.path}?{request.query_params}' if request.query_params else request.url.path
        return f'{request.method} {url}'

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, dir_frontend:str, alias_frontend:str, origenes_cors:list=['*'], titulo:str='', descripcion:str='', version:str='', doc:bool=False, entorno:str='') -> FastAPI:
        from fastapi.staticfiles import StaticFiles
        mi.dir_frontend = (Path(_F.obtener_ruta_raiz()) / f'{dir_frontend}').resolve()
        os.environ['ALIAS_FRONTEND'] = alias_frontend
        docs_url = '/docs' if doc else None
        redoc_url = '/redoc' if doc else None
        api = FastAPI(
            title=titulo,
            description=descripcion,
            version=version,
            docs_url=docs_url,
            redoc_url=redoc_url,
        )
        mi.titulo = titulo
        mi.descripcion = descripcion
        mi.version = version
        mi.entorno = entorno
        api.mount(f"{str(os.getenv('RAIZ_API', ''))}/{alias_frontend}", StaticFiles(directory=f'{mi.dir_frontend.as_posix()}'), name='frontend')
        mi._configurar_cors(api, origenes_cors)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        return api

    def mapear_enrutadores(mi, api:FastAPI, ubicacion:str):
        import importlib
        ruta_ubicacion = Path(ubicacion)
        modulo_base = 'web_fastapi'
        try:
            directorios = [d for d in ruta_ubicacion.iterdir() if d.is_dir()]
        except Exception as e:
            print(e)
            return
        for directorio in directorios:
            try:
                nombre_servicio = directorio.name
                if (directorio / f'{modulo_base}.py').is_file():
                    enrutador = importlib.import_module(f'{ubicacion}.{nombre_servicio}.{modulo_base}')
                    api.include_router(getattr(enrutador, 'enrutador'))
            except Exception as e:
                print(e)
                continue

    def iniciar_servicio(mi, app:str, host:str, puerto:int):
        if mi.entorno == _C.ENTORNO.DESARROLLO or mi.entorno == _C.ENTORNO.LOCAL:
            import uvicorn
            uvicorn.run(
                app,
                host=host,
                port=puerto,
                ssl_keyfile='key.pem',
                ssl_certfile='cert.pem',
                reload=True if mi.entorno == _C.ENTORNO.DESARROLLO else False
            )

    def manejar_errores(mi, api:FastAPI, dir_logs:str, archivo_logs:str, idiomas_disponibles:list):
        from fastapi.exceptions import (
            RequestValidationError,
            HTTPException,
        )
        from pydantic import ValidationError

        @api.exception_handler(_ErrorPersonalizado)
        async def _error_personalizado(request:Request, exc:_ErrorPersonalizado):
            traductor = _Traductor({'dominio': exc.traduccion, 'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            salida = ModeloRespuesta(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=exc.mensaje,
                detalles=exc.detalles,
                T=traductor
            ).diccionario()
            if exc.tipo == _C.SALIDA.ERROR:
                nombre = archivo_logs
                if exc.aplicacion and exc.servicio:
                    nombre = f'{exc.aplicacion}_{exc.servicio}'
                _RegistradorLogs.crear(f'{nombre}', 'ERROR', f'{dir_logs}/{nombre}.log').error(
                    f'{mi._obtener_url(request)} | {salida.__str__()}'
                )
            return JSONResponse(
                status_code=exc.codigo,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(_ErrorAutenticacion)
        async def _error_autenticacion(request:Request, exc:_ErrorAutenticacion):
            if exc.url_login:
                return RedirectResponse(url=exc.url_login)
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            salida = ModeloRespuesta(
                codigo=exc.codigo,
                tipo=_C.SALIDA.ALERTA,
                mensaje=exc.mensaje,
                detalles=[],
                T=traductor
            ).diccionario()
            return JSONResponse(
                status_code=exc.codigo,
                content=jsonable_encoder(salida)
        )

        @api.exception_handler(_ErrorDisco)
        async def _error_disco(request:Request, exc:_ErrorDisco):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            salida = ModeloRespuesta(
                codigo=exc.codigo,
                tipo='ERROR',
                mensaje=exc.mensaje,
                detalles=exc.detalles,
                T=traductor
            ).diccionario()
            _RegistradorLogs.crear(f'{archivo_logs}', 'ERROR', f'{dir_logs}/{archivo_logs}.log').error(
                f'{mi._obtener_url(request)} | {salida.__str__()}'
            )
            return JSONResponse(
                status_code=exc.codigo,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(ValidationError)
        async def _error_validacion(request:Request, exc:ValidationError):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            errores = exc.errors()
            detalles = []
            for error in errores:
                detalles.append({
                    'tipo': error['type'],
                    'error': error['msg'],
                    'origen': error['loc'],
                    'valor': error['input']
                })
            salida = ModeloRespuesta(
                codigo=_C.ESTADO._422_NO_PROCESABLE,
                tipo=_C.SALIDA.ALERTA,
                mensaje='Los-datos-recibidos-son-invalidos',
                detalles=detalles,
                T=traductor
            ).diccionario()
            return JSONResponse(
                status_code=_C.ESTADO._422_NO_PROCESABLE,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(RequestValidationError)
        async def _error_procesar_peticion(request:Request, exc:RequestValidationError):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            errores = exc.errors()
            detalles = []
            for error in errores:
                detalles.append({
                    'tipo': error['type'],
                    'error': error['msg'],
                    'origen': error['loc'],
                    'valor': error['input']
                })
            salida = ModeloRespuesta(
                codigo=_C.ESTADO._422_NO_PROCESABLE,
                tipo=_C.SALIDA.ALERTA,
                mensaje='Los-datos-recibidos-no-se-procesaron',
                detalles=detalles,
                T=traductor
            ).diccionario()
            return JSONResponse(
                status_code=_C.ESTADO._422_NO_PROCESABLE,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(HTTPException)
        async def _error_http(request:Request, exc:HTTPException):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            salida = ModeloRespuesta(
                codigo=exc.status_code,
                tipo=_F.tipo_salida(exc.status_code),
                mensaje=exc.detail,
                T=traductor
            ).diccionario()
            if exc.status_code >= 500:
                _RegistradorLogs.crear(archivo_logs, 'ERROR', f'{dir_logs}/{archivo_logs}.log').error(
                    f'{mi._obtener_url(request)} | {salida.__str__()}'
                )
            return JSONResponse(
                status_code=exc.status_code,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(Exception)
        async def _error_nomanejado(request:Request, exc:Exception):
            import sys
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            descripcion = f'<{exception_name}: {exception_value}>'
            salida = ModeloRespuesta(
                codigo=_C.ESTADO._500_ERROR,
                tipo=_C.SALIDA.ERROR,
                mensaje='Error-no-manejado',
                descripcion=descripcion,
                T=traductor
            ).diccionario()
            registrador = _RegistradorLogs.crear(archivo_logs, 'ERROR', f'{dir_logs}/{archivo_logs}.log')
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                registrador.error(exc, exc_info=True)
            else:
                registrador.error(f'{mi._obtener_url(request)} | {descripcion}')
            return JSONResponse(
                status_code=_C.ESTADO._500_ERROR,
                content=jsonable_encoder(salida)
            )


# --------------------------------------------------
# Clase: ComunicadorWeb
# --------------------------------------------------
class ComunicadorWeb(_Comunicador):

    # --------------------------------------------------
    # Métodos privados

    async def _recibir_peticion(mi, request:Request) -> dict:
        peticion = {}
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
        return peticion

    # --------------------------------------------------
    # Métodos públicos

    async def procesar_peticion(mi, request:Request, idiomas_aceptados:str, sesion:dict=None):
        super().procesar_peticion(idiomas_aceptados, sesion)
        from urllib.parse import urlparse
        url_analizada = urlparse(str(request.url))
        raiz_api = mi.config_web.get('raiz_api')
        dir_frontend = mi.config_web.get('frontend')
        servidor = f'{url_analizada.scheme}://{url_analizada.netloc}'
        partes = url_analizada.path.lstrip('/').split('/')
        raiz_api = '/' + partes[0] if len(partes) > 0 else ''
        aplicacion = '/' + partes[1] if len(partes) > 1 else ''
        recurso = '/' + '/'.join(partes[2:]) if len(partes) > 2 else '/'
        mi.contexto['url'] = {
            'servidor': servidor,
            'absoluta': f'{servidor}{url_analizada.path}',
            'relativa': url_analizada.path,
            'puntoentrada': f'{servidor}{raiz_api}',
            'puntofinal': f'{aplicacion}{recurso}',
            'app': f'{raiz_api}{aplicacion}',
            'recurso': recurso,
            'frontend': f'{raiz_api}/{dir_frontend}',
        }
        mi.contexto['web']['api_marco'] = 'FastAPI'
        mi.contexto['web']['dominio'] = url_analizada.hostname
        mi.contexto['web']['acepta'] = request.headers.get('accept', '')
        mi.contexto['peticion'] = await mi._recibir_peticion(request)


# --------------------------------------------------
# Clase: AutenticadorWeb
# --------------------------------------------------
class AutenticadorWeb(_Autenticador):

    # --------------------------------------------------
    # Métodos públicos

    async def validar_apikey(mi, request:Request) -> str:
        if 'Authorization' in request.headers:
            api_key_header = request.headers.get('Authorization').replace('Bearer ', '')
            if mi.api_keys and api_key_header and api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
        mensaje = 'API-key-invalida'
        raise _ErrorAutenticacion(
            mensaje=mensaje,
            codigo=_C.ESTADO._403_NO_AUTORIZADO,
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
        raise _ErrorAutenticacion(
            mensaje=mensaje,
            codigo=_C.ESTADO._401_NO_AUTENTICADO,
            url_login=mi.url_login
        )

    async def validar_todo(mi, request:Request):
        await mi.validar_apikey(request)
        await mi.validar_token(request)


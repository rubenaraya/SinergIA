# --------------------------------------------------
# backend\documentos\web_flask.py
# --------------------------------------------------

# Importaciones de Flask
from flask import (
    Blueprint,
    request,
    redirect,
    jsonify
)
from flask_pydantic import validate

# Importaciones de PySinergIA
from pysinergia import (
    Constantes as C,
)
from pysinergia.web import (
    configurar_microservicio,
)
from pysinergia.web.flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

# Importaciones del Microservicio personalizado
from .dominio import (
    PeticionBuscarDocumentos,
    PeticionVerDocumento,
    PeticionAgregarDocumento,
)
from .adaptadores import (
    ConfigDocumentos,
    ControladorDocumentos,
)

# --------------------------------------------------
# Configuración del Microservicio personalizado
aplicacion = 'sinergia'
configuracion = configurar_microservicio(ConfigDocumentos, __file__, aplicacion, None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = Blueprint(
    url_prefix=f'{configuracion.PREFIJO_MICROSERVICIO}',
    name=configuracion.MICROSERVICIO,
    import_name=__name__
)

# --------------------------------------------------
# Rutas del Microservicio personalizado

@enrutador.route('/', methods=['GET'])
def get_inicio():
    return redirect(f'/{configuracion.APP_GLOBAL}/{configuracion.ALIAS_FRONTEND}/{configuracion.APLICACION}/index.html')

@enrutador.route('/documentos', methods=['GET'])
#@autenticador.validar_token
#@autenticador.validar_apikey
@validate()
def buscar_documentos(query:PeticionBuscarDocumentos):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = ControladorDocumentos(configuracion, comunicador).buscar_documentos(query, conversion=C.CONVERSION.JSON)
    return jsonify(respuesta)

@enrutador.route('/documentos/<id>', methods=['GET'])
@validate()
def ver_documento(id):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = PeticionVerDocumento(id=id)
    respuesta = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    return jsonify(respuesta)

@enrutador.route('/documentos', methods=['POST'])
@validate()
def agregar_documento(body:PeticionAgregarDocumento):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = ControladorDocumentos(configuracion, comunicador).agregar_documento(body)
    return jsonify(respuesta), C.ESTADO._201_CREADO


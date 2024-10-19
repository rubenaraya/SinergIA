# --------------------------------------------------
# backend\documentos\web_flask.py
# --------------------------------------------------

# Importaciones de Flask
from flask import (
    Blueprint,
    jsonify,
    make_response,
    request,
    Response,
)
from flask_pydantic import validate

# Importaciones de PySinergIA
from pysinergia.config import *
from pysinergia.globales import Constantes
from pysinergia.interfaces.flask import *

# Importaciones del Microservicio
from .interacciones import ControladorDocumentos
from .modelos import (
    ValidadorBuscarDocumentos,
    ValidadorConsultarDocumento,
    ValidadorAgregarDocumento,
    ValidadorActualizarDocumento,
    FormActualizarDocumento,
)

# --------------------------------------------------
# Configuración del Microservicio
app_pwa = 'sinergia'
microservicio = 'documentos'
configuracion = configurar_microservicio(Configuracion, __file__, app_pwa, None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = Blueprint(
    url_prefix=f'{configuracion.PREFIJO_MICROSERVICIO}',
    name=configuracion.MICROSERVICIO,
    import_name=__name__
)

# --------------------------------------------------
# Rutas del Microservicio

#@autenticador.validar_token
#@autenticador.validar_apikey

@enrutador.route(f'/{microservicio}', methods=['GET'])
@validate()
def buscar_documentos(query:ValidadorBuscarDocumentos):
    comunicador.procesar_solicitud()
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).buscar_documentos(query)
    return make_response(jsonify(respuesta), codigo)

@enrutador.route(f'/{microservicio}', methods=['POST'])
@validate()
def agregar_documento(body:ValidadorAgregarDocumento):
    comunicador.procesar_solicitud()
    # body = ValidadorAgregarDocumento.model_validate_json(request.data) #request.get_json(silent=True)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).agregar_documento(body)
    return make_response(jsonify(respuesta), codigo)

@enrutador.route(f'/{microservicio}/<uid>', methods=['GET'])
def ver_documento(uid:str):
    comunicador.procesar_solicitud()
    peticion = ValidadorConsultarDocumento(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    return make_response(jsonify(respuesta), codigo)

@enrutador.route(f'/{microservicio}/<uid>', methods=['PUT'])
@validate()
def actualizar_documento(body:ValidadorActualizarDocumento, uid:str):
    comunicador.procesar_solicitud()
    # body = ValidadorActualizarDocumento.model_validate_json(request.data) #request.get_json(silent=True)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).actualizar_documento(body)
    return make_response(jsonify(respuesta), codigo)

@enrutador.route(f'/{microservicio}/<uid>', methods=['DELETE'])
def eliminar_documento(uid:str):
    comunicador.procesar_solicitud()
    peticion = ValidadorConsultarDocumento(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).eliminar_documento(peticion)
    return make_response(jsonify(respuesta), codigo)

# TODO: Pendiente
@enrutador.route(f'/{microservicio}/exportar/<conversion>', methods=['GET'])
@validate()
def exportar_documentos(query:ValidadorBuscarDocumentos):
    comunicador.procesar_solicitud()

# --------------------------------------------------
# Rutas de ejemplo y pruebas

@enrutador.route(f'/{microservicio}/crear', methods=['GET'])
def crear_tabla():
    comunicador.procesar_solicitud()
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).crear_tabla()
    return make_response(jsonify(respuesta), codigo)

@enrutador.route(f'/{microservicio}/form', methods=['GET'])
def form():
    comunicador.procesar_solicitud()
    formulario = FormActualizarDocumento(
        dto_contexto=comunicador.contexto,
        T=comunicador.traductor,
        #estado='Activo',
    )
    respuesta = comunicador.transformar_contenido(
        comunicador.agregar_contexto({'formulario': formulario.generar()}),
        plantilla='form_pagina.html',
    )
    return Response(respuesta, Constantes.ESTADO._200_EXITO, mimetype=Constantes.MIME.HTML)


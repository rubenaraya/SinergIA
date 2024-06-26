# backend\participantes\web_flask.py

from pysinergia.base import (
    configurar_microservicio,
    C,
    ImagenCargada,
    DocumentoCargado,
    AudioCargado,
    Respuesta,
    Repositorio,
)
from pysinergia.base.flask import *

# --------------------------------------------------
# Importaciones del Microservicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    PeticionAgregarParticipante,
    ProcedimientoActualizarParticipante,
    ProcedimientoAgregarParticipante,
    ProcedimientoEliminarParticipante,
    ProcedimientoBuscarParticipantes,
    FormActualizarParticipante,
    FormLogin,
)
from .adaptadores import (
    ControladorParticipantes as Controlador,
    ConfigParticipantes,
)

# --------------------------------------------------
# Configuración del Microservicio personalizado
configuracion = configurar_microservicio(ConfigParticipantes, __file__, 'prueba', None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = Blueprint(
    url_prefix=f'{configuracion.PREFIJO_MICROSERVICIO}',
    name=configuracion.MICROSERVICIO,
    import_name=__name__
)

# --------------------------------------------------
# Rutas del Microservicio personalizado
# --------------------------------------------------

@enrutador.route('/', methods=['GET'])
def get_inicio():
    return redirect(f'/{configuracion.APP_GLOBAL}/{configuracion.ALIAS_FRONTEND}/{configuracion.APLICACION}/index.html')

@enrutador.route('/participantes', methods=['GET'])
#@autenticador.validar_token
@validate()
def buscar_participantes(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, conversion=C.CONVERSION.JSON)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/participantes/<id>', methods=['GET'])
@validate()
def ver_participante(id):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(configuracion, comunicador).ver_participante(peticion)
    return jsonify(respuesta)

@enrutador.route('/participantes', methods=['POST'])
def agregar_participante(body:PeticionAgregarParticipante):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = Controlador(configuracion, comunicador).agregar_participante(body)
    return jsonify(respuesta), C.ESTADO._201_CREADO

@enrutador.route('/participantes/<id>', methods=['PUT'])
def actualizar_participante(id, body:FormActualizarParticipante):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    body.id = id
    respuesta = Controlador(configuracion, comunicador).actualizar_participante(body)
    return jsonify(respuesta), C.ESTADO._204_VACIO

@enrutador.route('/participantes/<int>', methods=['DELETE'])
def eliminar_participante(id):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(configuracion, comunicador).eliminar_participante(peticion)
    return jsonify(respuesta), C.ESTADO._204_VACIO


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.route('/login', methods=['GET'])
def get_login():
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    formulario = FormLogin(dto_contexto=comunicador.transferir_contexto(), T=comunicador.traspasar_traductor())
    respuesta = comunicador.transformar_contenido(
        comunicador.transferir_contexto({'formulario': formulario.generar()}),
        plantilla='form_login.html',
    )
    return Response(respuesta, C.ESTADO._200_EXITO, mimetype=C.MIME.HTML)

@enrutador.route('/login', methods=['POST'])
def post_login():
    respuesta = 'LOGIN'
    return respuesta

@enrutador.route('/token/<email>', methods=['GET'])
def token(email:str):
    autenticador.firmar_token(email)
    return Response(autenticador.token, C.ESTADO._200_EXITO, mimetype=C.MIME.TXT)

@enrutador.route('/pdf', methods=['GET'])
@validate()
def pdf(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.CONVERSION.PDF)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/docx', methods=['GET'])
@validate()
def docx(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.CONVERSION.WORD)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/xlsx', methods=['GET'])
@validate()
def xlsx(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.CONVERSION.EXCEL)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/csv', methods=['GET'])
@validate()
def csv(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.CONVERSION.CSV)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/html', methods=['GET'])
@validate()
def html(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.CONVERSION.HTML)
    return Response(response=contenido, headers=encabezados)

# --------------------------------------------------

@enrutador.route('/cargar/<tipo>', methods=['GET'])
def get_cargar(tipo):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)

    modelos = {"imagen": ImagenCargada, "documento": DocumentoCargado, "audio": AudioCargado}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        respuesta = Respuesta(
            codigo=codigo,
            conclusion=C.CONCLUSION.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).json()
        return respuesta, codigo

    return comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='cargar.html',
        ruta_plantillas=f'{configuracion.RUTA_MICROSERVICIO}/plantillas'
    )

@enrutador.route('/cargar/<tipo>', methods=['POST'])
def post_cargar(tipo):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)

    modelos = {"imagen": ImagenCargada, "documento": DocumentoCargado, "audio": AudioCargado}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        contenido = Respuesta(
            codigo=codigo,
            conclusion=C.CONCLUSION.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
    elif 'carga' not in request.files:
        codigo = C.ESTADO._422_NO_PROCESABLE
        contenido = Respuesta(
            codigo=codigo,
            conclusion=C.CONCLUSION.ALERTA,
            mensaje='No-se-recibio-ninguna-carga',
            T=comunicador.traspasar_traductor()
        ).diccionario()
    else:
        contenido = Controlador(configuracion, comunicador).cargar_archivo(portador_archivo(origen=request.files['carga']))
        codigo = contenido.get('codigo', C.ESTADO._200_EXITO)
    return jsonify(contenido), codigo

@enrutador.route('/manifest.json', methods=['GET'])
def manifest():
    idioma = request.headers.get('Accept-Language')
    comunicador.procesar_peticion(idioma)
    respuesta = comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='manifest.json',
    )
    return Response(respuesta, C.ESTADO._200_EXITO, mimetype=C.MIME.MANIFEST)

@enrutador.route('/zip', methods=['GET'])
def zip():
    idioma = request.headers.get('Accept-Language')
    comunicador.procesar_peticion(idioma)
    respuesta = 'Zip OK'
    zip = comunicador.disco.empaquetar_zip(
        dir_origen='documentos',
        ruta_archivo_zip='repositorios_prueba.zip'
    )
    if zip:
        comunicador.disco.extraer_zip(
            ruta_archivo_zip='repositorios_prueba.zip',
            dir_destino='zip'
        )
    return Response(respuesta, C.ESTADO._200_EXITO)

@enrutador.route('/img', methods=['GET'])
def img():
    idioma = request.headers.get('Accept-Language')
    comunicador.procesar_peticion(idioma)
    salidas = [
        {"ancho": 32, "alto": 32, "formato": "ICO", "nombre": "favicon-32x32.ico"},
        {"ancho": 64, "alto": 64, "formato": "ICO", "nombre": "favicon.ico"},
        {"ancho": 128, "alto": 128, "formato": "PNG", "nombre": "icon-128x128.png"},
        {"ancho": 256, "alto": 256, "formato": "JPEG", "nombre": "icon-256x256.jpg"},
    ]
    img = comunicador.disco.convertir_imagen(
        ruta_imagen='imagenes/logo.png',
        dir_destino='documentos/img',
        lista_salidas=salidas
    )
    return jsonify(img)

@enrutador.route('/audio', methods=['GET'])
def audio():
    from pysinergia.complementos.convertidor_audio import ConvertidorAudio
    idioma = request.headers.get('Accept-Language')
    comunicador.procesar_peticion(idioma)
    convertidor = ConvertidorAudio(configuracion.DISCO_RUTA)
    respuesta = convertidor.convertir(ruta_audio='audios/prueba1.opus', dir_destino='audios/convertidos')
    return jsonify(respuesta)

@enrutador.route('/sql', methods=['GET'])
def sql():
    # Enrutador
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = FormActualizarParticipante(
        id=1,
        nombre='Rubén Araya Tagle',
        email='raraya@masexperto.com',
        estado='Activo',
    )
    
    # Controlador (adaptador-api)
    peticion.agregar_contexto(comunicador.transferir_contexto())
    solicitud = peticion.serializar()

    # CasosDeUso (omitido)

    # Repositorio (adaptador-spi)
    procedimiento = ProcedimientoActualizarParticipante(
        dto_solicitud_datos=solicitud,
        dto_roles_sesion=sesion.get('roles'),
    ).serializar()
    repo = Repositorio(configuracion)
    repo.basedatos.conectar(configuracion.basedatos())
    instruccion, parametros = repo.basedatos.generar_comando(
        plantilla=repo.basedatos.INSTRUCCION.UPDATE_POR_ID,
        procedimiento=procedimiento
    )
    repo.basedatos.desconectar()
    resultado = {'instruccion': instruccion, 'parametros': parametros, 'procedimiento': procedimiento}

    # Controlador (adaptador-api)
    respuesta = Respuesta(
        T=comunicador.traspasar_traductor(),
        resultado=resultado
    ).diccionario()

    # Enrutador
    return jsonify(respuesta)

@enrutador.route('/form', methods=['GET'])
def form():
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    formulario = FormActualizarParticipante(
        dto_contexto=comunicador.transferir_contexto(),
        dto_roles_sesion=sesion.get('roles'),
        T=comunicador.traspasar_traductor(),
        #nombre='Rubén Araya',
        #email='raraya@masexperto.com',
        #estado='Activo',
    )
    respuesta = comunicador.transformar_contenido(
        comunicador.transferir_contexto({'formulario': formulario.generar()}),
        plantilla='form_pagina.html',
    )
    return Response(respuesta, C.ESTADO._200_EXITO, mimetype=C.MIME.HTML)

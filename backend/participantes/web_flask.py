# backend\participantes\web_flask.py

from pysinergia._dependencias.web_flask import *

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)
from .adaptadores import (
    ControladorParticipantes as Controlador,
    ConfigParticipantes as ConfigServicio,
)

# --------------------------------------------------
# Configuración del Servicio personalizado
aplicacion = 'prueba'
configuracion = cargar_configuracion(ConfigServicio, __name__, aplicacion, None)
comunicador = ComunicadorWeb(
    configuracion.web(),
    configuracion.disco(),
    Traductor(configuracion.traductor())
)
autenticador = AutenticadorWeb(
    configuracion.autenticacion(),
    url_login=f'/{configuracion.app_web}/{aplicacion}/login'
)
enrutador = Blueprint(
    name=configuracion.servicio,
    import_name=__name__,
    url_prefix=f'{configuracion.raiz_api}/{aplicacion}'
)

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.route('/', methods=['GET'])
def get_inicio():
    return redirect(f'/{configuracion.app_web}/{configuracion.frontend}/{aplicacion}/index.html')

@enrutador.route('/participantes', methods=['GET'])
#@autenticador.validar_token
@validate()
def buscar_participantes(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, formato=C.FORMATO.JSON)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/participantes/<id>', methods=['GET'])
@validate()
def ver_participante(id):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(configuracion, comunicador).ver_participante(peticion)
    return Response(Json.codificar(respuesta), C.ESTADO._200_EXITO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes', methods=['POST'])
def agregar_participante(body:ModeloNuevoParticipante):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = Controlador(configuracion, comunicador).agregar_participante(body)
    return Response(Json.codificar(respuesta), C.ESTADO._201_CREADO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes/<id>', methods=['PUT'])
def actualizar_participante(id, body:ModeloEditarParticipante):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    body.id = id
    respuesta = Controlador(configuracion, comunicador).actualizar_participante(body)
    return Response(Json.codificar(respuesta), C.ESTADO._204_VACIO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes/<int>', methods=['DELETE'])
def eliminar_participante(id):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(configuracion, comunicador).eliminar_participante(peticion)
    return Response(Json.codificar(respuesta), C.ESTADO._204_VACIO, mimetype=C.MIME.JSON)


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.route('/login', methods=['GET'])
def get_login():
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='login.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )
    return Response(respuesta, C.ESTADO._200_EXITO, mimetype=C.MIME.HTML)

@enrutador.route('/login', methods=['POST'])
def post_login():
    ...

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
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.FORMATO.PDF)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/docx', methods=['GET'])
@validate()
def docx(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.FORMATO.WORD)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/xlsx', methods=['GET'])
@validate()
def xlsx(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.FORMATO.EXCEL)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/csv', methods=['GET'])
@validate()
def csv(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.FORMATO.CSV)
    return Response(response=contenido, headers=encabezados)

@enrutador.route('/html', methods=['GET'])
@validate()
def html(query:PeticionBuscarParticipantes):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(query, C.FORMATO.HTML)
    return Response(response=contenido, headers=encabezados)

# --------------------------------------------------

@enrutador.route('/cargar/<tipo>', methods=['GET'])
def get_cargar(tipo):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)

    modelos = {"imagen": CargaImagen, "documento": CargaDocumento, "audio": CargaAudio}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        salida = ModeloRespuesta(
            codigo=codigo,
            tipo=C.SALIDA.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
        return Response(response=Json.codificar(salida), status=codigo, mimetype=C.MIME.JSON)

    return comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='cargar.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )

@enrutador.route('/cargar/<tipo>', methods=['POST'])
def post_cargar(tipo):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)

    modelos = {"imagen": CargaImagen, "documento": CargaDocumento, "audio": CargaAudio}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        contenido = ModeloRespuesta(
            codigo=codigo,
            tipo=C.SALIDA.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
    elif 'carga' not in request.files:
        codigo = C.ESTADO._422_NO_PROCESABLE
        contenido = ModeloRespuesta(
            codigo=codigo,
            tipo=C.SALIDA.ALERTA,
            mensaje='No-se-recibio-ninguna-carga',
            T=comunicador.traspasar_traductor()
        ).diccionario()
    else:
        contenido = Controlador(configuracion, comunicador).cargar_archivo(portador_archivo(origen=request.files['carga']))
        codigo = contenido.get('codigo', C.ESTADO._200_EXITO)
    return Response(response=Json.codificar(contenido), status=codigo, mimetype=C.MIME.JSON)

@enrutador.route('/manifest.json', methods=['GET'])
def manifest():
    idioma = request.headers.get('Accept-Language')
    comunicador.procesar_peticion(idioma)
    datos = {
        'name': 'Aplicación Web SinergIA',
        'short_name': 'App SinergIA',
        'id': 'App-prueba',
        'description': ''
    }
    respuesta = comunicador.transformar_contenido(
        comunicador.transferir_contexto(datos),
        plantilla='manifest.json',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
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
        ruta_imagen='imagenes/avatar-rat.jpg',
        dir_destino='documentos/img',
        lista_salidas=salidas
    )
    return Json.codificar(img)

@enrutador.route('/audio', methods=['GET'])
def audio():
    from pysinergia.exportadores.convertidor_audio import ConvertidorAudio
    idioma = request.headers.get('Accept-Language')
    comunicador.procesar_peticion(idioma)
    convertidor = ConvertidorAudio(configuracion.disco_ruta)
    respuesta = convertidor.convertir(ruta_audio='audios/prueba1.opus', dir_destino='audios/convertidos')
    return respuesta


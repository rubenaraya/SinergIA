# pysinergia\web.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Funciones as _F,
)

# --------------------------------------------------
# Clase: Comunicador
# --------------------------------------------------
class Comunicador:
    def __init__(mi, config:dict):
        mi.config:dict = config
        mi.idioma = None
        mi.traductor = None

    # --------------------------------------------------
    # Métodos públicos

    def asignar_idioma(mi, idiomas_aceptados:str):
        import gettext
        mi.idioma = _F.negociar_idioma(idiomas_aceptados, mi.config.get('idiomas'))
        mi.traductor = gettext.translation(
            domain=mi.config.get('traduccion'),
            localedir=mi.config.get('dir_locales'),
            languages=[mi.idioma],
            fallback=False,
        )

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='./') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        import os
        resultado = ''
        if os.path.exists(f'{directorio}/{plantilla}'):
            cargador = FileSystemLoader(directorio)
            entorno = Environment(loader=cargador)
            entorno.add_extension('jinja2.ext.i18n')
            if mi.traductor:
                entorno.install_gettext_translations(mi.traductor, newstyle=True)
            template = entorno.get_template(plantilla)
            resultado = template.render(info)
        return resultado

    def exportar_info(mi, formato:str, info:dict={}, plantilla:str='', opciones:dict={}):
        import importlib
        from pysinergia.adaptadores import I_Exportador
        opciones['idioma'] = mi.idioma
        contenido = mi.transformar_contenido(info=info, plantilla=plantilla)
        modulo = f'pysinergia.exportadores.exportador_{str(formato).lower()}'
        clase = f'Exportador{str(formato).capitalize()}'
        componente = getattr(importlib.import_module(modulo), clase)
        exportador:I_Exportador = componente(mi.config)
        return exportador.generar(contenido=contenido, opciones=opciones)


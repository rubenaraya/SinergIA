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


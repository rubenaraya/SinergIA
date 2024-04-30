# backend\prueba\participantes\adaptadores.py

from typing import Dict

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia import (
    Controlador,
    Operador,
)

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .servicio import (
    ACCION,
    ServicioParticipantes, 
    I_OperadorParticipantes
)
from .dominio import ModeloPeticion

# --------------------------------------------------
# Clase: ControladorParticipantes
# --------------------------------------------------
"""
Falta autorizar_acceso según roles
Falta manejar errores de la aplicación
Falta entregar un código interno del resultado ¿y un mensaje? ¿y un tipo?
Faltaría crear un formato de Vista? (ViewModel)
Falta indicar que_hacer al entregar respuesta (enviar, descargar, redirigir)
"""
class ControladorParticipantes(Controlador):

    # --------------------------------------------------
    # Métodos públicos (usados en la capa web)

    def buscar_participantes(mi, peticion:ModeloPeticion):
        """
        autorizar_acceso(permisos='?', credenciales='?')

        """
        # resultado = ServicioParticipantes(OperadorParticipantes(mi.config)).solicitar_accion(ACCION.BUSCAR_PARTICIPANTES, peticion)
        servicio = ServicioParticipantes(operador=OperadorParticipantes(mi.config))
        resultado = servicio.solicitar_accion(ACCION.BUSCAR_PARTICIPANTES, peticion)

        return mi.emisor.entregar_respuesta(resultado)
    
    def agregar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config)).solicitar_accion(
            ACCION.AGREGAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def ver_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config)).solicitar_accion(
            ACCION.VER_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def actualizar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config)).solicitar_accion(
            ACCION.ACTUALIZAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)

    def eliminar_participante(mi, peticion:ModeloPeticion):
        resultado = ServicioParticipantes(OperadorParticipantes(mi.config)).solicitar_accion(
            ACCION.ELIMINAR_PARTICIPANTE, peticion)
        return mi.emisor.entregar_respuesta(resultado)


# --------------------------------------------------
# Clase: OperadorParticipantes
# --------------------------------------------------
"""
Falta crear generar_instruccion y generar_consulta en I_ConectorBasedatos y BasedatosSqlite) -> Debería usar Entidad
Falta probar Modelos para insertar y actualizar participantes
Falta reemplazar "sql" por "instruccion" para hacerlo genérico
"""
class OperadorParticipantes(Operador, I_OperadorParticipantes):

    # --------------------------------------------------
    # Métodos públicos (usados en la capa de servicio)

    def recuperar_lista_participantes_todos(mi) -> Dict:
        mi.basedatos.conectar(mi.config.basedatos())

        sql = "SELECT * FROM participantes WHERE 1 ORDER BY id DESC"

        datos, total = mi.basedatos.obtener(sql=sql, parametros=[])
        mi.basedatos.desconectar()
        return dict(datos)

    def recuperar_lista_participantes_filtrados(mi) -> Dict:
        ...

    def recuperar_participante_por_id(mi) -> Dict:
        ...

    def insertar_nuevo_participante(mi) -> Dict:
        ...

    def actualizar_participante_por_id(mi) -> Dict:
        ...

    def eliminar_participante_por_id(mi) -> Dict:
        ...


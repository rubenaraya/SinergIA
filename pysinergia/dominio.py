# pysinergia\dominio.py

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from pydantic import BaseModel


# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad:
    ...


# --------------------------------------------------
# ClaseModelo: ModeloPeticion
# --------------------------------------------------
class ModeloPeticion(BaseModel):

    def diccionario(mi):
        return mi.model_dump()

    def json(mi):
        return mi.model_dump_json()


# --------------------------------------------------
# ClaseModelo: ModeloRespuesta
# --------------------------------------------------
class ModeloRespuesta(BaseModel):

    def diccionario(mi) -> dict:
        return mi.model_dump()

    def json(mi) -> str:
        return mi.model_dump_json()


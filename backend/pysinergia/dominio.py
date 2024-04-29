# backend\pysinergia\dominio.py

from pydantic import BaseModel

# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad():
    def __init__(mi):
        ...

class ModeloPeticion(BaseModel):
    def diccionario(mi):
        return mi.model_dump()
    def json(mi):
        return mi.model_dump_json()

class ModeloRespuesta(BaseModel):
    def diccionario(mi):
        return mi.model_dump()
    def json(mi):
        return mi.model_dump_json()

# backend\pysinergia\dominio.py

from pydantic import BaseModel

# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad():
        ...

# --------------------------------------------------
# Clase: ModeloPeticion
# --------------------------------------------------
class ModeloPeticion(BaseModel):
    def diccionario(mi):
        return mi.model_dump()
    def json(mi):
        return mi.model_dump_json()

# --------------------------------------------------
# Clase: ModeloRespuesta
# --------------------------------------------------
class ModeloRespuesta(BaseModel):
    def diccionario(mi):
        return mi.model_dump()
    def json(mi):
        return mi.model_dump_json()

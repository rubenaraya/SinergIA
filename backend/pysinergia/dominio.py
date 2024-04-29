# backend\pysinergia\dominio.py

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from pydantic import BaseModel
from dataclasses import (dataclass, asdict)

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia.globales import (
    UUID,
    Constantes
)

# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad():
    ...

# --------------------------------------------------
# ClaseDatos: Caso
# --------------------------------------------------
@dataclass
class Caso:
    uid: UUID

    @classmethod
    def importar(cls, datos):
        return cls(**datos)

    def exportar(mi):
        return asdict(mi)

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
    def diccionario(mi):
        return mi.model_dump()
    def json(mi):
        return mi.model_dump_json()

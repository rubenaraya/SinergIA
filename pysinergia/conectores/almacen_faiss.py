# pysinergia\conectores\almacen_faiss.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.conectores.almacen import (
    Almacen,
    ErrorAlmacen,
)

# --------------------------------------------------
# Clase: AlmacenFaiss
# --------------------------------------------------
class AlmacenFaiss(Almacen):
    def __init__(mi):
        super().__init__()

    def conectar(mi, config:dict) -> bool:
        return True


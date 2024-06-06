# pysinergia\conectores\almacen_chroma.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.conectores.almacen import (
    Almacen as _Almacen,
    ErrorAlmacen as _ErrorAlmacen,
)

# --------------------------------------------------
# Clase: AlmacenChroma
# --------------------------------------------------
class AlmacenChroma(_Almacen):
    def __init__(mi):
        super().__init__()

    def conectar(mi, config:dict) -> bool:
        return True


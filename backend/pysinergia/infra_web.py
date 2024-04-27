from fastapi import FastAPI
from backend.pysinergia.adaptadores import I_Emisor, I_Exportador

class Aplicacion():
    def __init__(mi):
        ...

class Emisor(I_Emisor):
    def __init__(mi):
        ...
    def entregar_respuesta(mi, resultado:str):
        return resultado

# --------------------------------------------------
# Colección de Exportadores
# --------------------------------------------------

class ExportadorExcel(I_Exportador):
    ...

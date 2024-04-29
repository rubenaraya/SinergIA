# backend\pysinergia\globales.py

import uuid

UUID = uuid.UUID

class Constantes:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    RUTA_CONECTORES = 'backend.pysinergia.conectores'
    LIB_SQLITE_REGEXP = './_lib/sqlean/regexp'

    class MODO:
        PRODUCCION = 'PRODUCCION'
        DESARROLLO = 'DESARROLLO'
        PRUEBAS = 'PRUEBAS'
        LOCAL = 'LOCAL'

    class CONECTOR:
        AlmacenChroma = 'AlmacenChroma'
        AlmacenFaiss = 'AlmacenFaiss'
        BasedatosMysql = 'BasedatosMysql'
        BasedatosSqlite = 'BasedatosSqlite'
        DiscoLocal = 'DiscoLocal'
        LlmOpenai = 'LlmOpenai'

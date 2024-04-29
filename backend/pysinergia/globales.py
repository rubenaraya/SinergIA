# backend\pysinergia\globales.py

class Constantes:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

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

# backend\pysinergia\conectores\__init__.py

# --------------------------------------------------
# Conectores para PySinergIA
# --------------------------------------------------

from backend.pysinergia.conectores.almacen_chroma import AlmacenChroma
from backend.pysinergia.conectores.almacen_faiss import AlmacenFaiss
from backend.pysinergia.conectores.basedatos_mysql import BasedatosMysql
from backend.pysinergia.conectores.basedatos_sqlite import BasedatosSqlite
from backend.pysinergia.conectores.disco_local import DiscoLocal
from backend.pysinergia.conectores.llm_openai import LlmOpenai
from backend.pysinergia.interfaces import ( I_ConectorAlmacen, I_ConectorBasedatos, I_ConectorDisco, I_ConectorLlm, I_ConectorSpi )

__all__ = [
    'I_ConectorAlmacen', 'I_ConectorBasedatos', 'I_ConectorDisco', 'I_ConectorLlm', 'I_ConectorSpi', 'I_Exportador',
    'AlmacenChroma', 'AlmacenFaiss', 'BasedatosMysql', 'BasedatosSqlite', 'DiscoLocal', 'LlmOpenai'
]

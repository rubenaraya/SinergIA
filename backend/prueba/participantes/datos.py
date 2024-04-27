from backend.pysinergia import (Operador, I_ConectorBasedatos)

class OperadorParticipantes(Operador):
    def __init__(mi):
        # inyectar
        from backend.pysinergia.conectores.basedatos_sqlite import BasedatosSqlite
        mi.basedatos:I_ConectorBasedatos = BasedatosSqlite()
        mi.basedatos.conectar(config={})
        ...


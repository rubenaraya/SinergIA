from backend.pysinergia.adaptadores import Operador, I_ConectorBasedatos

class OperadorParticipantes(Operador):
    def __init__(mi):
        # inyectar
        from backend.pysinergia.infra_datos import BasedatosSqlite
        mi.basedatos:I_ConectorBasedatos = BasedatosSqlite()
        mi.basedatos.conectar()
        ...


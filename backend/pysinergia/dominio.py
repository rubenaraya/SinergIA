# backend\pysinergia\dominio.py

from enum import Enum

# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad():
    def __init__(mi):
        ...

class Rol(str, Enum):
    Admin = "Admin"
    Usuario = "Usuario"
    Invitado = "Invitado"

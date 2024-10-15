# --------------------------------------------------
# pysinergia\conectores\basedatos_mysql.py
# --------------------------------------------------

from mysql.connector import (
    connect,
    MySQLConnection,
    Error,
)

# Importaciones de PySinergIA
from pysinergia.globales import (ErrorPersonalizado, Constantes)
from pysinergia.conectores.basedatos import Basedatos

# --------------------------------------------------
# Clase: BasedatosMysql
class BasedatosMysql(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.conexion:MySQLConnection = None
        mi.marca_param = '%s'
        mi.tipos = {
            'str': 'VARCHAR',
            'int': 'INT',
            'float': 'DOUBLE',
            'bool': 'BOOLEAN',
            'date': 'DATE',
            'datetime': 'DATETIME',
        }

    def _obtener_datos(mi, cursor) -> tuple:
        cursor = mi.conexion.cursor(dictionary=True)
        lista = [dict(fila) for fila in cursor.fetchall()]
        columnas = cursor.column_names
        return lista, columnas

    def conectar(mi, config:dict) -> bool:
        try:
            if mi.conexion and mi.basedatos == config.get('nombre'):
                return True
            if mi.conexion:
                mi.conexion.close()
            mi.basedatos = config.get('nombre')
            if mi.basedatos:
                mi.conexion = connect(
                    user=config.get('usuario'),
                    password=config.get('password'),
                    host=config.get('ruta'),
                    database=mi.basedatos
                )
                return mi.conexion.is_connected()
        except Error as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )
        return False

    def crear_tabla(mi, nombre:str, constructor:dict={}):
        try:
            columnas = ['id INT NOT NULL AUTO_INCREMENT PRIMARY KEY']
            sql_create_index = []
            for campo, detalles in constructor.items():
                tipo = detalles.get('tipo', 'str')
                largo = detalles.get('largo')
                default = detalles.get('default')
                indice = detalles.get('indice', '')
                if tipo == 'str':
                    if largo and largo > 255:
                        tipo_sql = 'LONGTEXT CHARACTER SET utf8'
                    elif largo:
                        tipo_sql = f"VARCHAR({largo}) CHARACTER SET utf8"
                    else:
                        tipo_sql = 'VARCHAR(255) CHARACTER SET utf8'
                elif tipo == 'int':
                    tipo_sql = f"INT({largo})" if largo else 'INT'
                else:
                    tipo_sql = mi.tipos[tipo]
                if default is None:
                    default_sql = 'DEFAULT NULL'
                else:
                    default_sql = f"DEFAULT '{default}' NOT NULL"
                columna = f"`{campo}` {tipo_sql} {default_sql}"
                columnas.append(columna)
                if indice == 'simple':
                    sql_create_index.append(f"CREATE INDEX IF NOT EXISTS `idx_{nombre}_{campo}` ON `{nombre}` (`{campo}` ASC);")
                elif indice == 'unico':
                    sql_create_index.append(f"CREATE UNIQUE INDEX IF NOT EXISTS `idx_{nombre}_{campo}` ON `{nombre}` (`{campo}` ASC);")
            columnas_sql = ', '.join(columnas)
            sql_create_table = f"CREATE TABLE IF NOT EXISTS `{nombre}` ({columnas_sql}) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            cursor = mi.conexion.cursor()
            cursor.execute(sql_create_table)
            for sql in sql_create_index:
                cursor.execute(sql)
            mi.conexion.commit()
            return {'total': len(sql_create_index) + 1, 'create_table': sql_create_table, 'sql_create_index': sql_create_index}
        except Exception as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )


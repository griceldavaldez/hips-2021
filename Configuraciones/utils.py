import os

#recibe una ruta relativa y devuele la ruta absoluta
def obtenerRutaAbsoluta(ruta_relativa):
    ruta_actual = os.path.dirname(__file__)
    ruta_absoluta = os.path.join(ruta_actual,ruta_relativa)
    return ruta_absoluta

#prueba
print(obtenerRutaAbsoluta("BaseDatos/conexion_postgres.py"))
import os

#recibe una ruta relativa y devuele la ruta absoluta
def obtenerRutaAbsoluta(ruta_relativa):
    ruta_actual = os.path.dirname(__file__)
    ruta_absoluta = os.path.join(ruta_actual,ruta_relativa)
    return ruta_absoluta

#prueba
print(obtenerRutaAbsoluta("BaseDatos/conexion_postgres.py"))

#obtener el usuario permitido para acceder al sistema por la interfaz
def obtenerUsuario(login):
    archivo = open(obtenerRutaAbsoluta("Configuraciones/usuarios_sistema_web.txt"), "r")
    lineas = archivo.readlines()
    usuario
    for i in range(0, len(lineas)):
        lineas[i] = lineas[i].strip('\n') 
        txt= lineas[i].split(";")

    archivo.close()
    return usuario
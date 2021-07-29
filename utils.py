import os
<<<<<<< HEAD:utils.py

from modelos_conf import Usuario

=======
from Configuraciones.modelos2 import Usuario
import datetime

#Retorna hora y fecha actual
def get_fecha():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
>>>>>>> main:Configuraciones/utils.py

#recibe una ruta relativa y devuele la ruta absoluta
def obtenerRutaAbsoluta(ruta_relativa):
    ruta_actual = os.path.dirname(__file__)
    ruta_absoluta = os.path.join(ruta_actual,ruta_relativa)
    return ruta_absoluta

#obtener el usuario permitido para acceder al sistema por la interfaz
def obtenerUsuario(login):
    archivo = open(obtenerRutaAbsoluta("usuarios_sistema_web.txt"), "r")
    lineas = archivo.readlines()
    archivo.close()
    for i in range(0, len(lineas)):
        lineas[i] = lineas[i].strip('\n') 
        txt= lineas[i].split(";")
        loginObtenido = txt[2]
        if(loginObtenido == login):
            usuario = Usuario(txt[0],txt[1],txt[2], txt[3])
            return usuario
    pass

def obtenerUsuarioPorId(id):
    archivo = open(obtenerRutaAbsoluta("usuarios_sistema_web.txt"), "r")
    lineas = archivo.readlines()
    archivo.close()
    for i in range(0, len(lineas)):
        lineas[i] = lineas[i].strip('\n') 
        txt= lineas[i].split(";")
        idObtenido = txt[0]
        if(int(idObtenido) == int(id)):
            usuario = Usuario(txt[0],txt[1],txt[2],txt[3])
            return usuario
    pass

print("hola mundo")
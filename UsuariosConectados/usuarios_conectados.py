import subprocess
from Correo.correo import enviar_correo
from BaseDatos.dao import AlarmaPrevencion, insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from utils import get_fecha

#Funcion: comprobar_usuarios_conectados
#	Obtiene las IP  de las maquinas conectadas al servidor
def comprobar_usuarios_conectados(admin):
    print("Inicia la funcion comprobar_usuarios_conectados() \n", "\t\t Hora: " + get_fecha())
    U_conectados = subprocess.Popen("w -i 2>/dev/null", stdout=subprocess.PIPE, shell=True)
    (output, err) = U_conectados.communicate()
    body = output.decode("utf-8")
    enviar_correo(admin[0], admin[1], 'Usuarios conectados', body)
    print( "\t\t Resultado: "  + "Usuarios conectados: " + body.replace("\n", " "))
    print("\t\t Accion: " + 'Se envio un correo al administrador con la informacion obtenida del escaneo')
    obj_alarm_prev = AlarmaPrevencion(get_fecha(), 'usuarios_conectados', "Usuarios conectados: " + body.replace("\n", " "), 'Se envio un correo al administrador con la informacion obtenida del escaneo')
    insertarAlarmaPrevencion(obj_alarm_prev)

    
import subprocess, os, sys, datetime

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import AlarmaPrevencion, insertarAlarmaPrevencion
from modelos import AlarmaPrevencion


def comprobar_usuarios_conectados(admin):
    U_conectados = subprocess.Popen("w -i 2>/dev/null", stdout=subprocess.PIPE, shell=True)
    (output, err) = U_conectados.communicate()
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    body = output.decode("utf-8")
    enviar_correo(admin[0], admin[1], 'Usuarios conectados', body)
    #print(output.decode("utf-8")+"\n")
    obj_alarm_prev = AlarmaPrevencion()
    obj_alarm_prev.setFechaHora(fecha_hora)
    obj_alarm_prev.setTipoEscaneo('usuarios_conectados')
    obj_alarm_prev.setResultado(body)
    obj_alarm_prev.setAccion('Se envio un correo al administrador con la informacion obtenida del escaneo')
    insertarAlarmaPrevencion(obj_alarm_prev)

    
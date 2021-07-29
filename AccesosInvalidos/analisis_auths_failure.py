import subprocess
from Correo.correo import enviar_correo
from Logs.logs import echo_alarmas_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from utils import get_fecha

#Funcion: analisis_auths_failure
#	Busca Authentication Failures en /var/log/secure. En el caso de encontrarlas, los alerta.
#	Guarda las alertas en el log correspondiente (Ver: echo_alarmas_log)
#	
def analisis_auths_failure(admin):
    print("Inicia la funcion analisis_auths_failure() \n", "\t\t Hora: " + get_fecha())
    p =subprocess.Popen("cat /var/log/secure | grep -i \"authentication failure\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body = ''
    for linea in ret_msg.splitlines():
        echo_alarmas_log(" Authentication failure: " + linea, 'analisis_auths_failure',"")
        print("\t\t Resultado: " + " Authentication failure: " + linea)
        print("\t\t Accion: " + "Se envio un correo al administrador para dar aviso de lo ocurrido")
    body = body + ret_msg
    if body != '':
        enviar_correo(admin[0], admin[1],'Tipo de Alerta : Authentication failure',body)
        obj_alarm_prev = AlarmaPrevencion(get_fecha(), "analisis_auths_failure", "Authentication failure: "+ body.replace("\n", " "),"Se envio un correo al administrador para dar aviso de lo ocurrido")
        insertarAlarmaPrevencion(obj_alarm_prev)
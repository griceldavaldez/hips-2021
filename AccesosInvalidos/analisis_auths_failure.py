import datetime, subprocess, os, sys
sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_alarmas_log

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

#Funcion: analisis_auths_failure
#	Busca Authentication Failures en /var/log/secure. En el caso de encontrarlas, los alerta.
#	Guarda las alertas en el log correspondiente (Ver: echo_alarmas_log)
#	
def analisis_auths_failure(admin):
    p =subprocess.Popen("cat /var/log/secure | grep -i \"authentication failure\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body = ''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for linea in ret_msg.splitlines():
        echo_alarmas_log(fecha_hora, " Authentication failure: " + linea, 'analisis_auths_failure',"")
    body = body + ret_msg
    if body != '':
        enviar_correo(admin[0], admin[1],'Tipo de Alerta : Authentication failure',body)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo("analisis_auths_failure")
        obj_alarm_prev.setResultado("Authentication failure: " + body.replace('\n', " ") )
        obj_alarm_prev.setAccion("Se envio un correo al administrador para dar aviso de lo ocurrido")
        insertarAlarmaPrevencion(obj_alarm_prev)
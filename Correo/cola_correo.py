import datetime, os, sys
import subprocess
sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_prevencion_log, echo_alarmas_log

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

#Funcion: verificar_cola_correo
#	Verifica si la cola de mails supero una cantidad maxima determinada
#Parametros:
#	MAX_Q_COUNT	(int) numero maximo de mails que pueden estar en cola
#   admin (lista) contiene los datos del administrador como el correo y pass
def verificar_cola_correo(MAX_Q_COUNT, admin):
    p = subprocess.Popen("mailq", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mail_list = output.decode("utf-8").splitlines()
    if MAX_Q_COUNT >-1 and len(mail_list) > MAX_Q_COUNT:
        p = subprocess.Popen("service postfix stop", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        info = "Posible ataque DoS/DDoS.La cola de correo alcanzo el limite de" + MAX_Q_COUNT + "correos electronicos"
        preven = "Servicio Postfix detenido"
        enviar_correo(admin[0], admin[1],'Tipo de alerta: Limite de cola de correo electronico alcanzado', info + "\n" + preven)
        echo_alarmas_log(fecha_hora, info , "verificar_cola_correo",'') 
        echo_prevencion_log(fecha_hora, preven, "Posible ataque DoS/DDoS")
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo("verificar_cola_correo")
        obj_alarm_prev.setResultado(info)
        obj_alarm_prev.setAccion(preven)
        insertarAlarmaPrevencion(obj_alarm_prev)


        
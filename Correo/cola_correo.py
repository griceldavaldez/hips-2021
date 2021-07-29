from utils import get_fecha
import subprocess
from Correo.correo import enviar_correo
from Logs.logs import echo_prevencion_log, echo_alarmas_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion

#Funcion: verificar_cola_correo
#	Verifica si la cola de mails supero una cantidad maxima determinada
#Parametros:
#	MAX_Q_COUNT	(int) numero maximo de mails que pueden estar en cola
#   admin (lista) contiene los datos del administrador como el correo y pass, sirve para enviar los correos
def verificar_cola_correo(MAX_Q_COUNT, admin):
    print("Inicia la funcion verificar_cola_correo() \n", "\t\t Hora: " + get_fecha())
    p = subprocess.Popen("mailq", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    mail_list = output.decode("utf-8").splitlines()
    if MAX_Q_COUNT >-1 and len(mail_list) > MAX_Q_COUNT:
        p = subprocess.Popen("service postfix stop", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        info = "Posible ataque DoS/DDoS.La cola de correo alcanzo el limite de" + MAX_Q_COUNT + "correos electronicos"
        print("\t\t Resultado: " + info)
        prevencion = "Servicio Postfix detenido"
        print("\t\t Accion: " + prevencion)
        enviar_correo(admin[0], admin[1],'Tipo de alerta: Limite de cola de correo electronico alcanzado', info + "\n" + prevencion)
        echo_alarmas_log(info , "verificar_cola_correo",'') 
        echo_prevencion_log(prevencion, "Posible ataque DoS/DDoS")
        obj_alarm_prev = AlarmaPrevencion(get_fecha(), "verificar_cola_correo", info, prevencion)
        insertarAlarmaPrevencion(obj_alarm_prev)


        
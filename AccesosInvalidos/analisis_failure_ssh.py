import subprocess
from Correo.correo import enviar_correo
from Logs.logs import echo_alarmas_log, echo_prevencion_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from AccesosInvalidos.analisis_accesos_invalidos import bloquear_ip
from utils import get_fecha

#Funcion: analisis_ssh
#	Verifica si alguien ha intentado realizar un login a nuestra maquina via SSH y ha
#	fracasado. Si ha fracasado 5 veces, se bloquea a dicha IP utilizando IPTables (ver: bloquear) y alerta via correo.
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#
#Parametros:
#	MI_IP	(string)IP de la maquina servidor. Para obviarla de la busqueda de intentos fallidos
#   limite (int) limite de intentos fallidos.Por lo general son 5
#   admin (list) contiene los datos del administrador como su correo y contraseña
def analisis_failure_ssh(MI_IP,limite, admin):
    counts = dict()
    ip_lista = list()
    p =subprocess.Popen("cat /var/log/secure | grep -i \"ssh\" | grep -i \"Failed password\" | grep -v \""+MI_IP+"\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body = ''
    body_prevencion = ''
    for linea in ret_msg.splitlines():
        ip = linea.split(" ")[-4] #la ip se encuentra en la posicion -4 del string
        ip_lista.append(ip)
        echo_alarmas_log("Error de autenticacion SSH" + linea, "analisis_failure_ssh",ip)
        print("\t\t Resultado: " + "Error de autenticacion SSH" + linea)
    for ip in ip_lista:
        if ip in counts:
            counts[ip]+=1
            if counts[ip] == limite :
                bloquear_ip(ip)
                body = body + '\n'+ip
                echo_prevencion_log(ip+" fue bloqueado usando IPTables "," SSH fallo la contraseña mas de "+ str (limite) +" veces")
                body_prevencion = body_prevencion + ip + "\n"
                print("\t\t Accion: " + ip+" fue bloqueado usando IPTables ")
        else:
            counts[ip]=1
    body = body + ret_msg
    if body != '':
        enviar_correo(admin[0], admin[1],'Tipo de Alerta : Error de autenticacion SSH',body)
    if body_prevencion != '':
        body_prevencion = "Las siguientes direcciones IP fueron bloqueadas usando IPTables :: Error de autenticacion SSH\n" + body_prevencion
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Bloqueo de IPs', body_prevencion)
        obj_alarm_prev = AlarmaPrevencion(None, get_fecha(), 'analisis_failure_ssh', "Demasiadas fallas de autenticacion SSH."+ " SSH fallo la contraseña mas de "+ str (limite) +" veces", body_prevencion.replace("\n", " "))
        insertarAlarmaPrevencion(obj_alarm_prev)
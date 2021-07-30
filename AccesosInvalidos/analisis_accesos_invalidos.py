import subprocess
from Logs.logs import echo_alarmas_log, echo_prevencion_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from Correo.correo import enviar_correo
from utils import get_fecha

#Funcion: analisis_directorio_invalido
#	Verifica si alguna maquina se encuentra realizando fuzzing. Luego de 5 intentos fallidos de
#	acceder a un directorio de la pagina web del servidor, se alerta y bloquea la IP
#	mediante el uso de IPTables (ver: bloquear_ip)
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#Parametros:
#	MY_IP	(string)IP de la maquina servidor. Para obviarla de la busqueda de intentos fallidos.
def analisis_directorio_invalido (MY_IP,limite, admin):
    print("Inicia la funcion analisis_directorio_invalido() \n", "\t\t Hora: " + get_fecha())
    counts = dict()
    ip_lista = list()
    p = subprocess.Popen("cat /var/log/httpd/access_log | grep -v "+MY_IP+" | grep -v ::1 | grep 404", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    for linea in ret_msg.splitlines():
        #la primera palabra de cada linea es la ip
        p_palabra = linea.split(" ")[0]
        ip_lista.append(p_palabra)
    body = ''
    for ip in ip_lista:
        if ip in counts:
            counts[ip]+=1
            if counts[ip] == limite :
                bloquear_ip(ip)
                body = body + ' \n '+ip
                echo_alarmas_log("Ip "+ip+" intentada "+str(limite)+" directorios inexistentes en el servidor web", "analisis_directorio_invalido",ip)
                print("\t\t Resultado: " + "Ip "+ip+" intentada "+str(limite)+" directorios inexistentes en el servidor web")
                echo_prevencion_log(ip+" Ip fue bloqueado usando IPTables","Ataque fuzzing. Directorio web desconocido")
                print("\t\t Accion: " + ip+" Ip fue bloqueado usando IPTables")
        else:
            counts[ip]=1
    if body != '':
        body = "IP bloqueadas: "+body
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Directorio web desconocido',body)
        obj_alarm_prev = AlarmaPrevencion(None, get_fecha(), "analisis_directorio_invalido", "Intentos repetidos para acceder a un directorio web inexistente. " + body.replace('\n', " "), "Ips fueron bloquedas usando IPTables y se envio un correo al administrador para dar aviso de la alarma")
        insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: bloquear_ip
#	Bloquea una ip dada utilizando IPTables.
#Parametros:
#	ip	(string) la IP que se desea bloquear.
def bloquear_ip(ip):
    p =subprocess.Popen("iptables -I INPUT -s "+ip+" -j DROP", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    p =subprocess.Popen("service iptables save", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

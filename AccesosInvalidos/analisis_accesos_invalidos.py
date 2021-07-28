import subprocess, datetime, os, sys
sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_alarmas_log, echo_prevencion_log

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

#Funcion: analisis_directorio_invalido
#	Verifica si alguna maquina se encuentra realizando fuzzing. Luego de 5 intentos fallidos de
#	acceder a un directorio de la pagina web del servidor, se alerta y bloquea la IP
#	mediante el uso de IPTable (ver: block_ip)
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmaslog y echo_prevencionlog)
#Parametros:
#	MY_IP	(string)IP de la maquina servidor. Para obviarla de la busqueda de intentos fallidos.
def analisis_directorio_invalido (MY_IP,limite, admin):
    counts = dict()
    ip_lista = list()
    p = subprocess.Popen("cat /var/log/httpd/access_log | grep -v "+MY_IP+" | grep -v ::1 | grep 404", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for line in ret_msg.splitlines():
        #la primera palabra de cada linea es la ip
        p_palabra = line.split(" ")[0]
        ip_lista.append(p_palabra)
    body = ''
    for ip in ip_lista:
        if ip in counts:
            counts[ip]+=1
            if counts[ip] == limite :
                bloquear_ip(ip)
                body = body + ' \n '+ip
                echo_alarmas_log(fecha_hora, "Ip "+ip+" intentada "+str(limite)+" directorios inexistentes en el servidor web", "analisis_directorio_invalido",ip)
                echo_prevencion_log(fecha_hora, ip+" Ip fue bloqueado usando IPTables","Ataque fuzzing. Directorio web desconocido")
        else:
            counts[ip]=1
    if body != '':
        body = "IP bloqueadas: "+body
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Directorio web desconocido',body)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo("analisis_directorio_invalido")
        obj_alarm_prev.setResultado("Intentos repetidos para acceder a un directorio web inexistente " + body.strip('\n') )
        obj_alarm_prev.setAccion("Ips fueron bloquedas usando IPTables y se envio un correo al administrador para dar aviso de la alarma")
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

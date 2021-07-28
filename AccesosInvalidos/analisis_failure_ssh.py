
from Correo.correo import enviar_correo
import datetime, subprocess, os
from Logs.logs import echo_alarmas_log, echo_prevencion_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from AccesosInvalidos.analisis_accesos_invalidos import bloquear_ip

#Funcion: analisis_ssh
#	Verifica si alguien ha intentado realizar un login a nuestra maquina via SSH y ha
#	fracasado. Si ha fracasado 5 veces, se bloquea a dicha IP utilizando IPTables (ver: block_ip) y alerta via mail.
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#
#Parametros:
#	MI_IP	(string)IP de la maquina servidor. Para obviarla de la busqueda de intentos fallidos.
def analisis_failure_ssh(MI_IP,limite, admin):
    counts = dict()
    ip_lista = list()
    p =subprocess.Popen("cat /var/log/secure | grep -i \"ssh\" | grep -i \"Failed password\" | grep -v \""+MI_IP+"\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body = ''
    body_prevencion = ''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for linea in ret_msg.splitlines():
        ip = linea.split(" ")[-4] #la ip se encuentra en la posicion -4 del string
        ip_lista.append(ip)
        echo_alarmas_log(fecha_hora, "Error de autenticacion SSH" + linea, "analisis_failure_ssh",ip)
    for ip in ip_lista:
        if ip in counts:
            counts[ip]+=1
            if counts[ip] == limite :
                bloquear_ip(ip)
                body = body + '\n'+ip
                echo_prevencion_log(fecha_hora, ip+" fue bloqueado usando IPTables "," SSH fallo la contraseña mas de "+ str (limite) +" veces")
                body_prevencion = body_prevencion + ip + "\n"
                #print(ip+ " fue bloqueado usando IPTables. Demasiadas fallas de autenticacion SSH.\n")
        else:
            counts[ip]=1
    body = body + ret_msg
    if body != '':
        enviar_correo(admin[0], admin[1],'Tipo de Alerta : Error de autenticacion SSH',body)
    if body_prevencion != '':
        body_prevencion = "Las siguientes direcciones IP fueron bloqueadas usando IPTables :: Error de autenticacion SSH\n" + body_prevencion
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Bloqueo de IPs', body_prevencion)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo("analisis_failure_ssh")
        obj_alarm_prev.setResultado("Demasiadas fallas de autenticacion SSH. " + " SSH fallo la contraseña mas de "+ str (limite) +" veces" )
        obj_alarm_prev.setAccion("Las siguientes direcciones IP fueron bloqueadas usando IPTables :: Error de autenticacion SSH " + body_prevencion.replace('\n', " "))
        insertarAlarmaPrevencion(obj_alarm_prev)
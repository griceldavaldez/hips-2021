import random, subprocess, string, datetime, os, sys
sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_alarmas_log, echo_prevencion_log


#Funcion: analisis_ataque_smtp
#	Invoca a las funciones que buscan patrones de un posible ataque SMTP.
#	(Ver: verificar_smtp_maillog , verificar_smtp_messages y verificar_smtp_secure)
def analisis_ataque_smtp(maxmailpu, admin):
    verificar_smtp_maillog(maxmailpu, admin)
    verificar_smtp_messages(maxmailpu, admin)
    verificar_smtp_secure(maxmailpu, admin)


#Funcion: verificar_smtp_maillog
#	Verifica si se han enviado una cantidad masiva de mails desde un mismo correo
#	y de ser asi lo pone en una lista negra y alerta. Lo hace revisando el archivo /var/log/maillog
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
def verificar_smtp_maillog(maxmailpu, admin):
    counts = dict()
    p = subprocess.Popen("cat  /var/log/maillog | grep -i authid", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = ''
    for linea in ret_msg.splitlines():
        correo = linea.split(' ')[-3]
        correo = correo[7:-1] #quitamos el authid= y la coma del final
        if correo in counts:
            counts[correo]+=1
            if counts[correo] == maxmailpu:
                body = body+correo+"\n"
                agregar_lista_negra_postfix(correo)
        else:
            counts[correo] = 1
    if body != '' :
        body = "Mas de" + str (maxmailpu) + "correos fueron enviados usando:" + body + "\n\n Todos los correos fueron agregados a la lista negra de postfix"
        enviar_correo(admin[0], admin[1],'Tipo de Alerta : Correos masivos',body)
    for key in counts:
        aux = counts[key]
        if aux >= maxmailpu and maxmailpu >=0:
            echo_alarmas_log(fecha_hora, str(aux)+" correos electronicos enviados usando "+key, 'analisis_ataque_smtp','')
            echo_prevencion_log(fecha_hora, key+" se agrego a la lista negra de correos electronicos de Postfix", "Ataque SMTP")
            obj_alarm_prev = AlarmaPrevencion()
            obj_alarm_prev.setFechaHora(fecha_hora)
            obj_alarm_prev.setTipoEscaneo('analisis_ataque_smtp')
            obj_alarm_prev.setResultado("Ataque SMTP. " + str(aux)+" correos electronicos enviados usando "+key)
            obj_alarm_prev.setAccion(key+" se agrego a la lista negra de correos electronicos de Postfix")
            insertarAlarmaPrevencion(obj_alarm_prev)
            

#Funcion: verificar_smtp_messages
#	Verifica si se produjeron multiples Authentication Errors hacia un mismo usuario.
#	Lo hace revisando el archivo /var/log/messages
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
def verificar_smtp_messages(maxmailpu, admin):
    counts = dict()
    p = subprocess.Popen("cat  /var/log/messages | grep -i \"[service=smtp]\" | grep -i \"auth failure\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body = ''
    nuevo_pass = ''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for linea in ret_msg.splitlines():
        usuario = linea.split('=')[1] #conseguimos condorito] [service
        usuario = usuario.split(']')[0] #aislamos el username del string anterior
        if usuario in counts:
            counts[usuario]+=1
            if counts[usuario] == maxmailpu:
                body = body + usuario +"\n"
                passw = get_random_string(random.randint(20,30))
                nuevo_pass = nuevo_pass + usuario + " :: " + passw
                p = subprocess.Popen("echo \""+usuario+":"+passw+"\" | chpasswd 2> /dev/null", stdout=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
        else:
            counts[usuario] = 1
    if body != '' :
        body = "Mas de "+str(maxmailpu)+" Fallo de autenticacion SMTP usando: " + body + "\n\n Se cambiaron todas las contraseñas de esos usuarios:\n\nUsername :: New_Password\n"+nuevo_pass
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Error masivo de autenticacion de usuario SMTP',body)
    for key in counts:
        aux = counts[key]
        if aux >= maxmailpu and maxmailpu >=0:
            echo_alarmas_log(fecha_hora, str(aux)+" fallos de autenticacion para "+key, 'analisis_ataque_smtp','')
            echo_prevencion_log(fecha_hora, "Fallo de autenticacion SMTP usando: " + body + "Se cambiaron todas las contraseñas", "Ataque SMTP" )
            obj_alarm_prev = AlarmaPrevencion()
            obj_alarm_prev.setFechaHora(fecha_hora)
            obj_alarm_prev.setTipoEscaneo('analisis_ataque_smtp')
            obj_alarm_prev.setResultado("Ataque SMTP"+ "Fallo de autenticacion SMTP usando: " + body.strip('\n') )
            obj_alarm_prev.setAccion("Se cambiaron todas las contraseñas de los usuarios involucrados")
            insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: verificar_smtp_secure
#	Verifica si se produjeron multiples Authentication Errors hacia un mismo usuario.
#	Lo hace revisando el archivo /var/log/secure
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmaslog y echo_prevencionlog)
def verificar_smtp_secure(maxmailpu, admin):
    counts = dict()
    p = subprocess.Popen("cat  /var/log/secure | grep -i \"(smtp:auth)\" | grep -i \"authentication failure\"", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body = ''
    nuevo_pass = ''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for linea in ret_msg.splitlines():
        usuario = linea.split('=')[-1] #conseguimos el username condorito
        if usuario in counts:
            counts[usuario]+=1
            if counts[usuario] == maxmailpu:
                body = body+usuario+"\n"
                passwd = get_random_string(random.randint(20,30))
                nuevo_pass = nuevo_pass + usuario + " :: " + passwd
                p = subprocess.Popen("echo \""+usuario+":"+passwd+"\" | chpasswd 2> /dev/null", stdout=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
        else:
            counts[usuario] = 1
    if body != '' :
        body = "Mas de "+str(maxmailpu)+" Error de autenticacion SMTP usando: " + body + "\n\n Se cambiaron todas las contraseñas de esos usuarios:\n\nUsername :: New_Password\n"+nuevo_pass
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Error masivo de autenticación de usuario SMTP',body)
    for key in counts:
        aux = counts[key]
        if aux >= maxmailpu and maxmailpu >=0:
            echo_alarmas_log(fecha_hora, str(aux)+" fallos de autenticacion para "+key, 'analisis_ataque_smtp','')
            echo_prevencion_log(fecha_hora, "Error masivo de autenticación de usuario SMTP usando: " + body.strip('\n') + "Se cambiaron todas las contraseñas", "Ataque SMTP")
            obj_alarm_prev = AlarmaPrevencion()
            obj_alarm_prev.setFechaHora(fecha_hora)
            obj_alarm_prev.setTipoEscaneo('analisis_ataque_smtp')
            obj_alarm_prev.setResultado("Ataque SMTP. "+ "Error masivo de autenticación de usuario SMTP usando: " + body.strip('\n'))
            obj_alarm_prev.setAccion("Se cambiaron todas las contraseñas de los usuarios involucrados")
            insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: get_random_string
#	genera un string con caraacteres aleatorios de longitud l
#Parametros:
#		len	(int) longitud de la cadena deseada.
#Retorna:
#		new_str	(string) la cadena de caracteres generada
def get_random_string(len):
    letters = string.ascii_letters + "1234567890!@#$%^&*()-_=+"
    nuevo_str = ''.join(random.choice(letters) for i in range(len))
    return (nuevo_str)


#Funcion: agregar_lista_negra_postfix
#	Agrega una direccion de correo a la lista negra de postfix
#Parametros:
#	correo	(string) direccion de correo electronico que se desea agregar a la lista negra.
def agregar_lista_negra_postfix(correo):#verificar si es que no esta
	p =subprocess.Popen("echo \""+correo+" REJECT\">>/etc/postfix/sender_access", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p =subprocess.Popen("postmap /etc/postfix/sender_access", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
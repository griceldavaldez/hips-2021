import subprocess, os
from Correo.correo import enviar_correo
from Logs.logs import echo_alarmas_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from utils import get_fecha


#Funcion: analsis_cron
#	Analiza las lineas retornadas por el comando crontab -l en busca de scripts, shells y
#	aplicaciones o herramientas consideradas peligrosas o no deseadas por el usuario.
#	Lo hace invocando a las funciones is_script_cron , is_shell_cron , is_sniffer_cron
#	Si los encuentra, alerta al usuario por mail.
#	Guarda las alertas en el log correspondiente (Ver: echo_alarmas_log)
#Parametros:
#	P_APP_LIST	(string) string con las aplicaciones consideradas peligrosas con el formato: app1|app2|app3
#   admin (dict) contiene los datos del administrador como el correo y la contraseña, sirven para mandar el correo
def analsis_cron(P_APP_LIST, admin):
    print("Inicia la funcion analsis_cron() \n", "\t\t Hora: " + get_fecha())
    app_list = P_APP_LIST.split("|")
    p =subprocess.Popen("crontab -l", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ret_msg = output.decode("utf-8")
    body_scripts = ''
    body_shells = ''
    body_sniffers = ''
    for linea in ret_msg.splitlines():
        result = is_shell_cron(linea, admin)
        if (result != ''):
            body_shells = body_shells + result
        result = is_script_cron(linea, admin)
        if (result != ''):
            body_scripts = body_scripts + result
        result = is_sniffer_cron(linea, app_list, admin)
        if (result != ''):
            body_sniffers = body_sniffers + result
    body = body_scripts + body_shells + body_sniffers
    if (body != ''):
        body = ""+body+"\nVerifique y tome una accion"
        enviar_correo(admin[0], admin[1],'Tipo de Alerta : Archivos sospechosos en Cron',body)
        echo_alarmas_log("Archivos sospechosos en Cron " + body.replace("\n", " "), 'analsis_cron', '')
        print("\t\t Resultado: " + "Archivos sospechosos en Cron " + body.replace("\n", " "))
        print("Se envio un correo al administrador para dar aviso de la alarma")
        obj_alarm_prev = AlarmaPrevencion(get_fecha(), 'analsis_cron', "Archivos sospechosos en Cron " + body.replace("\n", " ") , "Se envio un correo al administrador para dar aviso de la alarma")
        insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: is_shell_cron
#	Analiza el string que recibe como parametro, extrae el PATH encontrado en el string
#	y busca dentro de este archivo (si es que existe) el contenido '#!' que marca a los shells	
#Parametros:
#	linea	(string) una linea leida utilizando el comando crontab -l. Se debe respetar el
#		formato: * * * * * [USERNAME_ocional] DIRECTORIO_DE_SCRIPT
#Retorna:
#	(string) un string vacio ('') si el archivo ubicado en el path encontrado en la linea 
#	pasada como parametro no es un shell
#	o un string con la informacion de que se detecto un shell en la linea pasada como parametro
def is_shell_cron(linea):
    palabras = linea.split()
    ruta = palabras[-1]
    cat =subprocess.Popen("cat "+ruta+" 2> /dev/null | grep '#!'", stdout=subprocess.PIPE, shell=True)
    (output, err) = cat.communicate()
    txt = output.decode("utf-8")
    if(txt !=''):
        info = "Posible shell ejecutandose en cron:: "+linea+"\n"
        echo_alarmas_log(info, 'analsis_cron.shell','')
        return (info)
    return ('')


#Funcion: is_script_cron
#	Analiza el string que recibe como parametro en busca de terminaciones clasicas de
#	scripts (ejemplo: .py, .c, .exe, etc) y tambien terminaciones combinadas como .php.jpeg
#Parametros:
#	linea	(string) una linea leida utilizando el comando crontab -l. Se debe respetar el
#		formato: * * * * * [USERNAME_ocional] DIRECTORIO_DE_SCRIPT
#Retorna:
#	(string) un string vacio ('') si no se encontro una terminacion de script en el parametro
#	o un string con la informacion de que se detecto un script en la linea pasada como parametro
def is_script_cron(linea):
    palabras = linea.split()
    ruta = palabras[-1]
    exten = ['py','c','cpp','ruby','sh','exe','php','java','pl']
    dirs = ruta.split("/")
    script = dirs[-1]
    my_extens = script.split(".")
    my_extens.reverse()
    for e in my_extens:
        for e2 in exten:
            if (e==e2):
                if (os.path.isfile(ruta)):
                    info = "Posible script ejecutandose en cron :: "+linea+"\n"
                    echo_alarmas_log(info, 'analsis_cron.script','')
                    return (info)
    return ('')


#Funcion: is_sniffer_cron
#	Analiza el string que recibe como parametro y verifica si este ejecuta alguna de las
#	aplicaciones consideradas peligrosas o no deseadas segun el usuario.
#	Si los encuentra, alerta al usuario por correo.
#	Guarda las alertas en el log correspondiente (Ver: echo_alarmas_log)
#Parametros:
#	linea	(string) una linea leida utilizando el comando crontab -l. Se debe respetar el
#		formato: * * * * * [USERNAME_ocional] DIRECTORIO_DE_SCRIPT
#	P_APP_LIST	(string) string con las aplicaciones consideradas peligrosas con el formato: app1|app2|app3
#Retorna:
#	(string) un string vacio ('') si el archivo encontrado en la linea pasada como 
#	parametro no ecorresponde a una de las aplicaciones citadas en P_APP_LIST
#	o un string con la informacion de que se detecto una posible aplicacion no deseada en
#	la linea pasada como parametro
def is_sniffer_cron(linea, P_APP_LIST):
    palabras = linea.split()
    ruta = palabras[-1]
    dirs = ruta.split("/")
    app = dirs[-1]
    for e in P_APP_LIST:
        if (e==app):
            info = "Aplicaciones peligrosas como sniffers ejecutandose en cron :: "+linea+"\n"
            echo_alarmas_log(info, 'analsis_cron','')
            return (info)
    return ('')


import subprocess, datetime, os, sys

sys.path.append( os.path.abspath('../Cuarentena/'))
from cuarentena import enviar_a_cuarentena

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_alarmas_log, echo_prevencion_log

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../BaseDatos/'))
from modelos import AlarmaPrevencion
from dao import insertarAlarmaPrevencion


#Funcion: analisis_tmp
#	Invoca a las funciones encargadas de monitorear el directorio /tmp en busca de archivos sospechosos.
#	(ver: buscar_shells y buscar_scripts)
#
def analisis_tmp(admin):
    buscar_shells('/tmp', admin)
    buscar_scripts('/tmp', admin)


#Funcion: buscar_shells
#	Inspecciona los archivos dentro de un directorio (de forma recursiva con find) buscando patrones
#	de archivos shell (empiezan con #!).
#	Si los encuentra, alerta y mueve el archivo al directorio de cuarentena.
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmaslog y echo_prevencionlog)
#Parametros:
#	DIR	(string) absolute path del directorio donde se buscaran los shells. Normalmente es /tmp
#    admin (lista) lista con los datos del administrador para enviar correo
def buscar_shells(DIR, admin):
    msg = ''
    p = subprocess.Popen("find "+DIR+" -type f", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    archivos_tmp_string = output.decode("utf-8")
    for linea in archivos_tmp_string.splitlines():
        cat =subprocess.Popen("cat "+ linea +" | grep '#!'", stdout=subprocess.PIPE, shell=True)
        (output, err) = cat.communicate()
        txt = output.decode("utf-8")
        if(txt !=''):
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # la hora en que se hizo el escaneo
            msg += 'Se encontro un posible script de shell en:' + linea + '\n'
            enviar_a_cuarentena(linea)
            #print ('Se encontró un posible script de shell en:' + linea + "-> Archivo enviado a cuarentena. \ n")
            echo_alarmas_log( fecha_hora, "Shell encontrado" + linea, "analisis_tmp()", "")
            echo_prevencion_log(fecha_hora, "Archivo" + linea + "movido a carpeta de cuarentena", "Shell encontrado en "+ DIR)
    if msg!='':
        body = msg +"\nTodos los archivos se enviaron a cuarentena."
        enviar_correo(admin[0], admin[1], 'Tipo de alerta: Shells encontrados',body) # se envia el correo
        #se registra los resultados en la base de datos
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo('analisis_tmp')
        obj_alarm_prev.setResultado("Shells encontrados en " +DIR+  " : " + linea)
        obj_alarm_prev.setAccion("Todos los archivos se enviaron a cuarentena")
        insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: buscar_scripts
#	Inspecciona las terminaciones de los archivos dentro de un directorio (de forma recursiva con find)
#	buscando terminaciones clasicas de scripts (ejemplo: .py, .c, .exe, etc).
#	Si los encuentra, alerta y mueve el archivo al directorio de cuarentena.
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmaslog y echo_prevencionlog)
#Parametros:
#	DIR	(string) absolute path del directorio donde se buscaran los scripts. Normalmente es /tmp
#   admin (lista) lista con los datos del administrador para enviar correo

def buscar_scripts(DIR, admin):
    exten = ['py','c','cpp','ruby','sh','exe','php','java','pl']
    cmd = "find "+DIR+" -type f "
    for e in exten:
        cmd+= "-iname '*."+e+"' -o -iname '*."+e+".*' -o "
    if cmd!="find "+DIR+" -type f ":
        cmd = cmd[:-4]
    p =subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    body = ''
    scripts = output.decode("utf-8")
    body = body + scripts
    if body!='':
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        for linea in scripts.splitlines():
            enviar_a_cuarentena(linea)
            print ('Se encontró un posible script en:' + linea+  "-> Archivo enviado a cuarentena. \n")
            echo_alarmas_log(fecha_hora, "Script encontrado "+linea + "en " + DIR, 'analisis_tmp()',"")
            echo_prevencion_log("Archivo "+linea+" movido a la carpeta de cuarentena","Script encontrado en " +DIR)
        body = 'Se encontraron posibles archivos de script: \n' +body +"\nTodos los archivos se enviaron a cuarentena."
        enviar_correo(admin[0], admin[1], 'Tipo de alerta: Scripts encontrados', body)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo('analisis_tmp')
        obj_alarm_prev.setResultado("Script encontrado "+linea + "en " + DIR)
        obj_alarm_prev.setAccion("Archivo "+linea+" movido a la carpeta de cuarentena")
        insertarAlarmaPrevencion(obj_alarm_prev)
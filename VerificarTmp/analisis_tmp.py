
from VerificarTmp.verificar_tmp import buscar_scripts, buscar_shells
from Cuarentena.cuarentena import enviar_a_cuarentena
from Logs.logs import echo_alarmas_log, echo_prevencion_log
from Correo.correo import enviar_correo
from BaseDatos.modelos import AlarmaPrevencion
from BaseDatos.dao import insertarAlarmaPrevencion
import subprocess 
import datetime


def analisis_tmp(admin):
    buscar_shells('/tmp', admin)
    buscar_scripts('/tmp', admin)


def buscar_shells(DIR, admin):
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # la hora en que se hizo el escaneo
    msg = ''
    p = subprocess.Popen("find "+DIR+" -type f", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    archivos_tmp_string = output.decode("utf-8")
    for linea in archivos_tmp_string.splitlines():
        cat =subprocess.Popen("cat "+ linea +" | grep '#!'", stdout=subprocess.PIPE, shell=True)
        (output, err) = cat.communicate()
        txt = output.decode("utf-8")
        if(txt !=''):
            msg += 'Se encontró un posible script de shell en:' + linea + '\n'
            enviar_a_cuarentena(linea)
            #print ('Se encontró un posible script de shell en:' + linea + "-> Archivo enviado a cuarentena. \ n")
            echo_alarmas_log( fecha_hora, "Shell encontrado" + linea, "analisis_tmp()", "")
            echo_prevencion_log(fecha_hora, "Archivo" + linea + "movido a carpeta de cuarentena", "Shell encontrado en /tmp")
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


def buscar_scripts():
   

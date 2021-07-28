import datetime, subprocess, os, sys

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_prevencion_log, echo_alarmas_log

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

sys.path.append( os.path.abspath('../Cuarentena/'))
from cuarentena import enviar_a_cuarentena


#Funcion: analisis_promiscuo
#	Invoca a las funciones encargadas de monitorear los modos promiscuos y sniffers.
#	(Ver: verificar_modo_promiscuo y verificar_sniffers)
#Parametros:
#	P_DIR	(string)directorio de donde buscar los dispositivos, Normalmente es /var/log/secure
#	P_APP_LIST	(string) string con las aplicaciones consideradas peligrosas o no
#			deseadas segun el usuario separadas por medio de "|".
#			Se debe respetar el formato: app1|app2|app3
#   admin (lista) contiene los datos del administrador como el correo y pass
def analisis_promiscuo(P_DIR, P_APP_LIST, admin):
    verificar_modo_promiscuo(P_DIR, admin)
    verificar_sniffers(P_APP_LIST, admin)



#Funcion: check_promisc_devs
#	Verifica el estado del modo promiscuos de los dispositivos del ordenador, verificando
#	si fue encendido o apagado ultimamente.
#	En caso de encontrar algun dispositivo en modo promiscuo, lo alerta.
#	Guarda las alertas en el log correspondiente (Ver: echo_alarmas_log)
#Parametros:
#	P_DIR	(string)directorio de donde buscar los dispositivos, Normalmente es /var/log/secure
#   admin (lista) contiene los datos del administrador como el correo y pass
def verificar_modo_promiscuo(P_DIR, admin ):
    p_off = subprocess.Popen("cat "+P_DIR+" | grep \"left promisc\"", stdout=subprocess.PIPE, shell=True)
    (output_off, err) = p_off.communicate()
    datos_off = output_off.decode("utf-8")
    lista_off = datos_off.splitlines()
    l_off = len(lista_off)
    p_on = subprocess.Popen("cat "+P_DIR+" | grep \"entered promisc\"", stdout=subprocess.PIPE, shell=True)
    (output_on, err) = p_on.communicate()
    datos_on = output_on.decode("utf-8")
    lista_on = datos_on.splitlines()
    l_on = len(lista_on)
    body = ''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if l_off != l_on:
        compare = []
        dispositivos_on = []
        for linea in lista_off:
            compare.append(linea.split()[-4])
        for linea in lista_on:
            compare.append(linea.split()[-4])
        
        dict_counter = {i:compare.count(i) for i in compare}
        for dispositivo in dict_counter:
            if dict_counter[dispositivo]%2 != 0:
                dispositivos_on.append(dispositivo)
        for dispositivo in dispositivos_on:
            body = ''+dispositivo+' :: Modo promiscuo activado\n'
            echo_alarmas_log(fecha_hora, "El dispositivo: "+dispositivo+" Modo promiscuo activado", "analisis_promiscuo",'')
            #print(''+dispositivo+' :: Modo promiscuo esta activado\n')
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Modo promiscuo activado',body)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo('analisis_promiscuo')
        obj_alarm_prev.setResultado('Modo promiscuo activado:'+ dispositivo)
        obj_alarm_prev.setAccion("Se envio un correo al administrador para informar la alerta")
        insertarAlarmaPrevencion(obj_alarm_prev)

#Funcion: verificar_sniffers
#	Busca si se encuentran en el ordenador aplicaciones de sniffers no deseadas.
#	En caso de encontrar alguna, lo alerta, mata el proceso y lo pone en el directorio de cuarentena
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#Parametros:
#	P_APP_LIST	(string) string con las aplicaciones consideradas peligrosas o no
#			deseadas segun el usuario separadas por medio de "|"
#			Se debe respetar el formato: app1|app2|app3
#   admin (lista) contiene los datos del administrador como el correo y pass
def verificar_sniffers(P_APP_LIST, admin):
    p = subprocess.Popen("ps axo pid,command | grep -E '"+P_APP_LIST+"' | grep -v '"+P_APP_LIST+"'", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    body = output.decode("utf-8")
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for linea in body.splitlines():
        archivo_dir = linea.split(' ')[1]
        app_pid = linea.split(' ')[0]
        matar_proceso(app_pid)
        enviar_a_cuarentena(archivo_dir)
        echo_alarmas_log(fecha_hora, "Aplicacion sniffer encontrada en "+archivo_dir, 'analisis_promiscuo','')
        echo_prevencion_log(fecha_hora, "La aplicacion ubicada en "+ archivo_dir +" fue eliminada y enviada a la carpeta de cuarentena ", "Aplicacion sniffer encontrada")
    if len(body)>1:
        body = 'Servicio de sniffers encontrados:\n'+body+"\nTodos los sniffers fueron enviados a cuarentena"
        enviar_correo(admin[0], admin[1],'Tipo de Alarma: Sniffers encontrados',body)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo('analisis_promiscuo')
        obj_alarm_prev.setResultado('Servicio de sniffers encontrados:'+body.strip('\n'))
        obj_alarm_prev.setAccion("Los sniffers fueron eliminados y enviados a cuarentena")
        insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: kill_process
#	Mata el proceso especificado.
#Parametros:
#	pid	(string / int) process id del proceso a matar.
def matar_proceso(pid):
	p =subprocess.Popen("kill -9 "+str(pid), stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()

import subprocess
from Correo.correo import enviar_correo
from Logs.logs import echo_prevencion_log, echo_alarmas_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from Cuarentena.cuarentena import enviar_a_cuarentena
from utils import get_fecha


#Funcion: analisis_promiscuo
#	Invoca a las funciones encargadas de monitorear los modos promiscuos y sniffers.
#	(Ver: verificar_modo_promiscuo y verificar_sniffers)
#Parametros:
#	P_DIR	(string)directorio de donde buscar los dispositivos, Normalmente es /var/log/secure
#	P_APP_LIST	(string) string con las aplicaciones consideradas peligrosas con el formato: app1|app2|app3
#   admin (lista) contiene los datos del administrador como el correo y pass
def analisis_promiscuo(P_DIR, P_APP_LIST, admin):
    verificar_modo_promiscuo(P_DIR, admin)
    verificar_sniffers(P_APP_LIST, admin)



#Funcion: verificar_modo_promiscuo
#	Verifica el estado del modo promiscuo de los dispositivos del ordenador, verificando
#	si fue encendido o apagado ultimamente.
#	En caso de encontrar algun dispositivo en modo promiscuo, lo alerta.
#	Guarda las alertas en el log correspondiente (Ver: echo_alarmas_log)
#Parametros:
#	P_DIR	(string)directorio de donde buscar los dispositivos, Normalmente es /var/log/secure
#   admin (lista) contiene los datos del administrador como el correo y pass
def verificar_modo_promiscuo(P_DIR, admin ):
    print("Inicia la funcion verificar_modo_promiscuo() \n", "\t\t Hora: " + get_fecha())
    p_apag = subprocess.Popen("cat "+P_DIR+" | grep \"left promisc\"", stdout=subprocess.PIPE, shell=True)
    (output_off, err) = p_apag.communicate()
    datos_apag = output_off.decode("utf-8")
    lista_apag = datos_apag.splitlines()
    long_apag = len(lista_apag)
    p_encend = subprocess.Popen("cat "+P_DIR+" | grep \"entered promisc\"", stdout=subprocess.PIPE, shell=True)
    (output_on, err) = p_encend.communicate()
    datos_encen = output_on.decode("utf-8")
    lista_encen = datos_encen.splitlines()
    long_encen = len(lista_encen)
    body = ''
    if long_apag != long_encen:
        compare = []
        dispositivos_encen = []
        for linea in lista_apag:
            compare.append(linea.split()[-4])
        for linea in lista_encen:
            compare.append(linea.split()[-4])
        
        dict_counter = {i:compare.count(i) for i in compare}
        for dispositivo in dict_counter:
            if dict_counter[dispositivo]%2 != 0:
                dispositivos_encen.append(dispositivo)
        for dispositivo in dispositivos_encen:
            body = ''+dispositivo+' :: Modo promiscuo activado\n'
            echo_alarmas_log("El dispositivo: "+dispositivo+" se encuentra en modo promiscuo activado", "analisis_promiscuo.modo_promiscuo",'')
            print("\t\t Resultado: " + 'Modo promiscuo activado: '+ dispositivo)
            print("\t\t Accion: "+ "Se envio un correo al administrador para informar la alerta")
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Modo promiscuo activado',body)
        obj_alarm_prev = AlarmaPrevencion(get_fecha(), 'analisis_promiscuo.modo_promiscuo', 'Modo promiscuo activado. '+ body.replace("\n", " "), "Se envio un correo al administrador para informar la alerta")
        insertarAlarmaPrevencion(obj_alarm_prev)

#Funcion: verificar_sniffers
#	Busca si se encuentran en el ordenador aplicaciones de sniffers no deseadas.
#	En caso de encontrar alguna, lo alerta, mata el proceso y lo pone en el directorio de cuarentena
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#Parametros:
#	P_APP_LIST	(string) string con las aplicaciones consideradas peligrosas con el formato: app1|app2|app3
#   admin (lista) contiene los datos del administrador como el correo y pass
def verificar_sniffers(P_APP_LIST, admin):
    print("Inicia la funcion verificar_sniffers() \n", "\t\t Hora: " + get_fecha())
    p = subprocess.Popen("ps axo pid,command | grep -E '"+P_APP_LIST+"' | grep -v '"+P_APP_LIST+"'", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    body = output.decode("utf-8")
    for linea in body.splitlines():
        archivo_dir = linea.split(' ')[1]
        app_pid = linea.split(' ')[0]
        matar_proceso(app_pid)
        enviar_a_cuarentena(archivo_dir)
        echo_alarmas_log("Aplicacion sniffer encontrada en "+archivo_dir, 'analisis_promiscuo.sniffers','')
        print("\t\t Resultado: " + "Aplicacion sniffer encontrada en "+archivo_dir)
        echo_prevencion_log("La aplicacion ubicada en "+ archivo_dir +" fue eliminada y enviada a la carpeta de cuarentena ", "Aplicacion sniffer encontrada")
        print("\t\t Accion: "+ "La aplicacion ubicada en "+ archivo_dir +" fue eliminada y enviada a la carpeta de cuarentena ")
    if len(body)>1:
        body = 'Servicio de sniffers encontrados:\n'+body+"\nTodos los sniffers fueron enviados a cuarentena"
        enviar_correo(admin[0], admin[1],'Tipo de Alarma: Sniffers encontrados',body)
        obj_alarm_prev = AlarmaPrevencion(get_fecha(), 'analisis_promiscuo.sniffers', 'Servicio de sniffers encontrados:'+body.replace('\n', ' '), "Los sniffers fueron eliminados y enviados a cuarentena")
        insertarAlarmaPrevencion(obj_alarm_prev)


#Funcion: matar_proceso
#	Mata el proceso especificado.
#Parametros:
#	pid	(string / int) process id del proceso a matar.
def matar_proceso(pid):
	p =subprocess.Popen("kill -9 "+str(pid), stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()

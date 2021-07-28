import datetime, time, json, os, sys, psutil

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../Sniffers/'))
from analisis_promiscuo import matar_proceso

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_alarmas_log, echo_prevencion_log

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

#Funcion: analisis_consumo_procesos
#	Verifica el consumo de recursos de cpu, memoria y tiempo de los procesos activos.
#	En caso de encontrar algun proceso que sobrepase su valor de uso maximo lo alerta y lo mata.
#	(si no lo tiene definido, entonces se utilizaran los valores standard)
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmaslog y echo_prevencionlog)
#Parametros:
#	LIMIT_PROCESOS	(dict) diccionario con 'nombre_proceso', 'uso_cpu' 'uso_memoria','tiempo_maximo_ejecucion'
#				de los procesos.
#				name : (string) nombre del proceso
#				cpu_percent : (float) del 0 al 100, porcenje de uso de la cpu por el proceso
#				memory_percent : (float) del 0 al 100, porcenje de uso de la RAM por el proceso
#				create_time :	tiempo de creacion del proceso en POSIX

def analisis_consumo_procesos(LIMIT_PROCESOS, admin):
    lista_procesos = list()
    for proc in psutil.process_iter():
        dict_procesos = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time'])
        lista_procesos.append(dict_procesos)
    body = ''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for proc in lista_procesos:
        max_runtime = -1.000 # valores por defecto
        max_cpu = 90.000
        max_mem = 90.000
        for dic in LIMIT_PROCESOS:
            if (proc['name'].lower() == dic['nombre_proceso'].lower()):
                max_cpu = dic['uso_cpu']
                max_mem = dic['uso_memoria']
                max_runtime = dic['tiempo_maximo_ejecucion']
        p_runtime = time.time() - proc['create_time']

        exceeded = ''
        cpu_x=mem_x=runtime_x=False # Banderas para controlar si se ha excedido cpu, mem y/o runtime
        #Aqui se verifica si ha excedido el uso de la CPU
        if proc['cpu_percent'] > max_cpu:
            cpu_x = True
            exceeded=exceeded+'CPU'
        #Aqui se verifica si ha excedido el uso de la Memoria RAM
        if proc['memory_percent'] > max_mem:
            mem_x = True
            if exceeded != '':
                exceeded=exceeded+' & Memoria'
            else:
                exceeded=exceeded+'Memoria'
        #Aqui se verifica si el proceso ha excedido el tiempo de ejecucion
        if (p_runtime > max_runtime and max_runtime >=0.000) :
            runtime_x = True
            proc.update({'runtime':str(datetime.timedelta(seconds=int(p_runtime)))})
            if exceeded != '':
                exceeded=exceeded+' & Runtime'
            else:
                exceeded=exceeded+'Runtime'
        if cpu_x or mem_x or runtime_x:
            proc.update({'motivo': 'Excedida: '+exceeded+' el valor maximo para este proceso'})
            body+=json.dumps(proc)+'\n\n' #se guarda en formato json, por tratarse del tipo dict
            matar_proceso(proc['pid'])
            echo_alarmas_log(fecha_hora, "El proceso excedio el valor maximo de recursos "+json.dumps(proc), "analisis_consumo_procesos",'')
            echo_prevencion_log(fecha_hora, "Se mato al proceso con alto consumo de recursos "+json.dumps(proc), "Alto uso de recursos")
    if body !='':
        body = 'Se encontro un uso elevado del proceso: \n\n '+ body
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Alto uso de recursos',body)
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo("analisis_consumo_procesos")
        obj_alarm_prev.setResultado("Se encontro un uso elevado de procesos" + body.strip('\n') )
        obj_alarm_prev.setAccion("Se mato al proceso con alto consumo de recursos y se envio un correo al administrador")
        insertarAlarmaPrevencion(obj_alarm_prev)


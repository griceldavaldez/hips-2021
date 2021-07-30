import datetime, time, json, psutil
from Correo.correo import enviar_correo
from Sniffers.analisis_promiscuo import matar_proceso
from Logs.logs import echo_alarmas_log, echo_prevencion_log
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.dao import AlarmaPrevencion
from utils import get_fecha

#Funcion: analisis_consumo_procesos
#	Verifica el consumo de recursos de cpu, memoria y tiempo de los procesos activos.
#	En caso de encontrar algun proceso que sobrepase su valor de uso maximo lo alerta y lo mata.
#	(si no lo tiene definido, entonces se utilizaran los valores por defecto)
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#Parametros:
#	LIMIT_PROCESOS	(dict) diccionario con 'nombre_proceso', 'uso_cpu' 'uso_memoria','tiempo_maximo_ejecucion' de los procesos.
def analisis_consumo_procesos(LIMIT_PROCESOS, admin):
    print("Inicia la funcion analisis_consumo_procesos() \n", "\t\t Hora: " + get_fecha())
    lista_procesos = list()
    #psutil es una biblioteca multiplataforma para recuperar información sobre los procesos en ejecución y la utilización del sistema 
    #(CPU, memoria, discos, red, sensores) en Python.Utilizamos esta libreria, nos basandonos en el ejemplo 2 de: https://www.programcreek.com/python/example/53869/psutil.process_iter
    #pid :(int) pid del proceso, name : (string) nombre del proceso, cpu_percent : (float) del 0 al 100, porcenje de uso de la cpu por el proceso
    #memory_percent : (float) del 0 al 100, porcenje de uso de la RAM por el proceso, create_time :	tiempo de creacion del proceso en POSIX
    for proc in psutil.process_iter():
        dict_procesos = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time'])
        lista_procesos.append(dict_procesos)
    body = ''
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

        excede = ''
        cpu_x=mem_x=runtime_x=False # Banderas para controlar si se ha excedido cpu, mem y/o runtime
        #Aqui se verifica si ha excedido el uso de la CPU
        if proc['cpu_percent'] > max_cpu:
            cpu_x = True
            excede=excede+'CPU'
        #Aqui se verifica si ha excedido el uso de la Memoria RAM
        if proc['memory_percent'] > max_mem:
            mem_x = True
            if excede != '':
                excede=excede+' & Memoria'
            else:
                excede=excede+'Memoria'
        #Aqui se verifica si el proceso ha excedido el tiempo de ejecucion
        if (p_runtime > max_runtime and max_runtime >=0.000) :
            runtime_x = True
            proc.update({'runtime':str(datetime.timedelta(seconds=int(p_runtime)))})
            if excede != '':
                excede=excede+' & Runtime'
            else:
                excede=excede+'Runtime'
        if cpu_x or mem_x or runtime_x:
            proc.update({'reason': 'Excedida: '+excede+' el valor maximo para este proceso'})
            body+=json.dumps(proc)+'\n\n' #se guarda en formato json, por tratarse del tipo dict
            matar_proceso(proc['pid'])
            echo_alarmas_log("El proceso excedio el valor maximo de recursos "+json.dumps(proc), "analisis_consumo_procesos",'')
            print("\t\t Resultado: " + "El proceso excedio el valor maximo de recursos "+json.dumps(proc))
            echo_prevencion_log("Se mato al proceso con alto consumo de recursos "+json.dumps(proc), "Alto uso de recursos")
            print("\t\t Accion: " + "Se mato al proceso con alto consumo de recursos "+json.dumps(proc))
    if body !='':
        body = 'Se encontro un uso elevado del proceso: \n\n '+ body
        enviar_correo(admin[0], admin[1],'Tipo de Alerta: Alto uso de recursos',body)
        obj_alarm_prev = AlarmaPrevencion(None, get_fecha(), 'analisis_consumo_procesos', body.replace('\n', ' '), "Se mato al proceso con alto consumo de recursos y se envio un correo al administrador")
        insertarAlarmaPrevencion(obj_alarm_prev)


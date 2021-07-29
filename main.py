import os, subprocess
from preferencias import guardar_preferencias

from variables_globales import directorio_cuarentena
from VerificarMd5sum.analisis_md5sum import verificar_md5sum
from VerificarTmp.analisis_tmp import analisis_tmp
from UsuariosConectados.usuarios_conectados import comprobar_usuarios_conectados
from Correo.cola_correo import verificar_cola_correo
from AtaqueSmtp.analisis_ataque_smtp import analisis_ataque_smtp
from Sniffers.analisis_promiscuo import analisis_promiscuo
from Procesos.analisis_consumo import analisis_consumo_procesos
from AccesosInvalidos.analisis_accesos_invalidos import analisis_directorio_invalido
from AccesosInvalidos.analisis_auths_failure import analisis_auths_failure
from AccesosInvalidos.analisis_failure_ssh import analisis_failure_ssh
from Cron.analisis_cron import analsis_cron

#Funcion: main
#	Invoca a todas las funciones necesarias para el HIPS

def main():
    preferencias = guardar_preferencias()
    APPS_PELIGROSAS = preferencias['aplicacion_peligrosa']
    LIMIT_PROCESOS = preferencias['limite_proceso']
    MD5SUM_LISTA= preferencias['md5sum']
    general = preferencias['general']
    #se guardan las preferencias generales en variables individuales
    for i in general:
        MI_IP = i['ip']
        ADMIN_DATOS = [i['correo_admin'], i['pass_admin']] #Contiene los datos como correo y pass del admin
        MAXCPU = i['MAXCPU'] #max cpu por defecto
        MAXMEM = i['MAXMEM'] #max memoria por defecto
        MAX_Q_COUNT = i['cola_maxima_correo']
        MAX_MAIL_PU = i['correo_maximo_por_usuario']
        MAX_SSH = i['intento_maximo_ssh']
    MAX_FUZZ = 5
    P_DIR = '/var/log/messages'

    if os.path.isfile(P_DIR) is not True:
        P_DIR = '/var/log/syslog'
    # si no existe el directorio cuarentena, se crea
    if os.path.isdir(directorio_cuarentena) is not True: 
        p =subprocess.Popen("mkdir "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
    #se quitan los permisos de ejecucion para este directorio
    p =subprocess.Popen("chmod 664 "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True) 
    (output, err) = p.communicate()

    #si no se cargaron las configuraciones personalizadas, se cargan los valores por defecto
    for i in LIMIT_PROCESOS:
        if i['uso_cpu'] is None or i['uso_cpu'] == ' ': 
            i['uso_cpu'] = MAXCPU

        if i['uso_memoria'] is None or i['uso_memoria'] == ' ':
            i['uso_memoria'] = MAXMEM

    print("\n-------------------------\n\nESCANEANDO...\n\n-------------------------")
    verificar_cola_correo(MAX_Q_COUNT, ADMIN_DATOS)
    analisis_ataque_smtp(MAX_MAIL_PU, ADMIN_DATOS)
    analisis_promiscuo(P_DIR, APPS_PELIGROSAS, ADMIN_DATOS)
    analisis_consumo_procesos(LIMIT_PROCESOS, ADMIN_DATOS)
    comprobar_usuarios_conectados(ADMIN_DATOS)
    analisis_directorio_invalido(MI_IP,MAX_FUZZ, ADMIN_DATOS) 
    verificar_md5sum(MD5SUM_LISTA, ADMIN_DATOS)
    analisis_tmp(ADMIN_DATOS)
    analisis_auths_failure(ADMIN_DATOS)
    analsis_cron(APPS_PELIGROSAS, ADMIN_DATOS)
    analisis_failure_ssh(MI_IP,MAX_SSH, ADMIN_DATOS)
    print('\n-------------------------\n\nESCANEO COMPLETADO\n\n-------------------------')
    return(0)

#Programa principal
if __name__=='__main__':
    main()
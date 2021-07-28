from Configuraciones.preferencias import guardar_preferencias
import os, subprocess
from Main.variables_globales import directorio_cuarentena
from VerificarMd5sum.analisis_md5sum import verificar_md5sum
from VerificarTmp.analisis_tmp import analisis_tmp
from UsuariosConectados.usuarios_conectados import comprobar_usuarios_conectados

#Funcion: main
#	Invoca a todas las funciones necesarias para el HIPS repitiendose cada x intervalo de tiempo

def main():
    preferencias = guardar_preferencias()
    APPS_PELIGROSAS = preferencias['aplicacion_peligrosa']
    LIMIT_PROCESOS = preferencias['limite_proceso']
    MD5SUM_LISTA= preferencias['md5sum']
    general = preferencias['general']
    #se guardan las preferencias generales en variables individuales
    MI_IP = general['ip']
    ADMIN_DATOS = [general['correo_admin'], general['pass_admin']] #Contiene los datos como correo y pass del admin
    MAX_Q_COUNT = general['cola_maxima_correo']
    MAX_MAIL_PU = general['correo_maximo_por_usuario']
    MAX_SSH = general['intento_maximo_ssh']
    P_DIR = '/var/log/messages'

    if os.path.isfile(P_DIR) is not True:
        P_DIR = '/var/log/syslog'

    if os.path.isdir(directorio_cuarentena) is not True: # si no existe el directorio cuarentena, se crea
        p =subprocess.Popen("mkdir "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
    #se quitan los permisos de ejecucion para este directorio
    p =subprocess.Popen("chmod 664 "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True) 
    (output, err) = p.communicate()
    
    if LIMIT_PROCESOS['uso_cpu'] is None or LIMIT_PROCESOS['uso_cpu'] == '':
        MAX_CPU = general['MAXCPU']
    else:
        MAX_CPU = LIMIT_PROCESOS['uso_cpu']
    if LIMIT_PROCESOS['uso_memoria'] is None or LIMIT_PROCESOS['uso_memoria'] == '':
        MAX_MEM = general['MAXMEM']
    else:
        MAX_MEM = LIMIT_PROCESOS['uso_memoria']

    print("\n-------------------------\n\nESCANEANDO...\n\n-------------------------")
    check_mailq(MAX_Q_COUNT)
    check_smtp_attack(MAX_MAIL_PU)
    check_promisc(P_DIR, P_APP_LIST)
    process_usage(PROCESS_USAGE_LIMITS)
    comprobar_usuarios_conectados(ADMIN_DATOS)
    check_invalid_dir(MY_IP,MAX_FUZZ) #www.algo.com/noexiste
    check_promisc_apps(P_APP_LIST)
    verificar_md5sum(MD5SUM_LISTA, ADMIN_DATOS)
    analisis_tmp(ADMIN_DATOS)
    check_auths_log()
    check_cron_jobs(P_APP_LIST)
    check_failed_ssh(MY_IP,MAX_SSH)
    print('\n-------------------------\n\nESCANEO COMPLETADO\n\n-------------------------')
    return(0)

#Programa principal
if __name__=='__main__':
    main()
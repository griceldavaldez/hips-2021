import os, sys, subprocess
sys.path.append(os.path.abspath('../Configuraciones/'))
from preferencias import guardar_preferencias

from variables_globales import directorio_cuarentena

sys.path.append(os.path.abspath('../VerificarMd5sum/'))
from analisis_md5sum import verificar_md5sum

sys.path.append( os.path.abspath('../VerificarTmp/'))
from analisis_tmp import analisis_tmp

sys.path.append( os.path.abspath('../UsuariosConectados/'))
from usuarios_conectados import comprobar_usuarios_conectados

sys.path.append( os.path.abspath('../Correo/'))
from cola_correo import verificar_cola_correo

sys.path.insert(0, os.path.abspath('../AtaqueSmtp/'))
from analisis_ataque_smtp import analisis_ataque_smtp

sys.path.append( os.path.abspath('../Sniffers/'))
from analisis_promiscuo import analisis_promiscuo

sys.path.append( os.path.abspath('../Procesos/'))
from analisis_consumo import analisis_consumo_procesos

sys.path.append( os.path.abspath('../AccesosInvalidos/'))
from analisis_accesos_invalidos import analisis_directorio_invalido
from analisis_auths_failure import analisis_auths_failure
from analisis_failure_ssh import analisis_failure_ssh

sys.path.append( os.path.abspath('../Cron/'))
from analisis_cron import analsis_cron

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
    MAX_FUZZ = 5
    P_DIR = '/var/log/messages'

    if os.path.isfile(P_DIR) is not True:
        P_DIR = '/var/log/syslog'

    if os.path.isdir(directorio_cuarentena) is not True: # si no existe el directorio cuarentena, se crea
        p =subprocess.Popen("mkdir "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
    #se quitan los permisos de ejecucion para este directorio
    p =subprocess.Popen("chmod 664 "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True) 
    (output, err) = p.communicate()

    #si no se cargaron las configuraciones personalizadas, se cargan los valores por defecto
    if LIMIT_PROCESOS['uso_cpu'] is None or LIMIT_PROCESOS['uso_cpu'] == '': 
        LIMIT_PROCESOS['uso_cpu'] = general['MAXCPU']

    if LIMIT_PROCESOS['uso_memoria'] is None or LIMIT_PROCESOS['uso_memoria'] == '':
        LIMIT_PROCESOS['uso_memoria'] = general['MAXMEM']
  

    print("\n-------------------------\n\nESCANEANDO...\n\n-------------------------")
    verificar_cola_correo(MAX_Q_COUNT, ADMIN_DATOS)
    analisis_ataque_smtp(MAX_MAIL_PU, ADMIN_DATOS)
    analisis_promiscuo(P_DIR, APPS_PELIGROSAS, ADMIN_DATOS)
    analisis_consumo_procesos(LIMIT_PROCESOS, ADMIN_DATOS)
    comprobar_usuarios_conectados(ADMIN_DATOS)
    analisis_directorio_invalido(MI_IP,MAX_FUZZ, ADMIN_DATOS) #www.algo.com/noexiste
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
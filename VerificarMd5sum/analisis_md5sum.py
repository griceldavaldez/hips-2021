import subprocess, datetime, os, sys

sys.path.append( os.path.abspath('../Main/'))
from variables_globales import directorio_archivo_backup_hashes, md5_tmp_dir

sys.path.append( os.path.abspath('../Logs/'))
from logs import echo_alarmas_log, echo_prevencion_log

sys.path.append( os.path.abspath('../Correo/'))
from correo import enviar_correo

sys.path.append( os.path.abspath('../BaseDatos/'))
from dao import insertarAlarmaPrevencion
from modelos import AlarmaPrevencion

#Funcion: verificar_md5sum
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmaslog y echo_prevencionlog)
#Parametros:
#	MD5SUM_LIST	(list)lista con el hash producido mediante md5sum. Este se encuentra en el formato: hash dir
def verificar_md5sum(MD5SUM_LIST, admin):
    body = ''
    for mi_hash in MD5SUM_LIST:
        subprocess.Popen("echo "+mi_hash+" >> "+md5_tmp_dir, stdout=subprocess.PIPE, shell=True)
    p =subprocess.Popen("md5sum -c "+md5_tmp_dir, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if output.decode("utf-8")[-3:-1] != 'OK':
        body+=output.decode("utf-8")
        archivo_dir = output.decode("utf-8").split(" ")[0]
        echo_alarmas_log(fecha_hora, "MD5SUM alterada.El valor hash MD5SUM cambio para "+archivo_dir , 'verificar_md5sum',"")
        echo_prevencion_log(fecha_hora, 'Se envio un correo al administrador', 'El valor hash MD5SUM cambio para' +archivo_dir)
    if body != '':
        body = 'Hash MD5SUM modificada:\n\n' + body	
        enviar_correo(admin[0], admin[1],'Tipo de alerta: MD5SUM modificada',body)
        #print(body+"\n")
        obj_alarm_prev = AlarmaPrevencion()
        obj_alarm_prev.setFechaHora(fecha_hora)
        obj_alarm_prev.setTipoEscaneo("verificar_md5sum")
        obj_alarm_prev.setResultado("MD5SUM alterada.El valor hash MD5SUM cambio para "+archivo_dir)
        obj_alarm_prev.setAccion('Se envio un correo al administrador para dar aviso de lo ocurrido')
        insertarAlarmaPrevencion(obj_alarm_prev)
    subprocess.Popen("rm "+md5_tmp_dir, stdout=subprocess.PIPE, shell=True)


#Funcion: crear_md5sum_hash
#	Crea un hash md5sum utilizando la funcion md5sum para un archivo en especifico
#	Realiza una copia de seguridad del archivo en el directorio directorio_archivo_backup_hashes
#Parametros:
#	dir_str	(string) absolute path del archivo al cual queremos crearle un hash md5sum.
#Retorna:
#	(string) el hash producido
def crear_md5sum_hash(dir_str):
    p =subprocess.Popen("cp -R "+dir_str+" "+directorio_archivo_backup_hashes+"/", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p =subprocess.Popen("md5sum "+dir_str, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    var = str(output.decode("utf-8")[:-1])
    #var = var.strip(" {}".format(directorio_string))
    return  var 


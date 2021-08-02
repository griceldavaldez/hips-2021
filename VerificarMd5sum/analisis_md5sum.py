import subprocess
from variables_globales import directorio_archivo_backup_hashes, md5_tmp_dir
from Logs.logs import echo_alarmas_log, echo_prevencion_log
from Correo.correo import enviar_correo
from BaseDatos.dao import insertarAlarmaPrevencion
from BaseDatos.modelos import AlarmaPrevencion
from utils import get_fecha

#Funcion: verificar_md5sum
#	Guarda las alertas y las precauciones tomadas en los log correspondientes (Ver: echo_alarmas_log y echo_prevencion_log)
#Parametros:
#	MD5SUM_LIST	(list)lista con el hash producido mediante md5sum. Este se encuentra en el formato: hash dir
def verificar_md5sum(MD5SUM_LIST, admin):
    print("Inicia la funcion verificar_md5sum() \n", "\t\t Hora: " + get_fecha())
    body = ''
    print(MD5SUM_LIST)
    for mi_hash in MD5SUM_LIST:
        subprocess.Popen("echo "+mi_hash+" >> "+md5_tmp_dir, stdout=subprocess.PIPE, shell=True)
    p =subprocess.Popen("md5sum -c "+md5_tmp_dir, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #resultado = output.decode("utf-8")
    #print(resultado)
    #resultado = output.decode("utf-8")[-3:-1]
    #print(resultado)
    if "La suma no coincide" in output.decode("utf-8"):
        #####rint("Entro aca")
        body+=output.decode("utf-8")
        archivo_dir = output.decode("utf-8").split(" ")[0]
        echo_alarmas_log("MD5SUM alterada.El valor hash MD5SUM cambio para "+archivo_dir , 'verificar_md5sum',"")
        print("\t\t Resultado: " + "MD5SUM alterada.El valor hash MD5SUM cambio para "+archivo_dir)
        echo_prevencion_log('Se envio un correo al administrador', 'El valor hash MD5SUM cambio para' +archivo_dir)
        print("\t\t Accion: " + 'Se envio un correo al administrador')
    if body != '':
        body = 'Hash MD5SUM modificada:\n\n' + body	
        enviar_correo(admin[0], admin[1],'Tipo de alerta: MD5SUM modificada',body)
        obj_alarm_prev = AlarmaPrevencion(None, get_fecha(), "verificar_md5sum", body.replace("\n", " "), 'Se envio un correo al administrador para dar aviso de lo ocurrido')
        insertarAlarmaPrevencion(obj_alarm_prev)
    subprocess.Popen("rm "+md5_tmp_dir, stdout=subprocess.PIPE, shell=True)


#Funcion: crear_md5sum_hash
#	Crea un hash md5sum utilizando la funcion md5sum para un archivo en especifico
#	Realiza una copia de seguridad del archivo en el directorio directorio_archivo_backup_hashes
#Parametros:
#	dir_str	(string) ruta absoluta del archivo al cual queremos crearle un hash md5sum.
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


import psycopg2
import sys
sys.path.append("../Base-de-datos") 
from base_datos import conectar_postgres, cerrar_conexion
from dao import obtenerAplicacionPeligrosa, obtenerMd5sum, obtenerLimiteProceso, obtenerGeneral
#from modelos import AplicacionPeligrosa, General, LimiteProceso, Md5sum
import subprocess


def guardar_preferencias():
    preferencias = {'aplicacion_peligrosa':'','limite_proceso':[],'general':[], 'md5sum': [] }

    #Aqui cargamos las prefencias del usuario en cuanto a las aplicaciones maliciosas como sniffers.
    datos = obtenerAplicacionPeligrosa()
    dato_string = ''
    for fila in datos:
        #fila= AplicacionPeligrosa(fila)
        dato_string += fila.getNombreSniffer() +'|'
    if(dato_string != ''):
        preferencias['aplicacion_peligrosa'] = dato_string[:-1] # le quitamos el ultimo '|'

    #Aqui cargamos las prefencias del usuario en cuanto al uso máximo de CPU, memoria RAM, y máximo tiempo de vida de los procesos.
    datos = obtenerLimiteProceso()
    dato_lista = []
    for fila in datos:
        #fila = LimiteProceso(fila)
        dato_lista.append({'nombre_proceso':fila.getNombreProceso(), 'uso_cpu':fila.getUsoCpu(), 'uso_memoria':fila.getUsoMemoria(), 'tiempo_maximo_ejecucion':fila.getTiempoMaximoEjecucion()})
    preferencias['limite_proceso'] = dato_lista

    #Aqui cargamos las preferencias del usuario en cuanto a  informaciones generales como ip, correo, contrasenha y algunos valores por defecto.
    datos = obtenerGeneral()
    dato_lista = []
    for fila in datos:
        dato_lista.append({'ip':fila.getIP(),'correo_admin':fila.getCorreo(),'pass_admin':fila.getContrasenhaCorreo(),'MAXCPU':fila.getUsoCpuPorDefecto(),'MAXMEM':fila.getUsoMemoriaPorDefecto(),'intento_maximo_ssh': fila.getIntentoMaximoSSH(),'correo_maximo_por_usuario':fila.getCorreoMaximoPorUsuario(),'cola_maxima_correo': fila.getColaMaximaCorreo()})
    preferencias['general'] = dato_lista

    #Aqui cargamos las preferencias en cuanto a los directorios junto con sus hashes MD5SUM.
    dbConexion, dbCursor = conectar_postgres()
    md5sum_query = "SELECT directorio FROM md5sum WHERE hash IS NULL OR hash=\'\'"
    dbCursor.execute(md5sum_query)
    datos = dbCursor.fetchall()
    fue_actualizado = False
    for fila in datos:
        print("Directorio: ", fila[0])
        update_md5sum = 'UPDATE md5sum SET hash=\''+crear_md5sum_hash(fila[0])+'\' WHERE directorio=\''+ fila[0]+'\';'
        dbCursor.execute(update_md5sum)
        fue_actualizado = True
    dbConexion.commit()
    if fue_actualizado is not True: #si no fue actualizado, directamente se hace un select para recuperar los hashes
        datos = obtenerMd5sum('', 'hash')
        dato_lista = []
        for fila in datos:
            #fila = Md5sum(fila)
            dato_lista.append(fila.getHash())
        preferencias['md5sum']= dato_lista
    else: #si fue actualizado, se cierra la conexion y se vuelve a abrir para obtener los hashes
        cerrar_conexion(dbConexion, dbCursor)
        datos = obtenerMd5sum('', 'hash')
        dato_lista = []
        for fila in datos:
            #fila = Md5sum(fila)
            dato_lista.append(fila.getHash())
        preferencias['md5sum']= dato_lista
    return preferencias

#Funcion: crear_md5sum_hash
#Crea un hash md5sum utilizando la funcion md5sum para un archivo en especifico
#Realiza una copia de seguridad del archivo en el directorio directorio_archivo_backup_hashes
#Parametros:
#	dir_str	(string)absolute path del archivo al cual queremos crearle un hash md5sum.
#Retorna:
#	(string) el hash producido
directorio_archivo_backup_hashes = '/etc/backup_hashes_files'
def crear_md5sum_hash(directorio_string):
	global directorio_archivo_backup_hashes
	p =subprocess.Popen("cp -R "+directorio_string+" "+directorio_archivo_backup_hashes+"/", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p =subprocess.Popen("md5sum "+directorio_string, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	print('crear_md5sum_hash: output.decode("utf-8")', output.decode("utf-8"))
	#print('\n')
	print('crear_md5sum_hash: output.decode("utf-8")[:-1]',output.decode("utf-8")[:-1])
	return output.decode("utf-8")[:-1]
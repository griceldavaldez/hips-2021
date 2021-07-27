
from BaseDatos.base_datos import conectar_postgres, cerrar_conexion
from BaseDatos.dao import actualizarMd5sum, obtenerAplicacionPeligrosa, obtenerMd5sum, obtenerLimiteProceso, obtenerGeneral
from BaseDatos.modelos import Md5sum
from Main.variables_globales import directorio_archivo_backup_hashes
import subprocess

#Funcion que guarda las preferencias/configuraciones del administrador en una lista
#Trae las configuraciones de la base de datos postgres
def guardar_preferencias():
    preferencias = {'aplicacion_peligrosa':'','limite_proceso':[],'general':[], 'md5sum': [] }

    #Aqui cargamos las prefencias del usuario en cuanto a las aplicaciones maliciosas como sniffers.
    datos = obtenerAplicacionPeligrosa()
    dato_string = ''
    for i in range(0, len(datos)):
        dato_string += datos[i].getNombreSniffer() +'|'
    if(dato_string != ''):
        preferencias['aplicacion_peligrosa'] = dato_string[:-1] # le quitamos el ultimo '|'

    #Aqui cargamos las prefencias del usuario en cuanto al uso máximo de CPU, memoria RAM, y máximo tiempo de vida de los procesos.
    datos = obtenerLimiteProceso()
    dato_lista = []
    for i in range (0, len(datos)):
        dato_lista.append({'nombre_proceso':datos[i].getNombreProceso(), 'uso_cpu':datos[i].getUsoCpu(), 'uso_memoria':datos[i].getUsoMemoria(), 'tiempo_maximo_ejecucion':datos[i].getTiempoMaximoEjecucion()})
    preferencias['limite_proceso'] = dato_lista

    #Aqui cargamos las preferencias del usuario en cuanto a  informaciones generales como ip, correo, contrasenha y algunos valores por defecto.
    datos = obtenerGeneral()
    dato_lista = []
    dato_lista.append({'ip':datos.getIP(),'correo_admin':datos.getCorreo(),'pass_admin':datos.getContrasenhaCorreo(),'MAXCPU':datos.getUsoCpuPorDefecto(),'MAXMEM':datos.getUsoMemoriaPorDefecto(),'intento_maximo_ssh': datos.getIntentoMaximoSSH(),'correo_maximo_por_usuario':datos.getCorreoMaximoPorUsuario(),'cola_maxima_correo': datos.getColaMaximaCorreo()})
    preferencias['general'] = dato_lista

    #Aqui cargamos las preferencias en cuanto a los directorios junto con sus hashes MD5SUM.
    dbConexion, dbCursor = conectar_postgres()
    md5sum_query = "SELECT directorio FROM md5sum WHERE hash IS NULL OR hash=' '"
    dbCursor.execute(md5sum_query)
    datos = dbCursor.fetchall()
    fue_actualizado = False
    for fila in datos:
        obj_md5sum = Md5sum()
        obj_md5sum.setDirectorio(fila[0])
        obj_md5sum.setHash(str(crear_md5sum_hash(fila[0])))
        actualizarMd5sum(obj_md5sum)
        fue_actualizado = True
    if fue_actualizado is not True: #si no fue actualizado, directamente se hace un select para recuperar los hashes
        datos = obtenerMd5sum('', 'hash')
        dato_lista = []
        for i in range (0, len(datos)):
            dato_lista.append(datos[i].getHash())
        preferencias['md5sum']= dato_lista
    else: #si fue actualizado, se cierra la conexion y se vuelve a abrir para obtener los hashes
        cerrar_conexion(dbConexion, dbCursor)
        datos = obtenerMd5sum('', 'hash')
        dato_lista = []
        for i in range (0, len(datos)):
            dato_lista.append(datos[i].getHash())
        preferencias['md5sum']= dato_lista
    return preferencias

#Funcion: crear_md5sum_hash
#Crea un hash md5sum utilizando la funcion md5sum para un archivo en especifico
#Realiza una copia de seguridad del archivo en el directorio directorio_archivo_backup_hashes
#Parametros:
#	dir_str	(string)absolute path del archivo al cual queremos crearle un hash md5sum.
#Retorna:
#	(string) el hash producido
def crear_md5sum_hash(directorio_string):
    global directorio_archivo_backup_hashes
    p =subprocess.Popen("cp -R "+directorio_string+" "+directorio_archivo_backup_hashes+"/", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p =subprocess.Popen("md5sum "+directorio_string, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #print('crear_md5sum_hash: output.decode("utf-8")', output.decode("utf-8"))
    #print('\n')
    #print('crear_md5sum_hash: output.decode("utf-8")[:-1]',output.decode("utf-8")[:-1])
    var = str(output.decode("utf-8")[:-1])
    var = var.strip(" {}".format(directorio_string))
    #return output.decode("utf-8")[:-1]
    return var

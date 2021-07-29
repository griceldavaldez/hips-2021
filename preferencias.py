from BaseDatos.dao import obtenerAplicacionPeligrosa, obtenerMd5sum, obtenerLimiteProceso, obtenerGeneral

#Funcion: guardar_preferencias
#	Guarda las preferencias/configuraciones del administrador en una lista
#	Trae las configuraciones de la base de datos postgres
#Retorna:
#	(list) con las configuraciones obtenidas
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
    datos = obtenerMd5sum()
    dato_lista = []
    for i in range (0, len(datos)):
        dato_lista.append(datos[i].getHash())
    preferencias['md5sum']= dato_lista
    return preferencias



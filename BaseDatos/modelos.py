
#Clases que corresponden a las tablas de la base de datos postgres

#tabla general
class General(object):
    #Constructor de la clase
    def __init__(self, ip4, admin_e, passw, max_cpu, max_mem, max_ssh, max_pu, max_eq):
        self.ip = ip4
        self.correo = admin_e
        self.contrasenha_correo = passw
        self.uso_cpu_por_defecto = max_cpu
        self.uso_memoria_por_defecto = max_mem
        self.intento_maximo_ssh = max_ssh
        self.correo_maximo_por_usuario = max_pu
        self.cola_maxima_correo = max_eq
    #Metodos para obtener los atributos de la clase
    def getIP(self):
        return self.ip
    def getCorreo (self):
        return self.correo
    def getContrasenhaCorreo(self):
        return self.contrasenha_correo
    def getUsoCpuPorDefecto(self):
        return self.uso_cpu_por_defecto
    def getUsoMemoriaPorDefecto(self):
        return self.uso_memoria_por_defecto
    def getIntentoMaximoSSH(self):
        return self.intento_maximo_ssh
    def getCorreoMaximoPorUsuario(self):
        return self.correo_maximo_por_usuario
    def getColaMaximaCorreo(self):
        return self.cola_maxima_correo
    #Metodos para setear los atributos de la clase
    def setIP(self, ip4):
        self.ip = ip4
    def setCorreo (self, email):
        self.correo = email
    def setContrasenhaCorreo(self, passw):
        self.contrasenha_correo = passw
    def setUsoCpuPorDefecto(self, max_cpu):
        self.uso_cpu_por_defecto = max_cpu
    def setUsoMemoriaPorDefecto(self, max_mem):
        self.uso_memoria_por_defecto = max_mem
    def setIntentoMaximoSSH(self, max_ssh):
        self.intento_maximo_ssh = max_ssh
    def setCorreoMaximoPorUsuario(self, max_email_u):
        self.correo_maximo_por_usuario = max_email_u
    def setColaMaximaCorreo(self, q_max_email):
        self.cola_maxima_correo = q_max_email


#tabla md5sum
class Md5sum(object):
    #Constructor de la clase
    def __init__(self, dir, hash):
        self.directorio = dir
        self.hash = hash
    #Metodos para obtener los atributos de la clase
    def getDirectorio(self):
        return self.directorio
    def getHash(self):
        return self.hash
    #Metodos para setear los atributos de la clase
    def setDirectorio(self, dir):
        self.directorio = dir
    def setHash(self, hash):
        self.hash = hash 


#tabla aplicacion_peligrosa
class AplicacionPeligrosa(object): 
    #Constructor de la clase
    def __init__(self, app_pelig):
        self.nombre_sniffer = app_pelig
    #Metodos para obtener los atributos de la clase
    def getNombreSniffer(self):
        return self.nombre_sniffer
    #Metodos para setear los atributos de la clase
    def setNombreSniffer(self, name):
        self.nombre_sniffer = name


#tabla limite_procesos
class LimiteProceso(object):
    #Constructor de la clase
    def __init__(self, nombre, max_cpu, max_mem, max_time):
        self.nombre_proceso = nombre
        self.uso_cpu = max_cpu
        self.uso_memoria = max_mem
        self.tiempo_maximo_ejecucion = max_time
    #Metodos para obtener los atributos de la clase
    def getNombreProceso(self):
        return self.nombre_proceso 
    def getUsoCpu(self):
        return self.uso_cpu  
    def getUsoMemoria(self):
        return self.uso_memoria
    def getTiempoMaximoEjecucion(self):
        return self.tiempo_maximo_ejecucion
    #Metodos para setear los atributos de la clase
    def setNombreProceso(self, name_p):
        self.nombre_proceso = name_p
    def setUsoCpu(self, cpu):
        self.uso_cpu = cpu
    def setUsoMemoria(self, mem):
        self.uso_memoria = mem
    def setTiempoMaximoEjecucion(self, time_max):
        self.tiempo_maximo_ejecucion = time_max


#tabla alarma_prevencion
class AlarmaPrevencion(object):
    #Constructor de la clase
    def __init__(self, timestamp, t_scan, res, acc):
        self.fecha_hora = timestamp
        self.tipo_escaneo = t_scan
        self.resultado = res
        self.accion = acc
    #Metodos para obtener los atributos de la clase
    def getFechaHora(self):
        return self.fecha_hora
    def getTipoEscaneo(self):
        return self.tipo_escaneo
    def getResultado(self):
        return self.resultado
    def getAccion(self):
        return self.accion
    #Metodos para setear los atributos de la clase
    def setFechaHora(self, date):
        self.fecha_hora = date
    def setTipoEscaneo(self, t_scan):
        self.tipo_escaneo = t_scan
    def setResultado(self, res):
        self.resultado = res
    def setAccion(self, acc):
        self.accion = acc




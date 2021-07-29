from BaseDatos.modelos import General, Md5sum, LimiteProceso, AlarmaPrevencion, AplicacionPeligrosa
from BaseDatos.base_datos import conectar_postgres, cerrar_conexion
import psycopg2, subprocess
#from VerificarMd5sum.analisis_md5sum import crear_md5sum_hash
from variables_globales import directorio_archivo_backup_hashes

#CRUD PARA LA CLASE GENERAL
#Lista las configuraciones generales del administrador
def obtenerGeneral():
    try:
        dbConexion, dbCursor = conectar_postgres()
        select_general = "SELECT * FROM general;"
        dbCursor.execute(select_general)
        datos = dbCursor.fetchone()
        obj_gral = General(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7])
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerGeneral()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return obj_gral

#Actualiza/Modifica las configuraciones generales del administrador. Recibe como parametro un obj General
def actualizarGeneral(obj_gral):
    try:
        dbConexion, dbCursor = conectar_postgres()
        update_general = "UPDATE general SET ip='{}',correo='{}',contrasenha_correo='{}',uso_cpu_por_defecto={},uso_memoria_por_defecto={},intento_maximo_ssh={},correo_maximo_por_usuario={},cola_maxima_correo={};"
        dbCursor.execute(update_general.format(obj_gral.getIP(),obj_gral.getCorreo(),obj_gral.getContrasenhaCorreo(),obj_gral.getUsoCpuPorDefecto(),obj_gral.getUsoMemoriaPorDefecto(),obj_gral.getIntentoMaximoSSH(),obj_gral.getCorreoMaximoPorUsuario(),obj_gral.getColaMaximaCorreo()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion actualizarGeneral()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#CRUD PARA LA CLASE Md5SUM
#Lista todos los registros de la tabla md5sum 
def obtenerMd5sum():
    try:
        dbConexion, dbCursor = conectar_postgres()
        select_md5sum = "SELECT * FROM md5sum;"
        dbCursor.execute(select_md5sum)
        datos = dbCursor.fetchall()
        datos_lista = []
        for i in datos:
            obj_md5sum = Md5sum(i[0], i[1])
            datos_lista.append(obj_md5sum)
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return datos_lista

#Inserta los directorios junto con sus hashes en la tabla md5sum. Recibe como parametro el obj Md5sum.directorio
def insertarMd5sum(obj_md5sum):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_md5sum = "INSERT INTO md5sum(directorio, hash) values('{}', '{}');"
        dbCursor.execute(insert_md5sum.format(obj_md5sum.getDirectorio(), crear_md5sum_hash(obj_md5sum.getDirectorio())))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Elimina un registro de la tabla md5sum dado su Md5sum.directorio
def eliminarMd5sum(obj_md5sum):
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_md5sum =  "DELETE FROM md5sum where directorio = '{}';"
        dbCursor.execute(delete_md5sum.format(obj_md5sum.getDirectorio()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion eliminarMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#CRUD PARA LA CLASE AplicacionPeligrosa
#Lista todas las aplicaciones peligrosas como sniffers
def obtenerAplicacionPeligrosa():
    try:
        dbConexion, dbCursor = conectar_postgres()
        select_aplicacion_peligrosa =  "SELECT * FROM aplicacion_peligrosa;"
        dbCursor.execute(select_aplicacion_peligrosa)
        datos = dbCursor.fetchall()
        lista_datos = []
        for fila in datos:
            obj_app_pelig = AplicacionPeligrosa(fila[0])
            lista_datos.append(obj_app_pelig)
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerAplicacionPeligrosa()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return lista_datos

#Inserta aplicaciones peligrosas como sniffers
def insertarAplicacionPeligrosa(obj_app_pelig):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_aplicacion_peligrosa = "INSERT INTO aplicacion_peligrosa(nombre_sniffer) values('{}');"
        dbCursor.execute(insert_aplicacion_peligrosa.format(obj_app_pelig.getNombreSniffer()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarAplicacionPeligrosa()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Elimina un registro de la tabla aplicacion_peligrosa. Recibe como parametro el obj AplicacionPeligrosa.nombre_sniffer
def eliminarAplicacionPeligrosa(obj_app_pelig):
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_aplicacion_peligrosa =  "DELETE FROM aplicacion_peligrosa where nombre_sniffer = '{}' ;"
        dbCursor.execute(delete_aplicacion_peligrosa.format(obj_app_pelig.getNombreSniffer()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion eliminarAplicacionPeligrosa()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#CRUD PARA LA CLASE LimiteProceso
#Lista las configuraciones sobre los limites de los procesos
def obtenerLimiteProceso():
    try:
        dbConexion, dbCursor = conectar_postgres()
        select_limite_proceso =  "SELECT * FROM limite_proceso;"
        dbCursor.execute(select_limite_proceso)
        datos = dbCursor.fetchall()
        lista_datos = []
        for fila in datos:
            obj_lim_process = LimiteProceso(fila[0],fila[1],fila[2],fila[3])
            lista_datos.append(obj_lim_process)
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerLimiteProceso()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return lista_datos

#Inserta las configuraciones sobre los limites de los procesos 
def insertarLimiteProceso(obj_lim_process):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_limite_proceso = "INSERT INTO limite_proceso(nombre_proceso,uso_cpu,uso_memoria,tiempo_maximo_ejecucion) values('{}',{},{},{});"
        dbCursor.execute(insert_limite_proceso.format(obj_lim_process.getNombreProceso() , obj_lim_process.getUsoCpu(), obj_lim_process.getUsoMemoria(), obj_lim_process.getTiempoMaximoEjecucion()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarLimiteProceso()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Lista las configuraciones sobre los limites de los procesos dado su nombre. Recibe un obj LimiteProceso
def actualizarLimiteProceso(obj_lim_process):
    try:
        dbConexion, dbCursor = conectar_postgres()
        update_limite_proceso = "UPDATE limite_proceso SET "
        where = " where nombre_proceso = '{}';"
        nombre_proceso = obj_lim_process.getNombreProceso() #No debe ser null
        if obj_lim_process.getUsoCpu() is not None:
            campo = "uso_cpu = {};"
            query = update_limite_proceso + campo + where
            dbCursor.execute(query.format(obj_lim_process.getUsoCpu(), nombre_proceso))
        if obj_lim_process.getUsoMemoria() is not None:
            campo = "uso_memoria = {} "
            query = update_limite_proceso + campo + where
            dbCursor.execute(query.format(obj_lim_process.getUsoMemoria(), nombre_proceso))
        if obj_lim_process.getTiempoMaximoEjecucion()  is not None:
            campo = "tiempo_maximo_ejecucion = {} "
            query = update_limite_proceso + campo + where
            dbCursor.execute(query.format(obj_lim_process.getTiempoMaximoEjecucion(), nombre_proceso))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion actualizarLimiteProceso()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Elimina un registros de la tabla limite_proceso dado LimiteProceso.nombre_proceso
def eliminarLimiteProceso(obj_lim_process):
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_limite_proceso =  "DELETE FROM limite_proceso where nombre_proceso = '{}';"
        dbCursor.execute(delete_limite_proceso.format(obj_lim_process.getNombreProceso()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion eliminarLimiteProceso()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#CRUD PARA LA CLASE AlarmaPrevencion
#Lista las alarmas y acciones realizadas
def obtenerAlarmaPrevencion():
    try:
        dbConexion, dbCursor = conectar_postgres()
        select_alarma_prevencion = "SELECT * from alarma_prevencion;"
        dbCursor.execute(select_alarma_prevencion)
        datos = dbCursor.fetchall()
        lista_datos = []
        for i in datos:
            obj_alarm_prev = AlarmaPrevencion(i[0], i[1], i[2], i[3])
            lista_datos.append(obj_alarm_prev)    
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerAlarmaPrevencion()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return lista_datos

#Inserta las alarmas registradas con sus acciones/prevenciones. Solo a nivel de codigo se usa
def insertarAlarmaPrevencion(obj_alarm_prev):
    try:
        dbConexion, dbCursor = conectar_postgres()
        
        insert_alarma_prevencion = "INSERT INTO alarma_prevencion(fecha_hora,tipo_escaneo,resultado,accion) values('{}','{}','{}','{}');"
        dbCursor.execute(insert_alarma_prevencion.format(obj_alarm_prev.getFechaHora(), obj_alarm_prev.getTipoEscaneo(),obj_alarm_prev.getResultado(), obj_alarm_prev.getAccion()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarAlarmaPrevencion()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)



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


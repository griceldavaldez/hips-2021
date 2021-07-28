from modelos import General, Md5sum, LimiteProceso, AlarmaPrevencion, AplicacionPeligrosa
from base_datos import conectar_postgres, cerrar_conexion
import psycopg2

#CRUD PARA LA CLASE GENERAL
#Lista las configuraciones generales del administrador
def obtenerGeneral():
    try:
        dbConexion, dbCursor = conectar_postgres()
        select_general = "SELECT * FROM general;"
        dbCursor.execute(select_general)
        datos = dbCursor.fetchone()
        obj_gral = General()
        obj_gral.setIP(datos[0])
        obj_gral.setCorreo(datos[1])
        obj_gral.setContrasenhaCorreo(datos[2])
        obj_gral.setUsoCpuPorDefecto(datos[3])
        obj_gral.setUsoMemoriaPorDefecto (datos[4])
        obj_gral.setIntentoMaximoSSH(datos[5])
        obj_gral.setCorreoMaximoPorUsuario(datos[6])
        obj_gral.setColaMaximaCorreo(datos[7])
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerGeneral()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return obj_gral

#Inserta las configuraciones generales del administrador
def insertarGeneral(obj_gral):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_general = "INSERT INTO general(ip,correo,contrasenha_correo,uso_cpu_por_defecto,uso_memoria_por_defecto,intento_maximo_ssh,correo_maximo_por_usuario,cola_maxima_correo) "
        insert_general += "values('{}','{}','{}',{},{},{},{});"
        ip = obj_gral.getIP()
        correo = obj_gral.getCorreo()
        contrasenha_correo = obj_gral.getContrasenhaCorreo()
        uso_cpu_por_defecto = obj_gral.getUsoCpuPorDefecto()
        uso_memoria_por_defecto = obj_gral.getUsoMemoriaPorDefecto()
        intento_maximo_ssh = obj_gral.getIntentoMaximoSSH()
        correo_maximo_por_usuario = obj_gral.getCorreoMaximoPorUsuario()
        cola_maxima_correo = obj_gral.getColaMaximaCorreo()
        dbCursor.execute(insert_general.format(ip,correo,contrasenha_correo,uso_cpu_por_defecto,uso_memoria_por_defecto,intento_maximo_ssh,correo_maximo_por_usuario,cola_maxima_correo))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarGeneral(obj_gral)")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Actualiza/Modifica las configuraciones generales del administrador
def actualizarGeneral(obj_gral):
    try:
        dbConexion, dbCursor = conectar_postgres()
        update_general = "UPDATE general SET "
        if obj_gral.getIP() is not None:
            update_campo = update_general +  "ip='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getIP()))
        if obj_gral.getCorreo() is not None:
            update_campo = update_general +  "correo='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getCorreo()))
        if obj_gral.getContrasenhaCorreo() is not None:
            update_campo = update_general +  "contrasenha_correo='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getContrasenhaCorreo()))
        if obj_gral.getUsoCpuPorDefecto() is not None:
            update_campo = update_general +  "uso_cpu_por_defecto='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getUsoCpuPorDefecto()))
        if obj_gral.getUsoMemoriaPorDefecto() is not None:
            update_campo = update_general +  "uso_memoria_por_defecto='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getUsoMemoriaPorDefecto()))
        if obj_gral.getIntentoMaximoSSH() is not None:
            update_campo = update_general +  "intento_maximo_ssh='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getIntentoMaximoSSH()))
        if obj_gral.getCorreoMaximoPorUsuario() is not None:
            update_campo = update_general +  "correo_maximo_por_usuario='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getCorreoMaximoPorUsuario()))
        if obj_gral.getColaMaximaCorreo() is not None:
            update_campo = update_general +  "cola_maxima_correo='{}';"
            dbCursor.execute(update_campo.format(obj_gral.getColaMaximaCorreo()))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion actualizarGeneral(obj_gral)")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Elimina las configuraciones del administrador
def eliminarGeneral():
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_general = "DELETE FROM general;"
        dbCursor.execute(delete_general)
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion eliminarGeneral()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)


#CRUD PARA LA CLASE Md5SUM
#Lista los registros de la tabla md5sum segun el directorio y/o hash
def obtenerMd5sum(dir, hash):
    try:
        dbConexion, dbCursor = conectar_postgres()
        filtro = ''
        if dir == 'directorio' and hash != 'hash':
            filtro = 'directorio'
        if hash == 'hash' and dir != 'directorio':
            filtro = 'hash'
        filtro = str(filtro)
        filtro = filtro.replace(' ', '')
        filtro = filtro.replace('[', '')
        filtro = filtro.replace(']', '')
        filtro = filtro.replace("'", '')  
        if filtro == '':
            select_md5sum = "SELECT * FROM md5sum;"
            dbCursor.execute(select_md5sum)
            datos = dbCursor.fetchall()
            datos_lista = []
            for fila in datos:
                obj_md5sum = Md5sum()
                obj_md5sum.setDirectorio(fila[0])
                obj_md5sum.setHash(fila[1])
                datos_lista.append(obj_md5sum)
        else:
            select_md5sum =  "SELECT " + str(filtro) + " FROM md5sum;"
            dbCursor.execute(select_md5sum)
            datos = dbCursor.fetchall()
            datos_lista = []
            for fila in datos:
                obj_md5sum = Md5sum()
                if hash == 'hash':
                    obj_md5sum.setHash(fila[0])
                if dir == 'directorio':
                    obj_md5sum.setDirectorio(fila[0])
                datos_lista.append(obj_md5sum)
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return datos_lista

#Inserta los directorios de los cuales vamos a generar los hashes
def insertarMd5sum(obj_md5sum):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_md5sum = "INSERT INTO md5sum(directorio) values('{}');" #solo se inserta el directorio, en otra parte se carga el hash
        directorio = obj_md5sum.getDirectorio()
        dbCursor.execute(insert_md5sum.format(directorio))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

'''def insertarMd5sum(obj_md5sum):
    dbConexion, dbCursor = conectar_postgres()
    obj_md5sum = Md5sum(obj_md5sum) #hacemos cast para que pueda reconocerlo como objeto 
    directorio = obj_md5sum.getDirectorio()
    hash = obj_md5sum.getHash()
    insert_md5sum = "INSERT INTO md5sum(directorio, hash) values({}, {})"
    dbCursor.execute(insert_md5sum.format(directorio, hash))
    dbConexion.commit()
    cerrar_conexion(dbConexion, dbCursor)'''

#Actualiza/Modifica los hashes segun corresponda a un directorio dado
def actualizarMd5sum(obj_md5sum):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_md5sum = "UPDATE md5sum SET hash = '{}' where directorio = '{}';"
        directorio = obj_md5sum.getDirectorio()
        hash = obj_md5sum.getHash()
        dbCursor.execute(insert_md5sum.format(hash, directorio))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion actualizarMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Elimina todos los registros de la tabla md5sum
def eliminarMd5sum():
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_md5sum =  "DELETE FROM md5sum;"
        dbCursor.execute(delete_md5sum)
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
            obj_app_pelig = AplicacionPeligrosa()
            obj_app_pelig.setNombreSniffer(fila[0])
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
        nombre_sniffer = obj_app_pelig.getNombreSniffer()
        dbCursor.execute(insert_aplicacion_peligrosa.format(nombre_sniffer))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarAplicacionPeligrosa()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Elimina todos los registros de la tabla aplicacion_peligrosa
def eliminarAplicacionPeligrosa():
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_aplicacion_peligrosa =  "DELETE FROM aplicacion_peligrosa;"
        dbCursor.execute(delete_aplicacion_peligrosa)
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
            obj_lim_process = LimiteProceso()
            obj_lim_process.setNombreProceso(fila[0])
            obj_lim_process.setUsoCpu(fila[1])
            obj_lim_process.setUsoMemoria(fila[2])
            obj_lim_process.setTiempoMaximoEjecucion(fila[3])
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
        nombre_proceso = obj_lim_process.getNombreProceso() 
        uso_cpu = obj_lim_process.getUsoCpu()
        uso_memoria = obj_lim_process.getUsoMemoria()
        tiempo_maximo_ejecucion = obj_lim_process.getTiempoMaximoEjecucion()
        dbCursor.execute(insert_limite_proceso.format(nombre_proceso, uso_cpu, uso_memoria, tiempo_maximo_ejecucion))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarLimiteProceso()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#Lista las configuraciones sobre los limites de los procesos dado su nombre
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

#Elimina todos los registros de la tabla limite_proceso
def eliminarLimiteProceso():
    try:
        dbConexion, dbCursor = conectar_postgres()
        delete_limite_proceso =  "DELETE FROM limite_proceso;"
        dbCursor.execute(delete_limite_proceso)
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion eliminarLimiteProceso()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

#CRUD PARA LA CLASE AlarmaPrevencion
#Lista las alarmas y acciones realizadas
def obtenerAlarmaPrevencion(filtro_tipo_escaneo):
    try:
        dbConexion, dbCursor = conectar_postgres()
        tieneFiltro = False
        if len(filtro_tipo_escaneo) == 0:
            select_alarma_prevencion = "SELECT * from alarma_prevencion;"
        else:
            select_alarma_prevencion = "SELECT * from alarma_prevencion where tipo_escaneo = '{}';"
            tieneFiltro = True
        if tieneFiltro is not True:
            dbCursor.execute(select_alarma_prevencion)
        else:
            dbCursor.execute(select_alarma_prevencion.format(filtro_tipo_escaneo))
        datos = dbCursor.fetchall()
        lista_datos = []
        for fila in datos:
            obj_alarm_prev = AlarmaPrevencion()
            obj_alarm_prev.setFechaHora(fila[0])
            obj_alarm_prev.setTipoEscaneo(fila[1])
            obj_alarm_prev.setResultado(fila[2])
            obj_alarm_prev.setAccion(fila[3])
            lista_datos.append(obj_alarm_prev)    
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerAlarmaPrevencion()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return lista_datos

#Inserta las alarmas registradas con sus acciones/prevenciones
def insertarAlarmaPrevencion(obj_alarm_prev):
    try:
        dbConexion, dbCursor = conectar_postgres()
        insert_alarma_prevencion = "INSERT INTO alarma_prevencion(fecha_hora,tipo_escaneo,resultado,accion) values('{}','{}','{}','{}');"
        fecha_hora = obj_alarm_prev.getFechaHora()
        tipo_escaneo = obj_alarm_prev.getTipoEscaneo()
        resultado = obj_alarm_prev.getResultado()
        accion = obj_alarm_prev.getAccion()
        dbCursor.execute(insert_alarma_prevencion.format(fecha_hora,tipo_escaneo,resultado,accion))
        dbConexion.commit()
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion insertarAlarmaPrevencion()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)

from psycopg2.sql import NULL
from modelos import General, Md5sum, LimiteProceso, AlarmaPrevencion, AplicacionPeligrosa
from base_datos import conectar_postgres, cerrar_conexion, datos_conexion_postgres
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
        #obj_gral = General(obj_gral)
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
        #obj_gral = General(obj_gral)
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


#CRUD PARA LA CLASE Md5sum
#Lista los registros de la tabla md5sum segun el directorio y/o hash
def obtenerMd5sum(dir, hash):
    try:
        dbConexion, dbCursor = conectar_postgres()
        filtro = []
        if dir == 'directorio':
            filtro.append('directorio')
        if hash == 'hash':
            filtro.append('hash')
        filtro = str(filtro)
        filtro = filtro.replace(' ', '')
        filtro = filtro.replace('[', '')
        filtro = filtro.replace(']', '')
        filtro = filtro.replace("'", '')
        print(str(filtro))
        if len(filtro) == 0:
            select_md5sum = "SELECT * FROM md5sum;"
        else:
            select_md5sum =  "SELECT " + str(filtro) + " FROM md5sum;"
        dbCursor.execute(select_md5sum)
        datos = dbCursor.fetchall()
        obj_md5sum = Md5sum()
        datos_lista = []
        for fila in datos:
            obj_md5sum.setDirectorio(fila[0])
            obj_md5sum.setHash(fila[1])
            datos_lista.append(obj_md5sum)
    except psycopg2.DatabaseError as error:
        print("Ocurrio un error al ejecutar la funcion obtenerMd5sum()")
        print("Motivo:  ", error)
    finally:
        cerrar_conexion(dbConexion, dbCursor)
    return datos_lista

















def insertarMd5sum(obj_md5sum):
    dbConexion, dbCursor = conectar_postgres()
    obj_md5sum = Md5sum(obj_md5sum) #hacemos cast para que pueda reconocerlo como objeto 
    directorio = obj_md5sum.getDirectorio()
    hash = obj_md5sum.getHash()
    insert_md5sum = "INSERT INTO md5sum(directorio, hash) values({}, {})"
    dbCursor.execute(insert_md5sum.format(directorio, hash))
    dbConexion.commit()
    cerrar_conexion(dbConexion, dbCursor)
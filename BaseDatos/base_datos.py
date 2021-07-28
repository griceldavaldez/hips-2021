import psycopg2, os

#Lee de un archivo los datos para la conexion a la base de datos
#Retorna: nombre de la base de datos, usuario y contrasenha
def datos_conexion_postgres():
    dir = os.path.abspath('../BaseDatos/')
    archivo = open(dir + "/conexion_postgres.txt", "r") #FIJARSE SI HACE FALTA MODIFICAR RUTA
    lineas = archivo.readlines()
    for i in range(0, len(lineas)):
        lineas[i] = lineas[i].strip('\n') 
    archivo.close()
    return lineas

#Realiza la conexion a la base de datos postgres
#Retorna: dbConexion, dbCursor
def conectar_postgres():
    nombre_bd, usuario_bd, contrasenha_bd = datos_conexion_postgres()
    try:
        dbConexion = psycopg2.connect(database=nombre_bd, user=usuario_bd, password=contrasenha_bd)
        dbCursor = dbConexion.cursor()
    except psycopg2.DatabaseError as error:
        print("No se pudo establecer la conexion a la base de datos postgres")
        print("Motivo:  ", error)
    return dbConexion, dbCursor

#Cierra la conexion a la base de datos
def cerrar_conexion(dbConexion, dbCursor):
    dbCursor.close()
    dbConexion.close()

        


    


    

    




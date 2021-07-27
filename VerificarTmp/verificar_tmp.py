
from Cuarentena.cuarentena import enviar_a_cuarentena
import subprocess 

def analisis_tmp():
        buscar_shells("/tmp")
        buscar_scripts("/tmp")



def buscar_shells(DIR):
        msg = ''
        p =subprocess.Popen("find "+DIR+" -type f", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        archivos_tmp_string = output.decode("utf-8")
        for linea in archivos_tmp_string.splitlines():
                cat =subprocess.Popen("cat "+ linea +" | grep '#!'", stdout=subprocess.PIPE, shell=True)
                (output, err) = cat.communicate()
                txt = output.decode("utf-8")
                if(txt !=''):
                        msg += 'Se encontró un posible script de shell en:' + linea + '\ n'
                        enviar_a_cuarentena(linea)
                        print ('Se encontró un posible script de shell en:' + linea + "-> Archivo enviado a cuarentena. \ n")
                        echo_alarmaslog("Shell found "+line, "Shell found on "+DIR,"")
                        "Shell encontrado" + línea, "Shell encontrado en" + DIR, "")
                        echo_prevencionlog("File "+line+" moved to quarentine folder","Shell found on tmp")
        global gMYMAIL
        if msg!='':
                body = msg +"\nAll files were sent to quarentine."
                send_email(gMYMAIL,'Alert Type 2 : Shells found',body)





def  buscar_scripts(DIR):
        for dir, dir_n, archi_n in  os.walk(DIR): #asignamos el caminero del directorio tmp 
                for f in filenames:  # si se encuentra un archivo ejecutable se genera la alarma correspondiente, se pondra en cuarentena o la eliminacion
                        if (('.py' in f ) or ('.sh' in f ) or ('.exe' in f) or  ('.deb' in f )): #verifica las extensiones
                                band=1
                                fecha = time.strftime("%d/%m/%Y") #guardamos la fecha y hora para la posterior configuracion 
                                hora = time.strftime("%H:%M:%S")
                                mensaje = "Se ha detectado un archivo ejecutable, Se ejecutara su envio a cuarentena."
                                entrada_ejecutable = fecha + ' ====== ' + hora + '\n' + mensaje + ' ---->  ' + f + '\n\n'
                                archivo=open('/var/log/hids/prevencionhids.log', 'a')
                                os.system("chmod 400 " + "/tmp/" + f) #Quitamos todos los permisos del archivo y ponemos solo lectura para el duenho
                                os.system("mv "+ "/tmp/" + f + " /home/Cuarentena") #Ponemos el archivo en carpeta oculta de cuarentena
                                print("\nEl archivo "+ f +" fue puesto en cuarentena. \n")
                                archivo.write(str((entrada_ejecutable)))
                               #se procedera a desencriptar la contraseña de nuestro correo para luego realizar el envio de alerta con smtplib
                                #En la carpeta tendremos un archivo encriptado con openssl, esto para que no haya ninguna contraseña visible 					       desencripte con el comando de abajo luego de usar se eliminara
                                os.system("openssl enc -aes-256-cbc -d -in pass_correo.txt.encrypted -out pass_correo.txt -k ADMINISTRATOR")
                                pass_correo = open("pass_correo.txt")
                                datapass_correo = pass_correo.read().replace('\n','') #se copia a esta variable para poner de parametro en la configuracion
                                pass_correo.close() # se cierra archivo
                                os.system("rm -rf pass_correo.txt") #siempre eliminamos la contraseña del directorio para que no haya ninguna contraseña a la vista
                                msg['Subject'] = "SE HA DETECTADO UNA ALARMA EN EL HIPS" #cabecera del mensaje
                                msg.attach(MIMEText(entrada_ejecutable, 'plain')) #cuerpo del mensaje
                               #configuramos los parametros para el envio con smtp
                                server = smtplib.SMTP('smtp.gmail.com: 587')
                                server.starttls()
                                server.login(msg['From'], datapass_correo)
                                server.sendmail(msg['From'], msg['To'], msg.as_string()) #se realiza la ejecucion de envio
                                server.quit()
                                mensaje_ejecutable = 'echo "Se encontro un ejecutable, ver correo para mas informacion" '#Se avisa por terminal que ocurrio algo!
                                mensaje_alarma = 'Se encontro un ejecutable, ver correo para mas informacion'
                                entrada_alarma = fecha + ' ====== ' + hora + '\n' + mensaje_alarma + '\n\n\n'
                                archivo1 = open('/var/log/hids/alarmashids.log', 'a') #abrimos el archivo txt para escribir el registro
                                archivo1.write(str((entrada_alarma)))  
                                archivo1.close()
                                os.system(mensaje_ejecutable)
                                archivo.close()
                                web = open("/home/fabrizio/Escritorio/hidss/HIPS2020/hips2020/hips2020/10.txt", "a")
                                web.write(str((entrada_alarma)))
                                web.close()
        if band != 1:    
                print("la carpeta esta limpia")
        return 

import subprocess
from utils import get_fecha

#Funcion: echo_alarmas_log
#	Escribe en el log /var/log/hips/alarmas.log la alarma registrada.
#Parametros:
#	info		(string) el mlensaje de alarma a registrar.
#	tipo_alarma	(string) el tipo de la alarma, corresponden a las funciones llamadoras
#	ip		(string) IP responsable de generar la alarma (si es que hay ip, caso contrario ip = '')
def echo_alarmas_log(info, tipo_alarma,ip):
    fecha_hora = get_fecha()
    if ip == '':
        ip = "No se encontro IP"
    msg = ''+fecha_hora+" :: "+tipo_alarma+" :: "+ip+" :: "+info
    p =subprocess.Popen("echo \""+msg+"\">>/var/log/hips/alarmas.log", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()


#Funcion: echo_prevencion_log
#	Escribe en el log /var/log/hips/prevencion.log las medidas de prevencion tomadas debido a una alarma detectada.
#Parametros:
#	info	(string) decision tomada
#	razon	(string) motivo por el cual se tomo la decision
def echo_prevencion_log(info, razon):	
    fecha_hora = get_fecha()
    msg = ''+fecha_hora+" :: "+info+" :: Motivo --> "+ razon
    p =subprocess.Popen("echo \""+msg+"\">>/var/log/hips/prevencion.log", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
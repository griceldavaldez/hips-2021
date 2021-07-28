
import subprocess

#Funcion: echo_alarmaslog
#
#	Escribe en el log /var/log/hips/alarmas.log la alarma registrada.
#
#Parametros:
#	alarm		(string) el mlensaje de alarma a registrar.
#	alarm_type	(string) el tipo de la alarma (ej: AMTP attack).
#	ip		(string) IP responsable de generar la alar,a (si es que hay ip, caso contrario ip = '')
#
def echo_alarmas_log(fecha_hora, info, typo_alarma,ip):
    if ip == '':
        ip = "No se encontro IP"
    msg = ''+fecha_hora+" :: "+typo_alarma+" :: "+ip+" :: "+info
    p =subprocess.Popen("echo \""+msg+"\">>/var/log/hips/alarmas.log", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()


def echo_prevencion_log(fecha_hora, info, razon):	
	msg = ''+fecha_hora+" :: "+info+" :: Motivo --> "+ razon
	p =subprocess.Popen("echo \""+msg+"\">>/var/log/hips/prevencion.log", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
from Main.variables_globales import directorio_cuarentena
import subprocess


def enviar_a_cuarentena(s_archivo):
    global directorio_cuarentena
    p =subprocess.Popen("mv "+s_archivo+" "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    print(output.decode("utf-8"), "\n", err)
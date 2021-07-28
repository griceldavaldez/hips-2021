import subprocess, os, sys
sys.path.append( os.path.abspath('../Main/'))
from variables_globales import directorio_cuarentena

def enviar_a_cuarentena(s_archivo):
    global directorio_cuarentena
    p =subprocess.Popen("mv "+s_archivo+" "+directorio_cuarentena, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    print(output.decode("utf-8"), "\n", err)
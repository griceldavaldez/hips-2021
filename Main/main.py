import sys
sys.path.append("/home/gvaldez/pruebas-hips/hips-2021/Configuraciones") 
from preferencias import guardar_preferencias

if __name__=='__main__':
        preferencias = guardar_preferencias()
        print(preferencias)
        

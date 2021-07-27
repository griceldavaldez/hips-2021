import sys
sys.path.append("../Configuraciones") 
from preferencias import guardar_preferencias

if __name__=='__main__':
        preferencias = guardar_preferencias()
        print(preferencias)
        
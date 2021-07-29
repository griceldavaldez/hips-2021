import datetime
#Retorna hora y fecha actual
def get_fecha():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
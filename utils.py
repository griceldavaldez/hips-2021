import datetime
def get_fecha():
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    return fecha_hora
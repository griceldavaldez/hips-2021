from werkzeug import utils
from flask_login import UserMixin
from Configuraciones import utils



class Usuario(UserMixin):

    #Metodos para obtener los atributos de la clase
    def getId(self):
        return self.id
    def getNombre(self):
        return self.nombre
    def getLogin(self):
        return self.login
    def getPassword(self):
        return self.password
    #Metodos para setear los atributos de la clase
    def setId(self, id):
        self.id = id
    def setNombre(self, nombre):
        self.nombre = nombre
    def setLogin(self, login):
        self.login = login 
    def setPassword(self, password):
        self.password = password 
    def __init__(self, id, nombre, login, password):
        self.id = id
        self.nombre = nombre
        self.login = login
        self.password = password
    def __repr__(self):
        return "<Usuario Id:%s Nombre:%s Login:%s>" % (self.id, self.nombre, self.login)

    @staticmethod
    def get_by_id(id):
        return utils.obtenerUsuarioPorId(id)

    def check_password(self,password):
        if(password == self.password):
            return True
        return False

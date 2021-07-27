class Usuario(object):
    #Metodos para obtener los atributos de la clase
    def getNombre(self):
        return self.nombre
    def getLogin(self):
        return self.login
    def getPassword(self):
        return self.password
    #Metodos para setear los atributos de la clase
    def setNombre(self, nombre):
        self.nombre = nombre
    def setLogin(self, login):
        self.login = login 
    def setPassword(self, password):
        self.password = password 
    def __repr__(self):
        return "<Usuario Nombre:%s Login:%s Password:%s>" % (self.nombre, self.login, self.password)
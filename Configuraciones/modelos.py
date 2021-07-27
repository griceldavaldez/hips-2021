class Usuario(object):
    #Metodos para obtener los atributos de la clase
    def getNombre(self):
        return self.nombre
    def getUsuario(self):
        return self.usuario
    def getPass(self):
        return self.pass
    #Metodos para setear los atributos de la clase
    def setNombre(self, nombre):
        self.nombre = nombre
    def setUsuario(self, usuario):
        self.usuario = usuario 
    def setPass(self, pass):
        self.pass = pass 
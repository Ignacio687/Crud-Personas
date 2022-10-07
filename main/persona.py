class Persona:
    def __init__(self, documento, apellido, nombre):
        self.documento = documento
        self.apellido = apellido
        self.nombre = nombre

    def __repr__(self):
        return f'{self.apellido} {self.nombre}, DNI: {self.documento}'

    def modDocumento(self, documento):
        self.documento = documento

    def modApellido(self, apellido):
        self.apellido = apellido

    def modNombre(self, nombre):
        self.nombre = nombre
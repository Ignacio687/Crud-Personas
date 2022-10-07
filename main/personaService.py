from main.persona import Persona

class PersonaExistsError(Exception):
    pass

class PersonaNotFoundError(Exception):
    pass

class PersonaService():

    def __init__(self):
        self.personas = {}
    
    def add(self, DNI, lastName, name):
        try:
            if (self.personas[DNI]).documento == DNI:
                raise PersonaExistsError('This person is already on the sistem')
        except KeyError:
            self.personas[DNI] = Persona(DNI, lastName, name)
        else:
            self.personas[DNI] = Persona(DNI, lastName, name)

    def searchPersona(self, searchParameter):
        try:
            if isinstance(searchParameter, int):
                return f'{self.personas[searchParameter]}'
            else: 
                returnList = '; '.join([str(value) for key, value in self.personas.items() if searchParameter in str(value)])
                if len(returnList) == 0:
                    raise KeyError
                return returnList
        except KeyError:
            raise PersonaNotFoundError('There are no entries that match the especified search parameter')
        
    def delPersona(self, DNI):
        try:
            del self.personas[DNI]
        except KeyError:
            raise PersonaNotFoundError('There are no entries with that "DNI"')

    def update(self, DNI, option, string):
        try:
            if option:
                self.personas[DNI].modNombre(string)
            else: self.personas[DNI].modApellido(string)
        except KeyError:
            raise PersonaNotFoundError('There are no entries with that "DNI"')

    def showAll(self):
        return '; '.join([str(persona).strip('\n') for key, persona in self.personas.items()])

    def dellAll(self):
        self.personas.clear()
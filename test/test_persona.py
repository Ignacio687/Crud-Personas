import unittest
from main.filesService import *
from main.persona import Persona
from main.personaService import *

class PersonaService_PersonaManagementTests(unittest.TestCase):    

    def setUp(self):
        self.service = PersonaService()
    
    def test_AddNewPersona(self):
        self.service.add(44572902, 'Ramirez', 'Pedro')
        self.assertEqual(str(self.service.personas[44572902]), 'Ramirez Pedro, DNI: 44572902')
        
    def test_AddNewPersona_PersonaExists(self):
        self.service.add(44572902, 'Ramirez', 'Pedro')
        with self.assertRaises(PersonaExistsError):
            self.service.add(44572902, 'Ramirez', 'Pedro')
    
    def test_SearchPersona_ByDNI(self):
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.assertEqual(self.service.searchPersona(44572902), 'Ramirez Pedro, DNI: 44572902')
    
    def test_SearchPersona_ByDNI_PersonaNotFound(self):
        with self.assertRaises(PersonaNotFoundError):
            self.service.searchPersona(44572902)

    def test_SearchPersona_ByName(self):
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.assertEqual(self.service.searchPersona('Pedro'), 'Ramirez Pedro, DNI: 44572902')
    
    def test_SearchPersona_ByName_PersonaNotFound(self):
        with self.assertRaises(PersonaNotFoundError):
            self.service.searchPersona('Pedro')
    
    def test_SearchPersona_ByName_MoreThanOne(self):
        self.service.personas[44500924] = Persona(44500924, 'Brasolin', 'Juan')
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.personas[44582659] = Persona(44582659, 'Boldrini', 'Jose')
        self.service.personas[44572456] = Persona(44572456, 'Chaves', 'Pedro')
        self.assertEqual(self.service.searchPersona('Pedro'), 
        'Ramirez Pedro, DNI: 44572902; Chaves Pedro, DNI: 44572456')
    
    def test_DelPersona(self):
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.delPersona(44572902)
        self.assertEqual(str(self.service.personas.get(44572902)), 'None')
    
    def test_DelPersona_PersonaNotFound(self):
        with self.assertRaises(PersonaNotFoundError):
            self.service.delPersona(44572902)
    
    def test_Update(self):
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.update(44572902, 0, 'Chaves')
        self.service.update(44572902, 1, 'Juan')
        self.assertEqual(str(self.service.personas[44572902]), 
        'Chaves Juan, DNI: 44572902')
    
    def test_Update_PersonaNotFound(self):
        with self.assertRaises(PersonaNotFoundError):
            self.service.update(44572902, 0, 'Chaves')
        with self.assertRaises(PersonaNotFoundError):  
            self.service.update(44572902, 1, 'Juan')

    def test_ShowAllPersonas(self):
        self.service.personas[44500924] = Persona(44500924, 'Brasolin', 'Juan')
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.personas[44582659] = Persona(44582659, 'Boldrini', 'Jose')
        self.assertEqual(self.service.showAll(),  
        'Brasolin Juan, DNI: 44500924; Ramirez Pedro, DNI: 44572902; Boldrini Jose, DNI: 44582659')

    def test_ShowAllPersonas_Empty(self):
        self.assertEqual(self.service.showAll(), '')
   
    def test_DellAllPersonas(self):
        self.service.personas[44500924] = Persona(44500924, 'Brasolin', 'Juan')
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.personas[44582659] = Persona(44582659, 'Boldrini', 'Jose')
        self.service.dellAll()
        self.assertEqual(self.service.personas, {})

    def test_DellAllPersonas_AlreadyEmpty(self):
        self.service.dellAll()
        self.assertEqual(self.service.personas, {})

# if __name__=='__main__':
#     unittest.main()
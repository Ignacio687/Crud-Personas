import unittest
from main.filesService import *
from main.persona import Persona
from main.personaService import *
import os

class PersonaService_FileManagementTests(unittest.TestCase):

    def setUp(self):
        self.service = FileService()
        self.folderPath = self.service.filesFolderPath
        self.pathFormat = '\\' if '\\' in self.service.filesFolderPath else '/'
        self.eraseFiles()

    def eraseFiles(self):
        try:
            for fileName in os.listdir(self.folderPath):
                if '.txt' in fileName:
                    os.remove(self.folderPath+self.pathFormat+fileName)
        except FileNotFoundError:
            exit

    def createFile(self, fileName):
        TXTTestFile = open(self.folderPath+self.pathFormat+str(fileName)+'.txt','a')
        TXTTestFile.close()

    def test_zzzErraseAllResidualFiles(self):
        self.eraseFiles()

    def test_CreateFile(self):       
        self.service.createFile('Users')
        self.assertTrue(os.path.exists(self.folderPath))

    def test_CreateFile_Exception_FileAlreadyExists(self):
        self.service.createFile('Users')
        with self.assertRaises(FileExistsError):
            self.service.createFile('Users')

    def test_VerifyFileExists(self):
        self.createFile('Users')
        self.assertTrue(self.service.verifyFileExists('Users'))

    def test_VerifyFileExists_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.service.verifyFileExists('Users')

    def test_SearchAllFiles(self):
        for fileName in ['Users', 'Administrators', 'Guests']:
            self.createFile(fileName)
        self.assertEqual(self.service.searchAllFiles(), 'Administrators.txt; Guests.txt; Users.txt')

    def test_SearchAllFiles_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.service.searchAllFiles()

    def test_DeleteFile(self):
        self.createFile('Users')
        self.service.deleteFile('Users')
        self.assertFalse(os.path.exists(f'{self.folderPath}{self.pathFormat}Users.txt'))
            
    def test_DeleteFile_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.service.deleteFile('Users')
    
    def test_SearchPersona(self):
        self.createFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            file.write('pedro\n')
            file.write('1234\n')
            file.write('Ramirez Pedro, DNI: 44572902\n')
        self.assertEqual(self.service.searchPersonaInFile(44572902, 'Users'), 'Ramirez Pedro, DNI: 44572902 is in line 2')
        self.assertEqual(self.service.searchPersonaInFile('Pedro', 'Users'), 'Ramirez Pedro, DNI: 44572902 is in line 2')
        self.assertEqual(self.service.searchPersonaInFile('Ramirez', 'Users'), 'Ramirez Pedro, DNI: 44572902 is in line 2')
    
    def test_SearchPersona_MoreThanOne(self):
        self.createFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            for data in ['Chaves Pedro, DNI: 5794315\n', '1234\n',
            'Ramirez Pedro, DNI: 44572902\n', 'adasd1123\n', 'Chaves Jose, DNI: 1576421\n']:
                file.write(data)
        self.assertEqual(self.service.searchPersonaInFile('Pedro', 'Users'), 
        'Chaves Pedro, DNI: 5794315 is in line 0; Ramirez Pedro, DNI: 44572902 is in line 2')
        self.assertEqual(self.service.searchPersonaInFile('Chaves', 'Users'), 
        'Chaves Pedro, DNI: 5794315 is in line 0; Chaves Jose, DNI: 1576421 is in line 4')

    def test_SearchPersona_PersonaNotFound(self):
        self.createFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            file.write('pedro\n')
            file.write('1234\n')
            file.write('Ramirez Pedro, DNI: 44572902\n')
        with self.assertRaises(PersonaNotFoundInFileError):
            self.service.searchPersonaInFile(44572142, 'Users')
        with self.assertRaises(PersonaNotFoundInFileError):
            self.service.searchPersonaInFile('Jose', 'Users')
        with self.assertRaises(PersonaNotFoundInFileError):
            self.service.searchPersonaInFile('Lucas', 'Users')
    
    def test_SearchPersona_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.service.searchPersonaInFile(44572902, 'Users')

    def test_AddPersonaToFile(self):
        self.createFile('Users')
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.addInFile(44572902, 'Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt') as file:
            self.assertEqual(file.read(),'Ramirez Pedro, DNI: 44572902\n')

    def test_AddMultiplePersonaToFile(self):
        self.createFile('Users')
        for DNI, lastName, name in [44500924, 'Brasolin' , 'Juan'], [44572902, 'Ramirez', 'Pedro'], [44582659, 'Boldrini', 'Jose']:
            self.service.personas[DNI] = Persona(DNI, lastName, name)
        for persona in [44500924, 44572902, 44582659]:
            self.service.addInFile(persona, 'Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt') as file:
            self.assertEqual(file.read(),'Brasolin Juan, DNI: 44500924\n'
            +'Ramirez Pedro, DNI: 44572902\nBoldrini Jose, DNI: 44582659\n')

    def test_AddPersonaToFile_FileDoNotExists(self):
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        with self.assertRaises(FileNotFoundError): 
            self.service.addInFile(44572902, 'Users')

    def test_AddPersonaToFile_PersonaDoNotExists(self):
        self.createFile('Users')
        with self.assertRaises(PersonaNotFoundError): 
            self.service.addInFile(44572902, 'Users')
    
    def test_AddPersonaToFile_PersonaAlreadyExists(self):
        self.service.createFile('Users')
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        self.service.addInFile(44572902, 'Users')
        with self.assertRaises(PersonaExistsInFileError): 
            self.service.addInFile(44572902, 'Users')

    def test_ReadFile_Empty(self):
        self.createFile('Users')
        self.assertEqual(self.service.readFile('Users'), '')
    
    def test_ReadFile_OneLine(self):
        self.createFile('Users')
        self.service.personas[44572902] = Persona(44572902, 'Ramirez', 'Pedro')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            file.write(str(self.service.personas[44572902])+'\n')
        self.assertEqual(self.service.readFile('Users'),
        'Ramirez Pedro, DNI: 44572902')

    def test_ReadFile_MoreThanOneLine(self):
        self.createFile('Users')
        for DNI, lastName, name in [44500924, 'Brasolin' , 'Juan'], [44572902, 'Ramirez', 'Pedro'], [44582659, 'Boldrini', 'Jose']:
            self.service.personas[DNI] = Persona(DNI, lastName, name)
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            for persona in [44500924, 44572902, 44582659]:
                file.write(str(self.service.personas[persona])+'\n')
        self.assertEqual(self.service.readFile('Users'),
        'Brasolin Juan, DNI: 44500924; Ramirez Pedro, DNI: 44572902; '
        +'Boldrini Jose, DNI: 44582659')

    def test_ReadFile_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.assertEqual(self.service.readFile('Users'))

    def test_SaveAllPersonaToFile(self):
        self.createFile('Users')
        for DNI, lastName, name in [44500924, 'Brasolin' , 'Juan'], [44572902, 'Ramirez', 'Pedro'], [44582659, 'Boldrini', 'Jose']:
            self.service.personas[DNI] = Persona(DNI, lastName, name)
        self.service.saveAllPersonaToFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt') as file:
            self.assertEqual(file.read(),'Brasolin Juan, DNI: 44500924\n'
            +'Ramirez Pedro, DNI: 44572902\nBoldrini Jose, DNI: 44582659\n')

    def test_SaveAllPersonaToFile_PersonasEmpty(self):
        self.createFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            file.write('Brasolin Juan, DNI: 44500924\n')
        self.service.saveAllPersonaToFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'r') as file:
            self.assertEqual(file.read(),'Brasolin Juan, DNI: 44500924\n')

    def test_SaveAllPersonaToFil_SomePersonaAlreadyExists(self):
        self.createFile('Users')
        for DNI, lastName, name in [44500924, 'Brasolin' , 'Juan'], [44572902, 'Ramirez', 'Pedro'], [44582659, 'Boldrini', 'Jose']:
            self.service.personas[DNI] = Persona(DNI, lastName, name)
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'w') as file:
            file.write('Brasolin Juan, DNI: 44500924\n')
        self.service.saveAllPersonaToFile('Users')
        with open(f'{self.folderPath}{self.pathFormat}Users.txt', 'r') as file:
            self.assertEqual(file.read(),'Brasolin Juan, DNI: 44500924\n'
            +'Ramirez Pedro, DNI: 44572902\nBoldrini Jose, DNI: 44582659\n')

    def test_SaveAllPersonaToFile_FileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.service.saveAllPersonaToFile('Users')

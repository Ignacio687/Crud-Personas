from main.personaService import PersonaService
import os 

class PersonaExistsInFileError(Exception):
    pass

class PersonaNotFoundInFileError(Exception):
    pass

class FileService(PersonaService):

    def __init__(self, filesFolderPath=os.path.abspath('main/serviceTXTFiles')):
        super().__init__()
        self.filesFolderPath = filesFolderPath
        self.pathFormat = '\\' if '\\' in self.filesFolderPath else '/'

    def createFile(self, fileName):
        try:
            if self.verifyFileExists(fileName):
                raise FileExistsError('The file already exists in the specified directory')
        except FileNotFoundError:
            #If the file does not exist the verifyFileExists function will raise an exception, 
            #thats why the code used to create the file is in the except clause and not in try
            TXTFile = open(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt','a')
            TXTFile.close()
            
    def verifyFileExists(self, fileName):
        if os.path.exists(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt'):
           return True
        else:
            raise FileNotFoundError('The file do not exists in the specified directory')

    def searchAllFiles(self):
        if len(os.listdir(self.filesFolderPath)) != 0:
            return '; '.join(os.listdir(self.filesFolderPath))
        else:
            raise FileNotFoundError('There are no files in the specified directory')

    def deleteFile(self, fileName):
        if self.verifyFileExists(fileName):
            os.remove(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt')
   
    def addInFile(self, DNI, fileName):
        try:
            self.searchPersona(DNI)
            self.searchPersonaInFile(DNI, fileName)
        except PersonaNotFoundInFileError:   
            with open(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt', 'a') as file:
                file.write(f'{self.personas[DNI]}\n')
        else:
            raise PersonaExistsInFileError(f'{self.personas[DNI].nombre} already exists in {fileName}')

    def searchPersonaInFile(self, parameter, fileName):
        self.verifyFileExists(fileName)
        with open(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt', 'r') as file:
            fileList = file.readlines()
        if str(parameter) in '; '.join(fileList):
            return '; '.join([str(persona).strip('\n')+' is in line '+str(fileList.index(persona))
            for persona in fileList if str(parameter) in persona])
        else: raise PersonaNotFoundInFileError(f'There are no entries with "DNI" = {parameter} in {fileName}')

    def readFile(self, fileName):
        self.verifyFileExists(fileName)
        with open(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt') as file:
            return '; '.join(file.readlines()).replace('\n', '')
        
    def saveAllPersonaToFile(self, fileName):
        if self.verifyFileExists(fileName):
            for persona in self.personas.keys():
                try:
                    self.searchPersonaInFile(persona, fileName)
                except PersonaNotFoundInFileError:
                    with open(self.filesFolderPath+self.pathFormat+str(fileName)+'.txt', 'a') as file:
                        file.write(f'{self.personas[persona]}\n')
                else:
                    continue
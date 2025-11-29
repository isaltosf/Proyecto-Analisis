from abc import ABC, abstractmethod
from algoritmos import *


class EstrategiaCodificacion(ABC):
    @abstractmethod
    def codificar(self, cadena):
        pass

class CodificarXOR(EstrategiaCodificacion):
    def __init__(self, key):
        self.key = key
    
    def codificar(self, cadena):
        return procesarXOR(cadena, self.key)

class CodificarClasico(EstrategiaCodificacion):
    def codificar(self, cadena):
        return codificar(cadena)
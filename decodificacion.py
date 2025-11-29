from abc import ABC, abstractmethod
from algoritmos import *

class EstrategiaDecodificacion(ABC):
    @abstractmethod
    def decodificar(self, cadena, key):
        pass

class DecodificarXOR(EstrategiaDecodificacion):
    def decodificar(self, cadena, key):
        return procesarXOR(cadena, key)

class DecodificarClasico(EstrategiaDecodificacion):
    def decodificar(self, cadena, key):
        return decodificar(cadena, key)
class ContextoDecodificar:
    def __init__(self, estrategia):
        self.estrategia = estrategia
    
    def set_estrategia(self, estrategia):
        self.estrategia = estrategia

    def ejecutar(self, cadena, key):
        return self.estrategia.decodificar(cadena, key)

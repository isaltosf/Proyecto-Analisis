class ContextoCodificar:
    def __init__(self, estrategia):
        self.estrategia = estrategia
    
    def set_estrategia(self, estrategia):
        self.estrategia = estrategia

    def ejecutar(self, cadena):
        return self.estrategia.codificar(cadena)

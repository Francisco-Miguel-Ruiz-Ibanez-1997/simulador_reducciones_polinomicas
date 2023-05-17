from abc import ABC, abstractmethod

############################################################
# Clase padre de que la heredarán el resto de interfaces de 
# las poli-reducciones implementadas.
############################################################
class InterfazPoliReduccion(ABC):

    _nombre = None
    _ventana = None

    def get_nombre(self):
        return self._nombre

    # Método que se encargarán de implementar las interfaces
    # concretas de cada poli-reducción. Lanzará la interfaz
    # que contiene las ventanas y paneles de la poli-reducción
    # a lanzar.
    @abstractmethod
    def lanzar_interfaz_poli_reduccion(self, lista_resultados_previos):
        pass
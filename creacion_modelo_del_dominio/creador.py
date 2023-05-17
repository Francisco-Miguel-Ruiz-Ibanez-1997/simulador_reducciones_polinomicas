from abc import ABC, abstractmethod

#######################################################
# Clase abstracta de la que heredarán el resto de 
# creadores dedicados a la creación (fabricación) de
# de objetos del dominio (nodos, aristas y grafo).
#######################################################
class Creador(ABC):

    # Método que se encargarán de implementar las factorías
    # hijas de forma que construirán los objetos que 
    # constituyen el dominio la aplicación.
    @abstractmethod
    def metodo_factoria(self):
        pass
#######################################################################
# Clase Arista que representa las relaciones (poli-reducciones) entre 
# los nodos del grafo. Cada Arista contendrá: nombre, un nodo src, 
# un nodo dest, un booleano para controlar si la poli-reducción se ha
# realizado y una lista que contiene la información calculada en la 
# poli-reducción.
#######################################################################
class Arista():
    
    # Constructor
    def __init__(self, nombre, src, dest):

        self.nombre = nombre
        self.src = src
        self.dest = dest

        self.poli_reduccion_completada = False
        self.lista_informacion_calculada = []

    ### Getters y setters ###

    def get_nombre(self):
        return self.nombre

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_poli_reduccion_completada(self):
        return self.poli_reduccion_completada
    
    def set_poli_reduccion_completada(self, valor):
        self.poli_reduccion_completada = valor
    
    def get_lista_informacion_calculada(self):
        return self.lista_informacion_calculada
    
    def anadir_a_lista_informacion_calculada(self, informacion):
        self.lista_informacion_calculada.append(informacion)
    
    def resetear_lista_informacion_calculada(self):
        self.lista_informacion_calculada = []

        



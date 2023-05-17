from .creador import Creador
from .creador_nodos import CreadorNodos
from .creador_aristas import CreadorAristas

from modelo_del_dominio.grafo.grafo import Grafo

#######################################################
# Clase que se encarga de la creación (fabricación) de
# del grafo (junto con los nodos y arsitas), es decir,
# nuestro universo.
#######################################################
class CreadorGrafo(Creador):

    _unica_instancia = None

    # Instancia del creador.
    def get_unica_instancia():

        if CreadorGrafo._unica_instancia == None:
            CreadorGrafo._unica_instancia = CreadorGrafo()

        return CreadorGrafo._unica_instancia
    
    # Creación del grafo (universo) con los nodos y aristas creados.
    def metodo_factoria(self):

        nodo_sat3cnf = CreadorNodos.get_unica_instancia().get_lista_nodos()[0]
        nodo_hampath = CreadorNodos.get_unica_instancia().get_lista_nodos()[1]
        nodo_hamcycle = CreadorNodos.get_unica_instancia().get_lista_nodos()[2]

        arista_sat3nf_a_hampath = CreadorAristas.get_unica_instancia().get_lista_aristas()[0]
        arista_hampath_a_hamcycle = CreadorAristas.get_unica_instancia().get_lista_aristas()[1]

        lista_nodos = [nodo_sat3cnf, nodo_hampath, nodo_hamcycle]
        lista_aristas = [arista_sat3nf_a_hampath, arista_hampath_a_hamcycle]

        # Devolvemos grafo creado
        return Grafo(lista_nodos, lista_aristas)
######################################################################
# Clase Grafo que representa a las relaciones entre problemas (nodos)
# en cuanto a poli-reducciones se refieren. Diremos que dos nodos 
# estarán relacionados entre sí (hay una arista que los une) si 
# uno de ellos se poli-reduce en el otro.
#################################################################
class Grafo():

    # Constructor
    def __init__(self, nodos, aristas):

        self.lista_nodos = nodos
        self.lista_nodos_id = [nodo.id_nodo for nodo in self.lista_nodos]
        self.lista_aristas = aristas
    
    ### Getters ###
    
    # Obtiene un nodo por su nombre.
    def get_nodo(self, nombre):

        for nodo in self.lista_nodos:
            if nodo.get_nombre() == nombre:
                return nodo
        return None

    # Obtiene las aristas que contienen en su nodo src
    # el pasado por parámetro.
    def get_aristas_src(self, src):
        return [arista for arista in self.lista_aristas if arista.get_src().get_nombre() == src]
    
    # Función que obtiene, dada una lista de aristas,
    # una lista de los nombres de los nodos dest
    # de estas.
    def get_nodos_dest_aristas(self, aristas):
        return [arista.get_dest().get_nombre() for arista in aristas]
    
    # Devuelve una arista que contiene como nodos src y dest
    # los pasados por parámetro.
    def get_arista_nodos_src_dest(self, src, dest):

        for arista in self.lista_aristas:

            if arista.get_src().get_nombre() == src and arista.get_dest().get_nombre() == dest:
                return arista
        
        return None

    # Función que devuelve una lista de aristas
    # que conectan el nodo src con el nodo dest, ambos pasados
    # por parámetros. Esta función llama a encontrar_camino_de_nodos, que 
    # obtiene una lista de nodos a visitar desde el nodo
    # src hasta el nodo dest.
    def encontrar_aristas(self, src, dest, lista_aristas):

        lista_nodos_a_visitar = self.encontrar_camino_de_nodos(src, dest, lista_aristas)

        lista_aristas = []
        i = 0

        # Añadimos camino de aristas
        for i in range(0, len(lista_nodos_a_visitar) - 1):
            nodo_a = lista_nodos_a_visitar[i]
            nodo_b = lista_nodos_a_visitar[i+1]

            # Buscamos las aristas que unen src y dest en base a los nodos 
            # a visitar calculados
            lista_aristas.append(self.get_arista_nodos_src_dest(nodo_a, nodo_b))

            i += 1
        
        return lista_aristas

    # https://www.python.org/doc/essays/graphs/
    # Función que encuentra una camino (de aristas) entre 
    # los nodos src y dest. Emplea backtracking.
    def encontrar_camino_de_nodos(self, src, dest, camino):

        camino = camino + [src]

        # Si el nodo src es el mismo que el dest,
        # devolvemos camino
        if src == dest:
            return camino

        # Si es grafo no contiene el nodo src,
        # devolvemos lista vacía
        if self.get_nodo(src) == None:
            return []

        # Obtenemos las aristas que contienen en su nodo
        # src el nodo src que estamos buscando
        aristas = self.get_aristas_src(src)
        
        # Recorremos ahora los nodos dest de todas las aristas
        # anteriores
        for nodo in self.get_nodos_dest_aristas(aristas):
            if nodo not in camino:
                # Llamada recursiva. Backtracking. Búsqueda de nuevos
                # caminos en base al nuevo nodo src, que será el dest
                # de la arista anterior
                nuevo_camino = self.encontrar_camino_de_nodos(nodo, dest, camino)

                # Si tenemos nuevo camino, lo devolvemos
                if nuevo_camino:     
                    return nuevo_camino
        return []
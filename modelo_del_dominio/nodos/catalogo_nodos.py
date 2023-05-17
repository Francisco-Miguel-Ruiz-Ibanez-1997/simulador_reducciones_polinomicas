from creacion_modelo_del_dominio.proveedor_creador import ProveedorCreador

######################################################
# Clase que contiene todo el catálogo (repertorio) de 
# problemas (nodos) del simulador.
######################################################
class CatalogoNodos():

    _unica_instancia = None

    def __init__(self):

        self.lista_nodos = []

        # Inicialización y creación de problemas (nodos)
        self.inicializar_nodos()

    ### Getters ###

    def get_lista_nodos(self):
        return self.lista_nodos
    
    # Obtiene la lista de id de los nodos.
    def get_lista_id_nodos(self):
        return [nodo.get_id() for nodo in self.lista_nodos]
    
    # Obtiene la lista de nombres de nodos del grafo.
    def get_lista_nombres_nodos(self):
        return [nodo.get_nombre() for nodo in self.lista_nodos]

    # Devuelve un nodo.
    def get_nodo(self, nodo):

        for nodo1 in self.lista_nodos:
            if nodo1.get_id() == nodo.get_id():
                return nodo1
        return None

    # Devuelve un nodo por su id.
    def get_nodo_por_id(self, id_nodo):

        for nodo in self.lista_nodos:
            if nodo.get_id() == id_nodo:
                return nodo
        return None

    # Devuelve un nodo por su nombre.
    def get_nodo_por_nombre(self, nombre_nodo):

        for nodo in self.lista_nodos:
            if nodo.get_nombre() == nombre_nodo:
                return nodo
        return None

    # Instancia del catálogo.
    def get_unica_instancia():

        if  CatalogoNodos._unica_instancia == None:
            CatalogoNodos._unica_instancia = CatalogoNodos()

        return CatalogoNodos._unica_instancia
    
    # El catálogo solicita el creador de nodos y delega en él la creación de estos.
    def inicializar_nodos(self):

        self.lista_nodos = ProveedorCreador.get_unica_instancia().get_creador("nodos").metodo_factoria()


        



from creacion_modelo_del_dominio.proveedor_creador import ProveedorCreador

######################################################
# Clase que contiene todo el catálogo (repertorio) de 
# aristas del grafo del simulador.
######################################################
class CatalogoAristas():

    _unica_instancia = None

    def __init__(self):

        self.lista_aristas = []

        # Inicialización y creación de problemas (aristas)
        self.inicializar_aristas()
    
    ### Getters ###
    
    def get_lista_aristas(self):
        return self.lista_aristas

    # Devuelve una arista por su nombre.
    def get_arista(self, nombre_arista):

        for arista in self.lista_aristas:
            if arista.get_nombre() == nombre_arista:
                return arista 
        return None

    # Devuelve la lista de aristas como una lista de 
    # tuplas de nodo_src y nodo_dest.
    def get_lista_tuplas_aristas(self):
        return [(arista.get_src().get_id(), arista.get_dest().get_id()) for arista in self.lista_aristas]
        
    
    # Resetea la completación de las poli-reducciones (aristas) y resetea
    # la lista de información calculada en estas.
    def resetear_aristas(self):

        for arista in self.lista_aristas:
            arista.set_poli_reduccion_completada(False)
            arista.resetear_lista_informacion_calculada()

    # Instancia del catálogo.
    def get_unica_instancia():

        if CatalogoAristas._unica_instancia == None:
            CatalogoAristas._unica_instancia = CatalogoAristas()

        return CatalogoAristas._unica_instancia
    
    # El catálogo solicita el creador de aristas y delega en él la creación de estas.
    def inicializar_aristas(self):

        self.lista_aristas = ProveedorCreador.get_unica_instancia().get_creador("aristas").metodo_factoria()



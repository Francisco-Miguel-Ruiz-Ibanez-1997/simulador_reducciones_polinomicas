from modelo_del_dominio.nodos.catalogo_nodos import CatalogoNodos
from modelo_del_dominio.aristas.catalogo_aristas import CatalogoAristas
from creacion_modelo_del_dominio.proveedor_creador import ProveedorCreador

###########################################################
# Clase controladora. Se encarga da la comunicación entre 
# la gui de la app y el domino de esta, es decir, su fun-
# ción es la de transmitir datos a la gui para que los 
# muestre y recibir órdenes de esta para manipular los 
# datos del domino, como la actualización de estos. 
# También se encarga de comprobar que se está haciendo una
# simulación, de forma que el usuario no puede lanzar otra
# hasta que cancele la que esté en marcha o termine esta.
###########################################################
class Controlador():

    # Inicializacion de catalogos
    _catalogo_nodos = None
    _catalogo_aristas = None
    _grafo_universo = None

    _unica_instancia = None
    _num_simulaciones = 0
    _num_simulaciones_solver = 0

    def __init__(self):

        # Control sobre las simulaciones en marcha
        self._num_simulaciones = 0

        # Inicializacion de catálogos
        self._catalogo_nodos = CatalogoNodos.get_unica_instancia()
        self._catalogo_aristas = CatalogoAristas.get_unica_instancia()
        self._grafo_universo = ProveedorCreador.get_unica_instancia().get_creador("grafo").metodo_factoria()

        # Lista de las poli-reducciones que ha realizado el
        # usuario
        self.aristas_a_actualizar = []
    
    def get_num_simulaciones(self):
        return self._num_simulaciones
    
    def set_num_simulaciones(self, valor):
        self._num_simulaciones = valor
    
    def get_num_simulaciones_solver(self):
        return self._num_simulaciones_solver
    
    def set_num_simulaciones_solver(self, valor):
        self._num_simulaciones_solver = valor

    def get_aristas_a_actualizar(self):
        return self.aristas_a_actualizar

    def anadir_aristas_a_actualizar(self, arista):
        self.aristas_a_actualizar.append(arista)
    
    def resetear_aristas_a_actualizar(self):
        self.aristas_a_actualizar = []
    
    # Instancia del controlador.
    def get_unica_instancia():

        if Controlador._unica_instancia == None:
            Controlador._unica_instancia = Controlador()

        return Controlador._unica_instancia

    #############################################
    ######### MÉTODOS ASOCIADOS A NODOS #########
    #############################################

    def get_lista_nodos(self):
        return self._catalogo_nodos.get_lista_nodos()
    
    def get_lista_nombres_nodos(self):
        return self._catalogo_nodos.get_lista_nombres_nodos()

    def get_num_nodos(self):
        return len(self._catalogo_nodos.get_lista_nodos())
    
    def get_lista_id_nodos(self):
        return self._catalogo_nodos.get_lista_id_nodos()
    
    def get_nombre_nodo(self, nodo):
        return self._catalogo_nodos.get_nodo(nodo).get_nombre()

    def get_alias_nodo(self, nodo):
        return self._catalogo_nodos.get_nodo(nodo).get_alias()
    
    def get_alias_nodo_por_id(self, id_nodo):
        return self._catalogo_nodos.get_nodo_por_id(id_nodo).get_alias()
    
    def get_alias_nodo_por_nombre(self, nombre_nodo):
        return self._catalogo_nodos.get_nodo_por_nombre(nombre_nodo).get_alias()
    
    def get_color_nodo(self, nodo):
        return self._catalogo_nodos.get_nodo(nodo).get_color()
    
    def get_color_nodo_por_nombre(self, nombre_nodo):
        return self._catalogo_nodos.get_nodo_por_nombre(nombre_nodo).get_color()
    
    def get_texto_info_nodo(self, nombre_nodo):
        return self._catalogo_nodos.get_nodo_por_nombre(nombre_nodo).get_texto_info()

    def get_img_qr_nodo(self, nombre_nodo):
        return self._catalogo_nodos.get_nodo_por_nombre(nombre_nodo).get_img_qr()

    ###############################################
    ######### MÉTODOS ASOCIADOS A ARISTAS #########
    ###############################################
    
    def get_lista_tuplas_aristas(self):
        return self._catalogo_aristas.get_lista_tuplas_aristas()
    
    def get_arista(self, nombre_arista):
        return self._catalogo_aristas.get_arista(nombre_arista)

    def get_poli_reduccion_completada(self, nombre_arista):
        return self.get_arista(nombre_arista).get_poli_reduccion_completada()

    def set_poli_reduccion_completada(self, nombre_arista, valor):
        self.get_arista(nombre_arista).set_poli_reduccion_completada(valor)

    def get_arista_nombre_src(self, nombre_arista):
        return self.get_arista(nombre_arista).get_src().get_nombre()
    
    def get_arista_nombre_dest(self, nombre_arista):
         return self.get_arista(nombre_arista).get_dest().get_nombre()

    def get_arista_id_src(self, nombre_arista):
        return self.get_arista(nombre_arista).get_src().get_id()

    def get_arista_id_dest(self, nombre_arista):
        return self.get_arista(nombre_arista).get_dest().get_id()
    
    def get_lista_informacion_calculada_arista(self, nombre_arista):
        return self.get_arista(nombre_arista).get_lista_informacion_calculada()
    
    def anadir_a_lista_informacion_calculada_arista(self, nombre_arista, informacion):
        self.get_arista(nombre_arista).anadir_a_lista_informacion_calculada(informacion)
    
    def resetear_poli_reducciones(self):
        self._catalogo_aristas.resetear_aristas()

    ##############################################
    ######### MÉTODOS ASOCIADOS AL GRAFO #########
    ##############################################
    def buscar_aristas(self, problema_1, problema_2, lista_aristas):

        lista = []
        for arista in self._grafo_universo.encontrar_aristas(problema_1, problema_2, lista_aristas):
            lista.append(arista.get_nombre())
        
        return lista

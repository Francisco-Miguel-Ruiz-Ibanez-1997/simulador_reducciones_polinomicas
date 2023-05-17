from .interfaz_sat3cnf_a_hampath.interfaz_sat3cnf_a_hampath import InterfazSat3cnfAHampath
from .interfaz_hampath_a_hamcycle.interfaz_hampath_a_hamcycle import InterfazHampathHamcycle

###########################################################
# Clase que contiene todas las interfaces de las poli-
# reducciones implementadas. Se encargará de inicializarlas
# y de aportar la interfaz que se va a lanzar.
###########################################################
class RepertorioInterfacesPoliReduccion():

    _unica_instancia = None
    _lista_interfaces = []

    # Constructor.
    def __init__(self, ventana):

        self.inicializar_interfaces(ventana)
    
    # Método que se encarga de lanzar la interfaz de la poli-reducción pasada
    # por parámetro.
    def lanzar_interfaz_poli_reduccion(self, nombre, lista_resultados_previos):

        for interfaz in self._lista_interfaces:
            if interfaz.get_nombre() == nombre:
                interfaz.lanzar_interfaz_poli_reduccion(lista_resultados_previos)
    
    # Obtiene la lista de nombres de interfaces de las poli-
    # reducciones implementadas en el simulador.
    def get_lista_interfaces(self):
        
        lista = []
        for interfaz in self._lista_interfaces:
            lista.append(interfaz.get_nombre())
        
        return lista

    # Instancia del repertorio de interfaces.
    def get_unica_instancia(ventana):

        if RepertorioInterfacesPoliReduccion._unica_instancia == None:
            RepertorioInterfacesPoliReduccion._unica_instancia = RepertorioInterfacesPoliReduccion(ventana)
        
        return RepertorioInterfacesPoliReduccion._unica_instancia

    # Se encarga de crear las interfaces a lanzar.
    def inicializar_interfaces(self, ventana):
        
        intefaz_sat3cnf_a_hampath = InterfazSat3cnfAHampath("SAT3cnf->HAMPATH", ventana)
        interfaz_hampath_a_hamcycle = InterfazHampathHamcycle("HAMPATH->HAMCYCLE", ventana)

        self._lista_interfaces.append(intefaz_sat3cnf_a_hampath) 
        self._lista_interfaces.append(interfaz_hampath_a_hamcycle)

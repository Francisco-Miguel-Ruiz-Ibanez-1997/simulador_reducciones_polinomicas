
from .creador_nodos import CreadorNodos
from .creador_aristas import CreadorAristas
from .creador_grafo import CreadorGrafo

###################################################
# Clase que se encarga de suministrar y aportar
# los creadores (factorías) de los elementos del
# dominio. Así, evitamos detalles relativos a  
# cada creador (factoría) implementado (como su
# nombre), aportando un mayor grado de abstracción.
###################################################
class ProveedorCreador():

    _unica_instancia = None

    # Instacia del proveedor.
    def get_unica_instancia():

        if  ProveedorCreador._unica_instancia == None:
            ProveedorCreador._unica_instancia = ProveedorCreador()

        return ProveedorCreador._unica_instancia

    # Obtiene el creador según el argumento pasado por parámetro.
    def get_creador(self, tipo):
        if tipo == "nodos": 
            return CreadorNodos.get_unica_instancia()

        if tipo == "aristas": 
            return CreadorAristas.get_unica_instancia()

        if tipo == "grafo":
            return CreadorGrafo.get_unica_instancia()
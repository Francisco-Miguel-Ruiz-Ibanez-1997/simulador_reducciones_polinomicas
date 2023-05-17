from .creador import Creador

from modelo_del_dominio.nodos.nodo import Nodo

#######################################################
# Clase que se encarga de la creación (fabricación) de
# de los nodos (problemas).
#######################################################
class CreadorNodos(Creador):

    _unica_instancia = None

    _lista_nodos_creados = []
    
    ### Getters ###

    # Devuelve la lista de nodos.
    def get_lista_nodos(self):
        return self._lista_nodos_creados

    # Instancia del creador.
    def get_unica_instancia():

        if CreadorNodos._unica_instancia == None:
            CreadorNodos._unica_instancia = CreadorNodos()

        return CreadorNodos._unica_instancia
    
    # Creación de nodos.
    def metodo_factoria(self):

        #### NODO SAT3ncf 
        texto_info = "Es el problema de la satisfacibilidad booleana (SAT) que se \nse presenta bajo la forma normal conjuntiva "\
            "(esto es, que la fórmula \nbooleana está formada por una conjunción (^) de cláusulas, " + "donde \ncada cláusula está formada por la disyunción (v) de máximo tres literales).\nPara el simulador implementado, se considerarán como literales las \nvariables x1,...,x9." + \
            "\n\nSAT3cnf es NP-Completo. Lo sabemos puesto que:\n\n ▶ SAT3cnf pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, decreta si es válida o no. " + \
            "\n\n ▶ Existe el problema SAT, que es NP-Completo (por el Teorema\nde Cook-Levin), y que se poli-reduce a SAT3cnf."

        nodo_sat3cnf = Nodo(0, "SAT3cnf", "SAT3", "red", texto_info, "https://en.wikipedia.org/wiki/Boolean_satisfiability_problem")

        #### NODO HAMPATH
        texto_info = "Es el lenguaje de triplas, grafo dirigido G, vértice \"s\" y vértice \"t\", tal que \nexiste un camino de \"s\" a \"t\" que pasa por todos los vértices exactamente \nuna vez."\
            "\n\nEl lenguaje lo podemos expresar como: \n\n" + "HAMPATH = {< G, s, t >| G es g.d. con cam. hamiltoniano de \"s\" a \"t\"}.\n\n\n" + \
            "HAMPATH es NP-Completo. Lo sabemos puesto que:\n\n ▶ HAMPATH pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, determina si es válida o no)." + \
            "\n\n ▶ Existe un problema, SAT3cnf, que es NP-Completo, y que se poli-\nreduce a HAMPATH. Dicha poli-reducción se puede simular en esta\naplicación."

        nodo_hampath = Nodo(1,"HAMPATH", "HAMP", "green", texto_info, "https://www.geeksforgeeks.org/proof-hamiltonian-path-np-complete/")

        #### NODO HAMCYCLE
        texto_info = "Es el lenguaje de 1-tuplas formadas por un grafo dirigido G tal que \nexiste un ciclo que pasa por todos los vértices exactamente \nuna vez."\
            "\n\nEl lenguaje lo podemos expresar como: \n\n" + "HAMCYCLE = {< G>| G es g.d. con ciclo. hamiltoniano}.\n\n\n" + \
            "HAMCYCLE es NP-Completo. Lo sabemos puesto que:\n\n ▶ HAMCYCLE pertenece a la clase NP (existe un decisor en tiempo polinomial que, dada una solución encontrada, determina si es válida o no)." + \
            "\n\n ▶ Existe un problema, HAMPATH, que es NP-Completo, y que se poli-\nreduce a HAMCYCLE. Dicha poli-reducción se puede simular en esta\naplicación."
        nodo_hamcycle = Nodo(2,"HAMCYCLE", "HAMC", "blue", texto_info, "https://www.geeksforgeeks.org/proof-that-hamiltonian-cycle-is-np-complete/")

        self._lista_nodos_creados = [nodo_sat3cnf, nodo_hampath, nodo_hamcycle]

        # Devolvemos nodos creados
        return [nodo_sat3cnf, nodo_hampath, nodo_hamcycle]
    
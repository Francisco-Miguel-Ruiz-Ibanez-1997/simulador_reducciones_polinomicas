import tkinter as tk
import customtkinter as ctk
import copy

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .etapa import Etapa

##############################################################################
# Clase que engloba la etapa 5 a realizar en la poli-reducción. 
# En esta etapa, se comprueba si la fórmula introducida por el
# usuario es satisfacible o no; en caso de serlo, se muestra el grafo
# resultante hamiltoniano obtenido; si no lo es, no hay camino hamiltoniano
# posible. Por tanto, se prueba que solo hay camino hamiltoniano si y solo si
# la fórmula es satisfacible, por lo que SAT3cnf se poli-reduce a HAMPATH.
##############################################################################
class Etapa5(Etapa):

    def __init__(self, ventana, gestor_etapas):

        super().__init__(ventana, gestor_etapas)

        self.etapa_5_1_realizada = False
        self.etapa_5_2_realizada = False
        self.etapa_5_3_realizada = False

        self.panel_5_1 = None
    
    ### Getters y setters ###

    def get_panel_5(self):
        return self.panel_5
    
    def get_panel_5_1(self):
        return self.panel_5_1
    
    def resetear_panel_5_1(self):
        self.panel_5_1 = None

    def get_panel_5_2(self):
        return self.panel_5_2
    
    def get_panel_5_3(self):
        return self.panel_5_3
    
    def get_etapa_realizada_5_1(self):
        return self.etapa_5_1_realizada
    
    def set_etapa_realizada_5_1(self, valor):
        self.etapa_5_1_realizada = valor
    
    def get_etapa_realizada_5_2(self):
        return self.etapa_5_2_realizada
    
    def set_etapa_realizada_5_2(self, valor):
        self.etapa_5_2_realizada = valor
    
    def get_etapa_realizada_5_3(self):
        return self.etapa_5_3_realizada
    
    def set_etapa_realizada_5_3(self, valor):
        self.etapa_5_3_realizada = valor
    
    def get_lista_valores_literales(self):
        return copy.deepcopy(self.lista_valores_literales)

    ### Lanzador de etapa ###

    ################# ETAPA 5.0 #################

    # Comprobamos que la fórmula introducida es satisfacible
    # o no. En caso de serlo, continuaremos con la reducción
    # hasta calcular el camino hamiltoniano en el grafo resultante.
    # Si no es satisfacbile, terminamos la reduccióon, afirmando que,
    # como no es satisfacible, entonces no hay camino hamiltoniano.

    def lanzar_subetapa_0(self):

        # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_5 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_5.pack(fill="both", expand=True)

        # Ahora comprobamos la satisfaciblidad de la fórmula:
        satisfacible, self.lista_valores_literales = self.gestor_etapas.formula_satisfacible()
        if satisfacible:

            lista_texto = []
            texto = "Ya hemos completado el grafo. Vamos a ver que cumple las condiciones \npara " \
                "ser una reducción SAT3cnf ≤p HAMPATH. \n\n" \
                "Ahora veremos que, como nuestra fórmula booleana sí es satisfacible,\n" \
                "sí hay un camino hamiltoniano entre los nodos \"s\" y \"t\" en el grafo \n" \
                "anteriormente calculado en la Etapa 4."
                
            lista_texto.append(texto)

            texto = "Para ello, mostremos antes los conceptos de zagzig y zigzag:\n\n El camino azul en los rombos inferiores " \
                "de ejemplo representa qué \n significa zagziguear y qué " \
                "significa zigzaguear en un subgrafo rombo \n asociado a un literal."
            lista_texto.append(texto)

            self.gestor_etapas.crear_panel_informacion(panel=self.panel_5, altura=110, anchura=480, num_pasos=2, lista_texto=lista_texto,
                                                        mostrar_sol=False, mostrar_formula=True, num_etapa=5)

            self.crear_panel_grafo(self.panel_5)

            panel_botones_5 = ctk.CTkFrame(self.panel_5)
            panel_botones_5.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

            boton_anterior = ctk.CTkButton(panel_botones_5, text="Anterior", command=lambda:self.gestor_etapas.anterior(4))
            boton_anterior.grid(row=0, column=0, padx=(10,20), pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_5, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(5.1))
            boton_siguiente.grid(row=0, column=1, padx=(20,10), pady=10)
        
        # Si la fórmula no es satisfacible, mostramos que no podemos construir el 
        # camino hamiltoniano
        else:

            self.formula_es_satisfacible = False

            # Añadimos a la lista de informaicon la calculada que la reduccion
            # no ha generado un grafo con camino hamiltoniano
            self.gestor_etapas.anadir_a_lista_informacion_calculada(1,2)

            panel_botones_fin = ctk.CTkFrame(self.panel_5)
            panel_botones_fin.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

            lista_texto = []
            texto = "En nuestro grafo no tendremos un camino hamiltoniano entre \"s\" y \"t\",\n" \
                    "puesto que la fórmula ϕ no es satisfacible, es decir, no hay ninguna\n " \
                    "asignación de valores a los literales que haga que la fórmula sea\n" \
                    "verdadera.\n\n" \
                    "Así que, como no es satisfacible no hay camino hamiltoniano (solamente \n" \
                    "habrá camino hamiltoniano entre los dos nodos si y sólo si la fórmula\n " \
                    "es satisfacible)."

            lista_texto.append(texto)
            self.gestor_etapas.crear_panel_informacion(panel=self.panel_5, altura=110, anchura=480, num_pasos=1, lista_texto=lista_texto,
                                                        mostrar_sol = False, mostrar_formula = True,num_etapa=5)

            boton_anterior = ctk.CTkButton(panel_botones_fin, text="Anterior",command=lambda:self.gestor_etapas.anterior(4))
            boton_anterior.grid(row=0, column=0, padx=10, pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_fin, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(6))
            boton_siguiente.grid(row=0, column=1, padx=10, pady=10)


    # Función que crea un grafo con forma de rombo simple para 
    # indicar al usuario qué es zigzaguear y zagziguear, 
    # mostrando el camino que se sigue en cada caso.
    def crear_panel_grafo(self, panel):

        panel_grafo = ctk.CTkFrame(panel)
        panel_grafo.pack(padx=20, pady=(30,10), side="top", fill="both", expand=True)
        panel_grafo.grid_rowconfigure(0, weight=1)
        panel_grafo.grid_columnconfigure(0, weight=1)
        panel_grafo.grid_columnconfigure(1, weight=1)

        grafo = nx.DiGraph()
        grafo.add_edges_from([(1,2),(1,3),(3,2),(2,4),(3,4)])

        figure = Figure(figsize=(2.5,3), dpi=100)
        axis = figure.add_subplot(111)

        # Creamos grafo rombo simple
        pos = {}
        for node in grafo.nodes():

            match node:
                case 1:
                    pos[node] = (2,3)

                case 2:
                    pos[node] = (1, 2)

                case 3:
                     pos[node] = (3, 2)
                
                case 4: 
                    pos[node] = (2, 1)

        etiquetas = {}

        for nodo in grafo.nodes():
            etiquetas[nodo] = ""

         # Nuevo mapa de color para arcos
        edge_colors = ['#CCCFCE','blue','blue','blue','#CCCFCE']

        grosor_arcos = [0.8, 1.5, 1.5, 1.5, 0.8]

        ############ 1º Grafo. Zagzig
        nx.draw_networkx(grafo, ax=axis, labels=etiquetas, pos=pos, edge_color=edge_colors, 
                            node_size=250, width=grosor_arcos)

        figure.suptitle("Zagzig")
        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas._tkcanvas.grid(row=0, column=0, sticky="nsew")

        ############ 2º Grafo. Zigzag
        figure = Figure(figsize=(2.5,3), dpi=100)
        axis = figure.add_subplot(111)
        edge_colors = ['blue','#CCCFCE','#CCCFCE','blue','blue']
        grosor_arcos = [1.5, 0.8, 0.8, 1.5, 1.5]
        grafo.remove_edge(3,2)
        grafo.add_edge(2,3)

        nx.draw_networkx(grafo, ax=axis, labels=etiquetas, pos=pos, edge_color=edge_colors,
                            node_size=250, width=grosor_arcos)

        figure.suptitle("Zigzag")
        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas._tkcanvas.grid(row=0, column=1, sticky="nsew")


    ################# ETAPA 5.1 #################

    # Informamos al usuario qué vamos a realizar ahora.
    # Explicamos qué es zigzaguear y zagziguear en un grafo,
    # pues lo vamos a necesitar posteriormente.

    def lanzar_subetapa_1(self):

        # Realizamos etapa
        self.etapa_5_1_realizada = True

        # Creamos nuevo panel
        self.panel_5_1 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_5_1.pack(fill="both",expand=True)

        lista_texto = []
        texto = "Dada la asignación anterior de valores de verdad a los literales  \n " \
                "que satisface ϕ, el camino hamiltoniano se determina en  \n" \
                "base a dicha asignación de valores.\n\n" \
                "Para cada cláusula Cj en ϕ, con j = 1 . . . k, se elige un literal que\n" \
                "en ella aparezca, y que tenga valor Verdadero según la \n" \
                "asignación de valores anterior." 
                
        lista_texto.append(texto)

        texto = "Por tanto, tomaremos, de las siguientes cláusulas, los \nsiguientes literales: \n\n"

        i = 1
        self.tupla_literales_seleccionados_verdaderos = []

        # Vamos a obtener los valores que han sido seleccionados para realizar el camino hamiltoniano.
        # Para ello, para cada cláusula, escogeremos un valor establecido a verdarero
        for clausula in self.gestor_etapas.get_clausulas_formula():
            for literal, valor_literal in self.lista_valores_literales:

                # Si el literal aparece negado pero se le ha asigando un valor False, en realidad vale
                # True en la cláusula, así que lo tomamos
                if ("!" + literal in clausula) and (valor_literal == False):
                    texto += "▶ Cláusula " + str(i) + ": literal " + literal + ", puesto que !" + literal + " = Verdadero" + ".\n"
                    self.tupla_literales_seleccionados_verdaderos.append((literal,str(i),False))
                    break
                
                # Si el literal aparece sin negar y se le ha asigando un valor True, lo tomamos
                elif ("!" + literal not in clausula) and (literal in clausula) and (valor_literal == True):
                    texto += "▶ Cláusula " + str(i) + ": literal " + literal +  ", puesto que " + literal + " = Verdadero" + ".\n"
                    self.tupla_literales_seleccionados_verdaderos.append((literal,str(i),True))
                    break
            i += 1
        
        # Ordenamos literales
        self.tupla_literales_seleccionados_verdaderos = sorted(self.tupla_literales_seleccionados_verdaderos)
        lista_texto.append(texto)

        texto = "Ahora haremos lo siguiente: \n\n" \
                "▶ Si xi = Verdadero, su rombo correspondiente se recorre zigzagueando \n " \
                "(de izquierda a derecha); si, además, el literal xi se ha elegido para la\n " \
                "j-ésima cláusula, se toma el desvío por el nodo horizontal cj al nodo Cj,\n " \
                "pues las flechas serán tales que permitan la ida y la vuelta sin pasar por \n" \
                "un nodo dos veces.\n\n" \
                "▶ Si xi = False, su rombo correspondiente se recorre zagzigueando \n " \
                "(de derecha a izquierda); si además, el literal !xi se ha elegido para la \n " \
                "j-ésima cláusula, se toma ese desvío por el nodo horizontal cj al nodo Cj, \n " \
                "pues las flechas serán tales que permitan la ida y la vuelta sin pasar por \n " \
                "un nodo  dos veces.\n\n " \
                "▶ Si varios literales de una misma cláusula son verdaderos, sólo se \n " \
                "toma el desvío una vez." 

        lista_texto.append(texto)

        # Ahora establecemos el camino hamiltoniano en base a los literales anteriormente
        # escogidos:
        texto = "Entonces el camino hamiltoniano es el que: \n\n"  
        i = 1
        for literal, clausula, valor in self.tupla_literales_seleccionados_verdaderos:
            if valor == True and clausula != -1:
                texto += "▶ " + str(i) + ": Recorre el rombo del literal " + literal + " zigzagueando (izq-der)\n" \
                "tomando desvío por c" + clausula + " a la cláusula " + clausula + " (nodo cláusula C" + clausula + ").\n\n"
            
            elif valor == False and clausula != -1:
                texto += "▶ " + str(i) + ": Recorre el rombo del literal " + literal + " zagzigueando (der-izq)\n" \
                "tomando desvío por c" + clausula + " a la cláusula " + clausula + " (nodo cláusula C" + clausula + ").\n\n"

            i+=1

        # El resto de literales que no han sido tomados los tendremos en cuenta a la hora de realizar
        # el camino hamiltoniano, pues no realizaremos desvío a los nodos cláusula que les corresponde:
        self.tupla_literales_restantes = []

        for literal in self.gestor_etapas.get_literales_formula():

            # Realizamos ahora el recorrido para aquellos literales no seleccionados anteriormente.
            if(any([literal in tup for tup in self.tupla_literales_seleccionados_verdaderos])) == False:
                
                for lit, valor in self.lista_valores_literales:
                    if lit == literal and valor == True:
                        texto += "▶ " + str(i) + ": Recorre el rombo del literal " + literal + " zigzagueando (izq-der)\n" \
                        "sin tomar desvío a un nodo cláusula. \n\n"
                        self.tupla_literales_restantes.append((literal, str(-1), valor))
                        i += 1

                    elif lit == literal and valor == False:
                        texto += "▶ " + str(i) + ": Recorre el rombo del literal " + literal + " zagzigueando (der-izq)\n" \
                        "sin tomar desvío a un nodo cláusula. \n\n"
                        self.tupla_literales_restantes.append((literal, str(-1), valor))
                        i += 1
                    
        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_5_1,altura=110,anchura=480,num_pasos=4,
                                                lista_texto=lista_texto,mostrar_sol = True, 
                                                mostrar_formula = True,num_etapa=5.1)

        panel_botones_5_1 = ctk.CTkFrame(self.panel_5_1)
        panel_botones_5_1.pack(padx=10,pady=(0,10),fill=tk.Y,side='bottom')

        boton_anterior = ctk.CTkButton(panel_botones_5_1, text="Anterior",command=lambda:self.gestor_etapas.anterior(5))
        boton_anterior.grid(row=0, column = 0,padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_5_1, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(5.2))
        boton_siguiente.grid(row=0, column = 1, padx=(20,10), pady=10)

    ################# ETAPA 5.2 #################

    # Etapa última de la poli-reducción. Mostramos el camino hamiltoniano
    # resultante.

    def lanzar_subetapa_2(self):
        # Realizamos etapa
        self.etapa_5_2_realizada = True

        # Creamos nuevo panel
        self.panel_5_2 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_5_2.pack(fill="both", expand=True)

        lista_texto = []
        texto = "Por tanto, siguiendo el 4º paso anteriormente visto, llegaremos \n"\
            "al grafo Gϕ con el camino hamiltoniano (de color verde):"
        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_5_2, altura=110, anchura=480, num_pasos=1, lista_texto=lista_texto,
                                                    mostrar_sol=False, mostrar_formula=True, num_etapa=5.2)


        grafo_2 = self.gestor_etapas.get_etapa(2).get_grafo()
        grafo_4 = self.gestor_etapas.get_etapa(4).crear_grafo(grafo_2)

        # Creamos el primer grafo
        f = Figure(figsize=(7,3), dpi=100)
        a = f.add_subplot(111)

        panel_botones_5_2 = ctk.CTkFrame(self.panel_5_2)
        panel_botones_5_2.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        self.panel_botones_5_2 = panel_botones_5_2


        # Representamos el grafo obtenido
        self.crear_panel_grafo_5_2(self.panel_5_2, grafo_4, f, a)

        boton_anterior = ctk.CTkButton(panel_botones_5_2, text="Anterior", command=lambda:self.gestor_etapas.anterior(5.1))
        boton_anterior.grid(row=0, column=0, padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_5_2, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(5.3))
        boton_siguiente.grid(row=0, column=2, padx=(20,20), pady=10)

    # Creamos el grafo con el camino hamiltoniano.
    def crear_panel_grafo_5_2(self, panel, grafo, figure, axis):

        self.gestor_etapas.anadir_a_lista_informacion_calculada(0,2)
        
        panel_grafo = ctk.CTkFrame(panel)
        panel_grafo.pack(padx=10, pady=(30,10), side="top", fill="both", expand=True)

        boton_agrandar= ctk.CTkButton(self.panel_botones_5_2, text="Agrandar/guardar\n imagen",
                                    fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(figure,5))
        boton_agrandar.grid(row=0, column=1, padx=5, pady=10)

        altura_max_grafo = 2*self.gestor_etapas.get_num_literales_formula()
        anchura_max_grafo = 3*self.gestor_etapas.get_num_clausulas_formula()+ 1

        ######### PRIMER GRAFO A PINTAR #########
        # El grafo que pintaremos tiene aristas rectas y curvas. Como un grafo no puede tener
        # ambos tipos de aristas para graficar, primero pintaremos el grafo con aristas rectas 
        # (el grafo rombo) y posteriormente, encima de este (sin machacarse), el grafo horizontal 
        # con las aristas curvas

        # Creamos el grafo horizontal
        grafo_horizontal = self.gestor_etapas.get_etapa(3).crear_grafo_horizontal()

        # Al grafo le quitamos los nodos horizontales
        grafo_1 = grafo
        grafo_1.remove_nodes_from(grafo_horizontal)

        recorrido = sorted(self.tupla_literales_seleccionados_verdaderos + self.tupla_literales_restantes)

        # Quitamos los arcos del grafo con forma de rombo para establecer camino hamiltoniano 
        # en el primer grafo:
        for literal, _, valor in recorrido:
            if valor == True:
                lista_aristas = list(e for e in grafo.edges() if (e[0] == literal or e[1] == literal + " "))
                grafo.remove_edges_from(lista_aristas)
            
            else:
                lista_aristas = list(e for e in grafo.edges() if (e[1] == literal or e[0] == literal + " "))
                grafo.remove_edges_from(lista_aristas)

        # Nuevo mapa de color para arcos
        edge_colors = []

        # Nuevo mapa de grosor para arcos
        grosor_arcos = []

        for arco in grafo.edges():
            edge_colors.append("green")
            grosor_arcos.append(1.5)

        color_map = self.gestor_etapas.get_etapa(2).crear_mapa_color_nodos(grafo_1)
        etiquetas = self.gestor_etapas.get_etapa(2).crear_etiquetas(grafo_1)
        pos = self.gestor_etapas.get_etapa(2).get_pos_rombo_y_horizontales()

        # Grafica el grafo
        nx.draw_networkx(grafo, ax=axis, labels=etiquetas, pos=pos, edge_color = edge_colors, node_color=color_map,
                            node_size=200,font_size=6,width=grosor_arcos)

        # Guardamos información para poli-reducciones posteriores
        self.gestor_etapas.anadir_a_lista_informacion_calculada((grafo, pos, etiquetas, color_map,edge_colors, 
                                                                    self.gestor_etapas.get_etapa(2).get_posiciones_nodos_s_t()),3)

        ######### SEGUNDO GRAFO A PINTAR  #########

        # Creamos grafo final:
        grafo_2 = nx.DiGraph()

        # Creamos el grafo con los nodos horizontales
        grafo_2 = self.gestor_etapas.get_etapa(3).crear_grafo(grafo_2)
        
        # Creamos el grafo con los nodos horizontales y los arcos unidos a las cláusulas
        grafo_2 = self.gestor_etapas.get_etapa(4).crear_grafo(grafo_2)

        # Nuevo mapa de posiciones para los nodos horizontales
        pos1={}
        columna=1
        fila=1
        for node in grafo_horizontal.nodes():
            cad = node.split("-")
                
            pos1[node] = (1+columna, altura_max_grafo - fila)
            if (int(cad[1]) == anchura_max_grafo):
                fila +=2
                columna=1
            else: 
                columna +=1

        # Nuevo mapa de color para nodos
        color_map = self.gestor_etapas.get_etapa(2).crear_mapa_color_nodos(grafo_2)

        # Eliminamos aristas sobrantes entre nodos horizontales y nodos cláusula
        for literal, clausula, valor in recorrido:
            lista_aristas = []

            # Si el valor del literal es Verdadero, zigzagueamos, quitando las aristas que van hacia la izqda
            if valor == True:
                num = literal.split("x")[1]
                
                # Eliminamos aristas izqdas horizontales
                for e0, e1 in self.gestor_etapas.get_etapa(3).get_lista_aristas_hacia_izqda():
                    if e0 == literal or e0 == literal + " " or "-" + "l" + num in e0:
                        lista_aristas.append((e0,e1))
                grafo_2.remove_edges_from(lista_aristas)

                # Eliminamos aristas entre los nodos pareja con las clásulas
                if clausula != "-1":
                    #pass

                    fila = 1
                    for lit in sorted(self.gestor_etapas.get_literales_formula()):
                        if lit == "x" + num:
                            break
                        else:
                            fila +=1

                    grafo_2.remove_edge(str(fila) + "-" + str(3*(int(clausula))-1) + "-l" + num, str(fila) + "-" + str(3*(int(clausula)))+ "-l" + num)
                    
                # Si el literal no se ha escogido para la cláusula en cuestión, no hacemos desvío:
                else:
                    for n1, n2 in self.gestor_etapas.get_etapa(4).get_aristas_desvios():
                        if "-l" + num in n1 or "-l" + num in n2:
                            grafo_2.remove_edge(n1,n2)

            # Si el valor del literal es Falso, zagzigueamos, quitando las aristas que van hacia la derecha
            else:
                num = literal.split("x")[1]
                
                # Eliminamos aristas derechas horizontales
                for e0, e1 in self.gestor_etapas.get_etapa(3).get_lista_aristas_hacia_derecha():
                    if e0 == literal or e0 == literal + " " or "-l" + num in e0:
                        
                        lista_aristas.append((e0,e1))
                grafo_2.remove_edges_from(lista_aristas)

                # Eliminamos aristas entre los nodos pareja con las clásulas
                if clausula != "-1":
                   #pass

                    fila = 1
                    for lit in sorted(self.gestor_etapas.get_literales_formula()):
                        if lit == "x" + num:
                            break
                        else:
                            fila +=1

                    grafo_2.remove_edge(str(fila) + "-" + str(3*(int(clausula))) + "-l" + num, str(fila) + "-" + str(3*(int(clausula))-1)+ "-l" + num)
                
                # Si el literal no se ha escogido para la cláusula en cuestión, no hacemos desvío:
                else:
                    for n1, n2 in self.gestor_etapas.get_etapa(4).get_aristas_desvios():
                        if "-l"+num in n1 or "-l" + num in n2:
                            grafo_2.remove_edge(n1,n2)

        # Ahora quitamos los desvíos de los nodos seleccionados cuyas cláusulas no han sido seleccionadas
        lista_aristas = []
        for n1, n2 in self.gestor_etapas.get_etapa(4).get_aristas_desvios():
            if ("-" in n1 ):
                literal = n1.split("-")[2]
                literal = "x" + literal.split("l")[1]

                num_clausula = n2.split("C")[1]

                # Escogemos solamente aquellas tuplas en las que aparece el literal en cuestión
                lista = [tuple for tuple in recorrido if literal in tuple]
                
                # Si la cláusula no aparece en la lista anterior, no hacemos desvío, por lo que eliminamos
                # dicha arista del grafo
                if any([num_clausula in tuple for tuple in lista]) == False:
                    if (n1, "C"+num_clausula) not in lista_aristas:
                        lista_aristas.append((n1, "C"+num_clausula))
            
            else:
                literal = n2.split("-")[2]
                literal = "x" + literal.split("l")[1]
                num_clausula = n1.split("C")[1]

                # Escogemos solamente aquellas tuplas en las que aparece el literal en cuestión
                lista = [tuple for tuple in recorrido if literal in tuple]

                # Si la cláusula no aparece en la lista anterior, no hacemos desvío, por lo que eliminamos
                # dicha arista del grafo
                if any([num_clausula in tuple for tuple in lista]) == False:
                    if ("C"+num_clausula,n2) not in lista_aristas:
                        lista_aristas.append(("C"+num_clausula,n2))

        grafo_2.remove_edges_from(lista_aristas)

        # Nuevo mapa de color para arcos
        edge_colors = []

        grosor_arcos = []

        for arco in grafo_2.edges():
            edge_colors.append("green")
            if "C" in arco[0] or "C" in arco[1]:
                grosor_arcos.append(1.5)
            else:
                grosor_arcos.append(1.5)

        etiquetas = self.gestor_etapas.get_etapa(2).crear_etiquetas(grafo_2)

        nx.draw_networkx(grafo_2, ax=axis, labels=etiquetas, pos=dict(pos,**pos1), node_color=color_map, 
                        edge_color=edge_colors,node_size=190,font_size=6,
                        connectionstyle='arc3, rad=0.4', width=grosor_arcos)


        # Guardamos información para poli-reducciones posteriores
        self.gestor_etapas.anadir_a_lista_informacion_calculada((grafo_2, dict(pos,**pos1), etiquetas, color_map, edge_colors, 
                                                                    self.gestor_etapas.get_etapa(2).get_posiciones_nodos_s_t()), 4)

        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    ################# ETAPA 5.3 #################

    # Realizamos la última etapa de la poli-reducción.
    # Informamos al usuario de que la reducción realizada
    # es polinómica.

    def lanzar_subetapa_3(self):

        # Realizamos etapa
        self.etapa_5_3_realizada = True

        # Creamos nuevo panel
        self.panel_5_3 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_5_3.pack(fill="both", expand=True)

        texto = "Ya hemos obtenido el resultado de la reducción: los vértices \"s\" y \"t\" junto con\n" \
            "el grafo con el camino hamiltoniano obtenido anteriormente, que\n"\
            "es f(ϕ) = Gϕ.\n\n\n" \
            "Ahora, ¿cómo se obtiene la asignación de verdad que demuestra que ϕ es\n" \
            "satisfacible? Lo que haremos será realizar el proceso inverso al realizado:\n\n" \
            "▶ Si el camino es de zigzagueo en el rombo i-ésimo, se le da a su \n" \
            "correspondiente literal xi el valor Verdadero. \n\n" \
            "▶ Si el camino es de zagzigueo en el rombo i-ésimo, se le da a su \n" \
            "correspondiente literal xi el valor Falso. \n\n" \
            "▶ Como cada nodo cláusula aparecerá en el camino, observando cómo se\n" \
            "toma el desvío, (desde el primer o segundo miembro del par de nodos\n" \
            "horizontales) se puede determinar qué literales de la cláusula \n" \
            "correspondiente están a Verdadero.\n\n\n" \
            "Sólo queda demostrar que la reducción es polinomial: esto es obvio pues\n" \
            "el tamaño del grafo que esta reducción genera es proporcional \n" \
            "linealmente al tamaño de ϕ (3 × k + 1 vértices)." \

        panel = ctk.CTkFrame(self.panel_5_3)
        panel.pack(padx=10, pady=(100,10),fill="both")

        # Creamos panel con información
        canvas = tk.Canvas(panel, width=40, height=185)
        canvas.configure(bg='#63BCE9')
        canvas.pack(side="left", padx=(10,0), pady=10)
        canvas.create_text(20, 150, text="Etapa " + str(5.3), angle=90, anchor="w", font=('Arial', 15,'bold'))

        textbox = ctk.CTkTextbox(panel, width=485, height= 400)
        textbox.insert("1.0", texto)
        textbox.configure(state="disabled")
        textbox.pack(padx=10, pady=10)

        panel_botones_5_3 = ctk.CTkFrame(self.panel_5_3)
        panel_botones_5_3.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        boton_anterior = ctk.CTkButton(panel_botones_5_3, text="Anterior", command=lambda:self.gestor_etapas.anterior(5.2))
        boton_anterior.grid(row=0, column = 0, padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_5_3, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(6))
        boton_siguiente.grid(row=0, column = 1, padx=(20,10), pady=10)
import tkinter as tk
import customtkinter as ctk
import copy

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .etapa import Etapa

####################################################################
# Clase que engloba la etapa 3 a realizar en la poli-reducción. 
# Se encarga de realizar el tercer grafo obtenido en la reducción    
# según la fórmula introducida, con los nodos horizontales
# añadidos al grafo, incluidos los nodos separadores, a los que 
# ahora añadimos las aristas que unen todos los nodos horizontales
# añadidos al grafo.
#####################################################################
class Etapa3(Etapa):

    def __init__(self, ventana, gestor_etapas):

        super().__init__(ventana, gestor_etapas)

        # Listas que contienen las aristas hacia derecha e izquierda
        # de los nodos horizontales del grafo. Usaremos estas listas, si procede,
        # en etapas posteriores
        self.lista_aristas_hacia_derecha = []
        self.lista_aristas_hacia_izqda = []
    
    ### Getters y setters ###

    def get_panel_3(self):
        return self.panel_3
    
    def get_lista_aristas_hacia_derecha(self):
        return copy.deepcopy(self.lista_aristas_hacia_derecha)
    
    def get_lista_aristas_hacia_izqda(self):
        return copy.deepcopy(self.lista_aristas_hacia_izqda)

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_3 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_3.pack(fill="both",expand=True)

        lista_texto = []
        texto = "Entre cada dos nodos sucesivos de las horizontales, se añaden arcos " \
                "\ndirigidos en las dos direcciones."
        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_3,altura=110, anchura=480, num_pasos=1, lista_texto=lista_texto, 
                                                    mostrar_sol=False, mostrar_formula=True, num_etapa=3)
        
        # Recuperamos el grafo_2 para pintar el tercer grafo de la reducción
        grafo_2 = self.gestor_etapas.get_etapa(2).get_grafo()

        # Figura para pintar el grafo
        f = Figure(figsize=(7,3), dpi=100)
        a = f.add_subplot(111)

        panel_botones_3 = ctk.CTkFrame(self.panel_3)
        panel_botones_3.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        self.panel_botones_3 = panel_botones_3

        # Representamos el grafo obtenido
        self.crear_panel_grafo(self.panel_3, grafo_2, f, a)

        boton_anterior = ctk.CTkButton(panel_botones_3, text="Anterior",command=lambda:self.gestor_etapas.anterior(2))
        boton_anterior.grid(row=0, column=0, padx=10, pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_3, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(4))
        boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

    # Crea el tercer grafo de la poli-reducción a partir del grafo
    # pasado por parámetro, al que se le añaden las aristas entre 
    # los nodos horizontales.
    def crear_grafo(self, grafo):

        num_nodos_horizontales_literal = 3*self.gestor_etapas.get_num_clausulas_formula() + 1
        contador = 1

        lista_literales = []
        for i in sorted(self.gestor_etapas.get_literales_formula()):
            lista_literales.append(i)

        literal = 0
        
        # Ahora añadimos aristas entre los nodos horizontales creados
        nodos_horizontales = self.gestor_etapas.get_etapa(2).get_nodos_horizontales()

        for i in range(0,len(nodos_horizontales)-1):
            if contador < num_nodos_horizontales_literal:
                nodo = nodos_horizontales[i]
                nodo_sig = nodos_horizontales[i+1]

                # Unimos nodo xi con el primer horizontal
                if contador == 1:
                    grafo.add_edge(lista_literales[literal],nodo)
                    self.lista_aristas_hacia_derecha.append((lista_literales[literal],nodo))
                    grafo.add_edge(nodo, lista_literales[literal])
                    self.lista_aristas_hacia_izqda.append((nodo,lista_literales[literal]))
            
                # Añadimos aristas entre los nodos horizontales
                grafo.add_edge(nodo,nodo_sig)
                grafo.add_edge(nodo_sig,nodo)

                contador += 1

                # Unimos nodo xi con el último horizontal
                if contador == num_nodos_horizontales_literal:
                    grafo.add_edge(nodo_sig, lista_literales[literal] + " ")
                    self.lista_aristas_hacia_derecha.append((nodo_sig,lista_literales[literal] + " "))
                    grafo.add_edge(lista_literales[literal] + " ",nodo_sig)
                    self.lista_aristas_hacia_izqda.append((lista_literales[literal] + " ",nodo_sig))
                    literal +=1
            
            else:
                contador = 1
 
        return grafo

    # Pinta el segundo grafo rombo (junto con nodos horizontales y separadores)
    # de la reducción, y las aristas entre nodos horizontales.
    def crear_panel_grafo(self, panel, grafo, figure, axis):

        panel_grafo = ctk.CTkFrame(panel)
        panel_grafo.pack(padx=10, pady=(30,10), side="top", fill="both", expand=True)

        boton_agrandar= ctk.CTkButton(self.panel_botones_3,  text="Agrandar/guardar\n imagen",
                                    fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(figure,3))
        boton_agrandar.grid(row=0, column=1, padx=10, pady=10)

        ######### PRIMER GRAFO A PINTAR #########
        # El grafo que pintaremos tiene aristas rectas y curvas. Como un grafo no puede tener
        # ambos tipos de aristas para graficar, primero pintaremos el grafo con aristas rectas 
        # (el grafo rombo) y posteriormente, encima de este (sin machacarse), el grafo horizontal 
        # con las aristas curvas
        grafo_horizontal = self.crear_grafo_horizontal()

        # Al grafo original, de la etapa 2, le quitamos los nodos horizontales
        grafo_1 = grafo
        grafo_1.remove_nodes_from(grafo_horizontal)

        # Mapa de color. Usamos mismo mapa de color que el de la etapa 2:
        color_map = self.gestor_etapas.get_etapa(2).crear_mapa_color_nodos(grafo_1)
        # Etiquetas a los nodos del grafo
        etiquetas = self.gestor_etapas.get_etapa(2).crear_etiquetas(grafo_1)
        # Posición de los nodos. Empleamos la misma que la de la etapa 2:
        pos = self.gestor_etapas.get_etapa(2).get_pos_rombo_y_horizontales()

        edge_colors = ["#CCCFCE" for arco in grafo_1.edges()]

        # Pintamos el primer grafo
        nx.draw_networkx(grafo_1, ax=axis, labels=etiquetas, pos=pos, edge_color=edge_colors,
                            node_color=color_map, node_size=200, font_size=6)


        ######### SEGUNDO GRAFO A PINTAR #########
        altura_max_grafo = 2*self.gestor_etapas.get_num_literales_formula()
        anchura_max_grafo = 3*self.gestor_etapas.get_num_clausulas_formula()+ 1

        # Calculamos posiciones del grafo para representarlo correctamente
        columna = 1
        fila = 1
        pos1 = {}
        for node in grafo_horizontal.nodes():
            str = node.split("-")
                
            pos1[node] = (1+columna, altura_max_grafo - fila)
            if (int(str[1]) == anchura_max_grafo):
                fila +=2
                columna=1
            else: 
                columna +=1

        # Creamos el segundo grafo (que será el de los nodos horizontales)
        grafo_2 = nx.DiGraph()
        grafo_2 = self.crear_grafo(grafo_2)

        # Mapa de color. Usamos mismo mapa de color que el de la etapa 2
        color_map = self.gestor_etapas.get_etapa(2).crear_mapa_color_nodos(grafo_2)

        # Etiquetas a los nodos del grafo
        etiquetas = self.gestor_etapas.get_etapa(2).crear_etiquetas(grafo_2)

        # Grafica el grafo
        nx.draw_networkx(grafo_2, ax=axis, labels=etiquetas, pos=dict(pos,**pos1), node_color=color_map,
                            node_size=190, font_size=6, connectionstyle='arc3, rad=0.4')

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Crea un grafo dirigido únicamente con nodos horizontales unidos entre sí
    # por aristas en ambas direcciones.
    def crear_grafo_horizontal(self):

        grafo = nx.DiGraph()

        # Nº de nodos horizontales que tendrá cada literal
        num_nodos_horizontales_literal = 3*self.gestor_etapas.get_num_clausulas_formula() + 1
        contador = 1

        # Calculamos el nº de nodos horizontales que tendrá el grafo
        nodos_horizontales = self.gestor_etapas.get_etapa(2).get_nodos_horizontales()

        # Creamos como tal el grafo, añadiendo aristas entre sus nodos
        for i in range(0,len(nodos_horizontales)-1):
            if contador < num_nodos_horizontales_literal:
                nodo = nodos_horizontales[i]
                nodo_sig = nodos_horizontales[i+1]
            
                grafo.add_edge(nodo,nodo_sig)
                self.lista_aristas_hacia_derecha.append((nodo,nodo_sig))

                grafo.add_edge(nodo_sig,nodo)
                self.lista_aristas_hacia_izqda.append((nodo_sig,nodo))

                contador += 1
            
            else:
                contador = 1
        
        return grafo
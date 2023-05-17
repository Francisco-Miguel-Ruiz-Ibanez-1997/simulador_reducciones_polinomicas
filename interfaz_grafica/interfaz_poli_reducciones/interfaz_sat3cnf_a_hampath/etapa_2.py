import tkinter as tk
import customtkinter as ctk
import copy

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .etapa import Etapa

###################################################################
# Clase que engloba la etapa 2 a realizar en la poli-reducción. 
# Se encarga de realizar el segundo grafo obtenido en la reducción    
# según la fórmula introducida, con los nodos horizontales
# añadidos al grafo, incluidos los nodos separadores.
###################################################################
class Etapa2(Etapa):

    def __init__(self, ventana, gestor_etapas):

        super().__init__(ventana, gestor_etapas)
    

    ### Getters and de setters ###

    def get_panel_2(self):
        return self.panel_2
    
    def get_grafo(self):
        return copy.deepcopy(self.grafo_2)
    
    def get_nodos_horizontales(self):
        return copy.deepcopy(self.nodos_horizontales)
    
    def get_nodos_separadores(self):
         return copy.deepcopy(self.nodos_separadores)

    def get_pos_rombo_y_horizontales(self):
        return copy.deepcopy(self.pos_rombo_y_horizontales)
    
    def get_posiciones_nodos_s_t(self):
        return copy.deepcopy((self.posicion_nodo_s, self.posicion_nodo_s_nueva, self.posicion_nodo_t, self.posicion_nodo_t_nueva))

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_2 = ctk.CTkFrame(self.ventana, corner_radius = 0)
        self.panel_2.pack(fill="both",expand=True)

        lista_texto = []
        texto = "Por cada literal (i.e. por cada rombo), añadiremos nodos en la horizontal, " \
                "\n entre los nodos de las puntas derecha e izquierda. Tendremos que añadir " \
                "\n 3 x k + 1 nodos, con k = núm cláusulas. Por tanto, añadiremos:\n "\
                "3 x " + f'{self.gestor_etapas.get_num_clausulas_formula()}' + " + 1 = " + str(3*self.gestor_etapas.get_num_clausulas_formula()+1) + " nodos."
        lista_texto.append(texto)

        texto = "Para añadir los nodos, lo haremos de la siguiente manera: añadiremos \n" \
            "dos nodos ci por cada cláusula Ci y nodos separadores (grises) que irán \n " \
            "situados entre los nodos de las puntas (correspondientes a los literales) \n" \
            "y entre cada par de nodos ci añadidos por cláusula."
        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_2, altura=110, anchura=480, num_pasos=2, lista_texto=lista_texto, 
                                                    mostrar_sol=False, mostrar_formula=True, num_etapa=2)
        
        # Construimos grafo_2 a partir de grafo_1
        grafo_1 = self.gestor_etapas.get_etapa(1).get_grafo()
        self.grafo_2 = self.crear_grafo(grafo_1)

        # Figura para pintar el grafo
        f = Figure(figsize=(8,3), dpi=100)
        a = f.add_subplot(111)

        panel_botones_2 = ctk.CTkFrame(self.panel_2)
        panel_botones_2.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        self.panel_botones_2 = panel_botones_2

        # Representamos el grafo obtenido
        self.crear_panel_grafo(self.panel_2, self.grafo_2, f, a)

        boton_anterior = ctk.CTkButton(panel_botones_2, text="Anterior",command=lambda:self.gestor_etapas.anterior(1))
        boton_anterior.grid(row=0, column=0, padx=10, pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_2, text="Siguiente",command=lambda:self.gestor_etapas.siguiente(3))
        boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

    # Crea el segundo grafo de la poli-reducción a partir del grafo en forma 
    # de rombo inicial junto con los nodos horizontales (y separadores) añadidos
    # a este.
    def crear_grafo(self, grafo):

        num_literales = self.gestor_etapas.get_num_literales_formula()
        num_nodos_a_crear = 3*self.gestor_etapas.get_num_clausulas_formula()+ 1

        # Por cada literal, creamos 3*k+1 nodos, con k = num_clásusulas
        self.nodos_separadores = []
        self.nodos_horizontales = []

        lista_literales = sorted(list(self.gestor_etapas.get_literales_formula()))

        # Creamos los nodos horizontales y separadores. Estos tendrán la forma:
        # fila-anchura-l_num_literal, para indicar en qué posición se colocan y a 
        # qué literal se corresponden
        for i in range(1, num_literales+1):
            conta = 0
            lit = lista_literales[i-1].split("x")[1]
            lit = "l"+lit
            for j in range(1,num_nodos_a_crear+1):
                grafo.add_node(str(i)+"-"+str(j)+"-"+lit)
                self.nodos_horizontales.append(str(i)+"-"+str(j)+"-"+lit)

                # Los nodos separadores ocupan las posiciones 1, 4, 7, etc
                if (3*conta + 1) == j:
                    self.nodos_separadores.append(str(i)+"-"+str(j)+"-"+lit)
                    conta += 1

        return grafo
    
     # Pinta el segundo grafo rombo (junto con nodos horizontales y separadores)
     # de la reducción.
    def crear_panel_grafo(self, panel, grafo, figure, axis):

        panel_grafo = ctk.CTkFrame(panel)
        panel_grafo.pack(padx=10, pady=(30,10), side="top", fill="both", expand=True)

        boton_agrandar = ctk.CTkButton(self.panel_botones_2, text="Agrandar/guardar\n imagen",
                                    fg_color=("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(figure,2))
        boton_agrandar.grid(row=0, column=1, padx=10, pady=10)

        # Calculamos posiciones del grafo para representarlo correctamente
        pos = {}
        i = 0
        pos_clausulas = 1

        altura_max_grafo = 2*self.gestor_etapas.get_num_literales_formula()
        anchura_max_grafo = 3* self.gestor_etapas.get_num_clausulas_formula()+ 1

        columna=1
        fila=1

        for node in grafo.nodes():
            if "C" in node:
                pos[node] = (anchura_max_grafo+3,altura_max_grafo - pos_clausulas)
                pos_clausulas += 1 

            elif node == "s":
                pos[node] = (anchura_max_grafo/2+1+0.5, altura_max_grafo)
                self.posicion_nodo_s = (anchura_max_grafo/2+1+0.5, altura_max_grafo)
                self.posicion_nodo_s_nueva = (-1, altura_max_grafo)

                i += 1
            
            elif node == "t":
                pos[node] = (anchura_max_grafo/2+1+0.5, 0)
                self.posicion_nodo_t = (anchura_max_grafo/2+1+0.5, 0)
                self.posicion_nodo_t_nueva = (-1, 0)

            elif " " in node :
                pos[node] = (anchura_max_grafo+2, altura_max_grafo - i)
                i += 1

            elif "x" in node:
                pos[node] = (1, altura_max_grafo - i)

            elif "-" in node:
                cadena = node.split("-")
                
                pos[node] = (1+columna, altura_max_grafo - fila)
                if (int(cadena[1]) == anchura_max_grafo):
                    fila +=2
                    columna=1
                else: 
                    columna +=1

            else: 
                pos[node] = (anchura_max_grafo/2+1+0.5, altura_max_grafo - i)
                i += 1

        self.pos_rombo_y_horizontales = pos

        edge_colors = ["#CCCFCE" for arco in grafo.edges()]

        # Grafica el grafo
        nx.draw_networkx(grafo,ax=axis,labels=self.crear_etiquetas(grafo) ,pos=self.pos_rombo_y_horizontales,
                            edge_color = edge_colors, node_color=self.crear_mapa_color_nodos(grafo),node_size=200,font_size=6)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Crea mapa de color a los nodos del grafo.
    def crear_mapa_color_nodos(self, grafo):

        color_map = []
        for node in grafo.nodes():
            if "C" in node:
                color_map.append('#F15125')
            elif node in self.nodos_separadores:
                color_map.append('#B9BCBF')
            else:
                color_map.append('#4188F3')
        return color_map

    # Crea etiquetas a los nodos del grafo.
    def crear_etiquetas(self, grafo):

        etiquetas = {}
        num_clausula = 1
        contador = 0
        for nodo in grafo.nodes():
            if "-" in nodo and nodo not in self.nodos_separadores:
                etiquetas[nodo] = "c" + str(num_clausula)
                contador += 1
                if contador == 2:
                    contador=0
                    if num_clausula == self.gestor_etapas.get_num_clausulas_formula():
                        num_clausula = 1
                    else:
                        num_clausula +=1

            elif nodo in self.nodos_separadores :
                etiquetas[nodo] = ""

            elif "u" in nodo:
                etiquetas[nodo] = ""

            else:
                etiquetas[nodo] = nodo

        return etiquetas


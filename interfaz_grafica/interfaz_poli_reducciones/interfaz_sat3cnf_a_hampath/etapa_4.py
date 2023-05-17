import tkinter as tk
import customtkinter as ctk

import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import copy

from .etapa import Etapa

##################################################################
# Clase que engloba la etapa 4 a realizar en la poli-reducción. 
# Se encarga de realizar el cuarto grafo obtenido en la reducción    
# según la fórmula introducida, con los nodos horizontales
# añadidos al grafo, incluidos los nodos separadores e incluidas
# las aristas que unen todos los nodos horizontales, además de las 
# aristas que unen las parejas de nodos cláusula horizontales con 
# los nodos cláusula.
##################################################################
class Etapa4(Etapa):

    def __init__(self, ventana, gestor_etapas):

        super().__init__(ventana, gestor_etapas)
    
    ### Getters y setters ###

    def get_panel_4(self):
        return self.panel_4
    
    def get_aristas_desvios(self):
        return copy.deepcopy(self.aristas_desvios)

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_4 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_4.pack(fill="both", expand=True)

        lista_texto = []
        texto = "Ahora, si xi aparece en la cláusula Cj de la fórmula booleana ϕ, \n" \
        "entonces se establece un arco desde la pareja horizontal cj que hay en \n" \
        "el rombo de xi hasta el nodo Cj de forma que el primer nodo de la pareja\n" \
        "va hacia Cj y de este parte un arco hasta el segundo nodo de la pareja."
        lista_texto.append(texto)

        texto = "Si por el contrario aparece en la cláusula Cj el negado de xi, procedemos\n" \
        "de la misma forma, pero invirtiendo la navegabilidad de los arcos \n " \
        "anteriores. "
        lista_texto.append(texto)

        self.gestor_etapas.crear_panel_informacion(panel=self.panel_4, altura=110, anchura=480, num_pasos=2, lista_texto=lista_texto, 
                                                    mostrar_sol=False, mostrar_formula=True, num_etapa=4)
        
        grafo_2 = self.gestor_etapas.get_etapa(2).get_grafo()
        grafo_4 = self.crear_grafo(grafo_2)

        # Creamos el primer grafo
        f = Figure(figsize=(7,3), dpi=100)
        a = f.add_subplot(111)

        self.panel_grafo = None

        panel_botones_4 = ctk.CTkFrame(self.panel_4)
        panel_botones_4.pack(padx=10,pady=(5,10), fill=tk.Y, side='bottom')

        panel_botones_4_1 = ctk.CTkFrame(panel_botones_4, fg_color=("gray81", "gray20"))
        panel_botones_4_1.grid(row=0, column=1, padx=0, pady=5)

        self.panel_botones_4_1 = panel_botones_4_1

        # Representamos el grafo obtenido
        self.crear_panel_grafo(self.panel_4, grafo_4, f, a)

        boton_anterior = ctk.CTkButton(panel_botones_4, text="Anterior", command=lambda:self.gestor_etapas.anterior(3))
        boton_anterior.grid(row=0, column=0, padx=10, pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_4, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(5))
        boton_siguiente.grid(row=0, column=4, padx=10, pady=10)

    # Crea el grafo con el que los nodos pareja horizontales se unen mediante 
    # aristas con los nodos cláusula, partiendo del grafo obtenido en las etapas
    # anteriores.
    def crear_grafo(self, grafo):

        # Contadores
        pos_literal = 0
        pos_clausula = 0
        pareja = 0
        lista_literales = sorted(self.gestor_etapas.get_literales_formula())

        self.aristas_desvios = []

        # Recorremos la lista de nodos que hemos introducido horizontalmente al grafo original
        for nodo in self.gestor_etapas.get_etapa(2).get_nodos_horizontales():

            # Obviamos los nodos separadores
            if (nodo in self.gestor_etapas.get_etapa(2).get_nodos_separadores()) == False:

                # Si pasamos la pareja de nodos, reseteamos contadores
                if pareja == 2:
                    pareja = 0

                    # Comprobamos si pasamos al siguiente literal (siguiente nivel del grafo)
                    if pos_clausula + 1 == self.gestor_etapas.get_num_clausulas_formula():
                        pos_literal += 1
                        pos_clausula = 0

                    else:
                        pos_clausula += 1        

                # Comprobamos si aparece el literal negado en la cláusula
                if ("!" + lista_literales[pos_literal] in self.gestor_etapas.get_clausulas_formula()[pos_clausula]) and pareja == 0:
                    grafo.add_edge("C" + str(pos_clausula + 1),nodo)
                    self.aristas_desvios.append(("C" + str(pos_clausula + 1),nodo))
                    pareja += 1
                
                elif ("!" + lista_literales[pos_literal] in self.gestor_etapas.get_clausulas_formula()[pos_clausula]) and pareja == 1:
                    grafo.add_edge(nodo,"C" + str(pos_clausula + 1))
                    self.aristas_desvios.append((nodo,"C" + str(pos_clausula + 1)))
                    pareja += 1

                # Comprobamos si aparece el literal sin negar en la cláusula
                elif lista_literales[pos_literal] in self.gestor_etapas.get_clausulas_formula()[pos_clausula] and pareja == 0:
                    grafo.add_edge(nodo,"C" + str(pos_clausula + 1))
                    self.aristas_desvios.append((nodo,"C" + str(pos_clausula + 1)))
                    pareja += 1
                    
                elif lista_literales[pos_literal] in self.gestor_etapas.get_clausulas_formula()[pos_clausula] and pareja == 1:
                    grafo.add_edge("C" + str(pos_clausula + 1),nodo)
                    self.aristas_desvios.append(("C" + str(pos_clausula + 1),nodo))
                    pareja += 1
                
                # Si no encontramos nada en la cláusula, avanzamos al siguiente nodo
                else: 
                    pareja+=1

        return grafo

    # Pinta el grafo obtenido en esta etapa, que incluye las aristas que unen
    # los nodos cláusula con los nodos pareja-horizontales.
    def crear_panel_grafo (self, panel, grafo, figure, axis):
        
        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()
            figure = Figure(figsize=(7,3), dpi=100)
            axis = figure.add_subplot(111)
        
        panel_grafo = ctk.CTkFrame(panel)
        panel_grafo.pack(padx=10, pady=(10,5), side="top", fill="both", expand=True)

        boton_agrandar= ctk.CTkButton(self.panel_botones_4_1, text="Agrandar/guardar\n imagen",
                                    fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(figure, 4))
        boton_agrandar.grid(row=0, column=0, padx=5, pady=5)

        boton_cambiar_colores= ctk.CTkButton(self.panel_botones_4_1, text="Cambiar colores de los arcos",
                                            fg_color=("#8F61D4","#9A42D5"), hover_color=("#8041A9","#8041A9"),
                                            command=lambda:self.crear_panel_grafo(panel, grafo, figure, axis))

        boton_cambiar_colores.grid(row=1, column=0, padx=5, pady=(5,5))

        altura_max_grafo = 2 * self.gestor_etapas.get_num_literales_formula()
        anchura_max_grafo = 3 * self.gestor_etapas.get_num_clausulas_formula() + 1

        ######### PRIMER GRAFO A PINTAR  #########
        # El grafo que pintaremos tiene aristas rectas y curvas. Como un grafo no puede tener
        # ambos tipos de aristas para graficar, primero pintaremos el grafo con aristas rectas 
        # (el grafo rombo) y posteriormente, encima de este (sin machacarse), el grafo horizontal 
        # con las aristas curvas

        grafo_horizontal = self.gestor_etapas.get_etapa(3).crear_grafo_horizontal()

        # Al grafo le quitamos los nodos horizontales
        grafo_1 = grafo
        grafo_1.remove_nodes_from(grafo_horizontal)
        
        color_map = self.gestor_etapas.get_etapa(2).crear_mapa_color_nodos(grafo_1)
        etiquetas = self.gestor_etapas.get_etapa(2).crear_etiquetas(grafo_1)
        pos = self.gestor_etapas.get_etapa(2).get_pos_rombo_y_horizontales()

        edge_colors = ["#CCCFCE" for arco in grafo_1.edges()]

        # Grafica el grafo
        nx.draw_networkx(grafo_1, ax=axis, labels=etiquetas, pos=pos, edge_color=edge_colors,
                            node_color=color_map, node_size=200, font_size=6)

        # Guardamos información para poli-reducciones posteriores
        self.gestor_etapas.anadir_a_lista_informacion_calculada((grafo_1, pos, etiquetas, color_map, edge_colors, 
                                                                    self.gestor_etapas.get_etapa(2).get_posiciones_nodos_s_t()),0)

        ######### SEGUNDO GRAFO A PINTAR  #########
        grafo_2 = nx.DiGraph()

        # Creamos el grafo con los nodos horizontales
        grafo_2 = self.gestor_etapas.get_etapa(3).crear_grafo(grafo_2)
        
        # Creamos el grafo con los nodos horizontales y los arcos unidos a las cláusulas
        grafo_2 = self.crear_grafo(grafo_2)

        # Nuevo mapa de posiciones para los nodos horizontales
        pos1={}
        columna=1
        fila=1
        for node in grafo_horizontal.nodes():
            str = node.split("-")
                
            pos1[node] = (1+columna, altura_max_grafo - fila)
            if (int(str[1]) == anchura_max_grafo):
                fila +=2
                columna=1
            else: 
                columna +=1

        # Nuevo mapa de color para nodos
        color_map = self.gestor_etapas.get_etapa(2).crear_mapa_color_nodos(grafo_2)

        # Nuevo mapa de color para arcos
        edge_colors = []

        # Colores de los arcos para los nodos "pareja"
        colores_parejas = []

        posicion_color = 0

        grosor_arcos = []

        for arco in grafo_2.edges():

            # Si encontramos un arco con un nodo cláusula, le asociamos un color
            if ("C" in arco[0]):

                # Asignamos color aleatorio
                hexadecimal = ["#"+''.join([random.choice('abcdf0123456789') for i in range(6)])]
                colores_parejas.append((hexadecimal[0],arco[1]))
                edge_colors.append(hexadecimal[0])
                grosor_arcos.append(2)
                
                posicion_color +=1
        
            # Si no estamos ante un arco entre nodos "pareja" y nodo cláusula, pintamos el arco de color negro
            else:
                edge_colors.append("#CCCFCE")
                posicion_color +=1
                grosor_arcos.append(1)
        
        # Ahora asociamos a cada pareja de nodos horizontales el mismo color
        for color, nodo in colores_parejas:
            
            posicion_color = 0

            # Recorremos los arcos en busca de los nodos "pareja"
            for arco in grafo_2.edges():
                nodo1 = arco[0]
                nodo2 = arco[1]

                # Cogemos solo los nodos "pareja", obviando los nodos separadores, los nodos xi y los nodos cláusula
                if ("x" not in nodo1) and ("x" not in nodo2) and (nodo1 not in self.gestor_etapas.get_etapa(2).get_nodos_separadores()) and \
                    (nodo2 not in self.gestor_etapas.get_etapa(2).get_nodos_separadores()):

                    primer_numero = int(nodo.split("-")[0])
                    segundo_numero = int(nodo.split("-")[1])

                    # Comprobamos que el nodo tomado es el que quedaba en la pareja
                    if "C" not in nodo1 and nodo != nodo1 and "C" in nodo2:
                        primer_numero_1 = int(nodo1.split("-")[0])
                        segundo_numero_2 = int(nodo1.split("-")[1])

                        # Comprobamos que ambos nodos pareja están en el mismo nivel horizontal (mismo rombo literal)
                        if primer_numero == primer_numero_1:

                            # Comprobamos que estamos ante el componente que faltaba para completar la pareja.
                            # Podría ser el nodo anterior o el posterior
                            if (segundo_numero == segundo_numero_2 + 1) or (segundo_numero == segundo_numero_2 - 1):
                                edge_colors[posicion_color] = color
                                grosor_arcos[posicion_color] = 2

                # Actualizamos posición del color dentro de la lista de arcos
                posicion_color += 1
        
        etiquetas = self.gestor_etapas.get_etapa(2).crear_etiquetas(grafo_2)
        
        # Grafica el grafo
        nx.draw_networkx(grafo_2, ax=axis, labels=etiquetas, pos=dict(pos,**pos1), node_color=color_map,
                            edge_color=edge_colors, node_size=190, font_size=6,
                            connectionstyle='arc3, rad=0.4', width=grosor_arcos)
        
        # Guardamos información para poli-reducciones posteriores
        self.gestor_etapas.anadir_a_lista_informacion_calculada((grafo_2, dict(pos,**pos1), etiquetas, color_map, edge_colors, 
                                                                    self.gestor_etapas.get_etapa(2).get_posiciones_nodos_s_t()),1)
        # Pintamos el grafo
        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.panel_grafo = panel_grafo
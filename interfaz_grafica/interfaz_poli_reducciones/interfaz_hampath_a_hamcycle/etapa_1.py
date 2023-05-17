import tkinter as tk
import customtkinter as ctk

import networkx as nx
from matplotlib.figure import Figure
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import string

from ...interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa

#########################################################################
# Clase que engloba la etapa 1 a realizar en la poli-reducción. 
# Se encarga de establecer en el grafo seleccionado en la etapa anterior
# un ciclo hamiltoniano.
#########################################################################
class Etapa1(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

        self.panel_grafo = None

    ### Getters ###

    def get_panel_1(self):
        return self.panel_1

    ### Lanzador de etapa ###

    def lanzar_etapa(self):

        # Si no hay grafo hamiltoniano, mostramos mensaje de error
        if self.gestor_etapas.get_grafo_inicial() == None:

            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"),size=(50, 50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text = 'Selecciona el grafo hamiltoniano para comenzar \n la poli-reducción.')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

        else:

            self.gestor_etapas.get_etapa(0).get_panel_0_2().pack_forget()

            # Si la etapa está realizada, la mostramos
            if self.etapa_realizada == True:
                self.panel_1.pack(padx=10, pady=10, fill="both", expand=True)

            else:
                self.etapa_realizada = True

                self.panel_1 = ctk.CTkFrame(self.ventana, corner_radius = 0)
                self.panel_1.pack(fill="both", expand=True)

                # Opción 1: partir del nuevo grafo
                if not self.gestor_etapas.get_grafo_previo_escogido():

                    lista_texto = []
                    ultimo_nodo = list(string.ascii_lowercase)[self.gestor_etapas.get_etapa(0).get_num_nodos()-1]
                    texto = "Sea G el grafo dirigido anterior conteniendo el conjunto de vértices V, el\n" \
                        "conjunto de aristas E y los vértices \"a\", \"" + ultimo_nodo +"\" ∈ V. Sea < G, a, " + ultimo_nodo +" > su codifica-\n " \
                        "ción. Entonces, aplicando la función f(< G, a, " + ultimo_nodo +" >) = G', obtenemos G' un \ngrafo " \
                        "dirigido con V' = V ∪ {a', " + ultimo_nodo +"'} y E' = E ∪ {("+ultimo_nodo+", " + ultimo_nodo +"'), (" + ultimo_nodo +"', a'), (a', a)}."
                    lista_texto.append(texto)

                    texto = "Lo que hemos hecho ha sido, a través de la función f, añadir dos nodos,\n \"a' \"" \
                        " y \"" + ultimo_nodo +"' \" al grafo G, además de las aristas ("+ultimo_nodo+" ," + ultimo_nodo +"'), (" + ultimo_nodo +"', a') y (a', a).La función\n" \
                        "f construida es, por tanto, polinomial. \n\n"
                    
                    # Si hay camino hamiltoniano, lo indicamos
                    if self.gestor_etapas.get_grafo_nuevo_con_camino():
                        texto += "Con esto, ya hemos obtenido el grafo G', que contiene un ciclo \nhamiltoniano.\nSe ve claramente que G ∈ HAMPATH "\
                                " si y sólo si G' ∈ HAMCYCLE."

                    # Si no lo hay, lo indicamos también
                    else:
                        texto += "Con esto, ya hemos obtenido el grafo G', que, como podemos observar,\n no contiene un ciclo hamiltoniano. \nSe ve claramente que G ∈ HAMPATH"\
                                " si y sólo si G' ∈ HAMCYCLE."
                    lista_texto.append(texto)
                
                # Opción 2: partir del grafo hamiltoniano previo
                else:
                    lista_texto = []
                    texto = "Sea G el grafo dirigido anterior conteniendo el conjunto de vértices V, el\n" \
                        "conjunto de aristas E y los vértices \"s\", \"t\" ∈ V. Sea < G, s, t > su codifica-\n " \
                        "ción. Entonces, aplicando la función f(< G, s, t >) = G', obtenemos G' un \ngrafo " \
                        "dirigido con V' = V ∪ {s', t'} y E' = E ∪ {(t , t'), (t', s'), (s', s)}."
                    lista_texto.append(texto)

                    texto = "Lo que hemos hecho ha sido, a través de la función f, añadir dos nodos,\n \"s' \"" \
                        " y \"t' \" al grafo G, además de las aristas (t, t'), (t', s') y (s', s). La función\n" \
                        "f construida es, por tanto, polinomial. \n\n"

                    # Informamos si se ha generado ciclo hamiltoniano
                    if self.gestor_etapas.get_lista_resultados_previos()[2] == 0:
                        texto += "Con esto, ya hemos obtenido el grafo G', que contiene un ciclo \nhamiltoniano.\nSe ve claramente que G ∈ HAMPATH"\
                                " si y sólo si G' ∈ HAMCYCLE."

                    else:
                        texto += "Con esto, ya hemos obtenido el grafo G', que, como podemos observar,\n no contiene un ciclo hamiltoniano.\nSe ve claramente que G ∈ HAMPATH"\
                                " si y sólo si G' ∈ HAMCYCLE."

                    lista_texto.append(texto)

                panel_info = ctk.CTkFrame(self.panel_1)
                panel_info.pack(padx=10, pady=(10,0))

                canvas = tk.Canvas(panel_info, width=40, height=185)
                canvas.configure(bg='#63BCE9')
                canvas.pack(side="left", padx=(10,0), pady=10)
                canvas.create_text(20, 150, text="Etapa " + str(1) ,angle=90, anchor="w", font=('Arial', 15,'bold'))

                panel_pasos = ctk.CTkTabview(panel_info, height=110, width=450)
                panel_pasos.pack(side="top", padx=10, pady=10, fill="both")

                for paso in range (1, 3):
                    panel_pasos.add("Paso " + str(paso) + "º")

                    label = ctk.CTkLabel(panel_pasos.tab("Paso " + str(paso) + "º"), text=lista_texto[paso-1])
                    label.pack(fill="both")
        
                panel_botones_1 = ctk.CTkFrame(self.panel_1)
                panel_botones_1.pack(padx=10, pady=(5,10), fill=tk.Y, side='bottom')

                panel_botones_1_1 = ctk.CTkFrame(panel_botones_1, fg_color=("gray81", "gray20"))
                panel_botones_1_1.grid(row=0, column=1, padx=0, pady=5)

                self.panel_botones_1_1 = panel_botones_1_1

                # Si no tenemos grafo previo, procedemos a crear el ciclo
                # con el nuevo grafo, seleccionado anteriormente por el usuario
                if not self.gestor_etapas.get_grafo_previo_escogido():
                    self.crear_panel_grafo_nuevo(self.crear_grafo())
                
                else:
                    # Creamos el ciclo hamiltoniano en el grafo hamiltoniano creado en la poli-reducción
                    # anterior
                    self.crear_panel_grafo_previo(self.crear_grafo_1())

                boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.2))
                boton_anterior.grid(row=0, column=0, padx=10, pady=10)

                boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(2))
                boton_siguiente.grid(row=0, column=2, padx=10, pady=10)
    
    #############################################################
    ############ CASO CREAR NUEVO GRAFO HAMILTONIANO ############
    #############################################################

    # Crea el grafo con el ciclo hamiltoniano.
    def crear_grafo(self):

        # Cargamos el grafo inicial
        grafo = self.gestor_etapas.get_grafo_inicial()

        ultimo_nodo = list(string.ascii_lowercase)[self.gestor_etapas.get_etapa(0).get_num_nodos()-1]

        nodo_anadir_1 = "a'"
        nodo_anadir_2 = ultimo_nodo + "'"

        grafo.add_node(nodo_anadir_1)
        grafo.add_node(nodo_anadir_2)

        grafo.add_edge(ultimo_nodo, nodo_anadir_2)
        grafo.add_edge(nodo_anadir_2, nodo_anadir_1)
        grafo.add_edge(nodo_anadir_1, "a")

        self.ultimo_nodo = ultimo_nodo

        return grafo
    
    # Crea el panel del nuevo grafo con el ciclo hamiltoniano.
    def crear_panel_grafo_nuevo(self, grafo):

        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()
        
        self.panel_grafo = ctk.CTkFrame(self.panel_1)
        self.panel_grafo.pack(padx=10, pady=10, fill="both", expand=True)

        fig = Figure(figsize=(5,4), dpi=100)
        axis = fig.add_subplot(111)

        boton_agrandar= ctk.CTkButton(self.panel_botones_1_1, text="Agrandar/guardar\n imagen",
                                    fg_color = ("#70AB94","#4D8871"), hover_color = ("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(fig,1))
        boton_agrandar.grid(row=0,column=0, padx=5, pady=5)

        boton_repintar = ctk.CTkButton(self.panel_botones_1_1, text="Repintar grafo",
                                            fg_color = ("#8F61D4","#9A42D5"), hover_color=("#8041A9","#8041A9"),
                                            command=lambda:self.crear_panel_grafo_nuevo(grafo))
        boton_repintar.grid(row=1,column=0, padx=5, pady=(5,5))

        # Mapa de color
        color_map = ['#32B246' if (node == "a'") or (node == self.ultimo_nodo + "'") else '#4188F3' for node in grafo.nodes()]

        edge_colors = ['#32B246' if (edge[0]=="a'") or (edge[1] == "a'") or (edge[0]==self.ultimo_nodo + "'") or 
                        (edge[1] ==self.ultimo_nodo + "'") else '#CCCFCE' for edge in grafo.edges()]

        grosor_arcos = [2 if (edge[0]=="a'") or (edge[1] == "a'") or (edge[0]==self.ultimo_nodo + "'") or 
                        (edge[1] ==self.ultimo_nodo + "'") else 1 for edge in grafo.edges()]

        nx.draw_networkx(grafo, ax=axis, node_color=color_map, edge_color=edge_colors,   
                            width=grosor_arcos)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    ################################################################
    ############ CASO CARGAR GRAFO HAMILTONIANO  PREVIO ############
    ################################################################
    
    # Crea el grafo cargado previamente con el ciclo hamiltoniano.
    def crear_grafo_1(self):

        nodo_anadir_1 = "s'"
        nodo_anadir_2 = "t'"

        grafo = nx.DiGraph()

        grafo.add_node("s")
        grafo.add_node(nodo_anadir_1)

        grafo.add_node("t")
        grafo.add_node(nodo_anadir_2)

        grafo.add_edge("t", nodo_anadir_2)
        grafo.add_edge(nodo_anadir_2, nodo_anadir_1)
        grafo.add_edge(nodo_anadir_1, "s")

        return grafo
    
    # Crea el panel del grafo cargado previamente con el ciclo hamiltoniano.
    def crear_panel_grafo_previo(self, tercer_grafo):

        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()
        
        self.panel_grafo = ctk.CTkFrame(self.panel_1)
        self.panel_grafo.pack(padx=10, pady=10, fill="both", expand=True)

        fig = Figure(figsize=(5,4), dpi=100)
        axis = fig.add_subplot(111)

        boton_agrandar= ctk.CTkButton(self.panel_botones_1_1, text="Agrandar/guardar\n imagen",
                                    fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                    command=lambda:self.gestor_etapas.agrandar_grafo(fig,1))
        boton_agrandar.pack(padx=5, pady=5)

        # Comprobamos si el grafo tenía camino hamiltoniano o no
        if self.gestor_etapas.get_lista_resultados_previos()[2] == 0:
            index = 3

        else:
            index = 0

        # 1º Grafo
        (grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t) = self.gestor_etapas.get_lista_resultados_previos()[index]

        nx.draw_networkx(grafo,ax=axis,labels=etiquetas, pos=pos, node_color=color_map, 
                                edge_color=edge_colors, node_size=190,font_size=6)

        # 2º Grafo
        (grafo, pos, etiquetas, color_map, edge_colors, posiciones_s_t) = self.gestor_etapas.get_lista_resultados_previos()[index+1]

        nx.draw_networkx(grafo,ax=axis,labels=etiquetas, pos=pos, node_color=color_map, 
                                edge_color=edge_colors, node_size=190,font_size=6, connectionstyle = 'arc3, rad=0.4')        
        
        pos_s_t = posiciones_s_t

        # 3º Grafo. Es el grafo con la completación del ciclo hamiltoniano.
        pos_tercer_grafo = {}
        for nodo in tercer_grafo.nodes():
            if "'" in nodo:
                if "s" in nodo:
                    pos_tercer_grafo[nodo] = (pos_s_t[1][0], pos_s_t[1][1])
                else:
                    pos_tercer_grafo[nodo] = (pos_s_t[3][0], pos_s_t[3][1])
            else:
                if "s" in nodo:
                    pos_tercer_grafo[nodo] = (pos_s_t[0][0], pos_s_t[0][1])
                else:
                    pos_tercer_grafo[nodo] = (pos_s_t[2][0], pos_s_t[2][1])
        
        color_map = ['#B2D7FC' if "'" in node else '#4188F3' for node in tercer_grafo.nodes()]
        edge_colors = ['blue' for edge in tercer_grafo.edges()]
        grosor_arcos = [2 for edge in tercer_grafo.edges()]

        nx.draw_networkx(tercer_grafo, ax=axis, pos=pos_tercer_grafo, node_color=color_map, edge_color=edge_colors,
                            width=grosor_arcos, node_size=190, font_size=6)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(fig, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both", expand=True)


import tkinter as tk
import customtkinter as ctk
import copy

from PIL import Image
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from .etapa import Etapa

#########################################################################
# Clase que engloba la etapa 1 a realizar en la poli-reducción. 
# Se encarga de realizar el primer grafo de la reducción, en base
# a la fórmula que ha introducido el usuario. Se indica además los pasos
# que se han seguido para que el usuario sea consciente de ellos.
#########################################################################
class Etapa1(Etapa):

    def __init__(self, ventana, gestor_etapas):
        
        super().__init__(ventana, gestor_etapas)

    ### Getters y setters ###

    def get_panel_1(self):
        return self.panel_1
    
    def get_grafo(self):
        return copy.deepcopy(self.grafo_inicial)

    ### Lanzador de etapa ###

    def lanzar_etapa(self):
        
        # Si la fórmula es correcta, pasamos a la siguiente ventana
        if self.gestor_etapas.get_formula_correcta() == True:
            
            # Si introducimos más fórmulas, reseteamos las etapas para que las realicemos 
            # con los nuevos datos introducidos
            if self.gestor_etapas.get_num_formulas_introducidas() > 1:
                self.gestor_etapas.set_num_formulas_introducidas(1)
                self.gestor_etapas.resetear_etapas()

            self.gestor_etapas.get_etapa(0).get_panel_0_2().pack_forget()

            # Realizamos etapa
            self.etapa_realizada = True
 
            self.panel_1 = ctk.CTkFrame(self.ventana, corner_radius = 0)
            self.panel_1.pack(fill="both", expand=True)

            lista_texto = []
            texto = "Añadiremos un subgrafo con forma de rombo por cada literal. \nComo "  \
            "tenemos " + f'{self.gestor_etapas.get_num_literales_formula()}' + \
            " literal(es), tendremos " + f'{self.gestor_etapas.get_num_literales_formula()}' + " rombo(s)." 
            lista_texto.append(texto)

            texto = "La punta superior del primer rombo será el que haga de \"s\", y la última \n del " + \
            "último rombo hará de \"t\". \nTodas las flechas (aristas) apuntarán hacia abajo."
            lista_texto.append(texto)

            texto = "Ahora, añadimos un nodo Ci por cada cláusula. Como tenemos " + f'{self.gestor_etapas.get_num_clausulas_formula()}' + "\ncláusula(s), añadiremos " +\
                    f'{self.gestor_etapas.get_num_clausulas_formula()}' + " nodo(s) Ci."       
            lista_texto.append(texto)

            self.gestor_etapas.crear_panel_informacion(panel=self.panel_1, altura=110, anchura=450, num_pasos=3, lista_texto=lista_texto,
                                                        mostrar_sol=False, mostrar_formula=True, num_etapa=1)

            # Creamos el primer grafo
            f = Figure(figsize=(5,3), dpi=100)
            a = f.add_subplot(111)

            panel_botones_1 = ctk.CTkFrame(self.panel_1)
            panel_botones_1.pack(padx=10, pady=(0,10), side='bottom', fill=tk.Y)
            self.panel_botones_1 = panel_botones_1

            self.grafo_inicial = self.crear_grafo()

            self.crear_panel_grafo(self.panel_1, self.grafo_inicial, f, a)

            boton_anterior= ctk.CTkButton(panel_botones_1, text="Anterior", command=lambda:self.gestor_etapas.anterior(0.2))
            boton_anterior.grid(row=0, column=0,padx=10, pady=10)

            boton_siguiente = ctk.CTkButton(panel_botones_1, text="Siguiente", command=lambda:self.gestor_etapas.siguiente(2))
            boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

        # Si la fórmula booleana es incorrecta (o no se ha introducido aún), no podremos pasar a la 
        # siguiente etapa. Mostramos mensaje de error 
        else:
            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius=0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50,50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text='Fórmula booleana incorrecta')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

    # Crea el primer grafo de la poli-reducción, representando el grafo en forma 
    # de rombo.
    def crear_grafo(self):

        # Creamos grafo dirigido
        G = nx.DiGraph()

        # Añadimos los nodos iniciales s y t
        G.add_node("s")
        G.add_node("t")

        num_clausulas = self.gestor_etapas.get_num_clausulas_formula()

        # Añadimos tantos nodos aislados por cada cláusula que tengamos
        for i in range(1,num_clausulas+1):
            G.add_node("C"+str(i))

        # Ahora añadiremos los nodos del rombo. Serán: 2 * num_clausulas + (num_clausulas - 1)
        literal = 1
        contador = 1

        lista_literales = []
        for i in sorted(self.gestor_etapas.get_literales_formula()):
            lista_literales.append(i)

        # Si estamos ante el primer literal, ponemos aristas entre nodo s y nodos p1
        G.add_node(lista_literales[0])
        G.add_edge("s",lista_literales[0])

        G.add_node(lista_literales[0]+" ")
        G.add_edge("s",lista_literales[0]+" ")

        num_literales = self.gestor_etapas.get_num_literales_formula()
        for i in range(3,(2*num_literales + (num_literales-1))+1):

            # Añadimos dos nodos por cada literal encontrado
            if contador <= 2:
                if contador == 1:
                    G.add_node(lista_literales[literal-1]) # Aquí metemos los nodos x1, 
                                                           # pero como los rechaza, no pasa nada
                        
                else:
                    G.add_node(lista_literales[literal-1]+" ")
                       
                contador += 1
                
            # Añadimos nodo vacío, unión de los rombos
            else:
                G.add_node("u"+str(literal))
                G.add_edge(lista_literales[literal-1],"u"+str(literal))
                G.add_edge("u"+str(literal),lista_literales[literal])
                G.add_edge(lista_literales[literal-1]+" ","u"+str(literal))
                G.add_edge("u"+str(literal),lista_literales[literal]+" ")

                contador = 1
                literal +=1

        # Si estamos ante el último literal, ponemos aristas entre los últimos nodos y t
        if len(lista_literales) == 1:
            G.add_edge(lista_literales[0],"t")
            G.add_edge(lista_literales[0]+" ","t")

        else:
            G.add_edge(lista_literales[literal-1],"t")
            G.add_edge(lista_literales[literal-1]+" ","t")

        return G
    
    # Pinta el primer grafo rombo de la reducción.
    def crear_panel_grafo(self, panel, grafo, figure, axis):

        panel_grafo = ctk.CTkFrame(panel)
        panel_grafo.pack(padx=20,pady=(30,10),side="top", fill="both", expand=True)

        boton_agrandar = ctk.CTkButton(self.panel_botones_1, text="Agrandar/guardar\n imagen",
                                        fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"),
                                        command=lambda:self.gestor_etapas.agrandar_grafo(figure,1))
        boton_agrandar.grid(row=0,column=1,padx=10,pady=10)


        # Calculamos posiciones del grafo para representar un rombo
        pos = {}
        i = 0
        pos_clausulas = 1

        altura_max_grafo = 2*self.gestor_etapas.get_num_literales_formula()
        
        for node in grafo.nodes():
            if "C" in node:
                pos[node] = (4,altura_max_grafo - pos_clausulas)
                pos_clausulas += 1 

            elif node == "s":
                pos[node] = (2, altura_max_grafo)
                i += 1
            
            elif node == "t":
                pos[node] = (2, 0)

            elif " " in node :
                pos[node] = (3, altura_max_grafo - i)
                i += 1

            elif "x" in node:
                pos[node] = (1, altura_max_grafo - i)

            else: 
                pos[node] = (2, altura_max_grafo - i)
                i += 1
        
        # Mapa de color
        color_map = ['#F15125' if "C" in node else '#4188F3' for node in grafo.nodes()]

        # Etiquetas de los nodos del grafo
        etiquetas = {}
        for nodo in grafo.nodes():
            if "u" in nodo:
                etiquetas[nodo] = ""

            else:
                etiquetas[nodo] = nodo

        # Grafica el grafo
        nx.draw_networkx(grafo, ax=axis, labels=etiquetas, pos=pos, node_color=color_map)

        # Pintamos en la figura
        canvas = FigureCanvasTkAgg(figure, panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
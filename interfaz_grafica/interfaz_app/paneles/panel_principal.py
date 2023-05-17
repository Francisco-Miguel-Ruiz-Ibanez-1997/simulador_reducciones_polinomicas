
import tkinter as tk
import customtkinter as ctk

from PIL import Image
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import random

from .panel import Panel
from ..ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp
from ..ventanas.ventanas_hijas.ventana_secundaria import VentanaSecundaria
from ...interfaz_poli_reducciones.repertorio_interfaces_poli_reduccion import RepertorioInterfacesPoliReduccion

from controlador.controlador import Controlador

######################################################
# Clase que contiene el panel principal del simulador.
######################################################
class PanelPrincipal(Panel):

    # Constructor.
    def __init__(self, ventana=None):

        self.figure = None

        # Constructor del padre
        super().__init__(ventana)

        self.crear_panel_superior()
        self.crear_panel_grafo()
        self.crear_panel_inferior()

    ########################################################################
    ############################ PANEL SUPERIOR ############################ 
    ########################################################################

    # Crea el panel superior de la aplicación, que contiene la selección
    # de problemas para escoger a poli-reducir.
    def crear_panel_superior(self):

        # Creamos panel superior
        panel_superior = ctk.CTkFrame(self, fg_color=("#6889B1","gray20"))
        panel_superior.pack(side="top", padx=10, pady=20)
        panel_superior.grid_rowconfigure(0, weight=1)
        panel_superior.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(panel_superior, fg_color=("#A3B5CC","gray25"), text="Simulador de reducciones polinómicas",
                                font=ctk.CTkFont(size=20, weight="bold"))
        label.grid(row=0,column=0, padx=10, pady=(10,0), columnspan=4, sticky="nsew")

        # Creamos tabview para selección de problema 1
        panel_seleccion_1 = ctk.CTkTabview(panel_superior, height=50, width=200)
        panel_seleccion_1.grid(row=1, column=0, padx=(20,10), pady=10, sticky="nsew")
        panel_seleccion_1.add("1º problema")

        self.problema_1 = ""
        lista_valores = ["------"]
        for nombre_nodo in Controlador.get_unica_instancia().get_lista_nombres_nodos():
            lista_valores.append(nombre_nodo)
        combobox = ctk.CTkComboBox(panel_seleccion_1.tab("1º problema"), values=lista_valores, command=self.escoger_problema_1)
        combobox.pack(fill=ctk.X, padx=5, pady=5, side="top")

        # Panel símbolo de la poli-reducción
        panel_simbolo = ctk.CTkTabview(panel_superior, height=55, width=40, fg_color=("#6889B1","gray20"))
        panel_simbolo.grid(row=1, column=1, pady=10, sticky="nsew")

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/simbolo_poli_reduccion.jpg"), size=(55, 40))
        label = ctk.CTkLabel(panel_simbolo, image=bg_image, text="")
        label.grid(row=3,column=0, sticky="nsew")

        # Creamos tabview para selección de problema 2
        panel_seleccion_2 = ctk.CTkTabview(panel_superior, height=50, width=200)
        panel_seleccion_2.grid(row=1, column=2, padx=(10,20), pady=10, sticky="nsew")
        panel_seleccion_2.add("2º problema")

        self.problema_2 = ""
        combobox1 = ctk.CTkComboBox(panel_seleccion_2.tab("2º problema"), values=lista_valores, command=self.escoger_problema_2)
        combobox1.pack(fill=ctk.X, padx=5, pady=5, side="top")

    # Determinamos el problema escogido a reducir.
    def escoger_problema_1(self, problema_1 : str):
        if problema_1 != "------":
            self.problema_1 = problema_1
            alias_nodo = Controlador.get_unica_instancia().get_alias_nodo_por_nombre(self.problema_1)
            color_nodo = Controlador.get_unica_instancia().get_color_nodo_por_nombre(self.problema_1)
            label_info = [alias_nodo, color_nodo]
            self.crear_ventana_emergente(texto="Has seleccionado " + self.problema_1, label_info=label_info, error=False)
        else:
            self.problema_1 = ""

    # Determinamos el problema escogido al que reducimos.
    def escoger_problema_2(self, problema_2 : str):
        if problema_2 != "------":
            self.problema_2 = problema_2
            alias_nodo = Controlador.get_unica_instancia().get_alias_nodo_por_nombre(self.problema_2)
            color_nodo = Controlador.get_unica_instancia().get_color_nodo_por_nombre(self.problema_2)
            label_info = [alias_nodo, color_nodo]
            self.crear_ventana_emergente(texto="Has seleccionado " + self.problema_2, label_info=label_info, error=False)
        else:
            self.problema_2 = ""

    ########################################################################
    ############################ PANEL UNIVERSO ############################ 
    ########################################################################

    # Creamos panel del grafo principal (universo) del simulador. En él se 
    # muestra un  universo de problemas junto con las poli-reducciones a 
    # realizar, las realizadas y otras aún sin definir.
    def crear_panel_grafo(self):

        self.panel_central = ctk.CTkFrame(self,fg_color=("#4F769D","gray20"))
        self.panel_central.pack(pady=(0,0), padx=30, side='top', expand=True, fill="both")

        label = ctk.CTkLabel(self.panel_central, fg_color=("#A3B5CC","gray25"), text = "Universo de problemas y poli-reducciones entre ellos",font=ctk.CTkFont(size=17, weight="bold"))
        label.pack(side="top",padx=10, pady=(10,0), fill="both")

        # Panel para mostrar el grafo de relaciones
        self.panel_grafo = ctk.CTkFrame(self.panel_central, width=600, height=100)
        self.panel_grafo.pack(fill='both', pady=10, padx=10, side='left', expand=True)
        self.construir_grafo(aristas_a_actualizar=[])

        # Panel para la leyenda del grafo
        panel_leyenda = ctk.CTkFrame(self.panel_central, width=200, height=200)
        panel_leyenda.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        panel_leyenda.grid_rowconfigure(0, weight=1)
        panel_leyenda.grid_columnconfigure(0, weight=1)

        panel_leyenda_1 = ctk.CTkFrame(panel_leyenda,width=200,height=200)
        panel_leyenda_1.grid(pady=(10,10), padx=10, row=0, column=0, sticky="nswe")
        self.crear_leyenda(panel_leyenda_1)

        panel_leyenda_2 = ctk.CTkFrame(panel_leyenda, width=200, height=200)
        panel_leyenda_2.grid(pady=10, padx=10, row=2, column=0, sticky="nswe")

        boton_resetear_universo = ctk.CTkButton(panel_leyenda_2, text="Resetear poli-reducciones", fg_color = ("#8F61D4","#9A42D5"), 
                                                    hover_color=("#8041A9","#8041A9"),
                                                    command=lambda:self.resetear_poli_reducciones())
        boton_resetear_universo.pack(padx=10, pady=10, side="bottom")

        boton_repintar_universo = ctk.CTkButton(panel_leyenda_2, text="Repintar universo", fg_color = "#34649F",
                                                command=lambda:self.actualizar_grafo(Controlador.get_unica_instancia().get_aristas_a_actualizar()))
        boton_repintar_universo.pack(padx=10, pady=10, side="bottom")

    # Resetea el universo de problemas, poniendo las aristas que unen los nodos de color NEGRO.
    def resetear_poli_reducciones(self):
        
        Controlador.get_unica_instancia().resetear_aristas_a_actualizar()
        self.actualizar_grafo(Controlador.get_unica_instancia().get_aristas_a_actualizar())

        # Reseteamos las listas de informaciones calculadas, para que no interfieran con
        # otras simulaciones de las mismas aristas que pudiéramos lanzar. Reseteamos también
        # la completación de la poli-reducción (imponemos que no esté completada, para volver a lanzarla)
        Controlador.get_unica_instancia().resetear_poli_reducciones()

    # Función que construye un grafo inicial, e.d., presenta el universo de problemas, y las
    # poli-reducciones entre ellos.
    def construir_grafo(self, aristas_a_actualizar):

        if self.figure != None:
            self.figure = None
            self.figure = Figure(figsize=(5,3.1), dpi=99)
        
        else:
            self.figure = Figure(figsize=(5,3.1), dpi=99)

        axis = self.figure.add_subplot(111)
        g = nx.DiGraph()

        # Posiciones de los nodos en nuestro universoalias
        pos = {}
        pos_x = 0
        pos_y = 0

        # Etiquetas para los nodos
        etiquetas = {}

        # Añadimos al universo de lenguajes los lenguajes de nuestro grafo de reducciones y algunos lenguajes
        # aún sin definir
        for id_nodo in Controlador.get_unica_instancia().get_lista_id_nodos():
            
            # Nuestros problemas definidos en el programa
            g.add_node(id_nodo)

            # Asignamos alias a los nodos problemas a representar en el universo
            etiquetas[id_nodo] = Controlador.get_unica_instancia().get_alias_nodo_por_id(id_nodo)
            
            pos[id_nodo] = (pos_x,pos_y)

            pos_x += 1
            pos_y += 1

            # Reseteamos posiciones
            if pos_y == 6:
                pos_y = 0
                
            if pos_x % 2 == 0:
                pos_x = pos_x - 2

            num_nodos = Controlador.get_unica_instancia().get_num_nodos()

            # Si terminamos de pintar nuestro universo real, mostraremos este más nodos vacíos que no
            # representan nada (para una mejor visualización de nuestro universo de lenguajes)
            if id_nodo == num_nodos - 1:
                for i in range (id_nodo + 1, num_nodos + 15):
                    g.add_node(i) 

                    etiquetas[i] = ""
                    
                    pos[i] = (pos_x,pos_y)

                    pos_x += 1
                    pos_y += 1

                    # Reseteamos posiciones
                    if pos_y == 6:
                        pos_y = 0
                        
                    elif pos_x % 2 == 0:
                        pos_x = pos_x - 2
                    
        # Creamos las aristas que están implementadas en el simulador
        for (id_nodo_src, id_nodo_dest) in Controlador.get_unica_instancia().get_lista_tuplas_aristas():
            g.add_edge(id_nodo_src, id_nodo_dest)

        # Creamos unas aristas arbitrarias obtenidas al azar de nodos vacíos
        for i in range(num_nodos, num_nodos + 10):
            nodo_a = random.randrange(num_nodos, 10, 1)
            nodo_b = random.randrange(num_nodos, 10, 1)

            # Evitar ciclo 
            if nodo_a != nodo_b:
                g.add_edge(nodo_a, nodo_b)

        # Pinta aristas
        edge_colors = []
        grosor_arcos = []
        for edge in g.edges():
            n1 = edge[0]
            n2 = edge[1]

            # Si alguno de los nodos que contiene la arista es de nuestro universo implementado, pintamos 
            # la arista de color NEGRO o NARANJA, según veremos a continuación
            if n1 in Controlador.get_unica_instancia().get_lista_id_nodos():
                
                # Mostramos en color NEGRO las poli-reducciones que puede realizar el usuario, para orientarlo.
                # Si los nodos no están en las aristas a actualizar, entonces las pintamos de NEGRO 
                if [n1,n2] not in aristas_a_actualizar:
                    edge_colors.append("black")
                    grosor_arcos.append(1)

                # Actualizamos las aristas del grafo principal cuando el usuario haya realizado una poli-
                # reducción. En tal caso, mostraremos una arista de color NARANJA mostrando la realización
                # por parte del usuario de la reducción
                else:
                    for arista_nueva in aristas_a_actualizar:
                        
                        if (n1 == arista_nueva[0] and n2 == arista_nueva[1]) or (n1 == arista_nueva[1] and n2 == arista_nueva[0]):
                            edge_colors.append("orange")
                            grosor_arcos.append(3)

            else:
                edge_colors.append("gray")
                grosor_arcos.append(1)

        # Color de nodos
        color_map = []

        # Color de los nodos implementandados hasta ahora
        for nodo in Controlador.get_unica_instancia().get_lista_nodos():
            color_map.append(Controlador.get_unica_instancia().get_color_nodo(nodo))

        # Color de los nodos vacíos
        for i in range(num_nodos+1, len(g.nodes())+1):
            color_map.append("gray")

        nx.draw_networkx(g, ax=axis, node_shape="s", with_labels=False, edge_color=edge_colors,
                            node_color=color_map, width=grosor_arcos, pos=pos, node_size=420, alpha=0.8)
        
        nx.draw_networkx_labels(g, ax=axis, pos=pos, labels=etiquetas, font_color="white", font_size=7)
        
        # Ocultamos ejes
        axis.axis(False)

        # Grafica el universo en la figura
        canvas = FigureCanvasTkAgg(self.figure, self.panel_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both" , expand=True)

    # Función que se encarga de actualizar el grafo con las poli-reducciones
    # que el usuario ha realizado hasta ahora. Si el usuario realiza una reducción
    # entre un nodo A y otro B, se pintará la arista de color NARANJA entre A y B, 
    # simbolizando que la reducción se ha realizado.
    def actualizar_grafo(self, aristas_a_actualizar):

        if self.panel_grafo != None:
            self.panel_grafo.pack_forget()

        self.panel_grafo = ctk.CTkFrame(self.panel_central, width=600, height=100)
        self.panel_grafo.pack(fill='both', expand=True, pady=10, padx=10, side='left')
        self.construir_grafo(aristas_a_actualizar)

    # Crea la leyenda asociada al grafo principal (universo) del simulador.
    def crear_leyenda(self, panel):
        
        label = ctk.CTkLabel(panel,text="Leyenda de problemas", font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(side="top", pady=(10,10), padx=5)

        canvas = tk.Canvas(panel, width=200, height=170)
        scrolly = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollx = tk.Scrollbar(panel, orient="horizontal", command=canvas.xview)

        i = 0

        # Separación label-canvas
        label = tk.Label(canvas, text="  ")
        canvas.create_window(0, i*50, anchor='nw', window=label)
        i +=1

        for nodo in Controlador.get_unica_instancia().get_lista_nodos():

            # Colores de los nodos según nuestro grafo implementado
            label = tk.Label(canvas, text=Controlador.get_unica_instancia().get_alias_nodo(nodo), font=tk.font.Font(size=6),fg="white", background=Controlador.get_unica_instancia().get_color_nodo(nodo))
            canvas.create_window(10, i*50, anchor='nw', window=label, width=25, height=25)

            # Nombre nodos de problemas NP
            label = tk.Label(canvas, text=" " + Controlador.get_unica_instancia().get_nombre_nodo(nodo))
            canvas.create_window(45, i*50, anchor='nw', window=label)
            
            i += 1

        # Color leyenda gris resto de problemas NP
        label = tk.Label(canvas, text="     ", background="gray")
        canvas.create_window(10, i*50, anchor='nw', window=label, width=25, height=25)

        # Otros problemas NP
        label = tk.Label(canvas, text=" OTRO PROBLEMA")
        canvas.create_window(45, i*50, anchor='nw', window=label)

        i += 1

        # Separación canvas-scrollbarx
        label = tk.Label(canvas, text="  ")
        canvas.create_window(0, i*50, anchor='nw', window=label)

        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)
        canvas.configure(scrollregion=canvas.bbox('all'), xscrollcommand=scrollx.set)

        scrollx.pack(side="bottom", fill=tk.X)
        scrolly.pack(side="right", fill=tk.Y)
        canvas.pack(side="left", fill="both", expand=True)
    
    ########################################################################
    ############################ PANEL INFERIOR ############################ 
    ########################################################################

    # Función que crea el panel inferior de la aplicación, que 
    # contiene el botón para lanzar la simulación.
    def crear_panel_inferior(self):

        # Panel para botón de inicio de simulación
        panel_btn = ctk.CTkFrame(self, fg_color=("#6889B1","gray20"))
        panel_btn.pack(fill=tk.X, pady=20, padx=30, side='bottom')

        boton_iniciar = ctk.CTkButton(panel_btn, text="Iniciar simulador", fg_color="#2A7C37", hover_color="#329141", border_width=1, border_color="#BBBDBC",
                                        command=lambda:self.iniciar_simulacion(), width=250)    
        boton_iniciar.pack(pady=10, padx=10)
        
    # Función que crea una ventana o de error y muestra
    # como mensaje el texto pasado como parámetro.
    def crear_ventana_emergente(self, texto, label_info, error):

        ventana_emergente = VentanaPopUp(ventana_padre = self.ventana)
        ventana_emergente.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

        panel = ctk.CTkFrame(ventana_emergente, corner_radius = 0)
        panel.pack()

        if error:
            ventana_emergente.title("Error")

            # Imagen aviso
            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
            label = ctk.CTkLabel(panel, image=bg_image, text="")
            label.pack(padx=10, pady=10)
        
        else:
            ventana_emergente.title("Info")

            # Imagen info
            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info.png"), size=(50, 50))
            label = ctk.CTkLabel(panel, image=bg_image, text="")
            label.pack(padx=10, pady=10)

        lbl = ctk.CTkLabel(panel, text=texto)
        lbl.pack(padx=10, pady=(0,10))

        if label_info != None:
            lbl = ctk.CTkLabel(panel, text=" " + label_info[0] + " ", bg_color = label_info[1], text_color="#F7F8F9")
            lbl.pack(padx=10, pady=(0,20))

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_emergente.exit())
        boton_aceptar.pack(padx=10, pady=(0,10))

        ventana_emergente.center()

    # Función que inicia simulación.
    def iniciar_simulacion(self):

        # Comprobación de errores
        if (self.problema_1 == "") and (self.problema_2 == ""):

            self.crear_ventana_emergente("No se ha introducido ningún problema", label_info=None, error=True)

        elif (self.problema_1 == "") and (self.problema_2 != ""):

            self.crear_ventana_emergente("No se ha introducido el 1º problema", label_info=None, error=True)

        elif (self.problema_1 != "") and (self.problema_2 == ""):

            self.crear_ventana_emergente("No se ha introducido el 2º problema", label_info=None, error=True)

        elif(self.problema_1 == self.problema_2):

            self.crear_ventana_emergente("Ambos problemas introducidos son IGUALES", label_info=None, error=True)

        else:
            # Lanzamos simulador

            # Comprobamos si hay una simulación ya en marcha
            if Controlador.get_unica_instancia().get_num_simulaciones() == 1:
                self.crear_ventana_emergente(texto="Ya hay una simulación en marcha", label_info=None, error=True)

            else:

                # Buscamos las aristas del grafo entre los nodos origen y destino, 
                # para calcular las poli-reducciones a realizar.
                aristas = []
                aristas = Controlador.get_unica_instancia().buscar_aristas(self.problema_1
, self.problema_2, aristas)
        
                # Cuando no encuentra poli-reduccion
                if len(aristas) == 0:

                    self.crear_ventana_emergente(texto = "No se ha encontrado poli-reducción entre " \
                                    + "los problemas seleccionados", label_info=None, error=False)
                
                else:

                    # Iniciamos simulación. Establecemos que tenemos en marcha una simulación.
                    Controlador.get_unica_instancia().set_num_simulaciones(1)

                    # Calculamos si las poli_reducciones han sido ya completadas o no
                    completacion_poli_reducciones = [True if not Controlador.get_unica_instancia().get_poli_reduccion_completada(arista) else False for arista in aristas]
                    
                    # Si no todas están completadas, mostramos mensaje indicando qué vamos a hacer
                    if any(completacion_poli_reducciones):

                        # Informamos de la poli-reducción (o poli-reducciones) que vamos a realizar hasta ahora:
                        texto = "Se van a realizar las siguientes \npoli-reducciones:"

                        nombre_nodos_inicio = []
                        nombre_nodo_src = ""
                        nombre_nodo_dest = ""

                        for arista in aristas:

                            # Mostramos información de las poli-reducciones que se van a lanzar (completadas o no, luego ya informamos de ello)
                            nombre_nodo_src = Controlador.get_unica_instancia().get_arista_nombre_src(arista)

                            if nombre_nodo_src not in nombre_nodos_inicio:
                                nombre_nodos_inicio.append(nombre_nodo_src)
                            
                            nombre_nodo_dest = Controlador.get_unica_instancia().get_arista_nombre_dest(arista)

                            if nombre_nodo_dest not in nombre_nodos_inicio:
                                nombre_nodos_inicio.append(nombre_nodo_dest)

                        ventana_inicio_reduccion = self.crear_ventana_inicio_fin_simulacion(texto, nombre_nodos_inicio, None, None, False)
                        ventana_inicio_reduccion.resizable(0,0)
                        ventana_inicio_reduccion.mainloop()
                    
                    else:
                        pass

                    lista_informacion_calculada = []

                    for arista in aristas:

                        # Mostramos mensaje indicando qué poli-reducción ha sido completada
                        if Controlador.get_unica_instancia().get_poli_reduccion_completada(arista):
                            lista_texto = []
                            texto = "Poli-reducción "
                            lista_texto.append(texto)
                            

                            texto =  " ya realizada. \n\n Resetea las poli-reducciones para \npoder volver a realizarla."
                            lista_texto.append(texto)

                            nombre_nodos_fin = [Controlador.get_unica_instancia().get_arista_nombre_src(arista), Controlador.get_unica_instancia().get_arista_nombre_dest(arista)]

                            ventana_fin_reduccion = self.crear_ventana_inicio_fin_simulacion(None, None, lista_texto, nombre_nodos_fin, True)
                            ventana_fin_reduccion.resizable(0,0)
                            ventana_fin_reduccion.mainloop() 
                            
                        else:
                            
                            # Lanzamos ventana/interfaz de la poli-reducción
                            RepertorioInterfacesPoliReduccion.get_unica_instancia(self.ventana).lanzar_interfaz_poli_reduccion(arista, lista_informacion_calculada)
                            

                            # Guardamos la información que ha calculado la poli-reducción (en caso de que la necesite la siguiente poli-reducción a realizar)
                            lista_informacion_calculada = Controlador.get_unica_instancia().get_lista_informacion_calculada_arista(arista)

                            if Controlador.get_unica_instancia().get_poli_reduccion_completada(arista):

                                # Informamos de la poli-reducción realizada hasta ahora:
                                lista_texto = []
                                texto = "Poli-reducción "
                                lista_texto.append(texto)

                                texto =  " realizada. \n\n La poli-reducción se va a actualizar en el universo \nde problemas del simulador de la siguiente manera: "
                                lista_texto.append(texto)

                                nombre_nodos_fin = [Controlador.get_unica_instancia().get_arista_nombre_src(arista), Controlador.get_unica_instancia().get_arista_nombre_dest(arista)]

                                ventana_fin_reduccion = self.crear_ventana_inicio_fin_simulacion(None, None, lista_texto, nombre_nodos_fin, False)
                                ventana_fin_reduccion.resizable(0,0)
                                ventana_fin_reduccion.mainloop()

                                # Actualizamos grafo principal de la aplicación para mostrar la arista que 
                                # representa la poli-reducción realizada hasta ahora:
                                nueva_arista = [Controlador.get_unica_instancia().get_arista_id_src(arista),
                                                Controlador.get_unica_instancia().get_arista_id_dest(arista)]

                                if nueva_arista not in Controlador.get_unica_instancia().get_aristas_a_actualizar():
                                    Controlador.get_unica_instancia().anadir_aristas_a_actualizar(nueva_arista)
                        
                                self.actualizar_grafo(Controlador.get_unica_instancia().get_aristas_a_actualizar()) 

                    # Actualizamos contador de simulaciones en marchar. Lo ponemos a 0
                    Controlador.get_unica_instancia().set_num_simulaciones(0)

    
    # Crea una ventana para informar del fin de la simulación y 
    # de la actualización del universo de problemas del simulador.
    def crear_ventana_inicio_fin_simulacion(self, texto, nombre_nodos_inicio, lista_texto, nombre_nodos_fin, realizada):

        ventana_fin_reduccion = VentanaSecundaria(ventana_padre=self.ventana)
        ventana_fin_reduccion.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

        panel = ctk.CTkFrame(ventana_fin_reduccion, corner_radius=0)
        panel.pack()

        ventana_fin_reduccion.title("Info")

        # Imagen info
        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info.png"), size=(50, 50))
        label = ctk.CTkLabel(panel, image=bg_image, text="")
        label.pack(padx=10, pady=10)

        if texto != None:
            lbl = ctk.CTkLabel(panel, text=texto, font=ctk.CTkFont(size=14, weight="bold"))
            lbl.pack(padx=10, pady=10)

        # Caso inicio de la poli-reducción
        if nombre_nodos_inicio != None:
            alias_nodo = ""
            color_nodo = ""

            fila = 0

            for i in range(0, len(nombre_nodos_inicio)-1):
                
                panel_1 = ctk.CTkFrame(panel, corner_radius=0, fg_color = ("#BDC1C5", "gray50"))
                panel_1.pack(padx=10, pady=10)

                alias_nodo = Controlador.get_unica_instancia().get_alias_nodo_por_nombre(nombre_nodos_inicio[i])
                color_nodo = Controlador.get_unica_instancia().get_color_nodo_por_nombre(nombre_nodos_inicio[i])

                lbl = ctk.CTkLabel(panel_1, text=" " + alias_nodo + " ", bg_color = color_nodo, text_color="#F7F8F9")
                lbl.grid(row=fila, column=0, padx=10, pady=10)
                
                bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/flecha_izqda_negra.png"), size=(40, 40))
                label = ctk.CTkLabel(panel_1, image=bg_image, text="")
                label.grid(row=fila,column=1, padx=10, pady=10)

                alias_nodo = Controlador.get_unica_instancia().get_alias_nodo_por_nombre(nombre_nodos_inicio[i+1])
                color_nodo = Controlador.get_unica_instancia().get_color_nodo_por_nombre(nombre_nodos_inicio[i+1])

                lbl = ctk.CTkLabel(panel_1, text=" " + alias_nodo + " ", bg_color = color_nodo, text_color="#F7F8F9")
                lbl.grid(row=fila, column=2, padx=10, pady=10)

                fila += 1
        
        # Caso fin de la poli-reducción
        if lista_texto != None:
            
            lbl = ctk.CTkLabel(panel, text=lista_texto[0], font=ctk.CTkFont(size=14,weight="bold"))
            lbl.pack(padx=10, pady=0)

            panel_1 = panel_1 = ctk.CTkFrame(panel, corner_radius=0, fg_color = ("#BDC1C5", "gray50"))
            panel_1.pack(padx=10, pady=10)

            alias_nodo_1 = Controlador.get_unica_instancia().get_alias_nodo_por_nombre(nombre_nodos_fin[0])
            color_nodo_1 = Controlador.get_unica_instancia().get_color_nodo_por_nombre(nombre_nodos_fin[0])

            if not realizada:
                lbl = ctk.CTkLabel(panel_1, text=" " + alias_nodo_1 + " ", bg_color = color_nodo_1, text_color="#F7F8F9")
                lbl.grid(row=0, column=0, padx=10, pady=10)

                bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/flecha_izqda_negra.png"), size=(40, 40))
                label = ctk.CTkLabel(panel_1, image=bg_image, text="")
                label.grid(row=0, column=1, padx=10, pady=10)
                
            alias_nodo_2 = Controlador.get_unica_instancia().get_alias_nodo_por_nombre(nombre_nodos_fin[1])
            color_nodo_2 = Controlador.get_unica_instancia().get_color_nodo_por_nombre(nombre_nodos_fin[1])

            if not realizada:
                lbl = ctk.CTkLabel(panel_1, text=" " + alias_nodo_2 + " ", bg_color = color_nodo_2, text_color="#F7F8F9")
                lbl.grid(row=0, column=2, padx=10, pady=10)

            lbl = ctk.CTkLabel(panel, text=lista_texto[1], font=ctk.CTkFont(size=14,weight="bold"))
            lbl.pack(padx=10,pady=0)
     
            if not realizada:
                # Actualización del universo
                panel_1 = ctk.CTkFrame(panel, corner_radius=0, fg_color = ("#BDC1C5", "gray50"))
                panel_1.pack(padx=10, pady=10)

            lbl = ctk.CTkLabel(panel_1, text=" " + alias_nodo_1 + " ", bg_color = color_nodo_1, text_color="#F7F8F9")
            lbl.grid(row=0, column=0, padx=10, pady=10)

            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/flecha_izqda_naranja.png"), size=(40, 40))
            label = ctk.CTkLabel(panel_1, image=bg_image, text="")
            label.grid(row=0,column=1, padx=10, pady=10)
                
            lbl = ctk.CTkLabel(panel_1, text=" " + alias_nodo_2 + " ", bg_color = color_nodo_2, text_color="#F7F8F9")
            lbl.grid(row=0, column=2, padx=10, pady=10)

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_fin_reduccion.exit())
        boton_aceptar.pack(padx=10, pady=10)

        ventana_fin_reduccion.center()

        return ventana_fin_reduccion
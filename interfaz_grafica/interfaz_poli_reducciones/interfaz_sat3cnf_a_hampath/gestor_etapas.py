from .etapa_0 import *
from .etapa_1 import *
from .etapa_2 import *
from .etapa_3 import *
from .etapa_4 import *
from .etapa_5 import *
from .etapa_6 import *

from interfaz_grafica.interfaz_app.ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from controlador.controlador import Controlador

############################################################################
# Clase gestora de etapas de la poli-reducción SAT3cnf a HAMPATH.
# Se encarga de la gestión y de la comunicación entre las distintas etapas 
# a desarrollar en la poli-reducción. Además, engloba el uso de funciones
# comunes a todas las etapas a realizar.
############################################################################
class GestorEtapas():

    def __init__(self, ventana):

        # Ventana sobre la que se lanzará la ventana
        # de la poli-reducción
        self.ventana = ventana

        # Etapa 0
        self.etapa_0 = Etapa0(ventana, self)

        # Etapa 1
        self.etapa_1 = Etapa1(ventana, self)

        # Etapa 2
        self.etapa_2 = Etapa2(ventana, self)

        # Etapa 3
        self.etapa_3 = Etapa3(ventana, self)

        # Etapa 4
        self.etapa_4 = Etapa4(ventana, self)

        # Etapa 5
        self.etapa_5 = Etapa5(ventana, self)

        # Etapa 6
        self.etapa_6 = Etapa6(ventana, self)

        self.formula_booleana = None
        self.lista_informacion_calculada = [None, None, None, None, None]

    ### Getters y setters ###

    def anadir_a_lista_informacion_calculada(self, item, pos):

        self.lista_informacion_calculada[pos] = item

    def get_formula(self):
        return self.formula_booleana.get_formula_booleana()

    def set_formula(self, formula):
        self.formula_booleana = formula
    
    def get_formula_correcta(self):
        return self.formula_booleana.get_formula_correcta()

    def get_literales_formula(self):
        return self.formula_booleana.get_cjto_literales()
    
    def get_clausulas_formula(self):
        return self.formula_booleana.get_clausulas()
    
    def get_num_literales_formula(self):
        return self.formula_booleana.get_num_literales()
    
    def get_num_formulas_introducidas(self):
        return self.formula_booleana.get_num_formulas_introducidas()
    
    def get_num_clausulas_formula(self):
        return self.formula_booleana.get_num_clausulas()

    def set_num_formulas_introducidas(self, valor):
        self.formula_booleana.num_formulas_introducidas -= valor
    
    def formula_satisfacible(self):
        return self.formula_booleana.es_satisfacible()

    def get_etapa(self, num_etapa):

        match num_etapa:
            
            case 0:
                return self.etapa_0
            
            case 1:
                return self.etapa_1

            case 2:
                return self.etapa_2

            case 3:
                return self.etapa_3

            case 4:
                return self.etapa_4
            
            case 5:
                return self.etapa_5
    
    # Reseteo de etapas.
    def resetear_etapas(self):

        #self.etapa_0.set_etapa_realizada(False)
        self.etapa_1.set_etapa_realizada(False)
        self.etapa_2.set_etapa_realizada(False)
        self.etapa_3.set_etapa_realizada(False)
        self.etapa_4.set_etapa_realizada(False)
        self.etapa_5.set_etapa_realizada(False)
        self.etapa_5.set_etapa_realizada_5_1(False)
        self.etapa_5.resetear_panel_5_1()
        self.etapa_5.set_etapa_realizada_5_2(False)
        self.etapa_5.set_etapa_realizada_5_3(False)
        self.etapa_6.set_etapa_realizada(False)

    ### Métodos comunes a todas las etapas ###

    # Función que vuelve a la etapa anterior en la poli-reducción.
    def anterior(self, etapa):
        match etapa:
            
            # Volvemos al panel HAMPATH es NP
            case 0.1: 

                # Olvidamos paneles siguientes
                self.etapa_0.get_panel_0_2().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_0.get_panel_0_1().pack(padx=10, pady=10, fill="both", expand=True)

            # Volvemos al panel de introducción de fórmula
            case 0.2:

                # Olvidamos paneles siguientes
                self.etapa_1.get_panel_1().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_0.get_panel_0_2().pack(padx=10, pady=10, fill="both", expand=True)
               
            case 1:
                
                # Olvidamos paneles siguientes
                self.etapa_2.get_panel_2().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_1.get_panel_1().pack(fill="both", expand=True)
            
            case 2:

                # Olvidamos paneles siguientes
                self.etapa_3.get_panel_3().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_2.get_panel_2().pack(fill="both", expand=True)
            
            case 3:
                
                # Olvidamos paneles siguientes
                self.etapa_4.get_panel_4().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_3.get_panel_3().pack(fill="both", expand=True)
            
            case 4:

                # Olvidamos paneles siguientes
                self.etapa_5.get_panel_5().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_4.get_panel_4().pack(fill="both", expand=True)
            
            case 5:

                if self.etapa_6.get_panel_6() != None and self.etapa_5.get_panel_5_1() == None:
                    self.etapa_6.get_panel_6().pack_forget()

                    self.etapa_5.get_panel_5().pack(fill="both", expand=True)
                
                else:
                    # Olvidamos paneles siguientes
                    self.etapa_5.get_panel_5_1().pack_forget()

                    # Mostramos paneles anteriores
                    self.etapa_5.get_panel_5().pack(fill="both", expand=True)
            
            case 5.1:

                # Olvidamos paneles siguientes
                self.etapa_5.get_panel_5_2().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_5.get_panel_5_1().pack(fill="both", expand=True)
            
            case 5.2:

                # Olvidamos paneles siguientes
                self.etapa_5.get_panel_5_3().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_5.get_panel_5_2().pack(fill="both", expand=True)
            
            case 5.3:

                # Olvidamos paneles siguientes
                self.etapa_6.get_panel_6().pack_forget()

                # Mostramos paneles anteriores
                self.etapa_5.get_panel_5_3().pack(fill="both", expand=True)
            
    # Función que vuelve a la etapa siguiente en la poli-reducción.
    def siguiente(self, etapa):
        match etapa:

            case 0.1: 
                self.etapa_0.get_panel_0_0().pack_forget()
                
                self.etapa_0.lanzar_subetapa_1()

            case 0.2:
                self.etapa_0.get_panel_0_1().pack_forget()
                
                if self.etapa_0.get_etapa_realizada():
                    self.etapa_0.get_panel_0_2().pack(padx=10, pady=10, fill="both", expand=True)
                    
                else:
                    self.etapa_0.lanzar_subetapa_2()

            case 1:

                self.etapa_1.lanzar_etapa()

            case 2:

                self.etapa_1.get_panel_1().pack_forget()

                if self.etapa_2.get_etapa_realizada():
                    self.etapa_2.get_panel_2().pack(fill="both", expand=True)

                else:
                    self.etapa_2.lanzar_etapa()

            case 3:
                
                self.etapa_2.get_panel_2().pack_forget()

                if self.etapa_3.get_etapa_realizada():
                    self.etapa_3.get_panel_3().pack(fill="both", expand=True)

                else:
                    self.etapa_3.lanzar_etapa()

            case 4: 

                self.etapa_3.get_panel_3().pack_forget()

                if self.etapa_4.get_etapa_realizada():
                    self.etapa_4.get_panel_4().pack(fill="both", expand=True)

                else:
                    self.etapa_4.lanzar_etapa()
            
            case 5:
                self.etapa_4.get_panel_4().pack_forget()

                if self.etapa_5.get_etapa_realizada():
                    self.etapa_5.get_panel_5().pack(fill="both", expand=True)

                else:
                    self.etapa_5.lanzar_subetapa_0()
            
            case 5.1:
                self.etapa_5.get_panel_5().pack_forget()

                if self.etapa_5.get_etapa_realizada_5_1():
                    self.etapa_5.get_panel_5_1().pack(fill="both", expand=True)

                else:
                    self.etapa_5.lanzar_subetapa_1()
            
            case 5.2:
                self.etapa_5.get_panel_5_1().pack_forget()

                if self.etapa_5.get_etapa_realizada_5_2():
                    self.etapa_5.get_panel_5_2().pack(fill="both", expand=True)

                else:
                    self.etapa_5.lanzar_subetapa_2()
            
            case 5.3:
                self.etapa_5.get_panel_5_2().pack_forget()

                if self.etapa_5.get_etapa_realizada_5_3():
                    self.etapa_5.get_panel_5_3().pack(fill="both", expand=True)

                else:
                    self.etapa_5.lanzar_subetapa_3()
            
            case 6:

                satisfacible, _ = self.formula_satisfacible()
                if not satisfacible:
                    self.etapa_5.get_panel_5().pack_forget()

                else:
                    self.etapa_5.get_panel_5_3().pack_forget()

                if self.etapa_6.get_etapa_realizada():
                    self.etapa_6.get_panel_6().pack(padx=10, pady=10, fill="both", expand=True)

                else:
                    self.etapa_6.lanzar_etapa()

            # Terminamos de realizar la poli-reducción
            case 7:
                
                self.cerrar_simulacion()

    # Crea un panel con los datos de la fórmula introducida.
    def crear_panel_datos_introducidos(self, panel):

        panel_info = ctk.CTkTabview(panel, height=50, width=200)
        panel_info.pack(side="top")
        panel_info.add("Fórmula ϕ")
        panel_info.add("Num cláusulas")
        panel_info.add("Literales")
        panel_info.add("Num literales")

        label = ctk.CTkLabel(panel_info.tab("Fórmula ϕ"), text = f'{self.get_formula()}')
        label.pack(fill="both")

        label = ctk.CTkLabel(panel_info.tab("Num cláusulas"), text = str(self.get_num_clausulas_formula()))
        label.pack(fill="both")

        label = ctk.CTkLabel(panel_info.tab("Literales"), text = str(sorted(self.get_literales_formula())))
        label.pack(fill="both")

        label = ctk.CTkLabel(panel_info.tab("Num literales"), text = f'{self.get_num_literales_formula()}')
        label.pack(fill="both")
    
    # Crea un panel con pseudocódigo, explicando los pasos a nivel
    # algorítmico de qué es lo que hay que realizar. Texto alineado 
    # a la izquierda.
    def crear_panel_pseudocodigo(self, panel, altura, anchura, num_pasos, lista_texto):

        panel_pasos = ctk.CTkTabview(panel, height=altura, width=anchura)
        panel_pasos.pack(side="top", padx=10, pady=10, fill="both")

        for paso in range (1, num_pasos+1):
            panel_pasos.add("Paso " + str(paso) + "º")

            textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=460, height=300)
            textbox.insert("1.0", lista_texto[paso-1])
            textbox.configure(state="disabled")
            textbox.pack(padx=5, pady=10)

    # Crea un panel con los datos de los pasos que se han realizado.
    def crear_panel_informacion(self, panel, altura, anchura, num_pasos, lista_texto, mostrar_sol, mostrar_formula, num_etapa):

        if num_etapa != None:
            panel = ctk.CTkFrame(panel)
            panel.pack(padx=10, pady=(10,0))

            canvas = tk.Canvas(panel, width=40, height=185)
            canvas.configure(bg='#63BCE9')
            canvas.pack(side="left", padx=(10,0), pady=10)
            canvas.create_text(20, 150, text="Etapa " + str(num_etapa), angle=90, anchor="w", font = ('Arial', 15,'bold'))

        if mostrar_formula:
            self.crear_panel_datos_introducidos(panel)

        # Para mostrar la solución que halla el solver dpll para la fórmula booleana introducida
        if mostrar_sol:
            panel_valores = ctk.CTkFrame(panel, border_color="#4F769D", border_width=3)
            panel_valores.pack(padx=10, pady=(10,30))
            cadena_valor_literales = "La fórmula booleana ϕ es satisfacible para los siguientes valores: \n\n"
            for literal, valor_literal in self.etapa_5.get_lista_valores_literales():
                if valor_literal:
                    valor_literal = "Verdadero"
                else: 
                    valor_literal = "Falso"
                cadena_valor_literales += literal + " = " + str(valor_literal) + "\n"
            label = ctk.CTkLabel(panel_valores, text=cadena_valor_literales)
            label.pack(padx=10, pady=10)

        panel_pasos = ctk.CTkTabview(panel, height=altura, width=anchura)
        panel_pasos.pack(side="top", padx=10, pady=10, fill="both")

        for paso in range (1, num_pasos+1):
            panel_pasos.add("Paso " + str(paso) + "º")

            if paso == 2 and str(num_etapa) == "5.1":
                textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=370, height=150)
        
                textbox.insert("1.0", lista_texto[paso-1])
                textbox.configure(state="disabled")
                textbox.pack(padx=10, pady=10)

            elif paso != 4:
                label = ctk.CTkLabel(panel_pasos.tab("Paso " + str(paso) + "º"), text = lista_texto[paso-1])
                label.pack(fill="both")

            else:
                textbox = ctk.CTkTextbox(panel_pasos.tab("Paso " + str(paso) + "º"), width=370, height= 150)
        
                textbox.insert("1.0", lista_texto[paso-1])
                textbox.configure(state="disabled")
                textbox.pack(padx=10, pady=10)


    # Función que se encargar de guardar un grafo en una imagen.
    def guardar_imagen(self, figure, etapa):

        archivo = "reduccion_SAT3cnf_a_Hampath_grafo_" + str(etapa) + ".png"
        figure.savefig(archivo, dpi=800, bbox_inches = 'tight')

        ventana = VentanaPopUp(self.ventana)
        ventana.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana.title("Grafo guardado")

        panel = ctk.CTkFrame(ventana, corner_radius=0)
        panel.pack(fill="both", expand=True)

        label = ctk.CTkLabel(panel,text="Imagen guardada en el archivo : \n\n" + archivo)
        label.pack(side="top", padx=10, pady=10)

        boton = ctk.CTkButton(panel,text="Aceptar",command=lambda:ventana.exit())
        boton.pack(side="bottom", padx=10, pady=10)

        ventana.center()

    # Función que abre una nueva ventana en la que ver más grande en grafo pasado por parámetro. 
    def agrandar_grafo(self, figure, etapa):
        
        # Reestablecemos dpi
        figure.set_dpi(100)

        # Aumentamos tamaño del grafo
        figure.set_figwidth(8)
        figure.set_figheight(6.5)

        # Creamos ventana
        ventana = VentanaPopUp(self.ventana)
        ventana.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana.title("Ampliar/guardar grafo")

        panel = ctk.CTkFrame(ventana, corner_radius=0)
        panel.pack(side="left",fill="both", expand=True)
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        # Botones para guardar/cerrar
        boton = ctk.CTkButton(panel,text="Guardar imagen", command=lambda:self.guardar_imagen(figure,etapa))
        boton.grid(row=0, column=0, padx=10, pady=20, sticky="nswe")

        boton = ctk.CTkButton(panel, text="Cerrar", fg_color="red", hover_color="#D22121", command=lambda:ventana.exit(), height=50)
        boton.grid(row=1, column=0, padx=10, pady=(0,20), sticky="nswe")

        # Representamos el grafo
        canvas = FigureCanvasTkAgg(figure, ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ventana.center()

    # Cierra la poli-reducción y la termina, indicando que se ha realizado.
    # Guardamos la información calculada durante la poli-reducción, por si 
    # la necesita la poli-reducción siguiente.
    def cerrar_simulacion(self):

        # Guardamos la información calculada en la poli-reducción
        for item in self.lista_informacion_calculada:
            Controlador.get_unica_instancia().anadir_a_lista_informacion_calculada_arista("SAT3cnf->HAMPATH", item)

        # Activamos flag indicando que se ha realizado la poli-reducción
        Controlador.get_unica_instancia().get_arista("SAT3cnf->HAMPATH").set_poli_reduccion_completada(True)

        self.ventana.exit()
import tkinter as tk
import customtkinter as ctk
import sys
from PIL import Image
import qrcode
import qrcode.image.svg
import subprocess
from os import listdir
from os.path import isfile, join

from ..ventanas.ventanas_hijas.ventana_pop_up import VentanaPopUp

from modulos_externos.formula_booleana_sat3cnf.formula_booleana_sat3cnf import FormulaBooleanaSat3cnf

from .panel_repertorio_problemas import PanelRepertorioProblemasNp
from .panel_ayuda import PanelAyuda

from controlador.controlador import Controlador

#################################################
# Clase que contiene el panel menú del simulador. 
#################################################
class PanelMenu():

    # Constructor.
    def __init__(self, ventana=None, panel_principal=None):

        self.ventana = ventana
        self.panel_principal = panel_principal
        self.panel_repertorio = None
        self.panel_ayuda = None

        self.formula = None

        self.lista_frames = []

        self.crear_panel_menu()
    
    # Establece el panel principal de la app.
    def set_panel_principal(self, panel_principal):

        self.panel_principal = panel_principal
        self.lista_frames.append(panel_principal)

    # Crea el panel izquierdo de la aplicación, que contiene el menú de esta.
    def crear_panel_menu(self):

        panel_menu = ctk.CTkFrame(self.ventana, width=150, corner_radius=0, fg_color=("#4d77c3","#244C70"))
        panel_menu.grid_rowconfigure(7, weight=1)
        panel_menu.pack(side="left", fill="both", expand=False)

        # Fondo
        imagen_fondo = ctk.CTkImage(Image.open(("interfaz_grafica/interfaz_app/img/fondo_menu.jpg")), size=(300, 800))

        lbl = ctk.CTkLabel(panel_menu, text= "", image=imagen_fondo)
        lbl.img = imagen_fondo  # Keep a reference in case this code put is in a function.
        lbl.place(x=0, y=0, relwidth=1, relheight=1)

        logo_label = ctk.CTkLabel(panel_menu, text="Menú", font=ctk.CTkFont(size=20, weight="bold"),
                                fg_color="#244C70", text_color="#FFFFFF")
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Creación de botones de selección de menú
        boton_imagen = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/home.png"), size=(25, 25))
        boton_home = ctk.CTkButton(panel_menu, text="Inicio", fg_color=("#CAD4DC","#505152"), hover_color=("#B6BFC6", "#5E6061"), 
                                    text_color=("#000000","#FFFFFF"), command=lambda:self.volver_a_home(),
                                    image=boton_imagen, width=200)
        boton_home.grid(row=1, column=0, padx=20, pady=10)

        boton_imagen = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/lupa.png"), size=(25, 25))
        boton_repertorio = ctk.CTkButton(panel_menu, text="Repertorio de problemas", fg_color=("#CAD4DC","#505152"), hover_color=("#B6BFC6", "#5E6061"),
                                    text_color=("#000000","#FFFFFF"), command=lambda:self.mostrar_repertorio_problemas_np(),
                                    image=boton_imagen, width=200)
        boton_repertorio.grid(row=2, column=0, padx=20, pady=10) ##7DABD8 #6C9AC8

        boton_imagen = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/help.png"), size=(25, 25))
        boton_ayuda = ctk.CTkButton(panel_menu, text="Ayuda", fg_color=("#CAD4DC","#505152"), hover_color=("#B6BFC6", "#5E6061"),
                                    text_color=("#000000","#FFFFFF"), command=lambda:self.mostrar_panel_ayuda(),
                                    image=boton_imagen, width=200)
        boton_ayuda.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        appearance_mode_label = ctk.CTkLabel(panel_menu, text="Tema de la aplicación:", anchor="w",
                                    fg_color="#1C4062", text_color="#FFFFFF",)
        appearance_mode_label.grid(row=4, column=0, padx=20, pady=(29, 0))
        appearance_mode_optionemenu = ctk.CTkOptionMenu(panel_menu, text_color=("#000000","#FFFFFF"),
                                                        fg_color=("#CAD4DC","#505152"),
                                                        values=["Claro", "Oscuro"],
                                                        button_color=("#AFB5BB","#797B7D"),
                                                        button_hover_color = ("#B6BFC6", "#5E6061"),
                                                        command=self.cambiar_modo_app)
        appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/logo.png"), size=(180, 190))
        bg_image_label = ctk.CTkLabel(panel_menu, text="", image=bg_image)
        bg_image_label.grid(row=6, column=0, padx=30, pady=(20, 0))

        boton_imagen = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/mas.png"), size=(25, 25))

        boton_mas = ctk.CTkButton(panel_menu, text="Más", fg_color="#D18F13", hover_color="#E9A423",
                                    bg_color = "#263b5b",
                                    text_color=("#000000","#FFFFFF"), command=lambda:self.mostrar_menu_mas(),
                                    image=boton_imagen, width=100)
        boton_mas.grid(row=7, column=0, padx=20)

        boton_salir = ctk.CTkButton(panel_menu, text="Salir", fg_color="red", hover_color="#D22121",
                                     bg_color="#263b5b", command=lambda:exit())
        boton_salir.grid(row=8, column=0, padx=20, pady=20)
    
    # Menú con distintas opciones a ejecutar.
    def mostrar_menu_mas(self):

        ventana_menu_mas = VentanaPopUp(self.ventana)

        ventana_menu_mas.geometry("")
        ventana_menu_mas.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_menu_mas.title("Menú MÁS")
        ventana_menu_mas.resizable(1,1)

        label = ctk.CTkLabel(ventana_menu_mas, fg_color=("#A3B5CC","gray20"), text="Selecciona qué quieres realizar:",
                                font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(padx=10, pady=10, side="top", fill=ctk.X)

        panel_izqdo = ctk.CTkFrame(ventana_menu_mas)
        panel_izqdo.pack(fill="both", expand="True", padx=10, pady=10, side="left")

        boton_cook_levin = ctk.CTkButton(panel_izqdo, text="Reducción Cook-Levin", fg_color="#D79E12", hover_color="#F0B72D",
                                        width=200, command=lambda:self.mostrar_ventana_cook_levin(ventana_menu_mas))
        boton_cook_levin.pack(padx=10, pady=10)

        panel_derecho = ctk.CTkFrame(ventana_menu_mas)
        panel_derecho.pack(fill="both", expand="True", padx=(0,10), pady=10, side="right")

        boton_solver_dpll = ctk.CTkButton(panel_derecho, text="Usar solver DPLL para\n resolver fórmulas", fg_color=("#70AB94","#4D8871"), 
                                        hover_color=("#7FB9A2","#52987C"), width=200, command=lambda:self.mostrar_ventana_solver_sat(ventana_menu_mas))
        boton_solver_dpll.pack(padx=10, pady=10)

        ventana_menu_mas.center()

    #################################################
    ############### OPCIÓN COOK-LEVIN ###############
    #################################################

    # Lanza la opción de realizar la reducción Cook-Levin.
    def mostrar_ventana_cook_levin(self, ventana_menu_mas):

        ventana_menu_mas.destroy()

        ventana_cook_levin = VentanaPopUp(self.ventana)

        ventana_cook_levin.geometry("")
        ventana_cook_levin.configure(background="#9AA4B0")
        ventana_cook_levin.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        ventana_cook_levin.title("Reducción COOK-LEVIN")
        ventana_cook_levin.resizable(1,1)

        ficheros = [f for f in listdir("modulos_externos/reduccion_cook_levin/caso_de_uso/") if isfile(join("modulos_externos/reduccion_cook_levin/caso_de_uso/", f))]

        ficheros_entrada_cook_levin = ["------"]

        self.MT = ""
        self.palabra_introducida = ""
        for f in ficheros:
            if (".jff" in f or ".txt" in f):
                ficheros_entrada_cook_levin.append(f)

        panel_cook_levin = ctk.CTkFrame(ventana_cook_levin)
        panel_cook_levin.pack(fill="both", expand="True", padx=(10,10), pady=10, side="right")

        panel_cook_levin_1 = ctk.CTkFrame(panel_cook_levin)
        panel_cook_levin_1.pack(fill="both", expand="True", padx=(10,10), pady=10, side="top")


        # Creamos tabview para selección de MT
        panel_seleccion_1 = ctk.CTkTabview(panel_cook_levin_1, height=50, width=200)
        panel_seleccion_1.pack(padx=(10,10), pady=10, side="top",fill=ctk.X)
        panel_seleccion_1.add("1º: Selecciona la MT de entrada:")

        combobox = ctk.CTkComboBox(panel_seleccion_1.tab("1º: Selecciona la MT de entrada:"), values=ficheros_entrada_cook_levin, command=self.escoger_MT)
        combobox.pack(fill=ctk.X, padx=10, pady=10)

        # Creamos tabview para selección de palabra de entrada
        panel_seleccion_2 = ctk.CTkTabview(panel_cook_levin_1, height=50, width=200)
        panel_seleccion_2.pack(padx=(10,10), pady=10, side = "top",fill=ctk.X)
        panel_seleccion_2.add("2º: Escribe una palabra de entrada \nque reconoce la MT:")

        self.palabra = tk.StringVar()
        entry_formula = ctk.CTkEntry(panel_seleccion_2.tab("2º: Escribe una palabra de entrada \nque reconoce la MT:"), textvariable=self.palabra, width=150)
        entry_formula.pack(padx=10, pady=10, fill=ctk.X)

        boton_introducir = ctk.CTkButton(panel_seleccion_2.tab("2º: Escribe una palabra de entrada \nque reconoce la MT:"), text="Introducir", fg_color=("#70AB94","#4D8871"), hover_color=("#7FB9A2","#52987C"), 
                                            command=lambda:self.introducir_palabra())
        boton_introducir.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_cook_levin, text="Si se ha introducido la MT y la palabra de entrada, al pulsar el siguiente botón \nse lanzará en la terminal la reducción interactiva de Cook-Levin.",
                                font=ctk.CTkFont(size=12))
        label.pack(padx=10, pady=10, fill=ctk.X)

        boton_lanzar_reduccion = ctk.CTkButton(panel_cook_levin, text="Lanzar reducción", fg_color = "#15B6B9", hover_color="#1DD0D3", 
                                            command=lambda:self.lanzar_reduccion_cook_levin(ventana_cook_levin))
        boton_lanzar_reduccion.pack(padx=10, pady=10)

        label = ctk.CTkLabel(panel_cook_levin, text="NOTA: Antes de cerrar la aplicación general, asegúrate \n de haber cerrado la terminal de Cook-Levin con el comando \"q\".\n Lanza también una sola reducción Cook-Levin a la vez.",
                                font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(padx=10, pady=10, fill=ctk.X)

        ventana_cook_levin.center()

    # Método que comprueba que los datos son correctos. En caso de serlo, lanzará la reducción de Cook-Levin 
    # en la terminal.
    def lanzar_reduccion_cook_levin(self, ventana_cook_levin):

        # Caso no introducir MT
        if (self.MT == ""):
            ventana_error = VentanaPopUp(ventana_padre = self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel.pack()

            ventana_error.title("Error")

            # Imagen aviso
            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
            label = ctk.CTkLabel(panel, image=bg_image, text="")
            label.pack(padx=10, pady=10)

            lbl = ctk.CTkLabel(panel, text="Introduce una MT")
            lbl.pack(padx=10, pady=(0,10))

            boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.pack(padx=10, pady=(0,10))

            ventana_error.center()

        # Caso no intoducir palabra
        elif (self.palabra_introducida == ""):
            ventana_error = VentanaPopUp(ventana_padre = self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

            panel = ctk.CTkFrame(ventana_error, corner_radius = 0)
            panel.pack()

            ventana_error.title("Error")

            # Imagen aviso
            bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50, 50))
            label = ctk.CTkLabel(panel, image=bg_image, text="")
            label.pack(padx=10, pady=10)

            lbl = ctk.CTkLabel(panel, text="Introduce una palabra")
            lbl.pack(padx=10, pady=(0,10))

            boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.pack(padx=10, pady=(0,10))

            ventana_error.center()
        
        else:
            comando = "python modulos_externos/reduccion_cook_levin/main.py modulos_externos/reduccion_cook_levin/caso_de_uso/" + self.MT + " " + self.palabra_introducida
            subprocess.Popen(comando)
            ventana_cook_levin.destroy()

    def escoger_MT(self, MT : str):

        if MT != "------":
            self.MT = MT
    
    def introducir_palabra(self):
        self.palabra_introducida = f'{self.palabra.get()}'

        ventana_info = VentanaPopUp(ventana_padre = self.ventana)
        ventana_info.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')

        panel = ctk.CTkFrame(ventana_info, corner_radius = 0)
        panel.pack()

        ventana_info.title("Error")

        # Imagen info
        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info.png"), size=(50, 50))
        label = ctk.CTkLabel(panel, image=bg_image, text="")
        label.pack(padx=10, pady=10)

        lbl = ctk.CTkLabel(panel, text="Palabra \"" + self.palabra_introducida + "\" introducida")
        lbl.pack(padx=10, pady=(0,10))

        boton_aceptar = ctk.CTkButton(panel, text="Aceptar", command=lambda:ventana_info.exit())
        boton_aceptar.pack(padx=10, pady=(0,10))

        ventana_info.center()

    #############################################
    ############### OPCIÓN SOLVER ###############
    #############################################

    # Muestra una ventana en la que se podrá resolver fórmulas booleanas
    # en formato SAT3cnf y se podrá ver información sobre el solver
    # dpll.
    def mostrar_ventana_solver_sat(self, ventana_menu_mas):
        
        ventana_menu_mas.destroy()

        # Solo se podrá lanzar una ventana solver a la vez
        if Controlador.get_unica_instancia().get_num_simulaciones_solver() == 0:

            Controlador.get_unica_instancia().set_num_simulaciones_solver(1)

            ventana_solver = VentanaPopUp(self.ventana)

            ventana_solver.geometry("")
            ventana_solver.configure(background="#9AA4B0")
            ventana_solver.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_solver.title("Solver SAT3cnf")
            ventana_solver.resizable(1,1)
            ventana_solver.protocol("WM_DELETE_WINDOW", lambda:self.salir_solver(ventana_solver))

            label = ctk.CTkLabel(ventana_solver, fg_color=("#A3B5CC","gray20"), text="Solver DPLL para fórmulas booleanas en forma 3-cnf",
                                font=ctk.CTkFont(size=15, weight="bold"))
            label.pack(padx=10, pady=10, side="top", fill=ctk.X)

            panel_izqdo = ctk.CTkFrame(ventana_solver)
            panel_izqdo.pack(fill="both", expand="True", padx=10, pady=10, side="left")

            panel_derecho = ctk.CTkFrame(ventana_solver)
            panel_derecho.pack(fill="both", expand="True", padx=(0,10), pady=10, side="right")

            # Asignamos fórmula
            self.formula = FormulaBooleanaSat3cnf(ventana_solver, panel_izqdo, "")

            data = "https://es.wikipedia.org/wiki/Algoritmo_DPLL"
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save("interfaz_grafica/interfaz_app/img/qr_solver_dpll.png")

            # Mostramos imagen qr para más info
            im = Image.open("interfaz_grafica/interfaz_app/img/qr_solver_dpll.png")
            photo = ctk.CTkImage(im, size=(150,150))

            panel_qr = ctk.CTkFrame(panel_derecho)
            panel_qr.pack(side="top", padx=10, pady=(10,10),fill="both", expand=True)

            label = ctk.CTkLabel(panel_qr, text="Info sobre el solver DPLL:", font=ctk.CTkFont(size=13, weight="bold"))
            label.pack(side="top", padx=10, pady=10)

            label = ctk.CTkLabel(panel_qr, text="", image=photo)
            label.image = photo
            label.pack(padx=20, pady=(0,20))

            # Botón resolver fórmula
            boton_resolver = ctk.CTkButton(panel_derecho, text="Resolver fórmula", fg_color = "#15B6B9", 
                                        hover_color="#1DD0D3",
                                        width=200, command=lambda:self.resolver_formula())
            boton_resolver.pack(padx=10, pady=(100,10), side="bottom")

            ventana_solver.center()
        
        else:
            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius=0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info.png"), size=(50,50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text='Ya hay abierta una ventana para el solver')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()

    # Se encarga de llamar al método dpll para resolver la fórmula booleana.
    def resolver_formula(self):

        # Si no hay fórmula, mostramos mensaje de error
        if self.formula.get_formula_booleana() == "" or not self.formula.get_formula_correcta():
            ventana_error = VentanaPopUp(self.ventana)
            ventana_error.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_error.title(" ")

            panel_error = ctk.CTkFrame(ventana_error, corner_radius=0)
            panel_error.pack()

            # Imagen error
            imagen_error = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/error.png"), size=(50,50))
            label = ctk.CTkLabel(panel_error, image=imagen_error, text="")
            label.grid(row=0,column=0, padx=10, pady=10)

            label = ctk.CTkLabel(panel_error, text='Introduce una fórmula booleana correcta')
            label.grid(row=1, column=0, padx=10, pady=10)

            boton_aceptar = ctk.CTkButton(panel_error, text="Aceptar", command=lambda:ventana_error.exit())
            boton_aceptar.grid(row=2, column=0, padx=10, pady=10)

            ventana_error.center()
        
        # Mostramos solución
        else:
            ventana_solucion = VentanaPopUp(self.ventana)
            ventana_solucion.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
            ventana_solucion.title(" ")
            ventana_solucion.configure(background="#9AA4B0")

            satisfacible, literales = self.formula.es_satisfacible()

            # Si es satisfacible, mostramos valores
            if satisfacible:
                panel_valores = ctk.CTkFrame(ventana_solucion, border_color="#0F971B", border_width=3)
                panel_valores.pack(padx=10, pady=10, fill="both")

                cadena_valor_literales = "La fórmula ϕ es satisfacible \npara los siguientes valores: \n\n"
                for literal, valor_literal in literales:
                    if valor_literal:
                        valor_literal = "Verdadero"
                    else: 
                        valor_literal = "Falso"
                    cadena_valor_literales += literal + " = " + str(valor_literal) + "\n"
                label = ctk.CTkLabel(panel_valores, text=cadena_valor_literales)
                label.pack(padx=10, pady=10, fill="both")

                boton_aceptar = ctk.CTkButton(panel_valores, text="Aceptar", command=lambda:ventana_solucion.exit())
                boton_aceptar.pack(padx=10, pady=10)
            
            # Si no lo es, decimos que no es satisfacible
            else:
                panel_valores = ctk.CTkFrame(ventana_solucion, border_color="#B82811", border_width=3)
                panel_valores.pack(padx=10, pady=10, fill="both")
                label = ctk.CTkLabel(panel_valores, text = "La fórmula no es satisfacible.")
                label.pack(padx=10, pady=10, fill="both")

                boton_aceptar = ctk.CTkButton(panel_valores, text="Aceptar", command=lambda:ventana_solucion.exit())
                boton_aceptar.pack(padx=10, pady=10)
            
            ventana_solucion.center()
    
    # Sale del solver. Establece el flag que controla el número de 
    # ventanas solver abiertas a la vez a 0.
    def salir_solver(self, ventana):

        Controlador.get_unica_instancia().set_num_simulaciones_solver(0)
        ventana.exit()

    # Cierra ventana de la aplicación y sale exitosamente.
    def exit(self):

        self.ventana.destroy()
        sys.exit()

    # Función que oculta paneles, y permite permutar entre paneles.
    def ocultar_paneles(self):

        for i in self.lista_frames:
            self.lista_frames.remove(i)
            i.pack_forget()
    
    # Función que regresa al panel principal de la aplicación.
    def volver_a_home(self):

        self.ocultar_paneles()
        self.lista_frames.append(self.panel_principal)
        self.panel_principal.pack(fill='both', expand=1)

    # Función que muestra el panel del repertorio de problemas
    # que contiene el simulador.
    def mostrar_repertorio_problemas_np(self):

        self.ocultar_paneles()

        if self.panel_repertorio != None:
            self.panel_repertorio.pack(fill='both', expand=1)

        else:
            self.panel_repertorio = PanelRepertorioProblemasNp(ventana=self.ventana)
        
        self.lista_frames.append(self.panel_repertorio)

    # Función que muestra el panel ayuda de la aplicación.
    def mostrar_panel_ayuda(self):

        self.ocultar_paneles()

        if self.panel_ayuda != None:
            self.panel_ayuda.pack(fill='both', expand=1)
        else:
            self.panel_ayuda = PanelAyuda(ventana=self.ventana)

        self.lista_frames.append(self.panel_ayuda)

    # Función que cambia el modo de la aplicación.
    def cambiar_modo_app(self, nuevo_modo: str):

        if nuevo_modo == "Claro":
            nuevo_modo  = "Light"
            self.panel_principal.configure(fg_color="#98B3D0")

        else:
            nuevo_modo  = "Dark"
            self.panel_principal.configure(fg_color="gray10")

        ctk.set_appearance_mode(nuevo_modo)
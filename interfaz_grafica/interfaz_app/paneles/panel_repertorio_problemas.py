import tkinter as tk
import customtkinter as ctk
from PIL import Image

from .panel import Panel

from controlador.controlador import Controlador

###############################################
# Clase que muestra el panel de información de 
# los problemas que contiene la aplicación.
###############################################
class PanelRepertorioProblemasNp(Panel):
    
    # Constructor.
    def __init__(self, ventana=None):

        # Constructor del padre
        super().__init__(ventana)

        self.panel_info = None
        self.crear_panel_seleccion_problema_np()
    
    # Crea panel para seleccionar el problema sobre el que 
    # queremos ver información.
    def crear_panel_seleccion_problema_np(self):

        # Creamos panel superior
        panel_superior = ctk.CTkFrame(self, fg_color=("#6889B1","gray20"))
        panel_superior.pack(side="top", fill=tk.X, padx=150, pady=20)

        label = ctk.CTkLabel(panel_superior, fg_color=("#A3B5CC","gray25"), text="Información sobre problemas", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=40, pady=10, fill=tk.X)

        # Creamos tabview para selección de problema
        panel_seleccion = ctk.CTkTabview(panel_superior, height=50, width=250)
        panel_seleccion.pack(padx=20, pady=(0,10))
        panel_seleccion.add("Selecciona un problema")

        lista_valores = ["------"]
        for nombre_nodo in Controlador.get_unica_instancia().get_lista_nombres_nodos():              
            lista_valores.append(nombre_nodo)
        combobox = ctk.CTkComboBox(panel_seleccion.tab("Selecciona un problema"), values=lista_valores, command=self.mostrar_panel_repertorio_problemas_np)
        combobox.pack(fill=ctk.X, padx=5, pady=5, side="top")

    # Mostramos el repertorio de problemas que contiene nuestra aplicación.
    def mostrar_panel_repertorio_problemas_np(self, nombre_problema_np):

        if self.panel_info != None:
            self.panel_info.pack_forget()

        if nombre_problema_np != "------":

            self.panel_info = ctk.CTkFrame(self, fg_color = ("#6889B1","gray20"))
            self.panel_info.pack(fill="both", expand=True, padx=20, pady=(0,20))

            panel = ctk.CTkFrame(self.panel_info,fg_color=("#A3B5CC","gray25"))
            panel.pack(padx=10, pady=10, fill=tk.X)

            label = ctk.CTkLabel(panel, text=nombre_problema_np, font=ctk.CTkFont(size=15, weight="bold"))
            label.pack(padx=10)

            textbox = ctk.CTkTextbox(self.panel_info, width=365, height=350)
        
            textbox.pack(side='left', padx=30, pady=15,fill="both", expand=True)
            textbox.insert("1.0", Controlador.get_unica_instancia().get_texto_info_nodo(nombre_problema_np))
            textbox.configure(state="disabled")

            # Mostramos imagen qr para más info
            im = Image.open(Controlador.get_unica_instancia().get_img_qr_nodo(nombre_problema_np))
            photo = ctk.CTkImage(im, size=(200,200))

            panel_qr = ctk.CTkFrame(self.panel_info)
            panel_qr.pack(side="left", padx=10, pady=10,fill="both", expand=True)

            label = ctk.CTkLabel(panel_qr, text="Más info en:", font=ctk.CTkFont(size=13, weight="bold"))
            label.pack(side="top", padx=10, pady=(60,10))

            label = ctk.CTkLabel(panel_qr, text="", image=photo)
            label.image = photo
            label.pack(padx=20, pady=(0,20))
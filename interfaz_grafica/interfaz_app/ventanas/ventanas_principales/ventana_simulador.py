import tkinter as tk

from .ventana import Ventana
from ...paneles.panel_principal import PanelPrincipal
from ...paneles.panel_menu import PanelMenu

#########################################################
# Clase que contiene la ventana aplicación del simulador.
#########################################################
class VentanaSimulador(Ventana):

    # Constructor
    def __init__(self):

        # Creamos la ventana principal
        tk.Tk.__init__(self)
        
        # Ocultamos ventana mientras se cargan items de esta
        self.attributes('-alpha', 0.0)

        self.title('Simulador de reducciones polinómicas')
        self.iconbitmap('interfaz_grafica/interfaz_app/img/icono.ico')
        self.geometry("")

        # Creamos paneles menú y principal
        panel_menu = PanelMenu(ventana=self)
        panel_principal = PanelPrincipal(ventana=self)

        panel_menu.set_panel_principal(panel_principal)

        # Mostramos ventana solo cuando todos los paneles hayan sido cargados
        self.after(0, self.attributes, "-alpha", 1.0)
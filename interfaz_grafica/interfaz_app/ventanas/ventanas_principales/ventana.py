import tkinter as tk
from PIL import Image, ImageTk

import interfaz_grafica.interfaz_app.paneles as pn

#########################################
# Clase que representa una ventana simple.
# Hereda de tk.Tk
#########################################
class Ventana(tk.Tk):

    # Constructor.
    def __init__(self):

        # Constructor del padre
        super().__init__()
    
    # Función para centrar una ventana en la pantalla.
    def center(self):
        """
        https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        """
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.deiconify()
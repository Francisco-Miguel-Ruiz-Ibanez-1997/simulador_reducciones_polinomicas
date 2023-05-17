import tkinter as tk
from PIL import Image, ImageTk

from .ventana import Ventana

####################################################################
# Clase que representa la ventana de carga inicial de la aplicación.
####################################################################
class VentanaCarga(Ventana):

    # Constructor.
    def __init__(self):
        super().__init__()

        self.geometry("500x500")

        self.config(bg="#1F41A9")

        # Ocultamos panel de edición de ventana
        self.overrideredirect(True)

        # Cargamos archivo imagen gif
        archivo_imagen = Image.open("interfaz_grafica/interfaz_app/img/load.gif")
        self.frames = archivo_imagen.n_frames
        foto = ImageTk.PhotoImage(archivo_imagen)
        
        # Nuestra imagen será un gif, así que necesitamos mostrar distintos frames para mostrarla correctamente
        self.imagen = [tk.PhotoImage(file='interfaz_grafica/interfaz_app/img/load.gif', format='gif -index %i' %(i)) for i in range(self.frames)]
        
        # Aquí guardamos la animación del gif
        self.mostrarAnimacion = None

        # Fondo
        imagen_fondo = ImageTk.PhotoImage(Image.open(("interfaz_grafica/interfaz_app/img/fondo_carga.jpg")))

        lbl = tk.Label(self, image = imagen_fondo)
        lbl.img = imagen_fondo
        lbl.place(x=0, y=0, relwidth=1, relheight=1)

        lbl = tk.Label(self, text="\n Simulador de reduccciones \npolinómicas \n", bg ="#6F91C1",
                            fg="#FFFFFF", font=tk.font.Font(size=14, weight="bold"),
                            borderwidth=4, relief="sunken")
        lbl.pack(padx=10, pady=(60,20), side="top")

        lbl = tk.Label(self, text="Cargando ...", bg="#050c14", fg="#FFFFFF" )
        lbl.pack(padx=10, pady=(90,20), side="top")

        self.label = tk.Label(self, text=foto, width=80, height = 100)
        self.label.pack(padx=10, pady=(20,40), side="bottom")
        
    # Función que va calculando los distintos frames del gif, actualizando la imagen para 
    # mostrarla adecuadamente.
    def animacion(self, count, num_veces):

        nuevaImagen = self.imagen[count]
        self.label.configure(image=nuevaImagen)

        count += 1
        if count == self.frames:
            count = 0
    
        # num_veces: Variable auxiliar que empleamos para detener la animación antes de destruir la ventana de carga. Si nos pasamos,
        # paramos la animación.
        if num_veces < 45:
            num_veces += 1

            # Cada 50 ms se va actualizando la imagen gif
            self.mostrarAnimacion = self.after(50, lambda: self.animacion(count,num_veces))
        
        else:
            self.after_cancel(self.mostrarAnimacion)
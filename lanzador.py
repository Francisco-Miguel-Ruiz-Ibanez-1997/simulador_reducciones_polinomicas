# Lanzador de la aplicación.

import tkinter as tk
import ctypes

from interfaz_grafica.interfaz_app.ventanas.ventanas_principales.ventana_carga import VentanaCarga
from interfaz_grafica.interfaz_app.ventanas.ventanas_principales.ventana_simulador import VentanaSimulador

###### Método Principal ######
def main():
    
    # Pantallas de alta resolución
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # Creamos ventana de carga
    ventana = VentanaCarga()
    
    # Para la animación de carga
    ventana.animacion(0,num_veces=0)

    # Pasados 3000 ms, se destruye la ventana de carga y se muestra la de
    # la de la app
    ventana.after(3000,lambda:mostrar_app(ventana))

    ventana.center()
    tk.mainloop()

# Muestra la ventana de la aplicación del simulador en sí, destruyendo
# la ventana de carga.
def mostrar_app(ventana):

    # Destruimos la ventana de carga
    ventana.destroy()
    
    # Lanzamos el simulador  
    ventana_app = VentanaSimulador()

    ventana_app.center()

# Entry-point : función explícita que se llama cuando el archivo
# se ejecuta directamente a través de la consola.
if __name__ == '__main__':
    main()